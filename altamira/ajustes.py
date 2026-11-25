"""Modificación de una cuenta de la balanza 2025, con contrapartida opcional."""
import copy

from . import analisis, balanza
from .catalogo import CUENTAS, DEUDORA


def _signo(clave):
    return 1 if CUENTAS[clave].naturaleza == DEUDORA else -1


def fila_de_saldo(clave, saldo):
    """Convierte un saldo (positivo según su naturaleza) en columnas Debe y Haber."""
    neto = saldo * _signo(clave)
    return {"debe": neto if neto > 0 else 0, "haber": -neto if neto < 0 else 0}


def _mover(bal, clave, cambio_neto_deudor):
    saldo = balanza.saldos(bal)[clave] + cambio_neto_deudor * _signo(clave)
    bal[clave] = fila_de_saldo(clave, saldo)


def modificar(datos, clave, saldo, contrapartida=None):
    """Devuelve una copia de los datos con el nuevo saldo de la cuenta.

    Sin contrapartida solo cambia esa cuenta (el sistema alertará el descuadre).
    Con contrapartida se registra la partida doble y se recalcula el ISR del periodo
    contra el ISR por pagar.
    """
    if clave not in CUENTAS:
        raise ValueError(f"Cuenta desconocida: {clave}")
    if contrapartida and (contrapartida not in CUENTAS or contrapartida == clave):
        raise ValueError("La contrapartida debe ser otra cuenta de la balanza.")

    nuevos = copy.deepcopy(datos)
    bal = nuevos["balanza_2025"]
    cambio = (saldo - balanza.saldos(bal)[clave]) * _signo(clave)
    bal[clave] = fila_de_saldo(clave, saldo)

    if contrapartida:
        _mover(bal, contrapartida, -cambio)
        if "isr_periodo" not in (clave, contrapartida):
            ajuste = analisis.construir(nuevos).resultados[2025]["isr"] - balanza.saldos(bal)["isr_periodo"]
            _mover(bal, "isr_periodo", ajuste)
            _mover(bal, "isr_por_pagar", -ajuste)
    return nuevos
