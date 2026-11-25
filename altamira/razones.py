"""Las 13 razones financieras, sistema Du Pont, semáforo y comentarios (capítulo 3).

Se usan saldos de fin de año, ventas netas como numerador de las rotaciones y
cuentas por cobrar netas de la estimación.
"""
from typing import NamedTuple

from .formato import medida

CATEGORIAS = {
    "rentabilidad": "Rentabilidad",
    "utilizacion_activos": "Utilización de activos",
    "liquidez": "Liquidez",
    "utilizacion_deudas": "Utilización de deudas",
}
TOLERANCIA_AMARILLO = 0.10


class Razon(NamedTuple):
    numero: int
    clave: str
    nombre: str
    categoria: str
    unidad: str   # porcentaje | veces | dias
    mejor: str    # mayor | menor
    formula: str


DEFINICIONES = [Razon(n, *fila) for n, fila in enumerate([
    ("margen_utilidad", "Margen de utilidad", "rentabilidad", "porcentaje", "mayor",
     "Utilidad neta ÷ Ventas netas"),
    ("roa", "Rendimiento sobre los activos (ROA)", "rentabilidad", "porcentaje", "mayor",
     "Utilidad neta ÷ Activos totales"),
    ("roe", "Rendimiento sobre el capital contable (ROE)", "rentabilidad", "porcentaje", "mayor",
     "Utilidad neta ÷ Capital contable"),
    ("rotacion_cxc", "Rotación de las cuentas por cobrar", "utilizacion_activos", "veces", "mayor",
     "Ventas netas ÷ Cuentas por cobrar netas"),
    ("ppc", "Periodo promedio de cobranza", "utilizacion_activos", "dias", "menor",
     "Cuentas por cobrar netas ÷ (Ventas netas ÷ 360)"),
    ("rotacion_inventario", "Rotación del inventario", "utilizacion_activos", "veces", "mayor",
     "Ventas netas ÷ Inventario"),
    ("rotacion_activos_fijos", "Rotación de los activos fijos", "utilizacion_activos", "veces", "mayor",
     "Ventas netas ÷ Activos fijos netos"),
    ("rotacion_activos_totales", "Rotación de los activos totales", "utilizacion_activos", "veces", "mayor",
     "Ventas netas ÷ Activos totales"),
    ("razon_circulante", "Razón circulante", "liquidez", "veces", "mayor",
     "Activos circulantes ÷ Pasivos circulantes"),
    ("razon_rapida", "Razón rápida", "liquidez", "veces", "mayor",
     "(Activos circulantes − Inventario) ÷ Pasivos circulantes"),
    ("deuda_activos", "Deudas a activos totales", "utilizacion_deudas", "porcentaje", "menor",
     "Pasivos totales ÷ Activos totales"),
    ("rotacion_interes", "Rotación del interés ganado", "utilizacion_deudas", "veces", "mayor",
     "UAII ÷ Gastos por intereses"),
    ("cobertura_cargos_fijos", "Cobertura de los cargos fijos", "utilizacion_deudas", "veces", "mayor",
     "(UAII + Arrendamientos) ÷ (Intereses + Arrendamientos)"),
], start=1)]


def _dividir(a, b):
    return a / b if b else None


def _pct(a, b):
    cociente = _dividir(a, b)
    return None if cociente is None else cociente * 100


def calcular(analisis, anio):
    er, bg = analisis.resultados[anio], analisis.balances[anio]
    dias = analisis.datos["complementarios"]["dias_anio"]
    ventas = er["ventas_netas"]
    return {
        "margen_utilidad": _pct(er["utilidad_neta"], ventas),
        "roa": _pct(er["utilidad_neta"], bg["total_activos"]),
        "roe": _pct(er["utilidad_neta"], bg["total_capital"]),
        "rotacion_cxc": _dividir(ventas, bg["cxc_netas"]),
        "ppc": _dividir(bg["cxc_netas"], ventas / dias),
        "rotacion_inventario": _dividir(ventas, bg["inventarios"]),
        "rotacion_activos_fijos": _dividir(ventas, bg["activos_fijos_netos"]),
        "rotacion_activos_totales": _dividir(ventas, bg["total_activos"]),
        "razon_circulante": _dividir(bg["total_activo_circulante"], bg["total_pasivo_circulante"]),
        "razon_rapida": _dividir(bg["total_activo_circulante"] - bg["inventarios"],
                                 bg["total_pasivo_circulante"]),
        "deuda_activos": _pct(bg["total_pasivos"], bg["total_activos"]),
        "rotacion_interes": _dividir(er["uaii"], er["gastos_intereses"]),
        "cobertura_cargos_fijos": _dividir(er["uaii"] + er["arrendamientos"],
                                           er["gastos_intereses"] + er["arrendamientos"]),
    }


