def eliminar_inaccesibles(afd):
    visitados = set()
    stack = [afd.inicial]

    while stack:
        estado = stack.pop()
        if estado in visitados:
            continue
        visitados.add(estado)
        for c in afd.alfabeto:
            destino = afd.transiciones.get((estado, c))
            if destino is not None:
                stack.append(destino)

    return visitados


def _clave_par(p, q):
    return tuple(sorted((p, q)))


def minimizar_afd(afd):
    accesibles = eliminar_inaccesibles(afd)
    estados = sorted(accesibles)
    tabla = {}
    pasos = []

    for i in range(len(estados)):
        for j in range(i):
            p, q = estados[i], estados[j]
            tabla[(p, q)] = ((p in afd.finales) != (q in afd.finales))

    pasos.append({
        "fase": "Inicialización",
        "descripcion": "Se marcan pares distinguibles por pertenencia a estados finales.",
        "tabla": tabla.copy(),
    })

    cambio = True
    while cambio:
        cambio = False
        for (p, q) in list(tabla.keys()):
            if tabla[(p, q)]:
                continue
            for s in sorted(afd.alfabeto):
                p1 = afd.transiciones.get((p, s))
                q1 = afd.transiciones.get((q, s))
                if p1 is None or q1 is None or p1 == q1:
                    continue
                key = _clave_par(p1, q1)
                if key in tabla and tabla[key]:
                    tabla[(p, q)] = True
                    pasos.append({
                        "fase": "Marcado",
                        "descripcion": f"Se marca ({p}, {q}) porque con '{s}' va a ({p1}, {q1}) que ya era distinguible.",
                        "tabla": tabla.copy(),
                    })
                    cambio = True
                    break

    grupos = []
    usados = set()
    for estado in estados:
        if estado in usados:
            continue
        grupo = {estado}
        for otro in estados:
            if otro == estado or otro in usados:
                continue
            key = _clave_par(estado, otro)
            if key in tabla and not tabla[key]:
                grupo.add(otro)
        usados.update(grupo)
        grupos.append(frozenset(grupo))

    nuevo_inicial = next(g for g in grupos if afd.inicial in g)
    nuevo_finales = {g for g in grupos if any(e in afd.finales for e in g)}
    nuevo_trans = {}

    for g in grupos:
        representante = sorted(g)[0]
        for s in sorted(afd.alfabeto):
            destino = afd.transiciones.get((representante, s))
            if destino is None:
                continue
            grupo_dest = next(gr for gr in grupos if destino in gr)
            nuevo_trans[(g, s)] = grupo_dest

    return {
        "accesibles": accesibles,
        "inaccesibles": afd.estados - accesibles,
        "tabla": tabla,
        "grupos": grupos,
        "nuevo_estados": grupos,
        "nuevo_inicial": nuevo_inicial,
        "nuevo_finales": nuevo_finales,
        "nuevo_transiciones": nuevo_trans,
        "pasos": pasos,
    }
