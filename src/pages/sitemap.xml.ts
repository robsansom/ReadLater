import type { APIRoute } from 'astro';

const locales = ['', 'fr', 'es', 'de', 'ja'];
const pages = ['', 'support', 'privacy', 'terms'];

export const GET: APIRoute = ({ site }) => {
  const urls = pages.flatMap((page) =>
    locales.map((locale) => {
      const path = [locale, page].filter(Boolean).join('/');
      return new URL(path ? `/${path}/` : '/', site).href;
    }),
  );

  return new Response(`<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((url) => `  <url><loc>${url}</loc></url>`).join('\n')}
</urlset>
`, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
};
