"""Alertas de consistencia de los datos capturados."""
from . import balanza
from .balance import TOLERANCIA
from .formato import usd


def _alerta(codigo, nivel, mensaje):
    return {"codigo": codigo, "nivel": nivel, "mensaje": mensaje}


def alertas(analisis):
    salida = []
    debe, haber = balanza.totales(analisis.datos["balanza_2025"])
    if abs(debe - haber) >= TOLERANCIA:
        salida.append(_alerta("balanza_debe_haber", "error",
                              f"La balanza 2025 no cuadra: Debe {usd(debe)} ≠ Haber {usd(haber)} "
                              f"(diferencia {usd(debe - haber)})."))
    for anio, bg in sorted(analisis.balances.items()):
        if not bg["cuadra"]:
            salida.append(_alerta(f"balance_{anio}", "error",
                                  f"El balance {anio} no cuadra: Activos {usd(bg['total_activos'])} ≠ "
                                  f"Pasivos + Capital {usd(bg['total_pasivo_capital'])} "
                                  f"(diferencia {usd(bg['diferencia'])})."))
    registrados = {2024: analisis.datos["cuentas_2024"]["isr_periodo"],
                   2025: balanza.saldos(analisis.datos["balanza_2025"])["isr_periodo"]}
    for anio, registrado in registrados.items():
        calculado = analisis.resultados[anio]["isr"]
        if abs(registrado - calculado) >= TOLERANCIA:
            salida.append(_alerta(f"isr_{anio}", "aviso",
                                  f"El ISR capturado de {anio} ({usd(registrado)}) difiere del ISR calculado "
                                  f"sobre la utilidad antes de impuestos ({usd(calculado)})."))
    if not analisis.conciliacion_ur[2024]["concilia"]:
        salida.append(_alerta("conciliacion_ur_2024", "aviso",
                              "Utilidades retenidas 2024 no concilian: saldo 2023 + utilidad neta − dividendos "
                              f"= {usd(analisis.conciliacion_ur[2024]['saldo_final'])}."))
    if not analisis.conciliacion_ur[2025]["concilia"]:
        salida.append(_alerta("utilidades_retenidas", "aviso",
                              "El saldo inicial 2025 de utilidades retenidas no coincide con el saldo final 2024."))
    return salida
