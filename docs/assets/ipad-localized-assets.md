# Localized iPad Website Assets

These assets power the localized iPad section on the landing page.

## Website locations

- public/images/ipad/fr/ipad-collections-dark.{png,webp}
- public/images/ipad/fr/ipad-collections-light.{png,webp}
- public/images/ipad/de/ipad-collections-dark.{png,webp}
- public/images/ipad/de/ipad-collections-light.{png,webp}
- public/images/ipad/es/ipad-collections-dark.{png,webp}
- public/images/ipad/es/ipad-collections-light.{png,webp}
- public/images/ipad/ja/ipad-collections-dark.{png,webp}
- public/images/ipad/ja/ipad-collections-light.{png,webp}

English still uses the existing framed site assets:

- public/images/ipad-dark.{png,webp}
- public/images/ipad-light.{png,webp}

The untouched 2064 x 2752 simulator captures are stored in:

- source-assets/ipad/<locale>/ipad-collections-{dark,light}.png

The deployable images include the same device surround as the English assets.
Regenerate all framed PNG and WebP files from the website repo with:

```sh
python3 scripts/frame_ipad_assets.py --repo .
```

The script uses `public/images/ipad-dark.png` and `public/images/ipad-light.png`
as the frame templates, so future captures keep the website's established bezel.

## Source capture

Transferred from the app repo capture folder:

/Users/MummyDaddy/My Projects/Code Projects/Pouch3/Docs/WebsiteLocalizedCaptures/

Captured on iPad Pro 13-inch (M5), simulator UDID B6F477D1-8182-4754-B0F2-7910A76B6CFE, using the debug showcase seed packs:

- --reset-seed-data --seed-showcase --seed-showcase-lang=fr
- --reset-seed-data --seed-showcase --seed-showcase-lang=de
- --reset-seed-data --seed-showcase --seed-showcase-lang=es
- --reset-seed-data --seed-showcase --seed-showcase-lang=ja

For dark captures, the app Appearance setting was left on Auto (selectedAppTheme=system) and the simulator appearance was set to dark before relaunching. For light captures, the simulator appearance was set to light.

All source captures are 2064 x 2752. The framed website outputs are 1351 x 1761,
with WebP copies generated at quality 92.

## Visual QA

See docs/assets/ipad-localized-contact-sheet.png for the reviewed contact sheet.

## Code path

src/components/pages/IndexPage.astro maps Astro.currentLocale to the locale-specific public/images/ipad/<locale>/ipad-collections-* files. The default English page keeps the existing ipad-dark and ipad-light assets.
