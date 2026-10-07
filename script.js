// Mobile menu
const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-nav');
toggle.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  toggle.setAttribute('aria-expanded', open);
});
nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  nav.classList.remove('open');
  toggle.setAttribute('aria-expanded', false);
}));

// Footer year
document.getElementById('year').textContent = new Date().getFullYear();

// Offer form -> opens an email with the request details
// (αλλάξτε το email παρακάτω με το πραγματικό email του καταστήματος)
const OFFER_EMAIL = 'info@zervos-epipla.gr';
document.getElementById('offerForm').addEventListener('submit', e => {
  e.preventDefault();
  const f = new FormData(e.target);
  const body =
    `Ονοματεπώνυμο: ${f.get('name')}\n` +
    `Τηλέφωνο: ${f.get('phone')}\n` +
    `Email: ${f.get('email')}\n` +
    `Κατηγορία: ${f.get('category')}\n\n` +
    `${f.get('message')}`;
  const subject = `Αίτημα προσφοράς - ${f.get('category')}`;
  window.location.href =
    `mailto:${OFFER_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
});
