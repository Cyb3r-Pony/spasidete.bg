#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор на статичния сайт СпасиДете.БГ
Static-site generator for СпасиДете.БГ

Стартиране / Usage:   python3 build.py
Записва .html файловете в същата папка. / Writes the .html files next to itself.

Съдържанието е двуезично: всеки текстов блок съществува на български и на
английски, а превключвателят в горния десен ъгъл показва само избрания език.
Content is bilingual: every text block exists in Bulgarian and English; the
switch in the top-right corner shows only the selected language.
"""

import os
import html as _html

import content2 as C2

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# Помощни функции / helpers
# --------------------------------------------------------------------------


def bi(bg, en, tag="span", cls=None):
    """Двуезичен блок / bilingual block."""
    c = ' class="%s"' % cls if cls else ""
    return '<%s lang="bg"%s>%s</%s><%s lang="en"%s>%s</%s>' % (
        tag, c, bg, tag, tag, c, en, tag
    )


def p(bg, en, cls=None):
    return bi(bg, en, "p", cls)


def h(level, bg, en, cls=None):
    c = ' class="%s"' % cls if cls else ""
    return '<h{l} lang="bg"{c}>{bg}</h{l}><h{l} lang="en"{c}>{en}</h{l}>'.format(
        l=level, c=c, bg=bg, en=en
    )


def ul(bg_items, en_items, cls=None):
    c = ' class="%s"' % cls if cls else ""
    a = "".join("<li>%s</li>" % x for x in bg_items)
    b = "".join("<li>%s</li>" % x for x in en_items)
    return '<ul lang="bg"%s>%s</ul><ul lang="en"%s>%s</ul>' % (c, a, c, b)


def esc(s):
    return _html.escape(s, quote=True)


# --------------------------------------------------------------------------
# Снимки: WebP с резервен JPEG и два размера / pictures: WebP with a JPEG
# fallback, in two sizes. Браузърът сам избира най-лекия подходящ файл.
# --------------------------------------------------------------------------

_PHOTO_SIZES = {}          # попълва се от _scan_photos() / filled by _scan_photos()


def _scan_photos():
    """Прочита размерите на снимките веднъж / read every photo's size once."""
    import struct
    d = os.path.join(HERE, "assets", "img", "photos")
    if not os.path.isdir(d):
        return
    for fn in os.listdir(d):
        if not fn.endswith(".jpg"):
            continue
        path = os.path.join(d, fn)
        with open(path, "rb") as fh:
            data = fh.read()
        i, size = 2, None
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                size = (w, h)
                break
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            seg = struct.unpack(">H", data[i + 2:i + 4])[0]
            i += 2 + seg
        if size:
            _PHOTO_SIZES[fn] = size


