# ============================================================  # Título visual para separar las importaciones de la interfaz gráfica.
# SECCIÓN 1: IMPORTACIONES  # Esta parte carga Tkinter, JSON, rutas y funciones RSA del backend.
# ============================================================  # Cierre visual de la sección de importaciones.
from __future__ import annotations  # Activamos anotaciones modernas para que los tipos sean claros.

import json  # Importamos JSON para guardar y leer el archivo .txt compatible con bloc de notas.
import textwrap  # Importamos textwrap para crear recuadros ASCII legibles dentro de la interfaz.
import tkinter as tk  # Importamos Tkinter para construir una interfaz gráfica real.
from pathlib import Path  # Importamos Path para manejar rutas de archivos de forma segura.
from tkinter import filedialog, ttk  # Importamos diálogos de archivo y widgets modernos de Tkinter.
from typing import Any  # Importamos Any para representar datos JSON mixtos.

from rsa_backend import (  # Importamos la lógica RSA reutilizable desde el backend.
    DetalleGeneracionRSA,  # Importamos el detalle completo del proceso de generación RSA.
    LlavePrivada,  # Importamos la estructura de clave privada para descifrar textos y credenciales.
    LlavePublica,  # Importamos la estructura de clave pública para cifrar textos y credenciales.
    cifrar_dos_datos,  # Importamos el cifrado de dos credenciales del flujo empresa.
    cifrar_texto,  # Importamos la función que cifra texto con la clave pública.
    descifrar_dos_datos,  # Importamos el descifrado de dos credenciales del flujo empresa.
    descifrar_texto,  # Importamos la función que descifra bloques con la clave privada.
    generar_llaves,  # Importamos la generación automática de llaves para el flujo empleado/jefe.
    generar_llaves_desde_primos,  # Importamos la generación desde p, q, d y e.
    guardar_json,  # Importamos el guardado JSON usado por el flujo empresa.
    leer_json,  # Importamos la lectura JSON usada por el flujo empresa.
    llave_privada_desde_diccionario,  # Importamos la reconstrucción de llave privada desde archivo.
    llave_publica_a_diccionario,  # Importamos la serialización de llave pública compartible.
    llave_publica_desde_diccionario,  # Importamos la reconstrucción de llave pública desde archivo.
    obtener_posibles_d,  # Importamos el cálculo de posibles valores d.
    obtener_posibles_e,  # Importamos el cálculo de posibles valores e.
    par_de_llaves_a_diccionario,  # Importamos la serialización del par completo de llaves.
    validar_primos_una_o_dos_cifras,  # Importamos la validación de p y q manuales.
    verificar_par_de_llaves,  # Importamos una verificación interna para confirmar que las llaves funcionan.
)  # Cerramos la lista de importaciones propias.


# ============================================================  # Título visual para ubicar configuración global de la GUI.
# SECCIÓN 2: CONFIGURACIÓN  # Esta parte define rutas, colores y tamaños base de la ventana.
# ============================================================  # Cierre visual de la sección de configuración.
BASE_DIR = Path(__file__).resolve().parent  # Guardamos la carpeta actual del proyecto.
ARCHIVO_PUBLICO = BASE_DIR / "llave_publica.json"  # Definimos el archivo que el empleado puede compartir con el jefe.
ARCHIVO_PRIVADO = BASE_DIR / "llave_privada_empleado.json"  # Definimos el archivo privado que solo conserva el empleado.
ARCHIVO_CIFRADO = BASE_DIR / "credenciales_encriptadas.json"  # Definimos el archivo cifrado que el jefe devuelve al empleado.
ARCHIVO_MENSAJE_TXT = BASE_DIR / "mensaje_encriptado.txt"  # Definimos el TXT que se guardará por defecto en el modo paso a paso.
BITS_GUI = 16  # Definimos un tamaño pequeño para que la generación de llaves sea rápida en clase.
COLOR_FONDO = "#f6f8fb"  # Definimos un fondo claro para buena lectura.
COLOR_PANEL = "#ffffff"  # Definimos blanco para paneles de entrada y salida.
COLOR_PRIMARIO = "#0f5f9e"  # Definimos azul como color principal de acciones.
COLOR_ERROR = "#b00020"  # Definimos rojo para advertencias y errores.
COLOR_TEXTO = "#1f2937"  # Definimos gris oscuro para texto principal.


