import { escapeHtml } from '../utils/formatters.js';

export function TerminalBlocks(blocks = []) {
  if (!Array.isArray(blocks) || blocks.length === 0) return '';
  return blocks
    .map((block) => {
      const lines = Array.isArray(block.lines) ? block.lines : [];
      return `
        <section class="terminal-card${block.title?.includes('ADVERTENCIA') ? ' warning-card' : ''}">
          <div class="card-header">
            <div><h2 class="card-title">${escapeHtml(block.title || '')}</h2></div>
          </div>
          <div class="terminal-output no-prompt">
            ${lines.map((line) => `<div class="line">${escapeHtml(line)}</div>`).join('')}
          </div>
        </section>
      `;
    })
    .join('');
}