def pic(name, alt, sizes="100vw", cls="", eager=False, caption=None):
    """<picture> с WebP, малък вариант и JPEG за стари браузъри."""
    base = name[:-4] if name.endswith(".jpg") else name
    d = os.path.join(HERE, "assets", "img", "photos")
    jpg = "assets/img/photos/%s.jpg" % base
    w, h = _PHOTO_SIZES.get(base + ".jpg", (1400, 1050))
    half = max(640, w // 2)

    # Включваме само вариантите, които наистина съществуват на диска.
    # Only the variants that actually exist on disk go into the srcset.
    steps = []
    if os.path.exists(os.path.join(d, base + "-xs.webp")):
        steps.append(("-xs", 480))
    if half < w and os.path.exists(os.path.join(d, base + "-sm.webp")):
        steps.append(("-sm", half))
    if os.path.exists(os.path.join(d, base + "-md.webp")):
        steps.append(("-md", 960))
    steps.append(("", w))
    steps.sort(key=lambda s: s[1])

    webp_set = ", ".join("assets/img/photos/{b}{sfx}.webp {n}w".format(b=base, sfx=sfx, n=n)
                         for sfx, n in steps)
    jpg_set = ", ".join("assets/img/photos/{b}{sfx}.jpg {n}w".format(b=base, sfx=sfx, n=n)
                        for sfx, n in steps)
    load = ' fetchpriority="high"' if eager else ' loading="lazy"'
    img = (
        '<picture>'
        '<source type="image/webp" srcset="{ws}" sizes="{sz}">'
        '<img src="{jpg}" srcset="{js}" sizes="{sz}" alt="{alt}" '
        'width="{w}" height="{h}" decoding="async"{load}{cls}>'
        '</picture>'
    ).format(ws=webp_set, js=jpg_set, sz=sizes, jpg=jpg, alt=esc(alt),
             w=w, h=h, load=load, cls=(' class="%s"' % cls) if cls else "")
    if caption is None:
        return img
    return img + ("<figcaption>%s</figcaption>" % caption if caption else "")


def logo(name="logo-spasidete", cls="", alt="", w=0, h=0, lazy=False):
    """Марката на сайта. Подава се WebP с PNG за резерва.

    `logo-spasidete` е пълното лого с надписа — стои в лентата горе вляво.
    `logo-mark` е само щитът — ползва се там, където няма място за надпис,
    и е основата на иконата в браузъра.
    `logo-full` е логото заедно с реда на МВР — стои във футъра.

    The site's mark. A WebP is served with a PNG fallback.
    `logo-spasidete` is the full lockup with the wordmark, used in the top bar;
    `logo-mark` is the shield alone; `logo-full` carries the Ministry line and
    lives in the footer.
    """
    base = "assets/img/" + name
    return (
        '<picture>'
        '<source type="image/webp" srcset="{b}.webp">'
        '<img src="{b}.png" alt="{alt}" width="{w}" height="{h}" '
        'decoding="async"{lz}{cls}>'
        '</picture>'
    ).format(b=base, alt=esc(alt), w=w, h=h,
             lz=' loading="lazy"' if lazy else "",
             cls=(' class="%s"' % cls) if cls else "")


def emblem(name, alt="", cls="", w=0, h=0, lazy=True):
    """Емблемите също имат WebP / the emblems have a WebP version too.

    Никъде на сайта емблемата не се показва по-широка от 58 CSS px, затова
    по подразбиране тръгва вариантът от 192 px — достатъчен и при екран с
    тройна плътност. Оригиналът остава в srcset за по-големи случаи.

    Nowhere on the site is an emblem displayed wider than 58 CSS px, so the
    192 px variant is what ships by default — enough even on a 3x display.
    The original stays in the srcset for larger uses.
    """
    base = "assets/img/" + name
    small = os.path.exists(os.path.join(HERE, "assets", "img", name + "-sm.webp"))
    if small and w and w > 192:
        sh = int(round(h * 192.0 / w)) if h else 0
        return (
            '<picture>'
            '<source type="image/webp" srcset="{b}-sm.webp 192w, {b}.webp {w}w" sizes="{sz}px">'
            '<img src="{b}-sm.png" srcset="{b}-sm.png 192w, {b}.png {w}w" sizes="{sz}px" '
            'alt="{alt}" width="192" height="{sh}" decoding="async"{lz}{cls}>'
            '</picture>'
        ).format(b=base, alt=esc(alt), w=w, sh=sh, sz=64,
                 lz=' loading="lazy"' if lazy else "",
                 cls=(' class="%s"' % cls) if cls else "")
    return (
        '<picture>'
        '<source type="image/webp" srcset="{b}.webp">'
        '<img src="{b}.png" alt="{alt}" width="{w}" height="{h}" decoding="async"{lz}{cls}>'
        '</picture>'
    ).format(b=base, alt=esc(alt), w=w, h=h,
             lz=' loading="lazy"' if lazy else "",
             cls=(' class="%s"' % cls) if cls else "")


# --------------------------------------------------------------------------
# Икони (inline SVG) / icons
# --------------------------------------------------------------------------

ICON = {
    "up": '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>',
}

# --------------------------------------------------------------------------
# Знаме на ЕС — 12 звезди в кръг / EU flag — twelve stars in a circle
# --------------------------------------------------------------------------


def _eu_stars():
    import math
    pts = []
    for k in range(12):
        ang = math.radians(k * 30)              # 0° = на 12 часа / 12 o'clock
        cx = 45 + 18 * math.sin(ang)
        cy = 30 - 18 * math.cos(ang)
        star = []
        for i in range(10):
            r = 4.2 if i % 2 == 0 else 1.7
            a = math.radians(-90 + i * 36)
            star.append("%.2f,%.2f" % (cx + r * math.cos(a), cy + r * math.sin(a)))
        pts.append('<polygon points="%s"/>' % " ".join(star))
    return "".join(pts)


EU_STARS = _eu_stars()


# --------------------------------------------------------------------------
# Навигация / navigation
# --------------------------------------------------------------------------

NAV = [
    ("bullying.html", "Агресия и насилие", "Aggression &amp; violence"),
    ("advice.html", "Съвети", "Advice"),
    ("help.html", "Помощ", "Help"),
    ("campaigns.html", "Кампании", "Campaigns"),
    ("news.html", "Новини", "News"),
    ("resources.html", "Ресурси", "Resources"),
    ("about.html", "За нас", "About"),
]

def nav_html(active):
    items = []
    for href, bgl, enl in NAV:
        cur = ' aria-current="page"' if href == active else ""
        items.append(
            '<li><a href="%s"%s>%s</a></li>' % (href, cur, bi(bgl, enl))
        )
    return "\n        ".join(items)


# --------------------------------------------------------------------------
# Шаблон / template
# --------------------------------------------------------------------------

HEAD = """<!DOCTYPE html>
<html lang="bg" data-lang="bg">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title data-title-bg="{title_bg}" data-title-en="{title_en}">{title_bg}</title>
<meta name="description" data-desc-bg="{desc_bg}" data-desc-en="{desc_en}" content="{desc_bg}">
<meta name="theme-color" content="#0a1f38">
<meta property="og:type" content="website">
<meta property="og:site_name" content="СпасиДете.БГ">
<meta property="og:title" content="{title_bg}">
<meta property="og:description" content="{desc_bg}">
<meta property="og:locale" content="bg_BG">
<meta property="og:locale:alternate" content="en_GB">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="СпасиДете.БГ — агресията в детския свят">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="favicon.ico" sizes="16x16 24x24 32x32 48x48 64x64">
<link rel="icon" href="assets/img/icon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="assets/img/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="mask-icon" href="assets/img/mask-icon.svg" color="#1d4e89">
<link rel="stylesheet" href="assets/css/style.css">
{preload}
<script>
  /* Задава езика преди рисуване, за да няма премигване.
     Sets the language before paint so there is no flash. */
  (function () {{
    try {{
      var p = new URLSearchParams(location.search).get('lang');
      var l = (p === 'bg' || p === 'en') ? p : (localStorage.getItem('sd-lang') || 'bg');
      document.documentElement.setAttribute('data-lang', l);
      document.documentElement.setAttribute('lang', l);
    }} catch (e) {{}}
  }})();
</script>
</head>
<body>
<a class="skip-link" href="#main">{skip}</a>

<header class="nav">
  <div class="wrap nav__inner">
    <a class="brand" href="index.html" aria-label="СпасиДете.БГ — начало / home">
      {brandmark}
    </a>

    <nav class="nav__links" id="mainnav" aria-label="{t_mainnav}">
      <ul>
        {nav}
        <li class="nav__extra"><a href="contact.html"><span lang="bg">Контакти</span><span lang="en">Contact</span></a></li>
      </ul>
    </nav>

    <div class="nav__actions">
      <div class="langswitch" role="group" aria-label="Език / Language">
        <button type="button" data-lang="bg" aria-pressed="true">БГ</button>
        <button type="button" data-lang="en" aria-pressed="false">EN</button>
      </div>
      <a class="btn btn--danger btn--sm btn--report" href="report.html">{t_report}</a>
      <button class="navtoggle" type="button" aria-expanded="false" aria-controls="mainnav" aria-label="Меню / Menu"><span></span></button>
    </div>
  </div>
</header>

<div class="urgent">
  <div class="wrap urgent__inner">
    <span class="urgent__dot" aria-hidden="true"></span>
    {t_emergency}
    <a href="tel:112">112 <small>{t_emergency_sm}</small></a>
    <span class="sep" aria-hidden="true">·</span>
    <a href="tel:116111">116 111 <small>{t_child_sm}</small></a>
  </div>
</div>

<main id="main">
"""

FOOT = """</main>

<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <div class="footer__brand">
          {footmark}
          <span>
            <strong>СпасиДете.БГ</strong>
            {f_sub}
          </span>
        </div>
        {f_blurb}
      </div>
      <div>
        {f_h_site}
        <ul>{f_site_links}</ul>
      </div>
      <div>
        {f_h_inst}
        <ul>
          <li><a href="https://gdbop.bg/" target="_blank" rel="noopener">ГДБОП</a></li>
          <li><a href="https://www.cybercrime.bg/" target="_blank" rel="noopener">cybercrime.bg</a></li>
          <li><a href="https://www.mvr.bg/" target="_blank" rel="noopener">МВР</a></li>
          <li><a href="https://sacp.government.bg/" target="_blank" rel="noopener">ДАЗД</a></li>
          <li><a href="https://116111.bg/" target="_blank" rel="noopener">116 111</a></li>
        </ul>
      </div>
      <div>
        {f_h_contact}
        <ul>
          <li>{f_addr}</li>
          <li><a href="tel:+35929828363">+359 2 982 83 63</a></li>
          <li><a href="mailto:spasidete@cybercrime.bg">spasidete@cybercrime.bg</a></li>
        </ul>
      </div>
    </div>

    <div class="footer__eu">
      <svg class="eu-flag" viewBox="0 0 90 60" role="img" aria-label="Европейски съюз / European Union"><rect width="90" height="60" fill="#039"/><g fill="#FC0">{eu_stars}</g></svg>
      <span>
        <span lang="bg">Съ-финансиран по програма „Превенция и борба с престъпността“ на Европейския съюз.</span><span lang="en">Co-funded by the Prevention of and Fight against Crime Programme of the European Union.</span>
      </span>
    </div>

    <div class="footer__legal">
      <span>&copy; <span data-year>2026</span> {f_owner}</span>
      <span>{f_updated}</span>
    </div>
  </div>
</footer>

<button class="totop" type="button" aria-label="Нагоре / Back to top">{ic_up}</button>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


# Адресът, на който сайтът се обслужва в момента. Абсолютни адреси трябват на
# три места: og:image, og:url и каноничната връзка. Когато spasidete.bg започне
# да сочи към GitHub Pages, тук се сменя само този ред.
# The address the site is served from today. Absolute URLs are needed in three
# places: og:image, og:url and the canonical link. When spasidete.bg starts
# pointing at GitHub Pages, only this line changes.
SITE_BASE = "https://cyb3r-pony.github.io/spasidete.bg/"


def page(filename, title_bg, title_en, desc_bg, desc_en, body, preload=""):
    canonical = SITE_BASE + ("" if filename == "index.html" else filename)
    head = HEAD.format(
        canonical=canonical,
        og_image=SITE_BASE + "assets/img/og-image.jpg",
        title_bg=esc(title_bg),
        title_en=esc(title_en),
        desc_bg=esc(desc_bg),
        desc_en=esc(desc_en),
        skip=bi("Към основното съдържание", "Skip to main content"),
        t_report=bi(
            '<span class="lbl-full">Подай сигнал</span><span class="lbl-short">Сигнал</span>',
            '<span class="lbl-full">Report</span><span class="lbl-short">Report</span>',
        ),
        t_mainnav="Основна навигация / Main navigation",
        t_emergency=bi(
            "Ако дете е в опасност в момента, звъннете веднага:",
            "If a child is in danger right now, call immediately:",
            tag="b",
        ),
        t_emergency_sm=bi("спешен", "emergency"),
        t_child_sm=bi("линия за деца", "child line"),
        nav=nav_html(filename),
        preload=preload,
        brandmark=logo("logo-spasidete", cls="brand__mark",
                       alt="СпасиДете.БГ — превенция, защита, подкрепа",
                       w=382, h=160),
    )

    # Във футъра стоят само разделите. „Начало“, „Подай сигнал“ и „Контакти“
    # са винаги на един клик в горната лента, затова тук само биха удължили списъка.
    # The footer lists the sections only. Home, Report and Contact are always one
    # click away in the top bar, so here they would just lengthen the list.
    site_links = "".join(
        '<li><a href="%s">%s</a></li>' % (href, bi(b, e)) for href, b, e in NAV
    )

    foot = FOOT.format(
        f_sub=bi(
            "Детство без агресия",
            "A childhood without aggression",
        ),
        f_blurb=p(
            "Национален информационен портал на Министерството на вътрешните работи за агресията в "
            "детския свят във всичките ѝ форми — от деца, към деца и между деца, в училище, на улицата "
            "и онлайн — и за това къде всеки може да потърси помощ.",
            "A national information portal of the Ministry of Interior on aggression in the world of children in "
            "all its forms — by children, against children and between children, at school, in the street and "
            "online — and on where anyone can seek help.",
        ),
        f_h_site=h(2, "Разделите", "Sections"),
        f_site_links=site_links,
        f_h_inst=h(2, "Институции", "Institutions"),
        f_h_contact=h(2, "Контакт", "Contact"),
        f_addr=bi(
            "гр. София 1784, бул. „Цариградско шосе“ № 133А",
            "133A Tsarigradsko shose Blvd., Sofia 1784, Bulgaria",
        ),
        f_owner=bi(
            "Министерство на вътрешните работи",
            "Ministry of Interior of the Republic of Bulgaria",
        ),
        f_updated=bi("Последна актуализация: октомври 2026 г.", "Last updated: October 2026"),
        footmark=logo("logo-mark", cls="footer__mark", alt="", w=156, h=192, lazy=True),
        eu_stars=EU_STARS,
        ic_up=ICON["up"],
    )

    out = head + body + foot
    with open(os.path.join(HERE, filename), "w", encoding="utf-8") as fh:
        fh.write(out)
    print("  ->", filename, "%.1f KB" % (len(out.encode("utf-8")) / 1024.0))


def pagehead(bg_title, en_title, bg_sub, en_sub, crumb_bg, crumb_en, photo=None):
    """Заглавна лента; с `photo` — снимка вдясно от заглавието.
    Page header; with `photo`, an image sits to the right of the title."""
    if photo:
        inner = """<div class="pagehead__grid">
      <div>
        <div class="crumbs"><a href="index.html">{home}</a><span aria-hidden="true">/</span>{crumb}</div>
        {t}
        {s}
      </div>
      <figure class="pagehead__shot">{img}</figure>
    </div>"""
    else:
        inner = """<div class="crumbs"><a href="index.html">{home}</a><span aria-hidden="true">/</span>{crumb}</div>
    {t}
    {s}"""
    return ("""<section class="pagehead">
  <div class="wrap">
    """ + inner + """
  </div>
</section>
""").format(
        home=bi("Начало", "Home"),
        crumb=bi(crumb_bg, crumb_en),
        t=h(1, bg_title, en_title),
        s=p(bg_sub, en_sub),
        img=photo or "",
    )


# ==========================================================================
#  СЪДЪРЖАНИЕ / CONTENT
# ==========================================================================

# --- Телефонни линии и институции (от документа на МВР) -------------------
HELPLINES = [
    {
        "badge": "112", "badge_sm_bg": "24/7", "badge_sm_en": "24/7",
        "tel": "112", "urgent": True,
        "name_bg": "Национална система за спешни повиквания 112",
        "name_en": "112 — National Emergency Call System",
        "desc_bg": "Когато има непосредствена опасност за живота или здравето на дете — телесна повреда, заплаха, изчезнало дете, среща с непознат от интернет.",
        "desc_en": "When a child’s life or health is in immediate danger — injury, threats, a missing child, a meeting with a stranger met online.",
        "site": "https://www.mvr.bg/112/", "site_label": "mvr.bg/112",
        "email": None,
    },
    {
        "badge": "116 111", "badge_sm_bg": "безплатно", "badge_sm_en": "free",
        "tel": "116111", "urgent": False,
        "name_bg": "Национална телефонна линия за деца (ДАЗД)",
        "name_en": "National Child Helpline (SACP)",
        "desc_bg": "Безплатна и денонощна линия на Държавната агенция за закрила на детето. Деца могат да се обадят сами, анонимно, за всичко, което ги тревожи.",
        "desc_en": "A free, round-the-clock line run by the State Agency for Child Protection. Children can call on their own, anonymously, about anything that worries them.",
        "site": "https://116111.bg/", "site_label": "116111.bg",
        "email": None,
    },
    {
        "badge": "Онлайн", "badge_sm_bg": "сигнал", "badge_sm_en": "report",
        "tel": "+35929828363", "urgent": False,
        "name_bg": "Дирекция „Киберпрестъпност“ при ГДБОП-МВР",
        "name_en": "Cybercrime Directorate at GDBOP, Ministry of Interior",
        "desc_bg": "Сигнали за вредно и незаконно съдържание в българското интернет пространство — материали със сексуална злоупотреба с деца, заплахи, изнудване, склоняване на дете онлайн, разпространение на записи от насилие.",
        "desc_en": "Reports of harmful and illegal content in the Bulgarian internet space — child sexual abuse material, threats, extortion, online grooming, the spreading of recorded violence.",
        "site": "https://www.cybercrime.bg/", "site_label": "cybercrime.bg",
        "email": "spasidete@cybercrime.bg",
    },
    {
        "badge": "ГДБОП", "badge_sm_bg": "сигнал", "badge_sm_en": "report",
        "tel": "+35929828363", "urgent": False,
        "name_bg": "Главна дирекция „Борба с организираната престъпност“",
        "name_en": "General Directorate for Combating Organised Crime (GDBOP)",
        "desc_bg": "Официален канал за подаване на сигнал към ГДБОП. Анонимността на подателя се гарантира по реда на закона.",
        "desc_en": "The official channel for submitting a report to GDBOP. The anonymity of the person reporting is guaranteed by law.",
        "site": "https://gdbop.bg/", "site_label": "gdbop.bg",
        "email": None,
    },
    {
        "badge": "ДАЗД", "badge_sm_bg": "агенция", "badge_sm_en": "agency",
        "tel": "+35929339011", "urgent": False,
        "name_bg": "Държавна агенция за закрила на детето",
        "name_en": "State Agency for Child Protection",
        "desc_bg": "Държавният орган за закрила на детето. Приема сигнали за дете в риск и координира действията на институциите.",
        "desc_en": "The state body for child protection. It receives reports about children at risk and coordinates the institutions’ response.",
        "site": "https://sacp.government.bg/", "site_label": "sacp.government.bg",
        "email": "stopech@sacp.government.bg",
        "extra_bg": "тел. +359 2 933 90 11 · факс +359 2 980 24 15",
        "extra_en": "tel. +359 2 933 90 11 · fax +359 2 980 24 15",
    },
    {
        "badge": "0876", "badge_sm_bg": "692 280", "badge_sm_en": "692 280",
        "tel": "+359876692280", "urgent": False,
        "name_bg": "„Зона ЗаКрила“ — УНИЦЕФ България",
        "name_en": "“Zona ZaKrila” Child Advocacy Centres — UNICEF Bulgaria",
        "desc_bg": "Денонощен телефон на центровете за подкрепа на деца, пострадали или свидетели на насилие, и на техните семейства.",
        "desc_en": "A 24-hour line of the centres supporting children who have suffered or witnessed violence, and their families.",
        "site": "https://www.unicef.org/bulgaria/%D0%B7%D0%BE%D0%BD%D0%B0-%D0%B7%D0%B0%D0%BA%D1%80%D0%B8%D0%BB%D0%B0",
        "site_label": "unicef.org/bulgaria",
        "email": None,
    },
    {
        "badge": "0800 1 8676", "badge_sm_bg": "безплатно", "badge_sm_en": "free",
        "tel": "080018676", "urgent": False,
        "name_bg": "Гореща линия на фондация „Асоциация Анимус“",
        "name_en": "Hotline of the Animus Association Foundation",
        "desc_bg": "Национална гореща телефонна линия за подкрепа и насочване на хора, пострадали от насилие. Обаждането е безплатно.",
        "desc_en": "The national hotline for support and referral of people affected by violence. The call is free of charge.",
        "site": "https://animusassociation.org/programi-uslugi/goreshta-linia/",
        "site_label": "animusassociation.org",
        "email": None,
    },
    {
        "badge": "НМД", "badge_sm_bg": "организация", "badge_sm_en": "NGO",
        "tel": "+359879570178", "urgent": False,
        "name_bg": "Национална мрежа за децата",
        "name_en": "National Network for Children",
        "desc_bg": "Обединение на граждански организации, работещи с и за деца и семейства. Насочва към подходящата услуга в общността.",
        "desc_en": "An alliance of civil-society organisations working with and for children and families. It refers people to the right service in their community.",
        "site": "https://nmd.bg/", "site_label": "nmd.bg",
        "email": "office@nmd.bg",
        "extra_bg": "тел. +359 87 957 0178 · +359 2 444 4380",
        "extra_en": "tel. +359 87 957 0178 · +359 2 444 4380",
    },
    {
        "badge": "Интерпол", "badge_sm_bg": "НЦБ", "badge_sm_en": "NCB",
        "tel": "+35929824351", "urgent": False,
        "name_bg": "Национално централно бюро „Интерпол“",
        "name_en": "Interpol National Central Bureau",
        "desc_bg": "Сигнали за престъпления от международен мащаб, извършени чрез интернет, както и за сексуален туризъм.",
        "desc_en": "Reports of international-scale crimes committed via the internet, as well as sex tourism.",
        "site": "https://www.interpol.int/Who-we-are/Member-countries/Europe/BULGARIA",
        "site_label": "interpol.int",
        "email": None,
    },
]

LOCAL_HELP = [
    (
        "Детска педагогическа стая на МВР",
        "MoI Children’s Pedagogical Room",
        "Инспекторите от детските педагогически стаи работят с деца с противообществени прояви и с деца, пострадали от престъпление. Има такава към районните управления на МВР в цялата страна.",
        "Inspectors at the children’s pedagogical rooms work with children who display antisocial behaviour and with children who have been victims of crime. There is one at district police departments across the country.",
    ),
    (
        "Районно полицейско управление по местоживеене",
        "Your local district police department",
        "Най-бързият път към полицейска реакция по конкретен случай — включително за побой, заплахи и разпространение на записи от насилие.",
        "The fastest route to a police response on a specific case — including assault, threats and the spreading of recorded violence.",
    ),
    (
        "Отдел „Закрила на детето“ към Агенцията за социално подпомагане",
        "Child Protection Department at the Social Assistance Agency",
        "Местната социална служба, която оценява риска за детето и осигурява подкрепа за него и семейството му.",
        "The local social service that assesses the risk to the child and arranges support for the child and the family.",
    ),
    (
        "Класен ръководител, училищен психолог, педагогически съветник",
        "Class teacher, school psychologist, pedagogical counsellor",
        "Първата линия в училище. Училището е длъжно да реагира по механизма за противодействие на тормоза и насилието в институциите в системата на предучилищното и училищното образование.",
        "The first line of response at school. Schools are obliged to act under the mechanism for countering bullying and violence in pre-school and school education institutions.",
    ),
]

# --- Новини (от документа на МВР) -----------------------------------------
NEWS = [
    {
        "id": "n-dpu-shesto",
        "date": "2026-10-02",
        "date_bg": "2 октомври 2026 г.",
        "date_en": "2 October 2026",
        "tag": "mvr", "tag_bg": "МВР", "tag_en": "Ministry of Interior",
        "title_bg": "Стартира шестото издание на националната превантивна програма „Детско полицейско управление“",
        "title_en": "The sixth edition of the national preventive programme “Children’s Police Department” begins",
        "lead_bg": "В училища в цялата страна малките доброволци положиха тържествена клетва и заявиха готовност да спазват Етичния кодекс на Детското полицейско управление.",
        "lead_en": "In schools across the country the young volunteers took their oath and pledged to follow the Code of Ethics of the Children’s Police Department.",
        "sum_en": "The sixth edition of the Ministry of Interior’s national preventive programme opened in schools nationwide. Through practical sessions, demonstrations and meetings with officers, the children will get to know the work of different police structures and gain knowledge about personal safety, road safety, crime prevention and how to react in situations of risk. The programme is also aimed at building a sense of responsibility, discipline, respect for the rules and trust between children and the police.",
        "body_bg": [
            "В училища в цялата страна тържествено бе даден старт на шестото издание на националната превантивна програма на Министерството на вътрешните работи „Детско полицейско управление“. По време на церемониите малките доброволци положиха тържествена клетва и заявиха готовност да спазват Етичния кодекс на Детското полицейско управление.",
            "На официалните откривания децата бяха запознати с основните цели и дейности на програмата, както и с предстоящите занятия, в които ще участват. В рамките на инициативата те ще имат възможност чрез практически занимания, демонстрации и срещи с полицейски служители да се запознаят отблизо с различни аспекти от работата на полицията.",
            "Основната цел на програмата е по достъпен и интересен за децата начин да бъдат формирани знания и умения за безопасно поведение и реакция в различни ситуации. Заниманията са насочени и към изграждане на чувство за отговорност, дисциплина, уважение към правилата и доверие между децата и служителите на реда.",
            "В рамките на програмата доброволците ще се запознаят с дейността на различни полицейски структури и ще придобият практически знания по теми, свързани с личната безопасност, безопасността на движението, превенцията на престъпността и противообществените прояви, както и с начините за реакция при рискови ситуации.",
            "Шестото издание на „Детско полицейско управление“ поставя началото на поредица от образователни и практически инициативи, чрез които децата ще могат да учат, да придобиват нови умения и да се докоснат до професията на полицейския служител.",
        ],
        "src": "https://www.mvr.bg/gdnp/%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%B5%D0%BD-%D1%86%D0%B5%D0%BD%D1%82%D1%8A%D1%80/%D0%BF%D1%80%D0%B5%D1%81%D1%86%D0%B5%D0%BD%D1%82%D1%8A%D1%80/%D0%BD%D0%BE%D0%B2%D0%B8%D0%BD%D0%B8/93298",
        "src_label": "mvr.bg",
    },
    {
        "id": "n-ubiy-skorostta",
        "date": "2026-09-26",
        "date_bg": "26 септември 2026 г.",
        "date_en": "26 September 2026",
        "tag": "mvr", "tag_bg": "МВР", "tag_en": "Ministry of Interior",
        "title_bg": "МВР е партньор на кампанията „Убий скоростта, спаси дете“",
        "title_en": "The Ministry of Interior is a partner of the campaign “Kill the speed, save a child”",
        "lead_bg": "Кампанията е насочена към повишаване на вниманието към безопасността на движението по пътищата и превенцията на пътния травматизъм сред децата.",
        "lead_en": "The campaign is aimed at raising attention to road safety and at preventing road injuries among children.",
        "sum_en": "Officers from the General Directorate National Police, the General Directorate Fire Safety and Civil Protection and the Sofia Directorate presented information and practical demonstrations on road safety, fire safety, police work and police dogs, first aid and the work of volunteer units. A crash simulator let the children feel how much a seat belt matters: a frontal impact at only 7 km/h showed the force of the blow and the risk to unbelted passengers.",
        "body_bg": [
            "МВР е партньор в поредното издание на кампанията „Убий скоростта, спаси дете“ на Радио FM+, насочена към повишаване на вниманието към безопасността на движението по пътищата и превенцията на пътния травматизъм сред децата.",
            "В рамките на инициативата представители на Главна дирекция „Национална полиция“ и Главна дирекция „Пожарна безопасност и защита на населението“ и СДВР представиха информация и практически демонстрации, свързани с безопасността на движението по пътищата, пожарната безопасност, работата на полицейските служители и полицейските кучета, оказването на първа помощ и дейността на доброволческите формирования.",
            "Децата имаха възможност по интересен и достъпен начин да се запознаят с основните правила за безопасно поведение на пътя и да научат повече за отговорното участие в движението. За тях бяха организирани различни игри, предизвикателства и демонстрации с награди.",
            "Особен интерес предизвика специалният „краш симулатор“, чрез който участниците имаха възможност да усетят колко важно е използването на обезопасителен колан в автомобила. Симулацията на челен сблъсък, дори при скорост от едва 7 км/ч, показа нагледно силата на удара и риска за пътниците при непоставен обезопасителен колан.",
            "Чрез кампанията „Убий скоростта, спаси дете“ организаторите и партньорите ѝ отправят апел към всички участници в движението да спазват правилата, да шофират със съобразена скорост и да бъдат особено внимателни, когато на пътя има деца. Безопасността на пътя е споделена отговорност!",
        ],
        "src": "https://www.mvr.bg/gdnp/%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%B5%D0%BD-%D1%86%D0%B5%D0%BD%D1%82%D1%8A%D1%80/%D0%BF%D1%80%D0%B5%D1%81%D1%86%D0%B5%D0%BD%D1%82%D1%8A%D1%80/%D0%BD%D0%BE%D0%B2%D0%B8%D0%BD%D0%B8/93129",
        "src_label": "mvr.bg",
    },
    {
        "id": "n-malkite-geroi",
        "date": "2026-09-08",
        "date_bg": "8 септември 2026 г.",
        "date_en": "8 September 2026",
        "tag": "mvr", "tag_bg": "МВР", "tag_en": "Ministry of Interior",
        "title_bg": "Министър Демерджиев даде началото на инициативата „Малките големи герои“",
        "title_en": "Minister Demerdzhiev launches the “Little Big Heroes” initiative",
        "lead_bg": "Министерството на вътрешните работи ще поощрява добрия пример на деца и младежи, проявили гражданска доблест и отговорност.",
        "lead_en": "The Ministry of Interior will recognise children and young people who have shown civic courage and responsibility.",
        "sum_en": "The initiative highlights children and young people whose actions show courage and responsibility — among the first were a seven-year-old who helped after the floods near Strumyani and four young men who helped police detain a man impersonating a police officer. The Ministry intends to make the initiative permanent and to broaden its scope.",
        "body_bg": [
            "Да помагаш след наводнение, когато си едва на седем години. Да се включиш доброволно в преодоляването на последиците от сериозно бедствие. Да съдействаш на полицията да залови човек, представящ се за служител на реда. Това са част от първите истории в инициативата „Малките големи герои“, чието начало постави днес министър Иван Демерджиев. Идеята е Министерството на вътрешните работи да насочи общественото внимание към деца и младежи, чиито действия показват смелост, отговорност и гражданска доблест — добрите примери, които често остават встрани от него.",
            "„В последните седмици младите хора често попадаха във фокуса на обществото с негативни прояви. Ние искаме да се знае, че голяма част от българските младежи правят точно обратното — носят ценности, достойни за уважение, и дават добър пример“, заяви в своето изказване министър Демерджиев. По думите му превенцията не се изчерпва с реакцията срещу негативното поведение. Не по-малко важно е обществото да вижда и да оценява постъпките, които заслужават подражание.",
            "Най-малкият сред първите герои на инициативата е само на седем години. Димитър Стоянов завел със себе си своя син Владислав, за да помагат при преодоляването на последиците от тежкото наводнение в района на Струмяни. „Да заведеш седемгодишния си син там и да го научиш как се действа в такава ситуация, за мен е проява на доблест“, посочи при награждаването им вътрешният министър.",
            "За помощта си след бедствието в Струмяни бяха наградени още Николай Гутев, Христо Аврамски, Мартин Христов, Борислав Атанасов и Генади Танев. Други четирима младежи — Християн Кочев, Виктор Карушев, Александър Ваков и Андриян Кръстев — получиха признание за отговорното си поведение и проявения граждански дълг. Четиримата са помогнали за установяването и задържането на криминално проявен мъж, представял се за полицейски служител.",
            "Началото на „Малките големи герои“ е вдъхновено от още две отговорни момчета — 16-годишния Стилиян Трендафилов и 17-годишния Тонислав Леков, наградени за проявената смелост при спасяването на село Кошарица от голям пожар. Амбицията на Министерството на вътрешните работи е инициативата не само да се превърне в постоянна, но и да разшири обхвата си.",
        ],
        "src": "https://mvr.bg/press/%D0%B0%D0%BA%D1%82%D1%83%D0%B0%D0%BB%D0%BD%D0%B0-%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D1%8F/%D0%B0%D0%BA%D1%82%D1%83%D0%B0%D0%BB%D0%BD%D0%B0-%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D1%8F/%D0%BD%D0%BE%D0%B2%D0%B8%D0%BD%D0%B8/92768",
        "src_label": "mvr.bg",
    },
    {
        "id": "n-da-rastesh-onlain",
        "date": "2026-09-03",
        "date_bg": "3 септември 2026 г.",
        "date_en": "3 September 2026",
        "tag": "unicef", "tag_bg": "УНИЦЕФ", "tag_en": "UNICEF",
        "title_bg": "Да растеш онлайн: децата искат повече разбиране и подкрепа в дигиталния свят",
        "title_en": "Growing up online: children want more understanding and support in the digital world",
        "lead_bg": "Нови данни от изследване на УНИЦЕФ България и глобално проучване на платформата U-Report показват, че интернет е неразделна част от живота на децата, но възрастните често не разбират в пълна степен как младите хора преживяват дигиталната среда.",
        "lead_en": "New data from a UNICEF Bulgaria study and a global U-Report survey show that the internet is inseparable from children’s lives, yet adults often do not fully understand how young people experience the digital environment.",
        "sum_en": "Over a third of Bulgarian pupils (37%) started using the internet before the age of 8 and nearly 80% were active online before turning 10. More than half spend over four hours a day online in their free time. Faced with shocking content, 41% say they would tell no one; over a fifth report having experienced online bullying, most often from peers, and only 11% turn to a teacher or school specialist. The study — “Growing up online: children, the digital environment and safety” — was carried out by the Bulgarian Safer Internet Centre, the Parents Association and UNICEF.",
        "body_bg": [
            "„Да растеш онлайн: деца, дигитална среда и безопасност“ е изследване с участието на деца, родители и професионалисти от образователната система в България, реализирано съвместно от Националния център за безопасен интернет, Асоциация Родители и УНИЦЕФ.",
            "Резултатите показват, че дигиталният живот на децата у нас започва все по-рано. Над една трета от учениците (37%) са започнали да използват интернет преди 8-годишна възраст, а близо 80% вече са активни онлайн още преди да навършат 10 години. Почти всички ученици над 12-годишна възраст разполагат със собствен смартфон. Повече от половината деца прекарват над четири часа на ден онлайн в свободното си време, а приблизително една четвърт — повече от шест часа дневно, като няма разлика между момичетата и момчетата.",
            "Една от основните констатации в доклада е разликата между начина, по който децата преживяват дигиталната среда, и начина, по който възрастните я възприемат. Близо 80% от учениците ежедневно общуват онлайн с приятели, 62% търсят информация за училище, а 64% — за лични интереси. За разлика от тях възрастните по-често се фокусират върху потенциалните рискове.",
            "Особено тревожни са данните, които сочат, че децата трудно споделят за притеснителни преживявания онлайн. При среща с шокиращо съдържание 41% от учениците посочват, че не биха споделили с никого. Над една пета от учениците съобщават, че са преживели онлайн тормоз, като в повечето случаи той идва от връстници и съученици. В тези случаи 44% от децата споделят с родител или друг възрастен, но само 11% търсят подкрепа от учител или училищен специалист.",
            "Наблюдаваните в България тенденции намират потвърждение и в глобалното проучване „Животът онлайн“ на младежката платформа U-Report на УНИЦЕФ, в което са участвали над 211 000 деца от 119 държави. Данните показват, че онлайн безопасността не може да бъде постигната единствено чрез ограничения и контрол — необходим е цялостен подход, който започва още в ранна възраст и последователно развива дигитална и медийна грамотност, критично мислене и социално-емоционални умения.",
        ],
        "src": "https://www.unicef.org/bulgaria/%D0%BF%D1%80%D0%B5%D1%81-%D1%81%D1%8A%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D1%8F/%D0%B4%D0%B0-%D1%80%D0%B0%D1%81%D1%82%D0%B5%D1%88-%D0%BE%D0%BD%D0%BB%D0%B0%D0%B9%D0%BD-%D0%B4%D0%B5%D1%86%D0%B0%D1%82%D0%B0-%D0%B8%D1%81%D0%BA%D0%B0%D1%82-%D0%BF%D0%BE%D0%B2%D0%B5%D1%87%D0%B5-%D1%80%D0%B0%D0%B7%D0%B1%D0%B8%D1%80%D0%B0%D0%BD%D0%B5-%D0%B8-%D0%BF%D0%BE%D0%B4%D0%BA%D1%80%D0%B5%D0%BF%D0%B0-%D0%B2-%D0%B4%D0%B8%D0%B3%D0%B8%D1%82%D0%B0%D0%BB%D0%BD%D0%B8%D1%8F-%D1%81%D0%B2%D1%8F%D1%82",
        "src_label": "unicef.org/bulgaria",
    },
    {
        "id": "n-obrashtenie",
        "date": "2026-08-10",
        "date_bg": "10 август 2026 г.",
        "date_en": "10 August 2026",
        "tag": "mvr", "tag_bg": "МВР", "tag_en": "Ministry of Interior",
        "title_bg": "Обръщение на министъра на вътрешните работи Иван Демерджиев към родителите",
        "title_en": "Address by Interior Minister Ivan Demerdzhiev to parents",
        "lead_bg": "„Обръщам се към Вас не само като министър, но преди всичко като баща.“ Министърът предупреждава за радикализацията на деца в затворени онлайн групи и призовава родителите да бъдат присъстващи в живота на децата си.",
        "lead_en": "“I address you not only as a minister, but above all as a father.” The minister warns about the radicalisation of children in closed online groups and calls on parents to be present in their children’s lives.",
        "sum_en": "The minister describes a series of meetings with cybersecurity experts and social-media analysts tracking online radicalisation, and says the state had underestimated the scale of the digital manipulation of children. He argues that recorded beatings and humiliations uploaded as trophies are no longer isolated incidents but an ecosystem, and that closed online groups teach children that cruelty is strength and empathy is weakness. His central message to parents: know your children, know their circles, and be present — the state can shut down a network, but it cannot replace a parent.",
        "body_bg": [
            "„Обръщам се към Вас не само като министър, но преди всичко като баща, чието търпение е изчерпано.“",
            "Министърът посочва, че когато насилието се превръща в съдържание за социалните мрежи, обществото вече не говори за престъпност, а за патология. По думите му този разпад не започва днес — през последните двадесет години децата са станали свидетели на системна безнаказаност, в която законът се възприема като досадна подробност, а агресията — като най-прекият път към успеха.",
            "„Държавата няма как да замени семейството, нито може да компенсира отсъствието на родителя в процеса на израстване на неговото дете. Колкото и здрави основи да полагаме у дома, моралният компас на детето се калибрира в училище, сред приятелите, в разговорите онлайн и в онова, което подрастващите консумират всеки ден в социалните мрежи. Ако не познаваш детето си — не го възпитаваш. Ако не познаваш приятелите му — не го защитаваш. Ако не знаеш с кого говори и какво вижда в телефона си — не присъстваш в живота му.“",
            "Министърът отбелязва, че побоищата и униженията, които се записват и качват като трофей, вече не са случайни инциденти, а екосистема. През последния месец той е провел поредица от срещи с експерти по киберсигурност и анализатори на социалните мрежи, които проследяват радикализацията онлайн. „Досега държавата често подценяваше мащаба на дигиталната обработка на децата ни, но този период на институционално пренебрежение приключва. Виждаме ясни признаци, че част от тези деца се радикализират в затворени онлайн групи и през социалните мрежи, където им се внушава, че жестокостта е сила, а емпатията е слабост.“",
            "Обръщението завършва с призив към родителите: „Това е процес, в който родителите не са публика, а първа линия на защитата. Познавайте децата си. Следете кръговете им. Бъдете там — не с контрол на страха, а с присъствие, подкрепа и като морален компас. Защото държавата може да затвори мрежа. Може да заличи групи. Може да арестува престъпник. Но държавата никога не може да замени родителя, който е избрал да не бъде там.“",
        ],
        "src": "https://www.facebook.com/ivandemerdzhiev/posts/1456205509670966",
        "src_label": "facebook.com",
    },
    {
        "id": "n-nasilieto-e-bezsilie",
        "date": "",
        "date_bg": "",
        "date_en": "",
        "tag": "campaign", "tag_bg": "Кампания", "tag_en": "Campaign",
        "title_bg": "Съвместната инициатива на МВР и МОН „Насилието е безсилие“ достига до минимум 100 000 ученици в над 1000 училища",
        "title_en": "The joint MoI–MoES campaign “Violence is powerlessness” reaches at least 100,000 pupils in over 1,000 schools",
        "lead_bg": "Засилват се превенцията при работата с деца и мониторингът на социалните мрежи. МВР подготвя изцяло нов закон за противодействие на противообществените прояви на малолетни и непълнолетни.",
        "lead_en": "Prevention in work with children and the monitoring of social networks are both being stepped up. The Ministry of Interior is drafting an entirely new law on countering antisocial behaviour by minors.",
        "sum_en": "The Ministry of Interior is preparing a new law on countering antisocial acts by minors, replacing legislation it describes as outdated. Prevention is a central focus: a training strategy for officers who work with children, including inspectors at children’s pedagogical rooms, and early-identification mechanisms for aggressive and risky behaviour. Officers of the Cybercrime Directorate at GDBOP monitor the internet daily for content linked to unlawful acts, and the Ministry is exploring territorial cybercrime units. The “Violence is powerlessness” campaign, currently aimed at pupils in grades VIII and IX, is planned to reach at least 100,000 pupils in over 1,000 schools.",
        "body_bg": [
            "Министерството на вътрешните работи подготвя изцяло нов закон за противодействие на противообществените прояви на малолетни и непълнолетни. Амбицията е в кратки срокове работата да приключи и да бъде предложен проект на съвременен нормативен акт, който да осигури ефективна превенция при работата с децата. Действащата нормативна уредба е остаряла и не отговаря на съвременните условия и предизвикателства.",
            "Наред с подготовката на новия закон се обсъжда и промяна във функционирането на структурите, ангажирани с противообществените прояви на малолетни и непълнолетни, с цел повишаване на капацитета и ефективността на тяхната работа. Сред основните акценти е засилването на превенцията. МВР разработва стратегия за допълнително обучение на служителите, които работят с деца, включително инспекторите от детските педагогически стаи — за да се изградят работещи механизми за ранно идентифициране и предотвратяване на агресивно и рисково поведение.",
            "Засилен е и мониторингът на интернет пространството. Служителите на дирекция „Киберпрестъпност“ при ГДБОП ежедневно следят за съдържание, свързано с противоправни прояви, а при установени данни за престъпления информацията се насочва към компетентните структури. МВР работи и по възможността за изграждане на териториални звена за противодействие на киберпрестъпността, за да бъде увеличен капацитетът за работа в цялата страна.",
            "Обсъжда се и създаването на работна група с участието на Министерството на правосъдието, която да направи преглед на съответните разпоредби в Наказателния кодекс и доколко те са адекватни спрямо тежестта на отделните прояви и действащата европейска регламентация.",
            "Министерството на вътрешните работи и Министерството на образованието и науката ще разширят съвместните си превантивни инициативи. Сред тях е кампанията „Насилието е безсилие“, която в момента е насочена към ученици от VIII и IX клас. Предвижда се през следващата учебна година тя да достигне до минимум 100 000 ученици в над 1000 училища в страната.",
        ],
        "src": "https://www.mvr.bg/press/%D0%B0%D0%BA%D1%82%D1%83%D0%B0%D0%BB%D0%BD%D0%B0-%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D1%8F/%D0%B0%D0%BA%D1%82%D1%83%D0%B0%D0%BB%D0%BD%D0%B0-%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D1%8F/%D0%BD%D0%BE%D0%B2%D0%B8%D0%BD%D0%B8/92457",
        "src_label": "mvr.bg",
    },
    {
        "id": "n-gdnp-programa",
        "date": "",
        "date_bg": "",
        "date_en": "",
        "tag": "gdnp", "tag_bg": "ГДНП", "tag_en": "National Police",
        "title_bg": "Националната програма „Насилието е безсилие“ стартира в столични училища",
        "title_en": "The national programme “Violence is powerlessness” starts in Sofia schools",
        "lead_bg": "През учебната 2025/2026 година учениците от 8. и 9. клас в пет столични училища ще се обучават да разпознават домашното насилие и оскърбителното поведение.",
        "lead_en": "In the 2025/2026 school year, pupils in grades 8 and 9 at five Sofia schools will learn to recognise domestic violence and abusive behaviour.",
        "sum_en": "Developed by a multidisciplinary team on an idea from the Domestic Violence sector at the General Directorate National Police, the programme teaches pupils to recognise early warning signs, build self-respect and boundaries, and know they have a right to a healthy, supportive and safe relationship. It was approved by Interior Minister Daniel Mitov and Education Minister Krasimir Valchev, and is piloted in five Sofia schools.",
        "body_bg": [
            "През новата учебна година — 2025/2026, учениците от 8. – 9. клас в пет столични училища в часовете на класа ще се обучават да разпознават домашното насилие и оскърбителното поведение, да мобилизират своите способности, да се научат да отреагират на травматични преживявания, да премахнат чувството за вина и да повишат самооценката си.",
            "Националната програма „Насилието е безсилие“, изготвена от мултидисциплинарен екип по идея на сектор „Домашно насилие“ в ГДНП, бе представена на работна среща с представители на пилотните пет столични училища — СПГ „Княгиня Евдокия“, 40 СУ „Луи Пастьор“, 96 СУ, Професионална гимназия по облекло „Кн. Мария Луиза“ и 33 Езикова гимназия „Света София“.",
            "Старши комисар Иван Маджаров, заместник-директор на Главна дирекция „Национална полиция“, посочи, че целта не е просто младежите да бъдат информирани какво е токсична връзка, а да ги научим да разпознават ранните сигнали, да изграждат самоуважение и граници, да знаят, че имат право на здрава, подкрепяща и безопасна връзка — независимо от модела, който са виждали у дома. Той допълни, че е важно децата да разберат, че имат правото и силата да променят живота си чрез своите избори.",
            "„Сърцевината на превенцията е да изградим чувствителност и разбиране у младото поколение срещу насилието във всичките му проявления. Съвместната ни работа има потенциала да осветли не само темата с насилието, но и да даде възможност да се прекъсне предаването му в поколенията“, отбеляза главен инспектор Зорница Шуманова, национален координатор по линия на домашното насилие и началник на сектор „Домашно насилие“ в ГДНП.",
            "Националната програма „Насилието е безсилие“ е утвърдена от министъра на вътрешните работи Даниел Митов и министъра на образованието и науката Красимир Вълчев.",
        ],
        "src": "https://www.mvr.bg/gdnp/%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%B5%D0%BD-%D1%86%D0%B5%D0%BD%D1%82%D1%8A%D1%80/%D0%BF%D1%80%D0%B5%D1%81%D1%86%D0%B5%D0%BD%D1%82%D1%8A%D1%80/%D0%BD%D0%BE%D0%B2%D0%B8%D0%BD%D0%B8/84398",
        "src_label": "mvr.bg/gdnp",
    },
]

# --- Полезни връзки --------------------------------------------------------
RESOURCES = [
    {
        "url": "https://smarty-kids.bg/zaedno/",
        "host": "smarty-kids.bg",
        "title_bg": "„Заедно можем повече“ — за свят без агресия",
        "title_en": "“Together we can do more” — for a world without aggression",
        "desc_bg": "Кампания за превенция на агресията сред деца с материали и дейности за класната стая и за вкъщи.",
        "desc_en": "A campaign for preventing aggression among children, with materials and activities for the classroom and for home.",
    },
    {
        "url": "https://www.unicef.org/bulgaria/%D0%BD%D0%B0%D1%81%D0%B8%D0%BB%D0%B8%D0%B5-%D0%BD%D0%B0%D0%B4-%D0%B4%D0%B5%D1%86%D0%B0",
        "host": "unicef.org/bulgaria",
        "title_bg": "Насилие над деца — УНИЦЕФ България",
        "title_en": "Violence against children — UNICEF Bulgaria",
        "desc_bg": "Какво е насилие над дете, как се разпознава и как да сигнализираш за дете в риск или жертва на насилие.",
        "desc_en": "What violence against a child is, how to recognise it, and how to report a child at risk or a victim of violence.",
    },
    {
        "url": "https://www.unicef.org/bulgaria/%D1%81%D1%82%D1%8A%D0%BF%D0%BA%D0%B8-%D0%B7%D0%B0%D0%B5%D0%B4%D0%BD%D0%BE-%D0%B7%D0%B0-%D0%B4%D0%B0-%D1%81%D0%BF%D1%80%D0%B5%D0%BC-%D0%BD%D0%B0%D1%81%D0%B8%D0%BB%D0%B8%D0%B5%D1%82%D0%BE-%D0%B2-%D1%83%D1%87%D0%B8%D0%BB%D0%B8%D1%89%D0%B5",
        "host": "unicef.org/bulgaria",
        "title_bg": "„Стъпки заедно“ — за да спрем насилието в училище",
        "title_en": "“Steps together” — to stop violence at school",
        "desc_bg": "Програмата на УНИЦЕФ и Министерството на образованието и науката за сигурна и безопасна учебна и онлайн среда.",
        "desc_en": "The programme of UNICEF and the Ministry of Education and Science for a secure and safe learning and online environment.",
    },
    {
        "url": "https://gloriouswinner.com/tormoz-v-uchilishte/",
        "host": "gloriouswinner.com",
        "title_bg": "Тормоз в училище: истини и решения",
        "title_en": "Bullying at school: truths and solutions",
        "desc_bg": "Практични съвети към деца, родители и учители за разпознаване и спиране на училищния тормоз.",
        "desc_en": "Practical advice for children, parents and teachers on recognising and stopping school bullying.",
    },
    {
        "url": "https://www.unicef.org/bulgaria/documents/%D0%B4%D0%B0-%D1%80%D0%B0%D1%81%D1%82%D0%B5%D1%88-%D0%BE%D0%BD%D0%BB%D0%B0%D0%B9%D0%BD-%D0%B4%D0%B5%D1%86%D0%B0-%D0%B4%D0%B8%D0%B3%D0%B8%D1%82%D0%B0%D0%BB%D0%BD%D0%B0-%D1%81%D1%80%D0%B5%D0%B4%D0%B0-%D0%B8-%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82",
        "host": "unicef.org/bulgaria",
        "title_bg": "ДОКЛАД: „Да растеш онлайн: деца, дигитална среда и безопасност“",
        "title_en": "REPORT: “Growing up online: children, the digital environment and safety”",
        "desc_bg": "Проучване сред ученици от 5. до 12. клас, родители, учители и училищни специалисти — за онлайн рисковете, онлайн тормоза, изкуствения интелект и дигитално-медийната грамотност.",
        "desc_en": "A study among pupils in grades 5–12, parents, teachers and school specialists — on online risks, online bullying, artificial intelligence and digital media literacy.",
    },
    {
        "url": "https://www.cybercrime.bg/",
        "host": "cybercrime.bg",
        "title_bg": "Дирекция „Киберпрестъпност“ — ГДБОП",
        "title_en": "Cybercrime Directorate — GDBOP",
        "desc_bg": "Официалният сайт на дирекция „Киберпрестъпност“: сигнали за вредно и незаконно съдържание в българското интернет пространство.",
        "desc_en": "The official site of the Cybercrime Directorate: reports of harmful and illegal content in the Bulgarian internet space.",
    },
]


# ==========================================================================
#  Рендериране на повтарящи се блокове / repeated block rendering
# ==========================================================================


def _fmt_tel(t):
    """+35929828363 -> +359 2 982 83 63"""
    if not t.startswith("+359"):
        return t
    rest = t[4:]
    if rest.startswith("2"):                             # София / Sofia
        r = rest[1:]
        if len(r) == 7:
            return "+359 2 %s %s %s" % (r[:3], r[3:5], r[5:])
        return "+359 2 " + r
    if len(rest) == 9:                                   # мобилен / mobile
        return "+359 %s %s %s" % (rest[:2], rest[2:5], rest[5:])
    return "+359 " + rest


def render_helpline(item):
    # Ако значката е телефонен номер — води към набиране; иначе към сайта.
    # If the badge is a phone number it dials; otherwise it opens the site.
    numeric = item["badge"].replace(" ", "").isdigit()
    href = ("tel:" + item["tel"]) if numeric else item["site"]
    target = "" if numeric else ' target="_blank" rel="noopener"'
    tel = '<a class="helpline__badge" href="%s"%s>%s<small>%s</small></a>' % (
        href, target, item["badge"], bi(item["badge_sm_bg"], item["badge_sm_en"])
    )
    meta = []
    if item.get("extra_bg"):
        meta.append(bi(item["extra_bg"], item["extra_en"]))
    elif item.get("tel") and not numeric:
        pretty = _fmt_tel(item["tel"])
        meta.append(bi('тел. <a href="tel:%s">%s</a>' % (item["tel"], pretty),
                       'tel. <a href="tel:%s">%s</a>' % (item["tel"], pretty)))
    if item.get("email"):
        meta.append('<a href="mailto:%s">%s</a>' % (item["email"], item["email"]))
    meta.append('<a href="%s" target="_blank" rel="noopener">%s</a>' % (item["site"], item["site_label"]))
    return """<article class="helpline{urg}">
  {badge}
  <div class="helpline__body">
    {name}
    {desc}
  </div>
  <div class="helpline__meta">{meta}</div>
  <div class="helpline__go"><a class="btn btn--ghost btn--sm" href="{site}" target="_blank" rel="noopener">{go}</a></div>
</article>""".format(
        urg=" helpline--urgent" if item["urgent"] else "",
        badge=tel,
        name=h(3, item["name_bg"], item["name_en"]),
        desc=p(item["desc_bg"], item["desc_en"]),
        meta="".join("<span>%s</span>" % m for m in meta),
        site=item["site"],
        go=bi("Към сайта", "Visit site"),
    )


def render_news(item, expandable=True):
    date_html = ""
    if item["date_bg"]:
        date_html = '<time datetime="%s">%s</time>' % (
            item["date"], bi(item["date_bg"], item["date_en"])
        )
    body_bg = "".join("<p>%s</p>" % x for x in item["body_bg"])
    body = """<div class="newscard__body" id="{i}-body" hidden>
      <div lang="bg">{bg}</div>
      <div lang="en"><p>{en}</p><p class="note">{note}</p></div>
    </div>""".format(i=item["id"], bg=body_bg, en=item["sum_en"],
                     note="The full text of this statement is published in Bulgarian on the source page linked below.")

    toggle = """<button class="btn btn--ghost" type="button" data-expand="{i}-body" aria-expanded="false" aria-controls="{i}-body">
        <span lang="bg" data-label-open="Прочети повече" data-label-close="Скрий">Прочети повече</span><span lang="en" data-label-open="Read more" data-label-close="Hide">Read more</span>
      </button>""".format(i=item["id"])

    return """<article class="newscard" id="{i}">
  <div class="newscard__meta">
    <span class="tag tag--{tag}">{tagl}</span>
    {date}
  </div>
  {title}
  <p class="newscard__lead"><span lang="bg">{lead_bg}</span><span lang="en">{lead_en}</span></p>
  {body}
  <div class="newscard__foot">
    {toggle}
    <a class="linkout" href="{src}" target="_blank" rel="noopener"><span>{srct}:&nbsp;{srcl}&nbsp;&#8599;</span></a>
  </div>
</article>""".format(
        i=item["id"],
        tag=item["tag"],
        tagl=bi(item["tag_bg"], item["tag_en"]),
        date=date_html,
        title=h(2, item["title_bg"], item["title_en"]),
        lead_bg=item["lead_bg"],
        lead_en=item["lead_en"],
        body=body if expandable else "",
        toggle=toggle if expandable else "",
        src=item["src"],
        srct=bi("Източник", "Source"),
        srcl=item["src_label"],
    )


def render_resource(r):
    return """<a class="reslink" href="{url}" target="_blank" rel="noopener">
  <span class="reslink__host">{host}</span>
  {title}
  {desc}
</a>""".format(
        url=r["url"], host=r["host"],
        title=h(3, r["title_bg"], r["title_en"]),
        desc=p(r["desc_bg"], r["desc_en"]),
    )


# ==========================================================================
#  СТРАНИЦИ / PAGES
# ==========================================================================


SLIDES = [
    ("slide-1-velosiped", "Полицейски служител поздравява дете на велосипед на площадка за пътна безопасност"),
    ("slide-2-petichka", "Деца в светлоотразителни жилетки поздравяват полицейски служител"),
    ("slide-3-dete-policay", "Полицейски служител с дете по време на кампания"),
    ("slide-4-dvorec", "Полицейски служители с деца пред Националния дворец на децата"),
    ("slide-5-prehod", "Полицейски служители помагат на деца на пешеходна пътека"),
    ("slide-6-poligon", "Деца на обучителен полигон по безопасност на движението"),
]


def slides_html():
    """Ротацията — само снимки, без надписи / carousel — pictures only."""
    return "".join(
        '<div class="slide">%s</div>' % pic(
            f, alt, sizes="(max-width: 760px) 92vw, (max-width: 1100px) 46vw, 31vw",
            eager=(i == 0))
        for i, (f, alt) in enumerate(SLIDES)
    )


def build_index():
    teasers = "".join(
        """<a class="newsteaser" href="news.html#{i}">
      {d}
      {t}
      {l}
    </a>""".format(
            i=n["id"],
            d=('<time datetime="%s">%s</time>' % (n["date"], bi(n["date_bg"], n["date_en"]))) if n["date_bg"] else "",
            t=h(3, n["title_bg"], n["title_en"]),
            l=p(n["lead_bg"][:150] + "…", n["lead_en"][:150] + "…"),
        )
        for n in NEWS[:3]
    )

    body = """
<section class="hero">
  <div class="wrap hero__inner">
    <div>
      <span class="eyebrow">{eyebrow}</span>
      {h1}
      {sub}
      <div class="btn-row hero__actions">
        <a class="btn btn--lg btn--danger" href="report.html">{cta1}</a>
        <a class="tlink" href="bullying.html#types" style="margin-left:6px">{cta2}</a>
      </div>
    </div>
    <aside class="hero__panel">
      {panelh}
      <ul>
        <li><a href="tel:112"><span><span class="lbl">{l112}</span></span><span class="num">112</span></a></li>
        <li><a href="tel:116111"><span><span class="lbl">{l116}</span></span><span class="num">116 111</span></a></li>
        <li><a href="https://www.cybercrime.bg/" target="_blank" rel="noopener"><span class="hp-lbl">{hpe1}<span class="lbl">{lcyber}</span></span><span class="num">cybercrime.bg</span></a></li>
        <li><a href="https://gdbop.bg/" target="_blank" rel="noopener"><span class="hp-lbl">{hpe2}<span class="lbl">{lgdbop}</span></span><span class="num">gdbop.bg</span></a></li>
        <li><a href="https://www.mvr.bg/" target="_blank" rel="noopener"><span class="hp-lbl">{hpe3}<span class="lbl">{lmvr}</span></span><span class="num">mvr.bg</span></a></li>
      </ul>
    </aside>
  </div>
  <div class="wrap">
    <figure class="heroshot">{heroimg}</figure>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="platform">
      <div>
        <span class="eyebrow">{pl_eye}</span>
        {pl_h}
      </div>
      <div>{pl_p}</div>
    </div>
  </div>
</section>

<section class="section--carousel">
  <div class="wrap">
    <div class="carousel" data-carousel aria-roledescription="carousel" aria-label="{car_label}">
      <div class="carousel__track" id="car-track">
        {slides}
      </div>
      <button class="carousel__btn carousel__btn--prev" type="button" data-car="prev" aria-label="{car_prev}">&#8249;</button>
      <button class="carousel__btn carousel__btn--next" type="button" data-car="next" aria-label="{car_next}">&#8250;</button>
      <div class="carousel__dots" role="tablist" aria-label="{car_dots}"></div>
    </div>
  </div>
</section>

<section class="section section--sky">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{feye}</span>
      {fh}
      {fp}
    </div>
    <div class="grid grid--3">
      <div class="facet facet--to">
        <span class="facet__tag">{f1t}</span>
        {f1h}{f1p}
      </div>
      <div class="facet facet--from">
        <span class="facet__tag">{f2t}</span>
        {f2h}{f2p}
      </div>
      <div class="facet facet--between">
        <span class="facet__tag">{f3t}</span>
        {f3h}{f3p}
      </div>
    </div>
    <p class="note" style="margin-top:24px">{fnote}</p>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="callout callout--amber">
      {msgh}
      <blockquote><span lang="bg">„Агресията е сигнал — за проблем, страх, умора, емоция, загуба на контрол.“</span><span lang="en">“Aggression is a signal — of a problem, of fear, of exhaustion, of emotion, of a loss of control.”</span></blockquote>
      {msgp}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{qeyebrow}</span>
      {qh}
      {qp}
    </div>
    <div class="grid grid--4">
      <a class="card card--link card--action" href="help.html#linii">
        {c1h}{c1p}
        <span class="tlink">{c1b}</span>
      </a>
      <a class="card card--link card--action" href="bullying.html#types">
        {c2h}{c2p}
        <span class="tlink">{c2b}</span>
      </a>
      <a class="card card--link card--action" href="advice.html#roli">
        {c3h}{c3p}
        <span class="tlink">{c3b}</span>
      </a>
      <a class="card card--link card--action" href="resources.html#vrazki">
        {c4h}{c4p}
        <span class="tlink">{c4b}</span>
      </a>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{seyebrow}</span>
      {sh}
      {sp}
    </div>
    <div class="grid grid--4">
      <div class="stat"><div class="stat__num">47%</div>{s1}</div>
      <div class="stat"><div class="stat__num">45,9%</div>{s2}</div>
      <div class="stat"><div class="stat__num">31,2%</div>{s3}</div>
      <div class="stat"><div class="stat__num">14%</div>{s4}</div>
    </div>
    <p class="note" style="margin-top:22px">{snote}</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{neyebrow}</span>
      {nh}
    </div>
    <div class="grid grid--3">
      {teasers}
    </div>
    <div class="btn-row" style="margin-top:28px">
      <a class="btn btn--primary" href="news.html">{nall}</a>
    </div>
  </div>
</section>

<section class="section section--rose">
  <div class="wrap">
    <div class="callout callout--navy">
      <div class="grid grid--2" style="align-items:center;gap:30px">
        <div>
          {reph}
          {repp}
        </div>
        <div class="btn-row">
          <a class="btn btn--light btn--lg" href="https://www.cybercrime.bg/" target="_blank" rel="noopener">cybercrime.bg</a>
          <a class="btn btn--outline-light btn--lg" href="https://gdbop.bg/" target="_blank" rel="noopener">gdbop.bg</a>
          <a class="btn btn--outline-light btn--lg" href="tel:112">112</a>
        </div>
      </div>
    </div>
  </div>
</section>
""".format(
        eyebrow=bi("Министерство на вътрешните работи",
                   "Ministry of Interior of the Republic of Bulgaria"),
        h1=h(1, "Агресията не е детска игра.",
             "Aggression is not child’s play."),
        sub=p(
            "Удар в междучасието, подигравка в групата, заплаха в съобщение. Агресията в детския свят има "
            "много лица — и когато детето е жертва, и когато то самото посяга. Тук ще намерите как се "
            "разпознава, как се реагира и към кого да се обърнете — веднага.",
            "A blow at break time, mockery in the group chat, a threat in a message. Aggression in the world of "
            "children has many faces — when a child is the victim, and when a child is the one lashing out. Here "
            "you will find how to recognise it, how to respond and whom to turn to — straight away.",
            cls="lede",
        ),
        cta1=bi("Подай сигнал", "File a report"),
        cta2=bi("Какво е агресия?", "What is aggression?"),
        panelh=h(2, "Бърза помощ", "Quick help"),
        l112=bi("Спешен телефон, денонощно", "Emergency number, 24/7"),
        l116=bi("Линия за деца, безплатна", "Child helpline, free"),
        hpe1=emblem("cybercrime-gdbop", cls="hp-emblem", w=341, h=420, lazy=False),
        hpe2=emblem("gdbop-mvr", cls="hp-emblem hp-emblem--round", w=256, h=256, lazy=False),
        lcyber=bi("Сигнал за незаконно съдържание", "Report illegal content"),
        lgdbop=bi("Сигнал до ГДБОП", "Report to GDBOP"),
        hpe3=emblem("mvr-nacionalna-policiya", cls="hp-emblem", w=153, h=192, lazy=False),
        lmvr=bi("Министерство на вътрешните работи", "Ministry of Interior"),
        feye=bi("Трите посоки", "The three directions"),
        fh=h(2, "Агресията в детския свят", "Aggression in the world of children"),
        fp=p("Не е само онлайн и не е само в училище. Агресията идва от три посоки и всяка иска различен отговор.",
             "It is not only online and not only at school. Aggression comes from three directions, and each calls for a different answer.",
             cls="lede"),
        f1t=bi("Към детето", "Against a child"),
        f1h=h(3, "Когато детето е жертва", "When the child is the victim"),
        f1p=p("Побой, заплахи, изнудване, подигравки, изключване от групата, разпространение на снимки и записи. "
              "Насилие може да идва и от възрастен — вкъщи, в училище или онлайн.",
              "Beatings, threats, extortion, mockery, exclusion from the group, the spreading of photos and recordings. "
              "Violence can also come from an adult — at home, at school or online."),
        f2t=bi("От детето", "By a child"),
        f2h=h(3, "Когато детето посяга", "When the child lashes out"),
        f2p=p("Зад агресивното поведение почти винаги стои нещо друго — страх, безсилие, преживяно насилие, "
              "подражание. Детето, което удря, също има нужда от помощ, а не само от наказание.",
              "There is almost always something behind aggressive behaviour — fear, powerlessness, violence already "
              "experienced, imitation. The child who hits needs help too, not only punishment."),
        f3t=bi("Между децата", "Between children"),
        f3h=h(3, "Когато класът участва", "When the class takes part"),
        f3p=p("Тормозът рядко е между двама. Около него има подбудители, помощници и мълчаливи свидетели. "
              "Той спира тогава, когато групата спре да го поддържа.",
              "Bullying is rarely between two people. Around it there are instigators, assistants and silent witnesses. "
              "It stops when the group stops sustaining it."),
        fnote=bi(
            "Едно дете често минава и през трите роли. Затова сайтът не дели децата на „лоши“ и „добри“, а говори за поведение, което може да се промени.",
            "One child often passes through all three roles. That is why this site does not divide children into “bad” and “good”, but speaks about behaviour that can change.",
        ),
        msgh=h(2, "Посланието", "The message"),
        msgp=p(
            "Зад агресивното поведение почти винаги стои нещо друго. Това не оправдава насилието — "
            "но обяснява защо наказанието само по себе си не помага. Работещата защита започва с разпознаване, "
            "разговор и навременна намеса на възрастен, на когото детето вярва.",
            "There is almost always something else behind aggressive behaviour. That does not excuse violence — "
            "but it explains why punishment on its own does not help. Effective protection starts with recognition, "
            "conversation and the timely involvement of an adult the child trusts.",
        ),
        qeyebrow=bi("Откъде да започна", "Where to start"),
        qh=h(2, "Четири пътя напред", "Four ways forward"),
        qp=p("Изберете това, което ви е нужно точно сега.",
             "Choose what you need right now.", cls="lede"),
        c1h=h(3, "Случва се сега", "It’s happening now"),
        c1p=p("Телефони, институции и онлайн канали за сигнал — подредени по спешност.",
              "Phone numbers, institutions and online reporting channels — ordered by urgency."),
        c1b=bi("Потърси помощ", "Get help"),
        c2h=h(3, "Разпознай тормоза", "Recognise bullying"),
        c2p=p("Видовете агресия, признаците у детето и как да реагирате правилно.",
              "The types of aggression, the signs in a child and how to respond properly."),
        c2b=bi("Виж повече", "Learn more"),
        c3h=h(3, "Съвети", "Advice"),
        c3p=p("Отделни правила за деца, за родители и за учители — кратки и приложими.",
              "Separate rules for children, parents and teachers — short and usable."),
        c3b=bi("Към съветите", "See the advice"),
        c4h=h(3, "Полезни връзки", "Resources"),
        c4p=p("Кампании, програми и изследвания на МВР, УНИЦЕФ и партньорски организации.",
              "Campaigns, programmes and research by the Ministry of Interior, UNICEF and partner organisations."),
        c4b=bi("Разгледай", "Browse"),
        seyebrow=bi("Данните", "The data"),
        sh=h(2, "Какво показва изследването", "What the research shows"),
        sp=p("Данни на УНИЦЕФ България, Националния статистически институт и Държавната агенция за закрила на детето.",
             "Figures from UNICEF Bulgaria, the National Statistical Institute and the State Agency for Child Protection.",
             cls="lede"),
        s1=p("от децата в България са преживели някаква форма на насилие до 18-годишна възраст.",
             "of children in Bulgaria have experienced some form of violence before the age of 18."),
        s2=p("са засегнати от емоционално (психическо) насилие — най-разпространената форма.",
             "are affected by emotional (psychological) violence — the most widespread form."),
        s3=p("е разпространението на физическото насилие сред подрастващите.",
             "is the prevalence of physical violence among adolescents."),
        s4=p("или едно на всеки седем деца съобщава, че е било обект на онлайн тормоз.",
             "— one in every seven children — report having been subjected to online bullying."),
        heroimg=pic("hero", "Полицейска служителка и дете със знак на МВР",
                    sizes="(max-width: 1320px) 94vw, 1236px", eager=True),
        pl_eye=bi("За платформата", "About the platform"),
        pl_h=h(2, "Какво е „Спаси дете“", "What “Save a child” is"),
        pl_p="".join(p(x, y) for x, y in zip(C2.PLATFORM_BG, C2.PLATFORM_EN)),
        car_label="Снимки от дейностите / Photos from the activities",
        car_prev="Предишна снимка / Previous photo",
        car_next="Следваща снимка / Next photo",
        car_dots="Избор на снимка / Choose a photo",
        slides=slides_html(),
        snote=bi(
            "Данните идват от различни изследвания с различна методология и обхват. Подробностите и източниците са в раздела <a href=\"bullying.html#m1-vidove\">„Агресия и насилие“</a>.",
            "The figures come from different studies with different methodologies and scope. The details and the sources are in the <a href=\"bullying.html#m1-vidove\">Aggression and violence</a> section.",
        ),
        neyebrow=bi("Новини", "News"),
        nh=h(2, "От институциите", "From the institutions"),
        teasers=teasers,
        nall=bi("Всички новини", "All news"),
        reph=h(2, "Видяхте нещо незаконно в интернет?", "Seen something illegal online?"),
        repp=p("Подайте сигнал до дирекция „Киберпрестъпност“ при ГДБОП. При непосредствена опасност за дете — 112.",
               "Report it to the Cybercrime Directorate at GDBOP. If a child is in immediate danger — call 112."),
    )

    page(
        "index.html",
        "СпасиДете.БГ — агресията в детския свят и къде да потърсим помощ",
        "SpasiDete.BG — aggression in the world of children and where to seek help",
        "Национален портал на МВР за агресията в детския свят — от деца, към деца и между деца, в училище, на улицата и онлайн: как се разпознава, как се реагира, съвети за деца, родители и учители, телефони за помощ и подаване на сигнал.",
        "The Bulgarian Ministry of Interior’s national portal on aggression in the world of children — by children, against children and between children, at school, in the street and online: how to recognise it, how to respond, advice for children, parents and teachers, helplines and reporting channels.",
        body,
        preload='<link rel="preload" as="image" fetchpriority="high" '
                'href="assets/img/photos/hero.jpg" '
                'imagesrcset="assets/img/photos/hero-sm.webp 800w, assets/img/photos/hero.webp 1600w" '
                'imagesizes="(max-width: 1320px) 94vw, 1236px">',
    )


def _materials_section():
    """Петте материала от документа на МВР / the five materials."""

    toc = "".join(
        '<li><a href="#{i}"><span class="toc__n">{n}</span>{t}</a></li>'.format(
            i=m["id"], n=m["num"], t=bi(m["title_bg"], m["title_en"]))
        for m in C2.MATERIALS
    )

    arts = []
    for m in C2.MATERIALS:
        blocks = []
        for b in m["blocks"]:
            inner = h(3, b["h_bg"], b["h_en"])
            if "body_bg" in b:
                inner += "".join(p(x, y) for x, y in zip(b["body_bg"], b["body_en"]))
            if "list_bg" in b:
                inner += ul(b["list_bg"], b["list_en"], cls="advice")
            blocks.append('<div class="matblock">%s</div>' % inner)

        extra = ""
        if m.get("closing_bg"):
            extra += '<div class="callout" style="margin-top:28px">%s</div>' % p(m["closing_bg"], m["closing_en"])
        if m.get("warn_bg"):
            extra += '<div class="callout callout--amber" style="margin-top:28px">%s%s</div>' % (
                h(3, "Важно", "Worth noting"), p(m["warn_bg"], m["warn_en"]))
        if m.get("sources_bg"):
            extra += '<details class="qa" style="margin-top:28px"><summary>%s</summary><div class="qa__body">%s</div></details>' % (
                bi("Официални източници на данните", "Official sources for the figures"),
                ul(m["sources_bg"], m["sources_en"]))

        arts.append("""<article class="material" id="{i}">
  <div class="material__num" aria-hidden="true">{n}</div>
  {t}
  {l}
  {blocks}
  {extra}
</article>""".format(
            i=m["id"], n=m["num"],
            t=h(2, m["title_bg"], m["title_en"]),
            l=p(m["lead_bg"], m["lead_en"], cls="lede"),
            blocks="".join(blocks), extra=extra,
        ))

    return """
<section class="section" id="materiali">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e}</span>
      {hh}
      {pp}
    </div>
    <ol class="toc">{toc}</ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="measure">{arts}</div>
  </div>