# ============================================================  # Título visual para funciones auxiliares de texto y validación.
# SECCIÓN 3: UTILIDADES  # Esta parte formatea listas, procesos, bloques y recuadros de advertencia.
# ============================================================  # Cierre visual de la sección de utilidades.
def formatear_lista_enteros(valores: list[int], por_linea: int = 12, limite: int = 120) -> str:  # Formateamos listas largas de candidatos.
    visibles = valores[:limite]  # Tomamos una cantidad limitada para que la UI no se sature.
    lineas: list[str] = []  # Creamos una lista donde guardaremos líneas formateadas.
    for indice in range(0, len(visibles), por_linea):  # Recorremos la lista por grupos.
        grupo = visibles[indice : indice + por_linea]  # Extraemos el grupo actual.
        lineas.append(", ".join(str(valor) for valor in grupo))  # Convertimos el grupo a texto separado por comas.
    if len(valores) > limite:  # Verificamos si ocultamos parte de la lista por tamaño.
        lineas.append(f"... se calcularon {len(valores)} valores en total")  # Indicamos cuántos valores reales existen.
    return "\n".join(lineas)  # Devolvemos las líneas unidas.


def resumir_bloques(bloques: list[int], limite: int = 8) -> str:  # Resumimos bloques cifrados para que la pantalla no explote.
    if len(bloques) <= limite:  # Si hay pocos bloques, se puede mostrar todo.
        return str(bloques)  # Devolvemos la lista completa.
    visibles = ", ".join(str(numero) for numero in bloques[:limite])  # Convertimos los primeros bloques a texto.
    return f"[{visibles}, ...] total={len(bloques)} bloques"  # Devolvemos una vista compacta con total.


def texto_cabe_en_modulo(texto: str, n: int) -> bool:  # Validamos que cada bloque del texto cumpla M < n.
    bytes_texto = texto.encode("utf-8")  # Convertimos el texto a bytes para usar la misma lógica del backend.
    if not bytes_texto:  # Revisamos si el texto está vacío.
        return True  # Un texto vacío no rompe la restricción matemática.
    return max(bytes_texto) < n  # Devolvemos verdadero si el byte más grande es menor que n.


def construir_recuadro_advertencia(mensaje: str) -> str:  # Creamos un recuadro ASCII para advertencias.
    ancho = 78  # Definimos un ancho estable para el recuadro dentro del panel de salida.
    lineas = textwrap.wrap(mensaje, width=ancho - 6)  # Partimos el mensaje dejando margen para bordes.
    borde = "+" + "-" * (ancho - 2) + "+"  # Creamos el borde superior e inferior.
    resultado = [borde, f"| {'[!] ADVERTENCIA':<{ancho - 4}} |", borde]  # Creamos título con símbolo ASCII.
    resultado.extend(f"| {linea:<{ancho - 4}} |" for linea in lineas)  # Agregamos cada línea dentro del recuadro.
    resultado.append(borde)  # Cerramos el recuadro.
    return "\n".join(resultado)  # Devolvemos el recuadro como texto.


