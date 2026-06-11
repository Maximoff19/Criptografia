# ============================================================  # Título visual para separar las dependencias de la interfaz.
# SECCIÓN 1: IMPORTACIONES DE PYTHON  # Esta parte carga módulos para contraseña oculta, colores, terminal, rutas y tipos.
# ============================================================  # Cierre visual de la sección de importaciones estándar.
from __future__ import annotations  # Activamos anotaciones modernas para mantener el código claro.

import getpass  # Importamos getpass para pedir contraseñas sin mostrarlas en pantalla.
import json  # Importamos JSON para guardar el mensaje cifrado en un archivo .txt compatible con bloc de notas.
import os  # Importamos os para leer variables de entorno como NO_COLOR o FORCE_COLOR.
import shutil  # Importamos shutil para detectar el ancho real de la terminal.
import sys  # Importamos sys para saber si la salida actual realmente es una terminal interactiva.
import textwrap  # Importamos textwrap para partir textos largos sin romper la lectura.
from pathlib import Path  # Importamos Path para manejar archivos de llaves y mensajes cifrados.
from typing import Any  # Importamos Any porque los JSON mezclan números, textos y listas.

# ============================================================  # Título visual para separar la conexión con el backend RSA.
# SECCIÓN 2: IMPORTACIONES DEL BACKEND  # Esta parte trae funciones y modelos que hacen la matemática RSA real.
# ============================================================  # Cierre visual de la sección de imports propios.
from rsa_backend import (  # Importamos la lógica RSA separada de la interfaz de terminal.
    DetalleGeneracionRSA,  # Importamos el detalle completo del proceso RSA paso a paso.
    LlavePrivada,  # Importamos la estructura de la llave privada del empleado.
    LlavePublica,  # Importamos la estructura de la llave pública que recibe el jefe.
    cifrar_dos_datos,  # Importamos la función que cifra dos credenciales.
    cifrar_texto,  # Importamos la función que cifra texto libre bloque por bloque.
    descifrar_dos_datos,  # Importamos la función que descifra dos credenciales.
    descifrar_texto,  # Importamos la función que descifra texto libre desde bloques numéricos.
    generar_llaves,  # Importamos la función que crea p, q, n, phi, d y e.
    generar_llaves_desde_primos,  # Importamos la generación de llaves desde p, q y d ingresados por el usuario.
    guardar_json,  # Importamos la función para guardar archivos JSON.
    leer_json,  # Importamos la función para leer archivos JSON.
    llave_privada_desde_diccionario,  # Importamos la conversión de JSON a llave privada.
    llave_publica_a_diccionario,  # Importamos la conversión de llave pública a JSON.
    llave_publica_desde_diccionario,  # Importamos la conversión de JSON a llave pública.
    obtener_posibles_d,  # Importamos el cálculo de candidatos d para mostrarlos en el proceso.
    obtener_posibles_e,  # Importamos el cálculo de candidatos e para mostrarlos en el proceso.
    par_de_llaves_a_diccionario,  # Importamos la conversión del par completo a JSON.
    validar_primos_una_o_dos_cifras,  # Importamos la validación estricta de p y q manuales.
    verificar_par_de_llaves,  # Importamos la prueba rápida de consistencia de llaves.
)  # Cerramos la lista de importaciones desde el backend.


# ============================================================  # Título visual para ubicar constantes de archivos, tamaños y colores.
# SECCIÓN 3: CONFIGURACIÓN DE LA APLICACIÓN  # Esta parte define rutas, ancho de terminal, colores y logo ASCII.
# ============================================================  # Cierre visual de la sección de configuración.
BASE_DIR = Path(__file__).resolve().parent  # Guardamos la carpeta del proyecto para que los archivos se creen siempre acá.
ARCHIVO_PUBLICO = BASE_DIR / "llave_publica.json"  # Definimos el archivo que el empleado sí puede compartir con su jefe.
ARCHIVO_PRIVADO = BASE_DIR / "llave_privada_empleado.json"  # Definimos el archivo privado que solo conserva el empleado.
ARCHIVO_CIFRADO = BASE_DIR / "credenciales_encriptadas.json"  # Definimos el archivo que contiene las credenciales cifradas por el jefe.
ARCHIVO_MENSAJE_TXT = BASE_DIR / "mensaje_encriptado.txt"  # Definimos el archivo de texto para compartir el cifrado.
ANCHO_MINIMO = 64  # Definimos un ancho mínimo para que la interfaz no quede aplastada.
ANCHO_MAXIMO = 92  # Definimos un ancho máximo para evitar líneas demasiado largas.
BITS_DEMO = 16  # Definimos el tamaño por defecto de los primos para una demo rápida.
COLOR_RESET = "\033[0m"  # Definimos el código ANSI que vuelve el texto al color normal.
COLORES = {  # Definimos una paleta pequeña y consistente para no convertir la terminal en un carnaval.
    "primario": "\033[96m",  # Usamos cian brillante para títulos y acciones principales.
    "secundario": "\033[94m",  # Usamos azul para bordes y bloques informativos.
    "exito": "\033[92m",  # Usamos verde para estados correctos o finalizados.
    "advertencia": "\033[91m",  # Usamos rojo para advertencias importantes.
    "error": "\033[91m",  # Usamos rojo para errores que requieren corrección.
    "muted": "\033[90m",  # Usamos gris para texto secundario o separadores suaves.
    "negrita": "\033[1m",  # Usamos negrita para reforzar títulos sin depender solo del color.
}  # Cerramos la paleta ANSI.
ASCII_LOGO = [  # Definimos un encabezado ASCII liviano para darle identidad visual a la app.
    " ____   ____      _     ",  # Primera línea del logo RSA.
    "|  _ \\ / ___|    / \\    ",  # Segunda línea del logo RSA.
    "| |_) |\\___ \\   / _ \\   ",  # Tercera línea del logo RSA.
    "|  _ <  ___) | / ___ \\  ",  # Cuarta línea del logo RSA.
    "|_| \\_\\|____/ /_/   \\_\\ ",  # Quinta línea del logo RSA.
]  # Cerramos el bloque ASCII del logo.


# ============================================================  # Título visual para agrupar utilidades de presentación en terminal.
# SECCIÓN 4: UTILIDADES VISUALES DE TERMINAL  # Esta parte controla ancho, limpieza, colores, líneas, bloques y mensajes de estado.
# ============================================================  # Cierre visual de la sección de utilidades visuales.
def obtener_ancho_terminal() -> int:  # Calculamos un ancho cómodo según la terminal del usuario.
    columnas = shutil.get_terminal_size(fallback=(80, 24)).columns  # Leemos el ancho actual y usamos 80 si no se puede detectar.
    return max(ANCHO_MINIMO, min(columnas, ANCHO_MAXIMO))  # Limitamos el ancho para mantener una lectura estable.


def terminal_admite_colores() -> bool:  # Detectamos si conviene imprimir códigos ANSI de color.
    if "NO_COLOR" in os.environ:  # Respetamos el estándar NO_COLOR para desactivar colores manualmente.
        return False  # Devolvemos falso porque el usuario pidió salida sin color.
    if "FORCE_COLOR" in os.environ:  # Permitimos forzar colores aunque la salida no parezca interactiva.
        return True  # Devolvemos verdadero para pruebas o terminales especiales.
    return sys.stdout.isatty()  # Usamos colores solo cuando la salida estándar es una terminal real.


