import { escapeHtml } from '../utils/formatters.js';

export function Alert(title, message, variant = 'error') {
  const className = variant === 'success' ? 'alert is-success' : 'alert';
  return `
    <div class="${className}" role="alert">
      <div class="alert-title">${escapeHtml(title)}</div>
      <div class="alert-copy">${escapeHtml(message)}</div>
    </div>
  `;
}
