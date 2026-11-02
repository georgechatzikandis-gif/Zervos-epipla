import glob, re, json, html, os, urllib.parse, sys
SP=os.path.dirname(os.path.abspath(__file__))
T=json.load(open(os.path.join(SP,'translations.json')))
BASE='https://zervosepipla.gr/'
BRAND='ΖΕΡΒΟΣ Έπιπλα'; BRAND_EN='Zervos Furniture'
CATS_EN={'salonia':('Sofas','Sofas & living room furniture'),'trapezakia-saloniou':('Coffee tables','Coffee tables & side tables'),
 'krevatokamares':('Bedrooms','Bedroom furniture & beds'),'trapezaries':('Dining','Dining tables, sideboards & chairs'),
 'syntheseis':('Wall units','Wall units & TV units'),'paidika':('Kids','Kids\' & teen bedrooms'),'diakosmisi':('Decor','Decor & mirrors')}
TYPES={'Έπιπλο TV':'TV unit','Καθρέπτης':'Mirror','Καρέκλα':'Dining chair','Κουκέτα':'Bunk bed','Κρεβάτι':'Bed',
 'Κρεβατοκάμαρα':'Bedroom set','Μπουφές':'Sideboard','Παιδικό δωμάτιο':'Kids bedroom','Πολυθρονάκι':'Armchair',
 'Ροτόντα':'Round dining table','Σαλόνι':'Sofa','Σύνθεση τοίχου':'Wall unit','Τραπέζι Σαλονιού':'Coffee table','Τραπεζαρία':'Dining table'}
KW_EN='furniture Rhodes, furniture store Rhodes, furniture shop Rhodes Greece, Rhodes furniture, custom furniture Rhodes, Zervos furniture, Kremasti Rhodes, furniture near Rhodes airport, home furniture Rhodes, epipla rodos'
CAT_KW_EN={'salonia':'sofas Rhodes, corner sofa Rhodes, sofa bed Rhodes, living room furniture Rhodes, armchairs Rhodes',
 'trapezakia-saloniou':'coffee tables Rhodes, coffee table, side tables Rhodes, nesting tables, coffee table with storage',
 'krevatokamares':'bedroom furniture Rhodes, beds Rhodes, double bed, upholstered bed, bed with storage, LED bed, bedside tables',
 'trapezaries':'dining tables Rhodes, extendable dining table, round dining table, sideboards Rhodes, dining chairs Rhodes',
 'syntheseis':'wall units Rhodes, TV units Rhodes, TV stand, entertainment unit, media wall, display cabinet',
 'paidika':'kids bedroom furniture Rhodes, kids beds, bunk beds Rhodes, teen bedroom, children\'s furniture',
 'diakosmisi':'mirrors Rhodes, LED mirror, wall mirror, mirror clock, home decor Rhodes'}
