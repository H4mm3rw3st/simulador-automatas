import json
import xml.etree.ElementTree as ET


def leer_jff(ruta):
    tree = ET.parse(ruta)
    root = tree.getroot()

    estados = {}
    inicial = None
    finales = set()
    trans = {}
    alfabeto = set()

    for s in root.iter("state"):
        sid = s.get("id")
        nombre = s.get("name") or ("q" + sid)
        estados[sid] = nombre

        if s.find("initial") is not None:
            inicial = nombre
        if s.find("final") is not None:
            finales.add(nombre)

    for t in root.iter("transition"):
        o = estados[t.find("from").text]
        d = estados[t.find("to").text]
        lectura = t.find("read")
        simbolo = lectura.text if lectura is not None else None
        if simbolo is None:
            simbolo = "λ"

        alfabeto.add(simbolo)
        trans.setdefault((o, simbolo), []).append(d)

    return set(estados.values()), alfabeto, inicial, finales, trans


def exportar_json(ruta, tipo, estados, alfabeto, inicial, finales, transiciones):
    data = {
        "tipo": tipo,
        "estados": sorted(estados),
        "alfabeto": sorted(alfabeto),
        "inicial": inicial,
        "finales": sorted(finales),
        "transiciones": [
            {
                "origen": origen,
                "simbolo": simbolo,
                "destinos": sorted(destinos if isinstance(destinos, (set, list, tuple)) else [destinos]),
            }
            for (origen, simbolo), destinos in sorted(transiciones.items())
        ],
    }
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def exportar_txt(ruta, tipo, estados, alfabeto, inicial, finales, transiciones):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"Tipo: {tipo}\n")
        f.write(f"Estados: {', '.join(sorted(estados))}\n")
        f.write(f"Alfabeto: {', '.join(sorted(alfabeto))}\n")
        f.write(f"Inicial: {inicial}\n")
        f.write(f"Finales: {', '.join(sorted(finales))}\n")
        f.write("Transiciones:\n")
        for (origen, simbolo), destinos in sorted(transiciones.items()):
            if isinstance(destinos, (set, list, tuple)):
                destino_txt = ",".join(sorted(destinos))
            else:
                destino_txt = str(destinos)
            f.write(f"  {origen},{simbolo}->{destino_txt}\n")
