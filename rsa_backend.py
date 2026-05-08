# ============================================================  # Título visual para separar claramente las partes del backend.
# SECCIÓN 1: IMPORTACIONES  # Esta parte carga módulos de Python necesarios para JSON, rutas, tipos, datos y aleatoriedad segura.
# ============================================================  # Cierre visual de la sección de importaciones.
from __future__ import annotations  # Activamos anotaciones modernas para que los tipos sean claros.

import json  # Importamos JSON para guardar y leer llaves y mensajes cifrados.
import secrets  # Importamos secrets porque genera números aleatorios más adecuados para criptografía que random.
from dataclasses import dataclass  # Importamos dataclass para representar llaves de forma ordenada.
from pathlib import Path  # Importamos Path para manejar rutas de archivos sin depender del sistema operativo.
from typing import Any  # Importamos Any para describir datos JSON que pueden mezclar listas, textos y números.


# ============================================================  # Título visual para separar constantes globales del resto del código.
# SECCIÓN 2: CONFIGURACIÓN GENERAL  # Esta parte define valores base usados por todo el backend RSA.
# ============================================================  # Cierre visual de la sección de configuración.
CODIFICACION_TEXTO = "utf-8"  # Definimos UTF-8 para convertir credenciales con tildes o símbolos a bytes.
MINIMO_BITS_PRIMO = 8  # Definimos 8 bits como mínimo para que el módulo n sea mayor que cualquier byte.
RONDAS_MILLER_RABIN = 12  # Definimos rondas de prueba de primalidad para generar primos de forma confiable en este proyecto.


# ============================================================  # Título visual para ubicar las estructuras principales de datos.
# SECCIÓN 3: MODELOS DE LLAVES RSA  # Esta parte representa llaves públicas, privadas y el par completo generado.
# ============================================================  # Cierre visual de la sección de modelos.
@dataclass(frozen=True)  # Hacemos la clase inmutable para que una llave pública no cambie accidentalmente.
class LlavePublica:  # Definimos la estructura de la llave que el empleado sí puede compartir con su jefe.
    n: int  # Guardamos el módulo n = p * q que se usa tanto para cifrar como para descifrar.
    e: int  # Guardamos el exponente público e que se usa en la fórmula C = M^e mod n.


@dataclass(frozen=True)  # Hacemos la clase inmutable para proteger la llave privada en memoria.
class LlavePrivada:  # Definimos la estructura de la llave que solo debe conservar el empleado.
    n: int  # Guardamos el mismo módulo n que aparece también en la llave pública.
    d: int  # Guardamos el exponente privado d que se usa en la fórmula M = C^d mod n.


@dataclass(frozen=True)  # Hacemos inmutable el paquete completo de llaves y valores matemáticos.
class ParDeLlaves:  # Definimos el resultado completo de generar llaves RSA según el PDF.
    publica: LlavePublica  # Guardamos la llave pública (n, e) que puede viajar hacia el jefe.
    privada: LlavePrivada  # Guardamos la llave privada (n, d) que nunca debe compartirse.
    p: int  # Guardamos el primo p usado para calcular n, solo para explicación matemática local.
    q: int  # Guardamos el primo q usado para calcular n, solo para explicación matemática local.
    phi: int  # Guardamos phi(n) = (p - 1)(q - 1), solo para explicación matemática local.


@dataclass(frozen=True)  # Hacemos inmutable el detalle para que el proceso mostrado no se modifique accidentalmente.
class DetalleGeneracionRSA:  # Definimos una estructura con todo el proceso RSA paso a paso.
    p: int  # Guardamos el primo p ingresado por el usuario.
    q: int  # Guardamos el primo q ingresado por el usuario.
    n: int  # Guardamos n = p * q, que será el módulo RSA.
    phi: int  # Guardamos phi(n) = (p - 1)(q - 1), que se usa para d y e.
    posibles_d: list[int]  # Guardamos todos los d válidos menores que phi(n) y coprimos con phi(n).
    d: int  # Guardamos el d seleccionado para la clave privada.
    e_base: int  # Guardamos el inverso modular principal de d módulo phi(n).
    posibles_e: list[int]  # Guardamos ejemplos de valores e que cumplen e*d ≡ 1 mod phi(n).
    e: int  # Guardamos el e seleccionado para la clave pública.
    publica: LlavePublica  # Guardamos la clave pública final (n, e).
    privada: LlavePrivada  # Guardamos la clave privada final (n, d).


