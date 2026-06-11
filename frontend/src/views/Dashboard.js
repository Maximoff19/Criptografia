import { TerminalCard } from '../components/TerminalCard.js';
import { escapeHtml, storageGet } from '../utils/formatters.js';

export const Dashboard = {
  render() {
    const publicKey = storageGet('rsa.publicKey');
    const privateKey = storageGet('rsa.privateKey');
    const blocks = storageGet('rsa.lastEncryptedBlocks');
    return `
      <section class="view">
        <header class="view-header">
          <div class="eyebrow">$ menú principal</div>
          <h1 class="view-title">Criptografía RSA</h1>
          <p class="view-copy">Flujo empleado/jefe y texto RSA paso a paso.</p>
        </header>

        <div class="dashboard-hero">
          ${TerminalCard({
            title: 'Flujo empresa',
            copy: 'El empleado genera llaves, el jefe cifra credenciales y el empleado descifra lo recibido.',
            badge: 'rsa',
            accent: true,
            lines: [
              '1) Empleado: generar llaves pública y privada',
              '2) Empleado: mostrar llave pública para el jefe',
              '3) Jefe: cifrar dos credenciales con la llave pública',
              '4) Empleado: descifrar credenciales con la llave privada',
            ],
          })}
          <div class="metrics-grid">
            <div class="metric-card"><div class="metric-label">Clave publica</div><div class="metric-value">${publicKey ? 'lista' : 'pendiente'}</div></div>
            <div class="metric-card"><div class="metric-label">Clave privada</div><div class="metric-value">${privateKey ? 'lista' : 'pendiente'}</div></div>
            <div class="metric-card"><div class="metric-label">Bloques cifrados</div><div class="metric-value">${Array.isArray(blocks) ? blocks.length : 0}</div></div>
            <div class="metric-card"><div class="metric-label">Algoritmo</div><div class="metric-value">RSA</div></div>
          </div>
        </div>

        <div class="quick-grid">
          ${quickCard('/keys/generate', '01', 'Empleado: generar llaves pública y privada', 'La llave pública se comparte con el jefe para cifrar credenciales.')}
          ${quickCard('/public-key', '02', 'Empleado: mostrar llave pública para el jefe', 'Este es el único material que debería recibir el jefe.')}
          ${quickCard('/credentials/encrypt', '03', 'Jefe: cifrar dos credenciales con la llave pública', 'El resultado se guarda en credenciales_encriptadas.json para devolverlo al empleado.')}
        </div>

        ${TerminalCard({
          title: 'Texto RSA paso a paso',
          badge: 'manual',
          lines: [
            '5) Encriptar texto con p y q manuales',
            '6) Desencriptar mensaje desde archivo TXT',
            '7) Ver explicación RSA paso a paso',
            '0) Salir',
          ],
        })}
      </section>
    `;
  },

  init() {},
};

function quickCard(route, index, title, copy) {
  return `
    <a href="#${escapeHtml(route)}" class="terminal-card">
      <div class="card-header">
        <div>
          <div class="eyebrow">${escapeHtml(index)}</div>
          <h2 class="card-title">${escapeHtml(title)}</h2>
          <p class="card-copy">${escapeHtml(copy)}</p>
        </div>
      </div>
    </a>
  `;
}
