#!/usr/bin/env python3
"""Translated copies of the site (zh, ja, ko, fil) built from the English pages.

    python3 tools/i18n.py extract    write the strings still missing a translation to i18n/work/batch-NN.en.json
    python3 tools/i18n.py merge      fold i18n/work/batch-NN.<lang>.json into i18n/<lang>.json
    python3 tools/i18n.py build      write <lang>/<page>.html, the language picker, hreflang tags and sitemap entries
    python3 tools/i18n.py report     translation coverage per page and language

i18n/<lang>.json maps an English string to its translation. A page is only published in a language once at least
MIN_COVER of its strings are translated, so languages and pages can be rolled out in stages. Run after
build-content.py and clean-urls.py. Idempotent.
"""
import glob, html, json, os, re, sys

SITE = 'https://themillsglobal.com'
MIN_COVER = 0.97
BATCH = 110

LANGS = {
    'zh':  dict(html='zh-CN', hreflang='zh-Hans', locale='zh_CN', name='简体中文', short='中文', aria='语言', en='Chinese'),
    'ja':  dict(html='ja', hreflang='ja', locale='ja_JP', name='日本語', short='日本語', aria='言語', en='Japanese'),
    'ko':  dict(html='ko', hreflang='ko', locale='ko_KR', name='한국어', short='한국어', aria='언어', en='Korean'),
    'fil': dict(html='fil', hreflang='fil', locale='fil_PH', name='Filipino', short='FIL', aria='Wika'),
}
EN = dict(html='en', hreflang='en', locale='en_PH', name='English', short='EN', aria='Language')

CORE = ['index', 'about', 'contact', 'location', 'talk-to-a-broker', 'book-a-call', 'learning-pavilion', 'industries']
PAGES = CORE + sorted(f[:-5] for f in glob.glob('services-*.html')) + sorted(f[:-5] for f in glob.glob('industries-*.html'))
PAGES = [p for p in PAGES if os.path.exists(f'{p}.html')]

PICKER = re.compile(r'[ \t]*<!-- i18n:lang -->.*?<!-- /i18n:lang -->\n?', re.S)
ALTS = re.compile(r'[ \t]*<!-- i18n:alternates -->.*?<!-- /i18n:alternates -->\n?', re.S)
TOKENS = re.compile(r'(<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>|<svg\b.*?</svg>|<noscript\b.*?</noscript>|<[^>]+>)', re.S)
TEXT_ATTRS = ('alt', 'title', 'aria-label', 'placeholder')
META_KEYS = ('description', 'og:title', 'og:description', 'twitter:title', 'twitter:description')
ASSET_DIRS = ('css/', 'js/', 'assets/', 'content/')


KEEP = {'Instagram', 'Facebook', 'LinkedIn', 'YouTube', 'X', 'Threads', 'Crossy Customs', 'Manila · Cebu · Subic Bay',
        'THE MILLS GLOBAL CUSTOMS BROKERAGE', 'The Mills Global', 'JFK → LAX'}   # brand and place names stay as written


def skip(s):
    if s in KEEP or re.match(r'#\w+$', s) or re.match(r'(Level 24|Suite 301) ', s):
        return True
    if not re.search(r'[A-Za-z]', s) or re.match(r'(IMAGE|FLOAT): ', s) or re.match(r'\d+×\d+ ', s):
        return True
    if re.fullmatch(r'[\w.+-]+@[\w-]+(\.[\w-]+)+', s) or s.startswith(('http://', 'https://')):
        return True
    return bool(re.fullmatch(r'[\d.,+%KkMm/\s:-]+', s))


def attr_skip(k):
    """Image-slot labels such as 'IMAGE: assets/...jpg' or 'Heading: about who we are' are build placeholders."""
    return bool(re.match(r'(IMAGE|FLOAT): ', k) or re.search(r': [a-z0-9]+(?: [a-z0-9]+)*$', k))


def norm(s):
    return ' '.join(html.unescape(s).split())


def attr_texts(tag):
    """(attribute value, ...) of a tag that carry visible or searchable text."""
    out = []
    for a in TEXT_ATTRS:
        for m in re.finditer(r'(?<=[\s])' + a + r'="([^"]*)"', tag):
            if not attr_skip(norm(m.group(1))):
                out.append(m.group(1))
    if tag.startswith('<meta'):
        k = re.search(r'(?:name|property)="([^"]*)"', tag)
        c = re.search(r'content="([^"]*)"', tag)
        if k and c and k.group(1) in META_KEYS:
            out.append(c.group(1))
    return out


