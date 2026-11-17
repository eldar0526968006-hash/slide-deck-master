// Shared deck engine: fixed 1920x1080 stage, keyboard/click nav, notes panel (N), hash routing.
(function () {
  const stage = document.querySelector('.deck-stage');
  const slides = [...document.querySelectorAll('.slide')];
  const notes = document.querySelector('.notes-panel');
  const counter = document.querySelector('.deck-count');
  let i = Math.max(0, Math.min(slides.length - 1, (parseInt(location.hash.slice(1), 10) || 1) - 1));

  function fit() {
    const s = Math.min(innerWidth / 1920, innerHeight / 1080);
    stage.style.transform = `translate(${(innerWidth - 1920 * s) / 2}px, ${(innerHeight - 1080 * s) / 2}px) scale(${s})`;
  }
  function show(n) {
    i = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach((el, k) => el.classList.toggle('active', k === i));
    history.replaceState(null, '', '#' + (i + 1));
    if (counter) counter.textContent = `${i + 1} / ${slides.length}`;
    const a = slides[i].querySelector('aside.notes');
    if (notes) notes.innerHTML = a ? a.innerHTML : '';
  }
  addEventListener('resize', fit);
  addEventListener('keydown', (e) => {
    if (['ArrowLeft', 'ArrowDown', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); show(i + 1); } // RTL: left = forward
    else if (['ArrowRight', 'ArrowUp', 'PageUp'].includes(e.key)) { e.preventDefault(); show(i - 1); }
    else if (e.key === 'Home') show(0);
    else if (e.key === 'End') show(slides.length - 1);
    else if (e.key.toLowerCase() === 'n' && notes) notes.classList.toggle('open');
  });
  document.querySelector('.deck-viewport').addEventListener('click', (e) => {
    if (e.target.closest('a,button,.notes-panel')) return;
    show(e.clientX < innerWidth / 2 ? i + 1 : i - 1);
  });
  fit(); show(i);
})();
