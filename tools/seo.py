import glob, re, json, html
BASE='https://zervosepipla.gr/'
BRAND='ΖΕΡΒΟΣ Έπιπλα'
PHONE='+30 2241095275'; EMAIL='zervosinhouse@gmail.com'
IG='https://www.instagram.com/epiplozervos_/'; FB='https://www.facebook.com/share/1FdBfADpEP/'
CATS={
 'salonia':('Σαλόνια','Σαλόνια & καναπέδες','Sofas & living room furniture'),
 'trapezakia-saloniou':('Τραπεζάκια σαλονιού','Τραπεζάκια σαλονιού','Coffee tables'),
 'krevatokamares':('Κρεβατοκάμαρες','Κρεβατοκάμαρες','Bedroom furniture'),
 'trapezaries':('Τραπεζαρίες','Τραπεζαρίες, μπουφέδες & καρέκλες','Dining tables, sideboards & chairs'),
 'syntheseis':('Συνθέσεις τοίχου','Συνθέσεις τοίχου & έπιπλα TV','Wall units & TV units'),
 'paidika':('Παιδικά','Παιδικά δωμάτια','Kids bedroom furniture'),
 'diakosmisi':('Διακόσμηση','Διακόσμηση & καθρέπτες','Decor & mirrors'),
}
TYPES={'Έπιπλο TV':'TV unit','Καθρέπτης':'Mirror','Καρέκλα':'Dining chair','Κουκέτα':'Bunk bed','Κρεβάτι':'Bed',
 'Κρεβατοκάμαρα':'Bedroom set','Μπουφές':'Sideboard','Παιδικό δωμάτιο':'Kids bedroom','Πολυθρονάκι':'Armchair',
 'Ροτόντα':'Kids furniture','Σαλόνι':'Sofa','Σύνθεση τοίχου':'Wall unit','Τραπέζι Σαλονιού':'Coffee table','Τραπεζαρία':'Dining table'}
CAT_KW={
 'salonia':'σαλόνια Ρόδος, καναπέδες Ρόδος, γωνιακοί καναπέδες, καναπές κρεβάτι, πολυθρόνες, σαλόνι με μηχανισμό, salonia rodos, kanapedes rodos, sofas Rhodes, corner sofa Rhodes, sofa bed Rhodes, living room furniture Rhodes, armchairs Rhodes',
 'trapezakia-saloniou':'τραπεζάκια σαλονιού Ρόδος, τραπεζάκι σαλονιού, τραπεζάκια μέσης, βοηθητικά τραπεζάκια, τραπεζάκι με αποθηκευτικό χώρο, trapezakia saloniou, coffee tables Rhodes, coffee table, side tables Rhodes, living room tables',
 'krevatokamares':'κρεβατοκάμαρες Ρόδος, κρεβάτια Ρόδος, υφασμάτινα κρεβάτια, διπλά κρεβάτια, κομοδίνα, κρεβάτι με αποθηκευτικό χώρο, κρεβάτι με φωτισμό LED, krevatokamares rodos, bedroom furniture Rhodes, beds Rhodes, double bed, upholstered bed, bedside tables',
 'trapezaries':'τραπεζαρίες Ρόδος, τραπέζια τραπεζαρίας, επεκτεινόμενο τραπέζι, μπουφέδες Ρόδος, καρέκλες τραπεζαρίας, καρέκλες Ρόδος, trapezaries rodos, dining tables Rhodes, extendable dining table, sideboards Rhodes, dining chairs Rhodes',
 'syntheseis':'συνθέσεις τοίχου Ρόδος, σύνθεση σαλονιού, έπιπλο τηλεόρασης, έπιπλα TV, βιτρίνες, κρεμαστά έπιπλα, syntheseis toixou, wall units Rhodes, TV units Rhodes, TV stand, entertainment unit, display cabinet',
 'paidika':'παιδικά δωμάτια Ρόδος, παιδικά έπιπλα, εφηβικά δωμάτια, κουκέτες, παιδικά κρεβάτια, παιδικά γραφεία, paidika domatia rodos, kids bedroom furniture Rhodes, kids beds, bunk beds Rhodes, teen bedroom',
 'diakosmisi':'καθρέπτες Ρόδος, καθρέπτες με φωτισμό LED, καθρέπτης τοίχου, ρολόι τοίχου καθρέπτης, διακόσμηση σπιτιού Ρόδος, kathreptes rodos, mirrors Rhodes, LED mirror, wall mirror, home decor Rhodes',
}
KW_COMMON='έπιπλα Ρόδος, έπιπλα Ρόδου, κατάστημα επίπλων Ρόδος, έπιπλα Κρεμαστή, έπιπλα Ιαλυσός, έπιπλα Δωδεκάνησα, έπιπλα κατά παραγγελία, ΖΕΡΒΟΣ Έπιπλα, Έπιπλα Ζερβός, epipla rodos, epipla zervos, furniture Rhodes, furniture store Rhodes, furniture shop Rhodes Greece, custom furniture Rhodes, Zervos furniture, Kremasti Rhodes' #έπιπλα Ρόδος, κατάστημα επίπλων Ρόδος, έπιπλα Κρεμαστή, ΖΕΡΒΟΣ έπιπλα, Zervos, furniture Rhodes, furniture store Rhodes, Kremasti'

