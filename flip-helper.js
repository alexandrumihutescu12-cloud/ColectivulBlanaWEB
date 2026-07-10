function flipFilter(container, cardSelector, matchFn) {
  const cards = container.querySelectorAll(cardSelector);
  const firstRects = new Map();

  cards.forEach(card => {
    firstRects.set(card, card.getBoundingClientRect());
  });

  cards.forEach(card => {
    const matches = matchFn(card);
    card.classList.toggle('search-hidden', !matches);
  });

  requestAnimationFrame(() => {
    cards.forEach(card => {
      if (card.classList.contains('search-hidden')) return;

      const first = firstRects.get(card);
      const last = card.getBoundingClientRect();
      const deltaX = first.left - last.left;
      const deltaY = first.top - last.top;

      if (deltaX || deltaY) {
        card.style.transition = 'none';
        card.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(1)`;
        requestAnimationFrame(() => {
          card.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
          card.style.transform = '';
        });
      }
    });
  });
}