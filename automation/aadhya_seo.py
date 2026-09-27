import json
import pathlib
from urllib.parse import quote

BASE = "https://poornachandrabatthula-create.github.io/aadhya-computer-embroidery/"
ROOT = pathlib.Path(__file__).resolve().parents[1]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
CATEGORIES = [["computer-embroidery","COMPUTER EMBROIDERY","కంప్యూటర్ ఎంబ్రాయిడరీ"],["maggam-works","MAGGAM WORKS","మగ్గం వర్క్స్"],["blouse-stitching","BLOUSE STITCHING","బ్లౌజ్ స్టిచింగ్"],["kids-embroidery","KIDS EMBROIDERY","కిడ్స్ ఎంబ్రాయిడరీ"],["logo-embroidery","LOGO EMBROIDERY","లోగో ఎంబ్రాయిడరీ"],["saree-kuchhulu","SAREE KUCHHULU","చీర కుచ్చులు / టాసెల్స్"],["pick-fall","PICK & FALL","పికో & ఫాల్"],["saree-iron","SAREE IRON","చీర ఐరన్"]]

def build_gallery_manifest():
    sections = []
    total = 0
    for folder, en, te in CATEGORIES:
        images = []
        directory = ROOT / "images" / folder
        if directory.exists():
            for path in sorted(directory.iterdir(), key=lambda p: p.name.lower()):
                if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
                    rel = path.relative_to(ROOT).as_posix()
                    images.append({"src": quote(rel, safe="/._-()"), "alt": f"Aadhya {en.title()} work"})
        total += len(images)
        sections.append({"folder": folder, "en": en, "te": te, "images": images})
    payload = {"generated_by": "automation/aadhya_seo.py", "total_images": total, "sections": sections}
    (ROOT / "gallery-data.json").write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    return total

def build_sitemap():
    urls = []
    for path in sorted(ROOT.glob("*.html")):
        if path.name == "404.html" or path.name.startswith("google"):
            continue
        rel = path.relative_to(ROOT).as_posix()
        urls.append(BASE if rel == "index.html" else BASE + quote(rel, safe="/._-"))
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        xml.append(f"  <url><loc>{url}</loc></url>")
    xml.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(xml) + "\n", encoding="utf-8")

def main():
    total_images = build_gallery_manifest()
    build_sitemap()
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: " + BASE + "sitemap.xml\n", encoding="utf-8")
    (ROOT / "automation-status.json").write_text(json.dumps({"status": "ok", "gallery_images": total_images, "sitemap": BASE + "sitemap.xml"}, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Generated gallery-data.json with {total_images} images and refreshed sitemap/robots.")

if __name__ == "__main__":
    main()