</section>
""".format(
        e=bi("Материали", "Materials"),
        hh=h(2, "Агресия и насилие — как да ги разпознаем и предотвратим",
             "Aggression and violence — how to recognise and prevent them"),
        pp=p("Пет материала: какво се случва в България по данни на институциите, откъде идва агресията, "
             "какво казва тя, кога преминава в насилие и по какво се разпознава, когато е скрита.",
             "Five materials: what the institutions’ data show about Bulgaria, where aggression comes from, "
             "what it is saying, when it turns into violence, and how to recognise it when it is hidden.",
             cls="lede"),
        toc=toc,
        arts="".join(arts),
    )


def build_bullying():
    types = [
        ("t-verbal", "Вербална агресия", "Verbal aggression",
         "Обиди, заплахи, подигравки, обидни прякори, публично унижение — включително онлайн, в социалните мрежи и в чатовете.",
         "Insults, threats, mockery, offensive nicknames, public humiliation — including online, on social networks and in chats."),
        ("t-social", "Социална агресия", "Social aggression",
         "Изолация, игнориране, изключване от групата, разпространение на слухове и лъжи — включително онлайн.",
         "Isolation, ignoring, exclusion from the group, spreading rumours and lies — including online."),
        ("t-physical", "Физическа агресия", "Physical aggression",
         "Бой, блъскане, удряне, умишлено повреждане на вещи и други действия, насочени срещу тялото или имуществото.",
         "Beating, pushing, hitting, deliberately damaging belongings and other acts directed at the body or property."),
        ("t-cyber", "Кибертормоз", "Cyberbullying",
         "Заплашителни съобщения, изнудване с интимни снимки, фалшиви профили, изключване от групови чатове, запис и разпространение на побой или унижение.",
         "Threatening messages, extortion with intimate images, fake profiles, exclusion from group chats, recording and sharing a beating or a humiliation."),
    ]
    tcards = "".join(
        '<article class="typecard %s">%s%s</article>' % (c, h(3, b, e), p(db, de))
        for c, b, e, db, de in types
    )

    signs_bg = [
        "Рязка промяна в настроението или в поведението, затваряне в себе си.",
        "Нежелание да ходи на училище, чести оплаквания от главоболие или стомашни болки сутрин.",
        "Нарушен сън, кошмари, загуба на апетит.",
        "Изчезнали, скъсани или повредени вещи; „изгубени“ пари.",
        "Необяснени наранявания, синини или драскотини.",
        "Отдръпване от приятели и от дейности, които преди е харесвало.",
        "Спад в оценките и в концентрацията.",
        "Рязка промяна в поведението онлайн: крие екрана, изтрива съобщения, затваря или изтрива профили.",
        "Притеснение или страх след поглеждане в телефона.",
        "Изказвания за собствената безполезност, за вина или за това, че „си го заслужава“.",
    ]
    signs_en = [
        "A sudden change in mood or behaviour, withdrawing into themselves.",
        "Reluctance to go to school, frequent morning complaints of headaches or stomach aches.",
        "Disturbed sleep, nightmares, loss of appetite.",
        "Missing, torn or damaged belongings; money that has gone “lost”.",
        "Unexplained injuries, bruises or scratches.",
        "Pulling away from friends and from activities they used to enjoy.",
        "A drop in grades and in concentration.",
        "A sharp change in online behaviour: hiding the screen, deleting messages, closing or deleting accounts.",
        "Anxiety or fear after looking at their phone.",
        "Statements about being worthless, being to blame, or “deserving it”.",
    ]

    steps = [
        ("Изслушайте, без да обвинявате",
         "Listen without blaming",
         "Първата реакция определя дали детето ще продължи да споделя. Не питайте „А ти какво направи?“. Кажете ясно: вината не е твоя и добре че ми каза.",
         "The first reaction decides whether the child will keep talking. Do not ask “And what did you do?”. Say it plainly: this is not your fault, and I am glad you told me."),
        ("Не съветвайте детето да отвърне",
         "Do not tell the child to hit back",
         "„Отвърни му“ прехвърля отговорността върху детето и почти винаги влошава положението. Отговорността за спирането на тормоза е на възрастните.",
         "“Hit back” shifts the responsibility onto the child and almost always makes things worse. Stopping bullying is the adults’ responsibility."),
        ("Запазете доказателствата",
         "Preserve the evidence",
         "Направете екранни снимки на съобщенията, профилите и публикациите, като се вижда датата, часът и потребителското име. Не изтривайте нищо, преди да е запазено.",
         "Take screenshots of the messages, profiles and posts, with the date, time and username visible. Do not delete anything before it has been saved."),
        ("Блокирайте и докладвайте в платформата",
         "Block and report inside the platform",
         "Използвайте вградените инструменти на социалната мрежа или играта. Това ограничава контакта, но не замества сигнала до институциите.",
         "Use the built-in tools of the social network or the game. This limits contact, but it does not replace a report to the institutions."),
        ("Уведомете училището",
         "Inform the school",
         "Класният ръководител, училищният психолог или педагогическият съветник. Училището е длъжно да задейства механизма за противодействие на тормоза и насилието.",
         "The class teacher, the school psychologist or the pedagogical counsellor. The school is obliged to trigger the mechanism for countering bullying and violence."),
        ("Подайте сигнал до полицията",
         "Report to the police",
         "При заплахи, побой, изнудване, склоняване на дете онлайн или разпространение на записи от насилие — районното управление, детската педагогическа стая или дирекция „Киберпрестъпност“. При непосредствена опасност — 112.",
         "In cases of threats, assault, extortion, online grooming or the spreading of recorded violence — the district police department, the children’s pedagogical room or the Cybercrime Directorate. If there is immediate danger — 112."),
        ("Осигурете подкрепа на детето",
         "Arrange support for the child",
         "Тормозът оставя следа. Линията 116 111, „Зона ЗаКрила“ и училищният психолог предлагат безплатна подкрепа както на детето, така и на родителите.",
         "Bullying leaves a mark. The 116 111 helpline, the “Zona ZaKrila” centres and the school psychologist offer free support both to the child and to the parents."),
    ]
    steps_html = "".join(
        "<li><strong>%s</strong>%s</li>" % (bi(b, e), p(db, de))
        for b, e, db, de in steps
    )

    body = pagehead(
        "Агресия и насилие",
        "Aggression and violence",
        "Какво е тормозът, как изглежда онлайн, по какви признаци се разпознава и как да реагираме — за деца, родители и учители.",
        "What bullying is, what it looks like online, the signs that reveal it and how to respond — for children, parents and teachers.",
        "Агресия и насилие", "Aggression and violence",
        photo=pic("kampaniya-nikoga-poveche",
                  "Плакат на кампанията на МВР и УНИЦЕФ „Никога повече насилие у дома“",
                  sizes="(max-width: 900px) 260px, 300px", eager=True),
    ) + """
