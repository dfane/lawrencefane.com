"""Extract clean content from scraped Pixpa pages.

Output: content.json with bio, shows, collections, contact, and image lists for
the sculpture / drawings / home pages.
"""
import base64
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

HERE = Path(__file__).parent

# Nav strings to strip out of body text — they appear 2-3 times per page.
NAV_LINES = {
    "Lawrence Fane", "Home", "Selected Work", "Sculpture", "Drawings",
    "Contact", "About", "Bio", "Shows and Exhibitions",
    "Public Collections and Commissions",
}

# Pixpa share-widget tail that appears at the bottom of every content page.
TAIL_NOISE = {
    "Previous", "Next", "Lawrence Fane Studio", "Share", "Copied",
}


def soup(name):
    return BeautifulSoup((HERE / name).read_text(encoding="utf-8"), "html.parser")


def clean_text(node):
    if node is None:
        return ""
    for s in node(["script", "style", "noscript", "nav", "header", "footer"]):
        s.decompose()
    text = node.get_text("\n", strip=True)
    lines = [ln for ln in (l.strip() for l in text.split("\n")) if ln]
    # Drop nav links wherever they appear (Pixpa renders the menu 3x: top,
    # mobile, and footer). We drop until the first non-nav line, then keep all.
    out, started = [], False
    for ln in lines:
        if not started and ln in NAV_LINES:
            continue
        started = True
        # Even after content starts, skip standalone nav lines that recur
        if ln in NAV_LINES and len(out) > 0 and out[-1] in NAV_LINES:
            continue
        out.append(ln)
    # Final pass: drop nav and Pixpa share-widget cruft from the tail
    drop_at_tail = NAV_LINES | TAIL_NOISE
    while out and (
        out[-1] in drop_at_tail
        or out[-1].startswith("http://www.lawrencefane.com/")
        or out[-1].startswith("https://www.lawrencefane.com/")
    ):
        out.pop()
    return "\n".join(out)


def main_content(s):
    return (
        s.select_one(".pixpa-content-page")
        or s.select_one("#content")
        or s.select_one("main")
        or s.body
    )


def decode_pixpa_url(url):
    """Return (original_filename, s3_key) from a px-web-images URL.

    Pixpa URLs look like:
      https://px-web-images3.pixpa.com/HASH/rs:fit:1200:0/q:80/<base64>
    where <base64> decodes to s3://pixpa-test/com/large/122853/<id>-<id>-<slug>.jpg
    """
    m = re.search(r"/([A-Za-z0-9_=-]+)$", url)
    if not m:
        return None, None
    b64 = m.group(1)
    # Pixpa uses URL-safe base64 without padding sometimes
    padded = b64 + "=" * (-len(b64) % 4)
    try:
        decoded = base64.urlsafe_b64decode(padded).decode("utf-8", errors="replace")
    except Exception:
        return None, None
    # Pull out the filename slug
    fn = decoded.rsplit("/", 1)[-1]
    return fn, decoded


def gallery_images(s):
    """Pull image data from gallery pages. Returns list of dicts."""
    images = []
    seen = set()
    for img in s.find_all("img"):
        data_src = img.get("data-src", "")
        if "pixpa.com" not in data_src or "px-s3-img" in data_src:
            continue  # skip loader icons
        # Pick highest-res from srcset if present
        srcset = img.get("data-srcset", "") or img.get("srcset", "")
        best = data_src
        if srcset:
            best_w = 0
            for part in srcset.split(","):
                part = part.strip()
                bits = part.rsplit(" ", 1)
                if len(bits) == 2 and bits[1].endswith("w"):
                    try:
                        w = int(bits[1][:-1])
                    except ValueError:
                        continue
                    if w > best_w:
                        best_w = w
                        best = bits[0]
        decoded_filename, s3_key = decode_pixpa_url(best)
        filename = img.get("data-filename") or decoded_filename or ""
        if best in seen:
            continue
        seen.add(best)
        # Local filename: slug from decoded path
        local = decoded_filename or filename.lower().replace(" ", "-")
        images.append({
            "url": best,
            "title": filename.rsplit(".", 1)[0] if filename else "",
            "local": local,
            "width": img.get("data-width") or img.get("width"),
            "height": img.get("data-height") or img.get("height"),
        })
    return images


def page_title(s):
    # Pixpa wraps page title in h1 inside main content
    main = main_content(s)
    h = main.select_one("h1, h2, .pageTitle") if main else None
    return h.get_text(strip=True) if h else ""


def extract_all():
    out = {}

    for key, fname in [
        ("bio", "about1_about.html"),
        ("shows", "about1_shows-and-exhibits.html"),
        ("collections", "about1_public-collections-and-commissions.html"),
        ("contact", "contact.html"),
    ]:
        s = soup(fname)
        out[f"{key}_title"] = page_title(s)
        out[f"{key}_text"] = clean_text(main_content(s))

    for key, fname in [
        ("sculpture", "projects_project1.html"),
        ("drawings", "projects_project2.html"),
        ("home", "home.html"),
    ]:
        s = soup(fname)
        out[f"{key}_title"] = page_title(s)
        out[f"{key}_images"] = gallery_images(s)

    return out


if __name__ == "__main__":
    data = extract_all()
    (HERE / "content.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
    for k, v in data.items():
        if isinstance(v, str):
            print(f"=== {k} ({len(v)} chars) ===")
            print(v[:800])
            print()
        else:
            print(f"=== {k}: {len(v)} items ===")
            for item in v[:4]:
                print(f"  {item['title']!r:30s} -> {item['local']}")
            print()
