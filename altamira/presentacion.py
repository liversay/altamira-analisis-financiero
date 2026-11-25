"""Estructura de presentación de los estados financieros.

Cada renglón es (tipo, clave, concepto, signo). Las deducciones usan signo -1.
"""
from .catalogo import CUENTAS, ORDEN_COSTO_VENTAS, ORDEN_GASTOS_OPERACION


def _cuenta(clave, signo=1, concepto=None):
    return ("cuenta", clave, concepto or CUENTAS[clave].nombre, signo)


def _grupo(concepto):
    return ("grupo", None, concepto, 1)


def _subtotal(clave, concepto):
    return ("subtotal", clave, concepto, 1)


def _total(clave, concepto):
    return ("total", clave, concepto, 1)


ESTADO_RESULTADOS = [
    _grupo("Ventas"),
    _cuenta("ventas_brutas"),
    _cuenta("devoluciones_ventas", -1),
    _subtotal("ventas_netas", "Ventas netas"),
    _grupo("Costo de ventas"),
    *[_cuenta(c) for c in ORDEN_COSTO_VENTAS],
    _subtotal("costo_ventas", "Costo de ventas"),
    _subtotal("utilidad_bruta", "Utilidad bruta"),
    _grupo("Gastos de operación"),
    *[_cuenta(c) for c in ORDEN_GASTOS_OPERACION],
    _subtotal("total_gastos_operacion", "Total gastos de operación"),
    _subtotal("uaii", "Utilidad de operación (UAII)"),
    _grupo("Otros ingresos y gastos"),
    _cuenta("ingresos_financieros"),
    _cuenta("gastos_intereses", -1),
    _cuenta("perdidas_extraordinarias", -1),
    _subtotal("uai", "Utilidad antes de impuestos"),
    _cuenta("isr", -1, "Impuesto sobre la renta"),
    _total("utilidad_neta", "Utilidad neta"),
]

BALANCE_GENERAL = [
    _grupo("Activos circulantes"),
    _cuenta("caja_bancos"),
    _cuenta("valores_negociables"),
    _cuenta("cxc_comerciales"),
    _cuenta("estimacion_incobrables", -1),
    _subtotal("cxc_netas", "Cuentas por cobrar netas"),
    _cuenta("inv_materia_prima"),
    _cuenta("inv_en_proceso"),
    _cuenta("inv_terminados"),
    _cuenta("gastos_anticipados"),
    _subtotal("total_activo_circulante", "Total activos circulantes"),
    _grupo("Activos fijos"),
    _cuenta("terrenos"),
    _cuenta("edificios"),
    _cuenta("maquinaria_equipo"),
    _cuenta("equipo_transporte"),
    _cuenta("mobiliario_oficina"),
    _cuenta("depreciacion_acumulada", -1),
    _subtotal("activos_fijos_netos", "Activos fijos netos"),
    _grupo("Otros activos"),
    _cuenta("activos_intangibles"),
    _cuenta("amortizacion_acumulada", -1),
    _cuenta("inversiones_lp"),
    _subtotal("total_otros_activos", "Total otros activos"),
    _total("total_activos", "Total activos"),
    _grupo("Pasivos circulantes"),
    _cuenta("cxp_proveedores"),
    _cuenta("documentos_por_pagar"),
    _cuenta("gastos_acumulados"),
    _cuenta("isr_por_pagar"),
    _cuenta("porcion_corriente_deuda"),
    _cuenta("dividendos_por_pagar"),
    _subtotal("total_pasivo_circulante", "Total pasivos circulantes"),
    _grupo("Pasivos a largo plazo"),
    _cuenta("prestamo_lp"),
    _cuenta("bonos_por_pagar"),
    _subtotal("total_pasivo_lp", "Total pasivos a largo plazo"),
    _subtotal("total_pasivos", "Total pasivos"),
    _grupo("Capital contable"),
    _cuenta("capital_comun"),
    _cuenta("capital_pagado_exceso"),
    _cuenta("utilidades_retenidas"),
    _subtotal("total_capital", "Total capital contable"),
    _total("total_pasivo_capital", "Total pasivos y capital contable"),
]


def filas(estructura, valores_por_anio):
    """Renglones con el valor de cada año ya con su signo de presentación."""
    salida = []
    for tipo, clave, concepto, signo in estructura:
        fila = {"tipo": tipo, "clave": clave, "concepto": concepto, "deduccion": signo < 0}
        if clave:
            for anio, valores in valores_por_anio.items():
                fila[f"v{anio}"] = valores[clave] * signo
        salida.append(fila)
    return salida
