from logica.codificador import Codificador, normalizar_texto_codificador
from logica.diccionarios import ALFABETO_COMPLETO
from services.biblia_service import BibliaService


class CalculadoraBibliaService:
    """Suma valores de texto biblico usando el alfabeto completo de 29 letras."""

    def __init__(self):
        motor = Codificador(ALFABETO_COMPLETO)
        self.diccionario = motor.crear_diccionario(
            usar_ch=True,
            usar_ll=True,
            usar_enie=True,
        )
        self._cache_biblia_completa = None

    def sumar_texto(self, texto):
        texto = normalizar_texto_codificador(texto)
        total = 0
        cantidad = 0
        indice = 0

        while indice < len(texto):
            par = texto[indice:indice + 2]

            if par == "CH" and "CH" in self.diccionario:
                total += self.diccionario["CH"]
                cantidad += 1
                indice += 2
                continue

            if par == "LL" and "LL" in self.diccionario:
                total += self.diccionario["LL"]
                cantidad += 1
                indice += 2
                continue

            letra = texto[indice]
            valor = self.diccionario.get(letra)

            if valor is not None:
                total += valor
                cantidad += 1

            indice += 1

        return total, cantidad

    def sumar_textos(self, textos):
        total = 0
        cantidad = 0

        for texto in textos:
            subtotal, subcantidad = self.sumar_texto(texto)
            total += subtotal
            cantidad += subcantidad

        return total, cantidad

    def sumar_versiculos(self, libro_nombre, capitulo, versiculo_inicio, versiculo_fin):
        capitulo = int(capitulo)
        inicio, fin = sorted((int(versiculo_inicio), int(versiculo_fin)))
        versiculos = BibliaService.obtener_capitulo(libro_nombre, capitulo)
        seleccion = versiculos[inicio - 1:fin]
        total, cantidad = self.sumar_textos(seleccion)
        referencia = (
            f"{libro_nombre} {capitulo}:{inicio}"
            if inicio == fin
            else f"{libro_nombre} {capitulo}:{inicio}-{fin}"
        )
        return self._resultado("Versiculos", referencia, total, cantidad)

    def sumar_capitulos(self, libro_nombre, capitulo_inicio, capitulo_fin):
        inicio, fin = sorted((int(capitulo_inicio), int(capitulo_fin)))
        libro = BibliaService.libro_por_nombre(libro_nombre)
        capitulos = libro.get("capitulos", []) if libro else []

        def textos():
            for capitulo in capitulos[inicio - 1:fin]:
                for versiculo in capitulo:
                    yield versiculo

        total, cantidad = self.sumar_textos(textos())
        referencia = (
            f"{libro_nombre} {inicio}"
            if inicio == fin
            else f"{libro_nombre} {inicio}-{fin}"
        )
        return self._resultado("Capitulos", referencia, total, cantidad)

    def sumar_libros(self, libro_inicio, libro_fin=None):
        libros = BibliaService.libros()
        nombres = [libro.get("nombre", "") for libro in libros]
        normalizados = {
            BibliaService.normalizar(nombre): nombre
            for nombre in nombres
        }
        libro_inicio = normalizados.get(
            BibliaService.normalizar(libro_inicio),
            libro_inicio,
        )
        libro_fin = normalizados.get(
            BibliaService.normalizar(libro_fin),
            libro_fin,
        )

        if libro_inicio not in nombres:
            return self._resultado("Libros", str(libro_inicio or ""), 0, 0)

        if libro_fin not in nombres:
            libro_fin = libro_inicio

        inicio, fin = sorted((nombres.index(libro_inicio), nombres.index(libro_fin)))
        seleccion = libros[inicio:fin + 1]

        def textos():
            for libro in seleccion:
                for capitulo in libro.get("capitulos", []):
                    for versiculo in capitulo:
                        yield versiculo

        total, cantidad = self.sumar_textos(textos())
        referencia = (
            libro_inicio
            if libro_inicio == libro_fin
            else f"{libro_inicio} - {libro_fin}"
        )
        return self._resultado("Libros", referencia, total, cantidad)

    def sumar_biblia_completa(self):
        if self._cache_biblia_completa is not None:
            return self._cache_biblia_completa.copy()

        def textos():
            for libro in BibliaService.libros():
                for capitulo in libro.get("capitulos", []):
                    for versiculo in capitulo:
                        yield versiculo

        total, cantidad = self.sumar_textos(textos())
        self._cache_biblia_completa = self._resultado(
            "Biblia completa",
            "Biblia completa",
            total,
            cantidad,
        )
        return self._cache_biblia_completa.copy()

    def _resultado(self, alcance, referencia, total, cantidad):
        return {
            "alcance": alcance,
            "referencia": referencia,
            "total": total,
            "cantidad_letras": cantidad,
            "alfabeto": "Espanol antiguo 29 letras",
        }
