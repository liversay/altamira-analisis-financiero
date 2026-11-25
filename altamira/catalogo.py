"""Catálogo de cuentas: clasificación y naturaleza de cada cuenta de la balanza."""
from typing import NamedTuple

DEUDORA, ACREEDORA = "deudora", "acreedora"

SECCIONES = {
    "ingresos": "Ventas",
    "costo_ventas": "Costo de ventas",
    "gastos_operacion": "Gastos de operación",
    "otros_resultados": "Otros ingresos y gastos",
    "impuesto": "Impuesto sobre la renta",
    "activo_circulante": "Activos circulantes",
    "activo_fijo": "Activos fijos",
    "otros_activos": "Otros activos",
    "pasivo_circulante": "Pasivos circulantes",
    "pasivo_lp": "Pasivos a largo plazo",
    "capital": "Capital contable",
    "dividendos": "Dividendos",
}

SECCIONES_RESULTADOS = ("ingresos", "costo_ventas", "gastos_operacion", "otros_resultados", "impuesto", "dividendos")
SECCIONES_BALANCE = ("activo_circulante", "activo_fijo", "otros_activos", "pasivo_circulante", "pasivo_lp", "capital")


class Cuenta(NamedTuple):
    numero: int
    clave: str
    nombre: str
    seccion: str
    naturaleza: str


_FILAS = [
    ("activos_intangibles", "Activos intangibles (software y licencias)", "otros_activos", DEUDORA),
    ("amortizacion_acumulada", "Amortización acumulada de intangibles", "otros_activos", ACREEDORA),
    ("arrendamientos", "Arrendamientos", "gastos_operacion", DEUDORA),
    ("bonos_por_pagar", "Bonos por pagar", "pasivo_lp", ACREEDORA),
    ("caja_bancos", "Caja y bancos", "activo_circulante", DEUDORA),
    ("capital_comun", "Capital común", "capital", ACREEDORA),
    ("capital_pagado_exceso", "Capital pagado en exceso del valor nominal", "capital", ACREEDORA),
    ("costo_materiales", "Costo de materiales", "costo_ventas", DEUDORA),
    ("costos_indirectos", "Costos indirectos de fabricación", "costo_ventas", DEUDORA),
    ("cxc_comerciales", "Cuentas por cobrar comerciales", "activo_circulante", DEUDORA),
    ("cxp_proveedores", "Cuentas por pagar a proveedores", "pasivo_circulante", ACREEDORA),
    ("depreciacion_acumulada", "Depreciación acumulada", "activo_fijo", ACREEDORA),
    ("devoluciones_ventas", "Devoluciones y descuentos sobre ventas", "ingresos", DEUDORA),
    ("dividendos_decretados", "Dividendos decretados", "dividendos", DEUDORA),
    ("dividendos_por_pagar", "Dividendos por pagar", "pasivo_circulante", ACREEDORA),
    ("documentos_por_pagar", "Documentos por pagar (préstamo bancario a corto plazo)", "pasivo_circulante", ACREEDORA),
    ("edificios", "Edificios", "activo_fijo", DEUDORA),
    ("equipo_transporte", "Equipo de transporte", "activo_fijo", DEUDORA),
    ("estimacion_incobrables", "Estimación para cuentas incobrables", "activo_circulante", ACREEDORA),
    ("fletes_distribucion", "Fletes y distribución", "gastos_operacion", DEUDORA),
    ("gasto_amortizacion", "Gasto por amortización de intangibles", "gastos_operacion", DEUDORA),
    ("gasto_depreciacion", "Gasto por depreciación", "gastos_operacion", DEUDORA),
    ("gastos_acumulados", "Gastos acumulados por pagar", "pasivo_circulante", ACREEDORA),
    ("gastos_anticipados", "Gastos pagados por anticipado", "activo_circulante", DEUDORA),
    ("gastos_intereses", "Gastos por intereses", "otros_resultados", DEUDORA),
    ("honorarios_profesionales", "Honorarios profesionales", "gastos_operacion", DEUDORA),
    ("isr_periodo", "Impuesto sobre la renta del periodo", "impuesto", DEUDORA),
    ("isr_por_pagar", "Impuesto sobre la renta por pagar", "pasivo_circulante", ACREEDORA),
    ("ingresos_financieros", "Ingresos financieros", "otros_resultados", ACREEDORA),
    ("inv_materia_prima", "Inventario de materia prima", "activo_circulante", DEUDORA),
    ("inv_en_proceso", "Inventario de productos en proceso", "activo_circulante", DEUDORA),
    ("inv_terminados", "Inventario de productos terminados", "activo_circulante", DEUDORA),
    ("inversiones_lp", "Inversiones a largo plazo", "otros_activos", DEUDORA),
    ("mano_obra_directa", "Mano de obra directa", "costo_ventas", DEUDORA),
    ("mantenimiento", "Mantenimiento", "gastos_operacion", DEUDORA),
    ("maquinaria_equipo", "Maquinaria y equipo", "activo_fijo", DEUDORA),
    ("mobiliario_oficina", "Mobiliario y equipo de oficina", "activo_fijo", DEUDORA),
    ("otros_gastos", "Otros gastos generales", "gastos_operacion", DEUDORA),
    ("perdidas_extraordinarias", "Pérdidas extraordinarias", "otros_resultados", DEUDORA),
    ("porcion_corriente_deuda", "Porción corriente de la deuda a largo plazo", "pasivo_circulante", ACREEDORA),
    ("prestamo_lp", "Préstamo bancario a largo plazo", "pasivo_lp", ACREEDORA),
    ("publicidad", "Publicidad y mercadeo", "gastos_operacion", DEUDORA),
    ("seguros", "Seguros", "gastos_operacion", DEUDORA),
    ("servicios_publicos", "Servicios públicos", "gastos_operacion", DEUDORA),
    ("sueldos_administrativos", "Sueldos administrativos", "gastos_operacion", DEUDORA),
    ("sueldos_ventas", "Sueldos y comisiones de ventas", "gastos_operacion", DEUDORA),
    ("terrenos", "Terrenos", "activo_fijo", DEUDORA),
    ("utilidades_retenidas", "Utilidades retenidas", "capital", ACREEDORA),
    ("valores_negociables", "Valores negociables", "activo_circulante", DEUDORA),
    ("ventas_brutas", "Ventas brutas", "ingresos", ACREEDORA),
]

