# Backend educativo RSA en Python

Este proyecto implementa la lógica RSA del PDF **Aritmética modular y Criptografía RSA.pdf**:

- elegir primos distintos `p` y `q`
- calcular `n = p * q`
- calcular `phi(n) = (p - 1)(q - 1)`
- elegir `d` con `MCD(d, phi(n)) = 1`
- calcular `e` con `e * d ≡ 1 mod phi(n)`
- cifrar con `C = M^e mod n`
- descifrar con `M = C^d mod n`

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
- `mensaje_encriptado.txt`: contiene el mensaje cifrado, el proceso y la clave privada necesaria para desencriptar el ejercicio paso a paso.

## Menú de terminal

- `1`: empleado genera llaves pública y privada
- `2`: empleado muestra llave pública para el jefe
- `3`: jefe cifra dos credenciales con la llave pública
- `4`: empleado descifra credenciales con la llave privada
- `5`: encriptar texto con `p` y `q` manuales
- `6`: desencriptar mensaje desde archivo TXT
- `7`: ver explicación RSA paso a paso
- `0`: salir

## Advertencia seria

Esto es una implementación académica para aprender aritmética modular y RSA. Para credenciales reales de una empresa, no uses RSA casero ni RSA sin padding. En producción se usa una librería auditada como `cryptography` con RSA-OAEP, o directamente un protocolo probado como TLS/HTTPS.
