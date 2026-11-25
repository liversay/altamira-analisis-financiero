"""Prueba de aceptación: el sistema reproduce exactamente los estados 2024."""
import pytest

from altamira import analisis


@pytest.fixture
def a(datos):
    return analisis.construir(datos)


def test_estado_de_resultados_2024(a, publicado):
    er = a.resultados[2024]
    for concepto, esperado in publicado["resultados"].items():
        assert er[concepto] == pytest.approx(esperado), concepto


def test_utilidad_por_accion_2024(a, publicado):
    assert round(a.resultados[2024]["upa"], 2) == publicado["upa"]


def test_balance_general_2024(a, publicado):
    bg = a.balances[2024]
    for concepto, esperado in publicado["balance"].items():
        assert bg[concepto] == pytest.approx(esperado), concepto
    assert bg["cuadra"]


def test_utilidades_retenidas_2024_concilian_con_2023(a):
    c = a.conciliacion_ur[2024]
    assert (c["saldo_inicial"], c["utilidad_neta"], c["dividendos"]) == (1701000, 458250, 183000)
    assert c["saldo_final"] == pytest.approx(1976250)
    assert c["concilia"]


def test_totales_del_flujo_de_efectivo_2024(a, publicado):
    flujo = a.flujos[2024]
    for concepto, esperado in publicado["flujo"].items():
        assert flujo[concepto] == pytest.approx(esperado), concepto
    assert flujo["concilia"]


def test_cada_renglon_del_flujo_2024(a):
    flujo = a.flujos[2024]
    renglones = {r["clave"]: r["monto"] for s in ("operacion", "inversion", "financiamiento") for r in flujo[s]}
    esperado = {
        "utilidad_neta": 458250, "depreciacion": 330000, "amortizacion": 40000,
        "cxc": -77000, "inventarios": -85000, "anticipados": -5000,
        "cxp": 45000, "acumulados": 13000, "isr": 15000,
        "activos_fijos": -330000, "intangibles": -30000, "valores_negociables": 30000,
        "inversiones_lp": 0, "documentos": 50000, "deuda_lp": -150000, "dividendos": -177000,
    }
    assert renglones == pytest.approx(esperado)


def test_comparacion_contra_lo_publicado_aprueba_todo(a, publicado):
    filas = analisis.validar_2024(a, publicado)
    assert len(filas) == 23
    assert all(f["ok"] for f in filas)


def test_comparacion_detecta_una_cuenta_2024_alterada(datos, publicado):
    datos["cuentas_2024"]["publicidad"] += 1000
    filas = analisis.validar_2024(analisis.construir(datos), publicado)
    assert not next(f for f in filas if f["concepto"] == "utilidad_neta")["ok"]
