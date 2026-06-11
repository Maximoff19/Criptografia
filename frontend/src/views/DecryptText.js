import { Alert } from '../components/Alert.js';
import { CryptoButton } from '../components/CryptoButton.js';
import { LoadingSkeleton } from '../components/LoadingSkeleton.js';
import { ResultPanel } from '../components/ResultPanel.js';
import { TerminalCard } from '../components/TerminalCard.js';
import { TerminalBlocks } from '../components/TerminalBlocks.js';
import { TerminalTextarea } from '../components/TerminalInput.js';
import { api } from '../services/api.js';
import { escapeHtml, storageGet } from '../utils/formatters.js';
import { setLoading } from '../utils/validators.js';

export const DecryptText = {
  render() {
    const txtPackage = storageGet('rsa.lastTxtPackage');
    return `
      <section class="view">
        <header class="view-header">
          <div class="eyebrow">$ opción 6</div>
          <h1 class="view-title">Desencriptar mensaje desde archivo TXT</h1>
          <p class="view-copy">El archivo debe contener mensaje_encriptado y clave_privada_para_descifrar.</p>
        </header>
        <div class="panel-grid">
          <section class="form-panel">
            <div class="form-stack">
              <div class="field">
                <label for="txt-file">$ ruta del TXT [mensaje_encriptado.txt] &gt;</label>
                <input class="input" id="txt-file" type="file" accept=".txt,.json,application/json,text/plain" />
              </div>
              ${TerminalTextarea({ id: 'txt-package', label: 'contenido del TXT', value: txtPackage ? JSON.stringify(txtPackage, null, 2) : '', placeholder: '{ "mensaje_encriptado": [...], "clave_privada_para_descifrar": {...} }' })}
              <div class="button-row">
                ${CryptoButton('Desencriptar TXT', 'txt-decrypt-btn')}
                ${CryptoButton('Usar mensaje_encriptado.txt guardado', 'txt-decrypt-saved-btn', 'ghost')}
              </div>
            </div>
          </section>
          <div id="txt-decrypt-result" class="result-slot">
            ${TerminalCard({ title: 'Desencriptar archivo TXT', badge: 'esperando', lines: ['El archivo debe contener mensaje_encriptado y clave_privada_para_descifrar.'] })}
          </div>
        </div>
      </section>
    `;
  },

  init() {
    const fileInput = document.getElementById('txt-file');
    const textarea = document.getElementById('txt-package');
    const button = document.getElementById('txt-decrypt-btn');
    const savedButton = document.getElementById('txt-decrypt-saved-btn');
    const slot = document.getElementById('txt-decrypt-result');

    fileInput.addEventListener('change', async () => {
      const file = fileInput.files?.[0];
      if (!file) return;
      textarea.value = await file.text();
    });

    button.addEventListener('click', async () => {
      await decrypt(false, button, slot, textarea);
    });
    savedButton.addEventListener('click', async () => {
      await decrypt(true, savedButton, slot, textarea);
    });
  },
};

async function decrypt(useSaved, button, slot, textarea) {
  try {
    setLoading(button, true, 'Desencriptando');
    slot.innerHTML = LoadingSkeleton(4);
    let packageData = null;
    if (!useSaved) {
      const raw = textarea.value.trim();
      if (!raw) throw new Error('El archivo debe contener mensaje_encriptado y clave_privada_para_descifrar.');
      packageData = JSON.parse(raw);
    }
    const data = await api.terminalDecryptTxt(packageData);
    slot.innerHTML = `
      ${TerminalBlocks(data.terminal)}
      <section class="terminal-card is-accent">
        <div class="card-header"><div><h2 class="card-title">Texto desencriptado</h2></div></div>
        <pre class="terminal-output">${escapeHtml(data.decrypted_text)}</pre>
      </section>
      ${ResultPanel('Texto desencriptado', data, 'txt-decrypt-json')}
    `;
  } catch (error) {
    slot.innerHTML = Alert('error', error.message);
  } finally {
    setLoading(button, false);
  }
}
