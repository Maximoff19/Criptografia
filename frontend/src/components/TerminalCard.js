import { escapeHtml } from '../utils/formatters.js';
import { StatusBadge } from './StatusBadge.js';

export function TerminalCard({ title, copy = '', badge = '', lines = [], accent = false, body = '' }) {
  const output = lines.length
    ? `<div class="terminal-output">${lines.map((line) => `<div class="line">${escapeHtml(line)}</div>`).join('')}</div>`
    : '';
  return `
    <section class="terminal-card${accent ? ' is-accent' : ''}">
      <div class="card-header">
        <div>
          <h2 class="card-title">${escapeHtml(title)}</h2>
          ${copy ? `<p class="card-copy">${escapeHtml(copy)}</p>` : ''}
        </div>
        ${badge ? StatusBadge(badge) : ''}
      </div>
      ${body}
      ${output}
    </section>
  `;
}
