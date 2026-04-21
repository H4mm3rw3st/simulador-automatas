from pathlib import Path
import flet as ft

from automatas.afd import AFD
from automatas.afnd import AFND
from automatas.afnd_lambda import AFNDLambda
from automatas.conversion import convertir_afnd_a_afd, eliminar_lambda
from automatas.minimizacion import minimizar_afd
from extras.operaciones import subcadenas, prefijos, sufijos, kleene
from utils.jff_reader import leer_jff, exportar_json, exportar_txt


BASE_DIR = Path(__file__).resolve().parent
SALIDA_DIR = BASE_DIR / "salidas"
SALIDA_DIR.mkdir(exist_ok=True)


def texto_conjunto(conjunto):
    if not conjunto:
        return "∅"
    if isinstance(conjunto, frozenset):
        conjunto = set(conjunto)
    if isinstance(conjunto, set):
        return "{" + ", ".join(sorted(conjunto)) + "}"
    return str(conjunto)


def main(page: ft.Page):
    page.title = "Simulador de Autómatas"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 1200
    page.window_height = 900

    tipo = ft.Dropdown(
        label="Tipo de autómata",
        options=[
            ft.dropdown.Option("AFD"),
            ft.dropdown.Option("AFND"),
            ft.dropdown.Option("AFND-λ"),
        ],
        value="AFD",
        width=220,
    )
    estados = ft.TextField(label="Estados", hint_text="q0,q1,q2")
    alfabeto = ft.TextField(label="Alfabeto", hint_text="0,1,λ")
    inicial = ft.TextField(label="Estado inicial", hint_text="q0")
    finales = ft.TextField(label="Estados finales", hint_text="q1,q2")
    transiciones = ft.TextField(
        label="Transiciones",
        multiline=True,
        min_lines=4,
        max_lines=8,
        hint_text="q0,0->q0;q0,1->q1;q1,0->q1",
    )
    cadena = ft.TextField(label="Cadena a validar", hint_text="0101")
    ruta_jff = ft.TextField(label="Ruta archivo .jff")
    ruta_cadenas = ft.TextField(label="Ruta archivo de cadenas (.txt)")
    estado_clausura = ft.TextField(label="Estado para λ-clausura", hint_text="q0")

    resultado = ft.Text(selectable=True)
    salida = ft.Text(selectable=True)
    detalles = ft.Column(scroll=ft.ScrollMode.AUTO, height=350)

    def notificar(msg, color=ft.Colors.BLUE_200):
        page.snack_bar = ft.SnackBar(ft.Text(msg, color=color), open=True)
        page.update()

    def parse_lista(valor):
        return [x.strip() for x in valor.split(",") if x.strip()]

    def parsear():
        est = set(parse_lista(estados.value or ""))
        alf = set(parse_lista(alfabeto.value or ""))
        ini = (inicial.value or "").strip()
        fin = set(parse_lista(finales.value or ""))

        if not est:
            raise ValueError("Debes capturar al menos un estado")
        if not ini:
            raise ValueError("Debes capturar el estado inicial")

        trans = {}
        texto = (transiciones.value or "").replace("\n", ";")
        for r in texto.split(";"):
            r = r.strip()
            if not r:
                continue
            if "->" not in r or "," not in r:
                raise ValueError(f"Transición con formato inválido: {r}")
            izq, der = r.split("->", 1)
            origen, simbolo = [x.strip() for x in izq.split(",", 1)]
            destinos = [x.strip() for x in der.split(",") if x.strip()]
            if not destinos:
                raise ValueError(f"La transición no tiene destinos: {r}")
            trans[(origen, simbolo)] = destinos
        return est, alf, ini, fin, trans

    def limpiar_detalles():
        detalles.controls.clear()

    def agregar_linea(txt, bold=False):
        detalles.controls.append(ft.Text(txt, weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL, selectable=True))

    def construir_objeto():
        est, alf, ini, fin, trans = parsear()
        if tipo.value == "AFD":
            t = {}
            for k, v in trans.items():
                if len(v) != 1:
                    raise ValueError("En un AFD cada transición debe tener exactamente un destino")
                t[k] = v[0]
            return AFD(est, alf, ini, fin, t)
        if tipo.value == "AFND":
            return AFND(est, alf, ini, fin, trans)
        return AFNDLambda(est, alf, ini, fin, trans)

    def validar_cadena(e):
        try:
            limpiar_detalles()
            automata = construir_objeto()
            if tipo.value == "AFD":
                ok, rec, msg = automata.validar(cadena.value or "")
                for i, estado in enumerate(rec):
                    agregar_linea(f"Paso {i}: {estado}")
                agregar_linea(f"Estado final del recorrido: {rec[-1] if rec else automata.inicial}")
                agregar_linea(f"Mensaje: {msg}")
            else:
                ok, rec = automata.validar(cadena.value or "")[:2]
                for i, paso in enumerate(rec):
                    if isinstance(paso, dict):
                        agregar_linea(f"Paso {i} ({paso['simbolo']}): {texto_conjunto(paso['activos'])}")
                    else:
                        agregar_linea(f"Paso {i}: {texto_conjunto(paso)}")
            resultado.value = "ACEPTADA" if ok else "RECHAZADA"
        except Exception as ex:
            resultado.value = f"Error: {ex}"
        page.update()

    def cargar_jff_ui(e):
        try:
            est, alf, ini, fin, trans = leer_jff((ruta_jff.value or "").strip())
            estados.value = ",".join(sorted(est))
            alfabeto.value = ",".join(sorted(alf))
            inicial.value = ini
            finales.value = ",".join(sorted(fin))
            reglas = []
            for (o, s), d in sorted(trans.items()):
                reglas.append(f"{o},{s}->{','.join(d)}")
            transiciones.value = ";".join(reglas)
            resultado.value = "Archivo .jff cargado correctamente"
        except Exception as ex:
            resultado.value = f"Error: {ex}"
        page.update()

    def mostrar_clausura(e):
        try:
            limpiar_detalles()
            automata = construir_objeto()
            if not isinstance(automata, AFNDLambda):
                raise ValueError("La λ-clausura solo aplica para AFND-λ")
            objetivo = (estado_clausura.value or "").strip() or automata.inicial
            if objetivo not in automata.estados:
                raise ValueError("El estado solicitado no existe")
            clausura = automata.lambda_clausura({objetivo})
            salida.value = f"λ-clausura({objetivo}) = {texto_conjunto(clausura)}"
            agregar_linea(f"λ-clausura de {objetivo}: {texto_conjunto(clausura)}", bold=True)
        except Exception as ex:
            salida.value = f"Error: {ex}"
        page.update()

    def eliminar_lambda_ui(e):
        try:
            limpiar_detalles()
            automata = construir_objeto()
            if not isinstance(automata, AFNDLambda):
                raise ValueError("Selecciona AFND-λ para eliminar transiciones lambda")
            est2, alf2, ini2, fin2, trans2, pasos = eliminar_lambda(automata)
            salida.value = f"AFND sin λ generado. Estados: {len(est2)} | Finales: {sorted(fin2)}"
            for paso in pasos:
                agregar_linea(f"Estado {paso['estado']} | λ-clausura = {paso['clausura']}", bold=True)
                for simb, dest in paso["transiciones"].items():
                    agregar_linea(f"  con '{simb}' -> {dest}")
            exportar_txt(str(SALIDA_DIR / "afnd_sin_lambda.txt"), "AFND", est2, alf2, ini2, fin2, trans2)
        except Exception as ex:
            salida.value = f"Error: {ex}"
        page.update()

    def convertir_ui(e):
        try:
            limpiar_detalles()
            automata = construir_objeto()
            if isinstance(automata, AFNDLambda):
                raise ValueError("Primero elimina λ o captura un AFND sin λ")
            if not isinstance(automata, AFND) or isinstance(automata, AFD):
                raise ValueError("Selecciona AFND para aplicar subconjuntos")
            estados_afd, ini, fin_afd, trans_afd, pasos = convertir_afnd_a_afd(automata)
            salida.value = f"AFD generado por subconjuntos con {len(estados_afd)} estados"
            for paso in pasos:
                agregar_linea(f"Estado DFA {paso['estado']}", bold=True)
                for simb, dest in paso['transiciones'].items():
                    agregar_linea(f"  con '{simb}' -> {dest}")
            exportar_txt(str(SALIDA_DIR / "afd_convertido.txt"), "AFD", {texto_conjunto(e) for e in estados_afd}, automata.alfabeto, texto_conjunto(ini), {texto_conjunto(f) for f in fin_afd}, {(texto_conjunto(k[0]), k[1]): texto_conjunto(v) for k, v in trans_afd.items()})
        except Exception as ex:
            salida.value = f"Error: {ex}"
        page.update()

    def minimizar_ui(e):
        try:
            limpiar_detalles()
            automata = construir_objeto()
            if not isinstance(automata, AFD):
                raise ValueError("La minimización solo aplica a un AFD")
            res = minimizar_afd(automata)
            eliminados = len(automata.estados) - len(res['nuevo_estados'])
            salida.value = (
                f"AFD original: {len(automata.estados)} estados | "
                f"AFD mínimo: {len(res['nuevo_estados'])} estados | "
                f"Eliminados/Fusionados: {eliminados}"
            )
            agregar_linea(f"Estados accesibles: {sorted(res['accesibles'])}", bold=True)
            agregar_linea(f"Estados inaccesibles: {sorted(res['inaccesibles'])}")
            agregar_linea("Grupos equivalentes:", bold=True)
            for g in res['grupos']:
                agregar_linea(f"  {texto_conjunto(g)}")
            agregar_linea("Tabla de pares distinguibles:", bold=True)
            for (p, q), marcado in sorted(res['tabla'].items()):
                agregar_linea(f"  ({p}, {q}) -> {'X' if marcado else '≡'}")
            exportar_txt(str(SALIDA_DIR / "afd_minimo.txt"), "AFD mínimo", {texto_conjunto(g) for g in res['nuevo_estados']}, automata.alfabeto, texto_conjunto(res['nuevo_inicial']), {texto_conjunto(g) for g in res['nuevo_finales']}, {(texto_conjunto(k[0]), k[1]): texto_conjunto(v) for k, v in res['nuevo_transiciones'].items()})
        except Exception as ex:
            salida.value = f"Error: {ex}"
        page.update()

    def exportar_actual_json(e):
        try:
            est, alf, ini, fin, trans = parsear()
            ruta = SALIDA_DIR / "automata_exportado.json"
            exportar_json(str(ruta), tipo.value, est, alf, ini, fin, trans)
            salida.value = f"Exportado en: {ruta}"
        except Exception as ex:
            salida.value = f"Error: {ex}"
        page.update()

    def exportar_actual_txt(e):
        try:
            est, alf, ini, fin, trans = parsear()
            ruta = SALIDA_DIR / "automata_exportado.txt"
            exportar_txt(str(ruta), tipo.value, est, alf, ini, fin, trans)
            salida.value = f"Exportado en: {ruta}"
        except Exception as ex:
            salida.value = f"Error: {ex}"
        page.update()

    def pruebas_multiples_ui(e):
        try:
            automata = construir_objeto()
            ruta = Path((ruta_cadenas.value or "").strip())
            if not ruta.exists():
                raise ValueError("La ruta del archivo de cadenas no existe")
            lineas = [ln.rstrip("\n") for ln in ruta.read_text(encoding="utf-8").splitlines()]
            reporte = []
            for ln in lineas:
                if isinstance(automata, AFD):
                    ok, _, _ = automata.validar(ln)
                else:
                    ok = automata.validar(ln)[0]
                reporte.append(f"{ln!r}: {'ACEPTADA' if ok else 'RECHAZADA'}")
            out = SALIDA_DIR / "reporte_cadenas.txt"
            out.write_text("\n".join(reporte), encoding="utf-8")
            salida.value = f"Reporte generado en: {out}"
            limpiar_detalles()
            for r in reporte:
                agregar_linea(r)
        except Exception as ex:
            salida.value = f"Error: {ex}"
        page.update()

    def ver_sub(e):
        salida.value = "Subcadenas:\n" + str(subcadenas(cadena.value or ""))
        page.update()

    def ver_pref(e):
        salida.value = "Prefijos:\n" + str(prefijos(cadena.value or ""))
        page.update()

    def ver_suf(e):
        salida.value = "Sufijos:\n" + str(sufijos(cadena.value or ""))
        page.update()

    def ver_kleene(e):
        salida.value = "Kleene (hasta longitud 3):\n" + str(kleene(parse_lista(alfabeto.value or "")))
        page.update()

    page.add(
        ft.Column(
            controls=[
                ft.Text("Simulador de Autómatas", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("AFD, AFND, AFND-λ, conversión, λ-clausura, minimización, importación/exportación y pruebas múltiples."),
                ft.ResponsiveRow([
                    ft.Container(ft.Column([tipo, estados, alfabeto, inicial, finales, estado_clausura]), col={"md": 6}),
                    ft.Container(ft.Column([transiciones, cadena, ruta_jff, ruta_cadenas]), col={"md": 6}),
                ]),
                ft.Wrap([
                    ft.ElevatedButton("Validar cadena", on_click=validar_cadena),
                    ft.ElevatedButton("Cargar JFF", on_click=cargar_jff_ui),
                    ft.ElevatedButton("Mostrar λ-clausura", on_click=mostrar_clausura),
                    ft.ElevatedButton("Eliminar λ", on_click=eliminar_lambda_ui),
                    ft.ElevatedButton("Convertir AFND→AFD", on_click=convertir_ui),
                    ft.ElevatedButton("Minimizar AFD", on_click=minimizar_ui),
                    ft.ElevatedButton("Pruebas múltiples", on_click=pruebas_multiples_ui),
                    ft.ElevatedButton("Exportar TXT", on_click=exportar_actual_txt),
                    ft.ElevatedButton("Exportar JSON", on_click=exportar_actual_json),
                ], spacing=10, run_spacing=10),
                ft.Divider(),
                ft.Text("Resultado", weight=ft.FontWeight.BOLD),
                resultado,
                ft.Text("Detalles / paso a paso", weight=ft.FontWeight.BOLD),
                ft.Container(detalles, border=ft.border.all(1, ft.Colors.OUTLINE), padding=10, border_radius=8),
                ft.Text("Salida adicional", weight=ft.FontWeight.BOLD),
                salida,
                ft.Divider(),
                ft.Text("Extras", weight=ft.FontWeight.BOLD),
                ft.Wrap([
                    ft.ElevatedButton("Subcadenas", on_click=ver_sub),
                    ft.ElevatedButton("Prefijos", on_click=ver_pref),
                    ft.ElevatedButton("Sufijos", on_click=ver_suf),
                    ft.ElevatedButton("Kleene", on_click=ver_kleene),
                ], spacing=10),
            ],
            spacing=12,
        )
    )


ft.app(target=main)