def du_pont(analisis, anio):
    """ROA = margen × rotación; ROE = ROA ÷ (1 − deudas/activos)."""
    r = calcular(analisis, anio)
    margen, rotacion, deuda = r["margen_utilidad"], r["rotacion_activos_totales"], r["deuda_activos"]
    roa = None if margen is None or rotacion is None else margen * rotacion
    multiplicador = None if deuda is None or deuda == 100 else 1 / (1 - deuda / 100)
    roe = None if roa is None or multiplicador is None else roa * multiplicador
    return {"margen": margen, "rotacion": rotacion, "roa": roa, "deuda_activos": deuda,
            "multiplicador": multiplicador, "roe": roe}


def semaforo(valor, industria, mejor):
    """Verde: igual o mejor que la industria. Amarillo: hasta 10 % peor. Rojo: más de 10 % peor."""
    if valor is None:
        return "gris"
    desventaja = (industria - valor if mejor == "mayor" else valor - industria) / abs(industria)
    if desventaja <= 1e-9:
        return "verde"
    return "amarillo" if desventaja <= TOLERANCIA_AMARILLO + 1e-9 else "rojo"


def _tendencia(antes, despues, mejor):
    if antes is None or despues is None or abs(despues - antes) < 1e-9:
        return "igual"
    return "mejora" if (despues > antes) == (mejor == "mayor") else "empeora"


def tabla(analisis):
    industria = analisis.datos["industria"]
    valores = {anio: calcular(analisis, anio) for anio in (2024, 2025)}
    filas = []
    for d in DEFINICIONES:
        fila = d._asdict()
        fila["industria"] = industria[d.clave]
        for anio in (2024, 2025):
            fila[f"valor_{anio}"] = valores[anio][d.clave]
            fila[f"semaforo_{anio}"] = semaforo(valores[anio][d.clave], industria[d.clave], d.mejor)
        fila["tendencia"] = _tendencia(fila["valor_2024"], fila["valor_2025"], d.mejor)
        filas.append(fila)
    return filas


def _frase(fila):
    unidad = fila["unidad"]
    if fila["valor_2025"] is None:
        return f"{fila['nombre']}: no se puede calcular (denominador cero)."
    posicion = "igual o mejor que" if fila["semaforo_2025"] == "verde" else "peor que"
    cambio = {"mejora": "mejora", "empeora": "empeora", "igual": "se mantiene"}[fila["tendencia"]]
    return (f"{fila['nombre']}: {cambio} de {medida(fila['valor_2024'], unidad)} a "
            f"{medida(fila['valor_2025'], unidad)}, {posicion} la industria "
            f"({medida(fila['industria'], unidad)}).")


def _diagnostico(categoria, filas):
    bajo = sum(f["semaforo_2025"] in ("amarillo", "rojo") for f in filas)
    empeoran = sum(f["tendencia"] == "empeora" for f in filas)
    if bajo == 0:
        estado = "Posición favorable: todas las razones igualan o superan a la industria en 2025."
    elif bajo == len(filas):
        estado = "Posición débil: ninguna razón alcanza el promedio de la industria en 2025."
    else:
        estado = f"Posición mixta: {bajo} de {len(filas)} razones están por debajo de la industria en 2025."
    estado += f" {empeoran} de {len(filas)} empeoran frente a 2024."

    colores = {f["clave"]: f["semaforo_2025"] for f in filas}
    claves_flojas = {k for k, v in colores.items() if v in ("amarillo", "rojo")}
    notas = {
        "rentabilidad": "La empresa genera menos utilidad por cada dólar vendido, invertido o aportado; "
                        "conviene revisar costos, gastos operativos y financieros.",
        "utilizacion_activos": "Hay recursos inmovilizados: conviene endurecer la cobranza y controlar "
                               "inventarios y la productividad de la inversión en activos.",
        "liquidez": "La holgura para cubrir las obligaciones de corto plazo es insuficiente frente al sector.",
        "utilizacion_deudas": "El mayor peso de la deuda y de sus cargos reduce el margen de seguridad "
                              "para los acreedores.",
    }
    if claves_flojas:
        estado += " " + notas[categoria]
    return estado


def comentarios(analisis):
    filas = tabla(analisis)
    salida = {}
    for categoria in CATEGORIAS:
        grupo = [f for f in filas if f["categoria"] == categoria]
        salida[categoria] = " ".join([_diagnostico(categoria, grupo), *map(_frase, grupo)])
    return salida


def cambios(base, actual, anio=2025):
    """Razones que cambiaron entre dos escenarios, con su dirección y efecto."""
    antes, despues = calcular(base, anio), calcular(actual, anio)
    salida = []
    for d in DEFINICIONES:
        a, b = antes[d.clave], despues[d.clave]
        if a == b or (a is not None and b is not None and abs(a - b) < 1e-9):
            continue
        sube = a is None or (b is not None and b > a)
        salida.append({**d._asdict(), "antes": a, "despues": b,
                       "direccion": "sube" if sube else "baja",
                       "efecto": _tendencia(a, b, d.mejor)})
    return salida