CATALOGO = [Cuenta(numero, *fila) for numero, fila in enumerate(_FILAS, start=1)]
CUENTAS = {cuenta.clave: cuenta for cuenta in CATALOGO}

# Orden de presentación en los estados financieros
ORDEN_COSTO_VENTAS = ("costo_materiales", "mano_obra_directa", "costos_indirectos")
ORDEN_GASTOS_OPERACION = (
    "sueldos_administrativos", "sueldos_ventas", "publicidad", "arrendamientos",
    "servicios_publicos", "seguros", "mantenimiento", "honorarios_profesionales",
    "fletes_distribucion", "otros_gastos", "gasto_depreciacion", "gasto_amortizacion",
)
INVENTARIOS = ("inv_materia_prima", "inv_en_proceso", "inv_terminados")
ACTIVOS_CIRCULANTES = (
    "caja_bancos", "valores_negociables", "cxc_comerciales", "estimacion_incobrables",
    *INVENTARIOS, "gastos_anticipados",
)
ACTIVOS_FIJOS = ("terrenos", "edificios", "maquinaria_equipo", "equipo_transporte", "mobiliario_oficina")
OTROS_ACTIVOS = ("activos_intangibles", "amortizacion_acumulada", "inversiones_lp")
PASIVOS_CIRCULANTES = (
    "cxp_proveedores", "documentos_por_pagar", "gastos_acumulados", "isr_por_pagar",
    "porcion_corriente_deuda", "dividendos_por_pagar",
)
PASIVOS_LP = ("prestamo_lp", "bonos_por_pagar")
CUENTAS_CAPITAL = ("capital_comun", "capital_pagado_exceso", "utilidades_retenidas")
CONTRA_ACTIVOS = ("estimacion_incobrables", "depreciacion_acumulada", "amortizacion_acumulada")