def construir_proceso(texto: str, detalle: DetalleGeneracionRSA, bloques: list[int]) -> str:  # Construimos el proceso detallado para pantalla y TXT.
    return "\n".join(  # Unimos todas las líneas del proceso.
        [  # Abrimos la lista de líneas.
            "PROCESO DETALLADO RSA",  # Título del proceso.
            f"Texto original: {texto}",  # Texto ingresado por el usuario.
            f"p = {detalle.p}",  # Primo p.
            f"q = {detalle.q}",  # Primo q.
            f"n = p * q = {detalle.p} * {detalle.q} = {detalle.n}",  # Cálculo de n.
            f"phi(n) = (p - 1)(q - 1) = ({detalle.p} - 1)({detalle.q} - 1) = {detalle.phi}",  # Cálculo de phi.
            "Posibles valores de d con MCD(d, phi(n)) = 1:",  # Título de candidatos d.
            formatear_lista_enteros(detalle.posibles_d),  # Lista de candidatos d.
            f"d seleccionado = {detalle.d}",  # Valor d elegido.
            f"e debe cumplir e*d ≡ 1 mod phi(n), es decir e*{detalle.d} ≡ 1 mod {detalle.phi}",  # Congruencia para e.
            f"e base calculado = {detalle.e_base}",  # Inverso modular base.
            f"Posibles ejemplos de e = {', '.join(str(valor) for valor in detalle.posibles_e)}",  # Ejemplos de e.
            f"e seleccionado = {detalle.e}",  # Valor e elegido.
            f"Clave pública = (n, e) = ({detalle.n}, {detalle.e})",  # Clave pública.
            f"Clave privada = (n, d) = ({detalle.n}, {detalle.d})",  # Clave privada.
            f"Mensaje encriptado en bloques = {bloques}",  # Mensaje cifrado.
        ]  # Cerramos la lista de líneas.
    )  # Cerramos el join.


