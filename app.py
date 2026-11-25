"""Aplicación web de análisis financiero de Industrias Plásticas Altamira, S.A."""
import json
import os
from pathlib import Path
from urllib.parse import urlsplit

import markdown
from flask import Flask, abort, flash, redirect, render_template, request, send_file, url_for

from altamira import (ajustes, analisis, balanza, captura, catalogo, complementarios as comp, formato,
                      horizontal_vertical as hv, presentacion, razones, validaciones)
from altamira.repositorio import Repositorio

RAIZ = Path(__file__).resolve().parent
RUTA_BASE = RAIZ / "data" / "datos_base.json"
RUTA_ACTUAL = RAIZ / "data" / "datos_actuales.json"
RUTA_PUBLICADO = RAIZ / "data" / "publicado_2024.json"

MODULOS = [
    # (endpoint, número, título, descripción, ícono)
    ("captura_datos", 1, "Captura de datos", "Cuentas 2023–2025 y datos complementarios", "captura"),
    ("estado_resultados", 2, "Estado de resultados", "De ventas netas a utilidad por acción", "resultados"),
    ("balance_general", 3, "Balance general", "Comparativo y cierre de utilidades retenidas", "balance"),
    ("flujo_efectivo", 4, "Flujo de efectivo", "Método indirecto y flujo libre", "flujo"),
    ("razones_financieras", 5, "Razones financieras", "13 razones, semáforo y Du Pont", "razones"),
    ("analisis_hv", 6, "Horizontal y vertical", "Variaciones, estructura y gráficos", "analisis"),
    ("indicadores", 7, "Indicadores complementarios", "Escudo fiscal, calidad de utilidad y crédito", "indicadores"),
]

PESTANAS = {"2025": "Balanza 2025", "2024": "Estados 2024", "2023": "Balance 2023",
            "complementarios": "Datos complementarios"}

ETIQUETAS = {
    "acciones": "Acciones comunes en circulación", "valor_nominal": "Valor nominal por acción (US$)",
    "tasa_isr": "Tasa del impuesto sobre la renta (%)", "dias_anio": "Días del año comercial",
    "garrafones_unidades": "Garrafones vendidos en 2025 (unidades)",
    "garrafones_precio": "Precio por garrafón (US$)",
    "cubetas_unidades": "Cubetas vendidas en 2025 (unidades)", "cubetas_precio": "Precio por cubeta (US$)",
    "precio_accion": "Precio de mercado por acción (US$, opcional para P/U)",
}

CONCEPTOS_VALIDACION = {
    "ventas_netas": "Ventas netas", "costo_ventas": "Costo de ventas", "utilidad_bruta": "Utilidad bruta",
    "total_gastos_operacion": "Total gastos de operación", "uaii": "Utilidad de operación (UAII)",
    "uai": "Utilidad antes de impuestos", "isr": "Impuesto sobre la renta", "utilidad_neta": "Utilidad neta",
    "upa": "Utilidad por acción", "total_activo_circulante": "Total activos circulantes",
    "activos_fijos_netos": "Activos fijos netos", "total_activos": "Total activos",
    "total_pasivo_circulante": "Total pasivos circulantes", "total_pasivos": "Total pasivos",
    "total_capital": "Total capital contable", "total_pasivo_capital": "Total pasivos y capital",
    "total_operacion": "Flujo neto de operación", "total_inversion": "Flujo neto de inversión",
    "total_financiamiento": "Flujo neto de financiamiento", "cambio_neto": "Cambio neto en caja",
    "caja_inicial": "Caja inicial", "caja_final": "Caja final", "flujo_libre": "Flujo de efectivo libre",
}


def secciones(filas):
    """Agrupa los renglones por encabezado para mostrarlos como secciones colapsables."""
    grupos = []
    for fila in filas:
        if fila["tipo"] == "grupo":
            grupos.append({"titulo": fila["concepto"], "filas": [], "cuentas": 0})
        else:
            grupos[-1]["filas"].append(fila)
            grupos[-1]["cuentas"] += fila["tipo"] == "cuenta"
    return grupos


