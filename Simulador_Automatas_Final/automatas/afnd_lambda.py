from automatas.afnd import AFND


class AFNDLambda(AFND):
    def __init__(self, estados, alfabeto, inicial, finales, transiciones):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
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
            if simbolo != "λ" and simbolo not in self.alfabeto:
                raise ValueError(f"Símbolo inválido en AFND-λ: {simbolo}")
            for destino in destinos:
                if destino not in self.estados:
                    raise ValueError(f"Estado destino inválido: {destino}")

    def lambda_clausura(self, estados):
        stack = list(estados)
        clausura = set(estados)

        while stack:
            estado = stack.pop()
            for destino in self.transiciones.get((estado, "λ"), set()):
                if destino not in clausura:
                    clausura.add(destino)
                    stack.append(destino)

        return clausura

    def validar(self, cadena):
        simbolos = {s for s in self.alfabeto if s != "λ"}
        actuales = self.lambda_clausura({self.inicial})
        recorrido = [{"simbolo": "λ*", "activos": actuales.copy()}]

        for c in cadena:
            if c not in simbolos:
                return False, recorrido, f"Símbolo inválido: {c}"

            nuevos = set()
            for estado in actuales:
                nuevos.update(self.transiciones.get((estado, c), set()))

            actuales = self.lambda_clausura(nuevos)
            recorrido.append({"simbolo": c, "activos": actuales.copy()})

        return any(e in self.finales for e in actuales), recorrido