def strip_i18n(s):
    return ALTS.sub('', PICKER.sub('', s))


def strings(src):
    seen, out = set(), []
    for part in TOKENS.split(strip_i18n(src)):
        if not part:
            continue
        if part.startswith('<'):
            vals = attr_texts(part) if not part.startswith(('<!--', '<script', '<style', '<svg', '<noscript')) else []
        else:
            vals = [part]
        for v in vals:
            k = norm(v)
            if k and not skip(k) and k not in seen:
                seen.add(k); out.append(k)
    return out


def load(lang):
    p = f'i18n/{lang}.json'
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}


def page_url(lang, slug):
    if lang is None:
        return f"{SITE}/{'' if slug == 'index' else slug}"
    return f"{SITE}/{lang}" + ('' if slug == 'index' else f'/{slug}')


def fix_url(u, lang, live):
    """Make a relative URL from a root page work from /<lang>/<page>."""
    if not u or re.match(r'(https?:|#|mailto:|tel:|/|data:|javascript:)', u):
        return u
    m = re.match(r'([^?#]*)(\?[^#]*)?(#.*)?$', u)
    base, q, frag = m.group(1), m.group(2) or '', m.group(3) or ''
    b = base[2:] if base.startswith('./') else base
    b = b.rstrip('/')
    if b.endswith('.html'):
        b = b[:-5]
    if b in ('', '.', 'index'):
        return (f'/{lang}' if 'index' in live else '/') + q + frag
    if b.startswith(ASSET_DIRS) or '.' in os.path.basename(b):
        return '/' + b + q + frag
    if b in live:
        return f'/{lang}/{b}' + q + frag
    return '/' + b + q + frag


def translate_page(src, lang, d, live, slug):
    cfg = LANGS[lang]
    miss = []

    def tr(v, text=False):
        k = norm(v)
        if not k or skip(k) or (not text and attr_skip(k)):
            return v
        t = d.get(k)
        if not t:
            miss.append(k)
            return v
        t = html.escape(t, quote=not text)
        if text and lang in ('zh', 'ja', 'ko'):   # no spaces around inline elements in CJK text
            return t
        if text:  # keep the original surrounding whitespace
            return v[:len(v) - len(v.lstrip())] + t + v[len(v.rstrip()):]
        return t

    out = []
    for part in TOKENS.split(strip_i18n(src)):
        if not part:
            continue
        if part.startswith('<') and not part.startswith(('<!--', '<script', '<style', '<svg', '<noscript')):
            tag = part
            for a in TEXT_ATTRS:
                tag = re.sub(r'(?<=[\s])(' + a + r')="([^"]*)"', lambda m: f'{m.group(1)}="{tr(m.group(2))}"', tag)
            if tag.startswith('<meta'):
                k = re.search(r'(?:name|property)="([^"]*)"', tag)
                if k and k.group(1) in META_KEYS:
                    tag = re.sub(r'content="([^"]*)"', lambda m: f'content="{tr(m.group(1))}"', tag)
                if k and k.group(1) == 'og:locale':
                    tag = re.sub(r'content="[^"]*"', f'content="{cfg["locale"]}"', tag)
                if k and k.group(1) == 'og:url':
                    tag = re.sub(r'content="[^"]*"', f'content="{page_url(lang, slug)}"', tag)
            if tag.startswith('<link') and 'rel="canonical"' in tag:
                tag = re.sub(r'href="[^"]*"', f'href="{page_url(lang, slug)}"', tag)
            elif not (tag.startswith('<link') and 'rel="alternate"' in tag):
                tag = re.sub(r'\b(href|src|data-img|poster|data-src|action)="([^"]*)"',
                             lambda m: f'{m.group(1)}="{fix_url(m.group(2), lang, live)}"', tag)
            tag = re.sub(r'^<html lang="en"', f'<html lang="{cfg["html"]}"', tag)
            out.append(tag)
        elif part.startswith('<script'):      # external scripts need absolute paths too; inline code is left alone
            m = re.match(r'<script\b[^>]*>', part)
            head = re.sub(r'\b(src)="([^"]*)"', lambda k: f'{k.group(1)}="{fix_url(k.group(2), lang, live)}"', m.group(0))
            out.append(head + part[m.end():])
        elif part.startswith('<'):
            out.append(part)
        else:
            out.append(tr(part, text=True))
    return ''.join(out), miss