# ============================================================  # Título visual para marcar la matemática modular base.
# SECCIÓN 4: ARITMÉTICA MODULAR BÁSICA  # Esta parte calcula MCD, Euclides extendido e inverso modular para RSA.
# ============================================================  # Cierre visual de la sección matemática base.
def calcular_mcd(a: int, b: int) -> int:  # Calculamos el máximo común divisor usando Euclides.
    a = abs(a)  # Convertimos a positivo porque el MCD se define no negativo.
    b = abs(b)  # Convertimos b a positivo por la misma razón matemática.
    while b != 0:  # Repetimos hasta que el segundo valor sea cero.
        a, b = b, a % b  # Reemplazamos (a, b) por (b, residuo) según el algoritmo de Euclides.
    return a  # Devolvemos el último divisor no nulo, que es el MCD.


def algoritmo_extendido_euclides(a: int, b: int) -> tuple[int, int, int]:  # Calculamos MCD y coeficientes de Bézout.
    viejo_resto = a  # Guardamos el resto anterior, empezando con a.
    resto = b  # Guardamos el resto actual, empezando con b.
    viejo_x = 1  # Guardamos el coeficiente de a para el resto anterior.
    x = 0  # Guardamos el coeficiente de a para el resto actual.
    viejo_y = 0  # Guardamos el coeficiente de b para el resto anterior.
    y = 1  # Guardamos el coeficiente de b para el resto actual.
    while resto != 0:  # Iteramos mientras todavía haya resto para dividir.
        cociente = viejo_resto // resto  # Calculamos cuántas veces entra el resto actual en el anterior.
        viejo_resto, resto = resto, viejo_resto - cociente * resto  # Actualizamos los restos como en Euclides.
        viejo_x, x = x, viejo_x - cociente * x  # Actualizamos el coeficiente asociado a a.
        viejo_y, y = y, viejo_y - cociente * y  # Actualizamos el coeficiente asociado a b.
    return viejo_resto, viejo_x, viejo_y  # Devolvemos MCD y coeficientes x, y tales que ax + by = MCD.


def calcular_inverso_modular(valor: int, modulo: int) -> int:  # Calculamos el inverso modular pedido por e*d ≡ 1 mod phi(n).
    mcd, x, _ = algoritmo_extendido_euclides(valor, modulo)  # Obtenemos el MCD y el coeficiente que puede ser inverso.
    if mcd != 1:  # Verificamos que exista inverso, lo cual solo pasa si valor y módulo son coprimos.
        raise ValueError("No existe inverso modular porque los números no son coprimos.")  # Cortamos con un error claro.
    return x % modulo  # Normalizamos el inverso para que quede entre 0 y modulo - 1.


