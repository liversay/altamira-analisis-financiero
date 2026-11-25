from altamira import balanza, catalogo


def test_las_50_cuentas_de_la_balanza_estan_clasificadas(datos):
    assert len(catalogo.CATALOGO) == 50
    assert [c.clave for c in catalogo.CATALOGO] == list(datos["balanza_2025"])
    assert all(c.seccion in catalogo.SECCIONES for c in catalogo.CATALOGO)


def test_numeracion_sigue_la_balanza():
    assert catalogo.CUENTAS["activos_intangibles"].numero == 1
    assert catalogo.CUENTAS["gastos_intereses"].numero == 25
    assert catalogo.CUENTAS["ventas_brutas"].numero == 50


def test_balanza_suma_igual_en_debe_y_haber(datos):
    assert balanza.totales(datos["balanza_2025"]) == (20116250, 20116250)


def test_saldos_respetan_la_naturaleza_de_la_cuenta(datos):
    saldos = balanza.saldos(datos["balanza_2025"])
    assert saldos["cxc_comerciales"] == 1335000
    assert saldos["depreciacion_acumulada"] == 2662000
    assert saldos["ventas_brutas"] == 9540000


def test_saldo_contrario_a_la_naturaleza_es_negativo(datos):
    datos["balanza_2025"]["caja_bancos"] = {"debe": 0, "haber": 500}
    assert balanza.saldos(datos["balanza_2025"])["caja_bancos"] == -500