def label(c):
    """A language's own name, with its English name beside it when the script is not Latin."""
    return c['name'] + (f'<small class="lang__en" lang="en">{c["en"]}</small>' if 'en' in c else '')


def picker(cur, slug, live_by_lang):
    """Desktop <li> and mobile <details> language switchers, as marker-wrapped blocks."""
    cfg = EN if cur == 'en' else LANGS[cur]
    items = [('en', EN, f"/{'' if slug == 'index' else slug}" if slug else '/')]
    for code, c in LANGS.items():
        if slug and slug in live_by_lang.get(code, ()):
            href = f'/{code}' + ('' if slug == 'index' else f'/{slug}')
        else:
            href = f'/{code}' if 'index' in live_by_lang.get(code, ()) else None
        if href:
            items.append((code, c, href))
    if len(items) < 2:
        return '', ''
    links = ''.join(f'<a href="{h}" hreflang="{c["hreflang"]}" lang="{c["html"]}"'
                    + (' aria-current="true"' if code == cur else '') + f'>{label(c)}</a>' for code, c, h in items)
    globe = ('<svg class="lang__globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
             'stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/>'
             '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>')
    chev = ('<svg class="nav__link-btn__chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>')
    desk = (f'<!-- i18n:lang -->\n        <li class="nav__item nav__item--dropdown nav__item--lang"><button class="nav__link-btn" type="button" '
            f'aria-haspopup="true" aria-label="{cfg["aria"]}">{globe}<span>{cfg["short"]}</span>{chev}</button>'
            f'<div class="nav__dropdown nav__dropdown--right">{links}</div></li>\n        <!-- /i18n:lang -->\n')
    mob = (f'<!-- i18n:lang -->\n      <details class="nav__mobile-group"><summary>{globe}{cfg["aria"]}</summary>'
           f'<div class="nav__mobile-sublist">{links}</div></details>\n      <!-- /i18n:lang -->\n')
    return desk, mob


def with_picker(src, cur, slug, live_by_lang):
    src = PICKER.sub('', src)
    desk, mob = picker(cur, slug, live_by_lang)
    if not desk:
        return src
    a = src.find('<ul class="nav__links">')
    if a >= 0:
        e = src.index('</ul>', a)
        src = src[:e] + desk + '      ' + src[e:]
    m = re.search(r'[ \t]*<a [^>]*class="nav__mobile-cta"', src)
    if m:
        src = src[:m.start()] + mob + src[m.start():]
    return src


def with_alternates(src, slug, live_by_lang, add_css=False):
    src = ALTS.sub('', src)
    langs = [(c, LANGS[c]['hreflang']) for c in LANGS if slug in live_by_lang.get(c, ())]
    if langs:
        rows = [f'  <link rel="alternate" hreflang="en" href="{page_url(None, slug)}">']
        rows += [f'  <link rel="alternate" hreflang="{h}" href="{page_url(c, slug)}">' for c, h in langs]
        rows.append(f'  <link rel="alternate" hreflang="x-default" href="{page_url(None, slug)}">')
        block = '  <!-- i18n:alternates -->\n' + '\n'.join(rows) + '\n  <!-- /i18n:alternates -->\n'
        m = re.search(r'[ \t]*<link rel="canonical"[^>]*>\n', src)
        if m:
            src = src[:m.end()] + block + src[m.end():]
    return src


def coverage(slug, lang, dicts):
    ss = strings(open(f'{slug}.html', encoding='utf-8').read())
    have = sum(1 for s in ss if s in dicts[lang])
    return (have / len(ss) if ss else 1.0), len(ss) - have


def all_english_pages():
    return sorted(glob.glob('*.html') + glob.glob('articles/*.html') + glob.glob('news/*.html'))


