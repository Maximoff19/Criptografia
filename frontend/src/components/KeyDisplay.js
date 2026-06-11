import { escapeHtml } from '../utils/formatters.js';

export function KeyDisplay(title, keyData, type = 'public') {
  if (!keyData) return '';
  const exponentLabel = type === 'private' ? 'd' : 'e';
  const exponentValue = keyData[exponentLabel];
  return `
    <div class="terminal-card">
      <div class="card-header">
        <div>
          <h3 class="card-title">${escapeHtml(title)}</h3>
          <p class="card-copy">Clave ${escapeHtml(type)} en formato n/${escapeHtml(exponentLabel)}.</p>
        </div>
      </div>
      <div class="key-grid">
        <div class="key-value"><span>n</span><code>${escapeHtml(keyData.n)}</code></div>
        <div class="key-value"><span>${escapeHtml(exponentLabel)}</span><code>${escapeHtml(exponentValue)}</code></div>
      </div>
    </div>
  `;
}
