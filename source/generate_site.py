#!/usr/bin/env python3
"""Generate a single-page static site for Lawrence Fane from source/content.json.

Outputs:
  docs/index.html
  docs/styles.css

Images are expected to already live in docs/images/ (filenames match the
"local" field of each image in content.json).
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(HERE, "content.json")
SITE = os.path.join(ROOT, "docs")


def clean_title(t):
    """Return a human-friendly caption, or None if the title is junk
    (auto-generated filename, camera name, screenshot, numeric id)."""
    if not t:
        return None
    t = t.strip()
    if t.endswith("###") or t.endswith("_###"):
        return None
    if t.startswith("IMG_"):
        return None
    if t.lower().startswith("screen shot"):
        return None
    if re.match(r"^\d", t):  # starts with a digit -> filename/timestamp derived
        return None
    # light cleanup of export-artifact suffixes
    t = re.sub(r"\s*\bjpeg\b", "", t, flags=re.I)
    t = re.sub(r"\s*\b(lr|sml|cu|rgb|ovrvw)\b", "", t, flags=re.I)
    t = re.sub(r"\s*[_-]?v?\d+$", "", t)  # trailing " v1", "_1", "-1"
    t = re.sub(r"\s{2,}", " ", t).strip(" -_")
    return t or None


def gallery(images):
    items = []
    for img in images:
        src = "images/" + html.escape(img["local"])
        cap = clean_title(img.get("title"))
        alt = html.escape(cap or "Sculpture by Lawrence Fane")
        cap_attr = f' data-caption="{html.escape(cap)}"' if cap else ""
        figcap = f'<figcaption>{html.escape(cap)}</figcaption>' if cap else ""
        items.append(
            f'      <figure class="tile">\n'
            f'        <img src="{src}" alt="{alt}" loading="lazy"{cap_attr}>\n'
            f'        {figcap}\n'
            f'      </figure>'
        )
    return "\n".join(items)


def text_block(raw):
    """Render a multi-line text field. Lines ending in ':' become subheadings."""
    out = []
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        esc = html.escape(line)
        if line.endswith(":"):
            out.append(f'      <h3 class="subhead">{esc}</h3>')
        else:
            out.append(f'      <p class="entry">{esc}</p>')
    return "\n".join(out)


def main():
    with open(CONTENT, encoding="utf-8") as f:
        d = json.load(f)

    home_hero = d["home_images"][0]["local"] if d.get("home_images") else None

    # The collections text leads with its own heading line; drop it (we add one).
    collections_body = d["collections_text"]
    collections_body = re.sub(
        r"^\s*PUBLIC COLLECTIONS AND COMMISSIONS\s*\n", "", collections_body, flags=re.I
    )

    # Contact text leads with "Get in touch" + form field labels we don't want.
    contact_intro = (
        "Selected works are available for sale or donation to museums. "
        "Please get in touch for further information."
    )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lawrence Fane — Sculptor</title>
  <meta name="description" content="The sculpture and drawings of Lawrence Fane (1933–2008).">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="#home">Lawrence Fane</a>
    <nav class="nav">
      <a href="#sculpture">Sculpture</a>
      <a href="#drawings">Drawings</a>
      <a href="#about">About</a>
      <a href="#contact">Contact</a>
      <a class="nav-ig" href="https://www.instagram.com/lawrencefanestudio/" target="_blank" rel="noopener noreferrer" aria-label="Instagram — opens in a new tab">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.81-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.81-.25-2.23-.41a3.7 3.7 0 0 1-1.38-.9 3.7 3.7 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.81.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16Zm0 1.62c-3.15 0-3.5.01-4.74.07-.97.04-1.5.21-1.85.34-.46.18-.8.4-1.15.74-.34.35-.56.69-.74 1.15-.13.35-.3.88-.34 1.85-.06 1.24-.07 1.59-.07 4.74s.01 3.5.07 4.74c.04.97.21 1.5.34 1.85.18.46.4.8.74 1.15.35.34.69.56 1.15.74.35.13.88.3 1.85.34 1.24.06 1.59.07 4.74.07s3.5-.01 4.74-.07c.97-.04 1.5-.21 1.85-.34.46-.18.8-.4 1.15-.74.34-.35.56-.69.74-1.15.13-.35.3-.88.34-1.85.06-1.24.07-1.59.07-4.74s-.01-3.5-.07-4.74c-.04-.97-.21-1.5-.34-1.85a3.1 3.1 0 0 0-.74-1.15 3.1 3.1 0 0 0-1.15-.74c-.35-.13-.88-.3-1.85-.34-1.24-.06-1.59-.07-4.74-.07Zm0 2.76a5.46 5.46 0 1 1 0 10.92 5.46 5.46 0 0 1 0-10.92Zm0 9a3.54 3.54 0 1 0 0-7.08 3.54 3.54 0 0 0 0 7.08Zm6.95-9.22a1.28 1.28 0 1 1-2.55 0 1.28 1.28 0 0 1 2.55 0Z"/></svg>
        <span>Instagram</span>
      </a>
    </nav>
  </header>

  <section id="home" class="hero"{f' style="background-image:linear-gradient(rgba(20,18,15,.45),rgba(20,18,15,.55)),url(images/{html.escape(home_hero)})"' if home_hero else ''}>
    <div class="hero-inner">
      <h1>Lawrence Fane</h1>
      <p class="tagline">{html.escape(d['home_title'])}</p>
      <a class="cta" href="#sculpture">View the work</a>
    </div>
  </section>

  <main>
    <section id="sculpture" class="section">
      <div class="section-head">
        <h2>{html.escape(d['sculpture_title'])}</h2>
      </div>
      <div class="grid">
{gallery(d['sculpture_images'])}
      </div>
    </section>

    <section id="drawings" class="section alt">
      <div class="section-head">
        <h2>{html.escape(d['drawings_title'])}</h2>
      </div>
      <div class="grid">
{gallery(d['drawings_images'])}
      </div>
    </section>

    <section id="about" class="section">
      <div class="section-head">
        <h2>About</h2>
      </div>
      <div class="prose">
        <p class="bio">{html.escape(d['bio_text'])}</p>
      </div>
      <div class="columns">
        <div class="col">
          <h3 class="col-title">Exhibitions</h3>
{text_block(d['shows_text'])}
        </div>
        <div class="col">
          <h3 class="col-title">Public Collections &amp; Commissions</h3>
{text_block(collections_body)}
        </div>
      </div>
    </section>

    <section id="contact" class="section alt">
      <div class="section-head">
        <h2>{html.escape(d['contact_title'])}</h2>
      </div>
      <div class="prose contact">
        <p>{html.escape(contact_intro)}</p>
        <p class="email-link"><a href="mailto:info@lawrencefane.com">info@lawrencefane.com</a></p>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <p>Lawrence Fane (1933–2008). &copy; The Estate of Lawrence Fane.</p>
  </footer>

  <!-- Lightbox -->
  <div class="lightbox" id="lightbox" hidden>
    <button class="lb-close" aria-label="Close">&times;</button>
    <button class="lb-prev" aria-label="Previous">&#8249;</button>
    <img class="lb-img" id="lb-img" alt="">
    <button class="lb-next" aria-label="Next">&#8250;</button>
    <div class="lb-caption" id="lb-caption"></div>
  </div>

  <script src="app.js"></script>
</body>
</html>
"""

    css = """:root{
  --bg:#f7f5f1;
  --bg-alt:#efece5;
  --ink:#1f1c18;
  --muted:#6b655c;
  --accent:#8a5a2b;
  --line:#ddd8cf;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;background:var(--bg);color:var(--ink);
  font-family:var(--sans);line-height:1.6;
  -webkit-font-smoothing:antialiased;
}
img{display:block;max-width:100%}

/* Header */
.site-header{
  position:sticky;top:0;z-index:50;
  display:flex;align-items:center;justify-content:space-between;
  padding:.9rem 1.6rem;
  background:rgba(247,245,241,.92);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--line);
}
.brand{
  font-family:var(--serif);font-size:1.25rem;letter-spacing:.04em;
  color:var(--ink);text-decoration:none;font-weight:600;
}
.nav a{
  color:var(--muted);text-decoration:none;margin-left:1.4rem;
  font-size:.82rem;text-transform:uppercase;letter-spacing:.12em;
  transition:color .2s;
}
.nav a:hover{color:var(--accent)}
.nav a.nav-ig{display:inline-flex;align-items:center;gap:.4rem}
.nav a.nav-ig svg{display:block}

/* Hero */
.hero{
  min-height:78vh;display:flex;align-items:center;justify-content:center;
  text-align:center;color:#fff;background-size:cover;background-position:center;
  padding:4rem 1.5rem;
}
.hero-inner{max-width:760px}
.hero h1{
  font-family:var(--serif);font-weight:600;
  font-size:clamp(2.6rem,7vw,5rem);margin:0;letter-spacing:.02em;
  text-shadow:0 2px 24px rgba(0,0,0,.4);
}
.tagline{
  font-family:var(--serif);font-style:italic;
  font-size:clamp(1.05rem,2.4vw,1.5rem);margin:1rem auto 2rem;
  max-width:34ch;text-shadow:0 1px 12px rgba(0,0,0,.5);
}
.cta{
  display:inline-block;color:#fff;text-decoration:none;
  border:1px solid rgba(255,255,255,.7);padding:.7rem 1.6rem;
  text-transform:uppercase;letter-spacing:.14em;font-size:.78rem;
  transition:background .2s,color .2s;
}
.cta:hover{background:#fff;color:var(--ink)}

/* Sections */
.section{padding:5rem 1.6rem;max-width:1200px;margin:0 auto}
.section.alt{background:var(--bg-alt);max-width:none}
.section.alt > *{max-width:1200px;margin-left:auto;margin-right:auto}
.section-head{margin-bottom:2.5rem;text-align:center}
.section-head h2{
  font-family:var(--serif);font-weight:600;
  font-size:clamp(1.7rem,4vw,2.4rem);margin:0;
}
.section-head h2::after{
  content:"";display:block;width:48px;height:2px;background:var(--accent);
  margin:.9rem auto 0;
}

/* Galleries */
.grid{
  display:grid;gap:1.1rem;
  grid-template-columns:repeat(auto-fill,minmax(220px,1fr));
}
.tile{margin:0;cursor:zoom-in;overflow:hidden;background:#e7e2d9;position:relative}
.tile img{
  width:100%;height:260px;object-fit:cover;
  transition:transform .5s ease,filter .3s;
}
.tile:hover img{transform:scale(1.05);filter:brightness(1.04)}
.tile figcaption{
  position:absolute;left:0;right:0;bottom:0;
  font-family:var(--serif);font-style:italic;font-size:.9rem;
  color:#fff;padding:1.4rem .8rem .6rem;
  background:linear-gradient(transparent,rgba(0,0,0,.65));
  opacity:0;transform:translateY(6px);transition:opacity .3s,transform .3s;
}
.tile:hover figcaption{opacity:1;transform:none}

/* Prose */
.prose{max-width:760px;margin:0 auto}
.bio{font-size:1.12rem;line-height:1.8}
.columns{
  display:grid;gap:3rem;grid-template-columns:1fr 1fr;
  max-width:1000px;margin:3.5rem auto 0;
}
.col-title{
  font-family:var(--serif);font-size:1.3rem;margin:0 0 1rem;
  padding-bottom:.5rem;border-bottom:1px solid var(--line);
}
.subhead{
  font-family:var(--sans);text-transform:uppercase;letter-spacing:.1em;
  font-size:.78rem;color:var(--accent);margin:1.4rem 0 .5rem;
}
.entry{margin:.25rem 0;font-size:.92rem;color:var(--muted);line-height:1.5}

/* Contact */
.contact{text-align:center}
.email-link{margin-top:1.5rem}
.email-link a{
  font-family:var(--serif);font-size:1.4rem;color:var(--accent);
  text-decoration:none;border-bottom:1px solid transparent;transition:border-color .2s;
}
.email-link a:hover{border-bottom-color:var(--accent)}

/* Footer */
.site-footer{
  text-align:center;padding:2.5rem 1.6rem;color:var(--muted);
  font-size:.82rem;border-top:1px solid var(--line);
}

/* Lightbox */
.lightbox{
  position:fixed;inset:0;z-index:100;
  display:flex;align-items:center;justify-content:center;
  background:rgba(15,13,11,.94);
}
.lightbox[hidden]{display:none}
.lb-img{
  max-width:88vw;max-height:82vh;object-fit:contain;
  box-shadow:0 10px 60px rgba(0,0,0,.6);
}
.lb-caption{
  position:absolute;bottom:4vh;left:0;right:0;text-align:center;
  color:#eee;font-family:var(--serif);font-style:italic;font-size:1.05rem;
}
.lb-close,.lb-prev,.lb-next{
  position:absolute;background:none;border:0;color:#fff;cursor:pointer;
  font-size:2.6rem;line-height:1;opacity:.8;transition:opacity .2s;padding:1rem;
}
.lb-close:hover,.lb-prev:hover,.lb-next:hover{opacity:1}
.lb-close{top:1rem;right:1.4rem;font-size:2.2rem}
.lb-prev{left:1rem}
.lb-next{right:1rem}

@media (max-width:680px){
  .columns{grid-template-columns:1fr;gap:2rem}
  .tile img{height:200px}
  .nav a{margin-left:.9rem}
  .section{padding:3.5rem 1.1rem}
}
"""

    appjs = """// Lightbox + gallery navigation
(function () {
  var tiles = Array.prototype.slice.call(document.querySelectorAll('.tile img'));
  var lb = document.getElementById('lightbox');
  var lbImg = document.getElementById('lb-img');
  var lbCap = document.getElementById('lb-caption');
  var idx = -1;

  function show(i) {
    if (i < 0) i = tiles.length - 1;
    if (i >= tiles.length) i = 0;
    idx = i;
    var img = tiles[idx];
    lbImg.src = img.src;
    lbImg.alt = img.alt;
    var cap = img.getAttribute('data-caption') || '';
    lbCap.textContent = cap;
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
  }
  function close() {
    lb.hidden = true;
    document.body.style.overflow = '';
  }

  tiles.forEach(function (img, i) {
    img.addEventListener('click', function () { show(i); });
  });
  lb.querySelector('.lb-close').addEventListener('click', close);
  lb.querySelector('.lb-next').addEventListener('click', function (e) { e.stopPropagation(); show(idx + 1); });
  lb.querySelector('.lb-prev').addEventListener('click', function (e) { e.stopPropagation(); show(idx - 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowRight') show(idx + 1);
    else if (e.key === 'ArrowLeft') show(idx - 1);
  });
})();
"""

    os.makedirs(SITE, exist_ok=True)
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    with open(os.path.join(SITE, "styles.css"), "w", encoding="utf-8") as f:
        f.write(css)
    with open(os.path.join(SITE, "app.js"), "w", encoding="utf-8") as f:
        f.write(appjs)

    print("Wrote docs/index.html, docs/styles.css, docs/app.js")
    print("Sculpture images: %d" % len(d["sculpture_images"]))
    print("Drawing images:   %d" % len(d["drawings_images"]))


if __name__ == "__main__":
    main()
