# Criptografía RSA — Open-source para empresas que valoran su privacidad

**Una herramienta open-source** pensada para empresas que necesitan un entorno seguro y privado para gestionar credenciales y datos sensibles, sin depender de servicios third-party, sin servidores centrales, sin compartir secretos. Criptografía RSA pura implementada desde cero.

---

## ¿Qué es esto?

Es un **sistema de cifrado asimétrico open-source** que cualquier empresa puede descargar, auditar, modificar y ejecutar en su propio entorno — completamente off-line, sin conexión a internet, sin enviar datos a ningún lado.

El core del proyecto es RSA implementado desde los fundamentos matemáticos: generación de primos, cálculo de `n` y `φ(n)`, selección de exponentes `d` y `e`, cifrado y descifrado. No es un wrapper de OpenSSL ni una librería externa — es RSA hecho a mano, transparente, verificable.

Pensalo como un **laboratorio de criptografía asimétrica privado** que funciona en tres interfaces:

| Interfaz | Propósito |
|----------|-----------|
| **Web UI** | Interfaz visual moderna, oscura, tipo consola criptográfica |
| **Terminal** | Interfaz de texto completa con colores ANSI y menú interactivo |
| **GUI Tkinter** | Ventana gráfica tradicional con pestañas y botones |

Todas las interfaces usan el mismo backend matemático (`rsa_backend.py`). Lo que hacés en una, funciona igual en las otras.

---

## ¿Para qué sirve en una empresa?

El flujo principal resuelve un problema real: **cómo compartir credenciales de forma segura sin un intermediario**.

```
1. El empleado genera su par de llaves (pública y privada)
2. El empleado comparte SOLO la llave pública con su jefe
3. El jefe cifra credenciales (usuario/contraseña) con esa llave pública
4. El jefe devuelve el archivo cifrado al empleado
5. SOLO el empleado puede descifrar, usando su llave privada
```

**Por qué esto es importante para tu empresa:**

- ✅ **Zero trust**: no hay servidor central, no hay administrador que pueda leer las credenciales.
- ✅ **Privacidad total**: los datos cifrados pueden viajar por cualquier canal (email, USB, Slack) y nadie sin la llave privada puede leerlos.
- ✅ **Sin dependencias externas**: no necesitás un proveedor de cloud, no necesitás internet, no necesitás nada más que Python.
- ✅ **Código abierto y auditable**: cualquier equipo de seguridad puede revisar exactamente qué hace el algoritmo.
- ✅ **Off-line first**: todo corre en la máquina local. No hay telemetría, no hay logs externos, no hay filtración posible por el lado del servidor.

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

## Advertencia

Esta herramienta implementa RSA educativo sin padding. Para sistemas de producción con requisitos de seguridad formales, usá una librería auditada como `cryptography` con RSA-OAEP o un protocolo estándar como TLS/HTTPS.

Dicho esto: **la matemática es la misma**. Si entendés esta implementación, entendés cómo funciona RSA en cualquier sistema. Y si tu empresa necesita una solución transparente, auditable y sin dependencias, este proyecto es un excelente punto de partida.

---

**Open-source. Privado. Seguro. Sin excusas.**

Descargalo, auditá el código, modificá lo que necesites, ejecutalo en tu entorno. No hay servers, no hay tracking, no hay sorpresas. Solo matemática.