def cmd_extract():
    dicts = {l: load(l) for l in LANGS}
    todo, seen = [], set()
    group = sys.argv[2] if len(sys.argv) > 2 else 'all'
    pick = {'core': CORE, 'services': [p for p in PAGES if p.startswith('services-')],
            'industries': [p for p in PAGES if p.startswith('industries-')], 'all': PAGES}[group]
    for slug in pick:
        for s in strings(open(f'{slug}.html', encoding='utf-8').read()):
            if s not in seen and any(s not in dicts[l] for l in LANGS):
                seen.add(s); todo.append(s)
    os.makedirs('i18n/work', exist_ok=True)
    for f in glob.glob('i18n/work/batch-*.en.json'):
        os.remove(f)
    for i in range(0, len(todo), BATCH):
        chunk = {str(j + 1): s for j, s in enumerate(todo[i:i + BATCH])}
        json.dump(chunk, open(f'i18n/work/batch-{i // BATCH + 1:02d}.en.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{len(todo)} strings to translate in {(len(todo) + BATCH - 1) // BATCH} batches')


def cmd_merge():
    for f in sorted(glob.glob('i18n/work/batch-*.en.json')):
        en = json.load(open(f, encoding='utf-8'))
        for lang in LANGS:
            p = f.replace('.en.json', f'.{lang}.json')
            if not os.path.exists(p):
                continue
            tr = json.load(open(p, encoding='utf-8'))
            bad = [k for k in en if not str(tr.get(k, '')).strip()]
            if bad or set(tr) - set(en):
                print(f'{p}: missing {bad[:8]} extra {sorted(set(tr) - set(en))[:8]}')
                continue
            d = load(lang)
            d.update({en[k]: tr[k] for k in en})
            os.makedirs('i18n', exist_ok=True)
            json.dump(d, open(f'i18n/{lang}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
            print(f'{p}: merged {len(en)}')


def cmd_report():
    dicts = {l: load(l) for l in LANGS}
    print(f"{'page':48}" + ''.join(f'{l:>9}' for l in LANGS))
    for slug in PAGES:
        print(f'{slug:48}' + ''.join(f'{coverage(slug, l, dicts)[0] * 100:8.0f}%' for l in LANGS))


def cmd_build():
    dicts = {l: load(l) for l in LANGS}
    live_by_lang = {l: {s for s in PAGES if dicts[l] and coverage(s, l, dicts)[0] >= MIN_COVER} for l in LANGS}
    live_by_lang = {l: v for l, v in live_by_lang.items() if 'index' in v}      # a language needs its Home page
    # English pages: picker + alternates
    for f in all_english_pages():
        slug = f[:-5]
        src = open(f, encoding='utf-8').read()
        out = with_alternates(with_picker(src, 'en', slug if slug in PAGES else None, live_by_lang), slug, live_by_lang)
        if out != src:
            open(f, 'w', encoding='utf-8').write(out)
    # translated pages
    for lang in LANGS:
        for stale in glob.glob(f'{lang}/*.html'):
            if os.path.basename(stale)[:-5] not in live_by_lang.get(lang, ()):
                os.remove(stale)
        if lang not in live_by_lang:
            continue
        os.makedirs(lang, exist_ok=True)
        for slug in sorted(live_by_lang[lang]):
            src = open(f'{slug}.html', encoding='utf-8').read()
            out, miss = translate_page(src, lang, dicts[lang], live_by_lang[lang], slug)
            out = with_picker(out, lang, slug, live_by_lang)
            out = with_alternates(out, slug, live_by_lang)
            if '/css/lang.css' not in out:
                out = re.sub(r'(<link rel="stylesheet" href="/css/sections\.css[^>]*>\n)', r'\1  <link rel="stylesheet" href="/css/lang.css?v=2">\n', out, 1)
            open(f'{lang}/{slug}.html', 'w', encoding='utf-8').write(out)
    # sitemap
    if os.path.exists('sitemap.xml'):
        sm = open('sitemap.xml', encoding='utf-8').read()
        sm = re.sub(r'  <url><loc>' + re.escape(SITE) + r'/(zh|ja|ko|fil)(/[^<]*)?</loc></url>\n', '', sm)
        add = ''.join(f"  <url><loc>{page_url(l, s)}</loc></url>\n" for l in LANGS for s in PAGES if s in live_by_lang.get(l, ()))
        open('sitemap.xml', 'w', encoding='utf-8').write(sm.replace('</urlset>', add + '</urlset>'))
    for l in LANGS:
        print(l, len(live_by_lang.get(l, ())), 'pages')


if __name__ == '__main__':
    {'extract': cmd_extract, 'merge': cmd_merge, 'build': cmd_build, 'report': cmd_report}[sys.argv[1] if len(sys.argv) > 1 else 'report']()
