# Criptografía RSA — Herramienta educativa y empresarial

**Una contribución a la comunidad matemática** y una herramienta diseñada para que las empresas gestionen credenciales de forma totalmente segura usando criptografía RSA pura, sin dependencias externas, implementada desde los principios fundamentales.

---

## ¿Qué es esto?

Este proyecto implementa el algoritmo RSA completo desde cero: generación de primos, cálculo de `n` y `φ(n)`, selección de exponentes `d` y `e`, cifrado y descifrado. No es un wrapper de OpenSSL ni una librería externa — es RSA hecho a mano, con cada paso matemático visible y verificable.

Pensalo como un **laboratorio de criptografía asimétrica** que funciona en tres interfaces:

| Interfaz | Propósito |
|----------|-----------|
| **Web UI** | Interfaz visual moderna, oscura, tipo consola criptográfica |
| **Terminal** | Interfaz de texto completa con colores ANSI y menú interactivo |
| **GUI Tkinter** | Ventana gráfica tradicional con pestañas y botones |

Todas las interfaces usan el mismo backend matemático (`rsa_backend.py`). Lo que hacés en una, funciona igual en las otras.

---

## ¿Para qué sirve en una empresa?

El flujo principal refleja un caso real de gestión de credenciales:

```
1. El empleado genera su par de llaves (pública y privada)
2. El empleado comparte SOLO la llave pública con su jefe
3. El jefe cifra credenciales (usuario/contraseña) con esa llave pública
4. El jefe devuelve el archivo cifrado al empleado
5. SOLO el empleado puede descifrar, usando su llave privada
```

**Esto es seguridad en dos direcciones:**

- ✅ Si alguien intercepta la llave pública, **no puede descifrar** — solo cifrar.
- ✅ Si alguien roba el archivo cifrado, **no puede leerlo** sin la llave privada.
- ✅ La llave privada **nunca viaja** — la genera y la conserva el empleado.
- ✅ No hay servidor central, no hay contraseñas compartidas, no hay punto único de ataque.

---

## Interfaces disponibles

### 🖥️ Web UI (recomendada)

La interfaz web provee el mismo flujo que la terminal pero con diseño visual Vault Dark, ideal para demostraciones, presentaciones y uso diario.

```
┌─────────────────────────────────────────────────────┐
│  1  Generar llaves pública y privada                │
│  2  Mostrar llave pública para el jefe              │
│  3  Cifrar credenciales con llave pública           │
│  4  Descifrar credenciales con llave privada        │
│  5  Encriptar texto con p y q manuales              │
│  6  Desencriptar mensaje desde archivo TXT          │
│  7  Explicación RSA paso a paso                     │
└─────────────────────────────────────────────────────┘
```

**Para levantar la Web UI:**

```bash
# Terminal 1: Backend API (Flask)
python3 -m venv .venv
source .venv/bin/activate      # Linux/Mac
# source .venv/bin/activate.fish  # si usás fish shell
pip install -r requirements.txt
python3 -m api.api
# → API en http://localhost:5050

# Terminal 2: Frontend (Vite)
cd frontend
npm install
npm run dev
# → Web en http://localhost:5173
```

O también podés hacer build del frontend y servirlo desde Flask:

```bash
cd frontend
npm run build
# Después de eso, http://localhost:5050/ ya sirve la web completa
```

### 🧪 Terminal

```bash
python3 main.py
```

Menú numérico con las mismas 7 opciones, colores ANSI, recuadros de advertencia y output formateado. Variables de entorno útiles:

| Variable | Efecto |
|----------|--------|
| `NO_COLOR=1` | Desactiva colores ANSI |
| `FORCE_COLOR=1` | Fuerza colores aunque no se detecte terminal interactiva |
| `RSA_NO_CLEAR=1` | No limpia la pantalla entre pantallas (útil para capturar logs) |

### 🪟 GUI Tkinter

```bash
python3 gui.py
```

Ventana gráfica con pestañas para flujo empresa y flujo manual paso a paso.

---

## Flujo manual: texto RSA paso a paso

Además del flujo empresa, el proyecto incluye un modo educativo donde **cada cálculo matemático es visible**:

1. Ingresás el texto a encriptar
2. Ingresás `p` y `q` como primos diferentes de 1 o 2 cifras
3. El sistema calcula `n`, `φ(n)` y muestra todos los `d` posibles
4. Seleccionás `d` — solo los coprimos con `φ(n)` son válidos
5. El sistema calcula `e` como inverso modular de `d`
6. Se cifra el texto y se guarda en `mensaje_encriptado.txt`
7. Otro usuario puede abrir ese `.txt` y descifrarlo con la opción 6

Este modo es ideal para **aprender RSA** porque muestra exactamente cómo funciona cada operación matemática, sin magia ni cajas negras.

---

## Archivos generados

Cada operación produce archivos que persisten en el disco:

| Archivo | Contenido | ¿Se comparte? |
|---------|-----------|---------------|
| `llave_publica.json` | `(n, e)` — clave pública | ✅ Sí, con el jefe |
| `llave_privada_empleado.json` | `(n, d)` + detalle matemático | ❌ NO, solo local |
| `credenciales_encriptadas.json` | Credenciales cifradas por el jefe | ✅ Se devuelve al empleado |
| `mensaje_encriptado.txt` | Bloques cifrados + clave privada del ejercicio | ✅ Para compartir en el flujo paso a paso |

---

## Matemática detrás

El proyecto implementa RSA desde los fundamentos:

1. **Máximo común divisor** — algoritmo de Euclides para validar coprimos
2. **Euclides extendido** — encuentra inversos modulares para calcular `e`
3. **Test de primalidad Miller-Rabin** — genera y valida primos
4. **Cifrado**: `C = M^e mod n` — cada byte del texto se cifra individualmente
5. **Descifrado**: `M = C^d mod n` — solo posible con la llave privada correcta

Todo el código matemático está en `rsa_backend.py`, completamente aislado de las interfaces.

---

## Stack tecnológico

```
Backend:   Python 3.14+, Flask, flask-cors
Frontend:  JavaScript vanilla, Vite, CSS custom properties
GUI:       Tkinter (Python stdlib)
Matemática: Python puro (sin librerías criptográficas externas)
```

---

## Estructura del proyecto

```
Criptografia/
├── api/
│   └── api.py                    # Servidor Flask con endpoints REST + terminal
├── frontend/
│   ├── src/
│   │   ├── main.js               # Punto de entrada SPA
│   │   ├── components/           # Componentes UI reutilizables
│   │   ├── views/                # Vistas por operación (1-7)
│   │   ├── services/api.js       # Cliente HTTP
│   │   └── styles/               # Sistema de diseño Vault Dark
│   ├── public/favicon.svg        # Candado geométrico (sin caja)
│   └── package.json
├── rsa_backend.py                # Núcleo matemático RSA (reutilizable)
├── main.py                       # Interfaz de terminal
├── gui.py                        # Interfaz gráfica Tkinter
├── requirements.txt              # Flask >= 3.0, flask-cors >= 4.0
└── WEB_UI_ORCHESTRATION.md       # Documento de arquitectura y diseño
```

---

## Referencia rápida de API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/keys/generate` | Generar llaves automáticas |
| `POST` | `/api/keys/from-primes` | Llaves desde `p`, `q`, `d` manuales |
| `POST` | `/api/encrypt` | Cifrar texto con clave pública |
| `POST` | `/api/decrypt` | Descifrar bloques con clave privada |
| `POST` | `/api/credentials/encrypt` | Cifrar dos credenciales (jefe) |
| `POST` | `/api/credentials/decrypt` | Descifrar dos credenciales (empleado) |
| `POST` | `/api/verify` | Verificar que un par de llaves funciona |

También hay endpoints `/api/terminal/*` que devuelven el mismo output textual que la terminal, incluyendo bloques de título, líneas de proceso y advertencias.

---

## Licencia y advertencia

**Esto es una implementación académica** para aprender aritmética modular y criptografía RSA. No está auditada para producción. Para credenciales reales de una empresa, usá una librería probada como `cryptography` con RSA-OAEP, o directamente un protocolo como TLS/HTTPS.

Dicho esto: la matemática es la misma. Si entendés esta implementación, entendés cómo funciona RSA en cualquier sistema.

---

Contribuí a la comunidad matemática.
Aprendé, usá, mejorá, compartí.
