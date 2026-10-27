// Uso: node render.js <carpeta> frames <seg...>   → JPG de prueba en <carpeta>/cuadros
//      node render.js <carpeta> video salida.mp4 [fps]
// La carpeta debe tener escena.html que define render(T) y DURATION.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path'), fs = require('fs');
(async () => {
  const [dir, mode, ...args] = process.argv.slice(2);
  const base = path.resolve(dir);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.error('ERR', e.message));
  await p.goto('file://' + path.join(base, 'escena.html'));
  await p.waitForFunction(() => window.ready === true);
  const frame = (t, q) => p.evaluate(([t, q]) => { render(t); return cv.toDataURL('image/jpeg', q); }, [t, q]);
  if (mode === 'frames') {
    fs.mkdirSync(path.join(base, 'cuadros'), { recursive: true });
    for (const t of args) fs.writeFileSync(path.join(base, 'cuadros', `t${t}.jpg`), Buffer.from((await frame(+t, .85)).split(',')[1], 'base64'));
  } else {
    const out = path.resolve(args[0]), fps = +(args[1] || 30);
    const D = await p.evaluate(() => DURATION), N = Math.ceil(D * fps);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < N; i++) {
      const buf = Buffer.from((await frame(i / fps, .93)).split(',')[1], 'base64');
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 900 === 0) console.log(`${i}/${N}`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await b.close();
})();