def limpiar_pantalla() -> None:  # Limpiamos la consola entre pantallas para que el flujo no se apile visualmente.
    if "RSA_NO_CLEAR" in os.environ:  # Permitimos desactivar la limpieza cuando se quiera guardar una transcripción completa.
        return  # Salimos sin limpiar porque el usuario lo pidió por variable de entorno.
    if not sys.stdout.isatty():  # Evitamos imprimir códigos de control cuando la salida no es una terminal interactiva.
        return  # Salimos para que pruebas, pipes y redirecciones conserven texto plano.
    if os.environ.get("TERM", "").lower() == "dumb":  # Detectamos terminales mínimas que no manejan bien secuencias ANSI.
        return  # Salimos sin limpiar para no ensuciar la salida con caracteres raros.
    print("\033[2J\033[H", end="")  # Borramos la pantalla y movemos el cursor al inicio usando ANSI estándar.


def colorear(texto: str, color: str) -> str:  # Aplicamos un color ANSI sin hacer que la app dependa de ese color.
    if not terminal_admite_colores():  # Si la terminal no soporta color o el usuario lo desactivó, no alteramos el texto.
        return texto  # Devolvemos texto plano para accesibilidad y compatibilidad.
    codigo = COLORES.get(color, "")  # Buscamos el código ANSI solicitado en la paleta definida.
    if codigo == "":  # Verificamos si el color no existe en la paleta.
        return texto  # Devolvemos texto plano para no imprimir códigos raros.
    return f"{codigo}{texto}{COLOR_RESET}"  # Envolvemos el texto con color y luego reseteamos el estilo.


def imprimir_linea(caracter: str = "-", color: str = "muted") -> None:  # Imprimimos una línea divisoria consistente.
    print(colorear(caracter * obtener_ancho_terminal(), color))  # Repetimos el carácter elegido y aplicamos color si corresponde.


def imprimir_texto(texto: str, prefijo: str = "") -> None:  # Imprimimos texto largo adaptado al ancho de la terminal.
    ancho = obtener_ancho_terminal() - len(prefijo)  # Restamos el prefijo para que el texto no se pase del borde.
    for linea in textwrap.wrap(texto, width=max(20, ancho)):  # Partimos el texto en líneas legibles y seguras.
        print(f"{prefijo}{linea}")  # Imprimimos cada línea con el prefijo indicado.


def imprimir_bloque(titulo: str, lineas: list[str], caracter: str = "-", color: str = "secundario") -> None:  # Mostramos un bloque visual con título y contenido.
    imprimir_linea(caracter, color)  # Abrimos el bloque con una línea visual.
    print(colorear(titulo.upper(), "negrita"))  # Mostramos el título en mayúsculas y negrita para jerarquía visual.
    imprimir_linea(caracter, color)  # Separamos el título del contenido.
    for linea in lineas:  # Recorremos cada línea textual del bloque.
        imprimir_texto(linea)  # Imprimimos cada línea ajustada al ancho disponible.
    imprimir_linea(caracter, color)  # Cerramos el bloque con una línea visual.


def imprimir_recuadro_advertencia(mensaje: str) -> None:  # Mostramos advertencias en rojo, con símbolo y recuadro ASCII.
    ancho = min(obtener_ancho_terminal(), 86)  # Calculamos un ancho controlado para que el recuadro no se desborde.
    contenido = textwrap.wrap(mensaje, width=ancho - 6)  # Partimos el mensaje dejando espacio para bordes y padding.
    titulo = "[!] ADVERTENCIA"  # Definimos un título con símbolo ASCII para no depender solo del color.
    borde = "+" + "-" * (ancho - 2) + "+"  # Construimos el borde superior e inferior del recuadro.
    print(colorear(borde, "error"))  # Imprimimos el borde superior en rojo.
    print(colorear(f"| {titulo:<{ancho - 4}} |", "error"))  # Imprimimos el título alineado dentro del recuadro.
    print(colorear(borde, "error"))  # Imprimimos un separador rojo debajo del título.
    for linea in contenido:  # Recorremos cada línea del mensaje ya envuelta.
        print(colorear(f"| {linea:<{ancho - 4}} |", "error"))  # Imprimimos cada línea dentro del recuadro rojo.
    print(colorear(borde, "error"))  # Imprimimos el borde inferior del recuadro.


def imprimir_estado(mensaje: str, tipo: str = "INFO") -> None:  # Mostramos mensajes de estado sin depender de colores.
    if tipo.upper() == "ADVERTENCIA":  # Detectamos advertencias para tratarlas como un caso visual especial.
        imprimir_recuadro_advertencia(mensaje)  # Mostramos la advertencia en recuadro rojo con símbolo.
        return  # Salimos para no imprimir también la línea simple.
    colores_por_tipo = {"INFO": "primario", "ERROR": "error", "ADVERTENCIA": "advertencia", "OK": "exito", "EXITO": "exito"}  # Asociamos etiquetas con colores semánticos.
    color = colores_por_tipo.get(tipo.upper(), "muted")  # Elegimos el color según el tipo de estado.
    etiqueta = colorear(f"[{tipo}]", color)  # Coloreamos solo la etiqueta para conservar lectura clara.
    print(f"{etiqueta} {mensaje}")  # Imprimimos una etiqueta textual clara para accesibilidad.


# ============================================================  # Título visual para separar helpers de archivos y estado del flujo.
# SECCIÓN 5: ARCHIVOS Y RUTAS  # Esta parte da formato a rutas y verifica existencia de archivos cuando una acción lo necesita.
# ============================================================  # Cierre visual de la sección de archivos y rutas.
def formatear_ruta(ruta: Path) -> str:  # Convertimos una ruta a texto amigable para la terminal.
    return ruta.name  # Mostramos solo el nombre para no llenar la pantalla con rutas largas.


def existe_archivo(ruta: Path) -> bool:  # Verificamos si un archivo esperado ya existe.
    return ruta.exists() and ruta.is_file()  # Confirmamos existencia y que sea archivo, no carpeta.


def mostrar_logo_ascii() -> None:  # Mostramos el logo ASCII centrado y coloreado.
    for linea in ASCII_LOGO:  # Recorremos cada línea del dibujo ASCII.
        print(colorear(linea.center(obtener_ancho_terminal()), "primario"))  # Centramos y coloreamos la línea sin depender solo del color.


def mostrar_titulo() -> None:  # Mostramos el encabezado principal de la interfaz.
    print()  # Dejamos una línea inicial para separar la app del comando anterior.
    imprimir_linea("=", "primario")  # Imprimimos una línea fuerte para abrir la pantalla.
    mostrar_logo_ascii()  # Mostramos una identidad visual ASCII sin cargar dependencias externas.
    print(colorear("CRIPTOGRAFÍA RSA".center(obtener_ancho_terminal()), "negrita"))  # Centramos y reforzamos el nombre de la app.
    print(colorear("Flujo empleado/jefe y texto RSA paso a paso".center(obtener_ancho_terminal()), "secundario"))  # Centramos el propósito con color secundario.
    imprimir_linea("=", "primario")  # Cerramos el encabezado con otra línea fuerte.
    imprimir_linea("-", "muted")  # Separamos el encabezado del estado operativo.


