// Minimal vanilla slide-deck engine.
// Features: arrow/space navigation, progress bar, slide counter,
// fullscreen (F), speaker notes (.), overview (Esc), help (?).

(function () {
  const slides = Array.from(document.querySelectorAll('.slide'));
  const total = slides.length;
  let current = 0;

  const progress = document.getElementById('progress');
  const counter = document.getElementById('counter');
  const notesOverlay = document.getElementById('notes-overlay');
  const overview = document.getElementById('overview');
  const help = document.getElementById('help');

  function show(idx) {
    current = Math.max(0, Math.min(total - 1, idx));
    slides.forEach((s, i) => s.classList.toggle('active', i === current));
    progress.style.width = ((current + 1) / total) * 100 + '%';
    counter.textContent = (current + 1) + ' / ' + total;
    syncNotes();
    history.replaceState(null, '', '#' + (current + 1));
  }

  function syncNotes() {
    if (!notesOverlay.classList.contains('show')) return;
    const notes = slides[current].querySelector('.notes');
    notesOverlay.innerHTML = '<h4>Speaker notes</h4>' + (notes ? notes.innerHTML : '<em>(no notes)</em>');
  }

  function toggleNotes() {
    notesOverlay.classList.toggle('show');
    syncNotes();
  }

  function toggleOverview() {
    if (overview.classList.contains('show')) {
      overview.classList.remove('show');
    } else {
      overview.innerHTML = '';
      overview.classList.add('show');
      slides.forEach((s, i) => {
        const t = s.querySelector('h1, h2');
        const div = document.createElement('div');
        div.className = 'thumb';
        div.innerHTML = '<div class="thumb-num">Slide ' + (i + 1) + '</div>' +
                        '<div class="thumb-title">' + (t ? t.textContent : '(untitled)') + '</div>';
        div.addEventListener('click', () => { show(i); overview.classList.remove('show'); });
        overview.appendChild(div);
      });
    }
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen();
    else document.exitFullscreen();
  }

  function toggleHelp() { help.classList.toggle('show'); }

  document.addEventListener('keydown', (e) => {
    // Ignore when typing in inputs.
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    // Close overlays first.
    if (e.key === 'Escape') {
      if (help.classList.contains('show')) { help.classList.remove('show'); return; }
      if (overview.classList.contains('show')) { overview.classList.remove('show'); return; }
      toggleOverview();
      return;
    }

    switch (e.key) {
      case 'ArrowRight':
      case 'PageDown':
      case ' ':
      case 'n':
        show(current + 1); e.preventDefault(); break;
      case 'ArrowLeft':
      case 'PageUp':
      case 'p':
        show(current - 1); e.preventDefault(); break;
      case 'Home': show(0); e.preventDefault(); break;
      case 'End':  show(total - 1); e.preventDefault(); break;
      case 'f': case 'F': toggleFullscreen(); break;
      case '.': toggleNotes(); break;
      case '?': case '/': toggleHelp(); e.preventDefault(); break;
    }
  });

  // Click navigation: right half = next, left half = prev.
  document.getElementById('deck').addEventListener('click', (e) => {
    if (e.target.closest('a, button, .thumb')) return;
    const x = e.clientX / window.innerWidth;
    if (x > 0.5) show(current + 1); else show(current - 1);
  });

  // Start at hash if provided.
  const hash = parseInt(location.hash.replace('#', ''), 10);
  show(Number.isFinite(hash) && hash > 0 ? hash - 1 : 0);
})();
