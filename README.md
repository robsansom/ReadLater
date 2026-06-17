# Pouch — Landing Site

The marketing landing page for **Pouch — Find Later**, the privacy-first iOS app for saving links and organising them into collections.

Built with [Astro](https://astro.build) + [Tailwind CSS](https://tailwindcss.com), styled to mirror the App Store screenshots, and deployed via GitHub Pages.

## Pages

- `/` — landing (hero + alternating dark/light feature panels + feature grid + pricing)
- `/privacy` — Privacy Policy (Apple submission ready)
- `/support` — Support / FAQ / contact
- `/terms` — Terms of Use

## Local development

```bash
npm install
npm run dev          # http://localhost:4321
npm run build        # static output to ./dist
npm run preview      # preview the build
```

Requires Node 18.17.1+ (Node 20 / 22 recommended).

## Deploying to GitHub Pages

A workflow lives at [`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml). It uses the official [`withastro/action`](https://github.com/withastro/action) to build the site and `actions/deploy-pages` to publish on every push to `main`.

To enable Pages for the repo once it is on GitHub:

1. Go to **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. Push to `main`. The workflow will build and deploy.

### Adjust `astro.config.mjs` for your URL

Open [`astro.config.mjs`](./astro.config.mjs) and set the `site` value:

- **Project page** (e.g. `https://<username>.github.io/Pouch3-Website`):
  ```js
  site: 'https://<username>.github.io',
  base: '/Pouch3-Website',
  ```
- **User or organisation page** (`https://<username>.github.io`):
  ```js
  site: 'https://<username>.github.io',
  // leave `base` commented out
  ```
- **Custom domain** (e.g. `https://pouchapp.com`):
  ```js
  site: 'https://pouchapp.com',
  ```
  Also create `public/CNAME` containing your custom domain (one line, no protocol).

All asset URLs in the site already respect `import.meta.env.BASE_URL`, so they work in all three scenarios.

## Placeholders to update before submission

Search the codebase for the strings below and replace them.

| Placeholder                  | Where                                    | What to set it to                                      |
| ---------------------------- | ---------------------------------------- | ------------------------------------------------------ |
| `#app-store`                 | Hero, Pricing, Header, Footer            | Your App Store URL once the app is approved           |
| `support@pouchapp.example`   | Footer, Privacy, Support, Terms          | Your real support email                                |
| `https://example.github.io`  | `astro.config.mjs`                       | Your final GH Pages or custom-domain URL              |

## Project structure

```
src/
  layouts/Base.astro
  components/
    Header.astro
    Hero.astro
    FeaturePanel.astro
    FeatureGrid.astro
    Pricing.astro
    Footer.astro
  pages/
    index.astro
    privacy.astro
    support.astro
    terms.astro
  styles/global.css
public/
  images/        # iPhone + iPad screenshots, app icon
  favicon.png
```

## Visual system

- Brand red: `#FA3454` (matches the iOS app's `AccentColor`)
- Dark surface: `#0B0B0F`
- Light surface: `#F6F8F9` → `#E6EBEF`
- Peach gradient halos behind device frames (see `peach-halo` and `light-halo` in `src/styles/global.css`)
- Typeface: [Inter](https://rsms.me/inter) — closest free web equivalent to the SF Pro Display look used in the App Store screenshots
- Alternating full-bleed dark/light panels, each with a single bold headline and a single device screenshot — mirrors the App Store screenshot grid one-for-one

## Assets

The iPhone and iPad screenshots in `public/images/` are copies of the final App Store screenshots that live in the sibling `Pouch3` Xcode project. The originals were not moved or modified. If you replace any screenshot here, the corresponding panel on the landing page will pick it up automatically.

## Licence

Source code in this repository is intended for use as the Pouch marketing site. App imagery and the Pouch name and logo are the property of the Pouch app authors.
