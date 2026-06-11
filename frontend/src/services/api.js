const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5050/api';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok || data.success === false) {
    throw new Error(data.error || data.message || `Error HTTP ${response.status}`);
  }
  return data;
}

export const api = {
  baseUrl: API_BASE,

  health() {
    return request('/health');
  },

  generateKeys(bits = 16, persist = false) {
    return request('/keys/generate', {
      method: 'POST',
      body: JSON.stringify({ bits, persist }),
    });
  },

  terminalGenerateKeys(bits = 16) {
    return request('/terminal/generate-keys', {
      method: 'POST',
      body: JSON.stringify({ bits }),
    });
  },

  terminalShowPublicKey() {
    return request('/terminal/show-public-key');
  },

  terminalEncryptCredentials(dataOne, dataTwo, publicKey = null) {
    return request('/terminal/encrypt-credentials', {
      method: 'POST',
      body: JSON.stringify({ data_one: dataOne, data_two: dataTwo, public_key: publicKey }),
    });
  },

  terminalDecryptCredentials(encryptedOne = null, encryptedTwo = null, privateKey = null) {
    return request('/terminal/decrypt-credentials', {
      method: 'POST',
      body: JSON.stringify({ data_one_encrypted: encryptedOne, data_two_encrypted: encryptedTwo, private_key: privateKey }),
    });
  },

  terminalTextCandidates(text, p, q) {
    return request('/terminal/text-candidates', {
      method: 'POST',
      body: JSON.stringify({ text, p, q }),
    });
  },

  terminalEncryptTextStep(text, p, q, d, e = null) {
    return request('/terminal/encrypt-text-step', {
      method: 'POST',
      body: JSON.stringify({ text, p, q, d, e }),
    });
  },

  terminalDecryptTxt(packageData = null) {
    return request('/terminal/decrypt-txt', {
      method: 'POST',
      body: JSON.stringify({ package: packageData }),
    });
  },

  keysFromPrimes(p, q, d = null, e = null) {
    return request('/keys/from-primes', {
      method: 'POST',
      body: JSON.stringify({ p, q, d, e }),
    });
  },

  encrypt(text, publicKey) {
    return request('/encrypt', {
      method: 'POST',
      body: JSON.stringify({ text, public_key: publicKey }),
    });
  },

  decrypt(blocks, privateKey) {
    return request('/decrypt', {
      method: 'POST',
      body: JSON.stringify({ encrypted_blocks: blocks, private_key: privateKey }),
    });
  },

  encryptCredentials(dataOne, dataTwo, publicKey) {
    return request('/credentials/encrypt', {
      method: 'POST',
      body: JSON.stringify({ data_one: dataOne, data_two: dataTwo, public_key: publicKey }),
    });
  },

  decryptCredentials(encryptedOne, encryptedTwo, privateKey) {
    return request('/credentials/decrypt', {
      method: 'POST',
      body: JSON.stringify({
        data_one_encrypted: encryptedOne,
        data_two_encrypted: encryptedTwo,
        private_key: privateKey,
      }),
    });
  },

  verifyKeys(publicKey, privateKey, testMessage = 'prueba') {
    return request('/verify', {
      method: 'POST',
      body: JSON.stringify({ public_key: publicKey, private_key: privateKey, test_message: testMessage }),
    });
  },
};
