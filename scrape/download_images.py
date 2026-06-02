"""Download all unique images at best available size into ../images/."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
IMG_DIR = HERE.parent / "images"
IMG_DIR.mkdir(exist_ok=True)

data = json.loads((HERE / "content.json").read_text())

# Dedupe by local filename (multiple pages may reference the same image).
to_get = {}
for key in ("sculpture_images", "drawings_images", "home_images"):
    for item in data[key]:
        to_get.setdefault(item["local"], item["url"])

print(f"{len(to_get)} unique images to fetch")


def fetch(item):
    local, url = item
    dest = IMG_DIR / local
    if dest.exists() and dest.stat().st_size > 0:
        return local, "skip", dest.stat().st_size
    r = subprocess.run(
        ["curl", "-sL", "-A", "Mozilla/5.0", "-o", str(dest), url],
        capture_output=True,
    )
    size = dest.stat().st_size if dest.exists() else 0
    return local, "ok" if r.returncode == 0 and size > 0 else "fail", size


with ThreadPoolExecutor(max_workers=8) as ex:
    for local, status, size in ex.map(fetch, to_get.items()):
        print(f"{status:5s} {size:>8d}  {local}")
