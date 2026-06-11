import './styles/tokens.css';
import './styles/reset.css';
import './styles/base.css';
import './styles/components.css';
import './styles/pages.css';

import { NavSidebar } from './components/NavSidebar.js';
import { Alert } from './components/Alert.js';
import { copyText } from './utils/formatters.js';
import { currentRoute, onRouteChange } from './router.js';
import { Dashboard } from './views/Dashboard.js';
import { GenerateKeys } from './views/GenerateKeys.js';
import { PublicKey } from './views/PublicKey.js';
import { ManualKeys } from './views/ManualKeys.js';
import { DecryptText } from './views/DecryptText.js';
import { EncryptCredentials } from './views/EncryptCredentials.js';
import { DecryptCredentials } from './views/DecryptCredentials.js';
import { Help } from './views/Help.js';

const routes = {
  '/': Dashboard,
  '/keys/generate': GenerateKeys,
  '/public-key': PublicKey,
  '/credentials/encrypt': EncryptCredentials,
  '/credentials/decrypt': DecryptCredentials,
  '/text/encrypt': ManualKeys,
  '/text/decrypt': DecryptText,
  '/help': Help,
};

const root = document.getElementById('app');

function render(route) {
  const activeRoute = routes[route] ? route : '/';
  const view = routes[activeRoute];
  root.innerHTML = `
    <div class="app-shell">
      ${NavSidebar(activeRoute)}
      <main class="main-panel" id="main-panel"></main>
    </div>
  `;

  const main = document.getElementById('main-panel');
  try {
    main.innerHTML = view.render();
    view.init?.();
  } catch (error) {
    main.innerHTML = Alert('error de vista', error.message);
  }
}

document.addEventListener('click', async (event) => {
  const button = event.target.closest('[data-copy-id]');
  if (!button) return;
  const target = document.getElementById(button.dataset.copyId);
  if (!target) return;
  await copyText(target.textContent || '');
  const previous = button.textContent;
  button.textContent = 'Copiado';
  window.setTimeout(() => {
    button.textContent = previous;
  }, 900);
});

onRouteChange(render);

if (!window.location.hash) {
  window.history.replaceState(null, '', `#${currentRoute()}`);
}
