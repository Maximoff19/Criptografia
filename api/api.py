from __future__ import annotations

import os
import json
import sys
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_from_directory

try:
    from flask_cors import CORS
except ImportError:  # pragma: no cover - optional dependency fallback
    CORS = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"
ARCHIVO_PUBLICO = PROJECT_ROOT / "llave_publica.json"
ARCHIVO_PRIVADO = PROJECT_ROOT / "llave_privada_empleado.json"
ARCHIVO_CIFRADO = PROJECT_ROOT / "credenciales_encriptadas.json"
ARCHIVO_MENSAJE_TXT = PROJECT_ROOT / "mensaje_encriptado.txt"
BITS_DEMO = 16

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rsa_backend import (  # noqa: E402
    LlavePrivada,
    LlavePublica,
    cifrar_dos_datos,
    cifrar_texto,
    descifrar_dos_datos,
    descifrar_texto,
    generar_llaves,
    generar_llaves_desde_primos,
    guardar_json,
    leer_json,
    llave_privada_desde_diccionario,
    llave_publica_a_diccionario,
    llave_publica_desde_diccionario,
    obtener_posibles_e,
    obtener_posibles_d,
    par_de_llaves_a_diccionario,
    validar_primos_una_o_dos_cifras,
    verificar_par_de_llaves,
)


app = Flask(__name__, static_folder=None)

if CORS is not None:
    CORS(app)


@app.after_request
def add_cors_headers(response):
    response.headers.setdefault("Access-Control-Allow-Origin", "*")
    response.headers.setdefault("Access-Control-Allow-Headers", "Content-Type")
    response.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response


def json_payload() -> dict[str, Any]:
    data = request.get_json(silent=True)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError("El cuerpo JSON debe ser un objeto.")
    return data


def int_from(data: dict[str, Any], key: str, default: int | None = None) -> int:
    value = data.get(key, default)
    if value is None:
        raise ValueError(f"Falta el campo '{key}'.")
    try:
        return int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"El campo '{key}' debe ser un numero entero.") from error


