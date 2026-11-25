import json
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent


def _leer(nombre):
    return json.loads((RAIZ / "data" / nombre).read_text(encoding="utf-8"))


@pytest.fixture
def datos():
    return _leer("datos_base.json")


@pytest.fixture
def publicado():
    return _leer("publicado_2024.json")
