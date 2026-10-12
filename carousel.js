// Simple swipe/scroll carousel with arrows, counter and thumbnails
document.querySelectorAll('.carousel').forEach(carousel => {
  const track = carousel.querySelector('.carousel-track');
  const slides = [...track.children];
  const cur = carousel.querySelector('.cur');
  const thumbs = [...(carousel.nextElementSibling?.querySelectorAll('.carousel-thumb') || [])];
  let index = 0;

  const goTo = i => {
    index = (i + slides.length) % slides.length;
    track.scrollTo({ left: slides[index].offsetLeft, behavior: 'smooth' });
  };
  const update = () => {
    index = Math.round(track.scrollLeft / track.clientWidth);
    cur.textContent = index + 1;
    thumbs.forEach((t, i) => t.classList.toggle('active', i === index));
  };

  carousel.querySelector('.prev').addEventListener('click', () => goTo(index - 1));
  carousel.querySelector('.next').addEventListener('click', () => goTo(index + 1));
  thumbs.forEach((t, i) => t.addEventListener('click', () => goTo(i)));
  track.addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
  track.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(index - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); goTo(index + 1); }
  });
  update();
});
