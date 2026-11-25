"""Estado de resultados a partir de los saldos de las cuentas."""
from .catalogo import ORDEN_COSTO_VENTAS, ORDEN_GASTOS_OPERACION


def calcular(saldos, tasa_isr, acciones):
    er = {clave: saldos[clave] for clave in (
        "ventas_brutas", "devoluciones_ventas", *ORDEN_COSTO_VENTAS, *ORDEN_GASTOS_OPERACION,
        "ingresos_financieros", "gastos_intereses", "perdidas_extraordinarias",
    )}
    er["ventas_netas"] = er["ventas_brutas"] - er["devoluciones_ventas"]
    er["costo_ventas"] = sum(saldos[c] for c in ORDEN_COSTO_VENTAS)
    er["utilidad_bruta"] = er["ventas_netas"] - er["costo_ventas"]
    er["total_gastos_operacion"] = sum(saldos[c] for c in ORDEN_GASTOS_OPERACION)
    er["uaii"] = er["utilidad_bruta"] - er["total_gastos_operacion"]
    er["uai"] = (er["uaii"] + er["ingresos_financieros"]
                 - er["gastos_intereses"] - er["perdidas_extraordinarias"])
    er["isr"] = er["uai"] * tasa_isr / 100
    er["utilidad_neta"] = er["uai"] - er["isr"]
    er["upa"] = er["utilidad_neta"] / acciones if acciones else 0
    return er
