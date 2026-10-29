#!/usr/bin/env python3
"""Clean URLs: the files stay NAME.html on disk, but every link, canonical, og:url, JSON-LD url, sitemap entry and
email link points at the extensionless address (Vercel serves it with "cleanUrls": true; GitHub Pages does too).
Idempotent. Run LAST in any build (build-content.py calls it at the end)."""
import re, glob, os, io, json
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
HOST = r'https?://(?:www\.)?themillsglobal\.com/'

def fix_path(p, absolute):
    m = re.match(r'^([^?#]*?)\.html([?#].*)?$', p, re.S)
    if not m: return p
    core, rest = m.group(1), m.group(2) or ''
    if core == 'index' or core.endswith('/index'): core = core[:-5]
    if core == '' and not absolute: core = './'
    return core + rest

def fix_value(v):
    if re.match(r'^(#|mailto:|tel:|javascript:|data:|//)', v): return v
    m = re.match(r'^(' + HOST + r')(.*)$', v, re.S)
    if m: return m.group(1) + fix_path(m.group(2), True)
    if re.match(r'^[a-z][a-z0-9+.-]*:', v, re.I): return v        # other sites (tag manager etc.)
    return fix_path(v, False)

def clean_html(s):
    s = re.sub(r'(\b(?:href|data-href|action)=")([^"]*)(")', lambda m: m.group(1) + fix_value(m.group(2)) + m.group(3), s)
    # content="https://themillsglobal.com/x.html" (og:url etc.) and any absolute site URL in JSON-LD or text
    s = re.sub(r'(' + HOST + r')([A-Za-z0-9/_-]*?)(?:/?index)?\.html(?=[#?"\'\s<,)]|$)', lambda m: m.group(1) + m.group(2), s)
    return s

changed = 0
def write(path, new, old):
    global changed
    if new != old: io.open(path, 'w', encoding='utf-8').write(new); changed += 1

for f in glob.glob('*.html') + glob.glob('articles/*.html') + glob.glob('news/*.html'):
    s = io.open(f, encoding='utf-8').read(); write(f, clean_html(s), s)
# sitemap + n8n emails: absolute site URLs only
for f in ['sitemap.xml'] + glob.glob('n8n/**/*.json', recursive=True):
    if not os.path.exists(f): continue
    s = io.open(f, encoding='utf-8').read()
    n = re.sub(r'(' + HOST + r')([A-Za-z0-9/_-]*?)(?:/?index)?\.html(?=[#?"\'\s<,)\\]|$)', lambda m: m.group(1) + m.group(2), s)
    write(f, n, s)
# post index used by the blog listing
f = 'content/posts.json'
if os.path.exists(f):
    s = io.open(f, encoding='utf-8').read(); n = re.sub(r'("url": "(?:articles|news)/[^"]*?)\.html"', r'\1"', s); write(f, n, s)
print('clean URLs:', changed, 'files changed')