# ============================================================  # Título visual para separar la generación de números primos.
# SECCIÓN 5: PRUEBA Y GENERACIÓN DE PRIMOS  # Esta parte busca primos aleatorios usando Miller-Rabin para construir p y q.
# ============================================================  # Cierre visual de la sección de primos.
def es_probable_primo(numero: int, rondas: int = RONDAS_MILLER_RABIN) -> bool:  # Verificamos si un número parece primo.
    if numero < 2:  # Rechazamos números menores que 2 porque no son primos.
        return False  # Devolvemos falso para 0, 1 y negativos.
    primos_pequenos = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)  # Usamos primos chicos para descartar divisibles rápido.
    for primo in primos_pequenos:  # Recorremos los primos pequeños uno por uno.
        if numero == primo:  # Aceptamos si el número coincide exactamente con un primo pequeño.
            return True  # Devolvemos verdadero porque encontramos un primo exacto.
        if numero % primo == 0:  # Rechazamos si el número es divisible por un primo pequeño.
            return False  # Devolvemos falso porque un compuesto no sirve como p ni q.
    d = numero - 1  # Escribimos numero - 1 como d * 2^s para Miller-Rabin.
    s = 0  # Contamos cuántas veces se puede dividir por 2.
    while d % 2 == 0:  # Mientras d sea par seguimos factorizando potencias de 2.
        d //= 2  # Dividimos d entre 2 para quitar una potencia de 2.
        s += 1  # Aumentamos el contador de potencias de 2.
    for _ in range(rondas):  # Ejecutamos varias rondas para reducir la probabilidad de aceptar un compuesto.
        base = secrets.randbelow(numero - 3) + 2  # Elegimos una base aleatoria entre 2 y numero - 2.
        x = pow(base, d, numero)  # Calculamos base^d mod numero usando aritmética modular eficiente.
        if x == 1 or x == numero - 1:  # Aceptamos esta ronda si cae en un valor compatible con primo.
            continue  # Saltamos a la siguiente ronda porque esta no encontró evidencia de compuesto.
        for _ in range(s - 1):  # Elevamos al cuadrado hasta s - 1 veces buscando numero - 1.
            x = pow(x, 2, numero)  # Calculamos x^2 mod numero sin manejar números gigantes completos.
            if x == numero - 1:  # Si aparece numero - 1, la ronda queda aprobada.
                break  # Salimos del ciclo interno porque esta base no demostró que sea compuesto.
        else:  # Entramos aquí si nunca apareció numero - 1 en el ciclo interno.
            return False  # Devolvemos falso porque encontramos evidencia de que es compuesto.
    return True  # Devolvemos verdadero porque pasó todas las rondas de primalidad probabilística.


def generar_primo(bits: int) -> int:  # Generamos un número primo aleatorio con la cantidad de bits pedida.
    if bits < MINIMO_BITS_PRIMO:  # Validamos que el tamaño no sea demasiado pequeño para cifrar bytes.
        raise ValueError(f"El primo debe tener al menos {MINIMO_BITS_PRIMO} bits.")  # Informamos el mínimo permitido.
    while True:  # Repetimos hasta encontrar un candidato primo.
        candidato = secrets.randbits(bits)  # Creamos un candidato aleatorio con la cantidad de bits solicitada.
        candidato |= 1 << (bits - 1)  # Encendemos el bit superior para asegurar el tamaño real.
        candidato |= 1  # Encendemos el último bit para que el candidato sea impar.
        if es_probable_primo(candidato):  # Probamos si el candidato parece primo.
            return candidato  # Devolvemos el primo encontrado.


def elegir_exponente_privado(phi: int) -> int:  # Elegimos d como indica el PDF: d < phi(n) y MCD(d, phi(n)) = 1.
    while True:  # Repetimos hasta conseguir un d coprimo con phi.
        d = secrets.randbelow(phi - 3) + 2  # Elegimos d entre 2 y phi - 2 para evitar valores triviales.
        if calcular_mcd(d, phi) == 1:  # Validamos que d y phi sean coprimos para que exista e.
            return d  # Devolvemos el exponente privado aceptado.


def validar_primos_una_o_dos_cifras(p: int, q: int) -> None:  # Validamos los primos manuales de una o dos cifras.
    errores: list[str] = []  # Creamos una lista para acumular todos los errores encontrados.
    if p < 2 or p > 99:  # Verificamos que p tenga una o dos cifras y sea candidato primo positivo.
        errores.append("p debe ser un número primo de una o dos cifras, entre 2 y 99.")  # Agregamos un error claro para p.
    if q < 2 or q > 99:  # Verificamos que q tenga una o dos cifras y sea candidato primo positivo.
        errores.append("q debe ser un número primo de una o dos cifras, entre 2 y 99.")  # Agregamos un error claro para q.
    if p == q:  # Verificamos que los primos sean distintos como exige RSA.
        errores.append("p y q deben ser diferentes.")  # Agregamos el error de igualdad.
    if 2 <= p <= 99 and not es_probable_primo(p):  # Validamos primalidad de p cuando está en rango.
        errores.append("p no es primo; corregilo antes de continuar.")  # Agregamos el error de primalidad de p.
    if 2 <= q <= 99 and not es_probable_primo(q):  # Validamos primalidad de q cuando está en rango.
        errores.append("q no es primo; corregilo antes de continuar.")  # Agregamos el error de primalidad de q.
    if errores:  # Revisamos si se acumuló al menos un problema.
        raise ValueError("\n".join(errores))  # Rechazamos la entrada mostrando todos los problemas juntos.