def str_from(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or value.strip() == "":
        raise ValueError(f"El campo '{key}' debe ser texto no vacio.")
    return value


def public_key_from(data: dict[str, Any], key: str = "public_key") -> LlavePublica:
    raw = data.get(key)
    if not isinstance(raw, dict):
        raise ValueError(f"Falta el objeto '{key}'.")
    return LlavePublica(n=int_from(raw, "n"), e=int_from(raw, "e"))


def private_key_from(data: dict[str, Any], key: str = "private_key") -> LlavePrivada:
    raw = data.get(key)
    if not isinstance(raw, dict):
        raise ValueError(f"Falta el objeto '{key}'.")
    return LlavePrivada(n=int_from(raw, "n"), d=int_from(raw, "d"))


def blocks_from(data: dict[str, Any], key: str) -> list[int]:
    raw = data.get(key)
    if not isinstance(raw, list):
        raise ValueError(f"El campo '{key}' debe ser una lista de enteros.")
    try:
        return [int(value) for value in raw]
    except (TypeError, ValueError) as error:
        raise ValueError(f"El campo '{key}' solo acepta enteros.") from error


def formatear_ruta(ruta: Path) -> str:
    return ruta.name


def existe_archivo(ruta: Path) -> bool:
    return ruta.exists() and ruta.is_file()


def resumir_bloques(bloques: list[int], limite: int = 8) -> str:
    if len(bloques) <= limite:
        return str(bloques)
    visibles = ", ".join(str(numero) for numero in bloques[:limite])
    return f"[{visibles}, ...] total={len(bloques)} bloques"


def formatear_lista_enteros(valores: list[int], por_linea: int = 12, limite: int = 120) -> str:
    visibles = valores[:limite]
    lineas: list[str] = []
    for indice in range(0, len(visibles), por_linea):
        grupo = visibles[indice : indice + por_linea]
        lineas.append(", ".join(str(valor) for valor in grupo))
    if len(valores) > limite:
        lineas.append(f"... se calcularon {len(valores)} valores en total")
    return "\n".join(lineas)


def texto_cabe_en_modulo(texto: str, n: int) -> bool:
    bytes_texto = texto.encode("utf-8")
    if not bytes_texto:
        return True
    return max(bytes_texto) < n


def explicar_error_modulo(texto: str, n: int) -> str:
    maximo = max(texto.encode("utf-8"))
    return f"Con esos primos n={n}, pero el texto contiene un bloque M={maximo}. En RSA debe cumplirse M < n; elegí primos más grandes."


def construir_proceso_detallado(texto: str, detalle, bloques: list[int]) -> str:
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
    return "\n".join(lineas)


def cargar_llave_publica_guardada() -> LlavePublica | None:
    if not existe_archivo(ARCHIVO_PUBLICO):
        return None
    return llave_publica_desde_diccionario(leer_json(ARCHIVO_PUBLICO))


def cargar_llave_privada_guardada() -> LlavePrivada | None:
    if not existe_archivo(ARCHIVO_PRIVADO):
        return None
    datos = leer_json(ARCHIVO_PRIVADO)
    return llave_privada_desde_diccionario(datos["privada"])


def cargar_paquete_cifrado() -> dict[str, Any] | None:
    if not existe_archivo(ARCHIVO_CIFRADO):
        return None
    return leer_json(ARCHIVO_CIFRADO)


def guardar_mensaje_en_txt(detalle, bloques: list[int]) -> dict[str, Any]:
    paquete = {
        "mensaje_encriptado": bloques,
        "clave_privada_para_descifrar": {"n": detalle.n, "d": detalle.d},
    }
    ARCHIVO_MENSAJE_TXT.write_text(json.dumps(paquete, ensure_ascii=False, indent=2), encoding="utf-8")
    return paquete


def leer_mensaje_desde_txt_default() -> dict[str, Any]:
    texto = ARCHIVO_MENSAJE_TXT.read_text(encoding="utf-8")
    datos = json.loads(texto)
    if not isinstance(datos, dict):
        raise ValueError("El archivo TXT no contiene un paquete RSA válido.")
    return datos


def terminal_bloque(titulo: str, lineas: list[str]) -> dict[str, Any]:
    return {"title": titulo, "lines": lineas}


def handle_error(error: Exception, status: int = 400):
    return jsonify({"success": False, "error": str(error)}), status


def persist_key_pair(par) -> None:
    guardar_json(ARCHIVO_PRIVADO, par_de_llaves_a_diccionario(par))
    guardar_json(ARCHIVO_PUBLICO, llave_publica_a_diccionario(par.publica))


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "online",
            "version": "1.0.0",
            "algorithm": "RSA educativo sin padding",
            "endpoints": [
                "/api/keys/generate",
                "/api/keys/from-primes",
                "/api/encrypt",
                "/api/decrypt",
                "/api/credentials/encrypt",
                "/api/credentials/decrypt",
                "/api/verify",
                "/api/health",
            ],
        }
    )


@app.route("/api/terminal/generate-keys", methods=["POST", "OPTIONS"])
def terminal_generate_keys():
    if request.method == "OPTIONS":
        return jsonify({})
    try:
        data = json_payload()
        bits = int_from(data, "bits", BITS_DEMO)
        if bits < 8:
            raise ValueError("El valor mínimo permitido es 8.")
        par = generar_llaves(bits)
        if not verificar_par_de_llaves(par):
            raise RuntimeError("El par de llaves generado no pasó la verificación interna.")
        persist_key_pair(par)
        return jsonify(
            {
                "success": True,
                "public_key": {"n": par.publica.n, "e": par.publica.e},
                "private_key": {"n": par.privada.n, "d": par.privada.d},
                "mathematical_detail": {"p": par.p, "q": par.q, "phi": par.phi},
                "terminal": [
                    terminal_bloque(
                        "Paso 1 - Empleado genera llaves",
                        [
                            "La llave pública se comparte con el jefe para cifrar credenciales.",
                            "La llave privada se queda con el empleado para descifrar lo recibido.",
                        ],
                    ),
                    terminal_bloque(
                        "Llaves generadas correctamente",
                        [
                            f"Compartir con el jefe: {formatear_ruta(ARCHIVO_PUBLICO)}",
                            f"Guardar sin compartir: {formatear_ruta(ARCHIVO_PRIVADO)}",
                            f"Llave pública (n, e): ({par.publica.n}, {par.publica.e})",
                            f"Llave privada (n, d): ({par.privada.n}, {par.privada.d})",
                            f"Detalle matemático: p={par.p}, q={par.q}, phi(n)={par.phi}",
                        ],
                    ),
                ],
            }
        )
    except Exception as error:
        return handle_error(error)


