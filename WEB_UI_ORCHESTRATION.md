# 🧬 WEB UI — Orquestación para interfaz web RSA

> **Propósito:** Documentar la arquitectura, diseño visual, API y plan de implementación para construir una UI web moderna para la aplicación educativa de Criptografía RSA.
>
> **Stack objetivo:** Flask (backend API) + HTML/CSS/JS vanilla o React ligero (frontend)
>
> **Estado actual:** App de terminal + Tkinter. **No existe API web aún.** Este documento describe qué construir.

---

## 📋 Índice

1. [Análisis del proyecto actual](#1-análisis-del-proyecto-actual)
2. [Diseño visual y sistema de diseño](#2-diseño-visual-y-sistema-de-diseño)
3. [API REST — Endpoints propuestos](#3-api-rest--endpoints-propuestos)
4. [Arquitectura frontend](#4-arquitectura-frontend)
5. [Flujo de datos](#5-flujo-de-datos)
6. [Cómo levantar el proyecto](#6-cómo-levantar-el-proyecto)
7. [Roadmap de implementación](#7-roadmap-de-implementación)
8. [Árbol de archivos objetivo](#8-árbol-de-archivos-objetivo)

---

## 1. Análisis del proyecto actual

### 1.1 Estructura existente

```
Criptografia/
├── rsa_backend.py              # ⚡ Núcleo matemático RSA (reutilizable)
├── main.py                     # Interfaz de terminal
├── gui.py                      # Interfaz Tkinter
├── Aritmética modular y Criptografía RSA.pdf  # PDF de referencia académica
├── presentacion_rsa_flujo.pptx # Presentación del flujo RSA
├── README.md                   # Documentación existente
├── llave_publica.json          # Clave pública generada
├── llave_privada_empleado.json # Clave privada del empleado
├── credenciales_encriptadas.json # Credenciales cifradas
└── mensaje_encriptado.txt      # Mensaje cifrado en TXT
```

### 1.2 Backend disponible (`rsa_backend.py`)

El archivo `rsa_backend.py` contiene **toda la lógica RSA** en Python puro (sin dependencias externas). Es el corazón reutilizable. No es una API, sino una biblioteca de funciones.

| Función | Descripción |
|---|---|
| `generar_llaves(bits)` | Genera par completo: p, q, n, φ(n), d, e |
| `generar_llaves_desde_primos(p, q, d, e)` | Genera llaves desde valores manuales |
| `cifrar_texto(texto, llave_publica)` | Cifra texto → lista de enteros |
| `descifrar_texto(bloques, llave_privada)` | Descifra bloques → texto original |
| `cifrar_dos_datos(d1, d2, pub)` | Cifra dos credenciales (flujo empresa) |
| `descifrar_dos_datos(paquete, priv)` | Descifra dos credenciales |
| `verificar_par_de_llaves(par)` | Verifica que pública y privada funcionen |
| `guardar_json/leer_json` | Persistencia en archivos JSON |

**⚠️ No hay API web.** Todo es invocación directa desde Python. Para la UI web hay que crear una capa API.

### 1.3 Formato de datos

**Clave pública:**
```json
{ "n": 3487486853, "e": 3294627239 }
```

**Clave privada (solo local):**
```json
{ "privada": { "n": 3487486853, "d": 541377059 }, "publica": {...}, "detalle_matematico": {...} }
```

**Credenciales cifradas (flujo empresa):**
```json
{
  "algoritmo": "RSA educativo sin padding",
  "llave_publica_usada": { "n": ..., "e": ... },
  "dato_uno_cifrado": [2195736217, 14104274, ...],
  "dato_dos_cifrado": [2195736217, ...]
}
```

**Mensaje cifrado (flujo texto):**
```json
{
  "mensaje_encriptado": [2195736217, ...],
  "clave_privada_para_descifrar": { "n": ..., "d": ... }
}
```

---

## 2. Diseño visual y sistema de diseño

### 2.1 Concepto estético

```
╔══════════════════════════════════════════════════════════════╗
║            TÁCTICAL TELEMETRY × CRYPTO MINIMAL              ║
║  Fusión entre:                                               ║
║  • Terminales militares / HUD                               ║
║  • Dark mode profundo estilo "crypto vault"                  ║
║  • Precisión tipográfica suiza + monospace                   ║
║  • Efectos sutiles de phosphor glow                          ║
╚══════════════════════════════════════════════════════════════╝
```

La UI web debe sentirse como **operar una consola de cifrado**: oscura, precisa, con jerarquía matemática clara. Cada elemento debe transmitir seguridad y control.

**Inspiración visual:** interfaces de hardware criptográfico (HSM), paneles de monitoreo de seguridad, terminales militares, dashboards de blockchain.

### 2.2 Paleta cromática — "Vault Dark"

```css
/* DESIGN TOKENS — VAULT DARK */
:root {
  /* ─── Fondos ─── */
  --bg-primary:     #090909;   /* Fondo principal — negro profundo */
  --bg-secondary:   #0d0d0d;   /* Tarjetas, paneles secundarios */
  --bg-tertiary:    #111111;   /* Hover, superficies elevadas */
  --bg-elevated:    #161616;   /* Modales, dropdowns */
  --bg-input:       #0a0a0a;   /* Campos de entrada */

  /* ─── Superficies y bordes ─── */
  --surface:        #0d0d0d;
  --border:         #1a1a1a;   /* Bordes generales sutiles */
  --border-accent:  #00FF62;   /* Bordes de enfoque, resaltados */
  --border-hover:   #2a2a2a;   /* Bordes en hover */

  /* ─── Texto ─── */
  --text-primary:   #e8e8e8;   /* Texto principal */
  --text-secondary: #888888;   /* Texto secundario, metadatos */
  --text-muted:     #555555;   /* Placeholders, deshabilitado */
  --text-inverse:   #090909;   /* Texto sobre acentos */

  /* ─── Acento principal — VERDE FÓSFORO ─── */
  --accent:         #00FF62;   /* Acciones, highlights, éxitos */
  --accent-dim:     #00CC4E;   /* Hover de acentos */
  --accent-subtle:  #00FF6215; /* Fondo sutil de acento (glow) */
  --accent-glow:    0 0 20px rgba(0, 255, 98, 0.15); /* Efecto glow */

  /* ─── Semántica ─── */
  --success:        #00FF62;
  --warning:        #FFB800;
  --error:          #FF3355;
  --info:           #00B4FF;

  /* ─── Tipografía ─── */
  --font-display:   'SF Mono', 'JetBrains Mono', 'Geist Mono', monospace;
  --font-body:      'Inter', 'SF Pro Display', 'Geist Sans', sans-serif;
  --font-mono:      'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;

  /* ─── Radios ─── */
  --radius-sm:      4px;
  --radius-md:      8px;
  --radius-lg:      12px;
  --radius-xl:      16px;

  /* ─── Sombras ─── */
  --shadow-sm:      0 1px 2px rgba(0,0,0,0.5);
  --shadow-md:      0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg:      0 8px 32px rgba(0,0,0,0.6);
  --shadow-glow:    0 0 30px rgba(0, 255, 98, 0.08);
}
```

### 2.3 Principios de diseño (MANDATORIOS)

Estos principios son **reglas, no sugerencias.** La UI debe cumplirlos todos.

#### ✅ REGLAS DE ORO

| # | Principio | Aplicación |
|---|-----------|------------|
| 1 | **Dark profundo** | `#090909` como canvas base. Nunca usar fondos claros. |
| 2 | **Monospace dominante** | Todos los datos cifrados, claves y resultados en `font-mono`. Solo títulos largos pueden usar sans-serif. |
| 3 | **Verde fósforo como único acento** | `#00FF62` para botones primarios, borders activos, iconos de éxito, glows. No usar azul, naranja ni púrpura como primarios. |
| 4 | **Jerarquía terminal** | Los datos deben verse como output de consola. Sin decoraciones innecesarias. |
| 5 | **Transparencia cero** | Sin glassmorphism. Sin fondos translúcidos en paneles de trabajo. |
| 6 | **Bordes vivos** | `1px solid #1a1a1a` en tarjetas. Borde `#00FF62` solo en estado activo/foco. |
| 7 | **Espaciado generoso** | `py-16` a `py-24` entre secciones. `p-6` a `p-8` en tarjetas. |
| 8 | **Sin sombras genéricas** | Solo `box-shadow` personalizados ultra sutiles. Nada de `shadow-md` por defecto. |
| 9 | **Motion mínima y precisa** | Transiciones de 200ms. Hover states. Sin animaciones decorativas que no sirvan. |
| 10 | **Código sobre marketing** | La UI es una herramienta, no un landing page. El contenido es el centro. |

#### ❌ PROHIBICIONES ABSOLUTAS

| Prohibición | Alternativa |
|-------------|-------------|
| Gradientes de fondo | `#090909` sólido |
| Imágenes de stock | Iconos geométricos simples o datos reales |
| Sombras difusas genéricas | `box-shadow: 0 1px 2px rgba(0,0,0,0.5)` |
| Bordes redondeados > 16px | `border-radius: 8px` o `12px` máximo |
| Animaciones de carga tipo "spinner" | Skeleton screens con opacidad pulsante |
| Iconos de fontawesome/lucide estándar | Phosphor Icons bold weight o SVG inline |
| Efectos glass/blur en áreas de trabajo | Fondos sólidos para legibilidad |
| Colores pastel | Solo escala de grises + verde acento |

### 2.4 Tipografía

```
Jerarquía tipográfica:

Display (títulos mayores)  → font-mono, weight 600, tracking -0.02em
  Ej: "RSA Tool" — 2rem-3rem

Heading (secciones)        → font-mono, weight 500, tracking normal
  Ej: "Generar Llaves" — 1.25rem-1.5rem

Body (texto)               → font-sans, weight 400
  Ej: "Ingrese los primos p y q" — 0.875rem-1rem

Code (datos/output)        → font-mono, weight 400
  Ej: "n = 3487486853" — 0.75rem-0.875rem

Meta (etiquetas/chips)     → font-mono, weight 400, uppercase, tracking 0.05em
  Ej: "CIFRADO" — 0.625rem-0.75rem
```

**Fuentes recomendadas:**
- **Display/Headings:** `JetBrains Mono`, `SF Mono`, `Geist Mono`
- **Body:** `Inter`, `SF Pro Display`, `Geist Sans`
- **Etiquetas:** `JetBrains Mono` uppercase con tracking amplio

### 2.5 Componentes visuales

#### 2.5.1 Terminal Card (contenedor de datos)

```
┌──────────────────────────────────────┐
│  $ n = 3487486853                    │  ← Output de consola
│  $ e = 3294627239                    │     (monospace, text-primary)
│                                      │
│  [ CREDENCIALES CIFRADAS ]           │  ← Status chip verde
└──────────────────────────────────────┘
```

**Especificación:**
- Borde: `1px solid #1a1a1a` | `border-radius: 8px`
- Fondo: `#0d0d0d`
- Padding: `24px`
- Shadow: `0 1px 2px rgba(0,0,0,0.5)`

#### 2.5.2 Input Field (estilo terminal)

```
┌─────────────────────────────────────┐
│ $ Ingrese primo p > _               │  ← Prompt style
└─────────────────────────────────────┘
```

**Especificación:**
- Fondo: `#0a0a0a`
- Borde: `1px solid #1a1a1a` → focus: `1px solid #00FF62`
- Texto: `font-mono`, `#e8e8e8`
- Padding: `12px 16px`
- Placeholder: `#555555`
- Focus glow: `box-shadow: 0 0 0 3px rgba(0,255,98,0.1)`

#### 2.5.3 Primary Button

```
┌──────────────────────────────┐
│  [ → CIFRAR CON RSA ]       │  ← tracking amplio, uppercase
└──────────────────────────────┘
```

**Especificación:**
- Fondo: `#00FF62` → hover: `#00CC4E` → active: `scale(0.98)`
- Texto: `#090909`, `font-mono`, `uppercase`, `tracking: 0.05em`
- Padding: `12px 24px`
- Border-radius: `8px`
- Transition: `all 200ms ease`

#### 2.5.4 Decorative "Binance-style" lock icon (SVG)

```svg
<!-- Icono de candado geométrico minimalista -->
<svg viewBox="0 0 24 24" fill="none" stroke="#00FF62" stroke-width="1.5">
  <rect x="5" y="11" width="14" height="10" rx="2"/>
  <path d="M8 11V7a4 4 0 0 1 8 0v4"/>
  <circle cx="12" cy="16" r="1" fill="#00FF62"/>
</svg>
```

#### 2.5.5 Loading skeleton (para operaciones criptográficas)

```css
.skeleton {
  background: linear-gradient(90deg, #111111 25%, #1a1a1a 50%, #111111 75%);
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s infinite;
  border-radius: 6px;
}
@keyframes skeleton-pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### 2.6 Layout general

```
┌──────────────────────────────────────────────────┐
│  ⚡ CRYPTO RSA · encrypted tool    [vault-dark]  │ ← Header minimalista
│  ──────────────────────────────────────────────  │
│                                                    │
│  ┌──────────┐  ┌──────────────────────────────┐  │
│  │ NAV      │  │  PANEL PRINCIPAL              │  │
│  │          │  │                                │  │
│  │ [GENERAR]│  │  ┌─ Terminal Output ───────┐  │  │
│  │ [CIFRAR] │  │  │ $ n = 3487486853        │  │  │
│  │ [DECODE] │  │  │ $ phi = 3487368300       │  │  │
│  │ [TXT]    │  │  └──────────────────────────┘  │  │
│  │          │  │                                │  │
│  │          │  │  ┌─ Input Area ────────────┐  │  │
│  │          │  │  │ $ Ingrese p > _         │  │  │
│  │          │  │  │ $ Ingrese q > _         │  │  │
│  │          │  │  └──────────────────────────┘  │  │
│  └──────────┘  └──────────────────────────────┘  │
│                                                    │
│  ──────────────────────────────────────────────  │
│  [INFO] RSA Educativo · Sin padding · Solo fines  │ ← Footer
│  académicos                                        │
└──────────────────────────────────────────────────┘
```

**Responsive:**
- Desktop (≥1024px): Sidebar nav + panel principal
- Tablet (768-1023px): Nav horizontal colapsable + panel
- Mobile (<768px): Stack vertical, nav como hamburger

---

## 3. API REST — Endpoints propuestos

Se debe crear un servidor Flask (`api.py`) que envuelva `rsa_backend.py` en endpoints HTTP.

### 3.1 `POST /api/keys/generate`

Genera un par de llaves RSA automáticamente.

**Request:**
```json
{
  "bits": 16
}
```

**Response (200):**
```json
{
  "public_key": { "n": 3487486853, "e": 3294627239 },
  "private_key": { "n": 3487486853, "d": 541377059 },
  "mathematical_detail": { "p": 64403, "q": 54151, "phi": 3487368300 },
  "verified": true
}
```

### 3.2 `POST /api/keys/from-primes`

Genera llaves desde primos manuales `p` y `q`.

**Request:**
```json
{
  "p": 17,
  "q": 19,
  "d": 7
}
```

**Response (200):**
```json
{
  "n": 323,
  "phi": 288,
  "posibles_d": [5, 7, 11, 13, 17, 19, 23, 25, 29, 31, ...],
  "d": 7,
  "e_base": 247,
  "posibles_e": [247, 535, 823, 1111, 1399],
  "e": 247,
  "public_key": { "n": 323, "e": 247 },
  "private_key": { "n": 323, "d": 7 }
}
```

### 3.3 `POST /api/encrypt`

Cifra un texto con una clave pública.

**Request:**
```json
{
  "text": "Hola Mundo",
  "public_key": { "n": 3487486853, "e": 3294627239 }
}
```

**Response (200):**
```json
{
  "algorithm": "RSA educativo sin padding",
  "warning": "No usar en producción",
  "public_key_used": { "n": 3487486853, "e": 3294627239 },
  "encrypted_blocks": [2195736217, 14104274, ...],
  "block_count": 10,
  "original_length": 10
}
```

### 3.4 `POST /api/decrypt`

Descifra bloques con una clave privada.

**Request:**
```json
{
  "encrypted_blocks": [2195736217, 14104274, ...],
  "private_key": { "n": 3487486853, "d": 541377059 }
}
```

**Response (200):**
```json
{
  "decrypted_text": "Hola Mundo",
  "success": true
}
```

### 3.5 `POST /api/credentials/encrypt`

Cifra dos credenciales (flujo empresa: jefe cifra).

**Request:**
```json
{
  "data_one": "empleado@empresa.com",
  "data_two": "mi_contraseña_segura",
  "public_key": { "n": 3487486853, "e": 3294627239 }
}
```

**Response (200):**
```json
{
  "algorithm": "RSA educativo sin padding",
  "warning": "No usar en producción",
  "public_key_used": { "n": ..., "e": ... },
  "data_one_encrypted": [2195736217, ...],
  "data_two_encrypted": [2195736217, ...],
  "status": "encrypted"
}
```

### 3.6 `POST /api/credentials/decrypt`

Descifra dos credenciales (flujo empresa: empleado descifra).

**Request:**
```json
{
  "data_one_encrypted": [2195736217, ...],
  "data_two_encrypted": [2195736217, ...],
  "private_key": { "n": 3487486853, "d": 541377059 }
}
```

**Response (200):**
```json
{
  "data_one": "empleado@empresa.com",
  "data_two": "mi_contraseña_segura",
  "success": true
}
```

### 3.7 `POST /api/verify`

Verifica que un par de llaves funcione.

**Request:**
```json
{
  "public_key": { "n": 3487486853, "e": 3294627239 },
  "private_key": { "n": 3487486853, "d": 541377059 }
}
```

**Response (200):**
```json
{
  "verified": true,
  "test_message": "prueba",
  "encrypted_test": [12345, ...],
  "decrypted_test": "prueba"
}
```

### 3.8 `GET /api/health`

Health check del servidor.

**Response (200):**
```json
{
  "status": "online",
  "version": "1.0.0",
  "algorithm": "RSA educativo",
  "endpoints": [
    "/api/keys/generate",
    "/api/keys/from-primes",
    "/api/encrypt",
    "/api/decrypt",
    "/api/credentials/encrypt",
    "/api/credentials/decrypt",
    "/api/verify",
    "/api/health"
  ]
}
```

---

## 4. Arquitectura frontend

### 4.1 Stack recomendado

| Capa | Tecnología | Justificación |
|---|---|---|
| **Framework** | Vanilla JS + Vite | Sin dependencias pesadas, rápida, suficiente para una herramienta |
| **Alternativa** | React 19 + Vite | Si se prefiere componentización y estado manejable |
| **Estilos** | CSS puro con variables custom | Sin Tailwind ni frameworks CSS para mantener el control total |
| **Iconos** | Phosphor Icons (bold) o SVG inline | Estilo preciso, técnico, consistente |
| **HTTP** | `fetch()` nativo | Sin Axios ni librerías extra |
| **Build** | Vite | Dev server + build optimizado |
| **API server** | Flask (Python) | Misma stdlib que el backend, sin Node.js |

### 4.2 Árbol de componentes

```
src/
├── index.html
├── main.js                    # Entry point
├── styles/
│   ├── tokens.css             # Variables CSS (colores, fuentes, radios)
│   ├── reset.css              # Reset moderno
│   ├── base.css               # Estilos base (body, typography)
│   ├── components.css         # Componentes reutilizables
│   └── pages.css              # Estilos específicos de página/vista
├── components/
│   ├── TerminalCard.js        # Contenedor de output (estilo consola)
│   ├── TerminalInput.js       # Input con prompt style
│   ├── CryptoButton.js        # Botón principal verde
│   ├── KeyDisplay.js          # Visualizador de llaves
│   ├── BlockViewer.js         # Viewer de bloques cifrados
│   ├── ResultPanel.js         # Panel de resultados
│   ├── NavSidebar.js          # Navegación lateral
│   ├── StatusBadge.js         # Chips de estado (cifrado/descifrado)
│   ├── LoadingSkeleton.js     # Skeleton loader
│   └── Alert.js               # Alertas (error, warning, success)
├── views/
│   ├── GenerateKeys.js        # Vista: generar llaves automáticas
│   ├── ManualKeys.js          # Vista: llaves desde p, q manuales
│   ├── EncryptText.js         # Vista: cifrar texto
│   ├── DecryptText.js         # Vista: descifrar texto
│   ├── CredentialsFlow.js     # Vista: flujo empresa (cifrar/descifrar)
│   └── Help.js                # Vista: ayuda / explicación RSA
├── services/
│   └── api.js                 # Cliente API (fetch wrapper)
└── utils/
    ├── formatters.js          # Formateo de números, bloques, llaves
    └── validators.js          # Validación de primos, textos, etc.
```

### 4.3 Rutas del frontend

| Ruta | Vista | Descripción |
|---|---|---|
| `/` | Dashboard | Resumen + acceso rápido a operaciones |
| `/keys/generate` | GenerateKeys | Generar llaves automáticas |
| `/keys/manual` | ManualKeys | Ingresar p, q, d manualmente |
| `/encrypt` | EncryptText | Cifrar texto con clave pública |
| `/decrypt` | DecryptText | Descifrar bloques con clave privada |
| `/credentials` | CredentialsFlow | Flujo empresa: cifrar/descifrar credenciales |
| `/help` | Help | Explicación RSA paso a paso |

### 4.4 Servicio API (`services/api.js`)

```javascript
const API_BASE = 'http://localhost:5050/api';

export const api = {
  async generateKeys(bits = 16) {
    const res = await fetch(`${API_BASE}/keys/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bits })
    });
    return res.json();
  },

  async keysFromPrimes(p, q, d) {
    const res = await fetch(`${API_BASE}/keys/from-primes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ p, q, d })
    });
    return res.json();
  },

  async encrypt(text, publicKey) {
    const res = await fetch(`${API_BASE}/encrypt`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, public_key: publicKey })
    });
    return res.json();
  },

  async decrypt(blocks, privateKey) {
    const res = await fetch(`${API_BASE}/decrypt`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        encrypted_blocks: blocks,
        private_key: privateKey
      })
    });
    return res.json();
  },

  async encryptCredentials(dataOne, dataTwo, publicKey) {
    const res = await fetch(`${API_BASE}/credentials/encrypt`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        data_one: dataOne,
        data_two: dataTwo,
        public_key: publicKey
      })
    });
    return res.json();
  },

  async decryptCredentials(encryptedOne, encryptedTwo, privateKey) {
    const res = await fetch(`${API_BASE}/credentials/decrypt`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        data_one_encrypted: encryptedOne,
        data_two_encrypted: encryptedTwo,
        private_key: privateKey
      })
    });
    return res.json();
  },

  async verifyKeys(publicKey, privateKey) {
    const res = await fetch(`${API_BASE}/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        public_key: publicKey,
        private_key: privateKey
      })
    });
    return res.json();
  },

  async health() {
    const res = await fetch(`${API_BASE}/health`);
    return res.json();
  }
};
```

---

## 5. Flujo de datos

### 5.1 Flujo: Generar llaves automáticas

```
Usuario                    Frontend                      API (Flask)               rsa_backend.py
  │                           │                             │                          │
  │  Click "Generar"          │                             │                          │
  │ ───────────────────────>  │                             │                          │
  │                           │  POST /api/keys/generate    │                          │
  │                           │ ────────────────────────>   │                          │
  │                           │                             │  generar_llaves(bits)     │
  │                           │                             │ ──────────────────────>   │
  │                           │                             │                          │
  │                           │                             │  <── ParDeLlaves ──────  │
  │                           │                             │                          │
  │                           │  <── { public_key,          │                          │
  │                           │         private_key,        │                          │
  │                           │         details }           │                          │
  │                           │                             │                          │
  │  Muestra en TerminalCard  │                             │                          │
  │  <─────────────────────── │                             │                          │
```

### 5.2 Flujo: Cifrar texto

```
Usuario                    Frontend                      API (Flask)               rsa_backend.py
  │                           │                             │                          │
  │  Ingresa texto + n, e     │                             │                          │
  │ ───────────────────────>  │                             │                          │
  │                           │  Valida: text ≠ ""          │                          │
  │                           │  Valida: M < n              │                          │
  │                           │                             │                          │
  │                           │  POST /api/encrypt          │                          │
  │                           │ ────────────────────────>   │                          │
  │                           │                             │  cifrar_texto(t, pub)    │
  │                           │                             │ ──────────────────────>   │
  │                           │                             │                          │
  │                           │                             │  <── [blocks] ─────────  │
  │                           │                             │                          │
  │                           │  <── { encrypted_blocks,    │                          │
  │                           │         algorithm, ... }    │                          │
  │                           │                             │                          │
  │  Muestra bloques en       │                             │                          │
  │  BlockViewer              │                             │                          │
  │  <─────────────────────── │                             │                          │
```

### 5.3 Flujo: Descifrar credenciales (flujo empresa)

```
Usuario (Empleado)          Frontend                      API (Flask)               rsa_backend.py
  │                           │                             │                          │
  │  Pega bloques cifrados    │                             │                          │
  │  + clave privada (n, d)   │                             │                          │
  │ ───────────────────────>  │                             │                          │
  │                           │  POST /api/credentials/     │                          │
  │                           │         decrypt             │                          │
  │                           │ ────────────────────────>   │                          │
  │                           │                             │  descifrar_dos_datos()   │
  │                           │                             │ ──────────────────────>   │
  │                           │                             │                          │
  │                           │                             │  <── (d1, d2) ─────────  │
  │                           │                             │                          │
  │                           │  <── { data_one: "...",     │                          │
  │                           │         data_two: "..." }   │                          │
  │                           │                             │                          │
  │  Muestra datos            │                             │                          │
  │  descifrados             │                             │                          │
  │  <─────────────────────── │                             │                          │
```

### 5.4 Persistencia (sesión vs archivos)

| Dato | Frontend | Backend |
|---|---|---|
| Llaves generadas | `sessionStorage` (temporal) | Archivos JSON en disco |
| Bloques cifrados | `sessionStorage` (temporal) | Archivos JSON en disco |
| Texto descifrado | Solo en pantalla | No se persiste |
| Estado de UI | `localStorage` para tema | — |

**Flujo de archivos en backend (opcional):**
- `llave_publica.json` — se genera/sobrescribe
- `llave_privada_empleado.json` — se genera/sobrescribe
- `credenciales_encriptadas.json` — se genera al cifrar
- `mensaje_encriptado.txt` — se genera al cifrar texto manual

---

## 6. Cómo levantar el proyecto

### 6.1 Prerrequisitos

```bash
# Python 3.10+
python3 --version   # ≥ 3.10

# Node.js (para frontend con Vite, opcional)
node --version      # ≥ 18
```

### 6.2 Backend API (Flask)

```bash
# 1. Ir al directorio del proyecto
cd /ruta/a/Criptografia

# 2. (Opcional) Crear virtual env
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar Flask
pip install flask flask-cors

# 4. Ejecutar el servidor API
python3 api.py
# → Servidor en http://localhost:5050
```

**Archivo `api.py` (estructura mínima):**

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from rsa_backend import (
    generar_llaves, generar_llaves_desde_primos,
    cifrar_texto, descifrar_texto,
    cifrar_dos_datos, descifrar_dos_datos,
    verificar_par_de_llaves, ParDeLlaves,
    LlavePublica, LlavePrivada
)

app = Flask(__name__)
CORS(app)

@app.route('/api/health')
def health():
    return jsonify({
        "status": "online",
        "version": "1.0.0",
        "algorithm": "RSA educativo"
    })

@app.route('/api/keys/generate', methods=['POST'])
def keys_generate():
    data = request.get_json()
    bits = data.get('bits', 16)
    par = generar_llaves(bits)
    verified = verificar_par_de_llaves(par)
    return jsonify({
        "public_key": {"n": par.publica.n, "e": par.publica.e},
        "private_key": {"n": par.privada.n, "d": par.privada.d},
        "mathematical_detail": {"p": par.p, "q": par.q, "phi": par.phi},
        "verified": verified
    })

# ... más endpoints (from-primes, encrypt, decrypt, credentials, verify)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
```

### 6.3 Frontend (Vite + vanilla JS)

```bash
# 1. Crear projecto Vite
npm create vite@latest frontend -- --template vanilla
cd frontend

# 2. Desarrollo
npm run dev
# → Servidor en http://localhost:5173

# 3. Build producción
npm run build
# → Output en frontend/dist/
```

### 6.4 O ejecutar todo con un solo comando (recomendado)

```bash
# Desde la raíz del proyecto
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask-cors

# Terminal 1: Backend
python3 api.py

# Terminal 2: Frontend
cd frontend && npm run dev
```

---

## 7. Roadmap de implementación

### Fase 1: API base ⚡ (Día 1)

- [ ] Crear `api.py` con Flask + CORS
- [ ] Implementar `GET /api/health`
- [ ] Implementar `POST /api/keys/generate`
- [ ] Implementar `POST /api/encrypt`
- [ ] Implementar `POST /api/decrypt`
- [ ] Probar con `curl` o Postman

### Fase 2: Diseño system 🎨 (Día 1-2)

- [ ] Crear `tokens.css` con todas las variables CSS
- [ ] Crear `reset.css` y `base.css`
- [ ] Crear `components.css` con los componentes base
- [ ] Implementar layout general (sidebar + main)
- [ ] Probar diseño responsivo

### Fase 3: Vistas principales 🖥️ (Día 2-3)

- [ ] Vista `GenerateKeys` — generar llaves automáticas
- [ ] Vista `ManualKeys` — ingresar p, q, d manuales
- [ ] Vista `EncryptText` — cifrar texto
- [ ] Vista `DecryptText` — descifrar texto
- [ ] Vista `CredentialsFlow` — flujo empresa

### Fase 4: Features completas 🚀 (Día 3-4)

- [ ] Implementar `POST /api/keys/from-primes`
- [ ] Implementar `POST /api/credentials/encrypt`
- [ ] Implementar `POST /api/credentials/decrypt`
- [ ] Implementar `POST /api/verify`
- [ ] Vista `Help` — explicación RSA paso a paso
- [ ] Validaciones frontend (primos, texto, M < n)
- [ ] Loading states y errores visibles

### Fase 5: Pulido ✨ (Día 4-5)

- [ ] Animaciones de transición entre vistas
- [ ] Efecto glow en elementos activos
- [ ] Responsive design completo
- [ ] Copy to clipboard para llaves y bloques
- [ ] Descarga de JSON/TXT desde el frontend
- [ ] Prueba de flujo completo end-to-end

### Fase 6: Producción 🌐 (Opcional)

- [ ] Build frontend + servir desde Flask
- [ ] Manejo de errores consistente
- [ ] Modo offline (sin servidor, solo WASM o Pyodide)
- [ ] Docker compose (api + frontend)

---

## 8. Árbol de archivos objetivo

Al finalizar la implementación, el proyecto debe verse así:

```
Criptografia/
│
├── 📁 api/                          # Capa API
│   └── api.py                       #   Servidor Flask con endpoints
│
├── 📁 frontend/                     # Frontend web
│   ├── index.html                   #   Entry point
│   ├── package.json                 #   Dependencias
│   ├── vite.config.js               #   Config Vite
│   ├── 📁 public/                   #   Assets estáticos
│   │   └── favicon.svg              #     Favicon (candado geométrico)
│   └── 📁 src/
│       ├── main.js                  #   Entry point JS
│       ├── router.js                #   Enrutador SPA
│       ├── 📁 styles/
│       │   ├── tokens.css           #     Variables de diseño
│       │   ├── reset.css            #     Reset CSS
│       │   ├── base.css             #     Estilos base
│       │   ├── components.css       #     Componentes
│       │   └── pages.css            #     Estilos de vistas
│       ├── 📁 components/
│       │   ├── TerminalCard.js      #     Output tipo consola
│       │   ├── TerminalInput.js     #     Input con prompt
│       │   ├── CryptoButton.js      #     Botón principal
│       │   ├── KeyDisplay.js        #     Visualizador de llaves
│       │   ├── BlockViewer.js       #     Bloques cifrados
│       │   ├── ResultPanel.js       #     Panel de resultados
│       │   ├── NavSidebar.js        #     Navegación
│       │   ├── StatusBadge.js       #     Chips de estado
│       │   ├── LoadingSkeleton.js   #     Skeleton loader
│       │   └── Alert.js             #     Alertas
│       ├── 📁 views/
│       │   ├── GenerateKeys.js      #     Generar llaves automáticas
│       │   ├── ManualKeys.js        #     Llaves desde p, q
│       │   ├── EncryptText.js       #     Cifrar texto
│       │   ├── DecryptText.js       #     Descifrar texto
│       │   ├── CredentialsFlow.js   #     Flujo empresa
│       │   └── Help.js              #     Ayuda RSA
│       ├── 📁 services/
│       │   └── api.js               #     Cliente HTTP
│       └── 📁 utils/
│           ├── formatters.js        #     Formateadores
│           └── validators.js        #     Validadores
│
├── 📁 (archivos existentes)
│   ├── rsa_backend.py               #   Backend RSA (sin cambios)
│   ├── main.py                      #   Terminal UI (sin cambios)
│   ├── gui.py                       #   Tkinter UI (sin cambios)
│   ├── README.md
│   ├── WEB_UI_ORCHESTRATION.md      #   ← Estás aquí
│   ├── llave_publica.json
│   ├── llave_privada_empleado.json
│   ├── credenciales_encriptadas.json
│   └── mensaje_encriptado.txt
```

---

## Apéndice A: Checklist de diseño pre-flight

Antes de considerar completa la UI web, verificar:

```
[ ] Fondo #090909 en toda la app
[ ] Acento #00FF62 en todos los elementos interactivos
[ ] Sin colores pastel, sin gradientes
[ ] Sin glassmorphism en áreas de contenido
[ ] Sin bordes redondeados > 12px
[ ] Sin sombras por defecto (solo custom)
[ ] Fuente monospace en todos los datos cifrados
[ ] Inputs con estilo de terminal ($ prompt)
[ ] Botones en uppercase con tracking
[ ] Sin imágenes decorativas
[ ] Responsive: funciona en mobile
[ ] Copy to clipboard funcional
[ ] Errores visibles con Alert rojo
[ ] Loading skeleton durante operaciones criptográficas
[ ] Sin emojis en código ni UI
```

## Apéndice B: Referencia de API para consumir desde frontend

```
BASE_URL = http://localhost:5050/api

POST /api/keys/generate
  → Genera llaves RSA automáticas

POST /api/keys/from-primes
  → Genera llaves desde p, q, d manuales

POST /api/encrypt
  → Cifra texto con clave pública

POST /api/decrypt
  → Descifra bloques con clave privada

POST /api/credentials/encrypt
  → Cifra dos credenciales (flujo empresa)

POST /api/credentials/decrypt
  → Descifra dos credenciales (flujo empresa)

POST /api/verify
  → Verifica par de llaves

GET  /api/health
  → Health check
```

---

> **Documento generado como orquestación para construir la UI web del proyecto Criptografía RSA.**
>
> La implementación debe seguir estrictamente el sistema de diseño documentado.
> Cualquier desviación debe ser autorizada antes de implementarse.
