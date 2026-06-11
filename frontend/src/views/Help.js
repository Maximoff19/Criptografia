import { TerminalCard } from '../components/TerminalCard.js';

export const Help = {
  render() {
    return `
      <section class="view">
        <header class="view-header">
          <div class="eyebrow">$ opción 7</div>
          <h1 class="view-title">Ayuda - RSA paso a paso</h1>
          <p class="view-copy">Explicación rápida de RSA desde el menú.</p>
        </header>
        <div class="help-grid">
          ${TerminalCard({ title: '1. Se eligen dos primos distintos p y q.', badge: 'p q', lines: ['Los primos son la base del cálculo RSA.'] })}
          ${TerminalCard({ title: '2. Se calcula n = p * q.', badge: 'n', lines: ['n será el módulo usado para cifrar y descifrar.'] })}
          ${TerminalCard({ title: '3. Se calcula phi(n) = (p - 1)(q - 1).', badge: 'phi', lines: ['phi(n) se usa para elegir d y calcular e.'] })}
          ${TerminalCard({ title: '4. Se elige d menor que phi(n) con MCD(d, phi(n)) = 1.', badge: 'd', lines: ['d forma parte de la clave privada.'] })}
          ${TerminalCard({ title: '5. Se calcula e para que e*d sea congruente con 1 módulo phi(n).', badge: 'e', lines: ['e forma parte de la clave pública.'] })}
          ${TerminalCard({ title: '6. El jefe cifra con la pública (n, e): C = M^e mod n.', badge: 'cifrar', lines: ['La clave pública puede compartirse.'] })}
          ${TerminalCard({ title: '7. El empleado descifra con la privada (n, d): M = C^d mod n.', badge: 'descifrar', lines: ['La clave privada no se comparte.'] })}
        </div>
        ${TerminalCard({
          title: 'Advertencia',
          badge: 'warning',
          lines: ['No compartas llave_privada_empleado.json. Si lo hacés, la seguridad se cae.', 'Esto es una implementación académica para aprender aritmética modular y RSA.'],
        })}
      </section>
    `;
  },
};
