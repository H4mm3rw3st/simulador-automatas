class AFND:
    def __init__(self, estados, alfabeto, inicial, finales, transiciones):
        self.estados = set(estados)
        self.alfabeto = {s for s in alfabeto if s != "λ"}
        self.inicial = inicial
        self.finales = set(finales)
        self.transiciones = {
            (estado, simbolo): set(destinos)
            for (estado, simbolo), destinos in transiciones.items()
        }
        self._validar_estructura()

    def _validar_estructura(self):
        if self.inicial not in self.estados:
            raise ValueError("El estado inicial no pertenece al conjunto de estados")
        if not self.finales.issubset(self.estados):
            raise ValueError("Hay estados finales que no pertenecen al conjunto de estados")
        for (estado, simbolo), destinos in self.transiciones.items():
            if estado not in self.estados:
                raise ValueError(f"Estado origen inválido: {estado}")
            if simbolo not in self.alfabeto:
                raise ValueError(f"Símbolo inválido en AFND: {simbolo}")
            for destino in destinos:
                if destino not in self.estados:
                    raise ValueError(f"Estado destino inválido: {destino}")

    def mover(self, estados, simbolo):
        nuevos = set()
        for estado in estados:
            nuevos.update(self.transiciones.get((estado, simbolo), set()))
        return nuevos

    def validar(self, cadena):
        actuales = {self.inicial}
        recorrido = [actuales.copy()]

        for c in cadena:
            if c not in self.alfabeto:
                return False, recorrido, f"Símbolo inválido: {c}"
            actuales = self.mover(actuales, c)
            recorrido.append(actuales.copy())

        return any(e in self.finales for e in actuales), recorrido