# ============================================================  # Título visual para agrupar lectura de datos del usuario.
# SECCIÓN 6: ENTRADAS Y CONFIRMACIONES  # Esta parte pide números, confirmaciones y pausas de forma clara y validada.
# ============================================================  # Cierre visual de la sección de entradas.
def pausar() -> None:  # Detenemos la pantalla para que el usuario pueda leer.
    input(colorear("\nPresioná ENTER para volver al menú...", "muted"))  # Esperamos una confirmación sencilla con estilo secundario.


def pedir_entero(mensaje: str, valor_por_defecto: int | None = None, minimo: int | None = None) -> int:  # Pedimos un número entero desde la terminal.
    while True:  # Repetimos hasta recibir un entero válido.
        sufijo = f" [{valor_por_defecto}]" if valor_por_defecto is not None else ""  # Mostramos el valor por defecto si existe.
        texto = input(colorear(f"{mensaje}{sufijo}: ", "primario")).strip()  # Leemos la respuesta del usuario sin espacios laterales.
        if texto == "" and valor_por_defecto is not None:  # Aceptamos ENTER como valor por defecto.
            valor = valor_por_defecto  # Guardamos el valor por defecto como respuesta.
        else:  # Procesamos el texto escrito cuando no se usó el valor por defecto.
            try:  # Intentamos convertir el texto a entero.
                valor = int(texto)  # Guardamos el entero convertido.
            except ValueError:  # Capturamos entradas que no son números enteros.
                imprimir_estado("Tenés que escribir un número entero.", "ERROR")  # Explicamos el error sin romper el programa.
                continue  # Volvemos a pedir el dato.
        if minimo is not None and valor < minimo:  # Validamos el mínimo si fue configurado.
            imprimir_estado(f"El valor mínimo permitido es {minimo}.", "ERROR")  # Informamos cómo corregir el dato.
            continue  # Volvemos a pedir el dato.
        return valor  # Devolvemos el entero validado.


def confirmar(mensaje: str, por_defecto: bool = False) -> bool:  # Pedimos una respuesta sí/no con valor por defecto.
    etiqueta = "S/n" if por_defecto else "s/N"  # Mostramos visualmente cuál opción es la predeterminada.
    respuesta = input(colorear(f"{mensaje} [{etiqueta}]: ", "primario")).strip().lower()  # Leemos y normalizamos la respuesta.
    if respuesta == "":  # Detectamos ENTER sin texto.
        return por_defecto  # Devolvemos el valor por defecto elegido por la función llamadora.
    return respuesta in {"s", "si", "sí", "y", "yes"}  # Aceptamos variantes comunes de confirmación.


# ============================================================  # Título visual para separar carga y escritura manual de llaves.
# SECCIÓN 7: CARGA DE LLAVES RSA  # Esta parte obtiene llaves desde archivos JSON o desde datos escritos manualmente.
# ============================================================  # Cierre visual de la sección de carga de llaves.
def cargar_llave_publica_guardada() -> LlavePublica | None:  # Intentamos cargar la llave pública del archivo compartible.
    if not existe_archivo(ARCHIVO_PUBLICO):  # Verificamos si el archivo todavía no existe.
        return None  # Devolvemos None para indicar que no hay llave pública guardada.
    datos = leer_json(ARCHIVO_PUBLICO)  # Leemos el JSON de la llave pública.
    return llave_publica_desde_diccionario(datos)  # Convertimos el JSON a una llave pública real.


def cargar_llave_privada_guardada() -> LlavePrivada | None:  # Intentamos cargar la llave privada local del empleado.
    if not existe_archivo(ARCHIVO_PRIVADO):  # Verificamos si el archivo privado todavía no existe.
        return None  # Devolvemos None para indicar que no hay llave privada guardada.
    datos = leer_json(ARCHIVO_PRIVADO)  # Leemos el JSON privado completo.
    return llave_privada_desde_diccionario(datos["privada"])  # Extraemos y convertimos la sección privada.


def pedir_llave_publica_manual() -> LlavePublica:  # Permitimos escribir una llave pública recibida manualmente.
    imprimir_bloque("Carga manual de llave pública", ["Usá esta opción cuando el jefe recibió n y e por otro medio."], ".", "secundario")  # Damos contexto antes de pedir números.
    n = pedir_entero("Valor n de la llave pública", minimo=1)  # Pedimos el módulo n.
    e = pedir_entero("Valor e de la llave pública", minimo=1)  # Pedimos el exponente público e.
    return LlavePublica(n=n, e=e)  # Construimos la llave pública con esos valores.


def pedir_llave_privada_manual() -> LlavePrivada:  # Permitimos escribir una llave privada manualmente si no hay archivo.
    imprimir_bloque("Carga manual de llave privada", ["Solo el empleado debe conocer esta llave. Si la compartís, rompés el objetivo de seguridad."], ".", "advertencia")  # Advertimos antes de pedir datos privados.
    n = pedir_entero("Valor n de la llave privada", minimo=1)  # Pedimos el módulo n.
    d = pedir_entero("Valor d de la llave privada", minimo=1)  # Pedimos el exponente privado d.
    return LlavePrivada(n=n, d=d)  # Construimos la llave privada con esos valores.


def obtener_llave_publica_para_cifrar() -> LlavePublica:  # Obtenemos la llave pública que usará el jefe para cifrar.
    llave_guardada = cargar_llave_publica_guardada()  # Intentamos cargar una llave pública existente.
    if llave_guardada is not None:  # Revisamos si existe una llave pública lista.
        imprimir_estado(f"Encontré {formatear_ruta(ARCHIVO_PUBLICO)}.", "INFO")  # Informamos que hay archivo disponible.
        if confirmar("¿Querés usar esa llave pública?", True):  # Consultamos si usar la guardada con sí por defecto.
            return llave_guardada  # Devolvemos la llave pública guardada.
    return pedir_llave_publica_manual()  # Pedimos la llave pública manualmente si no se usa archivo.


def obtener_llave_privada_para_descifrar() -> LlavePrivada:  # Obtenemos la llave privada que usará el empleado para descifrar.
    llave_guardada = cargar_llave_privada_guardada()  # Intentamos cargar la llave privada local.
    if llave_guardada is not None:  # Revisamos si existe una llave privada lista.
        imprimir_estado(f"Encontré {formatear_ruta(ARCHIVO_PRIVADO)}.", "INFO")  # Informamos que hay archivo disponible.
        if confirmar("¿Querés usar esa llave privada?", True):  # Consultamos si usar la guardada con sí por defecto.
            return llave_guardada  # Devolvemos la llave privada guardada.
    return pedir_llave_privada_manual()  # Pedimos la llave privada manualmente si no se usa archivo.