<section class="section section--sky">
  <div class="wrap">
    <div class="grid grid--2" style="gap:40px;align-items:start">
      <div>
        <span class="eyebrow">{e1}</span>
        {h1}
        {p1}
        {p2}
      </div>
      <div class="callout">
        {h2}
        {p3}
      </div>
    </div>
  </div>
</section>

<section class="section" id="types">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e2}</span>
      {h3}
      {p4}
    </div>
    <div class="grid grid--4">{tcards}</div>
  </div>
</section>

<section class="section section--sand" id="signs">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e3}</span>
      {h4}
      {p5}
    </div>
    <div class="grid grid--2" style="align-items:start">
      {signs}
    </div>
    <p class="note" style="margin-top:22px">{note1}</p>
  </div>
</section>

<section class="section section--azure" id="react">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e4}</span>
      {h5}
      {p6}
    </div>
    <ol class="steps">{steps}</ol>
    <div class="btn-row" style="margin-top:32px">
      <a class="btn btn--primary btn--lg" href="help.html#linii">{cta1}</a>
      <a class="btn btn--ghost btn--lg" href="advice.html#roli">{cta2}</a>
    </div>
  </div>
</section>
""".format(
        e1=bi("Определение", "Definition"),
        h1=h(2, "Какво е булинг?", "What is bullying?"),
        p1=p(
            "Булингът (тормозът) е <strong>повтарящо се</strong> поведение, насочено срещу конкретно дете, при което "
            "има <strong>неравновесие на силите</strong> — заради възраст, физическа сила, положение в групата, "
            "брой или достъп до информация. Еднократният конфликт между равни не е тормоз; тормозът е модел, който "
            "се повтаря и от който детето не може да излезе само.",
            "Bullying is <strong>repeated</strong> behaviour directed at a particular child, in which there is an "
            "<strong>imbalance of power</strong> — because of age, physical strength, standing in the group, numbers "
            "or access to information. A one-off conflict between equals is not bullying; bullying is a pattern that "
            "repeats and that the child cannot escape alone.",
        ),
        p2=p(
            "Онлайн тормозът има три особености, които го правят по-тежък: той не спира на изхода на училището, "
            "публиката му е неограничена, а следата от него остава и може да бъде разпространена отново по всяко време.",
            "Online bullying has three features that make it harder to bear: it does not stop at the school gate, "
            "its audience is unlimited, and the trace it leaves remains and can be shared again at any moment.",
        ),
        e2=bi("Форми", "Forms"),
        h2=h(3, "Агресията е сигнал", "Aggression is a signal"),
        p3=p(
            "Агресията рядко е самоцел. Тя е сигнал — за проблем, страх, умора, силна емоция или загуба на контрол. "
            "Това важи и за детето, което упражнява тормоз: зад поведението му обикновено стои нещо, което остава "
            "невидимо за околните. Разбирането на този сигнал не е оправдание за насилието, а начин то да бъде спряно "
            "трайно, а не само наказано.",
            "Aggression is rarely an end in itself. It is a signal — of a problem, of fear, of exhaustion, of a strong "
            "emotion or of a loss of control. This holds for the child doing the bullying too: behind the behaviour "
            "there is usually something that stays invisible to those around. Understanding that signal does not excuse "
            "the violence — it is the way to stop it for good rather than merely punish it.",
        ),
        h3=h(2, "Видовете тормоз", "The types of bullying"),
        p4=p("Често се проявяват едновременно и се подсилват взаимно.",
             "They often appear at the same time and reinforce one another.", cls="lede"),
        tcards=tcards,
        e3=bi("Разпознаване", "Recognising it"),
        h4=h(2, "Как да я открием?", "How do we spot it?"),
        p5=p("Децата рядко казват директно. Обикновено първи се променят навиците, сънят и настроението.",
             "Children rarely say it outright. Usually habits, sleep and mood are the first things to change.", cls="lede"),
        signs=ul(signs_bg[:5], signs_en[:5], cls="signs") + ul(signs_bg[5:], signs_en[5:], cls="signs"),
        note1=bi(
            "Един признак сам по себе си не означава тормоз. Тревожен е моделът: няколко признака заедно, които се задържат във времето или се появяват рязко.",
            "A single sign on its own does not mean bullying. What matters is the pattern: several signs together that persist over time or appear abruptly.",
        ),
        e4=bi("Реакция", "Responding"),
        h5=h(2, "Как да реагираме?", "How do we respond?"),
        p6=p("Седем стъпки, в този ред.", "Seven steps, in this order.", cls="lede"),
        steps=steps_html,
        cta1=bi("Къде да потърсим помощ", "Where to seek help"),
        cta2=bi("Съвети по роля", "Advice by role"),
    ) + _materials_section()

    page(
        "bullying.html",
        "Агресия и насилие — СпасиДете.БГ",
        "Aggression and violence — SpasiDete.BG",
        "Какво е булинг, какви са видовете тормоз (вербален, социален, физически, онлайн), по какви признаци се разпознава и как да реагират родителите и училището.",
        "What bullying is, the types of bullying (verbal, social, physical, online), the signs that reveal it and how parents and schools should respond.",
        body,
    )


def build_advice():
    kids_bg = [
        "<strong>Не давай лична информация</strong> на човек, с когото си се запознал/а в интернет — нито твоя, нито на приятелите си. Имена, адрес, училище, телефон и снимки могат да бъдат използвани срещу теб.",
        "<strong>В интернет всеки е непознат.</strong> Дори профилът да изглежда като на твой познат, зад него може да стои друг човек.",
        "<strong>Не се съгласявай на среща</strong> с човек от интернет. Ако смяташ, че е наистина наложително — кажи на родителите си и отиди с тях.",
        "<strong>Ако нещо те обиди, шокира или смути</strong> — не го изтривай веднага. Покажи го на възрастен, на когото вярваш, и подай сигнал.",
        "<strong>Не изпращай свои интимни снимки</strong> на никого — дори на човек, на когото вярваш. След като снимката е изпратена, ти вече не контролираш къде отива.",
        "<strong>Ако някой те изнудва</strong> с твоя снимка или съобщение — спри да отговаряш, запази доказателствата и кажи на възрастен. Изнудването е престъпление и вината не е твоя.",
        "<strong>Не участвай и не препращай.</strong> Споделянето на запис от бой или унижение прави нараняването по-голямо, а теб — част от него.",
        "<strong>Подкрепи този, когото тормозят.</strong> Дори едно изречение „не си сам“ променя много. Ако е опасно да се намесиш — кажи на възрастен.",
        "<strong>Пази паролите си.</strong> Различна парола за всеки сайт, с главни и малки букви, цифри и знаци. Никога име, рожден ден, ЕГН или телефонен номер. Паролата не се споделя — дори с най-добрия приятел.",
        "<strong>Провери настройките за поверителност</strong> на профилите си: кой вижда публикациите ти, кой може да ти пише и кой вижда къде се намираш.",
        "<strong>Не прави нищо</strong>, което може да навреди на теб, на други хора или на нечие устройство.",
    ]
    kids_en = [
        "<strong>Do not give personal information</strong> to someone you met online — neither yours nor your friends’. Names, address, school, phone number and photos can be used against you.",
        "<strong>Online, everyone is a stranger.</strong> Even if the profile looks like someone you know, another person may be behind it.",
        "<strong>Do not agree to meet</strong> someone from the internet. If you believe it is truly necessary — tell your parents and go with them.",
        "<strong>If something offends, shocks or unsettles you</strong> — do not delete it straight away. Show it to an adult you trust and report it.",
        "<strong>Do not send intimate photos of yourself</strong> to anyone — not even to someone you trust. Once a photo is sent, you no longer control where it goes.",
        "<strong>If someone is blackmailing you</strong> with your photo or message — stop replying, save the evidence and tell an adult. Extortion is a crime and it is not your fault.",
        "<strong>Do not take part and do not forward.</strong> Sharing a recording of a beating or a humiliation makes the harm bigger and makes you part of it.",
        "<strong>Support the person being bullied.</strong> Even one sentence — “you are not alone” — changes a great deal. If stepping in would be dangerous, tell an adult.",
        "<strong>Protect your passwords.</strong> A different password for every site, with upper and lower case letters, digits and symbols. Never a name, a birthday, an ID number or a phone number. A password is not shared — not even with your best friend.",
        "<strong>Check the privacy settings</strong> on your accounts: who sees your posts, who can message you and who can see where you are.",
        "<strong>Do not do anything</strong> that could harm you, other people or someone’s device.",
    ]

    parents_bg = [
        "<strong>Говорете за рисковете</strong>, преди да се появят. Обяснете на детето си, че в интернет хората не винаги са това, за което се представят, и че възрастни с престъпни намерения се представят за деца.",
        "<strong>Ползвайте интернет заедно.</strong> Интересувайте се какви сайтове посещава детето, с кого общува, какви игри играе и какво гледа — не като проверка, а като разговор.",
        "<strong>Договорете правила за времето и мястото.</strong> Кога и къде се ползват устройства, кога телефонът остава извън стаята през нощта.",
        "<strong>Не позволявайте срещи</strong> с хора, с които детето се е запознало онлайн. Ако среща е неизбежна — придружете детето.",
        "<strong>Реагирайте спокойно, когато детето сподели.</strong> Паниката, наказанието или отнемането на телефона учат детето следващия път да мълчи.",
        "<strong>Запазете доказателствата</strong> — екранни снимки с дата, час и потребителско име — преди да блокирате или да изтриете каквото и да е.",
        "<strong>Подайте сигнал.</strong> При незаконно съдържание — дирекция „Киберпрестъпност“ при ГДБОП. При непосредствена опасност — 112. При проблем в училище — класният ръководител и училищният психолог.",
        "<strong>Използвайте родителски контрол и филтриращи програми</strong> според възрастта на детето — като допълнение към разговора, не вместо него.",
        "<strong>Следете кръга на детето.</strong> Кои са приятелите му, включително онлайн; в какви групи и чатове участва.",
        "<strong>Обърнете внимание на съдържанието, което консумира.</strong> Затворените групи, в които жестокостта се представя като сила, а емпатията — като слабост, са реален риск от радикализация.",
        "<strong>Потърсете подкрепа и за себе си.</strong> Линията 116 111 и „Зона ЗаКрила“ консултират и родители.",
    ]
    parents_en = [
        "<strong>Talk about the risks</strong> before they appear. Explain to your child that online people are not always who they claim to be, and that adults with criminal intentions present themselves as children.",
        "<strong>Use the internet together.</strong> Take an interest in the sites your child visits, whom they talk to, what games they play and what they watch — as a conversation, not an inspection.",
        "<strong>Agree rules about time and place.</strong> When and where devices are used, and when the phone stays out of the bedroom at night.",
        "<strong>Do not allow meetings</strong> with people your child met online. If a meeting is unavoidable, accompany your child.",
        "<strong>Stay calm when your child opens up.</strong> Panic, punishment or confiscating the phone teach the child to stay silent next time.",
        "<strong>Preserve the evidence</strong> — screenshots with the date, time and username — before blocking or deleting anything.",
        "<strong>File a report.</strong> For illegal content — the Cybercrime Directorate at GDBOP. For immediate danger — 112. For a problem at school — the class teacher and the school psychologist.",
        "<strong>Use parental controls and filtering software</strong> appropriate to your child’s age — as a supplement to the conversation, not a substitute for it.",
        "<strong>Know your child’s circle.</strong> Who their friends are, including online; which groups and chats they belong to.",
        "<strong>Pay attention to the content they consume.</strong> Closed groups in which cruelty is presented as strength and empathy as weakness are a real radicalisation risk.",
        "<strong>Seek support for yourself too.</strong> The 116 111 helpline and the “Zona ZaKrila” centres also advise parents.",
    ]

    teachers_bg = [
        "<strong>Знайте механизма.</strong> Училището е длъжно да прилага механизма за противодействие на тормоза и насилието в системата на предучилищното и училищното образование. Всеки в екипа трябва да знае какво прави при сигнал.",
        "<strong>Приемете всеки сигнал сериозно</strong> — включително анонимния и включително от трето дете. Проверката е задължителна, преценката идва след нея.",
        "<strong>Не правете очни ставки</strong> между тормозещия и тормозеното дете. Разговаряйте поотделно.",
        "<strong>Документирайте.</strong> Дата, участници, описание, предприети действия. Документацията защитава и детето, и училището.",
        "<strong>Работете и с детето, което тормози.</strong> Санкцията без работа по причината възпроизвежда поведението другаде.",
        "<strong>Наблюдавайте местата без надзор</strong> — коридори, тоалетни, съблекални, пътя до училище, груповите чатове на класа.",
        "<strong>Включете класа.</strong> Тормозът живее от мълчаливата публика. Работата с наблюдателите променя средата по-бързо от работата само с двамата участници.",
        "<strong>Информирайте родителите</strong> на всички засегнати деца — навреме и фактологично.",
        "<strong>Привлечете специалист.</strong> Училищният психолог, педагогическият съветник, отдел „Закрила на детето“ и инспекторът от детската педагогическа стая са част от решението.",
        "<strong>Включете темата в часа на класа.</strong> Кампаниите „Насилието е безсилие“ и програмата „Стъпки заедно“ на УНИЦЕФ и МОН предлагат готови материали.",
    ]
    teachers_en = [
        "<strong>Know the mechanism.</strong> Schools are obliged to apply the mechanism for countering bullying and violence in pre-school and school education. Everyone on the team should know what to do when a report comes in.",
        "<strong>Take every report seriously</strong> — including anonymous ones and ones from a third child. Checking is mandatory; judgement comes afterwards.",
        "<strong>Do not stage confrontations</strong> between the child bullying and the child being bullied. Speak to them separately.",
        "<strong>Document it.</strong> Date, those involved, description, action taken. Documentation protects both the child and the school.",
        "<strong>Work with the child who bullies too.</strong> A sanction without work on the cause simply reproduces the behaviour elsewhere.",
        "<strong>Watch the unsupervised places</strong> — corridors, toilets, changing rooms, the route to school, the class group chats.",
        "<strong>Involve the class.</strong> Bullying lives off a silent audience. Working with the bystanders changes the environment faster than working with the two participants alone.",
        "<strong>Inform the parents</strong> of all the children involved — promptly and factually.",
        "<strong>Bring in a specialist.</strong> The school psychologist, the pedagogical counsellor, the Child Protection Department and the inspector from the children’s pedagogical room are part of the solution.",
        "<strong>Bring the topic into class time.</strong> The “Violence is powerlessness” campaign and the UNICEF–Ministry of Education “Steps together” programme offer ready-made materials.",
    ]

    body = pagehead(
        "Съвети",
        "Advice",
        "Кратки и приложими правила — отделно за децата, за родителите, за учителите и за гражданите.",
        "Short, usable rules — separately for children, parents, teachers and citizens.",
        "Съвети", "Advice",
        photo=pic("dpu-risunka",
                  "Детска рисунка за Детското полицейско управление",
                  sizes="(max-width: 900px) 260px, 300px", eager=True),
    ) + """
