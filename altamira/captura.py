"""Lectura y validación de los valores escritos en los formularios de captura."""
import copy
import math

from .catalogo import CUENTAS

LIMITE = 1e13


def leer_numero(texto):
    limpio = str(texto).strip().replace("US$", "").replace(",", "").replace(" ", "")
    if not limpio:
        return 0
    if limpio.startswith("(") and limpio.endswith(")"):
        limpio = "-" + limpio[1:-1]
    numero = float(limpio)
    if not math.isfinite(numero) or abs(numero) > LIMITE:
        raise ValueError(texto)
    return int(numero) if numero.is_integer() else numero


def _destinos(datos):
    """Nombre de campo del formulario → (diccionario, clave, etiqueta, regla)."""
    for clave, fila in datos["balanza_2025"].items():
        for lado in ("debe", "haber"):
            yield f"b25_{clave}_{lado}", fila, lado, f"{CUENTAS[clave].nombre} 2025 ({lado})", "no_negativo"
    for prefijo, anio in (("c24", "2024"), ("c23", "2023")):
        cuentas = datos[f"cuentas_{anio}"]
        for clave in cuentas:
            regla = "libre" if clave == "utilidades_retenidas" else "no_negativo"
            yield f"{prefijo}_{clave}", cuentas, clave, f"{CUENTAS[clave].nombre} {anio}", regla
    reglas = {"acciones": "positivo", "dias_anio": "positivo", "tasa_isr": "porcentaje"}
    for clave in datos["complementarios"]:
        yield (f"comp_{clave}", datos["complementarios"], clave,
               clave.replace("_", " "), reglas.get(clave, "no_negativo"))
    for clave in datos["industria"]:
        yield f"ind_{clave}", datos["industria"], clave, f"Industria: {clave.replace('_', ' ')}", "positivo"


_REGLAS = {
    "libre": (lambda n: True, ""),
    "no_negativo": (lambda n: n >= 0, "no puede ser negativo"),
    "positivo": (lambda n: n > 0, "debe ser mayor que cero"),
    "porcentaje": (lambda n: 0 <= n <= 100, "debe estar entre 0 y 100"),
}


def aplicar(datos, campos):
    """Devuelve (datos nuevos, errores). Si hay algún error no se aplica ningún cambio."""
    nuevos, errores = copy.deepcopy(datos), []
    for campo, contenedor, clave, etiqueta, regla in _destinos(nuevos):
        if campo not in campos:
            continue
        try:
            numero = leer_numero(campos[campo])
        except ValueError:
            errores.append(f"{etiqueta}: «{campos[campo]}» no es un monto válido.")
            continue
        valida, mensaje = _REGLAS[regla]
        if not valida(numero):
            errores.append(f"{etiqueta}: {mensaje}.")
            continue
        contenedor[clave] = numero
    return (copy.deepcopy(datos), errores) if errores else (nuevos, [])
