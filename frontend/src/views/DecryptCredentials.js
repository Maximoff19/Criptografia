import { Alert } from '../components/Alert.js';
import { CryptoButton } from '../components/CryptoButton.js';
import { LoadingSkeleton } from '../components/LoadingSkeleton.js';
import { ResultPanel } from '../components/ResultPanel.js';
import { TerminalCard } from '../components/TerminalCard.js';
import { TerminalBlocks } from '../components/TerminalBlocks.js';
import { TerminalInput, TerminalTextarea } from '../components/TerminalInput.js';
import { api } from '../services/api.js';
import { escapeHtml, parseBlocks, storageGet } from '../utils/formatters.js';
import { privateKeyFromFields, setLoading } from '../utils/validators.js';

export const DecryptCredentials = {
  render() {
    const privateKey = storageGet('rsa.privateKey') || {};
    const packageData = storageGet('rsa.credentialsPackage') || {};
    return `
      <section class="view">
        <header class="view-header">
          <div class="eyebrow">$ opción 4</div>
          <h1 class="view-title">Empleado: descifrar credenciales con la llave privada</h1>
          <p class="view-copy">Solo la llave privada del empleado puede recuperar los datos originales.</p>
        </header>
        <div class="panel-grid">
          <section class="form-panel">
            <div class="card-header"><div><h2 class="card-title">Paso 4 - Empleado descifra credenciales</h2><p class="card-copy">Si ya existe credenciales_encriptadas.json, podés usar los datos guardados.</p></div></div>
            <div class="form-stack">
              ${TerminalTextarea({ id: 'cred-one-blocks', label: 'dato 1 cifrado', value: Array.isArray(packageData.data_one_encrypted) ? JSON.stringify(packageData.data_one_encrypted, null, 2) : '' })}
              ${TerminalTextarea({ id: 'cred-two-blocks', label: 'dato 2 cifrado', value: Array.isArray(packageData.data_two_encrypted) ? JSON.stringify(packageData.data_two_encrypted, null, 2) : '' })}
              ${TerminalInput({ id: 'private-n', label: 'valor n de la llave privada', type: 'number', value: privateKey.n || '' })}
              ${TerminalInput({ id: 'private-d', label: 'valor d de la llave privada', type: 'number', value: privateKey.d || '' })}
              <div class="button-row">
                ${CryptoButton('Descifrar credenciales con la llave privada', 'cred-decrypt-btn')}
                ${CryptoButton('Usar archivos guardados', 'cred-decrypt-saved-btn', 'ghost')}
              </div>
            </div>
          </section>
          <div id="cred-decrypt-result" class="result-slot">
            ${TerminalCard({ title: 'Credenciales descifradas', badge: 'esperando', lines: ['No existe credenciales_encriptadas.json; primero cifrá dos datos con la opción 3.'] })}
          </div>
        </div>
      </section>
    `;
  },

  init() {
    const button = document.getElementById('cred-decrypt-btn');
    const savedButton = document.getElementById('cred-decrypt-saved-btn');
    const slot = document.getElementById('cred-decrypt-result');

    button.addEventListener('click', async () => {
      await decrypt(false, button, slot);
    });
    savedButton.addEventListener('click', async () => {
      await decrypt(true, savedButton, slot);
    });
  },
};

async function decrypt(useSaved, button, slot) {
  try {
    setLoading(button, true, 'Descifrando');
    slot.innerHTML = LoadingSkeleton(4);
    const data = useSaved
      ? await api.terminalDecryptCredentials()
      : await api.terminalDecryptCredentials(
          parseBlocks(document.getElementById('cred-one-blocks').value),
          parseBlocks(document.getElementById('cred-two-blocks').value),
          privateKeyFromFields(),
        );
    slot.innerHTML = `
      ${TerminalBlocks(data.terminal)}
      <section class="terminal-card is-accent">
        <div class="card-header"><div><h2 class="card-title">Credenciales descifradas</h2></div></div>
        <pre class="terminal-output">Dato 1 original: ${escapeHtml(data.data_one)}\nDato 2 original: ${escapeHtml(data.data_two)}</pre>
      </section>
      ${ResultPanel('Credenciales descifradas', data, 'cred-decrypt-json')}
    `;
  } catch (error) {
    slot.innerHTML = Alert('error', error.message);
  } finally {
    setLoading(button, false);
  }
}
