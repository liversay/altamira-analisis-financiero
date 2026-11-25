import pytest

from altamira import analisis, catalogo, horizontal_vertical as hv


@pytest.fixture
def a(datos):
    return analisis.construir(datos)


def por_clave(filas):
    return {f["clave"]: f for f in filas if f["tipo"] != "grupo"}


def test_horizontal_incluye_cada_cuenta_de_la_balanza(a):
    claves = set(por_clave(hv.resultados(a))) | set(por_clave(hv.balance(a)))
    # la cuenta de ISR se presenta con el impuesto calculado ("isr")
    assert set(catalogo.CUENTAS) - {"isr_periodo"} <= claves
    assert "isr" in claves


def test_variacion_absoluta_y_porcentual(a):
    fila = por_clave(hv.balance(a))["cxc_comerciales"]
    assert (fila["v2024"], fila["v2025"], fila["absoluta"]) == (1060000, 1335000, 275000)
    assert fila["porcentual"] == pytest.approx(25.9434, abs=0.0005)
    assert por_clave(hv.resultados(a))["utilidad_neta"]["porcentual"] == pytest.approx(-54.5008, abs=0.0005)


def test_las_deducciones_se_presentan_en_negativo(a):
    fila = por_clave(hv.balance(a))["depreciacion_acumulada"]
    assert (fila["v2024"], fila["v2025"], fila["absoluta"]) == (-2280000, -2662000, -382000)
    assert fila["porcentual"] == pytest.approx(16.7544, abs=0.0005)


def test_variacion_porcentual_con_base_cero_no_esta_disponible(datos):
    datos["cuentas_2024"]["ingresos_financieros"] = 0
    fila = por_clave(hv.resultados(analisis.construir(datos)))["ingresos_financieros"]
    assert fila["absoluta"] == 12000 and fila["porcentual"] is None


def test_vertical_resultados_sobre_ventas_netas(a):
    filas = por_clave(hv.resultados(a))
    assert filas["ventas_netas"]["pct2025"] == pytest.approx(100)
    assert filas["costo_ventas"]["pct2024"] == pytest.approx(64.9913, abs=0.0005)
    assert filas["utilidad_neta"]["pct2025"] == pytest.approx(2.2393, abs=0.0005)


def test_vertical_balance_sobre_activo_total(a):
    filas = por_clave(hv.balance(a))
    for pct in ("pct2024", "pct2025"):
        assert filas["total_activos"][pct] == pytest.approx(100)
        assert filas["total_pasivo_capital"][pct] == pytest.approx(100)
        assert sum(filas[k][pct] for k in
                   ("total_activo_circulante", "activos_fijos_netos", "total_otros_activos")) == pytest.approx(100)
