import { escapeHtml } from '../utils/formatters.js';

export function StatusBadge(label, variant = 'default') {
  const className = variant === 'warning' ? ' is-warning' : variant === 'error' ? ' is-error' : '';
  return `<span class="status-badge${className}">${escapeHtml(label)}</span>`;
}