@app.route("/api/terminal/show-public-key", methods=["GET"])
def terminal_show_public_key():
    try:
        llave = cargar_llave_publica_guardada()
        if llave is None:
            raise FileNotFoundError("No existe llave_publica.json; primero generá las llaves con la opción 1.")
        return jsonify(
            {
                "success": True,
                "public_key": {"n": llave.n, "e": llave.e},
                "terminal": [
                    terminal_bloque("Paso 2 - Compartir llave pública", ["Este es el único material que debería recibir el jefe."]),
                    terminal_bloque(
                        "Datos para compartir:",
                        [f"n = {llave.n}", f"e = {llave.e}", f"archivo = {formatear_ruta(ARCHIVO_PUBLICO)}"],
                    ),
                    terminal_bloque("[!] ADVERTENCIA", ["No compartas llave_privada_empleado.json. Si lo hacés, la seguridad se cae."]),
                ],
            }
        )
    except Exception as error:
        return handle_error(error)


@app.route("/api/terminal/encrypt-credentials", methods=["POST", "OPTIONS"])
def terminal_encrypt_credentials():
    if request.method == "OPTIONS":
        return jsonify({})
    try:
        data = json_payload()
        llave = public_key_from(data) if isinstance(data.get("public_key"), dict) else cargar_llave_publica_guardada()
        if llave is None:
            raise FileNotFoundError("No existe llave_publica.json; primero generá las llaves con la opción 1.")
        dato_uno = str_from(data, "data_one")
        dato_dos = str_from(data, "data_two")
        paquete = cifrar_dos_datos(dato_uno, dato_dos, llave)
        guardar_json(ARCHIVO_CIFRADO, paquete)
        bloques_uno = list(paquete["dato_uno_cifrado"])
        bloques_dos = list(paquete["dato_dos_cifrado"])
        return jsonify(
            {
                "success": True,
                "package": paquete,
                "data_one_encrypted": bloques_uno,
                "data_two_encrypted": bloques_dos,
                "terminal": [
                    terminal_bloque(
                        "Paso 3 - Jefe cifra credenciales",
                        [
                            "Usá la llave pública del empleado. La contraseña se escribe oculta para evitar exposición visual.",
                            "El resultado se guarda en credenciales_encriptadas.json para devolverlo al empleado.",
                        ],
                    ),
                    terminal_bloque(
                        "Credenciales cifradas correctamente",
                        [
                            f"Archivo para devolver al empleado: {formatear_ruta(ARCHIVO_CIFRADO)}",
                            f"Dato 1 cifrado: {resumir_bloques(bloques_uno)}",
                            f"Dato 2 cifrado: {resumir_bloques(bloques_dos)}",
                        ],
                    ),
                ],
            }
        )
    except Exception as error:
        return handle_error(error)


