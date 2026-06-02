# Lawrence Fane — website

The website for the sculpture and drawings of Lawrence Fane (1933–2008).
It's a plain static website (just HTML, CSS, and a little JavaScript), so it can
be hosted anywhere — these instructions use **GitHub Pages**, which is free.

---

## What's in this folder

| Folder / file | What it is |
|---|---|
| **`site/`** | **The actual website that gets published.** This is the important folder. |
| `site/index.html` | The single page (all sections live here). |
| `site/styles.css` | All the styling (colors, fonts, layout). |
| `site/app.js` | The image lightbox and the contact form behavior. |
| `site/images/` | Every image shown on the site. |
| `scrape/` | Behind-the-scenes source material: the original scraped pages, the image downloader, and `content.json`. Not published. |
| `scrape/content.json` | The text and image list, kept separately so the page can be re-generated. |
| `scrape/generate_site.py` | A script that rebuilds `site/index.html` from `content.json`. |
| `images/` | The original full-size downloads (kept as a backup). Not published. |

> **Rule of thumb:** if it's not inside `site/`, it does not appear on the live website.

---

## Looking at the site on your own computer first

Before publishing, you can preview changes locally. Open the **Terminal** app, then:

```bash
cd /Users/fane/test_claude/lawrencefane-site/site
python3 -m http.server 8000
```

Now open your browser to **http://localhost:8000**. Press `Ctrl+C` in the Terminal
to stop the preview when you're done.

---

## Making changes

There are two ways to edit, depending on what you want to change.

### Option A — Change wording or the list of images (recommended)

The bio, exhibition list, collections list, and the gallery image lists all come
from **`scrape/content.json`**. Edit that file, then re-run the generator to
rebuild the page:

```bash
cd /Users/fane/test_claude/lawrencefane-site
python3 scrape/generate_site.py
```

This rewrites `site/index.html` (and `styles.css` / `app.js`) for you. Preview it
(see above), and if it looks right, publish it (see below).

### Option B — Tweak the design directly

For colors, fonts, spacing, or layout, edit **`site/styles.css`** directly.
For one-off wording or structure, you can edit **`site/index.html`** directly.

> ⚠️ Note: if you hand-edit `site/index.html` and *then* run the generator again,
> the generator will **overwrite** your hand edits. So pick one approach per change:
> either edit `content.json` + regenerate, **or** edit `site/index.html` by hand.

### Adding or replacing a photo

1. Put the image file into **`site/images/`**.
2. Add an entry for it in the matching list in `scrape/content.json` (e.g.
   `sculpture_images` or `drawings_images`). Copy an existing entry and change the
   `"title"` and `"local"` (the `"local"` value is just the file name).
3. Re-run the generator (Option A).

---

## Publishing to GitHub (first time only)

You only do these steps once.

### 1. Create the repository on GitHub

- Go to <https://github.com/new>.
- Name it (for example `lawrencefane-site`), leave it **Public**, and **do not**
  add a README/license (this folder already has files). Click **Create repository**.
- GitHub will show a page with a URL like
  `https://github.com/YOUR-USERNAME/lawrencefane-site.git` — keep it handy.

### 2. Push this folder up to it

In the Terminal:

```bash
cd /Users/fane/test_claude/lawrencefane-site
git init
git add .
git commit -m "Initial version of the Lawrence Fane website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/lawrencefane-site.git
git push -u origin main
```

(Replace the URL with the one from step 1. If git asks you to log in, follow the
prompts — GitHub will ask you to authenticate in your browser.)

### 3. Turn on GitHub Pages

- On GitHub, open your repository → **Settings** → **Pages** (left sidebar).
- Under **Build and deployment → Source**, choose **GitHub Actions**.

That's it. A workflow file is already included in this project
(`.github/workflows/deploy.yml`), so within a minute or two your site will be live at:

```
https://YOUR-USERNAME.github.io/lawrencefane-site/
```

You can watch it deploy under the repository's **Actions** tab.

---

## Publishing changes (every time after that)

Once the one-time setup is done, the routine for any future change is just three
commands. After editing (and previewing) your changes:

```bash
cd /Users/fane/test_claude/lawrencefane-site
git add .
git commit -m "Describe what you changed here"
git push
```

That's all. Every push to `main` automatically rebuilds and re-publishes the live
site — usually live within a minute. Check the **Actions** tab on GitHub if you
want to confirm it finished.

---

## The contact form

The site is static, so the contact form doesn't send email until you connect it
to something. You have two easy options:

- **Quickest — email link:** open `site/app.js`, find the line
  `var CONTACT_EMAIL = '';`, and put an email address between the quotes, e.g.
  `var CONTACT_EMAIL = 'name@example.com';`. The form will then open the
  visitor's email program with the message pre-filled.
- **Nicer — a hosted form service** (e.g. [Formspree](https://formspree.io)):
  sign up, get a form URL, and in `site/index.html` change
  `<form ... action="#" method="post">` so `action` points at that URL.

---

## Quick reference

| I want to… | Do this |
|---|---|
| Preview the site locally | `cd site` then `python3 -m http.server 8000`, open http://localhost:8000 |
| Change text / image lists | Edit `scrape/content.json`, then `python3 scrape/generate_site.py` |
| Change colors / layout | Edit `site/styles.css` |
| Publish my changes | `git add .` → `git commit -m "..."` → `git push` |
| See the live site | `https://YOUR-USERNAME.github.io/lawrencefane-site/` |
