export function intValue(id, label) {
  const input = document.getElementById(id);
  const value = Number.parseInt(input?.value ?? '', 10);
  if (Number.isNaN(value)) throw new Error(`${label} debe ser un numero entero.`);
  return value;
}

export function textValue(id, label) {
  const input = document.getElementById(id);
  const value = input?.value?.trim() ?? '';
  if (!value) throw new Error(`${label} no puede estar vacio.`);
  return value;
}

export function textAreaValue(id, label) {
  return textValue(id, label);
}

export function publicKeyFromFields(nId = 'public-n', eId = 'public-e') {
  return { n: intValue(nId, 'n'), e: intValue(eId, 'e') };
}

export function privateKeyFromFields(nId = 'private-n', dId = 'private-d') {
  return { n: intValue(nId, 'n'), d: intValue(dId, 'd') };
}

export function setLoading(button, isLoading, label = 'Procesando') {
  if (!button) return;
  button.disabled = isLoading;
  if (isLoading) {
    button.dataset.originalLabel = button.textContent;
    button.textContent = label;
  } else if (button.dataset.originalLabel) {
    button.textContent = button.dataset.originalLabel;
    delete button.dataset.originalLabel;
  }
}
