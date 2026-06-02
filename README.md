# Lawrence Fane — website

The website for the sculpture and drawings of Lawrence Fane (1933–2008).
It's a plain static website (just HTML, CSS, and a little JavaScript), so it can
be hosted anywhere — these instructions use **GitHub Pages**, which is free.

---

## What's in this folder

| Folder / file | What it is |
|---|---|
| **`docs/`** | **The actual website that gets published.** GitHub Pages serves this folder. |
| `docs/index.html` | The single page (all sections live here). |
| `docs/styles.css` | All the styling (colors, fonts, layout). |
| `docs/app.js` | The image lightbox behavior. |
| `docs/images/` | Every image shown on the site. |
| `source/` | The files used to maintain the site. Not published. |
| `source/content.json` | The text and image list, kept separately so the page can be re-generated. |
| `source/generate_site.py` | A script that rebuilds `docs/index.html` from `content.json`. |
| `source/download_images.py` | Helper to (re-)download images listed in `content.json` into `images/`. |
| `images/` | The original full-size downloads (kept as a backup). Not published. |

> **Rule of thumb:** if it's not inside `docs/`, it does not appear on the live website.
> (GitHub Pages is configured to publish the `docs/` folder — see below.)

---

## Looking at the site on your own computer first

Before publishing, you can preview changes locally. Open the **Terminal** app, then:

```bash
cd /Users/fane/test_claude/lawrencefane-site/docs
python3 -m http.server 8000
```

Now open your browser to **http://localhost:8000**. Press `Ctrl+C` in the Terminal
to stop the preview when you're done.

---

## Making changes

There are two ways to edit, depending on what you want to change.

### Option A — Change wording or the list of images (recommended)

The bio, exhibition list, collections list, and the gallery image lists all come
from **`source/content.json`**. Edit that file, then re-run the generator to
rebuild the page:

```bash
cd /Users/fane/test_claude/lawrencefane-site
python3 source/generate_site.py
```

This rewrites `docs/index.html` (and `styles.css` / `app.js`) for you. Preview it
(see above), and if it looks right, publish it (see below).

### Option B — Tweak the design directly

For colors, fonts, spacing, or layout, edit **`docs/styles.css`** directly.
For one-off wording or structure, you can edit **`docs/index.html`** directly.

> ⚠️ Note: if you hand-edit `docs/index.html` and *then* run the generator again,
> the generator will **overwrite** your hand edits. So pick one approach per change:
> either edit `content.json` + regenerate, **or** edit `docs/index.html` by hand.

### Adding or replacing a photo

1. Put the image file into **`docs/images/`**.
2. Add an entry for it in the matching list in `source/content.json` (e.g.
   `sculpture_images` or `drawings_images`). Copy an existing entry and change the
   `"title"` and `"local"` (the `"local"` value is just the file name).
3. Re-run the generator (Option A).

---

## Turning on GitHub Pages (one time only)

This repository is already connected to GitHub
(`git@github.com:dfane/lawrencefane.com.git`). The only one-time step is telling
GitHub Pages to publish the `docs/` folder:

1. On GitHub, open the repository → **Settings** → **Pages** (left sidebar).
2. Under **Build and deployment → Source**, choose **Deploy from a branch**.
3. Set the branch to **`main`** and the folder to **`/docs`**, then click **Save**.

Within a minute or two the site will be live at:

```
https://dfane.github.io/lawrencefane.com/
```

(That's it — there's no build step or GitHub Action to manage. Pages simply serves
whatever is in `docs/` on the `main` branch.)

---

## Publishing changes (every time after that)

Once Pages is turned on, the routine for any future change is just three commands.
After editing and previewing your changes (and re-running the generator if you
edited `content.json`):

```bash
cd /Users/fane/test_claude/lawrencefane-site
git add -A
git commit -m "Describe what you changed here"
git push
```

That's all. Every push to `main` re-publishes the `docs/` folder automatically —
the live site usually updates within a minute.

---

## The contact section

The **Get in touch** section is a simple email link to
`fane@dimitrifane.com` (clicking it opens the visitor's email program).
To change the address, edit the contact section near the bottom of
`source/generate_site.py` and re-run the generator.

---

## Quick reference

| I want to… | Do this |
|---|---|
| Preview the site locally | `cd docs` then `python3 -m http.server 8000`, open http://localhost:8000 |
| Change text / image lists | Edit `source/content.json`, then `python3 source/generate_site.py` |
| Change colors / layout | Edit `docs/styles.css` |
| Publish my changes | `git add -A` → `git commit -m "..."` → `git push` |
| See the live site | `https://dfane.github.io/lawrencefane.com/` |
