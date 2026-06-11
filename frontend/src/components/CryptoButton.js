import { escapeHtml } from '../utils/formatters.js';

export function CryptoButton(label, id, variant = 'primary', attrs = '') {
  const className = variant === 'ghost' ? 'ghost-button' : 'crypto-button';
  return `<button id="${escapeHtml(id)}" class="${className}" ${attrs}>${escapeHtml(label)}</button>`;
}
