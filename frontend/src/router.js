export function currentRoute() {
  const route = window.location.hash.replace(/^#/, '');
  return route || '/';
}

export function navigate(route) {
  window.location.hash = route;
}

export function onRouteChange(callback) {
  window.addEventListener('hashchange', () => callback(currentRoute()));
  callback(currentRoute());
}