@app.route("/api/terminal/decrypt-credentials", methods=["POST", "OPTIONS"])
def terminal_decrypt_credentials():
    if request.method == "OPTIONS":
        return jsonify({})
    try:
        data = json_payload()
        paquete = cargar_paquete_cifrado()
        if isinstance(data.get("data_one_encrypted"), list) and isinstance(data.get("data_two_encrypted"), list):
            paquete = {
                "dato_uno_cifrado": blocks_from(data, "data_one_encrypted"),
                "dato_dos_cifrado": blocks_from(data, "data_two_encrypted"),
            }
        if paquete is None:
            raise FileNotFoundError("No existe credenciales_encriptadas.json; primero cifrá dos datos con la opción 3.")
        llave = private_key_from(data) if isinstance(data.get("private_key"), dict) else cargar_llave_privada_guardada()
        if llave is None:
            raise FileNotFoundError("No existe llave_privada_empleado.json; primero generá las llaves con la opción 1.")
        dato_uno, dato_dos = descifrar_dos_datos(paquete, llave)
        return jsonify(
            {
                "success": True,
                "data_one": dato_uno,
                "data_two": dato_dos,
                "terminal": [
                    terminal_bloque("Paso 4 - Empleado descifra credenciales", ["Solo la llave privada del empleado puede recuperar los datos originales."]),
                    terminal_bloque("Credenciales descifradas", [f"Dato 1 original: {dato_uno}", f"Dato 2 original: {dato_dos}"]),
                ],
            }
        )
    except Exception as error:
        return handle_error(error)


@app.route("/api/terminal/text-candidates", methods=["POST", "OPTIONS"])
def terminal_text_candidates():
    if request.method == "OPTIONS":
        return jsonify({})
    try:
        data = json_payload()
        texto = str_from(data, "text")
        p = int_from(data, "p")
        q = int_from(data, "q")
        validar_primos_una_o_dos_cifras(p, q)
        n = p * q
        if not texto_cabe_en_modulo(texto, n):
            raise ValueError(explicar_error_modulo(texto, n))
        phi = (p - 1) * (q - 1)
        posibles_d = obtener_posibles_d(phi)
        return jsonify(
            {
                "success": True,
                "n": n,
                "phi": phi,
                "possible_d": posibles_d,
                "possible_d_text": formatear_lista_enteros(posibles_d),
                "terminal": [
                    terminal_bloque("Cálculo inicial", [f"n = p*q = {p}*{q} = {n}", f"phi(n) = (p-1)(q-1) = ({p}-1)({q}-1) = {phi}"]),
                    terminal_bloque("Posibles valores de d:", [formatear_lista_enteros(posibles_d)]),
                ],
            }
        )
    except Exception as error:
        return handle_error(error)


@app.route("/api/terminal/encrypt-text-step", methods=["POST", "OPTIONS"])
def terminal_encrypt_text_step():
    if request.method == "OPTIONS":
        return jsonify({})
    try:
        data = json_payload()
        texto = str_from(data, "text")
        p = int_from(data, "p")
        q = int_from(data, "q")
        d = int_from(data, "d")
        phi = (p - 1) * (q - 1)
        e_base, posibles_e = obtener_posibles_e(d, phi)
        raw_e = data.get("e")
        e = e_base if raw_e in (None, "") else int(raw_e)
        validar_primos_una_o_dos_cifras(p, q)
        n = p * q
        if not texto_cabe_en_modulo(texto, n):
            raise ValueError(explicar_error_modulo(texto, n))
        detalle = generar_llaves_desde_primos(p, q, d, e)
        bloques = cifrar_texto(texto, detalle.publica)
        proceso = construir_proceso_detallado(texto, detalle, bloques)
        paquete_txt = guardar_mensaje_en_txt(detalle, bloques)
        return jsonify(
            {
                "success": True,
                "process": proceso,
                "encrypted_blocks": bloques,
                "txt_package": paquete_txt,
                "possible_e": posibles_e,
                "terminal": [
                    terminal_bloque("Encriptar texto con RSA", ["Ingresá texto, dos primos p y q, y seleccioná d/e viendo el proceso completo."]),
                    terminal_bloque("Posibles valores de e", [f"Solución general: e = {detalle.e_base} + {detalle.phi}k, con k entero no negativo", f"Ejemplos: {', '.join(str(valor) for valor in detalle.posibles_e)}"]),
                    terminal_bloque("Proceso", proceso.splitlines()),
                    terminal_bloque(
                        "[!] ADVERTENCIA",
                        ["El TXT incluye la clave privada para que otro usuario pueda descifrar este ejercicio. En seguridad real, una clave privada no se comparte."],
                    ),
                    terminal_bloque("[EXITO]", [f"Mensaje encriptado guardado en {ARCHIVO_MENSAJE_TXT.name}."]),
                ],
            }
        )
    except Exception as error:
        return handle_error(error)


