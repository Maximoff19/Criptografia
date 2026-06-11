# Backend educativo RSA en Python

Este proyecto implementa la lógica RSA del PDF **Aritmética modular y Criptografía RSA.pdf**:

- elegir primos distintos `p` y `q`
- calcular `n = p * q`
- calcular `phi(n) = (p - 1)(q - 1)`
- elegir `d` con `MCD(d, phi(n)) = 1`
- calcular `e` con `e * d ≡ 1 mod phi(n)`
- cifrar con `C = M^e mod n`
- descifrar con `M = C^d mod n`

## Porciones importantes del código para el cálculo RSA

Acá tenés las funciones más importantes para entender el cálculo. No son decoración: estas partes son el corazón matemático del programa. Si entendés esto, entendés RSA; si no, solo estás apretando botones, y eso no sirve.

### 1. Máximo común divisor: `calcular_mcd`

Esta función usa el algoritmo de Euclides para saber si dos números son coprimos. En RSA se usa para validar que `d` sea compatible con `phi(n)`.

```python
def calcular_mcd(a: int, b: int) -> int:
    # Convertimos ambos números a positivos porque el MCD no depende del signo.
    a = abs(a)
    b = abs(b)

    # Mientras el segundo número no sea cero, seguimos aplicando Euclides.
    while b != 0:
        # El nuevo par pasa a ser: divisor actual y residuo de la división.
        a, b = b, a % b

    # Cuando b llega a cero, a contiene el máximo común divisor.
    return a
```

**Idea clave:** si `MCD(d, phi(n)) = 1`, entonces `d` tiene inverso modular y se puede calcular `e`.

### 2. Euclides extendido e inverso modular

RSA necesita encontrar `e` de forma que:

```text
e * d ≡ 1 mod phi(n)
```

Eso significa que `e` es el inverso modular de `d` módulo `phi(n)`.

```python
def algoritmo_extendido_euclides(a: int, b: int) -> tuple[int, int, int]:
    # Guardamos los restos del algoritmo de Euclides.
    viejo_resto = a
    resto = b

    # Coeficientes para construir la identidad de Bézout: ax + by = MCD(a, b).
    viejo_x = 1
    x = 0
    viejo_y = 0
    y = 1

    # Repetimos hasta que ya no quede resto.
    while resto != 0:
        # Calculamos el cociente de la división entera.
        cociente = viejo_resto // resto

        # Actualizamos restos y coeficientes.
        viejo_resto, resto = resto, viejo_resto - cociente * resto
        viejo_x, x = x, viejo_x - cociente * x
        viejo_y, y = y, viejo_y - cociente * y

    # Devuelve: MCD, coeficiente x y coeficiente y.
    return viejo_resto, viejo_x, viejo_y


def calcular_inverso_modular(valor: int, modulo: int) -> int:
    # Buscamos el coeficiente x tal que valor*x + modulo*y = 1.
    mcd, x, _ = algoritmo_extendido_euclides(valor, modulo)

    # Si el MCD no es 1, no existe inverso modular.
    if mcd != 1:
        raise ValueError("No existe inverso modular porque los números no son coprimos.")

    # Normalizamos x para que quede como número positivo dentro del módulo.
    return x % modulo
```

**Idea clave:** esta función calcula `e`, que después se usa en la clave pública `(n, e)`.

### 3. Validación de primos `p` y `q`

RSA arranca eligiendo dos primos distintos. Si `p` y `q` están mal, TODO el cálculo queda mal. No hay magia.

```python
def validar_primos_una_o_dos_cifras(p: int, q: int) -> None:
    # Acumulamos errores para mostrarlos todos juntos.
    errores: list[str] = []

    # p debe estar entre 2 y 99 para cumplir la consigna de una o dos cifras.
    if p < 2 or p > 99:
        errores.append("p debe ser un número primo de una o dos cifras, entre 2 y 99.")

    # q también debe estar entre 2 y 99.
    if q < 2 or q > 99:
        errores.append("q debe ser un número primo de una o dos cifras, entre 2 y 99.")

    # En RSA p y q no pueden ser iguales.
    if p == q:
        errores.append("p y q deben ser diferentes.")

    # Verificamos que p realmente sea primo.
    if 2 <= p <= 99 and not es_probable_primo(p):
        errores.append("p no es primo; corregilo antes de continuar.")

    # Verificamos que q realmente sea primo.
    if 2 <= q <= 99 and not es_probable_primo(q):
        errores.append("q no es primo; corregilo antes de continuar.")

    # Si hubo errores, detenemos el cálculo.
    if errores:
        raise ValueError("\n".join(errores))
```

