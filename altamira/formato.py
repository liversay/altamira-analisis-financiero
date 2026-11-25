"""Formato de cifras en dólares estadounidenses."""


def monto(valor):
    """Cifra con separador de miles; negativos entre paréntesis; centavos solo si existen."""
    centavos = round(abs(valor) * 100)
    texto = f"{centavos / 100:,.0f}" if centavos % 100 == 0 else f"{centavos / 100:,.2f}"
    return f"({texto})" if valor < 0 and centavos else texto


def usd(valor):
    return f"US$ {monto(valor)}"


def usd_accion(valor):
    texto = f"{abs(valor):,.2f}"
    return f"US$ ({texto})" if valor < 0 else f"US$ {texto}"


def porcentaje(valor):
    return "n/d" if valor is None else f"{valor:,.2f} %"


def medida(valor, unidad):
    if valor is None:
        return "n/d"
    if unidad == "porcentaje":
        return porcentaje(valor)
    return f"{valor:,.2f} {'días' if unidad == 'dias' else 'veces'}"
