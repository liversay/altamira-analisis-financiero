"""Construye todos los estados financieros a partir de las cuentas de entrada."""
from dataclasses import dataclass

from . import balance, balanza, estado_resultados, flujo_efectivo

ANIOS = (2024, 2025)


@dataclass
class Analisis:
    datos: dict
    resultados: dict
    balances: dict
    flujos: dict
    conciliacion_ur: dict
    dividendos: dict


def construir(datos):
    comp = datos["complementarios"]
    saldos = {
        2024: datos["cuentas_2024"],
        2025: balanza.saldos(datos["balanza_2025"]),
    }
    resultados = {a: estado_resultados.calcular(saldos[a], comp["tasa_isr"], comp["acciones"]) for a in ANIOS}
    dividendos = {a: saldos[a]["dividendos_decretados"] for a in ANIOS}

    # 2025 viene antes del cierre: se cierran utilidad neta y dividendos contra utilidades retenidas
    ur_2025 = saldos[2025]["utilidades_retenidas"] + resultados[2025]["utilidad_neta"] - dividendos[2025]
    balances = {
        2023: balance.calcular(datos["cuentas_2023"], datos["cuentas_2023"]["utilidades_retenidas"]),
        2024: balance.calcular(saldos[2024], saldos[2024]["utilidades_retenidas"]),
        2025: balance.calcular(saldos[2025], ur_2025),
    }
    conciliacion_ur = {
        2024: balance.conciliar_utilidades_retenidas(
            balances[2023]["utilidades_retenidas"], resultados[2024]["utilidad_neta"],
            dividendos[2024], balances[2024]["utilidades_retenidas"]),
        2025: balance.conciliar_utilidades_retenidas(
            saldos[2025]["utilidades_retenidas"], resultados[2025]["utilidad_neta"],
            dividendos[2025], ur_2025),
    }
    # El saldo inicial 2025 debe ser el saldo final 2024
    conciliacion_ur[2025]["concilia"] = abs(
        saldos[2025]["utilidades_retenidas"] - balances[2024]["utilidades_retenidas"]) < balance.TOLERANCIA

    flujos = {a: flujo_efectivo.calcular(resultados[a], balances[a], balances[a - 1], dividendos[a]) for a in ANIOS}
    return Analisis(datos, resultados, balances, flujos, conciliacion_ur, dividendos)


def validar_2024(analisis, publicado):
    """Compara cada total publicado de 2024 con lo que calcula el sistema."""
    fuentes = {
        "resultados": analisis.resultados[2024],
        "balance": analisis.balances[2024],
        "flujo": analisis.flujos[2024],
    }
    filas = []
    for grupo, obtenidos in fuentes.items():
        for concepto, esperado in publicado[grupo].items():
            filas.append({"grupo": grupo, "concepto": concepto, "esperado": esperado,
                          "obtenido": obtenidos[concepto],
                          "ok": abs(obtenidos[concepto] - esperado) < balance.TOLERANCIA})
    upa = analisis.resultados[2024]["upa"]
    filas.append({"grupo": "resultados", "concepto": "upa", "esperado": publicado["upa"],
                  "obtenido": upa, "ok": round(upa, 2) == publicado["upa"]})
    return filas
