"""Estado de flujo de efectivo (método indirecto) y flujo de efectivo libre."""
from .balance import TOLERANCIA


def _renglon(clave, concepto, monto):
    return {"clave": clave, "concepto": concepto, "monto": monto}


def _cambio_activo(clave, nombre, actual, anterior):
    delta = actual - anterior
    verbo = "Disminución" if delta < 0 else "Aumento"
    return _renglon(clave, f"{verbo} en {nombre}", -delta)


def _cambio_pasivo(clave, nombre, actual, anterior):
    delta = actual - anterior
    verbo = "Disminución" if delta < 0 else "Aumento"
    return _renglon(clave, f"{verbo} en {nombre}", delta)


def _inversion(clave, nombre, actual, anterior):
    delta = actual - anterior
    verbo = "Venta" if delta < 0 else "Compra"
    return _renglon(clave, f"{verbo} de {nombre}", -delta)


def calcular(er, actual, anterior, dividendos_decretados):
    """`actual` y `anterior` son balances generales de dos años consecutivos."""
    operacion = [
        _renglon("utilidad_neta", "Utilidad neta", er["utilidad_neta"]),
        _renglon("depreciacion", "Depreciación", er["gasto_depreciacion"]),
        _renglon("amortizacion", "Amortización de intangibles", er["gasto_amortizacion"]),
        _cambio_activo("cxc", "cuentas por cobrar (neto de estimación)", actual["cxc_netas"], anterior["cxc_netas"]),
        _cambio_activo("inventarios", "inventarios", actual["inventarios"], anterior["inventarios"]),
        _cambio_activo("anticipados", "gastos pagados por anticipado", actual["gastos_anticipados"], anterior["gastos_anticipados"]),
        _cambio_pasivo("cxp", "cuentas por pagar", actual["cxp_proveedores"], anterior["cxp_proveedores"]),
        _cambio_pasivo("acumulados", "gastos acumulados por pagar", actual["gastos_acumulados"], anterior["gastos_acumulados"]),
        _cambio_pasivo("isr", "ISR por pagar", actual["isr_por_pagar"], anterior["isr_por_pagar"]),
    ]
    inversion = [
        _inversion("activos_fijos", "activos fijos", actual["activos_fijos_brutos"], anterior["activos_fijos_brutos"]),
        _inversion("intangibles", "activos intangibles", actual["activos_intangibles"], anterior["activos_intangibles"]),
        _inversion("valores_negociables", "valores negociables", actual["valores_negociables"], anterior["valores_negociables"]),
        _inversion("inversiones_lp", "inversiones a largo plazo", actual["inversiones_lp"], anterior["inversiones_lp"]),
    ]

    def deuda_lp(bg):
        return bg["prestamo_lp"] + bg["bonos_por_pagar"] + bg["porcion_corriente_deuda"]

    cambio_deuda = deuda_lp(actual) - deuda_lp(anterior)
    dividendos_pagados = dividendos_decretados - (actual["dividendos_por_pagar"] - anterior["dividendos_por_pagar"])
    financiamiento = [
        _cambio_pasivo("documentos", "documentos por pagar", actual["documentos_por_pagar"], anterior["documentos_por_pagar"]),
        _renglon("deuda_lp",
                 "Pago de préstamo bancario a largo plazo" if cambio_deuda < 0
                 else "Aumento neto de la deuda a largo plazo", cambio_deuda),
        _renglon("dividendos", "Dividendos pagados", -dividendos_pagados),
    ]

    flujo = {"operacion": operacion, "inversion": inversion, "financiamiento": financiamiento}
    for seccion in ("operacion", "inversion", "financiamiento"):
        flujo[f"total_{seccion}"] = sum(r["monto"] for r in flujo[seccion])
    flujo["cambio_neto"] = flujo["total_operacion"] + flujo["total_inversion"] + flujo["total_financiamiento"]
    flujo["caja_inicial"] = anterior["caja_bancos"]
    flujo["caja_final"] = actual["caja_bancos"]
    flujo["diferencia"] = flujo["caja_final"] - flujo["caja_inicial"] - flujo["cambio_neto"]
    flujo["concilia"] = abs(flujo["diferencia"]) < TOLERANCIA
    flujo["compra_activos_fijos"] = actual["activos_fijos_brutos"] - anterior["activos_fijos_brutos"]
    flujo["dividendos_pagados"] = dividendos_pagados
    flujo["flujo_libre"] = flujo["total_operacion"] - flujo["compra_activos_fijos"] - dividendos_pagados
    return flujo