<section class="section section--azure" id="roli">
  <div class="wrap">
    <div class="tabs" data-tabs>
      <ul class="tabs__list" role="tablist" aria-label="{tl}">
        <li role="presentation"><button class="tabs__btn" id="tab-deca" role="tab" type="button" data-hash="deca" aria-controls="panel-deca" aria-selected="true">{t1}</button></li>
        <li role="presentation"><button class="tabs__btn" id="tab-roditeli" role="tab" type="button" data-hash="roditeli" aria-controls="panel-roditeli" aria-selected="false">{t2}</button></li>
        <li role="presentation"><button class="tabs__btn" id="tab-uchiteli" role="tab" type="button" data-hash="uchiteli" aria-controls="panel-uchiteli" aria-selected="false">{t3}</button></li>
        <li role="presentation"><button class="tabs__btn" id="tab-grazhdani" role="tab" type="button" data-hash="grazhdani" aria-controls="panel-grazhdani" aria-selected="false">{t4}</button></li>
      </ul>

      <div class="tabs__panel" id="panel-deca" role="tabpanel" aria-labelledby="tab-deca" tabindex="0">
        <div class="section-head">{h1}{p1}</div>
        <figure class="figure figure--inline">{img1}<figcaption>{cap1}</figcaption></figure>
        {l1}
      </div>

      <div class="tabs__panel" id="panel-roditeli" role="tabpanel" aria-labelledby="tab-roditeli" tabindex="0" hidden>
        <div class="section-head">{h2}{p2}</div>
        {l2}
      </div>

      <div class="tabs__panel" id="panel-uchiteli" role="tabpanel" aria-labelledby="tab-uchiteli" tabindex="0" hidden>
        <div class="section-head">{h3}{p3}</div>
        <figure class="figure figure--inline">{img3}<figcaption>{cap3}</figcaption></figure>
        {l3}
      </div>

      <div class="tabs__panel" id="panel-grazhdani" role="tabpanel" aria-labelledby="tab-grazhdani" tabindex="0" hidden>
        <div class="section-head">{h4}{p4}</div>
        <div class="callout callout--amber" style="margin-bottom:28px">{intro4}</div>
        <figure class="figure figure--inline">{img4}<figcaption>{cap4}</figcaption></figure>
        {l4}
        <div class="callout" style="margin-top:28px">{close4}</div>
      </div>
    </div>
  </div>
