import { escapeHtml, formatJson, summarizeBlocks } from '../utils/formatters.js';

export function BlockViewer(title, blocks, id = 'blocks-viewer') {
  if (!Array.isArray(blocks)) return '';
  return `
    <div class="terminal-card">
      <div class="card-header">
        <div>
          <h3 class="card-title">${escapeHtml(title)}</h3>
          <p class="card-copy">${escapeHtml(summarizeBlocks(blocks))}</p>
        </div>
        <button class="copy-button" data-copy-id="${escapeHtml(id)}">Copiar</button>
      </div>
      <pre id="${escapeHtml(id)}" class="block-viewer">${escapeHtml(formatJson(blocks))}</pre>
    </div>
  `;
}
