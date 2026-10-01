/* ============================================================
   СпасиДете.БГ — основни скриптове / main scripts
   Ванилен JavaScript, без външни зависимости.
   Vanilla JavaScript, no external dependencies.
   ============================================================ */
(function () {
  'use strict';

  var STORAGE_KEY = 'sd-lang';
  var LANGS = ['bg', 'en'];

  /* ---------- 1. Език / Language ------------------------------------ */

  function readStoredLang() {
    try { return window.localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }

  function storeLang(lang) {
    try { window.localStorage.setItem(STORAGE_KEY, lang); } catch (e) { /* private mode */ }
  }

  function applyLang(lang, persist) {
    if (LANGS.indexOf(lang) === -1) { lang = 'bg'; }
    var root = document.documentElement;
    root.setAttribute('data-lang', lang);
    root.setAttribute('lang', lang);
    if (persist) { storeLang(lang); }

    // Бутоните на превключвателя / switch buttons
    var buttons = document.querySelectorAll('.langswitch button[data-lang]');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].setAttribute('aria-pressed', String(buttons[i].getAttribute('data-lang') === lang));
    }

    // Заглавие на документа / document title
    var titleEl = document.querySelector('title[data-title-bg]');
    if (titleEl) {
      var t = titleEl.getAttribute('data-title-' + lang);
      if (t) { document.title = t; }
    }

    // Мета описание / meta description
    var desc = document.querySelector('meta[name="description"][data-desc-bg]');
    if (desc) {
      var d = desc.getAttribute('data-desc-' + lang);
      if (d) { desc.setAttribute('content', d); }
    }
  }

  function initLang() {
    var params = new URLSearchParams(window.location.search);
    var fromUrl = params.get('lang');
    var lang = (LANGS.indexOf(fromUrl) > -1) ? fromUrl : (readStoredLang() || 'bg');
    applyLang(lang, true);

    var sw = document.querySelectorAll('.langswitch button[data-lang]');
    for (var i = 0; i < sw.length; i++) {
      sw[i].addEventListener('click', function () {
        applyLang(this.getAttribute('data-lang'), true);
      });
    }
  }

  /* ---------- 2. Началото на страницата / always start at the top ---- */

  /* Текущият език на страницата / the page's current language */
  function curLang() {
    return document.documentElement.getAttribute('data-lang') === 'en' ? 'en' : 'bg';
  }

  function scrollToTop(smooth) {
    try {
      window.scrollTo({ top: 0, left: 0, behavior: smooth ? 'smooth' : 'auto' });
    } catch (e) {
      window.scrollTo(0, 0);           // по-стари браузъри / older browsers
    }
    // Някои браузъри връщат позицията малко след зареждането. Повтаряме
    // веднъж на следващия кадър, за да остане горе.
    // Some browsers restore the position shortly after load. We repeat it once
    // on the next frame so the page stays at the top.
    if (!smooth) {
      try {
        window.requestAnimationFrame(function () { window.scrollTo(0, 0); });
      } catch (e2) { /* няма rAF / no rAF */ }
    }
  }

  /* Името на файла на текущата страница / the current page's file name */
  function currentPage() {
    var last = window.location.pathname.split('/').pop();
    return last || 'index.html';
  }

  /* Води ли връзката към същата страница? / does the link point at this page? */
  function pointsHere(href) {
    var file = href.split('#')[0].split('?')[0].split('/').pop();
    if (!file) { file = 'index.html'; }
    return file === currentPage();
  }

  function initTopOnNavigate() {
    // Браузърът по подразбиране връща страницата там, където сме я оставили.
    // Изключваме това: всяка страница се отваря от началото си. Единственото
    // изключение е адрес с котва (#...) — тогава скачаме до самия раздел.
    // Browsers restore the previous scroll position by default. We turn that
    // off: every page opens at its top. The only exception is an address with
    // an anchor (#...), where we jump to that section instead.
    try {
      if ('scrollRestoration' in window.history) {
        window.history.scrollRestoration = 'manual';
      }
    } catch (e) { /* по-стари браузъри / older browsers */ }

    if (!window.location.hash) {
      scrollToTop(false);
      window.addEventListener('load', function () {
        if (!window.location.hash) { scrollToTop(false); }
      });
    }

    // Връщане от кеша на браузъра (назад/напред) — пак от началото.
    // Returning from the browser's cache (back/forward) — from the top again.
    window.addEventListener('pageshow', function (e) {
      if (e.persisted && !window.location.hash) { scrollToTop(false); }
    });

    var links = document.querySelectorAll('.brand, .nav__links a');
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener('click', function (e) {
        var href = this.getAttribute('href') || '';

        // Външни адреси и отваряне в нов раздел не се пипат.
        // External addresses and new-tab clicks are left alone.
        if (!href || /^(https?:|mailto:|tel:)/i.test(href)) { return; }
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) { return; }

        if (pointsHere(href) && href.indexOf('#') === -1) {
          // Вече сме на тази страница — плавно нагоре, без презареждане.
          // Already on this page — glide to the top instead of reloading.
          e.preventDefault();
          scrollToTop(true);
          if (document.activeElement && document.activeElement.blur) {
            document.activeElement.blur();
          }
        }
        // Друга страница се отваря от началото си сама — за това се грижи
        // scrollRestoration = 'manual' плюс превъртането при зареждане по-горе.
        // A different page opens at its top on its own — scrollRestoration =
        // 'manual' plus the scroll on load above take care of that.
      });
    }
  }

  /* ---------- 3. Мобилна навигация / mobile navigation -------------- */

  function initNav() {
    var toggle = document.querySelector('.navtoggle');
    var nav = document.querySelector('.nav__links');
    if (!toggle || !nav) { return; }

    function close() {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    }

    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });

    // Затваряне при избор на връзка / close after choosing a link
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a') && nav.classList.contains('is-open')) { close(); }
    });

    // Затваряне с Esc или при щракване извън менюто
    // Close with Esc or a click outside the menu
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { close(); toggle.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (!nav.classList.contains('is-open')) { return; }
      // Самият бутон се грижи за себе си; смяната на езика не бива да затваря менюто.
      // The toggle handles itself; switching language should not close the menu.
      if (e.target.closest('.navtoggle') || e.target.closest('.langswitch')) { return; }
      // Връзките в менюто вече се обработват по-горе.
      // Links inside the menu are handled above.
      if (e.target.closest('.nav__links')) { return; }
      // Всичко останало — включително марката и бутона „Подай сигнал“ — затваря менюто.
      // Everything else — the brand and the report button included — closes it.
      close();
    });
  }

  /* ---------- 4. Табове / tabs -------------------------------------- */

  function initTabs() {
    var groups = document.querySelectorAll('[data-tabs]');
    for (var g = 0; g < groups.length; g++) {
      (function (group) {
        var buttons = group.querySelectorAll('.tabs__btn');
        var panels = group.querySelectorAll('.tabs__panel');

        function select(index) {
          for (var i = 0; i < buttons.length; i++) {
            var on = i === index;
            buttons[i].setAttribute('aria-selected', String(on));
            buttons[i].setAttribute('tabindex', on ? '0' : '-1');
            if (panels[i]) { panels[i].hidden = !on; }
          }
        }

        for (var i = 0; i < buttons.length; i++) {
          (function (idx) {
            buttons[idx].addEventListener('click', function () {
              select(idx);
              if (history.replaceState && buttons[idx].dataset.hash) {
                history.replaceState(null, '', '#' + buttons[idx].dataset.hash);
              }
              // Смяната на раздел връща читателя в началото на страницата,
              // за да не започва новия текст от средата му.
              // Switching a tab returns the reader to the top of the page, so the
              // new text does not start halfway down.
              scrollToTop(true);
            });
            buttons[idx].addEventListener('keydown', function (e) {
              var next = null;
              if (e.key === 'ArrowRight') { next = (idx + 1) % buttons.length; }
              if (e.key === 'ArrowLeft') { next = (idx - 1 + buttons.length) % buttons.length; }
              if (next !== null) { e.preventDefault(); select(next); buttons[next].focus(); }
            });
          })(i);
        }

        // Отваряне по адрес #hash / open from URL hash
        var hash = window.location.hash.replace('#', '');
        var start = 0;
        if (hash) {
          for (var j = 0; j < buttons.length; j++) {
            if (buttons[j].dataset.hash === hash) { start = j; }
          }
        }
        select(start);
      })(groups[g]);
    }
  }

  /* ---------- 5. Разгъване на новини / expandable articles ---------- */

  function initExpanders() {
    var buttons = document.querySelectorAll('[data-expand]');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener('click', function () {
        var target = document.getElementById(this.getAttribute('data-expand'));
        if (!target) { return; }
        var open = target.hidden;
        target.hidden = !open;
        this.setAttribute('aria-expanded', String(open));
        var labels = this.querySelectorAll('[data-label-open]');
        for (var k = 0; k < labels.length; k++) {
          labels[k].textContent = open
            ? labels[k].getAttribute('data-label-close')
            : labels[k].getAttribute('data-label-open');
        }
        if (!open) { this.scrollIntoView({ block: 'nearest' }); }
      });
    }
  }

  /* ---------- 6. Бутон „нагоре“ / back to top ----------------------- */

  function initToTop() {
    var btn = document.querySelector('.totop');
    if (!btn) { return; }
    var ticking = false;
    function update() {
      btn.classList.toggle('is-visible', window.scrollY > 700);
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    update();
  }

  /* ---------- 7. Ротация на снимки / photo carousel ------------------ */

  function initCarousel() {
    var root = document.querySelector('[data-carousel]');
    if (!root) { return; }
    var track = root.querySelector('.carousel__track');
    var slides = root.querySelectorAll('.slide');
    var dotsBox = root.querySelector('.carousel__dots');
    var prev = root.querySelector('[data-car="prev"]');
    var next = root.querySelector('[data-car="next"]');
    if (!track || !slides.length) { return; }

    var timer = null;
    var paused = false;

    function perView() {
      var w = slides[0].getBoundingClientRect().width;
      return Math.max(1, Math.round(track.clientWidth / (w + 16)));
    }
    function pages() { return Math.max(1, slides.length - perView() + 1); }
    function current() {
      var step = slides[0].getBoundingClientRect().width + 16;
      return Math.round(track.scrollLeft / step);
    }
    function goTo(i) {
      var step = slides[0].getBoundingClientRect().width + 16;
      track.scrollTo({ left: i * step, behavior: 'smooth' });
    }

    // Точки / dots
    function buildDots() {
      dotsBox.innerHTML = '';
      for (var i = 0; i < pages(); i++) {
        (function (idx) {
          var b = document.createElement('button');
          b.type = 'button';
          b.setAttribute('role', 'tab');
          b.setAttribute('aria-label', String(idx + 1));
          b.addEventListener('click', function () { goTo(idx); restart(); });
          dotsBox.appendChild(b);
        })(i);
      }
      sync();
    }
    function sync() {
      var c = current();
      var dots = dotsBox.querySelectorAll('button');
      for (var i = 0; i < dots.length; i++) {
        dots[i].setAttribute('aria-selected', String(i === c));
      }
      if (prev) { prev.disabled = c <= 0; }
      if (next) { next.disabled = c >= pages() - 1; }
    }

    if (prev) { prev.addEventListener('click', function () { goTo(Math.max(0, current() - 1)); restart(); }); }
    if (next) { next.addEventListener('click', function () { goTo(Math.min(pages() - 1, current() + 1)); restart(); }); }

    var ticking = false;
    track.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(function () { sync(); ticking = false; }); ticking = true; }
    }, { passive: true });

    // Автоматично превъртане, спира при посягане / autoplay, stops on interaction
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function tick() {
      if (paused || document.hidden) { return; }
      var c = current();
      goTo(c >= pages() - 1 ? 0 : c + 1);
    }
    function start() { if (!reduce && !timer) { timer = window.setInterval(tick, 5500); } }
    function stop() { if (timer) { window.clearInterval(timer); timer = null; } }
    function restart() { stop(); start(); }

    root.addEventListener('mouseenter', function () { paused = true; });
    root.addEventListener('mouseleave', function () { paused = false; });
    root.addEventListener('focusin', function () { paused = true; });
    root.addEventListener('focusout', function () { paused = false; });
    track.addEventListener('touchstart', function () { paused = true; }, { passive: true });

    window.addEventListener('resize', function () { buildDots(); });
    buildDots();
    start();
  }

  /* ---------- 8. Формуляр за сигнал / report form -------------------- */

  function initReportForm() {
    var form = document.getElementById('sigform');
    if (!form) { return; }
    var sel = document.getElementById('f-region');
    var box = document.getElementById('regionbox');
    var status = document.getElementById('formstatus');
    var copyBtn = document.getElementById('copybtn');

    function lang() { return curLang(); }
    function t(bg, en) { return lang() === 'en' ? en : bg; }

    function chosen() {
      var o = sel.options[sel.selectedIndex];
      if (!o || !o.value) { return null; }
      return {
        mail: o.getAttribute('data-mail') || '',
        tel: o.getAttribute('data-tel') || '',
        name: o.getAttribute('data-' + lang()) || o.getAttribute('data-bg') || '',
        addr: o.getAttribute('data-addr') || '',
        tl: o.getAttribute('data-tl' + lang()) || o.getAttribute('data-tlbg') || '',
        fallback: o.getAttribute('data-fallback') === '1'
      };
    }

    function showRegion() {
      var c = chosen();
      if (!c) {
        document.getElementById('rb-name').textContent = t('Изберете област', 'Choose a region');
        document.getElementById('rb-tel').innerHTML = '<span class="muted">—</span>';
        document.getElementById('rb-mail').innerHTML = '<span class="muted">—</span>';
        document.getElementById('rb-addr').textContent = '—';
        return;
      }
      document.getElementById('rb-name').textContent = (lang() === 'en' ? 'Regional Directorate ' : 'ОДМВР ') + c.name;
      var telEl = document.getElementById('rb-tel');
      telEl.innerHTML = c.tel
        ? '<a href="tel:' + c.tel.replace(/\s/g, '') + '">' + c.tel + '</a>' +
          (c.tl ? ' <span class="muted">(' + c.tl + ')</span>' : '')
        : '<span class="muted">—</span>';
      var mailEl = document.getElementById('rb-mail');
      mailEl.innerHTML = '<a href="mailto:' + c.mail + '">' + c.mail + '</a>' +
        (c.fallback
          ? '<small>' + t('Тази дирекция не публикува електронен адрес. Писмото тръгва към приемната на МВР, която го пренасочва.',
                          'This directorate publishes no e-mail address. The letter goes to the Ministry of Interior’s reception, which forwards it.') + '</small>'
          : '');
      document.getElementById('rb-addr').textContent = c.addr || '—';
    }

    // Етикетите в падащото меню се сменят с езика (в <option> не може HTML).
    // The dropdown labels follow the language (HTML is not allowed inside <option>).
    function syncOptions() {
      for (var i = 0; i < sel.options.length; i++) {
        var o = sel.options[i];
        var v = o.value
          ? (o.getAttribute('data-' + lang()) || o.getAttribute('data-bg'))
          : (o.getAttribute('data-ph-' + lang()) || o.getAttribute('data-ph-bg'));
        if (v) { o.textContent = v; }
      }
    }

    sel.addEventListener('change', showRegion);
    document.addEventListener('click', function (e) {
      if (e.target.closest('.langswitch')) {
        window.setTimeout(function () { syncOptions(); showRegion(); }, 0);
      }
    });
    syncOptions();

    function val(id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; }

    function buildText() {
      var c = chosen();
      var L = lang() === 'en';
      var lines = [];
      lines.push(L ? 'REPORT OF VIOLENCE OR AGGRESSION INVOLVING A CHILD'
                   : 'СИГНАЛ ЗА НАСИЛИЕ ИЛИ АГРЕСИЯ, СВЪРЗАНИ С ДЕТЕ');
      lines.push('');
      lines.push((L ? 'Region: ' : 'Област: ') + (c ? c.name : '—'));
      if (val('f-place')) { lines.push((L ? 'Place: ' : 'Място: ') + val('f-place')); }
      if (val('f-when')) { lines.push((L ? 'When: ' : 'Кога: ') + val('f-when')); }
      if (val('f-who')) { lines.push((L ? 'Age of the child: ' : 'Възраст на детето: ') + val('f-who')); }
      lines.push('');
      lines.push(L ? 'What happened:' : 'Какво се е случило:');
      lines.push(val('f-what'));
      lines.push('');
      if (val('f-name') || val('f-contact')) {
        lines.push(L ? 'Submitted by:' : 'Подател:');
        if (val('f-name')) { lines.push('  ' + val('f-name')); }
        if (val('f-contact')) { lines.push('  ' + val('f-contact')); }
      } else {
        lines.push(L ? 'Submitted anonymously.' : 'Сигналът се подава анонимно.');
      }
      lines.push('');
      lines.push(L ? '— Prepared via spasidete.bg' : '— Подготвено чрез spasidete.bg');
      return lines.join('\n');
    }

    function say(msg, ok) {
      status.textContent = msg;
      status.style.color = ok ? 'var(--ink-2)' : 'var(--red)';
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var c = chosen();
      if (!c) { sel.focus(); say(t('Моля, изберете област.', 'Please choose a region.'), false); return; }
      if (!val('f-what')) {
        document.getElementById('f-what').focus();
        say(t('Моля, опишете какво се е случило.', 'Please describe what happened.'), false); return;
      }
      var subj = t('Сигнал за насилие/агресия над дете — ', 'Report of violence/aggression against a child — ') + c.name;
      var href = 'mailto:' + c.mail +
                 '?subject=' + encodeURIComponent(subj) +
                 '&body=' + encodeURIComponent(buildText());

      // Кирилицата заема по шест знака след кодиране, затова дори кратък
      // сигнал дава дълъг адрес. Пускаме писмото до 6000 знака — толкова
      // понасят съвременните пощенски програми — и само над тази граница
      // пращаме към копирането.
      // Cyrillic takes six characters each once encoded, so even a short
      // report yields a long address. We open the letter up to 6000
      // characters — what current mail clients handle — and only past that
      // send the sender to the copy button.
      if (href.length > 6000) {
        say(t('Описанието е твърде дълго за автоматично писмо. Натиснете „Копирай текста“ и го поставете в писмо до ' + c.mail + '.',
              'The description is too long for an automatic letter. Press “Copy the text” and paste it into an e-mail to ' + c.mail + '.'), false);
        return;
      }

      var a = document.createElement('a');
      a.href = href;
      a.style.display = 'none';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      say(t('Отваря се пощенската ви програма. Прегледайте писмото и го изпратете. Ако програмата не се отвори или текстът е отрязан, натиснете „Копирай текста“ и го поставете в ново писмо до ' + c.mail + '.',
            'Your e-mail program is opening. Review the letter and send it. If it does not open, or the text is cut off, press “Copy the text” and paste it into a new e-mail to ' + c.mail + '.'), true);
    });

    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        var text = buildText();
        function done() { say(t('Текстът е копиран.', 'The text has been copied.'), true); }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done, function () { fallback(text, done); });
        } else { fallback(text, done); }
      });
    }
    function fallback(text, done) {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', '');
      ta.style.position = 'absolute'; ta.style.left = '-9999px';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done(); }
      catch (e) { say(t('Копирането не бе успешно — маркирайте текста ръчно.',
                        'Copying failed — please select the text manually.'), false); }
      document.body.removeChild(ta);
    }
  }

  /* ---------- 9. Видео при поискване / click-to-load video ----------- */

  function initVideoFacade() {
    var boxes = document.querySelectorAll('.videofacade[data-yt]');

    // YouTube отказва да се вгражда, когато страницата е отворена направо от диска
    // (адрес file://) — тогава източникът на страницата е „null“ и плейърът
    // показва „Video unavailable“. В този случай отваряме видеото в YouTube.
    // YouTube refuses to embed when the page is opened straight from disk (a
    // file:// address): the page's origin is then "null" and the player shows
    // "Video unavailable". In that case we open the video on YouTube instead.
    var canEmbed = window.location.protocol === 'http:' ||
                   window.location.protocol === 'https:';

    for (var i = 0; i < boxes.length; i++) {
      (function (box) {
        var btn = box.querySelector('.videofacade__btn');
        var id = box.getAttribute('data-yt');
        if (!btn || !id) { return; }
        var watch = 'https://www.youtube.com/watch?v=' + encodeURIComponent(id);

        btn.addEventListener('click', function () {
          if (!canEmbed) { window.open(watch, '_blank', 'noopener'); return; }

          var frame = document.createElement('iframe');
          frame.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) +
                      '?autoplay=1&rel=0&playsinline=1';
          frame.title = box.getAttribute('data-title') || 'video';
          frame.setAttribute('allow',
            'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
          frame.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
          frame.setAttribute('allowfullscreen', '');
          frame.setAttribute('loading', 'eager');
          box.innerHTML = '';
          box.appendChild(frame);
          box.classList.add('is-playing');
          box.style.cursor = 'default';
          frame.focus();
        });

        // Подсказката под бутона казва какво ще стане и води към YouTube,
        // ако плейърът откаже да тръгне.
        // The hint under the button says what will happen and leads to YouTube
        // if the player refuses to start.
        var hint = box.querySelector('.videofacade__hint');
        if (hint && !canEmbed) {
          hint.innerHTML = '<span lang="bg">Отваря се в YouTube в нов раздел</span>' +
                           '<span lang="en">Opens on YouTube in a new tab</span>';
        }

        // Постоянна връзка под видеото — работи дори ако плейърът откаже.
        // A permanent link under the video — it works even if the player refuses.
        var slot = box.parentNode;
        if (slot && !slot.querySelector('.videolink')) {
          var a = document.createElement('a');
          a.className = 'videolink';
          a.href = watch;
          a.target = '_blank';
          a.rel = 'noopener';
          a.innerHTML = '<span lang="bg">Гледай в YouTube</span>' +
                        '<span lang="en">Watch on YouTube</span>';
          var credit = slot.querySelector('.videocredit');
          if (credit) { slot.insertBefore(a, credit); } else { slot.appendChild(a); }
        }
      })(boxes[i]);
    }
  }

  /* ---------- 10. Текуща година / current year ---------------------- */

  function initYear() {
    var els = document.querySelectorAll('[data-year]');
    for (var i = 0; i < els.length; i++) { els[i].textContent = new Date().getFullYear(); }
  }

  /* ---------- Старт / boot ------------------------------------------ */

  function boot() {
    initLang();
    initTopOnNavigate();
    initNav();
    initTabs();
    initExpanders();
    initToTop();
    initCarousel();
    initReportForm();
    initVideoFacade();
    initYear();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