# ============================================================  # Título visual para ubicar el flujo de generación de llaves.
# SECCIÓN 8: ACCIÓN 1 - GENERAR LLAVES  # Esta parte permite al empleado crear y guardar la llave pública y privada.
# ============================================================  # Cierre visual de la sección de generación.
def confirmar_reemplazo_de_llaves() -> bool:  # Confirmamos antes de sobrescribir llaves existentes.
    hay_llaves = existe_archivo(ARCHIVO_PUBLICO) or existe_archivo(ARCHIVO_PRIVADO)  # Detectamos si ya hay llaves guardadas.
    if not hay_llaves:  # Si no hay llaves existentes, no hay riesgo de sobrescritura.
        return True  # Permitimos continuar sin preguntar.
    imprimir_bloque(  # Mostramos una advertencia estructurada antes de una acción riesgosa.
        "Atención antes de reemplazar llaves",  # Definimos el título del bloque.
        [  # Abrimos la lista de mensajes del bloque.
            "Ya existen llaves guardadas en esta carpeta.",  # Explicamos el estado actual.
            "Si generás llaves nuevas, los mensajes cifrados con las llaves viejas podrían dejar de descifrarse.",  # Explicamos la consecuencia real.
            "Esto no es un detalle decorativo: es el contrato matemático de RSA.",  # Reforzamos el concepto para aprendizaje.
        ],  # Cerramos la lista de mensajes.
        "!",  # Usamos un separador visual distinto para advertencia.
        "advertencia",  # Usamos amarillo semántico para reforzar el riesgo sin depender solo del color.
    )  # Cerramos la llamada al bloque.
    return confirmar("¿Seguro que querés reemplazar las llaves?", False)  # Pedimos confirmación explícita con no por defecto.


def generar_y_guardar_llaves() -> None:  # Ejecutamos el flujo del empleado que crea sus llaves.
    imprimir_bloque(  # Mostramos contexto antes de pedir datos.
        "Paso 1 - Empleado genera llaves",  # Definimos el título del paso.
        [  # Abrimos la lista de mensajes.
            "La llave pública se comparte con el jefe para cifrar credenciales.",  # Explicamos el uso de la pública.
            "La llave privada se queda con el empleado para descifrar lo recibido.",  # Explicamos el uso de la privada.
        ],  # Cerramos la lista de mensajes.
        "-",  # Usamos una línea normal para separar el contenido del paso.
        "primario",  # Usamos el color principal para este paso del flujo.
    )  # Cerramos la llamada al bloque.
    if not confirmar_reemplazo_de_llaves():  # Consultamos si se permite sobrescribir llaves existentes.
        imprimir_estado("Operación cancelada. No se modificaron las llaves.", "INFO")  # Informamos cancelación segura.
        return  # Salimos sin tocar archivos.
    bits = pedir_entero("Bits de cada primo p y q para la demo", BITS_DEMO, minimo=8)  # Pedimos tamaño de primos con validación.
    imprimir_estado("Generando primos p y q; esperá unos segundos.", "INFO")  # Mostramos estado de carga.
    par = generar_llaves(bits)  # Generamos p, q, n, phi, d y e según el PDF.
    if not verificar_par_de_llaves(par):  # Validamos que el par de llaves cifre y descifre correctamente.
        raise RuntimeError("El par de llaves generado no pasó la verificación interna.")  # Cortamos si algo grave falló.
    guardar_json(ARCHIVO_PRIVADO, par_de_llaves_a_diccionario(par))  # Guardamos el archivo privado completo para el empleado.
    guardar_json(ARCHIVO_PUBLICO, llave_publica_a_diccionario(par.publica))  # Guardamos solo n y e para compartir con el jefe.
    imprimir_bloque(  # Mostramos resultado con jerarquía visual.
        "Llaves generadas correctamente",  # Definimos el título de éxito.
        [  # Abrimos la lista de datos importantes.
            f"Compartir con el jefe: {formatear_ruta(ARCHIVO_PUBLICO)}",  # Indicamos el archivo público.
            f"Guardar sin compartir: {formatear_ruta(ARCHIVO_PRIVADO)}",  # Indicamos el archivo privado.
            f"Llave pública (n, e): ({par.publica.n}, {par.publica.e})",  # Mostramos la llave pública por si se quiere copiar.
            f"Llave privada (n, d): ({par.privada.n}, {par.privada.d})",  # Mostramos la privada solo para aprendizaje local.
            f"Detalle matemático: p={par.p}, q={par.q}, phi(n)={par.phi}",  # Mostramos el cálculo base del PDF.
        ],  # Cerramos la lista de datos importantes.
        "=",  # Usamos separador fuerte para éxito.
        "exito",  # Usamos verde semántico para indicar que la operación terminó bien.
    )  # Cerramos el bloque de resultado.


# ============================================================  # Título visual para ubicar el flujo de compartir llave pública.
# SECCIÓN 9: ACCIÓN 2 - MOSTRAR LLAVE PÚBLICA  # Esta parte muestra solo la llave pública que el jefe puede usar.
# ============================================================  # Cierre visual de la sección de llave pública.
def mostrar_llave_publica() -> None:  # Mostramos la llave pública disponible.
    imprimir_bloque("Paso 2 - Compartir llave pública", ["Este es el único material que debería recibir el jefe."], "-", "primario")  # Presentamos el paso.
    llave = cargar_llave_publica_guardada()  # Cargamos la llave pública desde archivo.
    if llave is None:  # Verificamos si todavía no existe.
        imprimir_estado("No existe llave_publica.json; primero generá las llaves con la opción 1.", "ERROR")  # Indicamos el paso faltante.
        return  # Salimos de la función.
    print(colorear("Datos para compartir:", "negrita"))  # Indicamos que empieza la información copiable.
    print(f"  n = {llave.n}")  # Mostramos el módulo n.
    print(f"  e = {llave.e}")  # Mostramos el exponente público e.
    print(f"  archivo = {formatear_ruta(ARCHIVO_PUBLICO)}")  # Mostramos el archivo compartible.
    imprimir_estado("No compartas llave_privada_empleado.json. Si lo hacés, la seguridad se cae.", "ADVERTENCIA")  # Reforzamos la regla central.


# ============================================================  # Título visual para separar el formulario de datos sensibles.
# SECCIÓN 10: FORMULARIO DE CREDENCIALES  # Esta parte pide usuario y contraseña, evitando mostrar la contraseña en pantalla.
# ============================================================  # Cierre visual de la sección de formulario.
def pedir_credencial_visible() -> str:  # Pedimos el primer dato sensible de forma visible.
    while True:  # Repetimos hasta que el usuario escriba algo.
        valor = input(colorear("Usuario o identificador a cifrar: ", "primario")).strip()  # Pedimos un usuario, correo o identificador.
        if valor != "":  # Validamos que no esté vacío.
            return valor  # Devolvemos el dato capturado.
        imprimir_estado("El primer dato no puede estar vacío.", "ERROR")  # Indicamos cómo corregir el formulario.


def pedir_credencial_oculta() -> str:  # Pedimos el segundo dato sensible ocultando lo escrito.
    while True:  # Repetimos hasta que el usuario escriba algo.
        valor = getpass.getpass(colorear("Contraseña o segundo dato sensible a cifrar: ", "primario")).strip()  # Pedimos una contraseña sin eco visual.
        if valor != "":  # Validamos que no esté vacío.
            return valor  # Devolvemos el dato capturado.
        imprimir_estado("El segundo dato no puede estar vacío.", "ERROR")  # Indicamos cómo corregir el formulario.


