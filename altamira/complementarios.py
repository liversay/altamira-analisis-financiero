"""Indicadores complementarios (capítulos 2 y 3), literales a–g."""
from . import razones
from .balance import TOLERANCIA

CAPITAL_TRABAJO = ("cxc", "inventarios", "anticipados", "cxp", "acumulados", "isr")


def _tasa(analisis):
    return analisis.datos["complementarios"]["tasa_isr"]


def escudo_fiscal(analisis, anio=2025):
    er, tasa = analisis.resultados[anio], _tasa(analisis)
    depreciacion, amortizacion = er["gasto_depreciacion"], er["gasto_amortizacion"]
    no_efectivo = depreciacion + amortizacion
    escudo = no_efectivo * tasa / 100
    flujo = analisis.flujos[anio]["total_operacion"]
    return {
        "depreciacion": depreciacion, "amortizacion": amortizacion,
        "gasto_no_efectivo": no_efectivo, "tasa": tasa, "escudo": escudo,
        "utilidad_neta": er["utilidad_neta"],
        "utilidad_neta_sin": er["utilidad_neta"] + no_efectivo - escudo,
        # sin el gasto deducible se paga más impuesto en efectivo
        "flujo_operacion": flujo, "flujo_operacion_sin": flujo - escudo,
    }


def costo_despues_impuestos(analisis, anio=2025):
    er, tasa = analisis.resultados[anio], _tasa(analisis) / 100
    filas = [
        {"concepto": nombre, "antes": er[clave], "ahorro": er[clave] * tasa,
         "despues": er[clave] * (1 - tasa)}
        for nombre, clave in (("Gastos por intereses", "gastos_intereses"),
                              ("Arrendamientos", "arrendamientos"))
    ]
    total = {k: sum(f[k] for f in filas) for k in ("antes", "ahorro", "despues")}
    return {"filas": filas, "total": total, "tasa": _tasa(analisis)}


def valor_por_accion(analisis):
    comp = analisis.datos["complementarios"]
    acciones, precio = comp["acciones"], comp.get("precio_accion") or 0
    salida = {}
    for anio in (2024, 2025):
        upa = analisis.resultados[anio]["upa"]
        dividendo = analisis.dividendos[anio] / acciones
        libros = analisis.balances[anio]["total_capital"] / acciones
        salida[anio] = {
            "valor_libros": libros, "upa": upa, "dividendo": dividendo,
            "razon_pago": dividendo / upa * 100 if upa > 0 else None,
            "precio_utilidad": precio / upa if precio and upa > 0 else None,
            "precio_valor_libros": precio / libros if precio and libros > 0 else None,
        }
    return salida


def ventas_por_producto(analisis):
    comp = analisis.datos["complementarios"]
    productos = []
    for nombre, prefijo in (("Garrafones de 5 galones", "garrafones"), ("Cubetas industriales", "cubetas")):
        unidades, precio = comp[f"{prefijo}_unidades"], comp[f"{prefijo}_precio"]
        productos.append({"nombre": nombre, "unidades": unidades, "precio": precio,
                          "ventas": unidades * precio})
    total = sum(p["ventas"] for p in productos)
    for p in productos:
        p["participacion"] = p["ventas"] / total * 100 if total else None
    brutas = analisis.resultados[2025]["ventas_brutas"]
    return {"productos": productos, "total": total, "ventas_brutas": brutas,
            "diferencia": total - brutas, "concilia": abs(total - brutas) < TOLERANCIA}


def utilidad_vs_flujo(analisis):
    salida = {}
    for anio in (2024, 2025):
        flujo = analisis.flujos[anio]
        utilidad = analisis.resultados[anio]["utilidad_neta"]
        partidas = [r for r in flujo["operacion"] if r["clave"] in CAPITAL_TRABAJO]
        salida[anio] = {
            "utilidad_neta": utilidad, "flujo_operacion": flujo["total_operacion"],
            "diferencia": utilidad - flujo["total_operacion"],
            "no_efectivo": sum(r["monto"] for r in flujo["operacion"]
                               if r["clave"] in ("depreciacion", "amortizacion")),
            "capital_trabajo": sum(r["monto"] for r in partidas),
            "partidas": partidas,
            "principales": sorted(partidas, key=lambda r: abs(r["monto"]), reverse=True)[:3],
        }
    return salida


def du_pont_descompuesto(analisis):
    """Sustitución en cadena: primero margen, luego rotación y al final endeudamiento."""
    antes, despues = razones.du_pont(analisis, 2024), razones.du_pont(analisis, 2025)
    claves = ("margen", "rotacion", "multiplicador")
    if any(dp[k] is None for dp in (antes, despues) for k in claves):
        return None
    m0, r0, k0 = (antes[k] for k in claves)
    m1, r1, k1 = (despues[k] for k in claves)
    return {
        "antes": antes, "despues": despues,
        "efecto_margen": (m1 - m0) * r0 * k0,
        "efecto_rotacion": m1 * (r1 - r0) * k0,
        "efecto_endeudamiento": m1 * r1 * (k1 - k0),
        "variacion": despues["roe"] - antes["roe"],
    }


def politica_credito(analisis):
    dias = analisis.datos["complementarios"]["dias_anio"]
    ventas_diarias = analisis.resultados[2025]["ventas_netas"] / dias
    ppc = razones.calcular(analisis, 2025)["ppc"]
    objetivo = analisis.datos["industria"]["ppc"]
    exceso = max(ppc - objetivo, 0) if ppc is not None else 0
    return {"ppc": ppc, "ppc_industria": objetivo, "ventas_diarias": ventas_diarias,
            "dias_exceso": exceso, "efectivo_inmovilizado": exceso * ventas_diarias}
