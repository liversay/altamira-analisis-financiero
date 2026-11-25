import pytest

from altamira import captura
from altamira.repositorio import Repositorio


@pytest.mark.parametrize("texto,numero", [
    ("1,335,000", 1335000), ("US$ 4.50", 4.5), ("(5,000)", -5000), ("", 0), ("  72000 ", 72000)])
def test_lee_montos_escritos_por_el_usuario(texto, numero):
    assert captura.leer_numero(texto) == numero


@pytest.mark.parametrize("texto", ["abc", "12..5", "nan", "inf", "1e999"])
def test_rechaza_lo_que_no_es_un_monto(texto):
    with pytest.raises(ValueError):
        captura.leer_numero(texto)


def test_aplica_solo_los_campos_enviados(datos):
    nuevos, errores = captura.aplicar(datos, {"b25_caja_bancos_debe": "400,000", "c24_publicidad": "1",
                                              "comp_acciones": "100000", "ind_ppc": "30"})
    assert errores == []
    assert nuevos["balanza_2025"]["caja_bancos"] == {"debe": 400000, "haber": 0}
    assert nuevos["cuentas_2024"]["publicidad"] == 1
    assert (nuevos["complementarios"]["acciones"], nuevos["industria"]["ppc"]) == (100000, 30)
    assert datos["cuentas_2024"]["publicidad"] == 172000


@pytest.mark.parametrize("campos", [
    {"b25_caja_bancos_debe": "x"}, {"b25_caja_bancos_debe": "-1"}, {"comp_acciones": "0"},
    {"comp_dias_anio": "0"}, {"ind_ppc": "0"}, {"comp_tasa_isr": "101"}, {"c23_terrenos": "-5"}])
def test_un_valor_invalido_no_guarda_nada(datos, campos):
    nuevos, errores = captura.aplicar(datos, {"c24_publicidad": "1", **campos})
    assert errores and nuevos == datos


def test_repositorio_guarda_y_restaura(tmp_path, datos):
    base = tmp_path / "base.json"
    Repositorio(base, base).guardar(datos)
    repo = Repositorio(base, tmp_path / "actual.json")
    assert repo.cargar() == datos
    cambiado = repo.cargar()
    cambiado["cuentas_2024"]["publicidad"] = 9
    repo.guardar(cambiado)
    assert repo.cargar()["cuentas_2024"]["publicidad"] == 9
    assert repo.original() == datos and repo.modificado()
    repo.restaurar()
    assert repo.cargar() == datos and not repo.modificado()
