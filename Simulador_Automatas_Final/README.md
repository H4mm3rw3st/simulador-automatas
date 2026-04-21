# Simulador de Autómatas

Aplicación desarrollada en **Python + Flet** para trabajar con:

- AFD
- AFND
- AFND con transiciones lambda (AFND-λ)
- Conversión AFND → AFD por subconjuntos
- Eliminación de transiciones lambda
- Minimización de AFD
- Importación de archivos `.jff`
- Exportación a `.txt` y `.json`
- Validación de múltiples cadenas desde archivo

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

Si Flet no abre automáticamente, prueba:

```bash
flet run main.py
```

## Formato de captura manual

### Estados

```text
q0,q1,q2
```

### Alfabeto

```text
0,1
```

Para AFND-λ puedes incluir `λ`.

### Estado inicial

```text
q0
```

### Estados finales

```text
q2
```

### Transiciones

```text
q0,0->q0;q0,1->q1;q1,0->q2;q1,1->q1
```

En AFND y AFND-λ puedes poner múltiples destinos:

```text
q0,0->q0,q1
```

## Importación `.jff`

Escribe la ruta del archivo `.jff` en el campo correspondiente y pulsa **Cargar JFF**.

## Pruebas múltiples

Carga un archivo `.txt` con una cadena por línea y pulsa **Pruebas múltiples**. Se generará un reporte en la carpeta `salidas/`.

## Archivos generados

La aplicación crea archivos dentro de:

```text
salidas/
```

Ejemplos:

- `automata_exportado.txt`
- `automata_exportado.json`
- `afnd_sin_lambda.txt`
- `afd_convertido.txt`
- `afd_minimo.txt`
- `reporte_cadenas.txt`

## Estructura

```text
Simulador_Automatas/
├── automatas/
├── extras/
├── ui/
├── utils/
├── main.py
├── requirements.txt
└── README.md
```

## Observaciones

- La minimización se aplica solo a AFD.
- La λ-clausura se aplica solo a AFND-λ.
- Para convertir AFND-λ a AFD, primero elimina λ y luego usa la conversión por subconjuntos.
