import pytest

from altamira import analisis, complementarios as comp


@pytest.fixture
def a(datos):
    return analisis.construir(datos)


def test_a_escudo_fiscal_de_la_depreciacion(a):
    r = comp.escudo_fiscal(a)
    assert r == pytest.approx({
        "depreciacion": 382000, "amortizacion": 44000, "gasto_no_efectivo": 426000, "tasa": 25,
        "escudo": 106500, "utilidad_neta": 208500, "utilidad_neta_sin": 528000,
        "flujo_operacion": 194500, "flujo_operacion_sin": 88000,
    })


def test_b_costo_despues_de_impuestos(a):
    r = comp.costo_despues_impuestos(a)
    filas = {f["concepto"]: (f["antes"], f["ahorro"], f["despues"]) for f in r["filas"]}
    assert filas["Gastos por intereses"] == pytest.approx((214000, 53500, 160500))
    assert filas["Arrendamientos"] == pytest.approx((156000, 39000, 117000))
    assert (r["total"]["antes"], r["total"]["despues"]) == pytest.approx((370000, 277500))


def test_c_valor_en_libros_por_accion(a):
    r = comp.valor_por_accion(a)
    assert r[2024]["valor_libros"] == pytest.approx(16.88125)
    assert r[2025]["valor_libros"] == pytest.approx(17.50875)
    assert (r[2025]["upa"], r[2025]["dividendo"]) == pytest.approx((1.0425, 0.415))
    assert r[2024]["dividendo"] == pytest.approx(0.915)
    assert r[2025]["razon_pago"] == pytest.approx(39.8082, abs=0.0005)


def test_c_precio_utilidad_requiere_precio_de_mercado(datos, a):
    assert comp.valor_por_accion(a)[2025]["precio_utilidad"] is None
    datos["complementarios"]["precio_accion"] = 20.85
    r = comp.valor_por_accion(analisis.construir(datos))
    assert r[2025]["precio_utilidad"] == pytest.approx(20)


def test_d_conciliacion_de_ventas_por_producto(a):
    r = comp.ventas_por_producto(a)
    assert [p["ventas"] for p in r["productos"]] == pytest.approx([5220000, 4320000])
    assert [p["participacion"] for p in r["productos"]] == pytest.approx([54.7170, 45.2830], abs=0.0005)
    assert r["total"] == pytest.approx(9540000) and r["concilia"]


def test_d_detecta_que_las_ventas_no_concilian(datos):
    datos["complementarios"]["cubetas_precio"] = 9.1
    r = comp.ventas_por_producto(analisis.construir(datos))
    assert not r["concilia"] and r["diferencia"] == pytest.approx(48000)


def test_e_utilidad_neta_contra_flujo_de_operacion(a):
    r = comp.utilidad_vs_flujo(a)
    assert r[2024]["diferencia"] == pytest.approx(-276000)
    assert r[2025]["diferencia"] == pytest.approx(14000)
    assert [(p["clave"], p["monto"]) for p in r[2025]["principales"]] == [
        ("inventarios", -285000), ("cxc", -267000), ("cxp", 125000)]
    assert [p["clave"] for p in r[2024]["principales"]] == ["inventarios", "cxc", "cxp"]


def test_f_du_pont_descompuesto_suma_la_variacion_del_roe(a):
    r = comp.du_pont_descompuesto(a)
    assert r["variacion"] == pytest.approx(-7.6185, abs=0.001)
    assert r["efecto_margen"] == pytest.approx(-7.886, abs=0.002)
    assert r["efecto_rotacion"] == pytest.approx(-0.153, abs=0.002)
    assert r["efecto_endeudamiento"] == pytest.approx(0.420, abs=0.002)
    assert r["efecto_margen"] + r["efecto_rotacion"] + r["efecto_endeudamiento"] == pytest.approx(r["variacion"])


def test_g_costo_de_la_politica_de_credito(a):
    r = comp.politica_credito(a)
    assert r["ventas_diarias"] == pytest.approx(25863.89, abs=0.01)
    assert r["dias_exceso"] == pytest.approx(5.0698, abs=0.0005)
    assert r["efectivo_inmovilizado"] == pytest.approx(131125)


def test_g_sin_exceso_no_hay_efectivo_inmovilizado(datos):
    datos["industria"]["ppc"] = 60
    r = comp.politica_credito(analisis.construir(datos))
    assert r["efectivo_inmovilizado"] == 0 and r["dias_exceso"] == 0