def text(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',s))).strip()
def clip(s,n):
  if len(s)<=n: return s
  s=s[:n].rsplit(' ',1)[0].rstrip(',;:–-'); return s+'…'
def esc(s): return html.escape(s,quote=True)
def absimg(src): return BASE+src.split('?')[0]
def ld(obj): return '  <script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False)+'</script>\n'
def url(slug): return BASE if slug=='index' else BASE+slug
STORE_ID=BASE+'#store'

def head_block(title,desc,canon,img,kw,ogtype,extra_ld):
  b='  <!-- SEO -->\n'
  b+=f'  <title>{esc(title)}</title>\n'
  b+=f'  <meta name="description" content="{esc(desc)}">\n'
  b+=f'  <meta name="keywords" content="{esc(kw)}">\n'
  b+='  <meta name="robots" content="index, follow, max-image-preview:large">\n'
  b+=f'  <link rel="canonical" href="{canon}">\n'
  b+='  <meta name="geo.region" content="GR-L">\n  <meta name="geo.placename" content="Κρεμαστή, Ρόδος">\n'
  b+=f'  <meta property="og:type" content="{ogtype}">\n  <meta property="og:site_name" content="{BRAND}">\n'
  b+=f'  <meta property="og:title" content="{esc(title)}">\n  <meta property="og:description" content="{esc(desc)}">\n'
  b+=f'  <meta property="og:url" content="{canon}">\n  <meta property="og:image" content="{img}">\n'
  b+='  <meta property="og:locale" content="el_GR">\n  <meta property="og:locale:alternate" content="en_GB">\n'
  b+='  <meta name="twitter:card" content="summary_large_image">\n'
  b+=f'  <meta name="twitter:title" content="{esc(title)}">\n  <meta name="twitter:description" content="{esc(desc)}">\n  <meta name="twitter:image" content="{img}">\n'
  for o in extra_ld: b+=ld(o)
  b+='  <!-- /SEO -->\n'
  return b

def crumbs(items):
  return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
    {'@type':'ListItem','position':i+1,'name':n,'item':u} for i,(n,u) in enumerate(items)]}

def apply(f,block):
  s=open(f).read()
  s=re.sub(r'  <!-- SEO -->.*?<!-- /SEO -->\n','',s,flags=re.S)
  s=re.sub(r'  <title>.*?</title>\n','',s,flags=re.S)
  s=re.sub(r'  <meta name="description"[^>]*>\n','',s)
  s=re.sub(r'  <meta property="og:image"[^>]*>\n','',s)
  a='  <link rel="apple-touch-icon"'
  i=s.index(a); j=s.index('\n',i)+1
  s=s[:j]+block+s[j:]
  open(f,'w').write(s)

# products
prod_cat={}
for f in sorted(glob.glob('*.html')):
  slug=f[:-5]
  if slug=='index' or slug in CATS: continue
  s=open(f).read()
  cat=re.search(r'<a href="([a-z-]+)\.html[^"]*" class="crumb">',s).group(1)
  ptype=text(re.search(r'<p class="product-cat">(.*?)</p>',s).group(1))
  h1=text(re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S).group(1)).replace(' - ',' ')
  m=re.search(r'<p class="lead-dark">(.*?)</p>',s,re.S)
  lead=text(m.group(1)) if m else f'{h1}: {ptype.lower()} από τη συλλογή «{CATS[cat][1]}». Ρωτήστε μας για διαστάσεις, υφάσματα και χρώματα.'
  imgs=[absimg(m) for m in re.findall(r'<div class="carousel-slide"[^>]*><img src="([^"]+)"',s)]
  en=TYPES[ptype]; gr_cat,_,en_cat=CATS[cat]
  title=f'{h1} | {en} Rhodes | {BRAND}'
  desc=clip(lead,150)+f' {BRAND}, Κρεμαστή Ρόδου. {en} – Zervos Furniture, Rhodes.'
  name_only=h1.split()[-1]
  kw=f'{h1}, {name_only}, {ptype.lower()} {name_only}, {ptype.lower()} Ρόδος, {en.lower()} {name_only}, {en.lower()} Rhodes, '+', '.join(CAT_KW[cat].split(', ')[:8])+', '+KW_COMMON
  prod={'@context':'https://schema.org','@type':'Product','name':h1,'description':lead,'image':imgs,
        'url':url(slug),'category':f'{ptype} / {en}'}
  bc=crumbs([('Αρχική',BASE),(gr_cat,url(cat)),(h1,url(slug))])
  apply(f,head_block(title,desc,url(slug),imgs[0],kw,'product',[prod,bc]))
  prod_cat[slug]=cat

