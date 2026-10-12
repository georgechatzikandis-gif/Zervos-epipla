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
const offerForm = document.getElementById('offerForm');

// Prefill the offer form from links like index.html?cat=...&product=...#offer
if (offerForm) {
  const params = new URLSearchParams(location.search);
  const cat = params.get('cat');
  const product = params.get('product');
  if (cat) {
    const opt = [...offerForm.category.options].find(o => o.value === cat);
    if (opt) offerForm.category.value = cat;
  }
  if (product) offerForm.message.value = `Ενδιαφέρομαι για: ${product}`;
}

offerForm?.addEventListener('submit', e => {
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
