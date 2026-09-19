import pathlib
from urllib.parse import quote

BASE = "https://poornachandrabatthula-create.github.io/aadhya-computer-embroidery/"
SERVICES = [
    ("computer-embroidery-nizamabad.html", "Computer Embroidery in Nizamabad"),
    ("maggam-works-nizamabad.html", "Maggam Works in Nizamabad"),
    ("bridal-blouse-nizamabad.html", "Bridal Blouse Designs & Embroidery in Nizamabad"),
    ("blouse-stitching-nizamabad.html", "Blouse Stitching in Nizamabad"),
    ("saree-fall-pico-nizamabad.html", "Saree Fall & Pico in Nizamabad"),
    ("saree-embroidery-nizamabad.html", "Saree Embroidery in Nizamabad"),
    ("pick-fall-nizamabad.html", "Pick & Fall in Nizamabad"),
    ("saree-kuchhulu-nizamabad.html", "Saree Kuchhulu in Nizamabad"),
    ("logo-embroidery-nizamabad.html", "Logo Embroidery in Nizamabad"),
]
ROOT = pathlib.Path(__file__).resolve().parents[1]
SEO = ROOT / "seo"

def make_page(filename, title):
    service = title.replace(" in Nizamabad", "")
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Aadhya Embroidery & Maggam Works</title>
<meta name="description" content="{title} by Aadhya Embroidery & Maggam Works, Nizamabad. Orders and enquiries: 8977715939. Pickup & Delivery available across Nizamabad.">
<link rel="canonical" href="{base}seo/{filename}">
<meta name="robots" content="index,follow">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","name":"{service}","areaServed":{{"@type":"City","name":"Nizamabad"}},"provider":{{"@type":"LocalBusiness","name":"Aadhya Embroidery & Maggam Works","telephone":"+91-8977715939","url":"{base}"}}}}
</script>
</head>
<body>
<main>
<h1>{title}</h1>
<p>{service} service from Aadhya Embroidery & Maggam Works in Nizamabad, Telangana.</p>
<p>Computer Embroidery • Maggam Works • Bridal Blouse Designs • Blouse Stitching • Saree Embroidery • Saree Fall & Pico • Pick & Fall • Saree Kuchhulu • Logo Embroidery</p>
<p><a href="https://wa.me/918977715939">WhatsApp Enquiry</a> | <a href="tel:+918977715939">Call 8977715939</a></p>
<p>Pickup & Delivery available across Nizamabad.</p>
<p><a href="../index.html">Back to Aadhya home</a></p>
</main>
</body>
</html>
""".format(title=title, service=service, base=BASE, filename=filename)

def main():
    SEO.mkdir(exist_ok=True)
    for filename, title in SERVICES:
        (SEO / filename).write_text(make_page(filename, title), encoding="utf-8")

    urls = {BASE}
    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts or "node_modules" in p.parts:
            continue
        rel = p.relative_to(ROOT).as_posix()
        urls.add(BASE + ("" if rel == "index.html" else quote(rel, safe="/._-")))
    for filename, _ in SERVICES:
        urls.add(BASE + "seo/" + filename)

    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in sorted(urls):
        xml.append("  <url><loc>%s</loc></url>" % url)
    xml.append("</urlset>")

    (ROOT / "sitemap.xml").write_text("\n".join(xml) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: " + BASE + "sitemap.xml\n",
        encoding="utf-8"
    )
    (ROOT / "automation-status.json").write_text(
        '{"status":"ok","generated_service_pages":%d,"sitemap":"%ssitemap.xml"}\n'
        % (len(SERVICES), BASE),
        encoding="utf-8"
    )

if __name__ == "__main__":
    main()