**Idea clave:** sin primos válidos no existe un RSA correcto. Primero se valida, después se calcula.

### 4. Candidatos para `d` y `e`

`d` debe ser coprimo con `phi(n)`. Luego `e` se calcula como inverso modular de `d`.

```python
def obtener_posibles_d(phi: int) -> list[int]:
    # Buscamos todos los valores d entre 2 y phi - 1.
    # Solo sirven los que cumplen MCD(d, phi) = 1.
    return [d for d in range(2, phi) if calcular_mcd(d, phi) == 1]


def obtener_posibles_e(d: int, phi: int, cantidad: int = 5) -> tuple[int, list[int]]:
    # Calculamos el inverso modular principal de d.
    e_base = calcular_inverso_modular(d, phi)

    # Generamos ejemplos usando la forma general: e = e_base + phi*k.
    ejemplos = [e_base + phi * k for k in range(cantidad)]

    # Devolvemos el e base y algunos ejemplos posibles.
    return e_base, ejemplos
```

**Idea clave:** `d` forma la clave privada `(n, d)` y `e` forma la clave pública `(n, e)`.

### 5. Generación de llaves desde `p`, `q` y `d`

Esta es la función más importante del modo paso a paso, porque junta todos los cálculos matemáticos: `n`, `phi(n)`, `d`, `e`, clave pública y clave privada.

```python
def generar_llaves_desde_primos(p: int, q: int, d: int, e: int | None = None) -> DetalleGeneracionRSA:
    # Primero validamos que p y q sean primos aceptables y diferentes.
    validar_primos_una_o_dos_cifras(p, q)

    # Calculamos el módulo RSA.
    n = p * q

    # Calculamos phi(n), necesario para elegir d y calcular e.
    phi = (p - 1) * (q - 1)

    # Calculamos todos los valores posibles de d.
    posibles_d = obtener_posibles_d(phi)

    # Validamos que el d elegido esté permitido.
    if d not in posibles_d:
        raise ValueError("El valor d seleccionado no es válido porque no es coprimo con phi(n).")

    # Calculamos e como inverso modular de d módulo phi(n).
    e_base, posibles_e = obtener_posibles_e(d, phi)

    # Si no se pasa un e manual, usamos el e base.
    e_final = e_base if e is None else e

    # Verificamos la regla central: e*d debe dejar residuo 1 módulo phi(n).
    if (e_final * d) % phi != 1:
        raise ValueError("El valor e seleccionado no cumple e*d ≡ 1 mod phi(n).")

    # Armamos la clave pública y la clave privada.
    publica = LlavePublica(n=n, e=e_final)
    privada = LlavePrivada(n=n, d=d)

    # Devolvemos el detalle completo para mostrar el proceso en pantalla.
    return DetalleGeneracionRSA(
        p=p,
        q=q,
        n=n,
        phi=phi,
        posibles_d=posibles_d,
        d=d,
        e_base=e_base,
        posibles_e=posibles_e,
        e=e_final,
        publica=publica,
        privada=privada,
    )
```

**Idea clave:** esta función transforma `p` y `q` en las llaves reales del sistema.

### 6. Cifrado RSA

El cifrado usa la fórmula:

```text
C = M^e mod n
```

En el programa, cada carácter del texto se convierte a bytes y cada byte se cifra como un número.

