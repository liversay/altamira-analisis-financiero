from altamira import formato


def test_dolares_con_separador_de_miles_y_negativos_entre_parentesis():
    assert formato.usd(9311000) == "US$ 9,311,000"
    assert formato.usd(-89000) == "US$ (89,000)"


def test_centavos_solo_cuando_existen():
    assert formato.usd(152750.5) == "US$ 152,750.50"
    assert formato.monto(-0.0000001) == "0"


def test_monto_sin_simbolo_para_las_tablas():
    assert formato.monto(-175000) == "(175,000)"


def test_porcentaje_veces_y_dias():
    assert formato.porcentaje(2.2392) == "2.24 %"
    assert formato.medida(7.19, "veces") == "7.19 veces"
    assert formato.medida(50.07, "dias") == "50.07 días"
    assert formato.medida(None, "veces") == "n/d"


def test_dolares_por_accion_siempre_con_dos_decimales():
    assert formato.usd_accion(1.0425) == "US$ 1.04"
