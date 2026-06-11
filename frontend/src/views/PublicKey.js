import { Alert } from '../components/Alert.js';
import { CryptoButton } from '../components/CryptoButton.js';
import { KeyDisplay } from '../components/KeyDisplay.js';
import { LoadingSkeleton } from '../components/LoadingSkeleton.js';
import { ResultPanel } from '../components/ResultPanel.js';
import { TerminalCard } from '../components/TerminalCard.js';
import { TerminalBlocks } from '../components/TerminalBlocks.js';
import { api } from '../services/api.js';
import { copyText, storageSet } from '../utils/formatters.js';
import { setLoading } from '../utils/validators.js';

export const PublicKey = {
  render() {
    return `
      <section class="view">
        <header class="view-header">
          <div class="eyebrow">$ opción 2</div>
          <h1 class="view-title">Empleado: mostrar llave pública para el jefe</h1>
          <p class="view-copy">Este es el único material que debería recibir el jefe.</p>
        </header>
        <div class="panel-grid">
          <section class="form-panel">
            <div class="card-header"><div><h2 class="card-title">Paso 2 - Compartir llave pública</h2><p class="card-copy">Compartí solo la llave pública.</p></div></div>
            <div class="button-row">${CryptoButton('Mostrar llave pública para el jefe', 'show-public-btn')}</div>
          </section>
          <div id="public-result" class="result-slot">
            ${TerminalCard({ title: 'Datos para compartir', badge: 'esperando', lines: ['Primero generá las llaves con la opción 1.'] })}
          </div>
        </div>
      </section>
    `;
  },

  init() {
    const button = document.getElementById('show-public-btn');
    const slot = document.getElementById('public-result');
    button.addEventListener('click', async () => {
      try {
        setLoading(button, true, 'Cargando');
        slot.innerHTML = LoadingSkeleton(4);
        const data = await api.terminalShowPublicKey();
        storageSet('rsa.publicKey', data.public_key);
        slot.innerHTML = `
          ${TerminalBlocks(data.terminal)}
          ${KeyDisplay('Clave pública', data.public_key, 'public')}
          ${ResultPanel('Datos para compartir', data, 'public-key-json')}
          <div class="button-row"><button class="ghost-button" id="copy-public-key">Copiar llave pública</button></div>
        `;
        document.getElementById('copy-public-key').addEventListener('click', () => copyText(data.public_key));
      } catch (error) {
        slot.innerHTML = Alert('error', error.message);
      } finally {
        setLoading(button, false);
      }
    });
  },
};
