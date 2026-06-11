// Temporary receiver: the Figma desktop plugin POSTs exported PNG bytes
// here so we can save them to disk without manual exports.
import { createServer } from 'node:http';
import { writeFileSync, mkdirSync } from 'node:fs';
import { join, basename } from 'node:path';

const outDir = new URL('./figma-exports/', import.meta.url).pathname;
mkdirSync(outDir, { recursive: true });

const server = createServer((req, res) => {
  if (req.method !== 'POST') {
    res.writeHead(405).end();
    return;
  }
  const name = basename(new URL(req.url, 'http://x').searchParams.get('name') ?? 'export.png');
  const chunks = [];
  req.on('data', (c) => chunks.push(c));
  req.on('end', () => {
    const file = join(outDir, name);
    writeFileSync(file, Buffer.concat(chunks));
    console.log('saved', file, Buffer.concat(chunks).length, 'bytes');
    res.writeHead(200, { 'Access-Control-Allow-Origin': '*' }).end('ok');
  });
});

server.listen(9230, () => console.log('receiver listening on 9230'));
