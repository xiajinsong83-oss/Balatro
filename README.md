# BalatroHub - Hugo Edition

A Hugo-based static site for Balatro players. Built for SEO, AdSense, and automated daily content updates.

## Quick Start

```bash
# Install Hugo extended
brew install hugo  # macOS
# or download from https://github.com/gohugoio/hugo/releases

# Run local dev server
hugo server -D
```

## Project Structure

```
├── content/           # Markdown pages (static content)
│   ├── balatro/       # Balatro game section
│   └── legal/         # Privacy, Terms, About, Contact
├── data/balatro/      # YAML data files (auto-updated daily)
├── layouts/           # Hugo templates
│   ├── partials/      # Nav, sidebar, FAQ render, footer
│   └── shortcodes/    # Calculator, tool-card
├── assets/            # CSS, JS (processed by Hugo Pipes)
├── .github/workflows/ # CI/CD
│   ├── daily-data-update.yml  # Daily data refresh
│   └── hugo-build-deploy.yml # Build & deploy
├── scripts/           # Python data generator
└── hugo.toml          # Hugo config
```

## Daily Auto-Update Architecture

1. **GitHub Action** runs at 06:00 UTC daily
2. **Python script** fetches community issues, extracts facts, generates YAML
3. **Script commits** new YAML to `data/balatro/`
4. **Hugo rebuilds** automatically on push
5. **Cloudflare Pages** deploys the new static site

## Content Separation

| Type | Location | Update Frequency |
|------|----------|-----------------|
| Static (lore, tutorial) | `content/balatro/static/` | Monthly |
| Dynamic (bugs, FAQ, patches) | `data/balatro/*.yaml` | Daily (auto) |

## AdSense Setup

1. Add your AdSense client ID to `hugo.toml`:
   ```toml
   [params]
     adsenseClient = "ca-pub-XXXXXXXXXXXXXXXX"
   ```
2. Ad slots are injected via `layouts/partials/ads-inject.html`

## Deploy

Connect your GitHub repo to Cloudflare Pages / Netlify / GitHub Pages. Build command: `hugo --minify`. Output directory: `public`.

## Contact

39918849@qq.com
