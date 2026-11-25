import re
from pathlib import Path

import pytest

from app import crear_app

PAGINAS = ["/", "/captura", "/captura?pestana=2024", "/captura?pestana=2023",
           "/captura?pestana=complementarios", "/resultados", "/balance", "/flujo",
           "/flujo?anio=2024", "/razones", "/analisis", "/complementarios", "/manual"]


@pytest.fixture
def app(tmp_path):
    return crear_app(ruta_actual=tmp_path / "datos.json", pruebas=True)


@pytest.fixture
def cliente(app):
    return app.test_client()


def html(cliente, ruta):
    respuesta = cliente.get(ruta)
    assert respuesta.status_code == 200, ruta
    return respuesta.get_data(as_text=True)


@pytest.mark.parametrize("ruta", PAGINAS)
def test_cada_pantalla_responde(cliente, ruta):
    html(cliente, ruta)


@pytest.mark.parametrize("ruta", PAGINAS)
def test_ninguna_pantalla_menciona_contexto_academico(cliente, ruta):
    texto = html(cliente, ruta).lower()
    assert not re.search(r"parcial|universidad|\butp\b|examen|estudiante|sustentaci", texto)


def test_menu_enlaza_los_modulos_y_el_manual(cliente):
    pagina = html(cliente, "/")
    for ruta in ("/captura", "/resultados", "/balance", "/flujo", "/razones", "/analisis",
                 "/complementarios", "/manual"):
        assert f'href="{ruta}"' in pagina
    assert "Balance cuadrado" in pagina and "2024 reproducido" in pagina


@pytest.mark.parametrize("ruta,cifra", [
    ("/resultados", "208,500"), ("/balance", "7,793,750"), ("/balance", "2,101,750"),
    ("/flujo", "(669,500)"), ("/flujo?anio=2024", "227,250"), ("/razones", "50.07 días"),
    ("/analisis", "25.94 %"), ("/complementarios", "131,125")])
def test_las_pantallas_muestran_las_cifras_calculadas(cliente, ruta, cifra):
    assert cifra in html(cliente, ruta)


def test_sin_cambios_no_hay_alertas(cliente):
    assert 'role="alert"' not in html(cliente, "/resultados")


def test_guardar_una_cuenta_descuadrada_muestra_alerta_en_todas_las_pantallas(cliente):
    r = cliente.post("/captura", data={"pestana": "2025", "b25_cxc_comerciales_debe": "1,435,000"})
    assert r.status_code == 302
    for ruta in ("/captura", "/balance", "/razones"):
        pagina = html(cliente, ruta)
        assert 'role="alert"' in pagina and "no cuadra" in pagina
    assert "Balance descuadrado" in html(cliente, "/")


def test_ajuste_con_contrapartida_recalcula_y_muestra_razones_cambiadas(cliente):
    r = cliente.post("/captura/ajuste", data={"cuenta": "gastos_intereses", "saldo": "264,000",
                                              "contrapartida": "caja_bancos"}, follow_redirects=True)
    pagina = r.get_data(as_text=True)
    assert 'role="alert"' not in pagina
    assert "Razones que cambiaron" in pagina and "Rotación del interés ganado" in pagina
    assert "171,000" in html(cliente, "/resultados")


def test_valor_invalido_informa_y_no_guarda(cliente):
    r = cliente.post("/captura", data={"pestana": "2025", "b25_caja_bancos_debe": "hola"},
                     follow_redirects=True)
    assert "no es un monto válido" in r.get_data(as_text=True)
    assert "208,500" in html(cliente, "/resultados")


def test_ajuste_invalido_informa(cliente):
    r = cliente.post("/captura/ajuste", data={"cuenta": "caja_bancos", "saldo": "1",
                                              "contrapartida": "caja_bancos"}, follow_redirects=True)
    assert "otra cuenta" in r.get_data(as_text=True)


def test_restaurar_vuelve_a_los_datos_originales(cliente):
    cliente.post("/captura/ajuste", data={"cuenta": "gastos_intereses", "saldo": "264000",
                                          "contrapartida": "caja_bancos"})
    cliente.post("/restaurar")
    assert "208,500" in html(cliente, "/resultados")


def test_las_pantallas_resisten_denominadores_en_cero(cliente):
    cliente.post("/captura", data={"pestana": "2025", "b25_gastos_intereses_debe": "0",
                                   "b25_ventas_brutas_haber": "0", "b25_devoluciones_ventas_debe": "0"})
    for ruta in PAGINAS:
        html(cliente, ruta)


def test_manual_pdf_tiene_como_maximo_tres_paginas(cliente):
    pdf = Path(__file__).resolve().parent.parent / "docs" / "manual_usuario.pdf"
    assert pdf.exists()
    paginas = len(re.findall(rb"/Type\s*/Page(?![s\w])", pdf.read_bytes()))
    assert 1 <= paginas <= 3
    assert cliente.get("/manual.pdf").mimetype == "application/pdf"