GREEK=re.compile(r'[Ͱ-Ͽἀ-῿]')
def esc(s): return html.escape(s,quote=True)
def text(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',s))).strip()
def clip(s,n):
  if len(s)<=n: return s
  return s[:n].rsplit(' ',1)[0].rstrip(',;:–-')+'…'
def tr(s):
  k=s.strip()
  return T.get(k)
def url_gr(slug): return BASE if slug=='index' else BASE+slug
def url_en(slug): return BASE+'en/' if slug=='index' else BASE+'en/'+slug
def ld(o): return '  <script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>\n'

def translate_body(src):
  out=[]; skip=False
  for part in re.split(r'(<[^>]+>)',src):
    if part.startswith('<'):
      tag=part.lower()
      if tag.startswith('<script') or tag.startswith('<style'): skip=True
      elif tag.startswith('</script') or tag.startswith('</style'): skip=False
      def attr(m):
        v=html.unescape(m.group(2)); t=T.get(v)
        return m.group(1)+'="'+(esc(t) if t is not None else m.group(2))+'"'
      part=re.sub(r'\b(alt|aria-label|placeholder|title)="([^"]*)"',attr,part)
      out.append(part)
    else:
      if skip or not GREEK.search(part): out.append(part); continue
      # translate whole node, or entity-split pieces
      pieces=re.split(r'(&[a-z#0-9]+;)',part); res=[]
      for p in pieces:
        if p.startswith('&') or not GREEK.search(p): res.append(p); continue
        k=p.strip(); t=T.get(k)
        if t is None:
          t=T.get(html.unescape(k))
        if t is None: print('UNTRANSLATED',repr(k[:60]),file=sys.stderr); res.append(p); continue
        lead=p[:len(p)-len(p.lstrip())]; trail=p[len(p.rstrip()):]
        res.append(lead+esc(t).replace('&#x27;',"'")+trail)
      out.append(''.join(res))
  return ''.join(out)

def fix_links(s,cur):
  def rep(m):
    h=m.group(1)
    if h.startswith('#'): return f'href="en/{cur}.html{h}"'
    if re.match(r'(https?:|tel:|mailto:|en/)',h) or not re.match(r'[a-z0-9-]+\.html',h): return m.group(0)
    if 'product=' in h:
      def prod(mm):
        v=urllib.parse.unquote(mm.group(1)); t=T.get(v,v)
        return 'product='+urllib.parse.quote(t)
      h=re.sub(r'product=([^#&"]+)',prod,h)
    return f'href="en/{h}"'
  return re.sub(r'href="([^"]*)"',rep,s)

LANG_CSS_DONE=True
def lang_links(cur, to_en):
  if to_en:
    target=f'en/{cur}.html'; label='EN'; hl='en'; title='English'
  else:
    target=f'{cur}.html'; label='ΕΛ'; hl='el'; title='Ελληνικά'
  return (f'<a href="{target}" class="lang-switch" hreflang="{hl}" lang="{hl}" title="{title}">{label}</a>',
          f'<a href="{target}" class="lang-switch lang-mobile" hreflang="{hl}" lang="{hl}" title="{title}">{label}</a>')

def add_switch(s,cur,to_en):
  s=re.sub(r'\s*<a [^>]*class="lang-switch[^"]*"[^>]*>[^<]*</a>','',s)
  d,m=lang_links(cur,to_en)
  s=re.sub(r'(\n\s*)(<a href="[^"]*#offer" class="btn btn-dark btn-sm">)',r'\1'+d+r'\1\2',s,count=1)
  s=s.replace('<button class="nav-toggle"',m+'\n      <button class="nav-toggle"',1)
  return s

def hreflang(slug):
  return ('  <!-- HREFLANG -->\n'
    f'  <link rel="alternate" hreflang="el" href="{url_gr(slug)}">\n'
    f'  <link rel="alternate" hreflang="en" href="{url_en(slug)}">\n'
    f'  <link rel="alternate" hreflang="x-default" href="{url_gr(slug)}">\n'
    '  <!-- /HREFLANG -->\n')

def put_hreflang(s,slug):
  s=re.sub(r'  <!-- HREFLANG -->.*?<!-- /HREFLANG -->\n','',s,flags=re.S)
  return s.replace('  <!-- /SEO -->\n','  <!-- /SEO -->\n'+hreflang(slug),1)

def seo_en(title,desc,canon,img,kw,ogtype,lds):
  b='  <!-- SEO -->\n'
  b+=f'  <title>{esc(title)}</title>\n  <meta name="description" content="{esc(desc)}">\n  <meta name="keywords" content="{esc(kw)}">\n'
  b+='  <meta name="robots" content="index, follow, max-image-preview:large">\n'
  b+=f'  <link rel="canonical" href="{canon}">\n'
  b+='  <meta name="geo.region" content="GR-L">\n  <meta name="geo.placename" content="Kremasti, Rhodes">\n'
  b+=f'  <meta property="og:type" content="{ogtype}">\n  <meta property="og:site_name" content="{BRAND_EN}">\n'
  b+=f'  <meta property="og:title" content="{esc(title)}">\n  <meta property="og:description" content="{esc(desc)}">\n'
  b+=f'  <meta property="og:url" content="{canon}">\n  <meta property="og:image" content="{img}">\n'
  b+='  <meta property="og:locale" content="en_GB">\n  <meta property="og:locale:alternate" content="el_GR">\n'
  b+='  <meta name="twitter:card" content="summary_large_image">\n'
  b+=f'  <meta name="twitter:title" content="{esc(title)}">\n  <meta name="twitter:description" content="{esc(desc)}">\n  <meta name="twitter:image" content="{img}">\n'
  for o in lds: b+=ld(o)
  return b+'  <!-- /SEO -->\n'

def crumbs(items):
  return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
    {'@type':'ListItem','position':i+1,'name':n,'item':u} for i,(n,u) in enumerate(items)]}