```python
def cifrar_numero(mensaje: int, llave: LlavePublica) -> int:
    # En RSA el mensaje numérico M debe cumplir 0 <= M < n.
    if mensaje < 0 or mensaje >= llave.n:
        raise ValueError("Cada bloque del mensaje debe cumplir 0 <= M < n.")

    # Calculamos C = M^e mod n usando pow con módulo para hacerlo eficiente.
    return pow(mensaje, llave.e, llave.n)


def cifrar_texto(texto: str, llave: LlavePublica) -> list[int]:
    # Convertimos el texto a bytes UTF-8.
    bytes_mensaje = texto.encode(CODIFICACION_TEXTO)

    # Ciframos cada byte como un bloque independiente.
    return [cifrar_numero(byte, llave) for byte in bytes_mensaje]
```

**Idea clave:** para cifrar se usa la clave pública. Por eso el jefe puede cifrar sin conocer la clave privada.

### 7. Descifrado RSA

El descifrado usa la fórmula:

```text
M = C^d mod n
```

```python
def descifrar_numero(cifrado: int, llave: LlavePrivada) -> int:
    # El bloque cifrado C también debe estar dentro del rango modular.
    if cifrado < 0 or cifrado >= llave.n:
        raise ValueError("Cada bloque cifrado debe cumplir 0 <= C < n.")

    # Calculamos M = C^d mod n para recuperar el número original.
    return pow(cifrado, llave.d, llave.n)


def descifrar_texto(bloques: list[int], llave: LlavePrivada) -> str:
    # Desciframos cada bloque y recuperamos los bytes originales.
    bytes_descifrados = [descifrar_numero(int(bloque), llave) for bloque in bloques]

    # Validamos que cada resultado sea un byte real entre 0 y 255.
    for byte in bytes_descifrados:
        if byte < 0 or byte > 255:
            raise ValueError("La llave privada no corresponde o el mensaje cifrado está dañado.")

    # Reconstruimos el texto desde los bytes UTF-8.
    return bytes(bytes_descifrados).decode(CODIFICACION_TEXTO)
```

**Idea clave:** para descifrar se necesita la clave privada. Si se comparte `d`, se rompe la seguridad.

### 8. Proceso detallado que se muestra en pantalla

Esta función no hace la matemática, pero ordena el resultado para que se vea el cálculo completo en pantalla. El TXT generado no guarda este proceso ni el texto original: solo guarda el mensaje cifrado y la clave necesaria para descifrarlo.

```python
def construir_proceso_detallado(texto: str, detalle: DetalleGeneracionRSA, bloques: list[int]) -> str:
    # Creamos líneas explicativas para mostrar el proceso RSA completo.
    lineas = [
        "PROCESO DETALLADO RSA",
        f"Texto original: {texto}",
        f"p = {detalle.p}",
        f"q = {detalle.q}",
        f"n = p * q = {detalle.p} * {detalle.q} = {detalle.n}",
        f"phi(n) = (p - 1)(q - 1) = ({detalle.p} - 1)({detalle.q} - 1) = {detalle.phi}",
        "Posibles valores de d con MCD(d, phi(n)) = 1:",
        formatear_lista_enteros(detalle.posibles_d),
        f"d seleccionado = {detalle.d}",
        f"e debe cumplir e*d ≡ 1 mod phi(n), es decir e*{detalle.d} ≡ 1 mod {detalle.phi}",
        f"e base calculado = {detalle.e_base}",
        f"Posibles ejemplos de e = {', '.join(str(valor) for valor in detalle.posibles_e)}",
        f"e seleccionado = {detalle.e}",
        f"Clave pública = (n, e) = ({detalle.n}, {detalle.e})",
        f"Clave privada = (n, d) = ({detalle.n}, {detalle.d})",
        f"Mensaje encriptado en bloques = {bloques}",
    ]

    # Unimos todo en un texto listo para imprimir en pantalla.
    return "\n".join(lineas)
```

**Idea clave:** esto sirve para evidenciar el cálculo completo: no solo mostrar el resultado final, sino el camino matemático.

## Ejecutar interfaz web

La interfaz web agrega una API Flask sobre `rsa_backend.py` y un frontend Vite con estetica oscura tipo consola criptografica.

Instala dependencias del backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Levanta la API en una terminal:

```bash
python3 -m api.api
```

