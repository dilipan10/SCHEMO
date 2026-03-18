/* ================================================================
   Schemo – Main JavaScript
================================================================ */

/* ── Navbar: scroll effect ────────────────────────────────────── */
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.4)';
    } else {
      navbar.style.boxShadow = 'none';
    }
  });
}

/* ── Navbar: mobile toggle ──────────────────────────────────── */
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
  document.addEventListener('click', (e) => {
    if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
      navLinks.classList.remove('open');
    }
  });
}

/* ── Admin sidebar tab switching ────────────────────────────── */
const sidebarLinks = document.querySelectorAll('.sidebar-link[data-tab]');
sidebarLinks.forEach((link) => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const tab = link.dataset.tab;
    sidebarLinks.forEach((l) => l.classList.remove('active'));
    link.classList.add('active');
    document.querySelectorAll('.admin-tab-panel').forEach((panel) => {
      panel.style.display = 'none';
    });
    const target = document.getElementById(`${tab}-section`);
    if (target) target.style.display = 'block';
  });
});

/* ── Live user search in admin table ───────────────────────── */
const userSearch = document.getElementById('userSearch');
if (userSearch) {
  userSearch.addEventListener('input', () => {
    const q = userSearch.value.toLowerCase().trim();
    document.querySelectorAll('#usersTable tbody tr').forEach((row) => {
      const text = row.textContent.toLowerCase();
      row.style.display = !q || text.includes(q) ? '' : 'none';
    });
  });
}

/* ── Live scheme search + community filter ──────────────────── */
const schemeSearch = document.getElementById('schemeSearch');
const communityFilter = document.getElementById('communityFilter');
const allSchemesGrid = document.getElementById('allSchemesGrid');
const noResults = document.getElementById('noResults');

function filterSchemes() {
  if (!allSchemesGrid) return;
  const q = schemeSearch ? schemeSearch.value.toLowerCase().trim() : '';
  const comm = communityFilter ? communityFilter.value.toLowerCase().trim() : '';

  let visible = 0;
  allSchemesGrid.querySelectorAll('.scheme-card').forEach((card) => {
    const name = (card.dataset.name || '').toLowerCase();
    const community = (card.dataset.community || '').toLowerCase();
    const textMatch = !q || name.includes(q) || card.textContent.toLowerCase().includes(q);
    const commMatch = !comm || community.includes(comm);
    const show = textMatch && commMatch;
    card.style.display = show ? '' : 'none';
    if (show) visible++;
  });

  if (noResults) noResults.style.display = visible === 0 ? 'block' : 'none';
}

if (schemeSearch) schemeSearch.addEventListener('input', filterSchemes);
if (communityFilter) communityFilter.addEventListener('change', filterSchemes);

/* ── Signup form: client-side validation ────────────────────── */
const signupForm = document.getElementById('signupForm');
if (signupForm) {
  signupForm.addEventListener('submit', (e) => {
    const password = document.getElementById('password');
    const age = document.getElementById('age');
    const income = document.getElementById('income');
    const phone = document.getElementById('phone_number');

    if (phone && !/^\d{10}$/.test(phone.value.trim())) {
      e.preventDefault();
      showError(phone, 'Phone number must be exactly 10 digits.');
      return;
    }
    if (password && password.value.length < 6) {
      e.preventDefault();
      showError(password, 'Password must be at least 6 characters.');
      return;
    }
    if (age && (parseInt(age.value) < 1 || parseInt(age.value) > 120)) {
      e.preventDefault();
      showError(age, 'Please enter a valid age between 1 and 120.');
      return;
    }
    if (income && parseFloat(income.value) < 0) {
      e.preventDefault();
      showError(income, 'Income cannot be negative.');
      return;
    }
  });
}

function showError(input, message) {
  input.style.borderColor = '#EF4444';
  input.style.boxShadow = '0 0 0 3px rgba(239,68,68,0.2)';
  let err = input.parentElement.querySelector('.field-error');
  if (!err) {
    err = document.createElement('small');
    err.className = 'field-error';
    err.style.cssText = 'color:#F87171; font-size:.8rem; margin-top:.3rem; display:block;';
    input.parentElement.appendChild(err);
  }
  err.textContent = message;
  input.focus();
  input.addEventListener('input', () => {
    input.style.borderColor = '';
    input.style.boxShadow = '';
    if (err.parentNode) err.remove();
  }, { once: true });
}

/* ── Smooth scroll reveal animations ─────────────────────────── */
const revealEls = document.querySelectorAll('.step-card, .feature-card, .scheme-card, .detail-card, .profile-card');
if ('IntersectionObserver' in window && revealEls.length) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.08 }
  );
  revealEls.forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(24px)';
    el.style.transition = `opacity 0.5s ease ${i * 0.06}s, transform 0.5s ease ${i * 0.06}s`;
    observer.observe(el);
  });
}
