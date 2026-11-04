#!/usr/bin/env python3
"""Moves the site's dark navy family (#212431 and its shades) to the new brand navy #1F3244.
Primary maps exactly; the shades keep their relative lightness and take the new hue/saturation.
Idempotent (new values are never keys). Leaves the slate #4F5D75, the night-sky blacks and pure black overlays alone."""
import re, glob, os, io, colorsys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OLD_P, NEW_P = (33, 36, 49), (31, 50, 68)
def to_hls(r, g, b): return colorsys.rgb_to_hls(r/255, g/255, b/255)
oh, ol, os_ = to_hls(*OLD_P); nh, nl, ns = to_hls(*NEW_P)
def derive(rgb):
    if rgb == OLD_P: return NEW_P
    h, l, s = to_hls(*rgb)
    nl2 = min(0.95, max(0.02, l * (nl / ol)))
    ns2 = ns * min(1.0, s / os_)          # same saturation as the new navy (never more)
    r, g, b = colorsys.hls_to_rgb(nh, nl2, ns2)
    return tuple(round(x * 255) for x in (r, g, b))
# colours to move (hex as written in the code, upper-case) and the rgb triples used in rgba()/rgb()
HEX = ['#212431', '#1A1D29', '#2A2F41', '#2A2E40', '#30364B', '#3B475C', '#181A24', '#2F3B5C']
RGB = [(33, 36, 49), (17, 19, 28), (24, 26, 38), (14, 17, 26), (22, 30, 58), (26, 36, 70), (20, 26, 48)]
def h2t(h): return (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))
def t2h(t): return '#%02X%02X%02X' % t
hexmap = {h: t2h(derive(h2t(h))) for h in HEX}
rgbmap = {t: derive(t) for t in RGB}
if __name__ == '__main__' and os.environ.get('SHOW'):
    for k, v in hexmap.items(): print(k, '->', v)
    for k, v in rgbmap.items(): print(k, '->', v)
files = [f for f in glob.glob('css/*.css') + glob.glob('js/*.js') + glob.glob('*.html') + glob.glob('tools/*.py') + glob.glob('tools/*.js') + glob.glob('admin/*') + glob.glob('articles/*.html') + glob.glob('news/*.html')
         if os.path.isfile(f) and not f.endswith(('recolor-navy.py',))]
n = 0
for f in files:
    try: s = io.open(f, encoding='utf-8').read()
    except Exception: continue
    o = s
    for old, new in hexmap.items(): s = re.sub(re.escape(old) + r'(?![0-9A-Fa-f])', new, s, flags=re.I)
    def rg(m):
        t = (int(m.group(2)), int(m.group(3)), int(m.group(4)))
        if t in rgbmap: nt = rgbmap[t]; return f'{m.group(1)}{nt[0]}{m.group(5)}{nt[1]}{m.group(6)}{nt[2]}'
        return m.group(0)
    s = re.sub(r'(rgba?\(\s*)(\d+)(\s*,\s*)(\d+)(\s*,\s*)(\d+)', lambda m: (lambda t: (f'{m.group(1)}{rgbmap[t][0]}{m.group(3)}{rgbmap[t][1]}{m.group(5)}{rgbmap[t][2]}' if t in rgbmap else m.group(0)))((int(m.group(2)), int(m.group(4)), int(m.group(6)))), s)
    if s != o: io.open(f, 'w', encoding='utf-8').write(s); n += 1
print('recolored', n, 'files')
