export function LoadingSkeleton(lines = 4) {
  return `
    <div class="terminal-card">
      ${Array.from({ length: lines }, (_, index) => `<div class="skeleton" style="width:${90 - index * 12}%; margin-bottom:12px"></div>`).join('')}
    </div>
  `;
}