</section>

<section class="section section--rose">
  <div class="wrap">
    <div class="callout callout--red">
      {hh}
      {pp}
      <div class="btn-row" style="margin-top:20px">
        <a class="btn btn--danger btn--lg" href="tel:112">112</a>
        <a class="btn btn--ghost btn--lg" href="tel:116111">116 111</a>
        <a class="btn btn--ghost btn--lg" href="help.html#linii">{bb}</a>
      </div>
    </div>
  </div>
</section>
""".format(
        tl="Съвети по роля / Advice by role",
        t1=bi("Към децата", "For children"),
        t2=bi("Към родителите", "For parents"),
        t3=bi("Към учителите", "For teachers"),
        h1=h(2, "Деца, запомнете!", "Children, remember!"),
        p1=p("Интернет е невероятно място — стига да знаеш няколко прости правила.",
             "The internet is an amazing place — as long as you know a few simple rules.", cls="lede"),
        img1=pic("deca-patrulka", "Младежи в патрулен автомобил заедно с полицейски служител", sizes="(max-width: 680px) 90vw, 620px"),
        cap1=bi("Полицаят е човек, към когото може да се обърнеш — не само униформа.",
                "The officer is someone you can turn to — not just a uniform."),
        l1=ul(kids_bg, kids_en, cls="advice"),
        h2=h(2, "Родители!", "Parents!"),
        p2=p("Присъствието не е контрол. То е да знаете какво се случва и детето да знае, че може да ви каже.",
             "Being present is not control. It is knowing what is happening — and your child knowing they can tell you.", cls="lede"),
        l2=ul(parents_bg, parents_en, cls="advice"),
        t4=bi("Към гражданите", "For citizens"),
        img3=pic("uchiteli-klas", "Полицейски служители в час на класа", sizes="(max-width: 680px) 90vw, 620px"),
        cap3=bi("Занятие в училище с участието на полицейски служители.",
                "A classroom session with police officers taking part."),
        h4=h(2, "Виждаш конфликт или насилие над дете на обществено място?",
             "Seeing a conflict or violence against a child in public?"),
        p4=p("Не подминавай. Реагирай безопасно.", "Do not walk past. React safely.", cls="lede"),
        intro4=p(C2.CITIZENS_INTRO_BG, C2.CITIZENS_INTRO_EN),
        img4=pic("grazhdani-listovki", "Полицейски служител и деца раздават листовки на водач", sizes="(max-width: 680px) 90vw, 620px"),
        cap4=bi("Деца и полицейски служители в съвместна кампания на улицата.",
                "Children and police officers in a joint street campaign."),
        l4=ul(C2.CITIZENS_BG, C2.CITIZENS_EN, cls="advice"),
        close4=p(C2.CITIZENS_CLOSING_BG, C2.CITIZENS_CLOSING_EN),
        h3=h(2, "Учители и училищни специалисти", "Teachers and school specialists"),
        p3=p("Училището е мястото, където тормозът най-често започва — и мястото, където най-бързо може да бъде спрян.",
             "School is where bullying most often starts — and where it can be stopped fastest.", cls="lede"),
        l3=ul(teachers_bg, teachers_en, cls="advice"),
        hh=h(2, "Ако не сте сигурни — обадете се", "If you are not sure — call"),
        pp=p("Консултацията е безплатна и не ви задължава с нищо. По-добре е да попитате напразно, отколкото да изчакате.",
             "The consultation is free and commits you to nothing. It is better to ask needlessly than to wait."),
        bb=bi("Всички телефони", "All helplines"),
    )

    page(
        "advice.html",
        "Съвети за деца, родители, учители и граждани — СпасиДете.БГ",
        "Advice for children, parents, teachers and citizens — SpasiDete.BG",
        "Правила за безопасност в интернет и при тормоз — отделни съвети за децата, за родителите, за учителите и за гражданите, които стават свидетели на насилие.",
        "Online safety and anti-bullying rules — separate advice for children, parents, teachers and citizens who witness violence.",
        body,
    )


def build_help():
    lines = "".join(render_helpline(x) for x in HELPLINES)
    local = "".join(
        '<article class="card">%s%s</article>' % (h(3, b, e), p(db, de))
        for b, e, db, de in LOCAL_HELP
    )

    body = pagehead(
        "Къде и от кого да потърсим помощ",
        "Where and from whom to seek help",
        "Телефони, институции и онлайн канали за подаване на сигнал — подредени по спешност. Всички линии по-долу приемат сигнали и за деца, и от деца.",
        "Helplines, institutions and online reporting channels — ordered by urgency. Every line below takes reports both about children and from children.",
        "Потърси помощ", "Get help",
    ) + """
<section class="section section--sky section--tight">
  <div class="wrap">
    <div class="callout callout--red">
      <div class="grid grid--2" style="align-items:center;gap:26px">
        <div>
          {h0}
          {p0}
        </div>
        <div class="btn-row">
          <a class="btn btn--danger btn--lg" href="tel:112">{b112}</a>
          <a class="btn btn--ghost btn--lg" href="tel:116111">116 111</a>
          <a class="btn btn--ghost btn--lg" href="report.html#formulyar">{bform}</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e1}</span>
      {h1}
      {p1}
    </div>
    <div class="grid grid--3" style="gap:16px">
      <a class="card card--link card--emblem" href="https://www.cybercrime.bg/" target="_blank" rel="noopener">
        {emb1}
        <div>{c1h}{c1p}<span class="card__more">cybercrime.bg</span></div>
      </a>
      <a class="card card--link card--emblem" href="https://gdbop.bg/" target="_blank" rel="noopener">
        {emb2}
        <div>{c2h}{c2p}<span class="card__more">gdbop.bg</span></div>
      </a>
      <a class="card card--link card--emblem" href="https://www.mvr.bg/" target="_blank" rel="noopener">
        {emb3}
        <div>{c3h}{c3p}<span class="card__more">mvr.bg</span></div>
      </a>
    </div>
  </div>
</section>

<section class="section section--rose" id="linii">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e2}</span>
      {h2}
      {p2}
    </div>
    {lines}
  </div>
</section>

<section class="section" id="mesten">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e3}</span>
      {h3}
      {p3}
    </div>
    <div class="grid grid--2">{local}</div>
    <figure class="figure figure--wide" style="margin-top:34px">{limg}<figcaption>{lcap}</figcaption></figure>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e4}</span>
      {h4}
    </div>
    {faq}
  </div>
</section>
""".format(
        h0=h(2, "Има ли дете в опасност в момента?", "Is a child in danger right now?"),
        p0=p("Не изчаквайте и не се опитвайте да прецените сами колко е сериозно. Обадете се.",
             "Do not wait and do not try to judge on your own how serious it is. Call."),
        b112=bi("Звънни на 112", "Call 112"),
        bform=bi("Формуляр за сигнал", "Report form"),
        e1=bi("Онлайн сигнал", "Report online"),
        h1=h(2, "Подай сигнал в МВР", "Report to the Ministry of Interior"),
        p1=p("За вредно и незаконно съдържание в българското интернет пространство и за организирана престъпна дейност.",
             "For harmful and illegal content in the Bulgarian internet space and for organised criminal activity.", cls="lede"),
        emb1=emblem("cybercrime-gdbop", cls="emblem", w=341, h=420),
        emb2=emblem("gdbop-mvr", cls="emblem emblem--round", w=256, h=256),
        emb3=emblem("mvr-nacionalna-policiya", cls="emblem", w=153, h=192),
        c3h=h(3, "МВР — приемна и структури", "Ministry of Interior — reception and structures"),
        c3p=p("Официалният сайт на Министерството на вътрешните работи: областните дирекции, районните управления, "
              "детските педагогически стаи и приемната за граждани.",
              "The official site of the Ministry of Interior: the regional directorates, the district departments, "
              "the child pedagogical rooms and the citizens\u2019 reception."),
        c1h=h(3, "Дирекция „Киберпрестъпност“", "Cybercrime Directorate"),
        c1p=p("Материали със сексуална злоупотреба с деца, склоняване на дете онлайн, изнудване с интимни снимки, заплахи, разпространение на записи от насилие.",
              "Child sexual abuse material, online grooming, extortion with intimate images, threats, the spreading of recorded violence."),
        c2h=h(3, "ГДБОП — подай сигнал", "GDBOP — file a report"),
        c2p=p("Официалният канал на Главна дирекция „Борба с организираната престъпност“. Анонимността на подателя се гарантира по реда на закона.",
              "The official channel of the General Directorate for Combating Organised Crime. The anonymity of the person reporting is guaranteed by law."),
        e2=bi("Телефонни линии", "Helplines"),
        h2=h(2, "Институции и линии за помощ", "Institutions and helplines"),
        p2=p("Номерата са активни връзки — на телефон достатъчно е да докоснете номера.",
             "The numbers are active links — on a phone, simply tap the number.", cls="lede"),
        lines=lines,
        e3=bi("По местоживеене", "Locally"),
        h3=h(2, "Помощ във вашия град и училище", "Help in your town and school"),
        p3=p("Освен националните линии, най-бърза реакция често идва от най-близката институция.",
             "Besides the national lines, the fastest response often comes from the nearest institution.", cls="lede"),
        local=local,
        limg=pic("sabitie-bezopasnost", "Открито занятие по безопасност с участието на полицията",
                 sizes="(max-width: 980px) 92vw, 900px"),
        lcap=bi("Полицията в квартала — най-близката институция при сигнал за дете в риск.",
                "The police in the neighbourhood — the nearest institution when a child is at risk."),
        e4=bi("Въпроси", "Questions"),
        h4=h(2, "Често задавани въпроси", "Frequently asked questions"),
        faq=_help_faq(),
    )

    page(
        "help.html",
        "Къде да потърсим помощ — телефони и институции — СпасиДете.БГ",
        "Where to seek help — helplines and institutions — SpasiDete.BG",
        "112, 116 111, ДАЗД, „Зона ЗаКрила“, Анимус, Интерпол, дирекция „Киберпрестъпност“ и ГДБОП — телефони, имейли и връзки за подаване на сигнал.",
        "112, 116 111, SACP, “Zona ZaKrila”, Animus, Interpol, the Cybercrime Directorate and GDBOP — phone numbers, e-mails and reporting links.",
        body,
    )


def _help_faq():
    qa = [
        ("Мога ли да подам сигнал анонимно?",
         "Can I report anonymously?",
         "Да. Анонимността на подателя се гарантира по реда на закона. Имайте предвид, че без данни за контакт институцията не може да поиска уточнения от вас, което понякога забавя проверката.",
         "Yes. The anonymity of the person reporting is guaranteed by law. Bear in mind that without contact details the institution cannot ask you for clarification, which can slow the check down."),
        ("Дете съм. Мога ли да се обадя сам?",
         "I am a child. Can I call on my own?",
         "Да. Линията 116 111 е създадена точно за това — безплатна е, работи денонощно и можеш да се обадиш сам, без родител. Ако си в непосредствена опасност — 112.",
         "Yes. The 116 111 helpline exists precisely for this — it is free, it works around the clock, and you can call on your own, without a parent. If you are in immediate danger — 112."),
        ("Какво да запазя, преди да подам сигнал?",
         "What should I save before reporting?",
         "Екранни снимки на съобщенията и профилите, на които се виждат датата, часът и потребителското име; адресът (URL) на страницата или профила; имената на всички участници, ако ги знаете. Не изтривайте нищо, преди да е запазено.",
         "Screenshots of the messages and profiles showing the date, time and username; the address (URL) of the page or profile; the names of everyone involved, if you know them. Do not delete anything before it has been saved."),
        ("Тормозът е в училище, не онлайн. Пак ли е ваш случай?",
         "The bullying is at school, not online. Is it still your case?",
         "Започнете от училището — класния ръководител и училищния психолог — и от отдел „Закрила на детето“. При физическо насилие, заплахи или изнудване се сезира районното полицейско управление и детската педагогическа стая. Ако има запис, който се разпространява онлайн, това вече е и случай за дирекция „Киберпрестъпност“.",
         "Start with the school — the class teacher and the school psychologist — and with the Child Protection Department. In cases of physical violence, threats or extortion, notify the district police department and the children’s pedagogical room. If a recording is being shared online, it also becomes a case for the Cybercrime Directorate."),
        ("Детето ми е изпратило своя снимка и сега го изнудват.",
         "My child sent a photo of themselves and is now being blackmailed.",
         "Не плащайте и не отговаряйте. Запазете всичко, блокирайте профила и подайте сигнал незабавно — това е престъпление. Вината не е на детето и то трябва да го чуе от вас. Линията 116 111 и „Зона ЗаКрила“ предлагат подкрепа и на детето, и на родителя.",
         "Do not pay and do not reply. Save everything, block the account and report it immediately — this is a crime. The child is not to blame and needs to hear that from you. The 116 111 helpline and the “Zona ZaKrila” centres support both the child and the parent."),
    ]
    return "".join(
        """<details class="qa">
  <summary><span lang="bg">{qb}</span><span lang="en">{qe}</span></summary>
  <div class="qa__body">{a}</div>
</details>""".format(qb=qb, qe=qe, a=p(ab, ae))
        for qb, qe, ab, ae in qa
    )


def build_news():
    items = "".join(render_news(n) for n in NEWS)
    body = pagehead(
        "Новини",
        "News",
        "Съобщения и инициативи на Министерството на вътрешните работи, Главна дирекция „Национална полиция“, ГДБОП и партньорски организации.",
        "Announcements and initiatives from the Ministry of Interior, the General Directorate National Police, GDBOP and partner organisations.",
        "Новини", "News",
    ) + """
