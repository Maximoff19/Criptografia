export function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

export function formatJson(value) {
  return JSON.stringify(value, null, 2);
}

export function summarizeBlocks(blocks, limit = 8) {
  if (!Array.isArray(blocks)) return '[]';
  if (blocks.length <= limit) return `[${blocks.join(', ')}]`;
  return `[${blocks.slice(0, limit).join(', ')}, ...] total=${blocks.length}`;
}

export function parseBlocks(raw) {
  const text = String(raw || '').trim();
  if (!text) throw new Error('Debes ingresar bloques cifrados.');

  try {
    const parsed = JSON.parse(text);
    if (Array.isArray(parsed)) return parsed.map((value) => Number.parseInt(value, 10));
  } catch {
    // Fall through to comma/newline parser.
  }

  return text
    .split(/[\s,]+/)
    .filter(Boolean)
    .map((value) => {
      const number = Number.parseInt(value, 10);
      if (Number.isNaN(number)) throw new Error(`Bloque invalido: ${value}`);
      return number;
    });
}

export function storageSet(key, value) {
  sessionStorage.setItem(key, JSON.stringify(value));
}

export function storageGet(key) {
  const value = sessionStorage.getItem(key);
  if (!value) return null;
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

export async function copyText(value) {
  await navigator.clipboard.writeText(typeof value === 'string' ? value : formatJson(value));
}

export function downloadJson(filename, value) {
  const blob = new Blob([formatJson(value)], { type: 'application/json;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}