def resumir_bloques(bloques: list[int], limite: int = 8) -> str:  # Resumimos listas largas de bloques cifrados para mejorar lectura.
    if len(bloques) <= limite:  # Si la lista es corta, se puede mostrar completa.
        return str(bloques)  # Devolvemos la representación completa.
    visibles = ", ".join(str(numero) for numero in bloques[:limite])  # Convertimos los primeros bloques a texto.
    return f"[{visibles}, ...] total={len(bloques)} bloques"  # Devolvemos una vista compacta con el total.


def formatear_lista_enteros(valores: list[int], por_linea: int = 12, limite: int = 120) -> str:  # Formateamos listas de candidatos d o e para que sean legibles.
    visibles = valores[:limite]  # Tomamos una cantidad razonable para no saturar la terminal si la lista es enorme.
    lineas: list[str] = []  # Creamos una lista de líneas de texto formateadas.
    for indice in range(0, len(visibles), por_linea):  # Recorremos la lista por grupos de tamaño fijo.
        grupo = visibles[indice : indice + por_linea]  # Extraemos el grupo actual de enteros.
        lineas.append(", ".join(str(valor) for valor in grupo))  # Convertimos el grupo a una línea separada por comas.
    if len(valores) > limite:  # Verificamos si quedaron valores sin mostrar por límite de legibilidad.
        lineas.append(f"... se calcularon {len(valores)} valores en total")  # Avisamos que la lista completa existe pero fue resumida.
    return "\n".join(lineas)  # Devolvemos todas las líneas unidas para imprimirlas.


def pedir_texto_a_encriptar() -> str:  # Pedimos el texto libre que se quiere encriptar.
    while True:  # Repetimos hasta recibir un texto no vacío.
        texto = input(colorear("Texto o cadena a encriptar: ", "primario"))  # Pedimos el texto a cifrar.
        if texto != "":  # Validamos que el usuario no haya dejado vacío el campo.
            return texto  # Devolvemos el texto válido.
        imprimir_estado("El texto a encriptar no puede estar vacío.", "ERROR")  # Mostramos el error de formulario.


def pedir_primo(nombre: str) -> int:  # Pedimos un número primo manual de una o dos cifras.
    return pedir_entero(f"Ingresá {nombre}, primo de una o dos cifras", minimo=2)  # Reutilizamos la entrada entera validada por mínimo.


def texto_cabe_en_modulo(texto: str, n: int) -> bool:  # Revisamos la restricción RSA M < n para cada byte del texto.
    bytes_texto = texto.encode("utf-8")  # Convertimos el texto a bytes UTF-8 para usar la misma lógica del backend.
    if not bytes_texto:  # Revisamos el caso extremo de texto vacío aunque normalmente ya se validó antes.
        return True  # Un texto vacío no rompe la restricción matemática.
    return max(bytes_texto) < n  # Devolvemos verdadero solo si el mayor byte es menor que n.


def explicar_error_modulo(texto: str, n: int) -> str:  # Construimos un mensaje claro cuando n es demasiado pequeño.
    maximo = max(texto.encode("utf-8"))  # Calculamos el byte más grande del texto ingresado.
    return f"Con esos primos n={n}, pero el texto contiene un bloque M={maximo}. En RSA debe cumplirse M < n; elegí primos más grandes."  # Devolvemos explicación matemática accionable.


def pedir_p_q_validos_para_texto(texto: str) -> tuple[int, int]:  # Pedimos p y q hasta que sean primos válidos y permitan cifrar el texto.
    while True:  # Repetimos hasta obtener primos correctos.
        p = pedir_primo("p")  # Pedimos el primo p.
        q = pedir_primo("q")  # Pedimos el primo q.
        try:  # Intentamos validar p y q como primos manuales aceptados.
            validar_primos_una_o_dos_cifras(p, q)  # Rechazamos valores que no sean primos, distintos y de una o dos cifras.
        except ValueError as error:  # Capturamos errores de validación.
            imprimir_recuadro_advertencia(str(error))  # Mostramos el rechazo en recuadro rojo.
            continue  # Volvemos a pedir p y q.
        n = p * q  # Calculamos n para verificar que pueda cifrar los bloques del texto.
        if not texto_cabe_en_modulo(texto, n):  # Revisamos si algún bloque del texto no cabe en el módulo.
            imprimir_recuadro_advertencia(explicar_error_modulo(texto, n))  # Explicamos por qué esos primos no sirven.
            continue  # Volvemos a pedir primos más grandes.
        return p, q  # Devolvemos p y q cuando todo cumple.


def seleccionar_d(posibles_d: list[int]) -> int:  # Permitimos seleccionar manualmente un d válido.
    print(colorear("Posibles valores de d:", "negrita"))  # Mostramos el título de los candidatos d.
    print(formatear_lista_enteros(posibles_d))  # Mostramos la lista resumida o completa de candidatos.
    while True:  # Repetimos hasta que el usuario elija un d válido.
        d = pedir_entero("Seleccioná un valor d de la lista", minimo=2)  # Pedimos el d elegido.
        if d in posibles_d:  # Validamos que el d seleccionado esté en los candidatos.
            return d  # Devolvemos el d válido.
        imprimir_recuadro_advertencia("Ese d no está permitido porque no cumple MCD(d, phi(n)) = 1.")  # Explicamos el error matemático.


def seleccionar_e(d: int, phi: int) -> int:  # Permitimos revisar y seleccionar el valor e.
    e_base, posibles_e = obtener_posibles_e(d, phi)  # Calculamos el e base y ejemplos de la solución general.
    print(colorear("Posibles valores de e:", "negrita"))  # Mostramos el título de los candidatos e.
    print(f"Solución general: e = {e_base} + {phi}k, con k entero no negativo")  # Mostramos la fórmula general.
    print(f"Ejemplos: {', '.join(str(valor) for valor in posibles_e)}")  # Mostramos algunos ejemplos concretos.
    if confirmar(f"¿Querés usar e = {e_base}?", True):  # Ofrecemos usar el e base, que es el estándar más simple.
        return e_base  # Devolvemos el e base.
    while True:  # Repetimos hasta que el usuario escriba un e válido.
        e = pedir_entero("Ingresá un e que cumpla e*d ≡ 1 mod phi(n)", minimo=1)  # Pedimos un e manual.
        if (e * d) % phi == 1:  # Verificamos la congruencia exigida por RSA.
            return e  # Devolvemos el e válido.
        imprimir_recuadro_advertencia("Ese e no cumple e*d ≡ 1 mod phi(n). Elegí otro valor.")  # Explicamos el error matemático.