def secciones_captura(pestana, datos):
    """Cuentas de la pestaña agrupadas según la clasificación del catálogo."""
    saldos = balanza.saldos(datos["balanza_2025"])
    claves = datos["balanza_2025"] if pestana == "2025" else datos[f"cuentas_{pestana}"]
    grupos = []
    for seccion, titulo in catalogo.SECCIONES.items():
        filas = []
        for cuenta in catalogo.CATALOGO:
            if cuenta.seccion != seccion or cuenta.clave not in claves:
                continue
            fila = {"numero": cuenta.numero, "clave": cuenta.clave, "nombre": cuenta.nombre,
                    "naturaleza": cuenta.naturaleza}
            if pestana == "2025":
                fila.update(claves[cuenta.clave], saldo=saldos[cuenta.clave])
            else:
                fila["valor"] = claves[cuenta.clave]
            filas.append(fila)
        if filas:
            grupos.append({"titulo": titulo, "filas": filas})
    return grupos


def crear_app(ruta_actual=RUTA_ACTUAL, pruebas=False):
    app = Flask(__name__)
    # solo nombres locales: evita que un dominio ajeno apunte al sistema (DNS rebinding)
    app.config.update(TESTING=pruebas, SECRET_KEY=os.urandom(24), TRUSTED_HOSTS=["127.0.0.1", "localhost"])
    repo = Repositorio(RUTA_BASE, ruta_actual)
    publicado = json.loads(RUTA_PUBLICADO.read_text(encoding="utf-8"))

    app.jinja_env.filters.update(monto=formato.monto, usd=formato.usd, usd_accion=formato.usd_accion,
                                 pct=formato.porcentaje, medida=formato.medida)

    @app.before_request
    def rechazar_formularios_de_otro_sitio():
        """Protección CSRF: los cambios solo se aceptan desde las pantallas del propio sistema."""
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return
        origen = request.headers.get("Origin") or request.headers.get("Referer")
        if origen is not None and urlsplit(origen).netloc != request.host:
            abort(403)

    def actual():
        return analisis.construir(repo.cargar())

    def pagina(plantilla, a=None, **contexto):
        a = a or actual()
        validacion = analisis.validar_2024(a, publicado)
        return render_template(
            plantilla, a=a, modulos=MODULOS, alertas=validaciones.alertas(a), validacion=validacion,
            validacion_ok=all(f["ok"] for f in validacion),
            cuadra=all(bg["cuadra"] for bg in a.balances.values()),
            modificado=repo.modificado(), empresa="Industrias Plásticas Altamira, S.A.", **contexto)

    @app.get("/")
    def menu():
        a = actual()
        filas = razones.tabla(a)
        return pagina("menu.html", a, razones=filas, conceptos=CONCEPTOS_VALIDACION,
                      conteo={c: sum(f["semaforo_2025"] == c for f in filas)
                              for c in ("verde", "amarillo", "rojo", "gris")})

    @app.get("/captura")
    def captura_datos():
        pestana = request.args.get("pestana", "2025")
        if pestana not in PESTANAS:
            pestana = "2025"
        datos = repo.cargar()
        a = analisis.construir(datos)
        original = analisis.construir(repo.original())
        return pagina(
            "captura.html", a, pestana=pestana, pestanas=PESTANAS, datos=datos, etiquetas=ETIQUETAS,
            definiciones=razones.DEFINICIONES, cuentas=catalogo.CATALOGO,
            saldos=balanza.saldos(datos["balanza_2025"]), totales=balanza.totales(datos["balanza_2025"]),
            grupos=secciones_captura(pestana, datos) if pestana != "complementarios" else [],
            cambios=razones.cambios(original, a))

    @app.post("/captura")
    def guardar_captura():
        pestana = request.form.get("pestana", "2025")
        nuevos, errores = captura.aplicar(repo.cargar(), request.form)
        if errores:
            for error in errores:
                flash(error, "error")
        else:
            repo.guardar(nuevos)
            flash("Datos guardados. Todos los módulos se recalcularon.", "ok")
        return redirect(url_for("captura_datos", pestana=pestana))

    @app.post("/captura/ajuste")
    def ajustar_cuenta():
        try:
            texto = request.form.get("saldo", "")
            if not texto.strip():
                raise ValueError("Escriba el nuevo saldo de la cuenta.")
            try:
                saldo = captura.leer_numero(texto)
            except ValueError:
                raise ValueError(f"«{texto}» no es un monto válido.")
            nuevos = ajustes.modificar(repo.cargar(), request.form.get("cuenta", ""), saldo,
                                       request.form.get("contrapartida") or None)
        except ValueError as error:
            flash(str(error), "error")
        else:
            repo.guardar(nuevos)
            flash("Cuenta modificada. Todos los módulos se recalcularon.", "ok")
        return redirect(url_for("captura_datos"))

    @app.post("/restaurar")
    def restaurar():
        repo.restaurar()
        flash("Se restauraron los datos originales.", "ok")
        return redirect(url_for("captura_datos"))

    @app.get("/resultados")
    def estado_resultados():
        a = actual()
        return pagina("resultados.html", a, grupos=secciones(hv.resultados(a)))

    @app.get("/balance")
    def balance_general():
        a = actual()
        return pagina("balance.html", a,
                      grupos=secciones(presentacion.filas(presentacion.BALANCE_GENERAL,
                                                          {y: a.balances[y] for y in (2024, 2025)})))

    @app.get("/flujo")
    def flujo_efectivo():
        anio = 2024 if request.args.get("anio") == "2024" else 2025
        return pagina("flujo.html", anio=anio)

    @app.get("/razones")
    def razones_financieras():
        a = actual()
        filas = razones.tabla(a)
        return pagina("razones.html", a, filas=filas, categorias=razones.CATEGORIAS,
                      comentarios=razones.comentarios(a),
                      dupont={y: razones.du_pont(a, y) for y in (2024, 2025)})

    @app.get("/analisis")
    def analisis_hv():
        a = actual()
        return pagina("analisis_hv.html", a, horizontal={
            "Estado de resultados": secciones(hv.resultados(a)),
            "Balance general": secciones(hv.balance(a)),
        }, graficos=datos_graficos(a))

    @app.get("/complementarios")
    def indicadores():
        a = actual()
        return pagina("complementarios.html", a, escudo=comp.escudo_fiscal(a),
                      costo=comp.costo_despues_impuestos(a), acciones=comp.valor_por_accion(a),
                      ventas=comp.ventas_por_producto(a), calidad=comp.utilidad_vs_flujo(a),
                      dupont=comp.du_pont_descompuesto(a), credito=comp.politica_credito(a))

    @app.get("/manual")
    def manual():
        texto = (RAIZ / "docs" / "manual_usuario.md").read_text(encoding="utf-8")
        return pagina("manual.html", contenido=markdown.markdown(texto, extensions=["tables"]))

    @app.get("/manual.pdf")
    def manual_pdf():
        return send_file(RAIZ / "docs" / "manual_usuario.pdf", mimetype="application/pdf")

    return app


