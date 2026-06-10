// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

// Hosted on GitHub Pages behind the custom domain getreadlater.com
// (see public/CNAME). Custom domain means no `base` path is needed.
export default defineConfig({
  site: 'https://getreadlater.com',
  trailingSlash: 'ignore',
  integrations: [tailwind({ applyBaseStyles: false })],
});
