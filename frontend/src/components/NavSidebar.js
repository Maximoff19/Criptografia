import { escapeHtml } from '../utils/formatters.js';

const navItems = [
  ['/', '00', 'Menú'],
  ['/keys/generate', '01', 'Generar llaves'],
  ['/public-key', '02', 'Mostrar pública'],
  ['/credentials/encrypt', '03', 'Cifrar credenciales'],
  ['/credentials/decrypt', '04', 'Descifrar credenciales'],
  ['/text/encrypt', '05', 'Texto paso a paso'],
  ['/text/decrypt', '06', 'Desencriptar TXT'],
  ['/help', '07', 'Ayuda RSA'],
];

function lockIcon() {
  return `
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <rect x="5" y="11" width="14" height="10" rx="2" stroke="#00FF62" stroke-width="1.6"/>
      <path d="M8 11V7a4 4 0 0 1 8 0v4" stroke="#00FF62" stroke-width="1.6" stroke-linecap="round"/>
      <circle cx="12" cy="16" r="1" fill="#00FF62"/>
    </svg>
  `;
}

export function NavSidebar(activeRoute) {
  return `
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">${lockIcon()}</div>
        <div>
          <div class="brand-title">Criptografía RSA</div>
          <div class="brand-subtitle">Flujo empleado/jefe y texto RSA paso a paso</div>
        </div>
      </div>
      <nav class="nav-list" aria-label="Principal">
        ${navItems
          .map(([route, index, label]) => {
            const active = route === activeRoute ? ' is-active' : '';
            return `<a href="#${escapeHtml(route)}" class="nav-link${active}" data-route="${escapeHtml(route)}"><span class="nav-index">${escapeHtml(index)}</span><span>${escapeHtml(label)}</span></a>`;
          })
          .join('')}
      </nav>
      <div class="sidebar-footer">No compartas la llave privada. Si lo hacés, la seguridad se cae.</div>
    </aside>
  `;
}
