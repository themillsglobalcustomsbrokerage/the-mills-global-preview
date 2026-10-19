#!/usr/bin/env python3
"""On each industry page, moves 'Common Challenges' out of the Regulatory Focus section into its own dark,
image-backed section directly after the cargo cards (same style as Regulatory Focus). Idempotent."""
import re, glob, os, html
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def block_end(h, start):
    """Index just after the </div> that closes the <div> opening at `start`."""
    depth = 0
    for m in re.finditer(r'<div\b|</div>', h[start:]):
        depth += 1 if m.group(0) != '</div>' else -1
        if depth == 0: return start + m.end()
    raise ValueError('unbalanced')


n = 0
for f in sorted(glob.glob('industries-*.html')):
    slug = f[len('industries-'):-5]
    h = open(f).read()
    if 'id="common-challenges"' in h: continue
    ci = h.find('Common Challenges')
    s = h.rfind('<div class="insight-block">', 0, ci)
    e = block_end(h, s)
    block = h[s:e]
    title = re.search(r'<h3 class="insight-block__title">(.*?)</h3>', block, re.S).group(1)
    grid = re.search(r'(<div class="info-grid info-grid--3">.*?</div>\s*</div>)\s*$', block, re.S)
    grid_html = re.search(r'<div class="info-grid.*', block, re.S).group(0)
    grid_html = grid_html[:grid_html.rfind('</div>')].rstrip()      # drop the insight-block's own closing tag
    # remove from Regulatory Focus (and the blank line it leaves)
    h = h[:s].rstrip(' \n') + '\n' + h[e:].lstrip('\n')
    cta = re.search(r'<div class="cta-pair">.*?</div>', h[h.find('Regulatory Focus'):], re.S).group(0)
    cta = cta.replace('data-ga-label="regulatory-focus"', 'data-ga-label="common-challenges"')
    section = f'''  <!-- ============================================ -->
  <!-- COMMON CHALLENGES                            -->
  <!-- ============================================ -->
  <section class="section section--dark section--img-bg" id="common-challenges">
    <div class="img-slot img-slot--bg" data-img="assets/images/challenges/{slug}.jpg" role="img" aria-label="{html.escape(re.sub('<[^>]+>', '', title))}"><span class="img-slot__label">IMAGE: assets/images/challenges/{slug}.jpg</span></div>
    <div class="container">
      <div class="services-intro">
        <p class="section__eyebrow animate-in">Common Challenges</p>
        <h2 class="services-intro__heading animate-in" data-delay="1">{title}</h2>
      </div>
      <div style="margin-top: var(--space-2xl);">
        {grid_html}
      </div>
      {cta}
    </div>
  </section>

  <section class="section section--paper">
    <div class="container">
'''
    # split the cargo section right before the "Who We Help" block
    w = h.find('<div class="insight-block">\n        <p class="section__eyebrow">Who We Help</p>')
    assert w > 0, f
    ins = h.rfind('      </div>\n', 0, w) + len('      </div>\n')          # end of the cargo grid
    h = h[:ins] + '    </div>\n  </section>\n\n' + section + '      ' + h[w:].lstrip()
    open(f, 'w').write(h); n += 1
print('industry pages restructured:', n)
