import { Alert } from '../components/Alert.js';
import { BlockViewer } from '../components/BlockViewer.js';
import { CryptoButton } from '../components/CryptoButton.js';
import { LoadingSkeleton } from '../components/LoadingSkeleton.js';
import { ResultPanel } from '../components/ResultPanel.js';
import { TerminalCard } from '../components/TerminalCard.js';
import { TerminalBlocks } from '../components/TerminalBlocks.js';
import { TerminalInput, TerminalTextarea } from '../components/TerminalInput.js';
import { api } from '../services/api.js';
import { downloadJson, storageSet } from '../utils/formatters.js';
import { intValue, setLoading, textAreaValue } from '../utils/validators.js';

let candidates = [];

export const ManualKeys = {
  render() {
    return `
      <section class="view">
        <header class="view-header">
          <div class="eyebrow">$ opción 5</div>
          <h1 class="view-title">Encriptar texto con p y q manuales</h1>
          <p class="view-copy">Ingresá texto, dos primos p y q, y seleccioná d/e viendo el proceso completo.</p>
        </header>
        <div class="panel-grid">
          <section class="form-panel manual-flow">
            <div class="form-stack">
              ${TerminalTextarea({ id: 'manual-text', label: 'texto o cadena a encriptar', placeholder: 'Texto a encriptar' })}
              ${TerminalInput({ id: 'manual-p', label: 'ingresá p, primo de una o dos cifras', type: 'number', placeholder: '17', min: 2 })}
              ${TerminalInput({ id: 'manual-q', label: 'ingresá q, primo de una o dos cifras', type: 'number', placeholder: '19', min: 2 })}
              <div class="button-row">${CryptoButton('Calcular candidatos d', 'candidate-btn', 'ghost')}</div>
              <div class="field">
                <label for="manual-d">$ seleccioná un valor d de la lista &gt;</label>
                <select id="manual-d" class="select"><option value="">Primero calculá candidatos d</option></select>
              </div>
              ${TerminalInput({ id: 'manual-e', label: 'ingresá un e que cumpla e*d ≡ 1 mod phi(n)', type: 'number', placeholder: 'Vacío usa e base' })}
              <div class="button-row">${CryptoButton('Encriptar y guardar TXT', 'manual-encrypt-btn')}</div>
            </div>
          </section>
          <div id="manual-result" class="result-slot">
            ${TerminalCard({ title: 'Encriptar texto con RSA', badge: 'manual', lines: ['Ingresá texto, dos primos p y q, y seleccioná d/e viendo el proceso completo.'] })}
          </div>
        </div>
      </section>
    `;
  },

  init() {
    const candidateButton = document.getElementById('candidate-btn');
    const encryptButton = document.getElementById('manual-encrypt-btn');
    const select = document.getElementById('manual-d');
    const slot = document.getElementById('manual-result');

    candidateButton.addEventListener('click', async () => {
      try {
        setLoading(candidateButton, true, 'Calculando');
        slot.innerHTML = LoadingSkeleton(4);
        const text = textAreaValue('manual-text', 'texto a encriptar');
        const p = intValue('manual-p', 'p');
        const q = intValue('manual-q', 'q');
        const data = await api.terminalTextCandidates(text, p, q);
        candidates = data.possible_d;
        select.innerHTML = candidates.map((value) => `<option value="${value}">${value}</option>`).join('');
        slot.innerHTML = TerminalBlocks(data.terminal);
      } catch (error) {
        slot.innerHTML = Alert('error', error.message);
      } finally {
        setLoading(candidateButton, false);
      }
    });

    encryptButton.addEventListener('click', async () => {
      try {
        setLoading(encryptButton, true, 'Encriptando');
        slot.innerHTML = LoadingSkeleton(6);
        const text = textAreaValue('manual-text', 'texto a encriptar');
        const p = intValue('manual-p', 'p');
        const q = intValue('manual-q', 'q');
        const d = Number.parseInt(select.value, 10);
        if (Number.isNaN(d)) throw new Error('Ese d no está permitido porque no cumple MCD(d, phi(n)) = 1.');
        const rawE = document.getElementById('manual-e').value.trim();
        const e = rawE === '' ? null : Number.parseInt(rawE, 10);
        const data = await api.terminalEncryptTextStep(text, p, q, d, e);
        storageSet('rsa.lastEncryptedBlocks', data.encrypted_blocks);
        storageSet('rsa.lastTxtPackage', data.txt_package);
        slot.innerHTML = `
          ${TerminalBlocks(data.terminal)}
          ${BlockViewer('Mensaje encriptado en bloques', data.encrypted_blocks, 'manual-encrypted-blocks')}
          ${ResultPanel('mensaje_encriptado.txt', data.txt_package, 'txt-package-json')}
          <div class="button-row"><button class="ghost-button" id="download-txt-json">Descargar mensaje_encriptado.txt</button></div>
        `;
        document.getElementById('download-txt-json').addEventListener('click', () => downloadJson('mensaje_encriptado.txt', data.txt_package));
      } catch (error) {
        slot.innerHTML = Alert('error', error.message);
      } finally {
        setLoading(encryptButton, false);
      }
    });
  },
};
