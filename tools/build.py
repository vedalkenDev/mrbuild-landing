import json, sys, urllib.parse
OUT = sys.argv[1]
BASE = "https://vedalkendev.github.io/mrbuild-landing/"
STORE = "https://mrbuild-online.co.za"
FB = "https://www.facebook.com/people/Mr-Build/61551736583171/"
LEAFLET = "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/"

# slug, name, kind, district, street, town, postcode, tel, email, lat, lng
BRANCHES = [
  ("tzaneen","Tzaneen","mb","mopani","Cnr Danie Joubert & Claude Wheatley St","Tzaneen","0850","015 004 0560","tzaneen@mrbuild.co.za",-23.8357,30.1516),
  ("louis-trichardt","Louis Trichardt","mb","vhembe","6 Cnr Rissik & Grobler St","Louis Trichardt","0920","015 004 0168","louistrichardt@mrbuild.co.za",-23.0481,29.9046),
  ("musina","Musina","mb","vhembe","6 Pat Harrison Rd","Musina","0900","015 004 1031","musina@mrbuild.co.za",-22.3393,30.0424),
  ("giyani","Giyani","mb","mopani","92 B.A","Giyani","0826","015 812 3786","giyani@mrbuild.co.za",-23.3144,30.7168),
  ("sibasa","Sibasa","mb","vhembe","204 Makhado Rd","Sibasa","0970","015 963 3856","sibasa@mrbuild.co.za",-22.9308,30.4632),
  ("thohoyandou","Thohoyandou","mb","vhembe","90/91 B.A","Thohoyandou","0950","015 962 0444","thohoyandou@mrbuild.co.za",-22.9504,30.4785),
  ("mankweng","Mankweng","mb","capricorn","RE/22/1005, R71","Mankweng","0727","015 004 2297","",-23.8790,29.7210),
  ("the-builder-thohoyandou","Thohoyandou","tb","vhembe","70 Mphephu St","Thohoyandou","0950","015 962 5545","thohoyandou@thebuilder.co.za",-22.9872,30.4677),
  ("the-builder-giyani","Giyani","tb","mopani","32 B.A","Giyani","0826","015 004 0561","giyani@thebuilder.co.za",-23.313,30.7133),
]
def e164(t): return "+27" + t.replace(" ","")[1:]
def esc(s): return s.replace("&","&amp;")
def full(b): return ("Mr Build " if b[2]=="mb" else "The Builder ") + b[1]
def maps(b): return f"https://www.google.com/maps/dir/?api=1&destination={b[9]},{b[10]}"