def obtener_posibles_d(phi: int) -> list[int]:  # Calculamos todos los posibles d que cumplen MCD(d, phi(n)) = 1.
    return [d for d in range(2, phi) if calcular_mcd(d, phi) == 1]  # Devolvemos d entre 2 y phi - 1 coprimos con phi.


def obtener_posibles_e(d: int, phi: int, cantidad: int = 5) -> tuple[int, list[int]]:  # Calculamos ejemplos de e que cumplen e*d ≡ 1 mod phi(n).
    e_base = calcular_inverso_modular(d, phi)  # Calculamos el primer e positivo menor que phi usando inverso modular.
    ejemplos = [e_base + phi * k for k in range(cantidad)]  # Generamos ejemplos de la solución general e = e_base + phi*k.
    return e_base, ejemplos  # Devolvemos el e base y algunos valores posibles para mostrar el proceso.


def generar_llaves_desde_primos(p: int, q: int, d: int, e: int | None = None) -> DetalleGeneracionRSA:  # Generamos llaves usando p, q y d seleccionados por el usuario.
    validar_primos_una_o_dos_cifras(p, q)  # Rechazamos p y q si no cumplen las reglas del modo manual.
    n = p * q  # Calculamos n = p * q.
    phi = (p - 1) * (q - 1)  # Calculamos phi(n) = (p - 1)(q - 1).
    posibles_d = obtener_posibles_d(phi)  # Calculamos todos los d válidos para mostrarlos al usuario.
    if d not in posibles_d:  # Verificamos que el d elegido realmente sea válido.
        raise ValueError("El valor d seleccionado no es válido porque no es coprimo con phi(n).")  # Rechazamos d incorrecto.
    e_base, posibles_e = obtener_posibles_e(d, phi)  # Calculamos e y ejemplos de la solución general.
    e_final = e_base if e is None else e  # Usamos e_base si el usuario no seleccionó otro e congruente.
    if (e_final * d) % phi != 1:  # Validamos que el e final cumpla la congruencia de RSA.
        raise ValueError("El valor e seleccionado no cumple e*d ≡ 1 mod phi(n).")  # Rechazamos e incorrecto.
    publica = LlavePublica(n=n, e=e_final)  # Construimos la clave pública (n, e).
    privada = LlavePrivada(n=n, d=d)  # Construimos la clave privada (n, d).
    return DetalleGeneracionRSA(p=p, q=q, n=n, phi=phi, posibles_d=posibles_d, d=d, e_base=e_base, posibles_e=posibles_e, e=e_final, publica=publica, privada=privada)  # Devolvemos todo el detalle del proceso.


# ============================================================  # Título visual para el flujo principal de creación de llaves.
# SECCIÓN 6: GENERACIÓN DEL PAR DE LLAVES  # Esta parte aplica el orden del PDF: p, q, n, phi, d y e.
# ============================================================  # Cierre visual de la sección de generación de llaves.
def generar_llaves(bits_primo: int = 16) -> ParDeLlaves:  # Generamos el par de llaves RSA usando el orden explicado en el PDF.
    p = generar_primo(bits_primo)  # Elegimos el primer primo p.
    q = generar_primo(bits_primo)  # Elegimos el segundo primo q.
    while q == p:  # Verificamos que p y q sean distintos como exige RSA.
        q = generar_primo(bits_primo)  # Generamos otro q si salió igual que p.
    n = p * q  # Calculamos el módulo n = p * q.
    phi = (p - 1) * (q - 1)  # Calculamos phi(n) = (p - 1)(q - 1), como dice el PDF.
    d = elegir_exponente_privado(phi)  # Elegimos d privado tal que MCD(d, phi(n)) = 1.
    e = calcular_inverso_modular(d, phi)  # Calculamos e para que e*d ≡ 1 mod phi(n).
    if n <= 255:  # Verificamos que cada byte del mensaje sea menor que n.
        return generar_llaves(bits_primo + 1)  # Subimos un bit y regeneramos si el módulo quedó demasiado chico.
    publica = LlavePublica(n=n, e=e)  # Construimos la llave pública (n, e).
    privada = LlavePrivada(n=n, d=d)  # Construimos la llave privada (n, d).
    return ParDeLlaves(publica=publica, privada=privada, p=p, q=q, phi=phi)  # Devolvemos todo el paquete generado.