<section class="section section--azure">
  <div class="wrap">
    <div class="measure">{items}</div>
  </div>
</section>
""".format(items=items)

    page(
        "news.html",
        "Новини — СпасиДете.БГ",
        "News — SpasiDete.BG",
        "„Насилието е безсилие“, „Малките големи герои“, изследването „Да растеш онлайн“ и други съобщения на МВР, ГДНП и УНИЦЕФ.",
        "“Violence is powerlessness”, “Little Big Heroes”, the “Growing up online” study and other announcements from the Ministry of Interior, the National Police and UNICEF.",
        body,
    )


def build_resources():
    items = "".join(render_resource(r) for r in RESOURCES)
    body = pagehead(
        "Ресурси и полезни връзки",
        "Resources",
        "Кампании, програми, изследвания и организации, които работят по темата за агресията, тормоза и безопасността на децата онлайн.",
        "Campaigns, programmes, research and organisations working on aggression, bullying and children’s safety online.",
        "Ресурси", "Resources",
        photo=pic("bezopasnost-velosipedi",
                  "Полицейски служител с деца на велосипеди и тротинетки",
                  sizes="(max-width: 900px) 260px, 300px", eager=True),
    ) + """
<section class="section" id="vrazki">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e1}</span>
      {h0}
      {p0}
    </div>
    <div class="grid grid--2">{items}</div>
  </div>
</section>

<section class="section section--azure">
  <div class="wrap">
    <div class="callout">
      {h1}
      {p1}
      <div class="btn-row" style="margin-top:18px">
        <a class="btn btn--primary" href="contact.html#kontakt">{b1}</a>
      </div>
    </div>
  </div>
</section>
""".format(
        items=items,
        e1=bi("Подбрани", "Selected"),
        h0=h(2, "Кампании, програми и изследвания", "Campaigns, programmes and research"),
        p0=p("Материали на МВР, УНИЦЕФ и партньорски организации — всяка връзка води към първоизточника.",
             "Materials from the Ministry of Interior, UNICEF and partner organisations — every link leads to the original source.",
             cls="lede"),
        h1=h(2, "Липсва важен ресурс?", "Is an important resource missing?"),
        p1=p("Ако работите по темата и имате материали, които биха помогнали на деца, родители или учители, пишете ни.",
             "If you work in this field and have materials that would help children, parents or teachers, write to us."),
        b1=bi("Свържете се с нас", "Get in touch"),
    )

    page(
        "resources.html",
        "Ресурси и полезни връзки — СпасиДете.БГ",
        "Resources — SpasiDete.BG",
        "Кампании и програми срещу агресията и тормоза: SmartyKids, УНИЦЕФ България, „Стъпки заедно“, изследването „Да растеш онлайн“ и други.",
        "Campaigns and programmes against aggression and bullying: SmartyKids, UNICEF Bulgaria, “Steps together”, the “Growing up online” study and more.",
        body,
    )


def build_about():
    partners = [
        ("Главна дирекция „Борба с организираната престъпност“ (ГДБОП)",
         "General Directorate for Combating Organised Crime (GDBOP)",
         "Специализирана полицейска оперативно-издирвателна служба в рамките на МВР за противодействие и неутрализиране на престъпната дейност на местни и транснационални организирани престъпни структури. Бенефициент по проекта.",
         "A specialised police operational and investigative service within the Ministry of Interior, countering and neutralising the criminal activity of domestic and transnational organised crime structures. Beneficiary of the project.",
         "https://gdbop.bg/", "gdbop.bg"),
        ("Международна агенция за превенция на престъпността и политики за сигурност (Румъния)",
         "International Agency for Crime Prevention and Security Policies (Romania)",
         "Създадена през октомври 2009 г. с цел да насърчава и подкрепя инициативи и мерки — предимно в Румъния, но и на Балканския полуостров — за предотвратяване на престъпността, особено организираната, и за гарантиране на безопасността на обществото.",
         "Founded in October 2009 to promote and support initiatives and measures — primarily in Romania, but also across the Balkan Peninsula — for preventing crime, especially organised crime, and for ensuring public safety.",
         None, "prevenirea-criminalitatii.ro"),
        ("Сектор „Компютърни престъпления“ към МВР на Малта",
         "Cybercrime Unit, Malta Police Force",
         "Специализираното звено за компютърни престъпления в рамките на полицейските сили на Малта — партньор по проекта.",
         "The specialised computer crime unit within the Malta Police Force — a partner in the project.",
         "https://pulizija.gov.mt/", "pulizija.gov.mt"),
    ]
    pcards = "".join(
        '<article class="partner">{t}{d}<p>{link}</p></article>'.format(
            t=h(3, b, e), d=p(db, de),
            link=('<a href="%s" target="_blank" rel="noopener">%s &#8599;</a>' % (u, lbl))
                 if u else ('<span class="reslink__host">%s</span>' % lbl),
        )
        for b, e, db, de, u, lbl in partners
    )

    faq = [
        ("Кой поддържа този сайт?",
         "Who maintains this site?",
         "Сайтът е на Министерството на вътрешните работи. Поддържа се от дирекция „Киберпрестъпност“ при Главна дирекция „Борба с организираната престъпност“, а съдържанието се изготвя съвместно със структурите на МВР, които работят с деца — детските педагогически стаи, районните управления и Главна дирекция „Национална полиция“.",
         "The site belongs to the Ministry of Interior. It is maintained by the Cybercrime Directorate at the General Directorate for Combating Organised Crime, and its content is prepared together with the Ministry structures that work with children — the child pedagogical rooms, the regional police departments and the General Directorate National Police."),
        ("Какъв беше проектът „Децата — потенциални жертви на престъпления в интернет“?",
         "What was the project “Children — potential victims of crime on the internet”?",
         "Проект HOME/2012/ISEC/FP/C2/4000003996, разработен от ГДБОП по програма „Превенция и борба с престъпността“ на Европейската комисия. Той е насочен към по-ефективно противодействие на сексуалната експлоатация и злоупотреба с деца в интернет, към подобряване на механизмите за международно сътрудничество и към повишаване на професионалния капацитет на компетентните структури.",
         "Project HOME/2012/ISEC/FP/C2/4000003996, developed by GDBOP under the European Commission’s Prevention of and Fight against Crime Programme. It aimed at countering the sexual exploitation and abuse of children online more effectively, improving international cooperation mechanisms and raising the professional capacity of the competent structures."),
        ("Какъв беше бюджетът на проекта?",
         "What was the project budget?",
         "Общата стойност е 125 084,00 евро, от които 112 538,07 евро (89,97%) са отпуснати под формата на безвъзмезден грант от Европейската комисия, а останалите 12 545,93 евро (10,03%) представляват съфинансиране от ГДБОП и от „Международната агенция за превенция на престъпността и политики за сигурност“ на Румъния.",
         "The total value was EUR 125,084.00, of which EUR 112,538.07 (89.97%) was awarded as a grant by the European Commission, with the remaining EUR 12,545.93 (10.03%) co-financed by GDBOP and by Romania’s International Agency for Crime Prevention and Security Policies."),
        ("Какви бяха резултатите?",
         "What were the results?",
         "Споделени добри практики в превенцията и борбата с онлайн сексуалната експлоатация на деца; засилено оперативно сътрудничество между организацията-апликант и партньорите ѝ; разработена стандартизирана програма за обучение на правоохранителните органи според българските правила и процедури; подобрена координация между правоохранителната власт, правосъдието и европейските институции; и над 70 обучени служители на ГДБОП, правоохранителните органи и прокуратурата.",
         "Shared good practice in preventing and combating the online sexual exploitation of children; strengthened operational cooperation between the applicant organisation and its partners; a standardised training programme for law-enforcement bodies developed in line with Bulgarian rules and procedures; improved coordination between law enforcement, the judiciary and European institutions; and more than 70 trained officers from GDBOP, law-enforcement bodies and the prosecution service."),
        ("Какво е блокирането на достъпа до сайтове с детска сексуална експлоатация?",
         "What is the blocking of access to child sexual exploitation sites?",
         "Превантивна мярка, прилагана в много страни. Интерпол поддържа списък с домейни, за които е установено, че разпространяват материали със сексуална злоупотреба с деца; за да попадне домейн в списъка, той трябва да е бил докладван от най-малко три държави. Списъкът се предоставя безвъзмездно на доставчиците на интернет услуги, които се включват доброволно. При опит за достъп браузърът пренасочва към стоп-страница. Никаква информация за използвания от потребителя IP адрес не се съхранява.",
         "A preventive measure applied in many countries. Interpol maintains a list of domains found to distribute child sexual abuse material; to enter the list, a domain must have been reported by at least three countries. The list is provided free of charge to internet service providers that join voluntarily. On an attempted visit, the browser redirects to a stop page. No information about the user’s IP address is stored."),
    ]
    faq_html = "".join(
        """<details class="qa">
  <summary><span lang="bg">{qb}</span><span lang="en">{qe}</span></summary>
  <div class="qa__body">{a}</div>
</details>""".format(qb=qb, qe=qe, a=p(ab, ae))
        for qb, qe, ab, ae in faq
    )

    body = pagehead(
        "За сайта",
        "About the site",
        "СпасиДете.БГ е национален информационен портал на Министерството на вътрешните работи за агресията в детския свят. Създаден е в рамките на европейски проект за безопасността на децата онлайн и днес обхваща агресията във всичките ѝ форми — като постоянен ресурс за деца, родители и учители.",
        "SpasiDete.BG is a national information portal of the Bulgarian Ministry of Interior on aggression in the world of children. It was created within a European project on children’s safety online and today covers aggression in all its forms — as a permanent resource for children, parents and teachers.",
        "За сайта", "About",
    ) + """
<section class="section">
  <div class="wrap">
    <div class="grid grid--2" style="gap:40px;align-items:start">
      <div>
        <span class="eyebrow">{e1}</span>
        {h1}
        {p1}
        {p2}
      </div>
      <div class="databox">
        {h2}
        <dl>
          <dt>{d1}</dt><dd>HOME/2012/ISEC/FP/C2/4000003996</dd>
          <dt>{d2}</dt><dd>{v2}</dd>
          <dt>{d3}</dt><dd>125 084,00 EUR</dd>
          <dt>{d4}</dt><dd>112 538,07 EUR (89,97%)</dd>
          <dt>{d5}</dt><dd>12 545,93 EUR (10,03%)</dd>
          <dt>{d6}</dt><dd>{v6}</dd>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <figure class="figure">
      <picture><source type="image/webp" srcset="assets/img/conference.webp"><img src="assets/img/conference.jpg" width="958" height="364" alt="{imgalt}" decoding="async" loading="lazy"></picture>
      <figcaption>{imgcap}</figcaption>
    </figure>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e2}</span>
      {h3}
      {p3}
    </div>
    <div class="grid grid--3">{pcards}</div>
  </div>
</section>

<section class="section section--sky" id="isp">
  <div class="wrap">
    <div class="grid grid--2" style="gap:40px;align-items:start">
      <div>
        <span class="eyebrow">{e3}</span>
        {h4}
        {p4}
        {p5}
        {p6}
      </div>
      <div class="callout callout--navy">
        {h5}
        {p7}
        <div class="btn-row" style="margin-top:20px">
          <a class="btn btn--light" href="contact.html#kontakt">{b1}</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="faq">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e4}</span>
      {h6}
    </div>
    {faq}
  </div>
</section>
""".format(
        e1=bi("Произход", "Origin"),
        h1=h(2, "„Децата — потенциални жертви на престъпления в интернет“", "“Children — potential victims of crime on the internet”"),
        p1=p(
            "Киберпрестъпленията са сред най-динамично развиващите се и иновативни форми на престъпна дейност. "
            "Анонимността в мрежата улеснява експлоатацията и злоупотребата с най-уязвимата част от обществото — децата. "
            "Използването на интернет от организирани престъпни групи за изготвяне и разпространение на материали със "
            "сексуална злоупотреба с деца и за трафик на деца е добре документирано от редица национални и международни организации.",
            "Cybercrime is among the fastest-developing and most inventive forms of criminal activity. Anonymity online makes "
            "it easier to exploit and abuse the most vulnerable part of society — children. The use of the internet by organised "
            "criminal groups to produce and distribute child sexual abuse material and to traffic children is well documented "
            "by a range of national and international organisations.",
        ),
        p2=p(
            "Проектът е разработен от ГДБОП по програма „Превенция и борба с престъпността“ на Европейската комисия. "
            "В рамките му бяха проведени десет дейности — от международна конференция по противодействието на сексуалната "
            "експлоатация и злоупотреба с деца в интернет, през познавателни посещения в Малта и Румъния, до разработването на "
            "стандартизирана обучителна програма и регионални обучения в Северна и Южна България.",
            "The project was developed by GDBOP under the European Commission’s Prevention of and Fight against Crime Programme. "
            "It comprised ten activities — from an international conference on countering the sexual exploitation and abuse of "
            "children online, through study visits to Malta and Romania, to the development of a standardised training programme "
            "and regional training sessions in northern and southern Bulgaria.",
        ),
        h2=h(3, "Данни за проекта", "Project data"),
        d1=bi("Номер", "Number"),
        d2=bi("Програма", "Programme"),
        v2=bi("„Превенция и борба с престъпността“, Европейска комисия", "Prevention of and Fight against Crime, European Commission"),
        d3=bi("Обща стойност", "Total value"),
        d4=bi("Грант от ЕК", "EC grant"),
        d5=bi("Съфинансиране", "Co-financing"),
        d6=bi("Бенефициент", "Beneficiary"),
        v6=bi("ГДБОП — МВР", "GDBOP — Ministry of Interior"),
        imgalt=esc("Международна конференция по проекта — „Child sexual exploitation in Bulgaria: scope of the problem and the way forward“"),
        imgcap=bi(
            "Международна конференция по противодействието на сексуалната експлоатация и злоупотреба с деца в интернет, София.",
            "International conference on countering the sexual exploitation and abuse of children online, Sofia.",
        ),
        e2=bi("Партньори", "Partners"),
        h3=h(2, "Бенефициент и партньори", "Beneficiary and partners"),
        p3=p("Проектът е изпълнен от ГДБОП съвместно с партньори от Румъния и Малта.",
             "The project was carried out by GDBOP together with partners from Romania and Malta.", cls="lede"),
        pcards=pcards,
        e3=bi("Доставчици на интернет", "Internet providers"),
        h4=h(2, "Направи интернет по-безопасно място", "Make the internet a safer place"),
        p4=p(
            "В края на 2012 г. България се присъедини към Глобалния алианс за борба със сексуалната експлоатация на деца онлайн. "
            "Една от набелязаните мерки е блокирането на достъпа до сайтове с детска сексуална експлоатация в участващите страни.",
            "At the end of 2012 Bulgaria joined the Global Alliance against Child Sexual Abuse Online. One of the measures "
            "identified is blocking access to child sexual exploitation sites in the participating countries.",
        ),
        p5=p(
            "Интерпол поддържа списък с домейни, за които е установено, че разпространяват снимки или видео материали със "
            "сексуална злоупотреба с деца. Списъкът се предоставя напълно безвъзмездно на всеки доставчик на интернет услуги, "
            "пожелал доброволно да участва. При опит за достъп браузърът пренасочва потребителя към стоп-страница.",
            "Interpol maintains a list of domains found to distribute images or video showing the sexual abuse of children. "
            "The list is supplied entirely free of charge to any internet service provider that chooses to take part. "
            "On an attempted visit, the browser redirects the user to a stop page.",
        ),
        p6=p(
            "<strong>Никаква информация за използвания от потребителя IP адрес не се съхранява.</strong> Мярката е превантивна: "
            "тя не премахва съдържанието, а ограничава достъпа до него — особено достъпа на малолетни и непълнолетни.",
            "<strong>No information about the user’s IP address is stored.</strong> The measure is preventive: it does not remove "
            "the content but limits access to it — above all the access of minors.",
        ),
        h5=h(3, "Вие сте доставчик на интернет услуги?", "Are you an internet service provider?"),
        p7=p("Свържете се с дирекция „Киберпрестъпност“, за да се включите доброволно в инициативата и да получите достъп до актуалния списък.",
             "Contact the Cybercrime Directorate to join the initiative voluntarily and gain access to the current list."),
        b1=bi("Свържете се с нас", "Get in touch"),
        e4=bi("Въпроси", "Questions"),
        h6=h(2, "Често задавани въпроси", "Frequently asked questions"),
        faq=faq_html,
    )

    page(
        "about.html",
        "За проекта — СпасиДете.БГ",
        "About the project — SpasiDete.BG",
        "За проекта „Децата — потенциални жертви на престъпления в интернет“ (HOME/2012/ISEC/FP/C2/4000003996), партньорите и инициативата за доставчиците на интернет услуги.",
        "About the project “Children — potential victims of crime on the internet” (HOME/2012/ISEC/FP/C2/4000003996), its partners and the initiative for internet service providers.",
        body,
    )


def build_contact():
    body = pagehead(
        "Контакти",
        "Contact",
        "Въпроси за сайта, за проекта или за включване в инициативата за доставчиците на интернет услуги.",
        "Questions about the site, the project or joining the initiative for internet service providers.",
        "Контакти", "Contact",
    ) + """
<section class="section section--tight">
  <div class="wrap">
    <div class="callout callout--red">
      {h0}
      {p0}
      <div class="btn-row" style="margin-top:18px">
        <a class="btn btn--danger btn--lg" href="tel:112">112</a>
        <a class="btn btn--ghost btn--lg" href="tel:116111">116 111</a>
        <a class="btn btn--ghost btn--lg" href="help.html#linii">{b0}</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--sky" id="kontakt">
  <div class="wrap">
    <div class="grid grid--2" style="align-items:start">
      <div class="contactbox">
        {h1}
        {p1}
        <dl>
          <dt>{l_addr}</dt>
          <dd>{v_addr}</dd>
          <dt>{l_tel}</dt>
          <dd><a href="tel:+35929828363">+359 2 982 83 63</a></dd>
          <dt>{l_mail}</dt>
          <dd><a href="mailto:spasidete@cybercrime.bg">spasidete@cybercrime.bg</a></dd>
        </dl>
      </div>
      <div>
        <div class="card" style="margin-bottom:18px">
          <div class="emblem-pair">
            {emb1}
            {emb2}
          </div>
          {h2}
          {p2}
          <div class="btn-row" style="margin-top:14px">
            <a class="btn btn--primary" href="https://www.cybercrime.bg/" target="_blank" rel="noopener">cybercrime.bg</a>
            <a class="btn btn--ghost" href="https://gdbop.bg/" target="_blank" rel="noopener">gdbop.bg</a>
          </div>
        </div>
        <div class="card">
          {h3}
          {p3}
          <div class="btn-row" style="margin-top:14px">
            <a class="btn btn--ghost" href="about.html#isp">{b3}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