def construir_proceso_detallado(texto: str, detalle: DetalleGeneracionRSA, bloques: list[int]) -> str:  # Construimos el proceso detallado del cifrado RSA.
    lineas = [  # Creamos una lista de líneas para mostrar y guardar el proceso.
        "PROCESO DETALLADO RSA",  # Agregamos título del proceso.
        f"Texto original: {texto}",  # Mostramos el texto ingresado.
        f"p = {detalle.p}",  # Mostramos el primo p.
        f"q = {detalle.q}",  # Mostramos el primo q.
        f"n = p * q = {detalle.p} * {detalle.q} = {detalle.n}",  # Mostramos el cálculo de n.
        f"phi(n) = (p - 1)(q - 1) = ({detalle.p} - 1)({detalle.q} - 1) = {detalle.phi}",  # Mostramos phi.
        "Posibles valores de d con MCD(d, phi(n)) = 1:",  # Presentamos los candidatos d.
        formatear_lista_enteros(detalle.posibles_d),  # Agregamos los candidatos d formateados.
        f"d seleccionado = {detalle.d}",  # Mostramos d elegido.
        f"e debe cumplir e*d ≡ 1 mod phi(n), es decir e*{detalle.d} ≡ 1 mod {detalle.phi}",  # Mostramos la congruencia de e.
        f"e base calculado = {detalle.e_base}",  # Mostramos el inverso modular base.
        f"Posibles ejemplos de e = {', '.join(str(valor) for valor in detalle.posibles_e)}",  # Mostramos ejemplos de e.
        f"e seleccionado = {detalle.e}",  # Mostramos e elegido.
        f"Clave pública = (n, e) = ({detalle.n}, {detalle.e})",  # Mostramos la clave pública.
        f"Clave privada = (n, d) = ({detalle.n}, {detalle.d})",  # Mostramos la clave privada.
        f"Mensaje encriptado en bloques = {bloques}",  # Mostramos el resultado cifrado.
    ]  # Cerramos la lista de líneas.
    return "\n".join(lineas)  # Devolvemos todo el proceso como texto único.


def guardar_mensaje_en_txt(detalle: DetalleGeneracionRSA, bloques: list[int]) -> None:  # Guardamos solo el paquete necesario para descifrar el mensaje.
    paquete = {  # Creamos un objeto JSON legible que se puede abrir con bloc de notas.
        "mensaje_encriptado": bloques,  # Guardamos los bloques cifrados.
        "clave_privada_para_descifrar": {"n": detalle.n, "d": detalle.d},  # Guardamos la clave privada para que el archivo pueda descifrarse después.
    }  # Cerramos el paquete de salida.
    ARCHIVO_MENSAJE_TXT.write_text(json.dumps(paquete, ensure_ascii=False, indent=2), encoding="utf-8")  # Escribimos el archivo .txt en formato JSON legible.


def leer_mensaje_desde_txt(ruta: Path) -> dict[str, Any]:  # Leemos el archivo .txt que contiene el mensaje cifrado.
    texto = ruta.read_text(encoding="utf-8")  # Cargamos el contenido del archivo como texto.
    datos = json.loads(texto)  # Convertimos el JSON de bloc de notas a datos de Python.
    if not isinstance(datos, dict):  # Verificamos que la raíz sea un objeto JSON.
        raise ValueError("El archivo TXT no contiene un paquete RSA válido.")  # Rechazamos formatos inesperados.
    return datos  # Devolvemos el paquete leído.


def encriptar_texto_paso_a_paso() -> None:  # Ejecutamos el flujo completo para encriptar texto con p y q manuales.
    imprimir_bloque("Encriptar texto con RSA", ["Ingresá texto, dos primos p y q, y seleccioná d/e viendo el proceso completo."], "-", "primario")  # Presentamos la acción.
    texto = pedir_texto_a_encriptar()  # Pedimos el texto libre a encriptar.
    p, q = pedir_p_q_validos_para_texto(texto)  # Pedimos primos válidos que permitan cifrar el texto.
    phi = (p - 1) * (q - 1)  # Calculamos phi para obtener los candidatos d.
    posibles_d = obtener_posibles_d(phi)  # Calculamos los posibles d.
    print(f"n = p*q = {p}*{q} = {p * q}")  # Mostramos cálculo de n.
    print(f"phi(n) = (p-1)(q-1) = ({p}-1)({q}-1) = {phi}")  # Mostramos cálculo de phi.
    d = seleccionar_d(posibles_d)  # Pedimos seleccionar un d válido.
    e = seleccionar_e(d, phi)  # Pedimos revisar o seleccionar e.
    detalle = generar_llaves_desde_primos(p, q, d, e)  # Generamos llaves y detalle desde los valores elegidos.
    bloques = cifrar_texto(texto, detalle.publica)  # Encriptamos el texto con la clave pública.
    proceso = construir_proceso_detallado(texto, detalle, bloques)  # Construimos el reporte completo del proceso.
    print()  # Dejamos una línea antes del proceso.
    print(proceso)  # Mostramos el proceso en pantalla.
    imprimir_recuadro_advertencia("El TXT incluye la clave privada para que otro usuario pueda descifrar este ejercicio. En seguridad real, una clave privada no se comparte.")  # Advertimos en rojo dentro de recuadro ASCII.
    guardar_mensaje_en_txt(detalle, bloques)  # Guardamos solo el mensaje cifrado y la clave privada en TXT.
    imprimir_estado(f"Mensaje encriptado guardado en {ARCHIVO_MENSAJE_TXT.name}.", "EXITO")  # Confirmamos el guardado.


def desencriptar_archivo_txt() -> None:  # Ejecutamos el flujo de desencriptación desde archivo TXT.
    imprimir_bloque("Desencriptar archivo TXT", ["El archivo debe contener mensaje_encriptado y clave_privada_para_descifrar."], "-", "primario")  # Presentamos la acción.
    ruta_texto = input(colorear(f"Ruta del TXT [{ARCHIVO_MENSAJE_TXT.name}]: ", "primario")).strip()  # Pedimos ruta o aceptamos la predeterminada.
    ruta = ARCHIVO_MENSAJE_TXT if ruta_texto == "" else Path(ruta_texto)  # Usamos archivo predeterminado si el usuario presiona ENTER.
    datos = leer_mensaje_desde_txt(ruta)  # Leemos el paquete RSA desde el archivo TXT.
    bloques = [int(valor) for valor in datos["mensaje_encriptado"]]  # Convertimos los bloques cifrados a enteros.
    clave = datos["clave_privada_para_descifrar"]  # Extraemos la clave privada guardada para descifrar.
    privada = LlavePrivada(n=int(clave["n"]), d=int(clave["d"]))  # Reconstruimos la clave privada.
    texto = descifrar_texto(bloques, privada)  # Desciframos los bloques para recuperar el texto original.
    imprimir_bloque("Texto desencriptado", [texto], "=", "exito")  # Mostramos el resultado final.