def datos_graficos(a):
    er, bg = a.resultados, a.balances
    anios = (2024, 2025)

    def serie(fuente, claves):
        return {str(y): [fuente[y][k] for k in claves] for y in anios}

    def estructura(partes, fuente, base):
        return [{"nombre": nombre,
                 "valores": [sum(fuente[y][k] for k in claves) / fuente[y][base] * 100 if fuente[y][base] else 0
                             for y in anios]} for nombre, claves in partes]

    return {
        "resultados": {"etiquetas": ["Ventas netas", "Costo de ventas", "Utilidad bruta",
                                     "Gastos de operación", "UAII", "Utilidad neta"],
                       **serie(er, ("ventas_netas", "costo_ventas", "utilidad_bruta",
                                    "total_gastos_operacion", "uaii", "utilidad_neta"))},
        "activos": estructura([("Activos circulantes", ["total_activo_circulante"]),
                               ("Activos fijos netos", ["activos_fijos_netos"]),
                               ("Otros activos", ["total_otros_activos"])], bg, "total_activos"),
        "financiamiento": estructura([("Pasivos circulantes", ["total_pasivo_circulante"]),
                                      ("Pasivos a largo plazo", ["total_pasivo_lp"]),
                                      ("Capital contable", ["total_capital"])], bg, "total_activos"),
        "margenes": {"etiquetas": ["Costo de ventas", "Utilidad bruta", "Gastos de operación", "UAII",
                                   "Gastos por intereses", "Utilidad neta"],
                     **{str(y): [er[y][k] / er[y]["ventas_netas"] * 100 if er[y]["ventas_netas"] else 0
                                 for k in ("costo_ventas", "utilidad_bruta", "total_gastos_operacion",
                                           "uaii", "gastos_intereses", "utilidad_neta")] for y in anios}},
    }


if __name__ == "__main__":
    crear_app().run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)))
