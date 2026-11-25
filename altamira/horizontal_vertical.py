"""Análisis horizontal (variaciones) y vertical (porcentajes de una base)."""
from . import presentacion

# Dividendos no forma parte del estado de resultados, pero es una cuenta de la balanza
_DIVIDENDOS = ("cuenta", "dividendos_decretados", "Dividendos decretados", 1)


def _analizar(estructura, valores, base):
    filas = presentacion.filas(estructura, valores)
    for fila in filas:
        if not fila["clave"]:
            continue
        v2024, v2025 = fila["v2024"], fila["v2025"]
        fila["absoluta"] = v2025 - v2024
        # el porcentaje mide cómo creció el saldo de la cuenta, aunque se presente como deducción
        signo = -1 if fila["deduccion"] else 1
        fila["porcentual"] = signo * (v2025 - v2024) / abs(v2024) * 100 if v2024 else None
        for anio in (2024, 2025):
            total = valores[anio][base]
            fila[f"pct{anio}"] = fila[f"v{anio}"] / total * 100 if total else None
    return filas


def resultados(analisis):
    valores = {a: {**analisis.resultados[a], "dividendos_decretados": analisis.dividendos[a]}
               for a in (2024, 2025)}
    return _analizar([*presentacion.ESTADO_RESULTADOS, _DIVIDENDOS], valores, "ventas_netas")


def balance(analisis):
    valores = {a: analisis.balances[a] for a in (2024, 2025)}
    return _analizar(presentacion.BALANCE_GENERAL, valores, "total_activos")
