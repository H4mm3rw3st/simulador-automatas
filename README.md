Simulador de Autómatas
Este programa permite la simulación y análisis de autómatas finitos, facilitando el estudio práctico de los modelos vistos en clase. La aplicación cuenta con herramientas para trabajar con Autómatas Finitos Deterministas (AFD), Autómatas Finitos No Deterministas (AFND) y Autómatas Finitos No Deterministas con transiciones lambda (AFN-λ), además de funciones de conversión y minimización.

Funcionalidades
Simulación de AFD.
Simulación de AFND.
Simulación de AFN-λ.
Validación de cadenas de entrada.
Conversión de AFND a AFD mediante algoritmo de subconjuntos.
Eliminación de transiciones lambda.
Minimización de AFD.
Importación de archivos .jff.
Exportación de resultados.
Requisitos
Python 3.10 o superior.
pip instalado en el sistema.
Instalación

Ejecutar el siguiente comando para instalar las dependencias necesarias:

pip install -r requirements.txt
Ejecución

Para iniciar el programa ejecutar:

python main.py

Si existe algún problema con la interfaz gráfica, ejecutar:

flet run main.py

Estructura del Proyecto
main.py : archivo principal del programa.

Autores:
Hernandez Rios Cristian Sebastian
López Toledo Kevin Antonio
automatas/ : contiene la lógica de los autómatas y algoritmos principales.
utils/ : utilerías auxiliares.
requirements.txt : dependencias necesarias.
