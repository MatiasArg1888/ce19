import json
import os
from core.app_state import state
from core.rutas import ruta_datos

class Historial:

    def __init__(self, cargar_ahora=True):
        self.archivo = ruta_datos("historial.json")
        self.lista = []
        self._cargado = False
        if cargar_ahora:
            self.cargar()
    # ---------------------------------------------

    def cargar(self):
        if self._cargado:
            return

        if os.path.exists(self.archivo):
            with open(
                self.archivo,
                "r",
                encoding="utf-8"
            ) as archivo:

                self.lista = json.load(archivo)
        else:
            self.guardar_archivo()

        self._cargado = True
    # ---------------------------------------------
    def agregar(self, registro):
        self.cargar()

        self.lista.insert(
            0,
            registro
        )

        self.guardar_archivo()
        state.notify('update')



    # ---------------------------------------------

    def obtener(self):
        self.cargar()

        return self.lista



    # ---------------------------------------------

    def guardar_archivo(self):

        carpeta = os.path.dirname(
            self.archivo
        )

        if not os.path.exists(carpeta):

            os.makedirs(carpeta)


        with open(
            self.archivo,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                self.lista,
                archivo,
                indent=4,
                ensure_ascii=False
            )
