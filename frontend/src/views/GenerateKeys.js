import { Alert } from '../components/Alert.js';
import { CryptoButton } from '../components/CryptoButton.js';
import { KeyDisplay } from '../components/KeyDisplay.js';
import { LoadingSkeleton } from '../components/LoadingSkeleton.js';
import { ResultPanel } from '../components/ResultPanel.js';
import { TerminalCard } from '../components/TerminalCard.js';
import { TerminalBlocks } from '../components/TerminalBlocks.js';
import { TerminalInput } from '../components/TerminalInput.js';
import { api } from '../services/api.js';
import { copyText, downloadJson, storageSet } from '../utils/formatters.js';
import { intValue, setLoading } from '../utils/validators.js';

export const GenerateKeys = {
  render() {
    return `
      <section class="view">
        <header class="view-header">
          <div class="eyebrow">$ opción 1</div>
          <h1 class="view-title">Empleado: generar llaves pública y privada</h1>
          <p class="view-copy">La llave pública se comparte con el jefe para cifrar credenciales. La llave privada se queda con el empleado para descifrar lo recibido.</p>
        </header>
        <div class="panel-grid">
          <section class="form-panel">
            <div class="card-header"><div><h2 class="card-title">Paso 1 - Empleado genera llaves</h2><p class="card-copy">La llave pública se comparte. La llave privada no debe compartirse.</p></div></div>
            <div class="form-stack">
              ${TerminalInput({ id: 'bits', label: 'bits por primo', type: 'number', value: '16', min: 8 })}
              <div class="button-row">${CryptoButton('Generar llaves pública y privada', 'generate-btn')}</div>
            </div>
          </section>
          <div id="keys-result" class="result-slot">
            ${TerminalCard({ title: 'Resultado', badge: 'esperando', lines: ['Generá las llaves para ver la llave pública, la llave privada y el detalle matemático.'] })}
          </div>
        </div>
      </section>
    `;
  },

  init() {
    const button = document.getElementById('generate-btn');
    const slot = document.getElementById('keys-result');
    button.addEventListener('click', async () => {
      try {
        setLoading(button, true, 'Generando');
        slot.innerHTML = LoadingSkeleton(5);
        const bits = intValue('bits', 'bits');
        const data = await api.terminalGenerateKeys(bits);
        storageSet('rsa.publicKey', data.public_key);
        storageSet('rsa.privateKey', data.private_key);
        storageSet('rsa.keyPair', data);
        slot.innerHTML = `
          ${TerminalBlocks(data.terminal)}
          ${Alert('llaves generadas correctamente', 'Compartir con el jefe: llave_publica.json. Guardar sin compartir: llave_privada_empleado.json.', 'success')}
          <div class="key-grid">${KeyDisplay('Clave publica', data.public_key, 'public')}${KeyDisplay('Clave privada', data.private_key, 'private')}</div>
          ${ResultPanel('Detalle matematico', data, 'keys-json')}
          <div class="button-row">
            <button class="ghost-button" id="copy-keys">Copiar JSON</button>
            <button class="ghost-button" id="download-keys">Descargar JSON</button>
          </div>
        `;
        document.getElementById('copy-keys').addEventListener('click', () => copyText(data));
        document.getElementById('download-keys').addEventListener('click', () => downloadJson('rsa-keys.json', data));
      } catch (error) {
        slot.innerHTML = Alert('error', error.message);
      } finally {
        setLoading(button, false);
      }
    });
  },
};
