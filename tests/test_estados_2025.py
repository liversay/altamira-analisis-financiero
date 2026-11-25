"""Cifras 2025 calculadas a mano desde la balanza, independientes del código."""
import pytest

from altamira import analisis


@pytest.fixture
def a(datos):
    return analisis.construir(datos)


def test_estado_de_resultados_2025(a):
    er = a.resultados[2025]
    esperado = {"ventas_netas": 9311000, "costo_ventas": 6271000, "utilidad_bruta": 3040000,
                "total_gastos_operacion": 2522000, "uaii": 518000, "uai": 278000,
                "isr": 69500, "utilidad_neta": 208500, "upa": 1.0425}
    assert {k: er[k] for k in esperado} == pytest.approx(esperado)


def test_balance_general_2025_cuadra(a):
    bg = a.balances[2025]
    esperado = {"total_activo_circulante": 3204750, "activos_fijos_netos": 4123000,
                "total_otros_activos": 466000, "total_activos": 7793750,
                "total_pasivo_circulante": 1892000, "total_pasivos": 4292000,
                "utilidades_retenidas": 2101750, "total_capital": 3501750}
    assert {k: bg[k] for k in esperado} == pytest.approx(esperado)
    assert bg["cuadra"]


def test_cierre_de_utilidades_retenidas_2025(a):
    c = a.conciliacion_ur[2025]
    assert (c["saldo_inicial"], c["utilidad_neta"], c["dividendos"], c["saldo_final"]) == pytest.approx(
        (1976250, 208500, 83000, 2101750))
    assert c["concilia"]


def test_flujo_de_efectivo_2025_concilia_con_caja(a):
    flujo = a.flujos[2025]
    esperado = {"total_operacion": 194500, "total_inversion": -775000, "total_financiamiento": 481000,
                "cambio_neto": -99500, "caja_inicial": 437250, "caja_final": 337750,
                "dividendos_pagados": 89000, "flujo_libre": -669500}
    assert {k: flujo[k] for k in esperado} == pytest.approx(esperado)
    assert flujo["concilia"]