os.makedirs('en',exist_ok=True)
files=sorted(glob.glob('*.html'))
for f in files:
  slug=f[:-5]
  gr=open(f).read()
  # Greek page: switch + hreflang
  gr2=put_hreflang(add_switch(gr,slug,True),slug)
  if gr2!=gr: open(f,'w').write(gr2)
  s=gr2
  head_end=s.index('</head>'); head=s[:head_end]; body=s[head_end:]
  # ---- body
  body=translate_body(body)
  body=fix_links(body,slug)
  body=add_switch(body,slug,False)
  if slug=='index':
    body=re.sub(r'\s*<div lang="el">.*?</div>\n(?=\s*<div lang="en">)','\n',body,flags=re.S)
    body=body.replace('<div class="seo-cols">','<div class="seo-cols seo-single">',1)
  # ---- head
  head=head.replace('<html lang="el">','<html lang="en">')
  head=re.sub(r'  <meta name="google-site-verification"[^>]*>\n','',head)
  head=re.sub(r'  <!-- HREFLANG -->.*?<!-- /HREFLANG -->\n','',head,flags=re.S)
  head=head.replace('  <meta charset="utf-8">\n','  <meta charset="utf-8">\n  <base href="../">\n',1)
  # data for seo
  if slug=='index':
    title='Zervos Furniture Rhodes | Furniture store in Kremasti since 1966 | ΖΕΡΒΟΣ Έπιπλα'
    desc='Zervos Furniture (ΖΕΡΒΟΣ Έπιπλα), a family furniture store in Kremasti, Rhodes since 1966: sofas, bedrooms, dining tables, wall units, kids\' rooms and decor. Made-to-order furniture, we speak English.'
    kw=KW_EN+', sofas Rhodes, bedroom furniture Rhodes, dining tables Rhodes, coffee tables Rhodes, wall units Rhodes, kids furniture Rhodes, LED mirrors, English speaking furniture store Rhodes'
    m=re.search(r'<script type="application/ld\+json">(\{[^<]*"FurnitureStore".*?)</script>',head,re.S)
    store=json.loads(m.group(1))
    store['description']='Family furniture store in Kremasti, Rhodes since 1966: sofas, bedrooms, dining tables, wall units, kids\' rooms and decor. We speak English.'
    store['address']={'@type':'PostalAddress','streetAddress':'Leoforos Eleftherias','addressLocality':'Kremasti','addressRegion':'Rhodes','addressCountry':'GR'}
    store['hasOfferCatalog']={'@type':'OfferCatalog','name':'Furniture','itemListElement':[{'@type':'OfferCatalog','name':v[1],'url':url_en(k)} for k,v in CATS_EN.items()]}
    store['knowsLanguage']=['el','en']
    site={'@context':'https://schema.org','@type':'WebSite','@id':BASE+'en/#website','url':BASE+'en/','name':BRAND_EN,'inLanguage':'en','publisher':{'@id':BASE+'#store'}}
    block=seo_en(title,desc,url_en(slug),BASE+'images/og-logo.jpg',kw,'website',[store,site])
  elif slug in CATS_EN:
    short,long_=CATS_EN[slug]
    lead=text(re.search(r'<p class="lead">(.*?)</p>',body,re.S).group(1))
    links=[]
    for l in re.findall(r'<a href="en/([a-z0-9-]+)\.html" class="product-img">',body):
      if l not in links: links.append(l)
    first=re.search(r'class="product-img"><img src="([^"]+)"',body).group(1).split('?')[0]
    title=f'{long_} in Rhodes | {BRAND_EN} | ΖΕΡΒΟΣ Έπιπλα'
    desc=clip(lead,150)+f' {BRAND_EN}, Kremasti, Rhodes.'
    coll={'@context':'https://schema.org','@type':'CollectionPage','name':f'{long_} – {BRAND_EN}','description':lead,'url':url_en(slug),'inLanguage':'en',
      'isPartOf':{'@id':BASE+'en/#website'},'mainEntity':{'@type':'ItemList','numberOfItems':len(links),'itemListElement':[{'@type':'ListItem','position':i+1,'url':url_en(l)} for i,l in enumerate(links)]}}
    block=seo_en(title,desc,url_en(slug),BASE+first,CAT_KW_EN[slug]+', '+KW_EN,'website',[coll,crumbs([('Home',BASE+'en/'),(long_,url_en(slug))])])
  else:
    cat=re.search(r'<a href="en/([a-z-]+)\.html[^"]*" class="crumb">',body).group(1)
    ptype_gr=text(re.search(r'<p class="product-cat">(.*?)</p>',gr,re.S).group(1))
    en_type=TYPES[ptype_gr]
    h1=text(re.search(r'<h1[^>]*>(.*?)</h1>',body,re.S).group(1)).replace(' - ',' ')
    m=re.search(r'<p class="lead-dark">(.*?)</p>',body,re.S)
    lead=text(m.group(1)) if m else f'{h1}: {en_type.lower()} from our {CATS_EN[cat][1].lower()} collection. Ask us about sizes, fabrics and colours.'
    imgs=[BASE+x.split('?')[0] for x in re.findall(r'<div class="carousel-slide"[^>]*><img src="([^"]+)"',body)]
    name=h1.split()[-1] if h1 else h1
    title=f'{h1} | {en_type} Rhodes | {BRAND_EN}'
    desc=clip(lead,150)+f' {BRAND_EN}, Kremasti, Rhodes.'
    kw=f'{h1}, {name}, {en_type.lower()} {name}, {en_type.lower()} Rhodes, '+CAT_KW_EN[cat]+', '+KW_EN
    prod={'@context':'https://schema.org','@type':'Product','name':h1,'description':lead,'image':imgs,'url':url_en(slug),'category':en_type}
    block=seo_en(title,desc,url_en(slug),imgs[0],kw,'product',[prod,crumbs([('Home',BASE+'en/'),(CATS_EN[cat][1],url_en(cat)),(h1,url_en(slug))])])
  head=re.sub(r'  <!-- SEO -->.*?<!-- /SEO -->\n',lambda m: block+hreflang(slug),head,flags=re.S)
  open('en/'+f,'w').write(head+body)
print('built',len(files))