@app.route("/api/terminal/decrypt-txt", methods=["POST", "OPTIONS"])
def terminal_decrypt_txt():
    if request.method == "OPTIONS":
        return jsonify({})
    try:
        data = json_payload()
        paquete = data.get("package") if isinstance(data.get("package"), dict) else None
        if paquete is None:
            if not existe_archivo(ARCHIVO_MENSAJE_TXT):
                raise FileNotFoundError("No existe mensaje_encriptado.txt; primero encriptá texto con p y q manuales.")
            paquete = leer_mensaje_desde_txt_default()
        bloques = [int(valor) for valor in paquete["mensaje_encriptado"]]
        clave = paquete["clave_privada_para_descifrar"]
        privada = LlavePrivada(n=int(clave["n"]), d=int(clave["d"]))
        texto = descifrar_texto(bloques, privada)
        return jsonify(
            {
                "success": True,
                "decrypted_text": texto,
                "terminal": [
                    terminal_bloque("Desencriptar archivo TXT", ["El archivo debe contener mensaje_encriptado y clave_privada_para_descifrar."]),
                    terminal_bloque("Texto desencriptado", [texto]),
                ],
            }
        )
    except Exception as error:
        return handle_error(error)


@app.route("/api/keys/generate", methods=["POST", "OPTIONS"])
def keys_generate():
    if request.method == "OPTIONS":
        return jsonify({})
    try:
        data = json_payload()
        bits = int_from(data, "bits", 16)
        if bits < 8:
            raise ValueError("bits debe ser mayor o igual a 8.")
        par = generar_llaves(bits)
        if bool(data.get("persist", False)):
            persist_key_pair(par)
        return jsonify(
            {
                "success": True,
                "public_key": {"n": par.publica.n, "e": par.publica.e},
                "private_key": {"n": par.privada.n, "d": par.privada.d},
                "mathematical_detail": {"p": par.p, "q": par.q, "phi": par.phi},
                "verified": verificar_par_de_llaves(par),
            }
        )
    except Exception as error:
        return handle_error(error)


@app.route("/api/keys/from-primes", methods=["POST", "OPTIONS"])
def keys_from_primes():
    if request.method == "OPTIONS":
        return jsonify({})
    try:
        data = json_payload()
        p = int_from(data, "p")
        q = int_from(data, "q")
        raw_d = data.get("d")

        if raw_d in (None, ""):
            validar_primos_una_o_dos_cifras(p, q)
            n = p * q
            phi = (p - 1) * (q - 1)
            return jsonify(
                {
                    "success": True,
                    "mode": "candidates",
                    "n": n,
                    "phi": phi,
                    "possible_d": obtener_posibles_d(phi),
                }
            )

        d = int(raw_d)
        raw_e = data.get("e")
        e = None if raw_e in (None, "") else int(raw_e)
        detail = generar_llaves_desde_primos(p, q, d, e)
        return jsonify(
            {
                "success": True,
                "mode": "keys",
                "n": detail.n,
                "phi": detail.phi,
                "possible_d": detail.posibles_d,
                "d": detail.d,
                "e_base": detail.e_base,
                "possible_e": detail.posibles_e,
                "e": detail.e,
                "public_key": {"n": detail.publica.n, "e": detail.publica.e},
                "private_key": {"n": detail.privada.n, "d": detail.privada.d},
                "mathematical_detail": {"p": detail.p, "q": detail.q, "phi": detail.phi},
            }
        )
    except Exception as error:
        return handle_error(error)