Levanta el frontend en otra terminal:

```bash
cd frontend
npm install
npm run dev
```

URLs por defecto:

- API: `http://localhost:5050/api`
- Web: `http://localhost:5173`

Endpoints principales de la API:

- `GET /api/health`
- `POST /api/keys/generate`
- `POST /api/keys/from-primes`
- `POST /api/encrypt`
- `POST /api/decrypt`
- `POST /api/credentials/encrypt`
- `POST /api/credentials/decrypt`
- `POST /api/verify`

Para generar una build de produccion del frontend:

```bash
cd frontend
npm run build
```

Despues de generar `frontend/dist`, Flask tambien puede servir la web desde `http://localhost:5050`.

## Ejecutar interfaz gráfica

Para usar la app con ventana, ejecutá:

```bash
python3 gui.py
```

Desde la ventana podés:

- usar el flujo empresa: empleado genera llaves, jefe cifra credenciales y empleado descifra
- mostrar la llave pública que se puede compartir con el jefe
- guardar credenciales cifradas en `credenciales_encriptadas.json`
- usar el flujo de texto paso a paso con `p` y `q` manuales
- rechazar automáticamente valores que no sean primos
- calcular `n`, `phi(n)`, posibles valores de `d` y ejemplos de `e`
- guardar el mensaje encriptado en `mensaje_encriptado.txt`
- desencriptar un archivo `.txt` generado por el programa

## Ejecutar interfaz de terminal

```bash
python3 main.py
```

La interfaz de terminal ahora muestra:

- encabezado ASCII con identidad visual RSA
- colores ANSI semánticos cuando la terminal los soporta
- flujo principal empleado/jefe para llaves, cifrado y descifrado de credenciales
- flujo opcional de texto paso a paso con ingreso manual de `p` y `q`
- validación de números primos en el modo paso a paso
- cálculo detallado de `n`, `phi(n)`, `d`, `e` y claves en el modo paso a paso
- advertencias rojas en recuadros ASCII con símbolo `[!]`
- guardado del mensaje cifrado en archivo `.txt`
- explicación rápida de RSA desde el menú
- limpieza automática de consola entre menú y acciones para mantener la lectura ordenada

Si necesitás salida sin colores, ejecutá:

```bash
NO_COLOR=1 python3 main.py
```

Si tu terminal soporta color pero Python no la detecta como interactiva, podés forzarlo así:

```bash
FORCE_COLOR=1 python3 main.py
```

Si necesitás conservar todo el historial de salida para copiarlo o revisarlo, podés desactivar la limpieza automática:

```bash
RSA_NO_CLEAR=1 python3 main.py
```

## Flujo principal: empleado y jefe

1. El empleado genera la llave pública y la llave privada.
2. El empleado comparte solo la llave pública con el jefe.
3. El jefe cifra dos credenciales usando la llave pública.
4. El jefe devuelve el archivo cifrado al empleado.
5. El empleado descifra las credenciales usando su llave privada.

## Flujo opcional: texto RSA paso a paso

1. El usuario ingresa el texto a encriptar.
2. El usuario ingresa `p` y `q` como primos diferentes de una o dos cifras.
3. El sistema rechaza `p` o `q` si no son primos válidos.
4. El sistema muestra `n`, `phi(n)`, posibles `d`, `d` seleccionado, posibles `e`, `e` seleccionado y claves.
5. El sistema guarda el mensaje cifrado en `mensaje_encriptado.txt`.
6. Otro usuario puede abrir ese `.txt` y desencriptarlo desde la opción correspondiente.

## Archivos generados

- `llave_publica.json`: contiene la llave pública que el empleado puede compartir con el jefe.
- `llave_privada_empleado.json`: contiene la llave privada que solo debe conservar el empleado.
- `credenciales_encriptadas.json`: contiene las credenciales cifradas por el jefe.
- `mensaje_encriptado.txt`: contiene solo el mensaje cifrado y la clave privada necesaria para desencriptar el ejercicio paso a paso; no guarda el texto original ni el proceso detallado.

## Menú de terminal