# ============================================================  # Título visual para ubicar el flujo del jefe que cifra datos.
# SECCIÓN 11: ACCIÓN 3 - CIFRAR CREDENCIALES  # Esta parte cifra dos datos con la llave pública y guarda el paquete cifrado.
# ============================================================  # Cierre visual de la sección de cifrado.
def cifrar_credenciales() -> None:  # Ejecutamos el flujo del jefe que cifra dos datos con la llave pública.
    imprimir_bloque(  # Presentamos el paso como una tarea clara.
        "Paso 3 - Jefe cifra credenciales",  # Definimos el título del paso.
        [  # Abrimos la lista de instrucciones.
            "Usá la llave pública del empleado. La contraseña se escribe oculta para evitar exposición visual.",  # Explicamos la mejora de seguridad de UX.
            "El resultado se guarda en credenciales_encriptadas.json para devolverlo al empleado.",  # Explicamos el archivo de salida.
        ],  # Cerramos la lista de instrucciones.
        "-",  # Usamos una línea normal para separar instrucciones.
        "primario",  # Usamos el color principal para este paso del flujo.
    )  # Cerramos la llamada al bloque.
    llave = obtener_llave_publica_para_cifrar()  # Obtenemos la llave pública del empleado.
    dato_uno = pedir_credencial_visible()  # Pedimos el primer dato sensible.
    dato_dos = pedir_credencial_oculta()  # Pedimos el segundo dato sensible sin mostrarlo.
    paquete = cifrar_dos_datos(dato_uno, dato_dos, llave)  # Ciframos ambos datos con RSA.
    guardar_json(ARCHIVO_CIFRADO, paquete)  # Guardamos el paquete cifrado que el jefe devuelve al empleado.
    bloques_uno = list(paquete["dato_uno_cifrado"])  # Extraemos los bloques cifrados del primer dato.
    bloques_dos = list(paquete["dato_dos_cifrado"])  # Extraemos los bloques cifrados del segundo dato.
    imprimir_bloque(  # Mostramos el resultado sin saturar la pantalla.
        "Credenciales cifradas correctamente",  # Definimos el título de éxito.
        [  # Abrimos la lista de resultado.
            f"Archivo para devolver al empleado: {formatear_ruta(ARCHIVO_CIFRADO)}",  # Indicamos qué archivo se devuelve.
            f"Dato 1 cifrado: {resumir_bloques(bloques_uno)}",  # Mostramos resumen del primer cifrado.
            f"Dato 2 cifrado: {resumir_bloques(bloques_dos)}",  # Mostramos resumen del segundo cifrado.
        ],  # Cerramos la lista de resultado.
        "=",  # Usamos separador fuerte para éxito.
        "exito",  # Usamos verde semántico para confirmar el cifrado.
    )  # Cerramos el bloque de resultado.


# ============================================================  # Título visual para ubicar el flujo del empleado que descifra datos.
# SECCIÓN 12: ACCIÓN 4 - DESCIFRAR CREDENCIALES  # Esta parte lee el paquete cifrado y recupera los datos con la llave privada.
# ============================================================  # Cierre visual de la sección de descifrado.
def cargar_paquete_cifrado() -> dict[str, Any] | None:  # Intentamos cargar el archivo con credenciales cifradas.
    if not existe_archivo(ARCHIVO_CIFRADO):  # Revisamos si el archivo todavía no existe.
        return None  # Devolvemos None si no hay paquete para descifrar.
    return leer_json(ARCHIVO_CIFRADO)  # Leemos y devolvemos el paquete cifrado.


def descifrar_credenciales() -> None:  # Ejecutamos el flujo del empleado que descifra los datos recibidos.
    imprimir_bloque(  # Presentamos el paso antes de operar.
        "Paso 4 - Empleado descifra credenciales",  # Definimos el título del paso.
        ["Solo la llave privada del empleado puede recuperar los datos originales."],  # Explicamos el principio de RSA aplicado.
        "-",  # Usamos una línea normal para separar el contenido del paso.
        "primario",  # Usamos el color principal para este paso del flujo.
    )  # Cerramos la llamada al bloque.
    paquete = cargar_paquete_cifrado()  # Cargamos el paquete cifrado desde archivo.
    if paquete is None:  # Verificamos si no hay nada para descifrar.
        imprimir_estado("No existe credenciales_encriptadas.json; primero cifrá dos datos con la opción 3.", "ERROR")  # Indicamos el paso faltante.
        return  # Salimos de la función.
    llave = obtener_llave_privada_para_descifrar()  # Obtenemos la llave privada del empleado.
    dato_uno, dato_dos = descifrar_dos_datos(paquete, llave)  # Desciframos ambos datos.
    imprimir_bloque(  # Mostramos los datos recuperados de forma agrupada.
        "Credenciales descifradas",  # Definimos el título de resultado.
        [  # Abrimos la lista de datos recuperados.
            f"Dato 1 original: {dato_uno}",  # Mostramos el primer dato recuperado.
            f"Dato 2 original: {dato_dos}",  # Mostramos el segundo dato recuperado.
        ],  # Cerramos la lista de datos recuperados.
        "=",  # Usamos separador fuerte para resultado.
        "exito",  # Usamos verde semántico para indicar descifrado correcto.
    )  # Cerramos el bloque de resultado.


# ============================================================  # Título visual para separar funciones de aprendizaje y prueba.
# SECCIÓN 13: DEMO Y AYUDA RSA  # Esta parte muestra una demo automática y explica el algoritmo RSA.
# ============================================================  # Cierre visual de la sección educativa.
def ejecutar_demo_completo() -> None:  # Ejecutamos una demostración automática de todo el flujo.
    imprimir_bloque("Demo automática", ["Esta prueba no modifica tus archivos; ejecuta el flujo completo en memoria."], "-", "secundario")  # Explicamos el alcance de la demo.
    par = generar_llaves(BITS_DEMO)  # Generamos llaves pequeñas para la demo académica.
    dato_uno = "empleado@empresa-x.test"  # Definimos un usuario de ejemplo.
    dato_dos = "Clave-Demo-123"  # Definimos una contraseña de ejemplo.
    paquete = cifrar_dos_datos(dato_uno, dato_dos, par.publica)  # Simulamos al jefe cifrando con la pública.
    recuperado_uno, recuperado_dos = descifrar_dos_datos(paquete, par.privada)  # Simulamos al empleado descifrando con la privada.
    imprimir_bloque(  # Mostramos la demo como una historia de usuario.
        "Resultado de la demo",  # Definimos el título de resultado.
        [  # Abrimos la lista de datos de la demo.
            f"Pública que recibe el jefe: (n={par.publica.n}, e={par.publica.e})",  # Mostramos la llave pública.
            f"Privada que conserva el empleado: (n={par.privada.n}, d={par.privada.d})",  # Mostramos la llave privada para estudio.
            f"Dato 1 cifrado: {resumir_bloques(list(paquete['dato_uno_cifrado']))}",  # Mostramos el primer dato cifrado compacto.
            f"Dato 2 cifrado: {resumir_bloques(list(paquete['dato_dos_cifrado']))}",  # Mostramos el segundo dato cifrado compacto.
            f"Dato 1 descifrado: {recuperado_uno}",  # Mostramos el primer dato recuperado.
            f"Dato 2 descifrado: {recuperado_dos}",  # Mostramos el segundo dato recuperado.
        ],  # Cerramos la lista de datos de la demo.
        "=",  # Usamos separador fuerte para resultado.
        "exito",  # Usamos verde semántico para destacar que la demo cerró el ciclo.
    )  # Cerramos el bloque de resultado.