# ============================================================  # Título visual para separar conversión de objetos a datos guardables.
# SECCIÓN 7: SERIALIZACIÓN DE LLAVES Y JSON  # Esta parte convierte llaves a diccionarios y lee/escribe archivos JSON.
# ============================================================  # Cierre visual de la sección de serialización.
def llave_publica_a_diccionario(llave: LlavePublica) -> dict[str, int]:  # Convertimos la llave pública a formato JSON simple.
    return {"n": llave.n, "e": llave.e}  # Devolvemos solo n y e porque eso es lo único que debe compartir el empleado.


def llave_privada_a_diccionario(llave: LlavePrivada) -> dict[str, int]:  # Convertimos la llave privada a formato JSON simple.
    return {"n": llave.n, "d": llave.d}  # Devolvemos n y d porque esa es la llave privada del empleado.


def llave_publica_desde_diccionario(datos: dict[str, Any]) -> LlavePublica:  # Reconstruimos una llave pública desde JSON.
    return LlavePublica(n=int(datos["n"]), e=int(datos["e"]))  # Convertimos n y e a enteros por seguridad.


def llave_privada_desde_diccionario(datos: dict[str, Any]) -> LlavePrivada:  # Reconstruimos una llave privada desde JSON.
    return LlavePrivada(n=int(datos["n"]), d=int(datos["d"]))  # Convertimos n y d a enteros por seguridad.


def par_de_llaves_a_diccionario(par: ParDeLlaves) -> dict[str, Any]:  # Convertimos todo el par de llaves a JSON para guardarlo localmente.
    return {  # Creamos un diccionario con llave pública, privada y datos matemáticos.
        "publica": llave_publica_a_diccionario(par.publica),  # Guardamos la sección pública que se puede compartir.
        "privada": llave_privada_a_diccionario(par.privada),  # Guardamos la sección privada que no debe compartirse.
        "detalle_matematico": {"p": par.p, "q": par.q, "phi": par.phi},  # Guardamos p, q y phi solo para estudiar el proceso.
    }  # Cerramos el diccionario completo.


def guardar_json(ruta: Path, datos: dict[str, Any]) -> None:  # Guardamos un diccionario en un archivo JSON.
    texto = json.dumps(datos, ensure_ascii=False, indent=2)  # Convertimos los datos a texto JSON legible y con tildes correctas.
    ruta.write_text(texto + "\n", encoding=CODIFICACION_TEXTO)  # Escribimos el archivo usando UTF-8.


def leer_json(ruta: Path) -> dict[str, Any]:  # Leemos un archivo JSON desde disco.
    texto = ruta.read_text(encoding=CODIFICACION_TEXTO)  # Cargamos el texto usando UTF-8.
    datos = json.loads(texto)  # Parseamos el JSON a estructuras de Python.
    if not isinstance(datos, dict):  # Validamos que el archivo tenga un objeto JSON en la raíz.
        raise ValueError("El archivo JSON debe contener un objeto principal.")  # Rechazamos listas o valores sueltos.
    return datos  # Devolvemos el diccionario leído.


# ============================================================  # Título visual para separar las operaciones RSA directas.
# SECCIÓN 8: CIFRADO Y DESCIFRADO RSA  # Esta parte aplica C = M^e mod n y M = C^d mod n sobre números y texto.
# ============================================================  # Cierre visual de la sección de cifrado base.
def cifrar_numero(mensaje: int, llave: LlavePublica) -> int:  # Ciframos un número M con C = M^e mod n.
    if mensaje < 0 or mensaje >= llave.n:  # Verificamos la restricción del PDF: el mensaje M debe ser menor que n.
        raise ValueError("Cada bloque del mensaje debe cumplir 0 <= M < n.")  # Avisamos si el bloque no se puede cifrar.
    return pow(mensaje, llave.e, llave.n)  # Calculamos la potencia modular eficiente que produce el bloque cifrado.


