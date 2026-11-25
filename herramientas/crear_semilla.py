"""Genera data/datos_base.json con las cuentas de entrada originales."""
import json
from pathlib import Path

D, H = "debe", "haber"
# (clave, lado, monto) en el orden de la balanza de comprobación 2025 (cuentas 1 a 50)
BALANZA_2025 = [
    ("activos_intangibles", D, 410000), ("amortizacion_acumulada", H, 194000),
    ("arrendamientos", D, 156000), ("bonos_por_pagar", H, 800000),
    ("caja_bancos", D, 337750), ("capital_comun", H, 1000000),
    ("capital_pagado_exceso", H, 400000), ("costo_materiales", D, 3910000),
    ("costos_indirectos", D, 946000), ("cxc_comerciales", D, 1335000),
    ("cxp_proveedores", H, 780000), ("depreciacion_acumulada", H, 2662000),
    ("devoluciones_ventas", D, 229000), ("dividendos_decretados", D, 83000),
    ("dividendos_por_pagar", H, 40000), ("documentos_por_pagar", H, 520000),
    ("edificios", D, 1800000), ("equipo_transporte", D, 600000),
    ("estimacion_incobrables", H, 40000), ("fletes_distribucion", D, 248000),
    ("gasto_amortizacion", D, 44000), ("gasto_depreciacion", D, 382000),
    ("gastos_acumulados", H, 214000), ("gastos_anticipados", D, 72000),
    ("gastos_intereses", D, 214000), ("honorarios_profesionales", D, 61000),
    ("isr_periodo", D, 69500), ("isr_por_pagar", H, 88000),
    ("ingresos_financieros", H, 12000), ("inv_materia_prima", D, 540000),
    ("inv_en_proceso", D, 165000), ("inv_terminados", D, 735000),
    ("inversiones_lp", D, 250000), ("mano_obra_directa", D, 1415000),
    ("mantenimiento", D, 104000), ("maquinaria_equipo", D, 3480000),
    ("mobiliario_oficina", D, 255000), ("otros_gastos", D, 57000),
    ("perdidas_extraordinarias", D, 38000), ("porcion_corriente_deuda", H, 250000),
    ("prestamo_lp", H, 1600000), ("publicidad", D, 215000),
    ("seguros", D, 70000), ("servicios_publicos", D, 131000),
    ("sueldos_administrativos", D, 566000), ("sueldos_ventas", D, 488000),
    ("terrenos", D, 650000), ("utilidades_retenidas", H, 1976250),
    ("valores_negociables", D, 60000), ("ventas_brutas", H, 9540000),
]

RESULTADOS_2024 = {
    "ventas_brutas": 8750000, "devoluciones_ventas": 175000,
    "costo_materiales": 3430000, "mano_obra_directa": 1286000, "costos_indirectos": 857000,
    "sueldos_administrativos": 520000, "sueldos_ventas": 430000, "publicidad": 172000,
    "arrendamientos": 144000, "servicios_publicos": 118000, "seguros": 64000,
    "mantenimiento": 86000, "honorarios_profesionales": 52000, "fletes_distribucion": 215000,
    "otros_gastos": 48000, "gasto_depreciacion": 330000, "gasto_amortizacion": 40000,
    "ingresos_financieros": 18000, "gastos_intereses": 165000,
    "perdidas_extraordinarias": 25000, "isr_periodo": 152750, "dividendos_decretados": 183000,
}

CLAVES_BALANCE = [
    "caja_bancos", "valores_negociables", "cxc_comerciales", "estimacion_incobrables",
    "inv_materia_prima", "inv_en_proceso", "inv_terminados", "gastos_anticipados",
    "terrenos", "edificios", "maquinaria_equipo", "equipo_transporte", "mobiliario_oficina",
    "depreciacion_acumulada", "activos_intangibles", "amortizacion_acumulada", "inversiones_lp",
    "cxp_proveedores", "documentos_por_pagar", "gastos_acumulados", "isr_por_pagar",
    "porcion_corriente_deuda", "dividendos_por_pagar", "prestamo_lp", "bonos_por_pagar",
    "capital_comun", "capital_pagado_exceso", "utilidades_retenidas",
]
BALANCE_2024 = [437250, 120000, 1060000, 32000, 445000, 150000, 560000, 65000,
                650000, 1800000, 2850000, 480000, 230000, 2280000, 350000, 150000, 250000,
                655000, 350000, 198000, 110000, 200000, 46000, 1250000, 800000,
                1000000, 400000, 1976250]
BALANCE_2023 = [310000, 150000, 980000, 29000, 410000, 140000, 520000, 60000,
                650000, 1800000, 2600000, 420000, 210000, 1950000, 320000, 110000, 250000,
                610000, 300000, 185000, 95000, 200000, 40000, 1400000, 800000,
                1000000, 400000, 1701000]

datos = {
    "balanza_2025": {
        clave: {"debe": monto if lado == D else 0, "haber": monto if lado == H else 0}
        for clave, lado, monto in BALANZA_2025
    },
    "cuentas_2024": {**RESULTADOS_2024, **dict(zip(CLAVES_BALANCE, BALANCE_2024))},
    "cuentas_2023": dict(zip(CLAVES_BALANCE, BALANCE_2023)),
    "complementarios": {
        "acciones": 200000, "valor_nominal": 5.0, "tasa_isr": 25.0, "dias_anio": 360,
        "garrafones_unidades": 1160000, "garrafones_precio": 4.5,
        "cubetas_unidades": 480000, "cubetas_precio": 9.0,
        "precio_accion": 0,
    },
    "industria": {
        "margen_utilidad": 4.5, "roa": 5.5, "roe": 11.5, "rotacion_cxc": 8.0, "ppc": 45,
        "rotacion_inventario": 7.0, "rotacion_activos_fijos": 2.4,
        "rotacion_activos_totales": 1.25, "razon_circulante": 1.9, "razon_rapida": 1.1,
        "deuda_activos": 50, "rotacion_interes": 4.5, "cobertura_cargos_fijos": 3.0,
    },
}

destino = Path(__file__).resolve().parent.parent / "data" / "datos_base.json"
destino.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")