- `1`: empleado genera llaves pública y privada
- `2`: empleado muestra llave pública para el jefe
- `3`: jefe cifra dos credenciales con la llave pública
- `4`: empleado descifra credenciales con la llave privada
- `5`: encriptar texto con `p` y `q` manuales
- `6`: desencriptar mensaje desde archivo TXT
- `7`: ver explicación RSA paso a paso
- `0`: salir

## Librerías usadas

El proyecto no usa librerías externas instaladas con `pip`. Todo está hecho con módulos de la biblioteca estándar de Python y con el archivo local `rsa_backend.py`.

| Librería o módulo | Archivo donde se usa | Para qué se usa |
| --- | --- | --- |
| `json` | `rsa_backend.py`, `main.py`, `gui.py` | Convertir llaves, mensajes y credenciales a formato JSON para guardarlos y leerlos desde archivos. |
| `secrets` | `rsa_backend.py` | Generar números aleatorios más adecuados para criptografía, como primos candidatos y valores de `d`. |
| `dataclasses.dataclass` | `rsa_backend.py` | Crear estructuras simples e inmutables para las llaves y el detalle RSA. |
| `pathlib.Path` | `rsa_backend.py`, `main.py`, `gui.py` | Manejar rutas de archivos de forma clara y compatible entre sistemas operativos. |
| `typing.Any` | `rsa_backend.py`, `main.py`, `gui.py` | Anotar datos que vienen de JSON y pueden mezclar textos, números, listas y diccionarios. |
| `getpass` | `main.py` | Pedir contraseñas o datos sensibles en terminal sin mostrar lo escrito. |
| `os` | `main.py` | Leer variables de entorno como `NO_COLOR`, `FORCE_COLOR` y `RSA_NO_CLEAR`. |
| `shutil` | `main.py` | Detectar el ancho de la terminal para ajustar textos y separadores. |
| `sys` | `main.py` | Saber si la salida es una terminal interactiva antes de usar colores o limpiar pantalla. |
| `textwrap` | `main.py`, `gui.py` | Partir textos largos para que se vean ordenados en consola o en recuadros de advertencia. |
| `tkinter` / `tkinter.ttk` | `gui.py` | Construir la interfaz gráfica con ventana, botones, entradas, pestañas y área de salida. |
| `tkinter.filedialog` | `gui.py` | Abrir una ventana para seleccionar archivos `.txt` al desencriptar. |
| `rsa_backend` | `main.py`, `gui.py` | Reutilizar la lógica RSA: generación de llaves, cifrado, descifrado, validaciones y lectura/escritura JSON. |

## Funciones usadas y para qué sirven

### `rsa_backend.py`

Este archivo contiene la matemática y la lógica reutilizable. Es la parte más importante del proyecto porque no depende ni de la terminal ni de la ventana gráfica.

