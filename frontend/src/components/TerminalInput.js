import { escapeHtml } from '../utils/formatters.js';

export function TerminalInput({ id, label, type = 'text', value = '', placeholder = '', min = null }) {
  const minAttr = min === null ? '' : ` min="${escapeHtml(min)}"`;
  return `
    <div class="field">
      <label for="${escapeHtml(id)}">$ ${escapeHtml(label)} &gt;</label>
      <input class="input" id="${escapeHtml(id)}" type="${escapeHtml(type)}" value="${escapeHtml(value)}" placeholder="${escapeHtml(placeholder)}"${minAttr} />
    </div>
  `;
}

export function TerminalTextarea({ id, label, value = '', placeholder = '', rows = 6 }) {
  return `
    <div class="field">
      <label for="${escapeHtml(id)}">$ ${escapeHtml(label)} &gt;</label>
      <textarea class="textarea" id="${escapeHtml(id)}" rows="${escapeHtml(rows)}" placeholder="${escapeHtml(placeholder)}">${escapeHtml(value)}</textarea>
    </div>
  `;
}