# categories
for cat,(gr,gr_long,en) in CATS.items():
  f=cat+'.html'; s=open(f).read()
  lead=text(re.search(r'<p class="lead">(.*?)</p>',s,re.S).group(1))
  links=[]
  for m in re.findall(r'<a href="([a-z0-9-]+)\.html" class="product-img"><img src="([^"]+)"',s):
    if m[0] not in links: links.append(m[0])
  first=re.search(r'class="product-img"><img src="([^"]+)"',s).group(1)
  title=f'{gr_long} στη Ρόδο | {en} Rhodes | {BRAND}'
  desc=clip(lead,140)+f' {BRAND}, Κρεμαστή Ρόδου. {en} in Rhodes.'
  kw=CAT_KW[cat]+', '+KW_COMMON
  coll={'@context':'https://schema.org','@type':'CollectionPage','name':f'{gr_long} – {BRAND}','description':lead,
        'url':url(cat),'inLanguage':'el','isPartOf':{'@id':BASE+'#website'},
        'mainEntity':{'@type':'ItemList','numberOfItems':len(links),'itemListElement':[
          {'@type':'ListItem','position':i+1,'url':url(l)} for i,l in enumerate(links)]}}
  bc=crumbs([('Αρχική',BASE),(gr_long,url(cat))])
  apply(f,head_block(title,desc,url(cat),absimg(first),kw,'website',[coll,bc]))

# home
hours=[{'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday','Friday'],'opens':o,'closes':c} for o,c in [('09:30','13:00'),('17:00','20:30')]]
hours.append({'@type':'OpeningHoursSpecification','dayOfWeek':'Saturday','opens':'09:30','closes':'13:00'})
store={'@context':'https://schema.org','@type':'FurnitureStore','@id':STORE_ID,'name':BRAND,
  'alternateName':['Έπιπλα Ζερβός','Epipla Zervos','Zervos Furniture','ΕΠΙΠΛΑ ΖΕΡΒΟΣ'],
  'description':'Κατάστημα επίπλων στην Κρεμαστή Ρόδου από το 1966: σαλόνια, κρεβατοκάμαρες, τραπεζαρίες, συνθέσεις τοίχου, παιδικά δωμάτια και διακόσμηση. Furniture store in Kremasti, Rhodes since 1966. We speak English.',
  'url':BASE,'logo':BASE+'images/logo.png','image':[BASE+'video/showroom-poster.jpg',BASE+'images/logo.png'],
  'telephone':PHONE,'email':EMAIL,'foundingDate':'1966',
  'address':{'@type':'PostalAddress','streetAddress':'Λεωφόρος Ελευθερίας','addressLocality':'Κρεμαστή','addressRegion':'Ρόδος','addressCountry':'GR'},
  'areaServed':[{'@type':'Place','name':'Ρόδος'},{'@type':'Place','name':'Rhodes'},{'@type':'Place','name':'Δωδεκάνησα'}],
  'knowsLanguage':['el','en'],
  'openingHoursSpecification':hours,'sameAs':[IG,FB],
  'hasMap':'https://www.google.com/maps/search/?api=1&query=%CE%95%CE%A0%CE%99%CE%A0%CE%9B%CE%91+%CE%96%CE%95%CE%A1%CE%92%CE%9F%CE%A3%2C+Leoforos+Eleftherias%2C+Kremasti',
  'hasOfferCatalog':{'@type':'OfferCatalog','name':'Έπιπλα / Furniture','itemListElement':[
     {'@type':'OfferCatalog','name':f'{v[1]} / {v[2]}','url':url(k)} for k,v in CATS.items()]}}
site={'@context':'https://schema.org','@type':'WebSite','@id':BASE+'#website','url':BASE,'name':BRAND,
  'alternateName':'Zervos Furniture Rhodes','inLanguage':'el','publisher':{'@id':STORE_ID}}
title=f'{BRAND} Ρόδος | Κατάστημα επίπλων Κρεμαστή | Furniture store Rhodes'
desc='ΖΕΡΒΟΣ Έπιπλα από το 1966 στην Κρεμαστή Ρόδου: σαλόνια, κρεβατοκάμαρες, τραπεζαρίες, συνθέσεις τοίχου, παιδικά και διακόσμηση. Furniture store in Rhodes since 1966. We speak English.'
kw=KW_COMMON+', σαλόνια Ρόδος, καναπέδες Ρόδος, κρεβατοκάμαρες Ρόδος, τραπεζαρίες Ρόδος, τραπεζάκια σαλονιού, συνθέσεις τοίχου, παιδικά δωμάτια, καθρέπτες, furniture near Rhodes airport, English speaking furniture store Rhodes, sofas Rhodes, bedroom furniture Rhodes, dining tables Rhodes, wall units Rhodes, kids furniture Rhodes'
_old='έπιπλα Ρόδος, κατάστημα επίπλων Ρόδος, έπιπλα Κρεμαστή, σαλόνια Ρόδος, καναπέδες Ρόδος, κρεβατοκάμαρες Ρόδος, τραπεζαρίες Ρόδος, συνθέσεις τοίχου, παιδικά δωμάτια, ΖΕΡΒΟΣ έπιπλα, Zervos furniture, furniture store Rhodes, furniture Rhodes Greece, sofas Rhodes, bedroom furniture Rhodes, Kremasti'
apply('index.html',head_block(title,desc,BASE,BASE+'images/og-logo.jpg',kw,'website',[store,site]))
print('ok',len(prod_cat))
