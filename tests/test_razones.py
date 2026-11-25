"""Las 13 razones del capítulo 3, con valores calculados a mano."""
import pytest

from altamira import analisis, razones

ESPERADO = {
    # clave: (2024, 2025)
    "margen_utilidad": (5.3440, 2.2393),
    "roa": (6.5603, 2.6752),
    "roe": (13.5727, 5.9542),
    "rotacion_cxc": (8.3414, 7.1900),
    "ppc": (43.1580, 50.0698),
    "rotacion_inventario": (7.4242, 6.4660),
    "rotacion_activos_fijos": (2.2989, 2.2583),
    "rotacion_activos_totales": (1.2276, 1.1947),
    "razon_circulante": (1.7994, 1.6938),
    "razon_rapida": (1.0585, 0.9328),
    "deuda_activos": (51.6660, 55.0698),
    "rotacion_interes": (4.7455, 2.4206),
    "cobertura_cargos_fijos": (3.0000, 1.8216),
}


@pytest.fixture
def a(datos):
    return analisis.construir(datos)


def test_son_13_razones_en_las_cuatro_categorias(datos):
    assert [d.clave for d in razones.DEFINICIONES] == list(ESPERADO)
    conteo = {}
    for d in razones.DEFINICIONES:
        conteo[d.categoria] = conteo.get(d.categoria, 0) + 1
    assert conteo == {"rentabilidad": 3, "utilizacion_activos": 5, "liquidez": 2, "utilizacion_deudas": 3}


@pytest.mark.parametrize("clave", ESPERADO)
def test_valor_de_cada_razon(a, clave):
    for anio, esperado in zip((2024, 2025), ESPERADO[clave]):
        assert razones.calcular(a, anio)[clave] == pytest.approx(esperado, abs=0.0005), anio


def test_division_entre_cero_da_no_disponible(datos):
    datos["balanza_2025"]["gastos_intereses"] = {"debe": 0, "haber": 0}
    assert razones.calcular(analisis.construir(datos), 2025)["rotacion_interes"] is None


@pytest.mark.parametrize("anio", [2024, 2025])
def test_du_pont_coincide_con_el_calculo_directo(a, anio):
    dp = razones.du_pont(a, anio)
    directo = razones.calcular(a, anio)
    assert dp["roa"] == pytest.approx(dp["margen"] * dp["rotacion"])
    assert dp["roa"] == pytest.approx(directo["roa"])
    assert dp["roe"] == pytest.approx(dp["roa"] / (1 - dp["deuda_activos"] / 100))
    assert dp["roe"] == pytest.approx(directo["roe"])


@pytest.mark.parametrize("valor,industria,mejor,color", [
    (2.0, 1.9, "mayor", "verde"),
    (1.9, 1.9, "mayor", "verde"),
    (1.71, 1.9, "mayor", "amarillo"),   # exactamente 10 % peor
    (1.70, 1.9, "mayor", "rojo"),
    (44, 45, "menor", "verde"),
    (49.5, 45, "menor", "amarillo"),
    (50, 45, "menor", "rojo"),
    (None, 45, "menor", "gris"),
])
def test_semaforo(valor, industria, mejor, color):
    assert razones.semaforo(valor, industria, mejor) == color


def test_tabla_compara_ambos_anios_con_la_industria(a):
    fila = next(f for f in razones.tabla(a) if f["clave"] == "ppc")
    assert fila["industria"] == 45
    assert (fila["semaforo_2024"], fila["semaforo_2025"]) == ("verde", "rojo")
    assert fila["tendencia"] == "empeora"


def test_comentario_por_categoria_usa_las_cifras_calculadas(a):
    comentarios = razones.comentarios(a)
    assert set(comentarios) == set(razones.CATEGORIAS)
    assert "2.24 %" in comentarios["rentabilidad"] and "4.50 %" in comentarios["rentabilidad"]
    assert "50.07 días" in comentarios["utilizacion_activos"]
    assert "1.69 veces" in comentarios["liquidez"]
    assert "2.42 veces" in comentarios["utilizacion_deudas"]


def test_comentario_cambia_cuando_cambian_los_datos(datos):
    antes = razones.comentarios(analisis.construir(datos))["utilizacion_deudas"]
    datos["balanza_2025"]["gastos_intereses"]["debe"] = 50000
    despues = razones.comentarios(analisis.construir(datos))["utilizacion_deudas"]
    assert antes != despues and "10.36 veces" in despues
