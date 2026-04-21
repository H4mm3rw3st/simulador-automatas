def _nombre_estado_conjunto(conjunto):
    if not conjunto:
        return "∅"
    return "{" + ",".join(sorted(conjunto)) + "}"


def convertir_afnd_a_afd(afnd):
    inicial = frozenset([afnd.inicial])
    estados = {inicial}
    trans = {}
    finales = set()
    pendientes = [inicial]
    pasos = []

    while pendientes:
        actual = pendientes.pop(0)
        fila = {"estado": _nombre_estado_conjunto(actual), "transiciones": {}}

        for simbolo in sorted(afnd.alfabeto):
            nuevo = set()
            for e in actual:
                nuevo.update(afnd.transiciones.get((e, simbolo), set()))

            nuevo = frozenset(nuevo)
            fila["transiciones"][simbolo] = _nombre_estado_conjunto(nuevo)

            if nuevo:
                trans[(actual, simbolo)] = nuevo
                if nuevo not in estados:
                    estados.add(nuevo)
                    pendientes.append(nuevo)

        pasos.append(fila)

    for e in estados:
        if any(x in afnd.finales for x in e):
            finales.add(e)

    return estados, inicial, finales, trans, pasos


def eliminar_lambda(afndl):
    nuevas_trans = {}
    pasos = []

    for estado in sorted(afndl.estados):
        clausura = afndl.lambda_clausura({estado})
        detalle = {"estado": estado, "clausura": sorted(clausura), "transiciones": {}}

        for simbolo in sorted(s for s in afndl.alfabeto if s != "λ"):
            destinos = set()
            for e in clausura:
                for d in afndl.transiciones.get((e, simbolo), set()):
                    destinos.update(afndl.lambda_clausura({d}))

            if destinos:
                nuevas_trans[(estado, simbolo)] = set(destinos)
            detalle["transiciones"][simbolo] = sorted(destinos)

        pasos.append(detalle)

    nuevos_finales = set()
    for estado in afndl.estados:
        clausura = afndl.lambda_clausura({estado})
        if any(e in afndl.finales for e in clausura):
            nuevos_finales.add(estado)

    return afndl.estados, afndl.alfabeto - {"λ"}, afndl.inicial, nuevos_finales, nuevas_trans, pasos
