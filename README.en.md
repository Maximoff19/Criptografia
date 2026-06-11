# RSA Cryptography — Open-source for privacy-minded companies

**An open-source tool** built for companies that need a secure and private environment to manage credentials and sensitive data — no third-party services, no central servers, no shared secrets. Pure RSA cryptography implemented from scratch.

---

## What is this?

An **asymmetric encryption system** that any company can download, audit, modify and run in its own environment — completely off-line, no internet required, no data sent anywhere.

The core implements RSA from mathematical fundamentals: prime generation, `n` and `φ(n)` calculation, exponent selection for `d` and `e`, encryption and decryption. Not an OpenSSL wrapper, not an external library — handcrafted RSA, transparent and verifiable.

Think of it as a **private asymmetric cryptography lab** with three interfaces:

| Interface | Purpose |
|-----------|---------|
| **Web UI** | Modern dark-themed UI, crypto-console style |
| **Terminal** | Full text interface with ANSI colors and interactive menu |
| **GUI Tkinter** | Traditional window with tabs and buttons |

All interfaces share the same mathematical backend (`rsa_backend.py`). What you do in one works identically in the others.

---

## Why would a company use this?

The main workflow solves a real problem: **how to share credentials securely without an intermediary**.

```
1. Employee generates a key pair (public + private)
2. Employee shares ONLY the public key with the manager
3. Manager encrypts credentials (username/password) with the public key
4. Manager sends the encrypted file back to the employee
5. ONLY the employee can decrypt, using their private key
```

**Why this matters:**

- ✅ **Zero trust**: no central server, no admin who can read the credentials.
- ✅ **Total privacy**: encrypted data can travel through any channel (email, USB, Slack) and nobody without the private key can read it.
- ✅ **No external dependencies**: no cloud provider, no internet, nothing but Python.
- ✅ **Open-source and auditable**: any security team can review exactly what the algorithm does.
- ✅ **Off-line first**: everything runs locally. No telemetry, no external logs, no server-side leaks.

---

## Available interfaces

### Web UI (recommended)

The web interface provides the same workflow as the terminal with a Vault Dark design — ideal for demonstrations, presentations and daily use.

```
┌─────────────────────────────────────────────────────┐
│  1  Generate public and private keys                │
│  2  Show public key for manager                     │
│  3  Encrypt credentials with public key             │
│  4  Decrypt credentials with private key            │
│  5  Encrypt text with manual p and q                │
│  6  Decrypt message from TXT file                   │
│  7  RSA step-by-step explanation                    │
└─────────────────────────────────────────────────────┘
```

**To run the Web UI:**

```bash
# Terminal 1: Backend API (Flask)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m api.api
# → API at http://localhost:5050

# Terminal 2: Frontend (Vite)
cd frontend
npm install
npm run dev
# → Web at http://localhost:5173
```

Or build the frontend and serve it directly from Flask:

```bash
cd frontend
npm run build
# After that, http://localhost:5050/ serves the full web app
```

### Terminal

```bash
python3 main.py
```

Numeric menu with the same 7 options, ANSI colors, warning boxes and formatted output. Useful environment variables:

| Variable | Effect |
|----------|--------|
| `NO_COLOR=1` | Disables ANSI colors |
| `FORCE_COLOR=1` | Forces colors even if terminal is not detected as interactive |
| `RSA_NO_CLEAR=1` | Skips screen clearing between views (useful for logging) |

### GUI Tkinter

```bash
python3 gui.py
```

Graphical window with tabs for company workflow and manual step-by-step flow.

---

## Manual flow: RSA step by step

Beyond the company workflow, the project includes an educational mode where **every mathematical step is visible**:

1. Enter the text to encrypt
2. Enter `p` and `q` as different 1 or 2-digit primes
3. The system calculates `n`, `φ(n)` and shows all valid `d` values
4. Select `d` — only values coprime with `φ(n)` are valid
5. The system calculates `e` as the modular inverse of `d`
6. The text is encrypted and saved to `mensaje_encriptado.txt`
7. Another user can open that `.txt` and decrypt it with option 6

This mode is ideal for **learning RSA** because it shows exactly how every mathematical operation works — no magic, no black boxes.

---

## Generated files

Each operation produces files on disk:

| File | Content | Shared? |
|------|---------|---------|
| `llave_publica.json` | `(n, e)` — public key | ✅ Yes, with manager |
| `llave_privada_empleado.json` | `(n, d)` + math details | ❌ NO, local only |
| `credenciales_encriptadas.json` | Credentials encrypted by manager | ✅ Sent back to employee |
| `mensaje_encriptado.txt` | Encrypted blocks + private key for the exercise | ✅ Shared in step-by-step flow |

---

## Math behind it

The project implements RSA from the ground up:

1. **Greatest common divisor** — Euclid's algorithm to validate coprimes
2. **Extended Euclidean algorithm** — finds modular inverses to compute `e`
3. **Miller-Rabin primality test** — generates and validates primes
4. **Encryption**: `C = M^e mod n` — each byte is encrypted individually
5. **Decryption**: `M = C^d mod n` — only possible with the correct private key

All math lives in `rsa_backend.py`, completely isolated from the interfaces.

---

## Tech stack

```
Backend:   Python 3.14+, Flask, flask-cors
Frontend:  Vanilla JavaScript, Vite, CSS custom properties
GUI:       Tkinter (Python stdlib)
Math:      Pure Python (no external crypto libraries)
```

---

## Project structure

```
Criptografia/
├── api/
│   └── api.py                    # Flask server with REST + terminal endpoints
├── frontend/
│   ├── src/
│   │   ├── main.js               # SPA entry point
│   │   ├── components/           # Reusable UI components
│   │   ├── views/                # Views per operation (1-7)
│   │   ├── services/api.js       # HTTP client
│   │   └── styles/               # Vault Dark design system
│   ├── public/favicon.svg        # Geometric lock (no box)
│   └── package.json
├── rsa_backend.py                # RSA math core (reusable)
├── main.py                       # Terminal interface
├── gui.py                        # Tkinter GUI
├── requirements.txt              # Flask >= 3.0, flask-cors >= 4.0
└── WEB_UI_ORCHESTRATION.md       # Architecture and design document
```

---

## Quick API reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/keys/generate` | Generate automatic keys |
| `POST` | `/api/keys/from-primes` | Keys from `p`, `q`, `d` |
| `POST` | `/api/encrypt` | Encrypt text with public key |
| `POST` | `/api/decrypt` | Decrypt blocks with private key |
| `POST` | `/api/credentials/encrypt` | Encrypt two credentials (manager) |
| `POST` | `/api/credentials/decrypt` | Decrypt two credentials (employee) |
| `POST` | `/api/verify` | Verify a key pair works |

There are also `/api/terminal/*` endpoints that return the same textual output as the terminal, including title blocks, process lines and warnings.

---

## Disclaimer

This tool implements educational RSA without padding. For production systems with formal security requirements, use an audited library like `cryptography` with RSA-OAEP or a standard protocol like TLS/HTTPS.

That said: **the math is the same**. If you understand this implementation, you understand how RSA works in any system. And if your company needs a transparent, auditable, dependency-free solution, this project is an excellent starting point.

---

**Open-source. Private. Secure. No excuses.**

Download it, audit the code, modify what you need, run it in your environment. No servers, no tracking, no surprises. Just math.

---

## License

MIT — see [LICENSE](LICENSE) for details.
