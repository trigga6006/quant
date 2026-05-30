# Brand / Social card

The social ("OG") card for the **quant-research** skill, made by **Omni Impact**.

| File | Size | Use |
|------|------|-----|
| `index.html` | — | Source of truth (fluid; fills the viewport) |
| `og.png` | 1280×640, ~470 KB | **GitHub social preview** + general OG/Twitter card |
| `og@2x.png` | 2560×1280 | Retina / print / high-DPI use |

Design: black field with a cold light from the right, `/quant` set in **Geist** with a
salmon brand slash, a green uptrend (green = up, market convention) with a live readout,
and the Omni Impact mark anchored at the base. Type is Geist + Geist Mono throughout.

## Make it render when the repo link is pasted

GitHub does **not** read `og:image` meta tags from a repo — it serves the image you upload
under **Social preview**. To wire it up:

1. Go to **https://github.com/trigga6006/quant** → **Settings** → **General**.
2. Scroll to **Social preview** → **Edit** → upload `docs/brand/og.png`.
3. Done. Pasting the repo link in Slack / Discord / X / iMessage etc. now unfurls this card.

> Must be a PNG/JPG/GIF under **1 MB** and at least 640×320 (ideal 1280×640). `og.png` fits.

For a docs site (e.g. GitHub Pages), reference it with:

```html
<meta property="og:image" content="https://<your-domain>/docs/brand/og.png">
<meta name="twitter:card" content="summary_large_image">
```

## Re-render after editing `index.html`

Headless Chrome (Windows paths shown):

```bash
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
DIR="C:/Users/fowle/Documents/dev/skills/quant/docs/brand"

# 1280x640 (GitHub spec)
"$CHROME" --headless=new --hide-scrollbars --user-data-dir="$(mktemp -d)" \
  --window-size=1280,640 --virtual-time-budget=4000 \
  --screenshot="$DIR/og.png" "file:///$DIR/index.html"

# 2x retina (2560x1280)
"$CHROME" --headless=new --hide-scrollbars --user-data-dir="$(mktemp -d)" \
  --force-device-scale-factor=2 --window-size=1280,640 --virtual-time-budget=4000 \
  --screenshot="$DIR/og@2x.png" "file:///$DIR/index.html"
```

Notes: `--user-data-dir` avoids a Windows "access denied" write error; `--virtual-time-budget`
lets the Google Fonts (Geist / Geist Mono) finish loading before the screenshot.

## Live preview

`.claude/launch.json` serves this folder. Start the **quant-card** preview, then open the
served `index.html`.
