from altamira import analisis, validaciones


def alertas_de(datos):
    return validaciones.alertas(analisis.construir(datos))


def codigos(datos):
    return {a["codigo"] for a in alertas_de(datos)}


def test_datos_originales_no_generan_alertas(datos):
    assert alertas_de(datos) == []


def test_alerta_cuando_el_balance_no_cuadra(datos):
    datos["balanza_2025"]["cxc_comerciales"]["debe"] += 100000
    alertas = alertas_de(datos)
    descuadre = next(a for a in alertas if a["codigo"] == "balance_2025")
    assert "Activos" in descuadre["mensaje"] and "100,000" in descuadre["mensaje"]
    assert "balanza_debe_haber" in codigos(datos)
    assert descuadre["nivel"] == "error"


def test_alerta_cuando_no_cuadra_el_balance_2024(datos):
    datos["cuentas_2024"]["caja_bancos"] += 1
    assert "balance_2024" in codigos(datos)


def test_alerta_si_el_isr_de_la_balanza_difiere_del_calculado(datos):
    datos["balanza_2025"]["gastos_intereses"]["debe"] += 40000
    assert "isr_2025" in codigos(datos)


def test_alerta_si_el_saldo_inicial_de_utilidades_retenidas_no_es_el_final_2024(datos):
    datos["balanza_2025"]["utilidades_retenidas"]["haber"] += 10
    assert "utilidades_retenidas" in codigos(datos)


def test_alerta_si_el_isr_capturado_de_2024_difiere_del_calculado(datos):
    datos["cuentas_2024"]["isr_periodo"] = 1
    assert "isr_2024" in codigos(datos)