HOURS_LD = [
  {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"07:30","closes":"13:30"},
  {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"14:00","closes":"16:30"},
  {"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"07:30","closes":"12:30"},
]
ORG = {"@type":"Organization","@id":BASE+"#org","name":"Mr Build","alternateName":"Your Building Buddy","url":BASE,
       "logo":BASE+"img/logo-red.svg","email":"info@mrbuild.co.za","telephone":"+27150040560",
       "sameAs":[STORE,"https://www.instagram.com/mrbuild_sa/",FB]}

# Departments, in the order of the pylon sign outside the stores
DEPTS = [
  ("building","Building material","Cement, bricks, roofing.",f"{STORE}/?product_cat=building-supplies","292 items",""),
  ("plumbing","Plumbing","Pipes, taps, geysers, JoJo tanks.",f"{STORE}/?product_cat=plumbing","1,235 items",""),
  ("electrical","Electrical","Cable, breakers, lights, solar.",f"{STORE}/?product_cat=electrical-supplies","819 items",""),
  ("cutting","Cutting &amp; edging","Boards cut and edged to your list.","services.html#cutting","In store","y"),
  ("doors","Wrap doors","Doors wrapped to order.","services.html#doors","In store","y"),
  ("paint","Paint","Inside, outside, roof.",f"{STORE}/?product_cat=paint-supplies","962 items",""),
  ("diy","DIY","Melamine, Supawood, hinges.",f"{STORE}/?product_cat=wood-board-suplies","Board","k"),
  ("tools","Tools","Hand and power tools.",f"{STORE}/?product_cat=domestic-hardware","Hardware","k"),
]
BRANDS = [("bosch","Bosch"),("makita","Makita"),("dulux","Dulux"),("jojo","JoJo"),("tork_craft","Tork Craft"),("pg_bison","PG Bison"),
  ("nutec","Nutec"),("lasher","Lasher"),("harvey","Harvey Roofing"),("eureka","Eureka"),("bostik","Bostik"),("glue_devil","Glue Devil"),
  ("fortknox","Fort Knox"),("hamiltons","Hamilton's"),("academy","Academy Brushware"),("cornice_maker","Cornice Maker"),("sunridge","Sunridge"),
  ("waco","Waco"),("xpanda","Xpanda"),("matus","Matus"),("ruwag","Ruwag"),("pbes","PBES"),("national_edging","National Edging")]

def ic(name, cls="ic"):
    u = f"img/icons/{name}.svg"
    return f'<span class="{cls}" style="-webkit-mask-image:url({u});mask-image:url({u})" aria-hidden="true"></span>'

def head(file, title, desc, ld, img="img/store-pylon.jpg", img_alt="A Mr Build store and its pylon sign", leaflet=False):
    url = BASE + ("" if file=="index.html" else file)
    lf = f'''<link rel="stylesheet" href="{LEAFLET}leaflet.min.css" crossorigin="anonymous" referrerpolicy="no-referrer">
<script src="{LEAFLET}leaflet.min.js" defer crossorigin="anonymous" referrerpolicy="no-referrer"></script>
''' if leaflet else ""
    return f'''<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#D9232A">
<link rel="canonical" href="{url}">
<link rel="icon" href="img/buddy.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_ZA">
<meta property="og:site_name" content="Mr Build">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}{img}">
<meta property="og:image:alt" content="{img_alt}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{json.dumps({"@context":"https://schema.org","@graph":ld}, indent=2, ensure_ascii=False)}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lilita+One&family=Barlow:wght@500;600;700&display=swap">
{lf}<link rel="stylesheet" href="css/site.css">
<script src="js/site.js" defer></script>
</head>
<body>
'''

NAV = [("index.html","Home"),("services.html","Services"),("branches.html","Branches"),("about.html","About"),("contact.html","Contact")]
def nav(active):
    cur = lambda f: ' aria-current="page"' if f==active else ''
    links = "\n".join(f'      <li><a href="{f}"{cur(f)}>{t}</a></li>' for f,t in NAV[1:])
    dl = "\n".join(f'    <a href="{f}"{cur(f)}>{t}</a>' for f,t in NAV)
    return f'''<div class="concept">Design concept for Mr Build. Not the official website.</div>
<header class="nav" id="top">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Mr Build home"><img src="img/logo-red.svg" alt="Mr Build" width="257" height="72"></a>
    <ul class="nav-links">
{links}
    </ul>
    <a class="btn btn-y btn-sm btn-shop" href="{STORE}" target="_blank" rel="noopener">Shop online</a>
    <button class="menu-btn" id="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><span></span><span></span><span></span></button>
  </div>
  <nav class="drawer" id="drawer" aria-label="Mobile">
{dl}
    <a class="shop" href="{STORE}" target="_blank" rel="noopener">Shop online →</a>
  </nav>
</header>
'''

def footer():
    return f'''<section class="cta sec bg-y dots-k slant" aria-labelledby="cta-h">
  <div class="wrap">
    <div class="row">
      <div>
        <h2 id="cta-h">Order online.<br><span class="r">Collect in store.</span></h2>
        <p>9,572 products. No delivery, collection only.</p>
        <div class="ctas"><a class="btn btn-r" href="{STORE}" target="_blank" rel="noopener">Shop now →</a><a class="btn" href="branches.html">Find a store</a></div>
      </div>
      <img src="img/buddy.svg" alt="" width="92" height="100" loading="lazy">
    </div>
  </div>
</section>
<footer class="foot sec slant-r">
  <div class="wrap">
    <div class="grid">
      <div><a href="index.html" aria-label="Mr Build home"><img class="flogo" src="img/logo-white.svg" alt="Mr Build, Your Building Buddy" width="284" height="78" loading="lazy"></a></div>
      <div><p class="label">Shop</p><ul><li><a href="{STORE}" target="_blank" rel="noopener">Online store</a></li><li><a href="services.html">Departments</a></li><li><a href="services.html#cutting">Cutting &amp; edging</a></li></ul></div>
      <div><p class="label">Visit</p><ul><li><a href="branches.html">Stores &amp; hours</a></li><li><a href="about.html">About Buddy</a></li><li><a href="contact.html">Contact</a></li></ul></div>
      <div><p class="label">Follow</p><ul><li><a href="https://www.instagram.com/mrbuild_sa/" target="_blank" rel="noopener">Instagram</a></li><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li><li><a href="mailto:info@mrbuild.co.za">info@mrbuild.co.za</a></li></ul></div>
    </div>
    <p class="legal">© 2026 Mr Build. Concept site. Store photos supplied by Mr Build. Map © OpenStreetMap contributors.</p>
  </div>
</footer>
</body>
</html>
'''

def post(inner, bubble=None, title_board=False):
    b = f'<p class="bubble b">{bubble}</p>' if bubble else ""
    return f'''<div class="post">
      <img class="frame" src="img/frame.svg" alt="" aria-hidden="true">
      <div class="board">{inner}</div>
      {b}
      <img class="buddy" src="img/buddy.svg" alt="Buddy, the Mr Build mascot" width="92" height="100">
    </div>'''

def phero(title_html, lede, side_extra=""):
    return f'''<section class="phero dots" aria-label="Page header">
  <div class="wrap">
    {post(f'<h1>{title_html}</h1>')}
    <div class="side"><p class="lede">{lede}</p>{side_extra}</div>
  </div>
</section>
'''

def pylon(with_text=False):
    out = []
    for i,(slug,name,txt,href,cnt,var) in enumerate(DEPTS):
        ext = '' if href.endswith(("#cutting","#doors")) else ' target="_blank" rel="noopener"'
        p = f"<p>{txt}</p>" if with_text else ""
        out.append(f'''      <li class="rv {var}"><a href="{href}"{ext}><span class="ph"><img src="img/dept/{slug}.jpg" alt="" loading="lazy" width="480" height="360"></span><span class="ibox">{ic(slug)}</span><h3>{name}</h3>{p}<span class="cnt">{cnt}</span></a></li>''')
    return '<ul class="pylon">\n' + "\n".join(out) + "\n    </ul>"

BADGE = {'academy':'#000','bosch':'#003B6A','dulux':'#09316E','hamiltons':'#98012E','tork_craft':'#D2242A','matus':'#070809','makita':'#EE2A40'}

def _stk(f, n, dup):
    alt = '' if dup else n
    ah = ' aria-hidden="true"' if dup else ''
    if f in BADGE:
        return f'<li{ah}><span class="stk badge" style="--bg:{BADGE[f]}"><img src="img/brands/{f}.png" alt="{alt}" loading="lazy"></span></li>'
    return f'<li{ah}><span class="stk"><img src="img/brands/{f}.png" alt="{alt}" loading="lazy"></span></li>'

def brands():
    rows = [BRANDS[0::2], BRANDS[1::2]]
    out = '<div class="ticker">'
    for i, row in enumerate(rows):
        items = "".join(_stk(f, n, False) for f, n in row) + "".join(_stk(f, n, True) for f, n in row)
        out += f'<div class="band{" k rev" if i else ""}"><ul class="track">{items}</ul></div>'
    return out + '</div>'

def mapblock(dark=False):
    items = []
    for b in BRANCHES:
        sub = "Collection point" if b[2]=="tb" else ("Head office" if b[0]=="tzaneen" else "Mr Build")
        items.append(f'''<li class="{b[2]}"><button type="button" data-store="{b[0]}" aria-pressed="false"><span class="pinmini"><img src="img/{'bob-pin.png' if b[2]=='tb' else 'buddy.svg'}" alt=""></span><span><strong>{"The Builder " if b[2]=="tb" else ""}{b[1]}</strong><small>{sub} · <a href="tel:{e164(b[7])}">{b[7]}</a></small></span></button></li>''')
    data = json.dumps([{"id":b[0],"n":full(b),"k":b[2],"a":esc(", ".join(x for x in [b[4],b[5]] if x)),"t":b[7],"e":e164(b[7]),"d":maps(b),"ll":[b[9],b[10]]} for b in BRANCHES], ensure_ascii=False)
    return f'''<div class="mapwrap">
      <div class="map" id="map" role="region" aria-label="Map of Mr Build stores"><p class="nojs">The map needs JavaScript. All stores are listed here.</p></div>
      <ul class="stores">
        {chr(10).join(items)}
      </ul>
    </div>
    <script type="application/json" id="store-data">{data}</script>'''

def write(name, html):
    open(f"{OUT}/{name}","w").write(html)

# ================= HOME =================
home_ld = [ORG, {"@type":"WebSite","name":"Mr Build","url":BASE,"publisher":{"@id":BASE+"#org"}}]
home = head("index.html","Mr Build | Your Building Buddy in Limpopo",
  "Building supplies, hardware, board cutting and door wrapping at Mr Build in Limpopo. Order online, collect at your nearest store.", home_ld, leaflet=True) \
 + nav("index.html") + f'''<main>
<section class="hero dots" aria-labelledby="h-h">
  <div class="sticker"><div class="burst"><div><span class="num" data-count="38">38</span><small>years</small></div></div></div>
  <div class="wrap">
    {post('<img src="img/logo-red.svg" alt="Mr Build" width="257" height="72"><span class="tag">Your <b>Building</b> Buddy</span>')}
    <div>
      <h2 id="h-h">Build it.<br><span class="r">Fix it.</span><br>Collect it.</h2>
      <p class="lede">Building supplies for Limpopo. Shop online, collect at your store.</p>
      <div class="ctas"><a class="btn btn-r" href="{STORE}" target="_blank" rel="noopener">Shop online →</a><a class="btn" href="#stores">Find a store</a></div>
    </div>
  </div>
</section>

<section class="stats sec slant-r" aria-label="Mr Build in numbers" style="padding-bottom:calc(var(--cut) + 36px)">
  <div class="wrap"><ul>
    <li><b class="num">38</b><span>Years in Limpopo</span></li>
    <li><b class="num">9,572</b><span>Products online</span></li>
    <li><b class="num">9</b><span>Stores to collect</span></li>
  </ul></div>
</section>

<section class="sec slant" id="depts" aria-labelledby="d-h" style="background:var(--white)">
  <div class="wrap">
    <div class="shead rv"><h2 class="beam" id="d-h">What we sell</h2><a class="more" href="services.html">All departments →</a></div>
    {pylon()}
  </div>
</section>

<section class="how sec bg-k slant-r" aria-labelledby="how-h">
  <div class="wrap">
    <div class="buddy-big rv"><p class="bubble">Order online. I'll have it ready.</p><img src="img/buddy.svg" alt="Buddy, the Mr Build mascot" width="92" height="100" loading="lazy"></div>
    <div>
      <h2 class="beam y rv" id="how-h" style="margin-bottom:44px">How it works</h2>
      <ol class="panels">
        <li class="rv">{ic("tools")}<h3>Shop online</h3><p>Pick your store at checkout.</p></li>
        <li class="rv">{ic("building")}<h3>We pack it</h3><p>You get a message when it's ready.</p></li>
        <li class="rv">{ic("diy")}<h3>Collect</h3><p>Bring your order number and ID.</p></li>
      </ol>
      <span class="nodel">No delivery. Collection only.</span>
    </div>
  </div>
</section>

<section class="counter sec bg-r dots slant" aria-labelledby="c-h">
  <div class="wrap">
    <div class="rv">
      <h2 class="big" id="c-h"><span>Cut.</span><span>Edge.</span><span>Wrap.</span></h2>
      <p class="lede">Bring your cutting list. We cut and edge boards and wrap doors in store.</p>
      <a class="btn btn-y" href="services.html#cutting">How it works →</a>
    </div>
    <figure class="polaroid rv"><img src="img/wood.jpg" alt="Stacked boards ready for cutting" loading="lazy" width="1200" height="900"><figcaption>Boards cut to size</figcaption></figure>
  </div>
</section>

<section class="sec slant-r" aria-labelledby="y-h" style="background:var(--white)">
  <div class="wrap">
    <div class="shead rv"><h2 class="beam k" id="y-h">Come see us</h2></div>
    <ul class="yards">
      <li class="rv"><img src="img/store-pylon.jpg" alt="A Mr Build store with its red pylon sign, from above" loading="lazy" width="1600" height="1066"></li>
      <li class="rv"><img src="img/store-front.jpg" alt="A Mr Build shopfront on a main road, from above" loading="lazy" width="1280" height="720"></li>
      <li class="rv"><img src="img/store-yard.jpg" alt="A Mr Build yard stacked with bricks and blocks, from above" loading="lazy" width="1280" height="720"></li>
    </ul>
  </div>
</section>

<section class="sec bg-y dots-k slant" id="stores" aria-labelledby="s-h">
  <div class="wrap">
    <div class="shead rv"><h2 class="beam" id="s-h">Find your store</h2><a class="more" href="branches.html">Hours &amp; numbers →</a></div>
    {mapblock()}
  </div>
</section>

<section class="sec slant-r" aria-labelledby="b-h" style="background:var(--white)">
  <div class="wrap">
    <div class="shead rv"><h2 class="beam y" id="b-h">Brands we stock</h2></div>
    {brands()}
  </div>
</section>
</main>
''' + footer()
write("index.html", home)

# ================= SERVICES =================
svc_ld = [ORG, {"@type":"WebPage","name":"Services | Mr Build","url":BASE+"services.html","isPartOf":{"@id":BASE+"#org"}},
  {"@type":"Service","name":"Board cutting and edging","provider":{"@id":BASE+"#org"},"areaServed":"Limpopo"},
  {"@type":"Service","name":"Door wrapping","provider":{"@id":BASE+"#org"},"areaServed":"Limpopo"}]
services = head("services.html","Departments and services | Mr Build Limpopo",
  "Building material, plumbing, electrical, paint, DIY and tools, plus board cutting, edging and door wrapping at Mr Build in Limpopo.", svc_ld) \
 + nav("services.html") + "<main>\n" + phero('What we <span class="k">sell</span>',
  'Eight departments.<br><span class="y">One counter.</span>', f'<a class="btn btn-y" href="{STORE}" target="_blank" rel="noopener">Shop online →</a>') \
 + f'''<section class="sec slant-r" aria-labelledby="d-h" style="background:var(--white)">
  <div class="wrap">
    <div class="shead rv"><h2 class="beam" id="d-h">Departments</h2></div>
    {pylon(True)}
  </div>
</section>

<section class="counter sec bg-k slant" id="cutting" aria-labelledby="c-h">
  <div class="wrap">
    <div class="rv">
      <h2 class="big" id="c-h"><span>Cut.</span><span>Edge.</span><span>Wrap.</span></h2>
      <p class="lede" style="margin-bottom:28px">Done at the counter while you wait, or ready later.</p>
      <ol class="steps3">
        <li><b>1</b>Bring your list</li>
        <li><b>2</b>We cut &amp; edge</li>
        <li><b>3</b>Collect</li>
      </ol>
    </div>
    <div class="rv" style="display:grid;gap:28px">
      <figure class="slip" aria-label="Example cutting list">
        <h3>Cutting list</h3>
        <ol class="num">
          <li><span>16 mm white melamine</span></li>
          <li><span class="q">4×</span><span>900 × 450, edge 1 side</span></li>
          <li><span class="q">2×</span><span>1800 × 450, edge 2 sides</span></li>
          <li><span class="q">8×</span><span>868 × 430 shelf</span></li>
        </ol>
      </figure>
      <div class="note" id="doors" style="color:var(--black)">
        <div style="display:flex;gap:14px;align-items:center"><span class="ibox" style="width:60px;height:60px;background:#fff;border:var(--ln);border-radius:12px;display:grid;place-items:center">{ic("doors")}</span><h3>Wrapped doors<br><small style="font:600 15px var(--body);text-transform:none">Pick door and colour at the counter.</small></h3></div>
      </div>
    </div>
  </div>
</section>

<section class="sec slant-r" aria-labelledby="b-h" style="background:var(--white)">
  <div class="wrap">
    <div class="shead rv"><h2 class="beam y" id="b-h">Brands we stock</h2></div>
    {brands()}
  </div>
</section>
</main>
''' + footer()
write("services.html", services)

# ================= BRANCHES =================
br_ld = [ORG]
for b in BRANCHES:
    slug,name,kind,dist,street,town,pc,tel,mail,lat,lng = b
    d = {"@type":"HardwareStore","@id":BASE+"branches.html#"+slug,"name":full(b),"url":BASE+"branches.html#"+slug,
         "telephone":e164(tel),"geo":{"@type":"GeoCoordinates","latitude":lat,"longitude":lng},
         "address":{"@type":"PostalAddress","addressLocality":town,"postalCode":pc,"addressRegion":"Limpopo","addressCountry":"ZA"},
         "openingHoursSpecification":HOURS_LD}
    if street: d["address"]["streetAddress"]=street
    if mail: d["email"]=mail
    if kind=="mb": d["parentOrganization"]={"@id":BASE+"#org"}
    br_ld.append(d)
def bcard(b):
    slug,name,kind,dist,street,town,pc,tel,mail,lat,lng = b
    who = '<p class="who">Mr Build</p>' if kind=="mb" else '<p class="who tb">The Builder · Collection point</p>'
    addr = esc(", ".join(x for x in [street, town] if x))
    return f'''      <article class="bcard rv" id="{slug}" data-district="{dist}">
        <div class="top"><div>{who}<h2>{name}</h2></div><span class="status" data-status hidden></span></div>
        <address>{addr}</address>
        <p class="hrs num">Mon–Fri 07:30–16:30 · Sat 07:30–12:30</p>
        <div class="acts">
          <a class="btn btn-r btn-sm" href="tel:{e164(tel)}">Call</a>
          <a class="btn btn-sm" href="{maps(b)}" target="_blank" rel="noopener">Directions</a>
          {f'<a class="btn btn-sm" href="mailto:{mail}" aria-label="Email {mail}">Email</a>' if mail else ''}
        </div>
      </article>'''
branches = head("branches.html","Stores and opening hours | Mr Build Limpopo",
  "Mr Build stores in Tzaneen, Mankweng, Louis Trichardt, Musina, Giyani, Sibasa and Thohoyandou, plus The Builder collection points. Map, phone numbers and hours.", br_ld, leaflet=True) \
 + nav("branches.html") + "<main>\n" + phero('Find your <span class="k">store</span>',
  '9 stores in Limpopo.<br><span class="y">Tap a pin.</span>') \
 + f'''<section class="sec bg-y dots-k slant-r" aria-labelledby="m-h">
  <div class="wrap">
    <div class="shead rv"><h2 class="beam" id="m-h">Store map</h2></div>
    {mapblock()}
  </div>
</section>

<section class="sec slant" aria-label="Store list" style="background:var(--white)">
  <div class="wrap">
    <div class="chips" role="group" aria-label="Filter by district">
      <button class="chip" type="button" data-filter="all" aria-pressed="true">All</button>
      <button class="chip" type="button" data-filter="vhembe" aria-pressed="false">Vhembe</button>
      <button class="chip" type="button" data-filter="mopani" aria-pressed="false">Mopani</button>
      <button class="chip" type="button" data-filter="capricorn" aria-pressed="false">Capricorn</button>
    </div>
    <div class="bgrid">
{chr(10).join(bcard(b) for b in BRANCHES)}
    </div>
    <div class="note rv"><h3>Ordered online?</h3><span>Wait for the "ready" message. Bring your order number and ID.</span></div>
  </div>
</section>
</main>
''' + footer()
write("branches.html", branches)

# ================= ABOUT =================
ab_ld = [ORG, {"@type":"AboutPage","name":"About Mr Build","url":BASE+"about.html","about":{"@id":BASE+"#org"}}]
about = head("about.html","About Mr Build | Your Building Buddy",
  "Mr Build has supplied builders and homeowners in Limpopo for 38 years. Meet Buddy, see our stores and the brands we stock.", ab_ld, leaflet=True) \
 + nav("about.html") + "<main>\n" + phero('<span class="num" data-count="38">38</span> <span class="k">years</span>',
  'Limpopo\'s<br><span class="y">building buddy.</span>') \
 + f'''<section class="meet sec slant-r" aria-labelledby="meet-h" style="background:var(--white)">
  <div class="wrap">
    <div class="bimg rv"><img src="img/buddy.svg" alt="Buddy in his yellow hard hat and overalls" width="92" height="100" loading="lazy"></div>
    <div class="rv">
      <p class="bubble l" style="display:inline-block;margin-bottom:22px">Howzit! I'm Buddy.</p>
      <h2 id="meet-h">Your <span class="r">building</span> buddy</h2>
      <p>Retail and wholesale at one counter. Homeowner or contractor, same help.</p>
    </div>
  </div>
</section>

<section class="sec bg-r dots slant" aria-labelledby="w-h">
  <div class="wrap">
    <div class="shead rv"><h2 class="beam y" id="w-h">What we do</h2></div>
    <ul class="pylon">
      <li class="rv y"><a href="services.html"><span class="ibox">{ic("building")}</span><h3>Retail &amp; wholesale</h3><span class="cnt">One counter</span></a></li>
      <li class="rv y"><a href="services.html#cutting"><span class="ibox">{ic("cutting")}</span><h3>Cutting &amp; edging</h3><span class="cnt">In store</span></a></li>
      <li class="rv y"><a href="services.html#doors"><span class="ibox">{ic("doors")}</span><h3>Wrapped doors</h3><span class="cnt">To order</span></a></li>
      <li class="rv y"><a href="services.html"><span class="ibox">{ic("paint")}</span><h3>BILHAM décor</h3><span class="cnt">Our own range</span></a></li>
    </ul>
  </div>
</section>

<section class="sec slant-r" aria-labelledby="y-h" style="background:var(--white)">
  <div class="wrap">
    <div class="shead rv"><h2 class="beam k" id="y-h">Our stores</h2></div>
    <ul class="yards">
      <li class="rv"><img src="img/store-pylon.jpg" alt="A Mr Build store with its red pylon sign, from above" loading="lazy" width="1600" height="1066"></li>
      <li class="rv"><img src="img/store-front.jpg" alt="A Mr Build shopfront on a main road, from above" loading="lazy" width="1280" height="720"></li>
      <li class="rv"><img src="img/store-yard.jpg" alt="A Mr Build yard stacked with bricks and blocks, from above" loading="lazy" width="1280" height="720"></li>
    </ul>
  </div>
</section>

<section class="sec bg-y dots-k slant" aria-labelledby="s-h">
  <div class="wrap">
    <div class="shead rv"><h2 class="beam" id="s-h">Where we trade</h2><a class="more" href="branches.html">Hours &amp; numbers →</a></div>
    {mapblock()}
  </div>
</section>

<section class="sec slant-r" aria-labelledby="b-h" style="background:var(--white)">
  <div class="wrap">
    <div class="shead rv"><h2 class="beam y" id="b-h">On our shelves</h2></div>
    {brands()}
  </div>
</section>
</main>
''' + footer()
write("about.html", about)

# ================= CONTACT =================
ct_ld = [dict(ORG, contactPoint=[{"@type":"ContactPoint","contactType":"customer service","telephone":"+27150040560","email":"info@mrbuild.co.za","areaServed":"ZA","availableLanguage":["en"]}]),
         {"@type":"ContactPage","name":"Contact Mr Build","url":BASE+"contact.html"}]
opts = "".join(f'<option value="{full(b)}">{b[1]}{" (The Builder)" if b[2]=="tb" else ""}</option>' for b in BRANCHES)
quick = "".join(f'<li><span>{b[1]}{" · TB" if b[2]=="tb" else ""}</span><a href="tel:{e164(b[7])}">{b[7]}</a></li>' for b in BRANCHES)
contact = head("contact.html","Contact | Mr Build Limpopo",
  "Call your nearest Mr Build store, email info@mrbuild.co.za or send a message. Head office in Tzaneen.", ct_ld) \
 + nav("contact.html") + "<main>\n" + phero('Talk to <span class="k">us</span>',
  'Call your store.<br><span class="y">Or drop a message.</span>') \
 + f'''<section class="contact sec slant-r" aria-label="Contact form and numbers" style="background:var(--white)">
  <div class="wrap">
    <div class="form-wrap rv">
      <form class="form" id="contact-form" action="https://formspree.io/f/REPLACE_ME" method="post" novalidate data-concept="true">
        <h2>Send a message</h2>
        <div class="row2">
          <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required><p class="err" aria-live="polite"></p></div>
          <div class="field"><label for="f-branch">Store <span class="opt">(optional)</span></label><select id="f-branch" name="branch"><option value="">Any store</option>{opts}</select><p class="err"></p></div>
        </div>
        <div class="row2">
          <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel"><p class="err" aria-live="polite"></p></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"><p class="err" aria-live="polite"></p></div>
        </div>
        <div class="field"><label for="f-topic">About</label><select id="f-topic" name="topic"><option>A quote</option><option>Cutting &amp; edging</option><option>Wrapped doors</option><option>An online order</option><option>Something else</option></select><p class="err"></p></div>
        <div class="field"><label for="f-msg">Message</label><textarea id="f-msg" name="message" required></textarea><p class="err" aria-live="polite"></p></div>
        <p class="hint">Phone or email, so we can reply.</p>
        <button class="btn btn-r" type="submit">Send message <span aria-hidden="true">→</span></button>
      </form>
      <div class="sent" role="status"><img src="img/buddy.svg" alt="" width="92" height="100"><h2>Got it!</h2><p>Buddy will get back to you soon.</p></div>
    </div>
    <div class="rv">
      <div class="hq"><h3>Head office</h3><p>Tzaneen · <a href="tel:+27150040560">015 004 0560</a><br><a href="mailto:info@mrbuild.co.za">info@mrbuild.co.za</a></p></div>
      <ul class="phones">{quick}</ul>
    </div>
  </div>
</section>
</main>
''' + footer()
write("contact.html", contact)
print("ok")