| Función o clase | Para qué sirve |
| --- | --- |
| `LlavePublica` | Guarda la clave pública `(n, e)`, que se puede compartir para cifrar. |
| `LlavePrivada` | Guarda la clave privada `(n, d)`, que se usa para descifrar y no debe compartirse. |
| `ParDeLlaves` | Agrupa la llave pública, la llave privada y los valores matemáticos `p`, `q` y `phi`. |
| `DetalleGeneracionRSA` | Guarda todo el proceso paso a paso cuando el usuario ingresa `p`, `q`, `d` y `e`. |
| `calcular_mcd` | Calcula el máximo común divisor con Euclides; sirve para verificar si dos números son coprimos. |
| `algoritmo_extendido_euclides` | Calcula el MCD y los coeficientes de Bézout; se usa para hallar inversos modulares. |
| `calcular_inverso_modular` | Calcula el número que cumple `valor * inverso ≡ 1 mod modulo`; en RSA se usa para obtener `e`. |
| `es_probable_primo` | Verifica si un número probablemente es primo usando Miller-Rabin. |
| `generar_primo` | Genera un primo aleatorio de cierta cantidad de bits. |
| `elegir_exponente_privado` | Elige un `d` válido que sea coprimo con `phi(n)`. |
| `validar_primos_una_o_dos_cifras` | Revisa que `p` y `q` sean primos, distintos y de una o dos cifras. |
| `obtener_posibles_d` | Lista todos los valores de `d` válidos para un `phi(n)`. |
| `obtener_posibles_e` | Calcula el `e` base y ejemplos de otros `e` que cumplen la congruencia RSA. |
| `generar_llaves_desde_primos` | Construye las llaves usando `p`, `q`, `d` y opcionalmente `e`, mostrando el detalle matemático. |
| `generar_llaves` | Genera automáticamente un par de llaves RSA para el flujo empleado/jefe. |
| `llave_publica_a_diccionario` | Convierte una llave pública a diccionario para guardarla en JSON. |
| `llave_privada_a_diccionario` | Convierte una llave privada a diccionario para guardarla en JSON. |
| `llave_publica_desde_diccionario` | Reconstruye una llave pública desde datos leídos de JSON. |
| `llave_privada_desde_diccionario` | Reconstruye una llave privada desde datos leídos de JSON. |
| `par_de_llaves_a_diccionario` | Convierte el par completo de llaves a JSON, incluyendo detalle matemático. |
| `guardar_json` | Guarda datos en un archivo JSON legible. |
| `leer_json` | Lee un archivo JSON y valida que contenga un objeto principal. |
| `cifrar_numero` | Aplica `C = M^e mod n` sobre un bloque numérico. |
| `descifrar_numero` | Aplica `M = C^d mod n` sobre un bloque cifrado. |
| `cifrar_texto` | Convierte texto a bytes UTF-8 y cifra cada byte como bloque RSA. |
| `descifrar_texto` | Descifra bloques numéricos y reconstruye el texto original. |
| `cifrar_dos_datos` | Cifra dos credenciales usando la llave pública. |
| `descifrar_dos_datos` | Descifra dos credenciales usando la llave privada. |
| `verificar_par_de_llaves` | Prueba que una llave pública y una privada funcionen juntas cifrando y descifrando `"prueba"`. |

### `main.py`

Este archivo contiene la interfaz de terminal. Usa las funciones de `rsa_backend.py` y agrega menús, colores, validaciones de entrada y guardado de archivos.

| Función | Para qué sirve |
| --- | --- |
| `obtener_ancho_terminal` | Calcula un ancho cómodo para imprimir textos en consola. |
| `terminal_admite_colores` | Decide si se deben usar colores ANSI. |
| `limpiar_pantalla` | Limpia la consola entre pantallas cuando corresponde. |
| `colorear` | Aplica colores ANSI a textos de la terminal. |
| `imprimir_linea`, `imprimir_texto`, `imprimir_bloque` | Dan formato visual a separadores, párrafos y bloques informativos. |
| `imprimir_recuadro_advertencia`, `imprimir_estado` | Muestran advertencias, errores y estados importantes. |
| `formatear_ruta`, `existe_archivo` | Simplifican la presentación y validación de rutas. |
| `mostrar_logo_ascii`, `mostrar_titulo` | Muestran el encabezado visual de la app en terminal. |
| `pausar`, `pedir_entero`, `confirmar` | Controlan entradas del usuario y confirmaciones. |
| `cargar_llave_publica_guardada`, `cargar_llave_privada_guardada` | Leen llaves existentes desde archivos JSON. |
| `pedir_llave_publica_manual`, `pedir_llave_privada_manual` | Permiten ingresar llaves manualmente si no hay archivos. |
| `obtener_llave_publica_para_cifrar`, `obtener_llave_privada_para_descifrar` | Deciden si usar una llave guardada o pedirla manualmente. |
| `confirmar_reemplazo_de_llaves` | Evita sobrescribir llaves sin confirmación. |
| `generar_y_guardar_llaves` | Ejecuta el flujo del empleado para crear y guardar llaves. |
| `mostrar_llave_publica` | Muestra la llave pública que se comparte con el jefe. |
| `pedir_credencial_visible`, `pedir_credencial_oculta` | Piden los datos que el jefe va a cifrar. |
| `resumir_bloques`, `formatear_lista_enteros` | Acortan listas largas para que sean legibles. |
| `pedir_texto_a_encriptar`, `pedir_primo` | Piden el texto y los primos del modo paso a paso. |
| `texto_cabe_en_modulo`, `explicar_error_modulo` | Validan que cada byte del texto sea menor que `n`. |
| `pedir_p_q_validos_para_texto` | Repite la solicitud de `p` y `q` hasta que sean válidos para el texto. |
| `seleccionar_d`, `seleccionar_e` | Permiten elegir los exponentes RSA del modo paso a paso. |
| `construir_proceso_detallado` | Arma el texto explicativo del cálculo RSA completo. |
| `guardar_mensaje_en_txt`, `leer_mensaje_desde_txt` | Guardan y leen el TXT con mensaje cifrado y clave privada de descifrado, sin texto original ni proceso. |
| `encriptar_texto_paso_a_paso` | Ejecuta todo el flujo manual de cifrado con `p`, `q`, `d` y `e`. |
| `desencriptar_archivo_txt` | Lee un TXT generado por el programa y recupera el texto original. |
| `cifrar_credenciales`, `descifrar_credenciales` | Ejecutan el flujo jefe/empleado para cifrar y descifrar credenciales. |
| `cargar_paquete_cifrado` | Lee el archivo con las credenciales cifradas. |
| `ejecutar_demo_completo` | Corre una demostración automática del flujo completo. |
| `mostrar_explicacion_rsa` | Muestra una explicación breve de RSA desde el menú. |
| `mostrar_menu`, `ejecutar_opcion`, `ejecutar_menu` | Controlan el menú principal de la aplicación de terminal. |

