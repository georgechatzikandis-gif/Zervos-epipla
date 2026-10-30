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
const OFFER_EMAIL = 'zervosinhouse@gmail.com';
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

// Opening hours: live open/closed status in Greek time (Europe/Athens)
const hoursStatus = document.getElementById('hoursStatus');
if (hoursStatus) {
  // minutes from midnight; 0 = Sunday ... 6 = Saturday
  const morning = [9 * 60 + 30, 13 * 60];
  const evening = [17 * 60, 20 * 60 + 30];
  const HOURS = { 0: [], 1: [morning, evening], 2: [morning, evening], 3: [morning, evening],
                  4: [morning, evening], 5: [morning, evening], 6: [morning] };
  const ON_DAY = ['την Κυριακή', 'τη Δευτέρα', 'την Τρίτη', 'την Τετάρτη', 'την Πέμπτη', 'την Παρασκευή', 'το Σάββατο'];
  const WEEKDAYS = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
  const fmt = m => `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
  const textEl = hoursStatus.querySelector('.hours-status-text');

  const athensNow = () => {
    const parts = Object.fromEntries(new Intl.DateTimeFormat('en-GB', {
      timeZone: 'Europe/Athens', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
    }).formatToParts(new Date()).map(p => [p.type, p.value]));
    return { day: WEEKDAYS[parts.weekday], minutes: Number(parts.hour) * 60 + Number(parts.minute) };
  };

  const nextOpening = (day, minutes) => {
    for (let offset = 0; offset < 8; offset++) {
      const d = (day + offset) % 7;
      const slot = HOURS[d].find(([start]) => offset > 0 || start > minutes);
      if (slot) {
        const when = offset === 0 ? 'σήμερα' : offset === 1 ? 'αύριο' : ON_DAY[d];
        return `ανοίγει ${when} στις ${fmt(slot[0])}`;
      }
    }
    return '';
  };

  const updateHours = () => {
    const { day, minutes } = athensNow();
    const current = HOURS[day].find(([start, end]) => minutes >= start && minutes < end);
    hoursStatus.classList.toggle('is-open', Boolean(current));
    hoursStatus.classList.toggle('is-closed', !current);
    textEl.textContent = current
      ? `Ανοιχτά τώρα · κλείνει στις ${fmt(current[1])}`
      : `Κλειστά τώρα · ${nextOpening(day, minutes)}`;
    document.querySelectorAll('.hours-table tr').forEach(tr => {
      const isToday = Number(tr.dataset.day) === day;
      tr.classList.toggle('today', isToday);
      tr.classList.toggle('today-open', isToday && Boolean(current));
      tr.classList.toggle('today-closed', isToday && !current);
    });
  };

  updateHours();
  setInterval(updateHours, 30 * 1000);
}
