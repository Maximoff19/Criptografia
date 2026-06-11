import { Alert } from '../components/Alert.js';
import { BlockViewer } from '../components/BlockViewer.js';
import { CryptoButton } from '../components/CryptoButton.js';
import { LoadingSkeleton } from '../components/LoadingSkeleton.js';
import { ResultPanel } from '../components/ResultPanel.js';
import { TerminalCard } from '../components/TerminalCard.js';
import { TerminalBlocks } from '../components/TerminalBlocks.js';
import { TerminalInput } from '../components/TerminalInput.js';
import { api } from '../services/api.js';
import { storageGet, storageSet } from '../utils/formatters.js';
import { intValue, setLoading, textValue } from '../utils/validators.js';

export const EncryptCredentials = {
  render() {
    const publicKey = storageGet('rsa.publicKey') || {};
    return `
      <section class="view">
        <header class="view-header">
          <div class="eyebrow">$ opción 3</div>
          <h1 class="view-title">Jefe: cifrar dos credenciales con la llave pública</h1>
          <p class="view-copy">Usá la llave pública del empleado. La contraseña se escribe oculta para evitar exposición visual.</p>
        </header>
        <div class="panel-grid">
          <section class="form-panel">
            <div class="card-header"><div><h2 class="card-title">Paso 3 - Jefe cifra credenciales</h2><p class="card-copy">El resultado se guarda en credenciales_encriptadas.json para devolverlo al empleado.</p></div></div>
            <div class="form-stack">
              ${TerminalInput({ id: 'cred-one', label: 'usuario o identificador a cifrar', placeholder: 'usuario o identificador' })}
              ${TerminalInput({ id: 'cred-two', label: 'contraseña o segundo dato sensible a cifrar', type: 'password', placeholder: 'contraseña o secreto' })}
              ${TerminalInput({ id: 'public-n', label: 'valor n de la llave pública', type: 'number', value: publicKey.n || '' })}
              ${TerminalInput({ id: 'public-e', label: 'valor e de la llave pública', type: 'number', value: publicKey.e || '' })}
              <div class="button-row">${CryptoButton('Cifrar dos credenciales con la llave pública', 'cred-encrypt-btn')}</div>
            </div>
          </section>
          <div id="cred-encrypt-result" class="result-slot">
            ${TerminalCard({ title: 'Credenciales cifradas correctamente', badge: 'esperando', lines: ['El resultado se guarda en credenciales_encriptadas.json para devolverlo al empleado.'] })}
          </div>
        </div>
      </section>
    `;
  },

  init() {
    const button = document.getElementById('cred-encrypt-btn');
    const slot = document.getElementById('cred-encrypt-result');
    button.addEventListener('click', async () => {
      try {
        setLoading(button, true, 'Cifrando');
        slot.innerHTML = LoadingSkeleton(5);
        const publicKey = optionalPublicKey();
        const data = await api.terminalEncryptCredentials(textValue('cred-one', 'primer dato'), textValue('cred-two', 'segundo dato'), publicKey);
        storageSet('rsa.credentialsPackage', data);
        slot.innerHTML = `
          ${TerminalBlocks(data.terminal)}
          <div class="key-grid">${BlockViewer('Dato 1 cifrado', data.data_one_encrypted, 'cred-one-encrypted')}${BlockViewer('Dato 2 cifrado', data.data_two_encrypted, 'cred-two-encrypted')}</div>
          ${ResultPanel('Credenciales cifradas correctamente', data, 'cred-encrypt-json')}
        `;
      } catch (error) {
        slot.innerHTML = Alert('error', error.message);
      } finally {
        setLoading(button, false);
      }
    });
  },
};

function optionalPublicKey() {
  const n = document.getElementById('public-n').value.trim();
  const e = document.getElementById('public-e').value.trim();
  if (n === '' && e === '') return null;
  return { n: intValue('public-n', 'n'), e: intValue('public-e', 'e') };
}