def mostrar_explicacion_rsa() -> None:  # Mostramos una explicación breve de la lógica matemática.
    imprimir_bloque(  # Agrupamos la explicación como ayuda contextual.
        "Ayuda - RSA paso a paso",  # Definimos el título de ayuda.
        [  # Abrimos las líneas de explicación.
            "1. Se eligen dos primos distintos p y q.",  # Explicamos el primer paso matemático.
            "2. Se calcula n = p * q.",  # Explicamos el módulo RSA.
            "3. Se calcula phi(n) = (p - 1)(q - 1).",  # Explicamos la función de Euler.
            "4. Se elige d menor que phi(n) con MCD(d, phi(n)) = 1.",  # Explicamos el exponente privado.
            "5. Se calcula e para que e*d sea congruente con 1 módulo phi(n).",  # Explicamos el inverso modular.
            "6. El jefe cifra con la pública (n, e): C = M^e mod n.",  # Explicamos el cifrado.
            "7. El empleado descifra con la privada (n, d): M = C^d mod n.",  # Explicamos el descifrado.
        ],  # Cerramos las líneas de explicación.
        "-",  # Usamos una línea normal para separar la ayuda.
        "secundario",  # Usamos azul para diferenciar ayuda de acciones críticas.
    )  # Cerramos el bloque de ayuda.


# ============================================================  # Título visual para agrupar la navegación de la app.
# SECCIÓN 14: MENÚ Y NAVEGACIÓN  # Esta parte muestra opciones, ejecuta la acción elegida y mantiene la app abierta.
# ============================================================  # Cierre visual de la sección de navegación.
def mostrar_menu() -> None:  # Mostramos las opciones disponibles con agrupación por flujo mental.
    print(colorear("Flujo empresa:", "negrita"))  # Agrupamos como principal el flujo empleado/jefe original.
    print(f"  {colorear('1)', 'primario')} Empleado: generar llaves pública y privada")  # Opción para crear llaves del empleado.
    print(f"  {colorear('2)', 'primario')} Empleado: mostrar llave pública para el jefe")  # Opción para compartir la pública.
    print(f"  {colorear('3)', 'primario')} Jefe: cifrar dos credenciales con la llave pública")  # Opción para cifrar credenciales.
    print(f"  {colorear('4)', 'primario')} Empleado: descifrar credenciales con la llave privada")  # Opción para descifrar credenciales.
    print()  # Dejamos una línea para separar acciones principales de soporte.
    print(colorear("Texto RSA paso a paso:", "negrita"))  # Dejamos el flujo manual como opción adicional.
    print(f"  {colorear('5)', 'secundario')} Encriptar texto con p y q manuales")  # Opción para cifrar texto con primos manuales.
    print(f"  {colorear('6)', 'secundario')} Desencriptar mensaje desde archivo TXT")  # Opción para descifrar el TXT generado.
    print()  # Dejamos una línea para separar soporte.
    print(colorear("Soporte y aprendizaje:", "negrita"))  # Agrupamos acciones de ayuda.
    print(f"  {colorear('7)', 'secundario')} Ver explicación RSA paso a paso")  # Opción de ayuda matemática.
    print(f"  {colorear('0)', 'muted')} Salir")  # Opción para cerrar el programa.


def ejecutar_opcion(opcion: str) -> bool:  # Ejecutamos una opción y devolvemos si el menú debe continuar.
    if opcion == "1":  # Detectamos la opción de generar llaves del empleado.
        generar_y_guardar_llaves()  # Ejecutamos la generación de llaves.
        pausar()  # Pausamos para leer el resultado.
        return True  # Indicamos que el menú debe continuar.
    if opcion == "2":  # Detectamos la opción de mostrar llave pública.
        mostrar_llave_publica()  # Mostramos la llave pública para compartir.
        pausar()  # Pausamos para leer el resultado.
        return True  # Indicamos que el menú debe continuar.
    if opcion == "3":  # Detectamos la opción de cifrar credenciales.
        cifrar_credenciales()  # Ejecutamos el cifrado de credenciales.
        pausar()  # Pausamos para leer el resultado.
        return True  # Indicamos que el menú debe continuar.
    if opcion == "4":  # Detectamos la opción de descifrar credenciales.
        descifrar_credenciales()  # Ejecutamos el descifrado de credenciales.
        pausar()  # Pausamos para leer el resultado.
        return True  # Indicamos que el menú debe continuar.
    if opcion == "5":  # Detectamos la opción de encriptar texto paso a paso.
        encriptar_texto_paso_a_paso()  # Ejecutamos el flujo de encriptación con p y q manuales.
        pausar()  # Pausamos para leer el resultado.
        return True  # Indicamos que el menú debe continuar.
    if opcion == "6":  # Detectamos la opción de desencriptar desde archivo TXT.
        desencriptar_archivo_txt()  # Ejecutamos el flujo de desencriptación desde TXT.
        pausar()  # Pausamos para leer el resultado.
        return True  # Indicamos que el menú debe continuar.
    if opcion == "7":  # Detectamos la opción de mostrar ayuda matemática.
        mostrar_explicacion_rsa()  # Mostramos la explicación RSA.
        pausar()  # Pausamos para leer el resultado.
        return True  # Indicamos que el menú debe continuar.
    if opcion == "0":  # Detectamos la opción de salir.
        imprimir_estado("Cerrando la interfaz RSA.", "INFO")  # Avisamos que terminamos.
        return False  # Indicamos que el menú debe cerrarse.
    imprimir_estado("Opción inválida. Elegí un número del menú.", "ERROR")  # Mostramos error claro para navegación.
    pausar()  # Pausamos para que el usuario lea.
    return True  # Mantenemos el menú abierto después del error.


def ejecutar_menu() -> None:  # Controlamos el ciclo principal de la terminal.
    continuar = True  # Inicializamos el ciclo como activo.
    while continuar:  # Mantenemos la aplicación abierta hasta que el usuario decida salir.
        limpiar_pantalla()  # Limpiamos antes de dibujar el menú para no acumular pantallas anteriores.
        mostrar_titulo()  # Mostramos el encabezado de la aplicación.
        mostrar_menu()  # Mostramos las opciones del menú.
        opcion = input(colorear("\nElegí una opción: ", "primario")).strip()  # Leemos la opción elegida con prompt destacado.
        limpiar_pantalla()  # Limpiamos antes de ejecutar la acción para que el resultado no quede pegado al menú.
        try:  # Encerramos cada acción para mostrar errores entendibles.
            continuar = ejecutar_opcion(opcion)  # Ejecutamos la opción y actualizamos el estado del ciclo.
        except Exception as error:  # Capturamos errores esperables de archivos, llaves o datos mal cargados.
            imprimir_estado(str(error), "ERROR")  # Mostramos el mensaje técnico del error con etiqueta clara.
            imprimir_texto("Revisá que estés usando la llave correcta y que los archivos JSON no hayan sido modificados a mano.")  # Damos una acción correctiva.
            pausar()  # Pausamos para que el usuario pueda corregir.


# ============================================================  # Título visual para marcar el punto de entrada del programa.
# SECCIÓN 15: ARRANQUE DE LA APLICACIÓN  # Esta parte ejecuta el menú solo cuando main.py se abre directamente.
# ============================================================  # Cierre visual de la sección de arranque.
if __name__ == "__main__":  # Ejecutamos la terminal solo cuando este archivo se abre directamente.
    ejecutar_menu()  # Lanzamos la interfaz interactiva.
