class AFD:
    def __init__(self, estados, alfabeto, inicial, finales, transiciones):
        self.estados = set(estados)
        self.alfabeto = {s for s in alfabeto if s != "λ"}
        self.inicial = inicial
        self.finales = set(finales)
        self.transiciones = dict(transiciones)
        self._validar_estructura()

    def _validar_estructura(self):
        if self.inicial not in self.estados:
            raise ValueError("El estado inicial no pertenece al conjunto de estados")
        if not self.finales.issubset(self.estados):
            raise ValueError("Hay estados finales que no pertenecen al conjunto de estados")
        for (estado, simbolo), destino in self.transiciones.items():
            if estado not in self.estados:
                raise ValueError(f"Estado origen inválido: {estado}")
            if simbolo not in self.alfabeto:
                raise ValueError(f"Símbolo inválido en AFD: {simbolo}")
            if destino not in self.estados:
                raise ValueError(f"Estado destino inválido: {destino}")

    def validar(self, cadena):
        estado = self.inicial
        recorrido = [estado]

        for c in cadena:
            if c not in self.alfabeto:
                return False, recorrido, f"Símbolo inválido: {c}"

            if (estado, c) not in self.transiciones:
                return False, recorrido, "Transición no definida"

            estado = self.transiciones[(estado, c)]
            recorrido.append(estado)

        return estado in self.finales, recorrido, "OK"
