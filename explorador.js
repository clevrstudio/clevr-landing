(() => {
  const root = document.getElementById('explorar-soluciones');
  if (!root) return;
  const tabs = [...root.querySelectorAll('[role="tab"]')];
  const panels = root.querySelector('.explore-panel-wrap');
  function select(tab, focus = false) {
    for (const item of tabs) {
      const active = item === tab;
      item.setAttribute('aria-selected', String(active));
      item.tabIndex = active || (!tab && item === tabs[0]) ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !active;
    }
    panels.hidden = !tab;
    if (focus) tab.focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => select(tab.getAttribute('aria-selected') === 'true' ? null : tab));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); select(tabs[next], true); }
    });
  });
  root.addEventListener('click', event => {
    if (panels.hidden || event.target.closest('.explore-tab, .explore-panel, a')) return;
    select(null);
  });
  root.addEventListener('keydown', event => {
    if (event.key !== 'Escape' || panels.hidden) return;
    const active = tabs.find(tab => tab.getAttribute('aria-selected') === 'true');
    select(null);
    active?.focus();
  });
  // Keep the open panel while it is being read. Reset once the entire section
  // leaves the viewport, so returning visitors see the unselected circles.
  const observer = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting || panels.hidden) return;
    const exitedAbove = root.getBoundingClientRect().bottom < 0;
    const previousHeight = root.offsetHeight;
    select(null);
    if (exitedAbove) window.scrollBy(0, root.offsetHeight - previousHeight);
  });
  observer.observe(root);
})();