# ============================================================  # Título visual para la aplicación principal de Tkinter.
# SECCIÓN 4: INTERFAZ GRÁFICA  # Esta clase construye la ventana, entradas, botones y panel de salida.
# ============================================================  # Cierre visual de la sección de interfaz.
class AplicacionRSA(tk.Tk):  # Creamos una ventana principal especializada para la aplicación RSA.
    def __init__(self) -> None:  # Inicializamos la interfaz gráfica.
        super().__init__()  # Inicializamos la clase base Tk.
        self.title("Criptografía RSA")  # Definimos el título de la ventana.
        self.geometry("1040x760")  # Definimos un tamaño amplio para dos flujos y proceso detallado.
        self.configure(bg=COLOR_FONDO)  # Aplicamos color de fondo general.
        self.detalle_actual: DetalleGeneracionRSA | None = None  # Guardamos el detalle RSA calculado actualmente.
        self.posibles_d: list[int] = []  # Guardamos los posibles d calculados para el combo.
        self.crear_estilos()  # Configuramos estilos visuales de ttk.
        self.crear_widgets()  # Creamos todos los elementos de la ventana.

    def crear_estilos(self) -> None:  # Configuramos estilos consistentes para widgets ttk.
        estilo = ttk.Style()  # Creamos el manejador de estilos.
        estilo.configure("TFrame", background=COLOR_FONDO)  # Definimos fondo para frames generales.
        estilo.configure("Panel.TFrame", background=COLOR_PANEL)  # Definimos fondo blanco para paneles.
        estilo.configure("Titulo.TLabel", background=COLOR_FONDO, foreground=COLOR_PRIMARIO, font=("Arial", 20, "bold"))  # Definimos estilo de título.
        estilo.configure("Subtitulo.TLabel", background=COLOR_PANEL, foreground=COLOR_PRIMARIO, font=("Arial", 11, "bold"))  # Definimos subtítulos de secciones.
        estilo.configure("TLabel", background=COLOR_PANEL, foreground=COLOR_TEXTO, font=("Arial", 10))  # Definimos estilo de etiquetas.
        estilo.configure("TButton", font=("Arial", 10, "bold"), padding=8)  # Definimos estilo de botones.

    def crear_widgets(self) -> None:  # Construimos el layout principal de la GUI.
        titulo = ttk.Label(self, text="Criptografía RSA", style="Titulo.TLabel")  # Creamos el título principal sin texto decorativo innecesario.
        titulo.pack(pady=(16, 8))  # Ubicamos el título con espacio vertical.
        contenedor = ttk.Frame(self, padding=16)  # Creamos un contenedor general.
        contenedor.pack(fill="both", expand=True)  # Hacemos que el contenedor ocupe toda la ventana.
        panel_entrada = ttk.Frame(contenedor, style="Panel.TFrame", padding=16)  # Creamos panel izquierdo para entradas.
        panel_entrada.pack(side="left", fill="y", padx=(0, 12))  # Ubicamos panel de entrada a la izquierda.
        panel_salida = ttk.Frame(contenedor, style="Panel.TFrame", padding=16)  # Creamos panel derecho para resultados.
        panel_salida.pack(side="right", fill="both", expand=True)  # Ubicamos panel de salida a la derecha.
        pestañas = ttk.Notebook(panel_entrada)  # Creamos pestañas para separar el flujo empresa del modo paso a paso.
        pestañas.pack(fill="both", expand=True)  # Permitimos que las pestañas ocupen el panel de entrada.
        pestaña_empresa = ttk.Frame(pestañas, style="Panel.TFrame", padding=12)  # Creamos la pestaña del flujo empleado/jefe.
        pestaña_manual = ttk.Frame(pestañas, style="Panel.TFrame", padding=12)  # Creamos la pestaña del flujo manual paso a paso.
        pestañas.add(pestaña_empresa, text="Flujo empresa")  # Agregamos la pestaña principal de empresa.
        pestañas.add(pestaña_manual, text="Texto paso a paso")  # Agregamos la pestaña secundaria de texto manual.
        self.crear_pestaña_empresa(pestaña_empresa)  # Construimos los controles del flujo empleado/jefe.
        self.crear_pestaña_manual(pestaña_manual)  # Construimos los controles del flujo paso a paso.
        ttk.Label(panel_salida, text="Proceso y resultado").pack(anchor="w")  # Etiqueta del panel de salida.
        self.salida = tk.Text(panel_salida, wrap="word", bg="#0b1020", fg="#e5e7eb", insertbackground="#ffffff")  # Área de salida estilo consola.
        self.salida.pack(fill="both", expand=True, pady=(4, 0))  # Ubicamos el área de salida.
        self.salida.tag_configure("rojo", foreground=COLOR_ERROR)  # Configuramos etiqueta roja para advertencias.
        self.salida.tag_configure("ok", foreground="#22c55e")  # Configuramos etiqueta verde para éxitos.

    def crear_pestaña_empresa(self, panel: ttk.Frame) -> None:  # Construimos la pestaña del flujo original empleado/jefe.
        ttk.Label(panel, text="Empleado", style="Subtitulo.TLabel").pack(anchor="w")  # Marcamos el bloque del empleado.
        ttk.Button(panel, text="Generar llaves pública y privada", command=self.generar_llaves_empresa).pack(fill="x", pady=(4, 8))  # Botón para crear llaves.
        ttk.Button(panel, text="Mostrar llave pública para el jefe", command=self.mostrar_publica_empresa).pack(fill="x", pady=(0, 16))  # Botón para ver la pública.
        ttk.Label(panel, text="Jefe", style="Subtitulo.TLabel").pack(anchor="w")  # Marcamos el bloque del jefe.
        ttk.Label(panel, text="Usuario o identificador").pack(anchor="w")  # Etiqueta para el primer dato.
        self.dato_uno_var = tk.StringVar()  # Variable del primer dato sensible.
        ttk.Entry(panel, textvariable=self.dato_uno_var, width=34).pack(anchor="w", pady=(4, 10))  # Campo del primer dato.
        ttk.Label(panel, text="Contraseña o segundo dato").pack(anchor="w")  # Etiqueta para el segundo dato.
        self.dato_dos_var = tk.StringVar()  # Variable del segundo dato sensible.
        ttk.Entry(panel, textvariable=self.dato_dos_var, width=34, show="*").pack(anchor="w", pady=(4, 10))  # Campo oculto para el segundo dato.
        ttk.Button(panel, text="Cifrar credenciales con llave pública", command=self.cifrar_empresa).pack(fill="x", pady=(4, 12))  # Botón para cifrar credenciales.
        ttk.Label(panel, text="Empleado", style="Subtitulo.TLabel").pack(anchor="w")  # Marcamos el cierre del flujo por el empleado.
        ttk.Button(panel, text="Descifrar credenciales con llave privada", command=self.descifrar_empresa).pack(fill="x", pady=(4, 8))  # Botón para descifrar credenciales.

    def crear_pestaña_manual(self, panel: ttk.Frame) -> None:  # Construimos la pestaña del texto RSA paso a paso.
        ttk.Label(panel, text="Texto a encriptar").pack(anchor="w")  # Etiqueta para el texto.
        self.texto = tk.Text(panel, width=36, height=5, wrap="word")  # Campo multilínea para texto libre.
        self.texto.pack(pady=(4, 12))  # Ubicamos campo de texto.
        ttk.Label(panel, text="Primo p (1 o 2 cifras)").pack(anchor="w")  # Etiqueta para p.
        self.p_var = tk.StringVar()  # Variable vinculada al campo p.
        ttk.Entry(panel, textvariable=self.p_var, width=18).pack(anchor="w", pady=(4, 12))  # Campo de entrada para p.
        ttk.Label(panel, text="Primo q (1 o 2 cifras)").pack(anchor="w")  # Etiqueta para q.
        self.q_var = tk.StringVar()  # Variable vinculada al campo q.
        ttk.Entry(panel, textvariable=self.q_var, width=18).pack(anchor="w", pady=(4, 12))  # Campo de entrada para q.
        ttk.Button(panel, text="Calcular candidatos d", command=self.calcular_candidatos).pack(fill="x", pady=(4, 12))  # Botón para validar y calcular d.
        ttk.Label(panel, text="Seleccionar d").pack(anchor="w")  # Etiqueta para selector d.
        self.d_var = tk.StringVar()  # Variable vinculada al combo de d.
        self.combo_d = ttk.Combobox(panel, textvariable=self.d_var, state="readonly", width=24)  # Combo para elegir d.
        self.combo_d.pack(anchor="w", pady=(4, 12))  # Ubicamos el combo de d.
        ttk.Button(panel, text="Encriptar y guardar TXT", command=self.encriptar_guardar).pack(fill="x", pady=(8, 8))  # Botón para cifrar y guardar.
        ttk.Button(panel, text="Desencriptar TXT", command=self.desencriptar_txt).pack(fill="x", pady=(0, 8))  # Botón para descifrar archivo.

    def escribir(self, texto: str, etiqueta: str | None = None) -> None:  # Escribimos texto en el panel de salida.
        self.salida.insert("end", texto + "\n", etiqueta)  # Insertamos texto con etiqueta opcional.
        self.salida.see("end")  # Movemos la vista al final.

    def limpiar_salida(self) -> None:  # Limpiamos el panel de salida.
        self.salida.delete("1.0", "end")  # Borramos todo el contenido actual.

    def advertir(self, mensaje: str) -> None:  # Mostramos advertencias rojas en recuadro ASCII.
        self.escribir(construir_recuadro_advertencia(mensaje), "rojo")  # Insertamos el recuadro con etiqueta roja.

    def cargar_llave_publica_empresa(self) -> LlavePublica:  # Cargamos la llave pública del flujo empresa.
        if not ARCHIVO_PUBLICO.exists():  # Verificamos que el archivo público exista.
            raise ValueError("No existe llave_publica.json; primero generá las llaves del empleado.")  # Explicamos el paso faltante.
        return llave_publica_desde_diccionario(leer_json(ARCHIVO_PUBLICO))  # Reconstruimos y devolvemos la llave pública.

    def cargar_llave_privada_empresa(self) -> LlavePrivada:  # Cargamos la llave privada del flujo empresa.
        if not ARCHIVO_PRIVADO.exists():  # Verificamos que el archivo privado exista.
            raise ValueError("No existe llave_privada_empleado.json; primero generá las llaves del empleado.")  # Explicamos el paso faltante.
        datos = leer_json(ARCHIVO_PRIVADO)  # Leemos el archivo privado completo.
        return llave_privada_desde_diccionario(datos["privada"])  # Extraemos y reconstruimos la llave privada.

    def generar_llaves_empresa(self) -> None:  # Ejecutamos la generación de llaves del empleado.
        self.limpiar_salida()  # Limpiamos cualquier resultado anterior.
        try:  # Intentamos generar y guardar las llaves.
            self.escribir("Generando llaves RSA para el empleado...")  # Informamos que empieza el cálculo.
            self.update_idletasks()  # Refrescamos la ventana antes del cálculo.
            par = generar_llaves(BITS_GUI)  # Generamos el par de llaves del empleado.
            if not verificar_par_de_llaves(par):  # Verificamos que el par cifre y descifre correctamente.
                raise RuntimeError("El par de llaves generado no pasó la verificación interna.")  # Cortamos si algo grave falló.
            guardar_json(ARCHIVO_PRIVADO, par_de_llaves_a_diccionario(par))  # Guardamos el archivo privado completo.
            guardar_json(ARCHIVO_PUBLICO, llave_publica_a_diccionario(par.publica))  # Guardamos la llave pública compartible.
            self.limpiar_salida()  # Limpiamos el mensaje temporal.
            self.escribir("LLAVES GENERADAS CORRECTAMENTE", "ok")  # Mostramos estado de éxito.
            self.escribir(f"Archivo público para el jefe: {ARCHIVO_PUBLICO.name}", "ok")  # Indicamos el archivo público.
            self.escribir(f"Archivo privado del empleado: {ARCHIVO_PRIVADO.name}", "ok")  # Indicamos el archivo privado.
            self.escribir(f"Llave pública (n, e): ({par.publica.n}, {par.publica.e})")  # Mostramos la llave pública.
            self.escribir(f"Llave privada (n, d): ({par.privada.n}, {par.privada.d})")  # Mostramos la privada para estudio local.
            self.escribir(f"Detalle matemático: p={par.p}, q={par.q}, phi(n)={par.phi}")  # Mostramos el cálculo base.
            self.advertir("No compartas llave_privada_empleado.json. La privada existe para descifrar, no para viajar por correo ni chat.")  # Reforzamos la regla central.
        except Exception as error:  # Capturamos fallos inesperados o de archivo.
            self.limpiar_salida()  # Limpiamos la salida parcial.
            self.advertir(str(error))  # Mostramos el error en rojo.

    def mostrar_publica_empresa(self) -> None:  # Mostramos la llave pública para que el jefe pueda cifrar.
        self.limpiar_salida()  # Limpiamos resultados anteriores.
        try:  # Intentamos cargar la llave pública.
            llave = self.cargar_llave_publica_empresa()  # Cargamos la llave pública guardada.
            self.escribir("LLAVE PÚBLICA PARA COMPARTIR", "ok")  # Mostramos título de salida.
            self.escribir(f"n = {llave.n}")  # Mostramos n.
            self.escribir(f"e = {llave.e}")  # Mostramos e.
            self.escribir(f"archivo = {ARCHIVO_PUBLICO.name}")  # Mostramos el archivo compartible.
            self.advertir("Compartí solo esta llave pública. Si compartís la privada, cualquiera puede descifrar.")  # Advertimos sobre la frontera pública/privada.
        except Exception as error:  # Capturamos errores de archivo.
            self.advertir(str(error))  # Mostramos el error en rojo.

    def cifrar_empresa(self) -> None:  # Ejecutamos el cifrado de credenciales del jefe.
        self.limpiar_salida()  # Limpiamos resultados anteriores.
        try:  # Intentamos cifrar los dos datos.
            dato_uno = self.dato_uno_var.get().strip()  # Leemos el primer dato sensible.
            dato_dos = self.dato_dos_var.get().strip()  # Leemos el segundo dato sensible.
            if dato_uno == "" or dato_dos == "":  # Verificamos que ambos campos tengan contenido.
                raise ValueError("Completá el usuario y la contraseña antes de cifrar.")  # Rechazamos formularios incompletos.
            llave = self.cargar_llave_publica_empresa()  # Cargamos la llave pública del empleado.
            paquete = cifrar_dos_datos(dato_uno, dato_dos, llave)  # Ciframos ambos datos con RSA.
            guardar_json(ARCHIVO_CIFRADO, paquete)  # Guardamos el paquete cifrado para devolver al empleado.
            self.escribir("CREDENCIALES CIFRADAS", "ok")  # Mostramos estado de éxito.
            self.escribir(f"Archivo para devolver al empleado: {ARCHIVO_CIFRADO.name}", "ok")  # Indicamos el archivo generado.
            self.escribir(f"Dato 1 cifrado: {resumir_bloques(list(paquete['dato_uno_cifrado']))}")  # Mostramos resumen del primer cifrado.
            self.escribir(f"Dato 2 cifrado: {resumir_bloques(list(paquete['dato_dos_cifrado']))}")  # Mostramos resumen del segundo cifrado.
        except Exception as error:  # Capturamos errores de llaves o datos.
            self.advertir(str(error))  # Mostramos el error en rojo.

    def descifrar_empresa(self) -> None:  # Ejecutamos el descifrado de credenciales del empleado.
        self.limpiar_salida()  # Limpiamos resultados anteriores.
        try:  # Intentamos leer y descifrar el paquete.
            if not ARCHIVO_CIFRADO.exists():  # Verificamos que exista el archivo cifrado.
                raise ValueError("No existe credenciales_encriptadas.json; primero cifrá credenciales con la llave pública.")  # Explicamos el paso faltante.
            paquete = leer_json(ARCHIVO_CIFRADO)  # Leemos el paquete cifrado.
            llave = self.cargar_llave_privada_empresa()  # Cargamos la llave privada del empleado.
            dato_uno, dato_dos = descifrar_dos_datos(paquete, llave)  # Desciframos ambos datos sensibles.
            self.escribir("CREDENCIALES DESCIFRADAS", "ok")  # Mostramos estado de éxito.
            self.escribir(f"Dato 1 original: {dato_uno}", "ok")  # Mostramos el primer dato recuperado.
            self.escribir(f"Dato 2 original: {dato_dos}", "ok")  # Mostramos el segundo dato recuperado.
        except Exception as error:  # Capturamos errores de archivo, llave o descifrado.
            self.advertir(str(error))  # Mostramos el error en rojo.

    def leer_primos(self) -> tuple[int, int]:  # Leemos p y q desde los campos de entrada.
        p = int(self.p_var.get().strip())  # Convertimos p a entero.
        q = int(self.q_var.get().strip())  # Convertimos q a entero.
        validar_primos_una_o_dos_cifras(p, q)  # Validamos p y q como primos manuales aceptados.
        return p, q  # Devolvemos p y q validados.

    def leer_texto(self) -> str:  # Leemos el texto ingresado por el usuario.
        texto = self.texto.get("1.0", "end").strip()  # Obtenemos el contenido del campo multilínea.
        if texto == "":  # Verificamos que el texto no esté vacío.
            raise ValueError("El texto a encriptar no puede estar vacío.")  # Rechazamos texto vacío.
        return texto  # Devolvemos el texto válido.

    def calcular_candidatos(self) -> None:  # Calculamos n, phi y posibles d.
        self.limpiar_salida()  # Limpiamos resultados anteriores.
        try:  # Intentamos validar todo el formulario.
            texto = self.leer_texto()  # Leemos el texto a cifrar.
            p, q = self.leer_primos()  # Leemos y validamos primos.
            n = p * q  # Calculamos n.
            if not texto_cabe_en_modulo(texto, n):  # Verificamos que cada bloque del texto sea menor que n.
                raise ValueError(f"Con esos primos n={n}, pero el texto contiene bytes mayores o iguales a n. Elegí primos más grandes.")  # Rechazamos módulos chicos.
            phi = (p - 1) * (q - 1)  # Calculamos phi(n).
            self.posibles_d = obtener_posibles_d(phi)  # Calculamos candidatos d.
            self.combo_d["values"] = [str(valor) for valor in self.posibles_d]  # Cargamos los candidatos en el combo.
            self.combo_d.set(str(self.posibles_d[0]))  # Seleccionamos el primer candidato por defecto.
            self.escribir(f"n = p*q = {p}*{q} = {n}")  # Mostramos n.
            self.escribir(f"phi(n) = (p-1)(q-1) = ({p}-1)({q}-1) = {phi}")  # Mostramos phi.
            self.escribir("Posibles valores de d:")  # Título de candidatos d.
            self.escribir(formatear_lista_enteros(self.posibles_d))  # Mostramos candidatos d.
        except Exception as error:  # Capturamos cualquier error de validación.
            self.advertir(str(error))  # Mostramos el error como advertencia roja.

    def encriptar_guardar(self) -> None:  # Encriptamos el texto y guardamos el archivo TXT.
        self.limpiar_salida()  # Limpiamos resultados anteriores.
        try:  # Intentamos ejecutar todo el proceso.
            texto = self.leer_texto()  # Leemos el texto.
            p, q = self.leer_primos()  # Leemos p y q.
            if self.d_var.get().strip() == "":  # Verificamos que exista un d seleccionado.
                raise ValueError("Primero calculá candidatos d y seleccioná uno.")  # Explicamos el paso faltante.
            d = int(self.d_var.get())  # Leemos d seleccionado.
            e_base, _ = obtener_posibles_e(d, (p - 1) * (q - 1))  # Calculamos e base.
            detalle = generar_llaves_desde_primos(p, q, d, e_base)  # Generamos el detalle completo de claves.
            bloques = cifrar_texto(texto, detalle.publica)  # Ciframos el texto.
            proceso = construir_proceso(texto, detalle, bloques)  # Construimos el proceso detallado.
            paquete = {"mensaje_encriptado": bloques, "clave_privada_para_descifrar": {"n": detalle.n, "d": detalle.d}}  # Creamos paquete TXT sin texto original ni proceso detallado.
            ARCHIVO_MENSAJE_TXT.write_text(json.dumps(paquete, ensure_ascii=False, indent=2), encoding="utf-8")  # Guardamos el TXT.
            self.escribir(proceso)  # Mostramos el proceso.
            self.advertir("El TXT incluye clave privada para poder descifrar este ejercicio. En seguridad real, una clave privada no se comparte.")  # Mostramos advertencia roja.
            self.escribir(f"Archivo guardado: {ARCHIVO_MENSAJE_TXT}", "ok")  # Confirmamos guardado.
        except Exception as error:  # Capturamos errores de cálculo o formulario.
            self.advertir(str(error))  # Mostramos el error en recuadro rojo.

    def desencriptar_txt(self) -> None:  # Desencriptamos un archivo TXT generado por la app.
        ruta = filedialog.askopenfilename(initialdir=BASE_DIR, title="Seleccionar TXT", filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")])  # Abrimos diálogo de archivo.
        if ruta == "":  # Revisamos si el usuario canceló.
            return  # Salimos sin hacer nada.
        self.limpiar_salida()  # Limpiamos resultados anteriores.
        try:  # Intentamos leer y descifrar.
            datos: dict[str, Any] = json.loads(Path(ruta).read_text(encoding="utf-8"))  # Leemos el paquete JSON del TXT.
            bloques = [int(valor) for valor in datos["mensaje_encriptado"]]  # Convertimos bloques a enteros.
            clave = datos["clave_privada_para_descifrar"]  # Extraemos clave privada.
            privada = LlavePrivada(n=int(clave["n"]), d=int(clave["d"]))  # Reconstruimos clave privada.
            texto = descifrar_texto(bloques, privada)  # Desciframos texto.
            self.escribir("TEXTO DESENCRIPTADO", "ok")  # Mostramos título de éxito.
            self.escribir(texto, "ok")  # Mostramos texto recuperado.
        except Exception as error:  # Capturamos errores de archivo o clave.
            self.advertir(str(error))  # Mostramos error en recuadro rojo.


# ============================================================  # Título visual para el arranque de la GUI.
# SECCIÓN 5: ARRANQUE  # Esta parte abre la ventana solo cuando gui.py se ejecuta directamente.
# ============================================================  # Cierre visual de la sección de arranque.
if __name__ == "__main__":  # Verificamos si este archivo se ejecutó directamente.
    app = AplicacionRSA()  # Creamos la aplicación gráfica.
    app.mainloop()  # Iniciamos el bucle de eventos de Tkinter.