""".format(
        h0=h(2, "Това не е канал за спешни сигнали", "This is not an emergency channel"),
        p0=p("Ако дете е в опасност в момента, не пишете имейл — обадете се.",
             "If a child is in danger right now, do not send an e-mail — call."),
        b0=bi("Всички линии за помощ", "All helplines"),
        h1=h(2, "Дирекция „Киберпрестъпност“, ГДБОП", "Cybercrime Directorate, GDBOP"),
        p1=p("Главна дирекция „Борба с организираната престъпност“ — Министерство на вътрешните работи.",
             "General Directorate for Combating Organised Crime — Ministry of Interior."),
        l_addr=bi("Адрес", "Address"),
        v_addr=bi("гр. София 1784, бул. „Цариградско шосе“ № 133А",
                  "133A Tsarigradsko shose Blvd., Sofia 1784, Bulgaria"),
        l_tel=bi("Телефон", "Phone"),
        l_mail=bi("Електронна поща", "E-mail"),
        emb1=emblem("cybercrime-gdbop", cls="emblem", w=341, h=420),
        emb2=emblem("gdbop-mvr", cls="emblem emblem--round", w=256, h=256),
        h2=h(3, "Подаване на сигнал", "Filing a report"),
        p2=p("За вредно и незаконно съдържание в интернет и за организирана престъпна дейност използвайте официалните канали.",
             "For harmful and illegal content online and for organised criminal activity, use the official channels."),
        h3=h(3, "Доставчици на интернет услуги", "Internet service providers"),
        p3=p("Включете се доброволно в инициативата за блокиране на достъпа до сайтове със сексуална злоупотреба с деца.",
             "Join the initiative for blocking access to child sexual abuse sites voluntarily."),
        b3=bi("Как работи", "How it works"),
    )

    page(
        "contact.html",
        "Контакти — СпасиДете.БГ",
        "Contact — SpasiDete.BG",
        "Дирекция „Киберпрестъпност“, ГДБОП — адрес, телефон и електронна поща. Спешни сигнали: 112 и 116 111.",
        "Cybercrime Directorate, GDBOP — address, phone and e-mail. Emergencies: 112 and 116 111.",
        body,
    )


# ==========================================================================

def build_report():
    """Страница „Подай сигнал“ с формуляр по области / the report page."""

    opts = []
    for bg, en, slug, tel, tl_bg, tl_en, mail, addr in C2.ODMVR:
        opts.append(
            '<option value="{slug}" data-mail="{mail}" data-tel="{tel}"{fb} '
            'data-bg="{bg}" data-en="{en}" data-addr="{addr}" '
            'data-tlbg="{tlbg}" data-tlen="{tlen}">{bg}</option>'.format(
                slug=slug, mail=(mail or C2.FALLBACK_EMAIL), tel=tel,
                fb=('' if mail else ' data-fallback="1"'),
                bg=esc(bg), en=esc(en), addr=esc(addr),
                tlbg=esc(tl_bg), tlen=esc(tl_en))
        )
    options = "\n          ".join(opts)

    rows = "".join(
        """<tr>
  <th scope="row">{bg}</th>
  <td data-l="{dl_tel}">{tel}</td>
  <td data-l="{dl_mail}">{mail}</td>
  <td class="t-addr" data-l="{dl_addr}">{addr}</td>
</tr>""".format(
            bg=bi(bg, en),
            tel=('<a href="tel:%s">%s</a><small>%s</small>' % (tel.replace(" ", ""), tel, bi(tl_bg, tl_en))) if tel else "<span class=\"muted\">—</span>",
            mail=('<a href="mailto:%s">%s</a>' % (mail, mail)) if mail else "<span class=\"muted\">—</span>",
            addr=esc(addr),
            dl_tel="Телефон", dl_mail="Електронна поща", dl_addr="Адрес",
        )
        for bg, en, slug, tel, tl_bg, tl_en, mail, addr in C2.ODMVR
    )

    others = "".join(
        '<article class="card">%s%s</article>' % (h(3, b, e), p(db, de))
        for b, e, db, de in C2.OTHER_CHANNELS
    )

    body = pagehead(
        "Подай сигнал",
        "File a report",
        "Опишете всички свидетелства или станали ви известни факти и обстоятелства около случая. "
        "Формулярът подготвя писмо до дежурната част на областната дирекция на МВР, която отговаря за мястото на случилото се.",
        "Describe every piece of evidence and every fact or circumstance of the case known to you. "
        "The form prepares a letter to the duty unit of the regional directorate responsible for the place where it happened.",
        "Подай сигнал", "File a report",
    ) + """
<section class="section section--rose section--tight">
  <div class="wrap">
    <div class="callout callout--red">
      <div class="grid grid--2" style="align-items:center;gap:26px">
        <div>
          {h0}
          {p0}
        </div>
        <div class="btn-row">
          <a class="btn btn--danger btn--lg" href="tel:112">{b112}</a>
          <a class="btn btn--ghost btn--lg" href="tel:116111">116 111</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="formulyar">
  <div class="wrap">
    <div class="grid" style="grid-template-columns:1.25fr .75fr;gap:46px;align-items:start" id="formgrid">
      <div>
        <span class="eyebrow">{e1}</span>
        {h1}
        {p1}

        <form class="sigform" id="sigform" novalidate>
          <div class="field">
            <label for="f-region">{l_region} <span class="req" aria-hidden="true">*</span></label>
            <select id="f-region" name="region" required>
              <option value="" data-ph-bg="— изберете област —" data-ph-en="— choose a region —">— изберете област —</option>
              {options}
            </select>
            <p class="hint">{hint_region}</p>
          </div>

          <div class="field">
            <label for="f-place">{l_place}</label>
            <input type="text" id="f-place" name="place" autocomplete="off">
            <p class="hint">{hint_place}</p>
          </div>

          <div class="field field--split">
            <div>
              <label for="f-when">{l_when}</label>
              <input type="text" id="f-when" name="when" autocomplete="off">
            </div>
            <div>
              <label for="f-who">{l_who}</label>
              <input type="text" id="f-who" name="who" autocomplete="off">
            </div>
          </div>

          <div class="field">
            <label for="f-what">{l_what} <span class="req" aria-hidden="true">*</span></label>
            <textarea id="f-what" name="what" rows="7" required></textarea>
            <p class="hint">{hint_what}</p>
          </div>

          <div class="field field--split">
            <div>
              <label for="f-name">{l_name}</label>
              <input type="text" id="f-name" name="name" autocomplete="name">
            </div>
            <div>
              <label for="f-contact">{l_contact}</label>
              <input type="text" id="f-contact" name="contact" autocomplete="email">
            </div>
          </div>
          <p class="hint">{hint_anon}</p>

          <div class="formnote">{note_privacy}</div>

          <div class="btn-row" style="margin-top:20px">
            <button class="btn btn--danger btn--lg" type="submit">{b_send}</button>
            <button class="btn btn--ghost" type="button" id="copybtn">{b_copy}</button>
          </div>
          <p class="hint" id="formstatus" role="status" aria-live="polite"></p>
        </form>
      </div>

      <aside class="sidepanel" id="regionbox">
        {h_panel}
        <dl>
          <dt>{l_dir}</dt><dd id="rb-name">{rb_empty}</dd>
          <dt>{l_tel}</dt><dd id="rb-tel">—</dd>
          <dt>{l_mail}</dt><dd id="rb-mail">—</dd>
          <dt>{l_addr}</dt><dd id="rb-addr">—</dd>
        </dl>
      </aside>
    </div>
  </div>
</section>

<section class="section section--azure">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e2}</span>
      {h2}
      {p2}
    </div>
    <div class="grid grid--2">{others}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e3}</span>
      {h3}
      {p3}
    </div>
    <div class="tablewrap" id="spravochnik">
      <table class="dirtable">
        <thead><tr><th scope="col">{th1}</th><th scope="col">{th2}</th><th scope="col">{th3}</th><th scope="col">{th4}</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <p class="note">{note_src}</p>
  </div>
</section>
""".format(
        h0=h(2, "Има ли дете в опасност в момента?", "Is a child in danger right now?"),
        p0=p("Не изчаквайте и не попълвайте формуляр. Обадете се.",
             "Do not wait and do not fill in a form. Call."),
        b112=bi("Звънни на 112", "Call 112"),
        e1=bi("Формуляр", "The form"),
        h1=h(2, "Опишете случая", "Describe the case"),
        p1=p("Попълнете каквото знаете. Бутонът отваря пощенската ви програма с готово писмо до "
             "избраната дирекция — вие го преглеждате и изпращате сами. Сайтът не съхранява нищо от написаното.",
             "Fill in what you know. The button opens your e-mail program with a ready letter to the "
             "directorate you chose — you review it and send it yourself. The site stores nothing you write.",
             cls="lede"),
        l_region=bi("Област, в която се е случило", "Region where it happened"),
        options=options,
        hint_region=bi("Ако не знаете областта, изберете тази, в която живеете, и опишете мястото по-долу.",
                       "If you do not know the region, choose the one you live in and describe the place below."),
        l_place=bi("Населено място, адрес, училище", "Town, address, school"),
        hint_place=bi("Например: гр. Пловдив, 25-то СУ, двора зад физкултурния салон.",
                      "For example: Plovdiv, School No. 25, the yard behind the gym."),
        l_when=bi("Кога се е случило", "When it happened"),
        l_who=bi("Възраст на детето", "The child’s age"),
        l_what=bi("Какво се е случило", "What happened"),
        hint_what=bi("Опишете всички свидетелства или станали ви известни факти и обстоятелства — кой, какво, кога, колко пъти, има ли свидетели.",
                     "Describe every piece of evidence and every fact known to you — who, what, when, how many times, whether there were witnesses."),
        l_name=bi("Вашето име (по избор)", "Your name (optional)"),
        l_contact=bi("Телефон или имейл (по избор)", "Phone or e-mail (optional)"),
        hint_anon=bi("Сигналът може да е анонимен. Без данни за контакт обаче институцията не може да поиска уточнения от вас.",
                     "A report can be anonymous. Without contact details, though, the institution cannot ask you for clarification."),
        note_privacy=bi(
            "<strong>Не прикачвайте снимки или видео на дете.</strong> Ако разполагате с такива, запазете ги "
            "и ги предайте лично на разследващия служител. Не ги разпространявайте и не ги публикувайте.",
            "<strong>Do not attach photographs or video of a child.</strong> If you have any, keep them safe and "
            "hand them over in person to the investigating officer. Do not share or publish them."),
        b_send=bi("Подготви писмото", "Prepare the letter"),
        b_copy=bi("Копирай текста", "Copy the text"),
        h_panel=h(3, "Към кого отива", "Where it goes"),
        rb_empty=bi("Изберете област", "Choose a region"),
        l_dir=bi("Дирекция", "Directorate"),
        l_tel=bi("Телефон", "Phone"),
        l_mail=bi("Електронна поща", "E-mail"),
        l_addr=bi("Адрес", "Address"),
        e2=bi("Други възможности", "Other options"),
        h2=h(2, "Сигнал може да подадете и тук", "You can also report here"),
        p2=p("Формулярът не е единственият път. Всеки от тези канали приема сигнал за дете в риск.",
             "The form is not the only route. Each of these channels accepts a report about a child at risk.",
             cls="lede"),
        others=others,
        e3=bi("Справочник", "Directory"),
        h3=h(2, "Областните дирекции на МВР", "The regional directorates"),
        p3=p("Телефоните са активни връзки — на телефон е достатъчно да докоснете номера.",
             "The phone numbers are active links — on a phone, simply tap the number.", cls="lede"),
        th1=bi("Област", "Region"),
        th2=bi("Телефон", "Phone"),
        th3=bi("Електронна поща", "E-mail"),
        th4=bi("Адрес", "Address"),
        rows=rows,
        note_src=bi(
            "Данните са взети от публичните страници за контакт на областните дирекции на mvr.bg и са проверени на 1 октомври 2026 г. "
            "Там, където дирекцията не публикува обща електронна поща, формулярът използва приемната на МВР: "
            "<a href=\"mailto:priemna@mvr.bg\">priemna@mvr.bg</a>.",
            "The data come from the published contact pages of the regional directorates on mvr.bg and were checked on 1 October 2026. "
            "Where a directorate publishes no general e-mail address, the form uses the Ministry’s public reception: "
            "<a href=\"mailto:priemna@mvr.bg\">priemna@mvr.bg</a>."),
    )

    page(
        "report.html",
        "Подай сигнал — СпасиДете.БГ",
        "File a report — SpasiDete.BG",
        "Формуляр за сигнал за насилие или агресия над дете, насочен към дежурната част на съответната областна дирекция на МВР, плюс справочник с контактите на всички ОДМВР.",
        "A form for reporting violence or aggression against a child, addressed to the duty unit of the relevant regional directorate, plus a directory of all regional directorates.",
        body,
    )


def build_campaigns():
    items = []
    for c in C2.CAMPAIGNS:
        if c["youtube"]:
            # Плейърът на YouTube тежи над мегабайт и слага бисквитки, затова
            # се зарежда чак когато посетителят натисне „Пусни“.
            # The YouTube player weighs over a megabyte and sets cookies, so it
            # loads only once the visitor presses play.
            media = """<div class="videobox">
        <div class="videobox__frame videofacade" data-yt="{yt}" data-title="{t}">
          {poster}
          <button class="videofacade__btn" type="button" aria-label="{play}">
            <span class="videofacade__play" aria-hidden="true"></span>
          </button>
          <span class="videofacade__hint">{hint}</span>
        </div>
        {credit}
      </div>""".format(
                yt=c["youtube"], t=esc(c["title_bg"]),
                poster=pic(c["photo"], c["photo_alt_bg"], sizes="(max-width: 960px) 92vw, 46vw"),
                play=esc("Пусни видеото / Play the video"),
                hint=bi("Натиснете, за да пуснете видеото от YouTube",
                        "Press to load the video from YouTube"),
                credit=('<p class="videocredit">%s</p>' % bi(c["credit_bg"], c["credit_en"]))
                       if c.get("credit_bg") else "")
        else:
            media = '<figure class="figure">%s<figcaption>%s</figcaption></figure>' % (
                pic(c["photo"], c["photo_alt_bg"], sizes="(max-width: 960px) 92vw, 46vw"),
                bi(c["photo_alt_bg"], c["photo_alt_en"]))

        items.append("""<article class="campaign" id="{i}">
  <div class="campaign__text">
    {t}
    {l}
    {b}
  </div>
  <div class="campaign__media">{media}</div>
</article>""".format(
            i=c["id"],
            t=h(2, c["title_bg"], c["title_en"]),
            l=p(c["lead_bg"], c["lead_en"], cls="lede"),
            b="".join(p(x, y) for x, y in zip(c["body_bg"], c["body_en"])),
            media=media,
        ))

    gallery = "".join(
        '<figure class="galitem">%s<figcaption>%s</figcaption></figure>' % (
            pic(f, abg, sizes="(max-width: 620px) 88vw, 280px"), bi(abg, aen))
        for f, abg, aen in C2.CAMPAIGN_GALLERY
    )

    body = pagehead(
        "Кампании на МВР",
        "Ministry of Interior campaigns",
        "Превенцията не е еднократно събитие. Това са програмите и кампаниите, с които МВР работи с деца, родители и училища.",
        "Prevention is not a one-off event. These are the programmes and campaigns through which the Ministry works with children, parents and schools.",
        "Кампании", "Campaigns",
    ) + """
<section class="section">
  <div class="wrap">
    {items}
  </div>
</section>

<section class="section section--azure" id="video">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e2}</span>
      {h2}
      {p2}
    </div>
    <div class="videoslot">
      <div class="videobox__frame videofacade" data-yt="{v_id}" data-title="{v_title}">
        {v_poster}
        <button class="videofacade__btn" type="button" aria-label="{v_play}">
          <span class="videofacade__play" aria-hidden="true"></span>
        </button>
        <span class="videofacade__hint">{v_hint}</span>
      </div>
      <p class="videocredit">{v_credit}</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{e3}</span>
      {h3}
    </div>
    <div class="gallery">{gallery}</div>
  </div>
</section>
""".format(
        items="".join(items),
        e2=bi("Видео", "Video"),
        h2=h(2, "Кампания на МВР „Спаси Дете“", "The Ministry of Interior’s “Save a child” campaign"),
        p2=p("Видеото на платформата. Зарежда се само когато го пуснете — дотогава YouTube не получава нищо за вас.",
             "The platform’s video. It loads only when you press play — until then YouTube receives nothing about you.",
             cls="lede"),
        v_id=C2.PLATFORM_VIDEO["youtube"],
        v_title=esc(C2.PLATFORM_VIDEO["title_bg"]),
        v_poster=pic(C2.PLATFORM_VIDEO["poster"], C2.PLATFORM_VIDEO["poster_alt_bg"],
                     sizes="(max-width: 880px) 92vw, 820px"),
        v_play=esc("Пусни видеото / Play the video"),
        v_hint=bi("Натиснете, за да пуснете видеото от YouTube",
                  "Press to load the video from YouTube"),
        v_credit=bi(C2.PLATFORM_VIDEO["credit_bg"], C2.PLATFORM_VIDEO["credit_en"]),
        e3=bi("Галерия", "Gallery"),
        h3=h(2, "От дейностите", "From the activities"),
        gallery=gallery,
    )

    page(
        "campaigns.html",
        "Кампании на МВР — СпасиДете.БГ",
        "Ministry of Interior campaigns — SpasiDete.BG",
        "„Добрият пример“, „Насилието е безсилие“ и „Никога повече насилие у дома“ — програмите и кампаниите на МВР за превенция на агресията сред деца.",
        "“The Good Example”, “Violence is powerlessness” and “Never again violence at home” — the Ministry’s programmes for preventing aggression among children.",
        body,
    )


def build_404():
    body = """
<section class="section" style="text-align:center">
  <div class="wrap" style="max-width:640px">
    {h1}
    {p1}
    <div class="btn-row" style="justify-content:center;margin-top:26px">
      <a class="btn btn--primary btn--lg" href="index.html">{b1}</a>
      <a class="btn btn--ghost btn--lg" href="help.html">{b2}</a>
    </div>
  </div>
</section>
""".format(
        h1=h(1, "Страницата не е намерена", "Page not found"),
        p1=p("Адресът, който отворихте, не съществува или е бил преместен.",
             "The address you opened does not exist or has been moved.", cls="lede center-wrap"),
        b1=bi("Към началната страница", "Go to the home page"),
        b2=bi("Потърси помощ", "Get help"),
    )
    page("404.html", "Страницата не е намерена — СпасиДете.БГ",
         "Page not found — SpasiDete.BG",
         "Страницата не е намерена.", "Page not found.", body)


def build_extras():
    base = SITE_BASE
    urls = ["index.html"] + [f for f, _, _ in NAV] + ["report.html", "contact.html"]
    items = "".join(
        '  <url><loc>%s%s</loc><changefreq>monthly</changefreq><priority>%s</priority></url>\n'
        % (base, "" if u == "index.html" else u, "1.0" if u == "index.html" else "0.7")
        for u in urls
    )
    with open(os.path.join(HERE, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + items + "</urlset>\n")
    with open(os.path.join(HERE, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write("User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % base)
    # GitHub Pages: не обработвай с Jekyll / do not process with Jekyll
    open(os.path.join(HERE, ".nojekyll"), "w").close()
    print("  -> sitemap.xml, robots.txt, .nojekyll")


def main():
    _scan_photos()
    print("Building СпасиДете.БГ …")
    build_index()
    build_bullying()
    build_advice()
    build_help()
    build_news()
    build_resources()
    build_about()
    build_contact()
    build_report()
    build_campaigns()
    build_404()
    build_extras()
    print("Done.")


if __name__ == "__main__":
    main()