@app.route("/api/encrypt", methods=["POST", "OPTIONS"])
def encrypt():
    if request.method == "OPTIONS":
        return jsonify({})
    try:
        data = json_payload()
        text = str_from(data, "text")
        public_key = public_key_from(data)
        encrypted = cifrar_texto(text, public_key)
        return jsonify(
            {
                "success": True,
                "algorithm": "RSA educativo sin padding",
                "warning": "No usar en produccion; usar RSA-OAEP en sistemas reales.",
                "public_key_used": {"n": public_key.n, "e": public_key.e},
                "encrypted_blocks": encrypted,
                "block_count": len(encrypted),
                "original_length": len(text),
            }
        )
    except Exception as error:
        return handle_error(error)


@app.route("/api/decrypt", methods=["POST", "OPTIONS"])
def decrypt():
    if request.method == "OPTIONS":
        return jsonify({})
    try:
        data = json_payload()
        blocks = blocks_from(data, "encrypted_blocks")
        private_key = private_key_from(data)
        return jsonify({"success": True, "decrypted_text": descifrar_texto(blocks, private_key)})
    except Exception as error:
        return handle_error(error)


@app.route("/api/credentials/encrypt", methods=["POST", "OPTIONS"])
def credentials_encrypt():
    if request.method == "OPTIONS":
        return jsonify({})
    try:
        data = json_payload()
        data_one = str_from(data, "data_one")
        data_two = str_from(data, "data_two")
        public_key = public_key_from(data)
        package = cifrar_dos_datos(data_one, data_two, public_key)
        return jsonify(
            {
                "success": True,
                "algorithm": package["algoritmo"],
                "warning": package["advertencia"],
                "public_key_used": package["llave_publica_usada"],
                "data_one_encrypted": package["dato_uno_cifrado"],
                "data_two_encrypted": package["dato_dos_cifrado"],
                "status": "encrypted",
            }
        )
    except Exception as error:
        return handle_error(error)


@app.route("/api/credentials/decrypt", methods=["POST", "OPTIONS"])
def credentials_decrypt():
    if request.method == "OPTIONS":
        return jsonify({})
    try:
        data = json_payload()
        private_key = private_key_from(data)
        package = {
            "dato_uno_cifrado": blocks_from(data, "data_one_encrypted"),
            "dato_dos_cifrado": blocks_from(data, "data_two_encrypted"),
        }
        data_one, data_two = descifrar_dos_datos(package, private_key)
        return jsonify({"success": True, "data_one": data_one, "data_two": data_two})
    except Exception as error:
        return handle_error(error)


@app.route("/api/verify", methods=["POST", "OPTIONS"])
def verify():
    if request.method == "OPTIONS":
        return jsonify({})
    try:
        data = json_payload()
        public_key = public_key_from(data)
        private_key = private_key_from(data)
        test_message = str(data.get("test_message", "prueba"))
        encrypted = cifrar_texto(test_message, public_key)
        decrypted = descifrar_texto(encrypted, private_key)
        return jsonify(
            {
                "success": True,
                "verified": decrypted == test_message,
                "test_message": test_message,
                "encrypted_test": encrypted,
                "decrypted_test": decrypted,
            }
        )
    except Exception as error:
        return handle_error(error)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path: str):
    if path.startswith("api/"):
        return jsonify({"success": False, "error": "Endpoint no encontrado."}), 404
    if not FRONTEND_DIST.exists():
        return jsonify({"message": "Frontend build no encontrado. Ejecuta npm run build en frontend/."}), 404
    candidate = FRONTEND_DIST / path
    if path and candidate.exists() and candidate.is_file():
        return send_from_directory(FRONTEND_DIST, path)
    return send_from_directory(FRONTEND_DIST, "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5050"))
    app.run(host="0.0.0.0", port=port, debug=True)
