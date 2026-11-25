"""Persistencia de los datos de entrada en JSON. Nunca se guardan cifras derivadas."""
import json
import os
from pathlib import Path


class Repositorio:
    def __init__(self, ruta_base, ruta_actual):
        self.ruta_base = Path(ruta_base)
        self.ruta_actual = Path(ruta_actual)

    @staticmethod
    def _leer(ruta):
        return json.loads(ruta.read_text(encoding="utf-8"))

    def original(self):
        return self._leer(self.ruta_base)

    def cargar(self):
        return self._leer(self.ruta_actual) if self.ruta_actual.exists() else self.original()

    def modificado(self):
        return self.cargar() != self.original()

    def guardar(self, datos):
        temporal = self.ruta_actual.with_name(self.ruta_actual.name + ".tmp")
        temporal.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")
        os.replace(temporal, self.ruta_actual)

    def restaurar(self):
        if self.ruta_actual != self.ruta_base:
            self.ruta_actual.unlink(missing_ok=True)
