"""Modificar una cuenta de la balanza y ver cómo reaccionan las razones."""
import copy

import pytest

from altamira import ajustes, analisis, balanza, razones, validaciones


def direcciones(base, nuevos):
    cambios = razones.cambios(analisis.construir(base), analisis.construir(nuevos))
    return {c["clave"]: c["direccion"] for c in cambios}


def test_aumentar_cuentas_por_cobrar_contra_caja(datos):
    nuevos = ajustes.modificar(datos, "cxc_comerciales", 1435000, contrapartida="caja_bancos")
    assert nuevos["balanza_2025"]["caja_bancos"]["debe"] == 237750
    assert validaciones.alertas(analisis.construir(nuevos)) == []
    # los activos, pasivos y utilidad no cambian: solo la cobranza
    assert direcciones(datos, nuevos) == {"rotacion_cxc": "baja", "ppc": "sube"}


def test_aumentar_intereses_pagados_en_efectivo(datos):
    nuevos = ajustes.modificar(datos, "gastos_intereses", 264000, contrapartida="caja_bancos")
    a = analisis.construir(nuevos)
    assert a.resultados[2025]["utilidad_neta"] == pytest.approx(171000)
    # el ISR y el ISR por pagar se recalculan para que todo siga cuadrando
    saldos = balanza.saldos(nuevos["balanza_2025"])
    assert (saldos["isr_periodo"], saldos["isr_por_pagar"]) == pytest.approx((57000, 75500))
    assert validaciones.alertas(a) == []
    d = direcciones(datos, nuevos)
    assert {d[k] for k in ("margen_utilidad", "roa", "roe", "rotacion_interes", "cobertura_cargos_fijos")} == {"baja"}
    assert d["rotacion_activos_totales"] == "sube"
    assert "rotacion_cxc" not in d


def test_modificar_sin_contrapartida_descuadra_y_alerta(datos):
    nuevos = ajustes.modificar(datos, "cxc_comerciales", 1435000)
    codigos = {x["codigo"] for x in validaciones.alertas(analisis.construir(nuevos))}
    assert {"balanza_debe_haber", "balance_2025"} <= codigos


def test_contrapartida_acreedora(datos):
    nuevos = ajustes.modificar(datos, "cxc_comerciales", 1435000, contrapartida="ventas_brutas")
    assert nuevos["balanza_2025"]["ventas_brutas"]["haber"] == 9640000
    a = analisis.construir(nuevos)
    assert a.balances[2025]["cuadra"]
    assert a.resultados[2025]["utilidad_neta"] == pytest.approx(283500)


def test_no_altera_los_datos_recibidos(datos):
    copia = copy.deepcopy(datos)
    ajustes.modificar(datos, "cxc_comerciales", 1, contrapartida="caja_bancos")
    assert datos == copia


@pytest.mark.parametrize("clave,contrapartida", [("no_existe", None), ("caja_bancos", "caja_bancos"),
                                                  ("caja_bancos", "otra")])
def test_cuentas_invalidas(datos, clave, contrapartida):
    with pytest.raises(ValueError):
        ajustes.modificar(datos, clave, 100, contrapartida=contrapartida)


def test_alerta_si_utilidades_retenidas_2024_no_concilian(datos):
    datos["cuentas_2024"]["publicidad"] += 1000
    codigos = {x["codigo"] for x in validaciones.alertas(analisis.construir(datos))}
    assert "conciliacion_ur_2024" in codigos
