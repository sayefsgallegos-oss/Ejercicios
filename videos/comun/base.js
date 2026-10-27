// Utilidades de dibujo compartidas por los videos de Lu.
// Cada escena define render(T) y DURATION, y usa estas funciones.
const cv = document.getElementById('cv'), g = cv.getContext('2d');
const FONT = 'Inter, "Noto Color Emoji", sans-serif';
const C = {
  bg: '#f6f1e7', card: '#ffffff', line: '#e6dfd2', ink: '#1f2937', soft: '#6b7280',
  grid: '#e4ded3', gridNeg: '#f0ece5', axis: '#374151',
  p1: '#2563eb', p2: '#9333ea', p3: '#059669', cut: '#dc2626', hi: '#f59e0b', hiInk: '#b45309'
};

// ---------- tiempo ----------
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const ease = x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
const lin = (T, a, b) => clamp((T - a) / (b - a));
const P = (T, a, b) => ease(lin(T, a, b));
const win = (T, a, b, f = .4) => P(T, a, a + f) * (1 - P(T, b - f, b));
const pop = (T, a) => { const x = lin(T, a, a + .45); return x <= 0 ? 0 : x >= 1 ? 1 : ease(x) * (1 + .3 * Math.sin(x * Math.PI)); };
const fallDy = (T, t0) => { const p = lin(T, t0, t0 + 1.6); return { dy: p * p * 520, alpha: 1 - p, gone: p >= 1 }; };
function hexA(h, a) { const n = parseInt(h.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; }
// devuelve el último elemento de una lista [[t, ...], ...] cuyo t ya pasó
function current(list, T) { let i = -1; list.forEach((e, k) => { if (e[0] <= T) i = k; }); return i < 0 ? null : list[i]; }

// ---------- texto y cajas ----------
function txt(s, x, y, size, col, o = {}) {
  g.save(); g.globalAlpha *= (o.alpha ?? 1);
  g.font = `${o.w || 500} ${size}px ${FONT}`; g.fillStyle = col;
  g.textAlign = o.align || 'left'; g.textBaseline = o.base || 'middle';
  g.fillText(s, x, y); const w = g.measureText(s).width; g.restore(); return w;
}
function tw(s, size, w = 500) { g.save(); g.font = `${w} ${size}px ${FONT}`; const r = g.measureText(s).width; g.restore(); return r; }
function rr(x, y, w, h, r, fill, stroke, lw = 2, alpha = 1) {
  g.save(); g.globalAlpha *= alpha; g.beginPath(); g.roundRect(x, y, w, h, r);
  if (fill) { g.fillStyle = fill; g.fill(); }
  if (stroke) { g.strokeStyle = stroke; g.lineWidth = lw; g.stroke(); }
  g.restore();
}
function wrap(s, size, w, maxW) {
  const out = [];
  for (const para of s.split('\n')) {
    let line = '';
    for (const word of para.split(' ')) {
      const t = line ? line + ' ' + word : word;
      if (tw(t, size, w) > maxW && line) { out.push(line); line = word; } else line = t;
    }
    out.push(line);
  }
  return out;
}
function label(s, x, y, col, o = {}) {
  const size = o.size || 28, w = tw(s, size, 700) + 22;
  const ax = o.align === 'right' ? x - w : o.align === 'center' ? x - w / 2 : x;
  rr(ax, y - size * .75, w, size * 1.5, 10, '#fff', col, 3, o.alpha ?? 1);
  txt(s, ax + 11, y + 1, size, col, { w: 700, alpha: o.alpha ?? 1 });
}
function arrow(x1, y1, x2, y2, col, lw = 5, alpha = 1) {
  g.save(); g.globalAlpha *= alpha; g.strokeStyle = col; g.fillStyle = col; g.lineWidth = lw; g.lineCap = 'round';
  g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke();
  const a = Math.atan2(y2 - y1, x2 - x1), h = 18;
  g.beginPath(); g.moveTo(x2 + Math.cos(a) * 4, y2 + Math.sin(a) * 4);
  g.lineTo(x2 - h * Math.cos(a - .45), y2 - h * Math.sin(a - .45));
  g.lineTo(x2 - h * Math.cos(a + .45), y2 - h * Math.sin(a + .45)); g.closePath(); g.fill();
  g.restore();
}

// nota amarilla con texto que cambia según NOTAS = [[t, texto], ...]
function noteCard(T, notas, x, y, w, h, size = 38) {
  rr(x, y, w, h, 22, '#fffbeb', '#fcd34d', 2);
  const n = current(notas, T); if (!n) return;
  const al = P(T, n[0], n[0] + .35);
  const lines = wrap(n[1], size, 700, w - 56), lh = size * 1.3;
  const y0 = y + h / 2 - (lines.length - 1) * lh / 2;
  lines.forEach((l, k) => txt(l, x + 28, y0 + k * lh + (1 - al) * 12, size, C.ink, { w: 700, alpha: al }));
}

// ---------- plano cartesiano ----------
function makePlane(o) {
  const pl = Object.assign({}, o);
  pl.X = t => o.x0 + (t - o.xmin) / (o.xmax - o.xmin) * (o.x1 - o.x0);
  pl.Y = f => o.y1 - (f - o.ymin) / (o.ymax - o.ymin) * (o.y1 - o.y0);
  pl.clip = () => { g.beginPath(); g.rect(o.x0, o.y0, o.x1 - o.x0, o.y1 - o.y0); g.clip(); };
  return pl;
}
function curve(pl, fn, t0, t1, col, lw, o = {}) {
  if (t1 <= t0) return;
  g.save(); g.globalAlpha *= (o.alpha ?? 1);
  g.strokeStyle = col; g.lineWidth = lw; g.lineCap = 'round'; g.lineJoin = 'round';
  if (o.dash) g.setLineDash(o.dash);
  g.beginPath();
  const n = Math.max(2, Math.ceil((t1 - t0) * 60));
  for (let i = 0; i <= n; i++) {
    const t = t0 + (t1 - t0) * i / n, y = pl.Y(fn(t)) + (o.dy || 0);
    i ? g.lineTo(pl.X(t), y) : g.moveTo(pl.X(t), y);
  }
  g.stroke(); g.restore();
}
function dot(pl, t, f, col, o = {}) {
  const s = o.scale ?? 1; if (s <= 0) return;
  g.save(); g.globalAlpha *= (o.alpha ?? 1);
  const x = pl.X(t), y = pl.Y(f) + (o.dy || 0), r = (o.r || 12) * s;
  g.beginPath(); g.arc(x, y, r, 0, 7);
  g.fillStyle = o.hollow ? '#fff' : col; g.fill();
  g.lineWidth = o.hollow ? 5 : 4; g.strokeStyle = o.hollow ? col : '#fff'; g.stroke();
  g.restore();
}
function dashLine(x1, y1, x2, y2, col, alpha = 1, lw = 3) {
  g.save(); g.globalAlpha *= alpha; g.strokeStyle = col; g.lineWidth = lw; g.setLineDash([10, 9]);
  g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke(); g.restore();
}

// ---------- tijeras y cortes ----------
function scissors(x, y, open, alpha) {
  if (alpha <= 0) return;
  g.save(); g.globalAlpha *= alpha; g.translate(x, y); g.scale(1.25, 1.25);
  const L = 44, H = 30;
  for (const s of [-1, 1]) {
    const tx = s * Math.sin(open) * L, ty = Math.cos(open) * L;
    const hx = -s * Math.sin(open) * H, hy = -Math.cos(open) * H;
    g.strokeStyle = '#475569'; g.lineWidth = 7; g.lineCap = 'round';
    g.beginPath(); g.moveTo(hx, hy); g.lineTo(tx, ty); g.stroke();
    const k = 1 + 15 / H;
    g.strokeStyle = C.cut; g.lineWidth = 6;
    g.beginPath(); g.arc(hx * k, hy * k, 13, 0, 7); g.stroke();
  }
  g.fillStyle = '#1f2937'; g.beginPath(); g.arc(0, 0, 4.5, 0, 7); g.fill();
  g.restore();
}
// corte k = {c, g0, s0, s1, end}: línea vertical en x = c y tijeras que bajan
function drawCut(pl, T, k, name = 'x', labelY = pl.y1 - 26) {
  if (T < k.g0 || T > k.end + .6) return;
  const fade = 1 - P(T, k.end, k.end + .6);
  const grow = P(T, k.g0, k.g0 + .8);
  const yTop = pl.y0, yBot = pl.y1, yEnd = yTop + (yBot - yTop) * grow;
  const sp = lin(T, k.s0, k.s1), ys = yTop + (yBot - yTop) * sp, X = pl.X(k.c);
  g.save(); g.globalAlpha = fade;
  g.strokeStyle = C.cut; g.lineWidth = 4; g.setLineDash([14, 10]);
  g.beginPath(); g.moveTo(X, yTop); g.lineTo(X, yEnd); g.stroke();
  if (sp > 0) { g.setLineDash([]); g.lineWidth = 5; g.beginPath(); g.moveTo(X, yTop); g.lineTo(X, ys); g.stroke(); }
  g.restore();
  label(`✂ ${name} = ${k.c}`, X, labelY, C.cut, { size: 24, align: 'center', alpha: fade * P(T, k.g0, k.g0 + .5) });
  const sa = P(T, k.g0 + .4, k.g0 + .9) * (1 - P(T, k.s1, k.s1 + .5)) * fade;
  const open = sp > 0 && sp < 1 ? .08 + .38 * Math.abs(Math.sin((T - k.s0) * 9)) : .4;
  scissors(X, sp > 0 ? ys : yTop + 70, open, sa);
}

// ---------- arranque ----------
window.ready = false;
window.addEventListener('load', () => {
  Promise.all(['500', '600', '700', '800'].map(w => document.fonts.load(`${w} 40px Inter`)).concat(document.fonts.load('40px "Noto Color Emoji"', '📸')))
    .then(() => { render(0); window.ready = true; });
});