### `gui.py`

Este archivo contiene la interfaz gráfica con Tkinter. Usa el mismo backend RSA, pero organiza el uso en botones, pestañas y cuadros de texto.

| Función, clase o método | Para qué sirve |
| --- | --- |
| `formatear_lista_enteros` | Muestra listas largas de candidatos `d` sin saturar la pantalla. |
| `resumir_bloques` | Resume bloques cifrados para mostrar solo una parte y el total. |
| `texto_cabe_en_modulo` | Verifica que el texto pueda cifrarse con el valor actual de `n`. |
| `construir_recuadro_advertencia` | Crea advertencias en formato de recuadro ASCII dentro de la GUI. |
| `construir_proceso` | Arma el detalle del proceso RSA para mostrarlo en pantalla. |
| `AplicacionRSA` | Clase principal de la ventana gráfica. |
| `crear_estilos` | Define colores, fuentes y estilos visuales de la GUI. |
| `crear_widgets` | Construye la estructura principal: paneles, pestañas, botones y salida. |
| `crear_pestaña_empresa` | Crea los controles del flujo empleado/jefe. |
| `crear_pestaña_manual` | Crea los controles del flujo de texto paso a paso. |
| `escribir`, `limpiar_salida`, `advertir` | Manejan el área de resultados de la ventana. |
| `cargar_llave_publica_empresa`, `cargar_llave_privada_empresa` | Cargan llaves desde archivos para la GUI. |
| `generar_llaves_empresa` | Genera y guarda llaves desde la ventana. |
| `mostrar_publica_empresa` | Muestra la llave pública para compartir. |
| `cifrar_empresa` | Cifra dos credenciales desde la pestaña del jefe. |
| `descifrar_empresa` | Descifra credenciales desde la pestaña del empleado. |
| `leer_primos`, `leer_texto` | Leen y validan los datos escritos en la GUI. |
| `calcular_candidatos` | Calcula `n`, `phi(n)` y posibles valores de `d`. |
| `encriptar_guardar` | Cifra el texto manual, muestra el proceso y guarda el TXT. |
| `desencriptar_txt` | Abre un TXT, lee los bloques cifrados y recupera el texto. |

## Advertencia seria

Esto es una implementación académica para aprender aritmética modular y RSA. Para credenciales reales de una empresa, no uses RSA casero ni RSA sin padding. En producción se usa una librería auditada como `cryptography` con RSA-OAEP, o directamente un protocolo probado como TLS/HTTPS.