def descifrar_numero(cifrado: int, llave: LlavePrivada) -> int:  # Desciframos un número C con M = C^d mod n.
    if cifrado < 0 or cifrado >= llave.n:  # Verificamos que el bloque cifrado esté en el rango modular válido.
        raise ValueError("Cada bloque cifrado debe cumplir 0 <= C < n.")  # Avisamos si el bloque no corresponde a esta llave.
    return pow(cifrado, llave.d, llave.n)  # Calculamos la potencia modular que recupera el bloque original.


def cifrar_texto(texto: str, llave: LlavePublica) -> list[int]:  # Ciframos texto convirtiéndolo primero a bytes UTF-8.
    bytes_mensaje = texto.encode(CODIFICACION_TEXTO)  # Convertimos el texto a bytes para trabajar con números menores que 256.
    return [cifrar_numero(byte, llave) for byte in bytes_mensaje]  # Ciframos cada byte como un mensaje M independiente.


def descifrar_texto(bloques: list[int], llave: LlavePrivada) -> str:  # Desciframos una lista de bloques numéricos a texto.
    bytes_descifrados = [descifrar_numero(int(bloque), llave) for bloque in bloques]  # Recuperamos cada byte original.
    for byte in bytes_descifrados:  # Revisamos que todos los resultados realmente sean bytes.
        if byte < 0 or byte > 255:  # Detectamos valores imposibles para UTF-8 por una llave incorrecta o datos corruptos.
            raise ValueError("La llave privada no corresponde o el mensaje cifrado está dañado.")  # Cortamos con diagnóstico claro.
    return bytes(bytes_descifrados).decode(CODIFICACION_TEXTO)  # Reconstruimos el texto original desde los bytes.


# ============================================================  # Título visual para marcar el caso de uso pedido por el usuario.
# SECCIÓN 9: FLUJO DE CREDENCIALES  # Esta parte cifra y descifra los dos datos sensibles del empleado y su jefe.
# ============================================================  # Cierre visual de la sección de credenciales.
def cifrar_dos_datos(dato_uno: str, dato_dos: str, llave: LlavePublica) -> dict[str, Any]:  # Ciframos dos credenciales con la llave pública.
    return {  # Armamos el paquete que el jefe le puede devolver al empleado.
        "algoritmo": "RSA educativo sin padding",  # Indicamos explícitamente que es una implementación académica.
        "advertencia": "No usar en producción; para sistemas reales usar RSA-OAEP de una librería auditada.",  # Dejamos clara la limitación de seguridad.
        "llave_publica_usada": llave_publica_a_diccionario(llave),  # Guardamos la llave pública usada para trazabilidad.
        "dato_uno_cifrado": cifrar_texto(dato_uno, llave),  # Ciframos el primer dato sensible.
        "dato_dos_cifrado": cifrar_texto(dato_dos, llave),  # Ciframos el segundo dato sensible.
    }  # Cerramos el paquete cifrado.


def descifrar_dos_datos(paquete: dict[str, Any], llave: LlavePrivada) -> tuple[str, str]:  # Desciframos los dos datos con la llave privada.
    dato_uno = descifrar_texto(list(paquete["dato_uno_cifrado"]), llave)  # Desciframos el primer dato sensible.
    dato_dos = descifrar_texto(list(paquete["dato_dos_cifrado"]), llave)  # Desciframos el segundo dato sensible.
    return dato_uno, dato_dos  # Devolvemos ambos datos originales al empleado.


# ============================================================  # Título visual para ubicar la prueba interna del backend.
# SECCIÓN 10: VERIFICACIÓN INTERNA  # Esta parte prueba que una llave pública y una privada realmente trabajen juntas.
# ============================================================  # Cierre visual de la sección de verificación.
def verificar_par_de_llaves(par: ParDeLlaves) -> bool:  # Probamos que una llave pública y privada trabajen como pareja.
    mensaje_prueba = "prueba"  # Usamos un texto corto para validar el ciclo completo.
    cifrado = cifrar_texto(mensaje_prueba, par.publica)  # Ciframos la prueba con la llave pública.
    descifrado = descifrar_texto(cifrado, par.privada)  # Desciframos la prueba con la llave privada.
    return descifrado == mensaje_prueba  # Confirmamos que el resultado sea exactamente el original.
