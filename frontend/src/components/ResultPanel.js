import { escapeHtml, formatJson } from '../utils/formatters.js';

export function ResultPanel(title, value, id = 'result-json') {
  return `
    <section class="result-panel">
      <div class="card-header">
        <div>
          <h2 class="card-title">${escapeHtml(title)}</h2>
          <p class="card-copy">Datos completos de la operación.</p>
        </div>
        <button class="copy-button" data-copy-id="${escapeHtml(id)}">Copiar</button>
      </div>
      <pre id="${escapeHtml(id)}" class="code-box">${escapeHtml(formatJson(value))}</pre>
    </section>
  `;
}
