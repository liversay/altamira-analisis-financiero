"""Balance general y validación Activos = Pasivos + Capital."""
from . import catalogo as c

TOLERANCIA = 0.5


def calcular(saldos, utilidades_retenidas):
    claves = (*c.ACTIVOS_CIRCULANTES, *c.ACTIVOS_FIJOS, "depreciacion_acumulada", *c.OTROS_ACTIVOS,
              *c.PASIVOS_CIRCULANTES, *c.PASIVOS_LP, *c.CUENTAS_CAPITAL)
    bg = {clave: saldos[clave] for clave in claves}
    bg["utilidades_retenidas"] = utilidades_retenidas

    bg["cxc_netas"] = bg["cxc_comerciales"] - bg["estimacion_incobrables"]
    bg["inventarios"] = sum(bg[x] for x in c.INVENTARIOS)
    bg["total_activo_circulante"] = (bg["caja_bancos"] + bg["valores_negociables"] + bg["cxc_netas"]
                                     + bg["inventarios"] + bg["gastos_anticipados"])
    bg["activos_fijos_brutos"] = sum(bg[x] for x in c.ACTIVOS_FIJOS)
    bg["activos_fijos_netos"] = bg["activos_fijos_brutos"] - bg["depreciacion_acumulada"]
    bg["intangibles_netos"] = bg["activos_intangibles"] - bg["amortizacion_acumulada"]
    bg["total_otros_activos"] = bg["intangibles_netos"] + bg["inversiones_lp"]
    bg["total_activos"] = (bg["total_activo_circulante"] + bg["activos_fijos_netos"]
                           + bg["total_otros_activos"])

    bg["total_pasivo_circulante"] = sum(bg[x] for x in c.PASIVOS_CIRCULANTES)
    bg["total_pasivo_lp"] = sum(bg[x] for x in c.PASIVOS_LP)
    bg["total_pasivos"] = bg["total_pasivo_circulante"] + bg["total_pasivo_lp"]
    bg["total_capital"] = sum(bg[x] for x in c.CUENTAS_CAPITAL)
    bg["total_pasivo_capital"] = bg["total_pasivos"] + bg["total_capital"]

    bg["diferencia"] = bg["total_activos"] - bg["total_pasivo_capital"]
    bg["cuadra"] = abs(bg["diferencia"]) < TOLERANCIA
    return bg


def conciliar_utilidades_retenidas(saldo_inicial, utilidad_neta, dividendos, saldo_esperado):
    saldo_final = saldo_inicial + utilidad_neta - dividendos
    return {
        "saldo_inicial": saldo_inicial, "utilidad_neta": utilidad_neta, "dividendos": dividendos,
        "saldo_final": saldo_final, "concilia": abs(saldo_final - saldo_esperado) < TOLERANCIA,
    }
