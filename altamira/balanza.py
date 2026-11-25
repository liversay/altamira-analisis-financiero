"""Balanza de comprobación: totales y saldos por cuenta."""
from .catalogo import CUENTAS, DEUDORA


def totales(balanza):
    debe = sum(fila["debe"] for fila in balanza.values())
    haber = sum(fila["haber"] for fila in balanza.values())
    return debe, haber


def saldos(balanza):
    """Saldo de cada cuenta, positivo cuando está del lado de su naturaleza."""
    return {
        clave: (fila["debe"] - fila["haber"]) * (1 if CUENTAS[clave].naturaleza == DEUDORA else -1)
        for clave, fila in balanza.items()
    }
