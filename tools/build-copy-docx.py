#!/usr/bin/env python3
"""Builds docs/SERVICE-INDUSTRY-COPY.docx: for each service, the Home slider (scope) description and the hero (benefit) copy;
for each industry, the hero (benefit) copy. Reads the live pages so it always matches the site. No dependencies."""
import re, html, os, zipfile
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
def clean(t): return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t))).strip()
def x(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
idx = open('index.html', encoding='utf-8').read()
# order and names come from the site's own navigation
navs = re.findall(r'<div class="nav__dropdown nav__dropdown--wide">(.*?)</div>', idx, re.S)
def links(block, prefix): return [(m.group(1), clean(m.group(2))) for m in re.finditer(r'<a href="(' + prefix + r'[^"]+\.html)">(.*?)</a>', block)]
services = links(navs[0], 'services-'); industries = links(navs[1], 'industries-')
slides = {clean(t): clean(d) for t, d in re.findall(r'service-slide__title">(.*?)</h3>\s*<p class="service-slide__text">(.*?)</p>', idx, re.S)}
def hero(f): return clean(re.search(r'service-hero__subtitle">(.*?)</p>', open(f, encoding='utf-8').read(), re.S).group(1))

body = []
def p(text='', style=None, runs=None, num=False):
    ppr = ''
    if style: ppr += f'<w:pStyle w:val="{style}"/>'
    if num: ppr += '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
    r = runs or [(text, False)]
    rx = ''.join(f'<w:r>{"<w:rPr><w:b/></w:rPr>" if b else ""}<w:t xml:space="preserve">{x(t)}</w:t></w:r>' for t, b in r)
    body.append(f'<w:p>{"<w:pPr>" + ppr + "</w:pPr>" if ppr else ""}{rx}</w:p>')
p('The Mills Global: Service and Industry Copy', 'Title')
p('Each service has two layers of copy. The slider description is scope-focused and appears in the Home services slider. The hero copy is benefit-focused and appears at the top of the service page, with the same line in the page\'s contact block, the hover previews and the follow-up emails.')
p('Industries have hero copy only (benefit-focused).')
p('Services', 'Heading1')
for f, name in services:
    p(name, 'Heading2')
    p(num=True, runs=[('Slider (scope-focused): ', True), (slides.get(name, '(not in slider)'), False)])
    p(num=True, runs=[('Hero (benefit-focused): ', True), (hero(f), False)])
p('Industries', 'Heading1')
for f, name in industries:
    p(name, 'Heading2')
    p(num=True, runs=[('Hero (benefit-focused): ', True), (hero(f), False)])
W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
doc = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W}><w:body>{"".join(body)}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1200" w:right="1300" w:bottom="1200" w:left="1300" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>'
styles = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {W}>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:sz w:val="22"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="200"/></w:pPr><w:rPr><w:b/><w:color w:val="212431"/><w:sz w:val="44"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="360" w:after="120"/></w:pPr><w:rPr><w:b/><w:color w:val="EA5C1F"/><w:sz w:val="34"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="60"/></w:pPr><w:rPr><w:b/><w:color w:val="212431"/><w:sz w:val="28"/></w:rPr></w:style>
</w:styles>'''
numbering = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering {W}>
<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="&#8226;"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="540" w:hanging="270"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/></w:rPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>'''
ct = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/></Types>'
rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
drels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/></Relationships>'
os.makedirs('docs', exist_ok=True)
out = 'docs/SERVICE-INDUSTRY-COPY.docx'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', ct); z.writestr('_rels/.rels', rels)
    z.writestr('word/document.xml', doc); z.writestr('word/styles.xml', styles); z.writestr('word/numbering.xml', numbering); z.writestr('word/_rels/document.xml.rels', drels)
print('wrote', out, len(services), 'services,', len(industries), 'industries')
