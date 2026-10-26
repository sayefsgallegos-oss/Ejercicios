// Video: función por partes como un collage (Lu · Matemática Básica)
// render(T) dibuja el cuadro del segundo T. Los tiempos salen del .srt del audio.
const cv = document.getElementById('cv'), g = cv.getContext('2d');
const DURATION = 346;
const FONT = 'Inter, "Noto Color Emoji", sans-serif';
const C = {
  bg: '#f6f1e7', card: '#ffffff', line: '#e6dfd2', ink: '#1f2937', soft: '#6b7280',
  grid: '#e4ded3', gridNeg: '#f0ece5', axis: '#374151',
  p1: '#2563eb', p2: '#9333ea', p3: '#059669', cut: '#dc2626', hi: '#f59e0b', sub: 'rgba(31,41,55,.9)'
};

// ---------- utilidades ----------
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const ease = x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
const lin = (T, a, b) => clamp((T - a) / (b - a));
const P = (T, a, b) => ease(lin(T, a, b));
const win = (T, a, b, f = .4) => P(T, a, a + f) * (1 - P(T, b - f, b));
const pop = (T, a) => { const x = lin(T, a, a + .45); return x <= 0 ? 0 : x >= 1 ? 1 : ease(x) * (1 + .3 * Math.sin(x * Math.PI)); };
function hexA(h, a) { const n = parseInt(h.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; }

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

// ---------- plano ----------
const PL = { x0: 110, x1: 1170, y0: 70, y1: 890 };
const xmin = -4, xmax = 12.4, ymin = -4.5, ymax = 23;
const X = t => PL.x0 + (t - xmin) / (xmax - xmin) * (PL.x1 - PL.x0);
const Y = f => PL.y1 - (f - ymin) / (ymax - ymin) * (PL.y1 - PL.y0);

function curve(fn, t0, t1, col, lw, o = {}) {
  if (t1 <= t0) return;
  g.save(); g.globalAlpha *= (o.alpha ?? 1);
  g.strokeStyle = col; g.lineWidth = lw; g.lineCap = 'round'; g.lineJoin = 'round';
  if (o.dash) g.setLineDash(o.dash);
  g.beginPath();
  const n = Math.max(2, Math.ceil((t1 - t0) * 40));
  for (let i = 0; i <= n; i++) {
    const t = t0 + (t1 - t0) * i / n, y = Y(fn(t)) + (o.dy || 0);
    i ? g.lineTo(X(t), y) : g.moveTo(X(t), y);
  }
  g.stroke(); g.restore();
}
function dot(t, f, col, o = {}) {
  const s = o.scale ?? 1; if (s <= 0) return;
  g.save(); g.globalAlpha *= (o.alpha ?? 1);
  const x = X(t), y = Y(f) + (o.dy || 0), r = (o.r || 11) * s;
  g.beginPath(); g.arc(x, y, r, 0, 7);
  g.fillStyle = o.hollow ? '#fff' : col; g.fill();
  g.lineWidth = 4; g.strokeStyle = o.hollow ? col : '#fff'; g.stroke();
  if (o.hollow) { g.beginPath(); g.arc(x, y, r, 0, 7); g.strokeStyle = col; g.stroke(); }
  g.restore();
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
function vdash(t, f0, f1, col, alpha = 1, lw = 3) {
  g.save(); g.globalAlpha *= alpha; g.strokeStyle = col; g.lineWidth = lw; g.setLineDash([10, 9]);
  g.beginPath(); g.moveTo(X(t), Y(f0)); g.lineTo(X(t), Y(f1)); g.stroke(); g.restore();
}
function hdash(f, t0, t1, col, alpha = 1, lw = 3) {
  g.save(); g.globalAlpha *= alpha; g.strokeStyle = col; g.lineWidth = lw; g.setLineDash([10, 9]);
  g.beginPath(); g.moveTo(X(t0), Y(f)); g.lineTo(X(t1), Y(f)); g.stroke(); g.restore();
}

function drawPlane(T) {
  rr(40, 40, 1160, 880, 26, C.card, C.line, 2);
  g.save(); g.beginPath(); g.rect(PL.x0, PL.y0, PL.x1 - PL.x0, PL.y1 - PL.y0); g.clip();
  // zona negativa más clara (fuera del plano del examen)
  g.fillStyle = '#faf8f4';
  g.fillRect(PL.x0, PL.y0, X(0) - PL.x0, PL.y1 - PL.y0);
  g.fillRect(X(0), Y(0), PL.x1 - X(0), PL.y1 - Y(0));
  g.lineWidth = 1.5;
  for (let t = -4; t <= 12; t++) { g.strokeStyle = t < 0 ? C.gridNeg : C.grid; g.beginPath(); g.moveTo(X(t), PL.y0); g.lineTo(X(t), PL.y1); g.stroke(); }
  for (let f = -3; f <= 21; f += 3) { g.strokeStyle = f < 0 ? C.gridNeg : C.grid; g.beginPath(); g.moveTo(PL.x0, Y(f)); g.lineTo(PL.x1, Y(f)); g.stroke(); }
  g.restore();
  // ejes
  arrow(PL.x0, Y(0), PL.x1 + 12, Y(0), C.axis, 3);
  arrow(X(0), PL.y1, X(0), PL.y0 - 14, C.axis, 3);
  for (let t = 1; t <= 11; t++) txt(String(t), X(t), Y(0) + 26, 22, C.soft, { align: 'center', w: 600 });
  for (let f = 3; f <= 21; f += 3) txt(String(f), X(0) - 12, Y(f), 22, C.soft, { align: 'right', w: 600 });
  txt('0', X(0) - 12, Y(0) + 22, 22, C.soft, { align: 'right', w: 600 });
  // nombres de ejes
  const hl = win(T, 296, 304) * (.6 + .4 * Math.sin(T * 6));
  const n1 = 't: Tiempo (min)', n2 = 'f(t): Distancia (km)';
  const w1 = tw(n1, 26, 700), w2 = tw(n2, 26, 700);
  const x1 = PL.x1 - w1 - 6, y1 = Y(0) + 62, x2 = X(0) + 16, y2 = PL.y0 + 6;
  if (hl > 0) { rr(x1 - 10, y1 - 22, w1 + 20, 44, 10, hexA(C.hi, .35 * hl), C.hi, 3, hl); rr(x2 - 10, y2 - 22, w2 + 20, 44, 10, hexA(C.hi, .35 * hl), C.hi, 3, hl); }
  txt(n1, x1, y1, 26, C.ink, { w: 700 });
  txt(n2, x2, y2, 26, C.ink, { w: 700 });
}

// ---------- tijeras ----------
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
// un corte: línea vertical en c, tijeras que bajan, y se borra al final
function drawCut(T, k) {
  if (T < k.g0 || T > k.end + .6) return;
  const fade = 1 - P(T, k.end, k.end + .6);
  const grow = P(T, k.g0, k.g0 + .8);
  const yTop = PL.y0, yBot = PL.y1, yEnd = yTop + (yBot - yTop) * grow;
  const sp = lin(T, k.s0, k.s1), ys = yTop + (yBot - yTop) * sp;
  g.save(); g.globalAlpha = fade;
  g.strokeStyle = C.cut; g.lineWidth = 4; g.setLineDash([14, 10]);
  g.beginPath(); g.moveTo(X(k.c), yTop); g.lineTo(X(k.c), yEnd); g.stroke();
  if (sp > 0) { g.setLineDash([]); g.lineWidth = 5; g.beginPath(); g.moveTo(X(k.c), yTop); g.lineTo(X(k.c), ys); g.stroke(); }
  g.restore();
  label('✂ t = ' + k.c, X(k.c), PL.y1 - 26, C.cut, { size: 24, align: 'center', alpha: fade * P(T, k.g0, k.g0 + .5) });
  const sa = P(T, k.g0 + .4, k.g0 + .9) * (1 - P(T, k.s1, k.s1 + .5)) * fade;
  const open = sp > 0 && sp < 1 ? .08 + .38 * Math.abs(Math.sin((T - k.s0) * 9)) : .4;
  scissors(X(k.c), sp > 0 ? ys : yTop + 70, open, sa);
}

// ---------- las tres partes ----------
const parab = T => {
  const h = 2 * P(T, 190.7, 194.5), v = 6 * P(T, 202.5, 205.5), k = 1 - P(T, 213, 218.5) / 3;
  return t => k * (t - h) ** 2 + v;
};
const PIEZAS = [
  { col: C.p1, fn: () => t => 3 * t, a: 0, b: 2, draw: [100.7, 103.9], fallA: 131.2, fallB: 141.2, glow: 147.2, join: 150.2 },
  { col: C.p2, fn: parab, a: 2, b: 5, draw: [181.2, 183.6], fallA: 239.2, fallB: 239.2, glow: 236, join: 244.6 },
  { col: C.p3, fn: () => t => 1.5 * t + 4.5, a: 5, b: 11, draw: [274.5, 276.3], fallA: 282.0, fallB: 282.0, glow: 281.9, join: 283.5 },
];
const CORTES = [
  { c: 0, g0: 122.2, s0: 127, s1: 130.5, end: 136 },
  { c: 2, g0: 138.1, s0: 139, s1: 140.8, end: 146 },
  { c: 2, g0: 230.3, s0: 231.2, s1: 233.6, end: 243.5 },
  { c: 5, g0: 234.5, s0: 235.5, s1: 238.6, end: 243.5 },
  { c: 5, g0: 278.6, s0: 279.2, s1: 280.4, end: 285 },
  { c: 11, g0: 280.2, s0: 280.6, s1: 281.8, end: 285 },
];
const fallDy = (T, t0) => { const p = lin(T, t0, t0 + 1.6); return { dy: p * p * 520, alpha: 1 - p, gone: p >= 1 }; };

function collageAlpha(T) {
  const dim = (a, b) => P(T, a, a + .6) * (1 - P(T, b, b + .6));
  return 1 - .7 * Math.max(dim(157.5, 244.6), dim(247.7, 283.5));
}

function drawPieces(T) {
  g.save(); g.beginPath(); g.rect(PL.x0, PL.y0, PL.x1 - PL.x0, PL.y1 - PL.y0); g.clip();
  const ca = collageAlpha(T);
  for (const p of PIEZAS) {
    if (T < p.draw[0]) continue;
    const f = p.fn(T), xEnd = xmin + (xmax - xmin) * lin(T, p.draw[0], p.draw[1]);
    if (T >= p.join) {
      const pulse = 1 - P(T, p.join, p.join + 1.5);
      if (pulse > 0) curve(f, p.a, p.b, p.col, 30, { alpha: .3 * pulse });
      curve(f, p.a, p.b, '#fff', 13, { alpha: ca });
      curve(f, p.a, p.b, p.col, 8, { alpha: ca });
      continue;
    }
    // brillo de "me quedo con lo del medio"
    const gl = P(T, p.glow, p.glow + .5);
    if (gl > 0) curve(f, p.a, p.b, p.col, 24, { alpha: .22 * gl });
    curve(f, Math.max(p.a, xmin), Math.min(p.b, xEnd), p.col, 6);
    for (const [s0, s1, ft] of [[xmin, p.a, p.fallA], [p.b, xmax, p.fallB]]) {
      const fd = T >= ft ? fallDy(T, ft) : { dy: 0, alpha: 1 };
      if (fd.gone) continue;
      curve(f, s0, Math.min(s1, xEnd), p.col, 6, { dy: fd.dy, alpha: fd.alpha });
    }
  }
  g.restore();
}

// franjas "solo me importa"
const FRANJAS = [[0, 2, C.p1, 108.3, 150.2], [2, 5, C.p2, 225.6, 244.6], [5, 11, C.p3, 274.5, 283.5]];
function drawStrips(T) {
  for (const [a, b, col, t0, t1] of FRANJAS) {
    const al = win(T, t0, t1, .5); if (al <= 0) continue;
    g.save(); g.globalAlpha = al; g.fillStyle = hexA(col, .09);
    g.fillRect(X(a), PL.y0, X(b) - X(a), PL.y1 - PL.y0);
    g.fillStyle = hexA(col, .55); g.fillRect(X(a), Y(0) - 5, X(b) - X(a), 10);
    g.restore();
  }
}

// puntos de la tabulación
function tabPoint(T, t, f, col, at, gone, lab, fallAt) {
  if (T < at || T > gone + .5) return;
  let al = 1 - P(T, gone, gone + .5), dy = 0;
  if (fallAt && T >= fallAt) { const fd = fallDy(T, fallAt); al *= fd.alpha; dy = fd.dy; }
  const pr = P(T, at, at + .8);
  g.save(); g.globalAlpha = al;
  g.strokeStyle = hexA(col, .7); g.lineWidth = 3; g.setLineDash([8, 8]);
  g.beginPath(); g.moveTo(X(t), Y(0) + dy); g.lineTo(X(t), Y(0) + (Y(f) - Y(0)) * pr + dy); g.stroke();
  g.beginPath(); g.moveTo(X(0), Y(f) + dy); g.lineTo(X(0) + (X(t) - X(0)) * pr, Y(f) + dy); g.stroke();
  g.restore();
  dot(t, f, col, { scale: pop(T, at + .5), alpha: al, dy, r: 12 });
  if (T > at + .7) label(lab, X(t) + 22, Y(f) + 30 + dy, col, { size: 24, alpha: al * P(T, at + .7, at + 1.1) });
}

// la parábola: original fantasma, vértice y flechas
function drawParabolaHelpers(T) {
  const ghost = win(T, 190.7, 225.6, .6);
  if (ghost > 0) curve(t => t * t, -4, 4.5, C.p2, 3, { alpha: .45 * ghost, dash: [10, 10] });
  const g2 = win(T, 213, 225.6, .6);
  if (g2 > 0) curve(t => (t - 2) ** 2 + 6, -1, 5, C.p2, 3, { alpha: .45 * g2, dash: [6, 8] });
  if (T >= 181.2 && T < 229) {
    const h = 2 * P(T, 190.7, 194.5), v = 6 * P(T, 202.5, 205.5), al = 1 - P(T, 228, 229);
    dot(h, v, C.p2, { scale: pop(T, 182), alpha: al, r: 12 });
    const L = [['(0; 0)', 182.5, 190.7], ['(2; 0)', 194.8, 202.5], ['(2; 6)', 205.8, 228.5]];
    for (const [s, a, b] of L) { const w = win(T, a, b); if (w > 0) label(s, X(h) + 36, Y(v) - 34, C.p2, { size: 26, alpha: w }); }
  }
  const a1 = win(T, 190.7, 202.5, .5);
  if (a1 > 0) { arrow(X(0), Y(-2.6), X(2), Y(-2.6), C.p2, 5, a1); label('2 a la derecha', X(2) + 18, Y(-2.6), C.p2, { size: 24, alpha: a1 }); }
  const a2 = win(T, 202.5, 213, .5);
  if (a2 > 0) { arrow(X(2) + 40, Y(0), X(2) + 40, Y(6), C.p2, 5, a2); label('6 arriba', X(2) + 60, Y(3), C.p2, { size: 24, alpha: a2 }); }
  const a3 = win(T, 213, 225.6, .5);
  if (a3 > 0) label('× 2/3: se achata', X(5.3), Y(16), C.p2, { size: 24, alpha: a3 });
}

// vista previa del collage (intro)
function drawPreview(T) {
  const out = 1 - P(T, 33.2, 34.2);
  const fs = [t => 3 * t, t => 2 / 3 * (t - 2) ** 2 + 6, t => 1.5 * t + 4.5];
  [[0, 2, C.p1, 25.1], [2, 5, C.p2, 26.5], [5, 11, C.p3, 28.7]].forEach(([a, b, col, at], i) => {
    const al = P(T, at, at + .6) * out; if (al <= 0) return;
    curve(fs[i], a, b, col, 7, { alpha: .55 * al, dash: [12, 10] });
    const m = (a + b) / 2;
    label(String(i + 1), X(m) - 50, Y(fs[i](m)) - 10, col, { size: 26, alpha: al });
  });
}

// preguntas sobre la gráfica
function drawQuestions(T) {
  // P1: triángulos de pendiente y sombra [0; 2]
  const q1 = win(T, 307, 320, .5);
  if (q1 > 0) {
    curve(t => 3 * t, 0, 2, C.p1, 26, { alpha: .25 * q1 });
    for (const [t0, at] of [[0, 307], [1, 308.2]]) {
      const al = q1 * P(T, at, at + .5); if (al <= 0) continue;
      g.save(); g.globalAlpha = al; g.strokeStyle = C.hi; g.lineWidth = 4;
      g.beginPath(); g.moveTo(X(t0), Y(3 * t0)); g.lineTo(X(t0 + 1), Y(3 * t0)); g.lineTo(X(t0 + 1), Y(3 * t0 + 3)); g.stroke(); g.restore();
    }
    if (T > 308.5) {
      const al = q1 * P(T, 308.5, 309);
      label('+1 min', X(1.5), Y(3) + 28, '#b45309', { size: 22, align: 'center', alpha: al });
      label('+3 km', X(2) + 14, Y(4.5), '#b45309', { size: 22, alpha: al });
    }
  }
  const s1 = win(T, 314, 320, .5);
  if (s1 > 0) shadowOnAxis(0, 2, C.p1, s1, t => 3 * t);
  // P2: línea de 15 km, corte en t = 7 y sombra [7; 11]
  const q2 = win(T, 323, 346, .5);
  if (q2 > 0) {
    g.save(); g.globalAlpha = q2; g.strokeStyle = C.hi; g.lineWidth = 4; g.setLineDash([16, 10]);
    const xe = X(xmin) + (PL.x1 - X(xmin)) * P(T, 323, 324.5);
    g.beginPath(); g.moveTo(X(0), Y(15)); g.lineTo(Math.max(X(0), xe), Y(15)); g.stroke(); g.restore();
    label('15 km', X(0) - 14, Y(15), '#b45309', { size: 24, align: 'right', alpha: q2 });
    const gl = q2 * P(T, 326, 326.8);
    if (gl > 0) curve(t => 1.5 * t + 4.5, 7, 11, C.hi, 26, { alpha: .45 * gl });
    const d = q2 * P(T, 328, 328.6);
    if (d > 0) { vdash(7, 15, 15 - 15 * P(T, 328.3, 329.3), '#b45309', d, 4); dot(7, 15, C.hi, { scale: pop(T, 328), alpha: q2 }); label('(7; 15)', X(7) - 18, Y(15) - 38, '#b45309', { size: 24, align: 'right', alpha: d }); }
  }
  const s2 = win(T, 332, 346, .5);
  if (s2 > 0) shadowOnAxis(7, 11, C.hi, s2, t => 1.5 * t + 4.5);
}
function shadowOnAxis(a, b, col, al, f) {
  g.save(); g.globalAlpha = al; g.fillStyle = hexA(col, .14);
  g.beginPath(); g.moveTo(X(a), Y(f(a)));
  for (let i = 0; i <= 30; i++) { const t = a + (b - a) * i / 30; g.lineTo(X(t), Y(f(t))); }
  g.lineTo(X(b), Y(0)); g.lineTo(X(a), Y(0)); g.closePath(); g.fill();
  g.fillStyle = col; g.fillRect(X(a), Y(0) - 7, X(b) - X(a), 14); g.restore();
  dot(a, 0, col, { alpha: al, r: 12 }); dot(b, 0, col, { alpha: al, r: 12 });
}

// ---------- panel derecho ----------
const PX = 1230, PW = 650;
const ROWS = [
  { col: C.p1, dom: '0 ≤ t ≤ 2' },
  { col: C.p2, dom: '2 < t ≤ 5' },
  { col: C.p3, dom: '5 < t ≤ 11' },
];
function rowState(T, i) {
  // foco: [desde, hasta, fila]
  const F = [[34.4, 157.5, 0], [157.5, 247.7, 1], [247.7, 287.6, 2], [304, 320, 0], [320, 346, 2]];
  let focus = 0, dim = 0;
  for (const [a, b, r] of F) { const w = win(T, a, b, .4); if (r === i) focus = Math.max(focus, w); else dim = Math.max(dim, w * (a === 34.4 ? P(T, 36.9, 37.6) : 1)); }
  for (let k = 0; k < 3; k++) if (k === i) focus = Math.max(focus, win(T, 16.4 + k * 1.7, 16.4 + k * 1.7 + 1.9, .3));
  return { focus, alpha: 1 - .72 * dim * (1 - focus) };
}
const DOMHI = [[108.3, 152, 0], [225.6, 246, 1], [274.5, 285.7, 2]];
function formulaCard(T) {
  const y0 = 130, h = 270;
  rr(PX, y0, PW, h, 22, C.card, C.line, 2);
  txt('f(t) =', PX + 22, y0 + h / 2, 38, C.ink, { w: 700 });
  // llave
  const bx = PX + 150, top = y0 + 26, bot = y0 + h - 26, mid = (top + bot) / 2;
  g.save(); g.strokeStyle = C.ink; g.lineWidth = 4; g.lineCap = 'round'; g.beginPath();
  g.moveTo(bx + 16, top); g.quadraticCurveTo(bx, top, bx, top + 18); g.lineTo(bx, mid - 18);
  g.quadraticCurveTo(bx, mid, bx - 14, mid); g.quadraticCurveTo(bx, mid, bx, mid + 18);
  g.lineTo(bx, bot - 18); g.quadraticCurveTo(bx, bot, bx + 16, bot); g.stroke(); g.restore();
  const ex = PX + 186, dx = PX + 455;
  ROWS.forEach((r, i) => {
    const yc = y0 + 55 + i * 80, st = rowState(T, i);
    if (st.focus > 0) rr(ex - 14, yc - 34, PW - (ex - PX) + 2, 68, 14, hexA(r.col, .14 * st.focus), hexA(r.col, st.focus), 3);
    g.save(); g.globalAlpha = st.alpha;
    g.fillStyle = r.col; g.beginPath(); g.roundRect(ex - 14, yc - 26, 6, 52, 3); g.fill();
    if (i === 0) txt('3t', ex + 6, yc, 36, C.ink, { w: 600 });
    if (i === 1) {
      txt('2', ex + 18, yc - 17, 26, C.ink, { w: 600, align: 'center' });
      g.fillStyle = C.ink; g.fillRect(ex + 6, yc - 2, 24, 3);
      txt('3', ex + 18, yc + 17, 26, C.ink, { w: 600, align: 'center' });
      txt('(t − 2)² + 6', ex + 38, yc, 34, C.ink, { w: 600 });
    }
    if (i === 2) txt('1,5t + 4,5', ex + 6, yc, 34, C.ink, { w: 600 });
    let dh = 0; for (const [a, b, k] of DOMHI) if (k === i) dh = Math.max(dh, win(T, a, b, .4));
    const dw = tw(r.dom, 30, 600);
    if (dh > 0) rr(dx - 8, yc - 22, dw + 16, 44, 8, hexA(C.hi, .45 * dh));
    txt(r.dom, dx, yc, 30, dh > .5 ? C.ink : C.soft, { w: dh > .5 ? 800 : 600 });
    g.restore();
  });
}

const TILES = [['0 a 2', C.p1, 150.2], ['2 a 5', C.p2, 244.6], ['5 a 11', C.p3, 283.5]];
function collageTiles(T) {
  txt('Mi collage', PX + 4, 84, 30, C.ink, { w: 800 });
  const pulse = win(T, 22.6, 33.7) * (.5 + .5 * Math.sin(T * 5));
  TILES.forEach(([s, col, at], i) => {
    const x = PX + 205 + i * 150, y = 58, w = 136, h = 52;
    const on = P(T, at, at + .4), sc = T > at ? pop(T, at) : 1;
    g.save(); g.translate(x + w / 2, y + h / 2); g.scale(sc, sc); g.translate(-x - w / 2, -y - h / 2);
    g.save(); g.setLineDash(on > 0 ? [] : [8, 6]);
    rr(x, y, w, h, 12, on > 0 ? hexA(col, on) : (pulse > 0 ? hexA(col, .12 * pulse) : null), col, 3);
    g.restore();
    txt(s, x + w / 2, y + h / 2 + 1, 26, on > .5 ? '#fff' : col, { w: 700, align: 'center' });
    g.restore();
  });
}

const NOTAS = [
  [0, 'Hola Lu 👋\nHoy: graficar una función por partes'],
  [14.3, 'Esta función está partida en 3 pedazos'],
  [22.6, 'Es un collage 📸\n3 pedazos → 1 sola gráfica'],
  [34.4, 'Parte 1: f(t) = 3t\nPor ahora, olvida lo demás'],
  [45.7, '3t es una función lineal\n→ se grafica con una recta inclinada'],
  [49.6, '¿Por qué lineal?\nLa t no tiene exponente (ni ², ni ³)'],
  [58.8, 'Para graficarla: tabulamos'],
  [64.7, 'Invento 2 valores de t\ny hallo f(t)'],
  [95.9, 'Con 2 puntos ya puedo trazar la recta'],
  [104.1, '¡Así se grafica una función lineal!'],
  [108.3, 'Pero solo me importa\n0 ≤ t ≤ 2'],
  [117.3, '✂ Corto en t = 0\ny boto lo de la izquierda'],
  [136, '✂ Corto en t = 2\ny boto lo de la derecha'],
  [147.2, 'Me quedo con lo del medio\n→ ¡va al collage! 📌'],
  [155.8, '¡Listo! Siguiente 👉'],
  [157.5, 'Parte 2: función cuadrática\n→ es una parábola'],
  [177.7, 'Empiezo con la original: t²'],
  [185.7, '(t − 2): resta adentro\n→ 2 a la DERECHA'],
  [196.8, '+ 6: suma afuera\n→ 6 ARRIBA'],
  [208.3, '× 2/3: la achata un poquito\nla posición no cambia'],
  [225.6, 'Solo me importa\n2 < t ≤ 5'],
  [230.3, '✂ Corto en 2 y en 5\ny me quedo con lo del centro'],
  [244.6, '→ ¡va al collage! 📌'],
  [247.7, 'Parte 3: f(t) = 1,5t + 4,5\nTambién es lineal → tabulamos'],
  [274.5, 'Recta lista. Solo me importa\n5 < t ≤ 11'],
  [278.6, '✂ Corto en 5 y en 11'],
  [281.9, 'Me quedo con lo del centro\n→ ¡va al collage! 📌'],
  [287.6, '¡Collage listo! 🎉\nEsta es la gráfica de f'],
  [296, 'En el examen ✍️\nnombre y unidad en cada eje'],
  [304, 'Pregunta 1: ¿en qué intervalo\nva a 3 km/min constante?'],
  [320, 'Pregunta 2: ¿en qué intervalo\nrecorrió por lo menos 15 km?'],
  [341, '¡Tú puedes, Lu! 💪'],
];
function noteCard(T) {
  const y0 = 420, h = 205;
  rr(PX, y0, PW, h, 22, '#fffbeb', '#fcd34d', 2);
  let i = 0; while (i + 1 < NOTAS.length && NOTAS[i + 1][0] <= T) i++;
  const [t0, s] = NOTAS[i], al = P(T, t0, t0 + .35);
  const lines = wrap(s, 38, 700, PW - 56);
  const lh = 50, yStart = y0 + h / 2 - (lines.length - 1) * lh / 2;
  lines.forEach((l, k) => txt(l, PX + 28, yStart + k * lh + (1 - al) * 12, 38, C.ink, { w: 700, alpha: al }));
}

// tarjeta inferior: tablas, traslaciones, preguntas
const LY0 = 645, LH = 275;
function lowerCard(T) {
  const modes = [
    [58.8, 155.8, tabla1], [175.4, 246, traslaciones], [253.1, 287.6, tabla3],
    [296, 304, ejes], [304, 320, preg1], [320, 346, preg2],
  ];
  let any = 0;
  for (const [a, b, fn] of modes) { const w = win(T, a, b, .4); if (w > 0) { any = Math.max(any, w); g.save(); g.globalAlpha = w; rr(PX, LY0, PW, LH, 22, C.card, C.line, 2); fn(T); g.restore(); } }
  if (any < 1) { g.save(); g.globalAlpha = 1 - any; rr(PX, LY0, PW, LH, 22, null, C.line, 2); g.restore(); }
}
function tabla(T, col, head, rows) {
  const x0 = PX + 24, cw = [90, 340, 170], y0 = LY0 + 46, rh = 72;
  rr(x0, y0 - 28, cw[0] + cw[1] + cw[2], 56, 10, hexA(col, .12));
  const hx = [x0 + cw[0] / 2, x0 + cw[0] + 16, x0 + cw[0] + cw[1] + 14];
  txt('t', hx[0], y0, 30, col, { w: 800, align: 'center' });
  txt(head, hx[1], y0, 28, col, { w: 800 });
  txt('punto', hx[2], y0, 28, col, { w: 800 });
  g.save(); g.strokeStyle = C.line; g.lineWidth = 2;
  for (const xx of [x0 + cw[0], x0 + cw[0] + cw[1]]) { g.beginPath(); g.moveTo(xx, y0 - 28); g.lineTo(xx, y0 + 2 * rh + 36); g.stroke(); }
  g.restore();
  rows.forEach(([t, at, calc, ac, pt, ap], k) => {
    const y = y0 + (k + 1) * rh;
    txt(t, hx[0], y, 34, C.ink, { w: 700, align: 'center', alpha: P(T, at, at + .4) });
    txt(calc, hx[1], y, 30, C.ink, { w: 600, alpha: P(T, ac, ac + .4) });
    txt(pt, hx[2], y, 30, col, { w: 800, alpha: P(T, ap, ap + .4) });
  });
}
const tabla1 = T => tabla(T, C.p1, 'f(t) = 3t', [['1', 80.5, '3 · 1 = 3', 82.6, '(1; 3)', 85.2], ['2', 88.6, '3 · 2 = 6', 90.4, '(2; 6)', 93.8]]);
const tabla3 = T => tabla(T, C.p3, 'f(t) = 1,5t + 4,5', [['1', 260.6, '1,5·1 + 4,5 = 6', 262.1, '(1; 6)', 268.3], ['2', 264.3, '1,5·2 + 4,5 = 7,5', 266, '(2; 7,5)', 269.3]]);
function traslaciones(T) {
  const S = [['t²', 'la original', 177.7], ['(t − 2)²', '2 a la derecha →', 185.7], ['(t − 2)² + 6', '6 arriba ↑', 196.8], ['2/3 · (t − 2)² + 6', 'se achata', 208.3]];
  let cur = -1; S.forEach((s, k) => { if (T >= s[2]) cur = k; });
  S.forEach(([f, d, at], k) => {
    const y = LY0 + 44 + k * 62, al = P(T, at, at + .4); if (al <= 0) return;
    if (k === cur) rr(PX + 14, y - 27, PW - 28, 54, 12, hexA(C.p2, .13), C.p2, 2, al);
    txt(f, PX + 30, y, 30, C.ink, { w: 700, alpha: al });
    txt(d, PX + PW - 30, y, 26, C.p2, { w: 700, align: 'right', alpha: al });
  });
}
function ejes() {
  txt('Eje horizontal', PX + 28, LY0 + 70, 28, C.soft, { w: 700 });
  txt('t: Tiempo (min)', PX + 28, LY0 + 112, 34, C.ink, { w: 800 });
  txt('Eje vertical', PX + 28, LY0 + 170, 28, C.soft, { w: 700 });
  txt('f(t): Distancia (km)', PX + 28, LY0 + 212, 34, C.ink, { w: 800 });
}
function pasos(T, L, ans, ansAt, col) {
  L.forEach(([s, at], k) => { const lines = wrap(s, 28, 600, PW - 56); lines.forEach((l, j) => txt(l, PX + 28, LY0 + 40 + k * 56 + j * 34, 28, C.ink, { w: 600, alpha: P(T, at, at + .4) })); });
  const a = P(T, ansAt, ansAt + .4);
  if (a > 0) { rr(PX + 20, LY0 + LH - 78, PW - 40, 62, 14, hexA(col, .15), col, 3, a); txt(ans, PX + PW / 2, LY0 + LH - 47, 36, C.ink, { w: 800, align: 'center', alpha: a }); }
}
const preg1 = T => pasos(T, [['f(t) = 3t → cada minuto suma 3 km', 307], ['Eso es velocidad constante: 3 km/min', 311], ['Ojo: la parte 3 también es recta, pero va a 1,5 km/min', 316.5]], 'Respuesta: t ∈ [0; 2]', 314, C.p1);
const preg2 = T => pasos(T, [['Por lo menos 15 → 15 o más (≥ 15)', 323], ['1,5t + 4,5 = 15  →  t = 7', 328], ['🔦 Foco arriba: la sombra va de 7 a 11', 332]], 'Respuesta: t ∈ [7; 11]', 335, '#d97706');

// ---------- subtítulos (texto limpio del .srt) ----------
const SUBS = [
  [1.0, 3.1, 'Hola Lu, te voy a pasar'], [3.3, 5.37, 'estos videos para que entiendas un poquito mejor'], [5.6, 7.4, 'cómo vamos a trabajar'],
  [8.3, 9.87, 'esta resolución de problemas,'], [10.37, 12.2, 'este tipo de problemas. A ver,'], [12.67, 13.77, 'lo primero es entender'],
  [14.27, 16.13, 'que esta función que te están dando'], [16.37, 17.6, 'está partida en tres.'], [18.0, 19.73, 'Es como si tuvieras que resolver'],
  [20.13, 21.77, 'tres funciones en una sola.'], [22.6, 24.97, 'Vas a hacer un collage, algo así como haces'], [25.13, 25.93, 'con las fotos.'],
  [26.47, 28.4, 'Vamos a unir las tres funciones'], [28.67, 29.7, 'en una sola función.'], [29.9, 33.73, 'Como te dije, como un collage. Entonces, primero'],
  [34.4, 36.5, 'vamos a ver la función 3t.'], [36.87, 37.8, 'Imagínate que no hay'], [37.93, 38.67, 'absolutamente nada'],
  [38.67, 41.37, 'y nos quedamos con la primera línea: la función 3t.'], [42.17, 45.13, 'En esta función 3t, para poder graficar'],
  [45.67, 49.13, 'este tipo de funciones… ojo, son funciones lineales'], [49.57, 51.33, 'porque la t no tiene exponente:'],
  [51.57, 53.4, 'ni cuadrado, ni cúbico, ni nada.'], [54.17, 55.5, 'Entonces, para graficar'], [55.6, 58.17, 'estas funciones lineales, lo que hacemos es'],
  [58.8, 61.0, 'tabular. ¿Y cómo tabulamos?'], [61.47, 63.9, 'Fácil. Tabular significa que'], [64.7, 67.67, 'tú vas a inventarte dos valores de t cualquiera'],
  [68.1, 69.67, 'y vas a hallar'], [70.2, 73.87, 'los valores de y, o sea, de la función.'], [74.6, 75.4, 'Entonces,'],
  [75.77, 79.87, 'tenemos la función f(t) = 3 · t.'], [80.47, 84.8, 'Por ejemplo, cuando t vale 1, la función vale 3.'], [85.17, 87.87, 'Ya tenemos el primer punto: (1; 3).'],
  [88.57, 89.7, 'Cuando t vale 2,'], [90.1, 92.9, 'la función es 6. Ya tenemos el segundo punto:'], [93.77, 95.77, '(2; 6). Entonces,'],
  [95.93, 98.73, 'lo graficamos. ¿Cómo se grafica una función lineal?'], [99.3, 100.53, 'Pones los dos puntos'], [100.73, 103.9, 'y trazas una línea recta que pase por esos dos puntos.'],
  [104.1, 105.7, 'Así se grafica una función lineal.'], [106.47, 107.9, 'Ahora, si te das cuenta,'], [108.33, 111.3, 'al costadito de la función nos están diciendo que'],
  [111.67, 112.47, 'de esa gráfica'], [112.97, 116.7, 'solamente me importa la parte que va de 0 hasta 2.'], [117.27, 119.67, 'Así que lo que vamos a hacer es: en 0'],
  [120.5, 121.93, 'voy a agarrar una tijerita.'], [122.2, 126.33, 'Primero que nada, dibujo una línea vertical en 0'], [126.97, 130.27, 'y con una tijerita corto todo'],
  [131.2, 135.17, 'y voy a eliminar la parte anterior al 0.'], [135.97, 137.97, 'Igualito me voy al 2. En 2'], [138.13, 140.73, 'trazo otra vertical y corto con una tijerita'],
  [141.0, 142.87, 'y me olvido de la parte de la derecha.'], [143.2, 144.17, 'Como me están diciendo'], [144.3, 146.9, 'que solamente importa lo que va entre 0 y 2,'],
  [147.2, 149.5, 'me voy a quedar con esa parte de la función.'], [150.17, 152.07, 'Entonces, una vez que ya lo tengo cortado,'], [152.77, 154.53, 'esto va a mi collage final.'],
  [155.77, 156.73, '¡Listo! Siguiente.'], [157.53, 160.2, 'La otra es una función cuadrática,'], [160.3, 161.2, 'que nosotros ya hemos visto'],
  [161.3, 163.8, 'cómo graficar. Recuerda:'], [164.93, 166.57, 'en este caso dice'], [166.8, 168.73, '(t − 2)² + 6.'],
  [168.93, 170.97, 'Ahí hay un 2/3, que'], [171.17, 172.6, 'para la forma de la función'], [173.2, 174.73, 'no cambia mucho, ¿ok?'],
  [175.4, 177.0, 'Entonces, ¿qué vamos a hacer?'], [177.7, 180.57, 'Primero que nada, recuerda lo que dijimos: ponemos'], [181.2, 182.2, 'la función original,'],
  [182.97, 185.27, 'que es la parábola t².'], [185.73, 188.6, 'Como le estoy restando 2 adentro, me voy a mover'], [189.67, 190.47, 'en horizontal.'],
  [190.7, 193.53, 'En este caso, como es −2, me muevo dos espacios'], [193.67, 194.47, 'a la derecha.'], [195.07, 196.47, 'Una vez que se haya movido,'],
  [196.8, 198.57, 'dice que le voy a sumar 6.'], [198.87, 201.97, 'Y recuerda que sumar 6 afuera significa moverme'], [202.5, 204.5, 'hacia arriba 6 espacios.'],
  [204.93, 206.37, '¡Listo! Ya lo tengo movido.'], [207.3, 208.17, 'Y ese…'], [208.27, 210.53, 'como te digo, ese 2/3 que está multiplicando'],
  [210.6, 212.97, 'lo único que hace es'], [213.33, 215.57, 'agachar un poquito la función,'], [216.0, 218.97, 'comprimirla un poquito. Pero en cuanto'],
  [219.77, 222.3, 'a la posición, sigue estando acá.'], [223.07, 224.73, '¡Listo! Entonces, ya que tenemos esto,'], [225.57, 228.17, 'ahora me dicen que esa parte de la función'],
  [228.33, 229.7, 'solamente va de 2 a 5.'], [230.27, 233.0, 'Así que hago lo que hice antes: desde 2'], [233.33, 234.3, 'corto, corto, corto…'],
  [234.53, 238.87, 'hasta 5: corto, corto, corto.'], [239.0, 240.4, 'Lo que está fuera de eso'], [240.57, 243.8, 'lo elimino y me quedo con lo del centro. Así que'],
  [244.57, 247.53, 'eso va a mi collage final. La siguiente'], [247.73, 249.67, 'también es una función lineal, como la primera,'], [249.8, 252.5, 'así que ya sabemos cómo hacerlo: tabulamos.'],
  [253.13, 257.53, 'Pongo la función: f(t) = 1,5t + 4,5.'], [258.33, 261.67, 'Hago mi tablita al costado: t vale 1,'], [262.1, 267.17, 'la función vale 6. Cuando t vale 2, la función vale 7,5.'],
  [268.33, 271.33, 'Y pongo los dos puntos que acabamos de encontrar'], [273.1, 274.3, 'en la gráfica.'], [274.53, 277.87, 'Trazo una línea recta, y me dicen que va de 5 a 11.'],
  [278.6, 281.77, 'Igual: en 5, corto, corto, corto. En 11, corto, corto, corto.'], [281.9, 284.9, 'Me quedo con lo del centro y lo uno a mi collage final.'],
  [285.67, 287.07, 'Una vez que ya lo hicimos,'], [287.67, 290.07, 'ya tenemos la gráfica…'], [290.87, 293.13, 'la gráfica final, mejor dicho.'],
];
function subtitle(T) {
  const s = SUBS.find(([a, b]) => T >= a && T <= b + .25); if (!s) return;
  const al = P(T, s[0], s[0] + .15) * (1 - P(T, s[1] + .1, s[1] + .25));
  const w = tw(s[2], 34, 600) + 56;
  rr(960 - w / 2, 948, w, 70, 18, C.sub, null, 0, al);
  txt(s[2], 960, 984, 34, '#fff', { w: 600, align: 'center', alpha: al });
}

function intro(T) {
  const al = win(T, .2, 12.6, .6); if (al <= 0) return;
  const cx = (PL.x0 + PL.x1) / 2, cy = 420;
  rr(cx - 380, cy - 120, 760, 240, 28, '#fff', C.line, 3, al);
  txt('Función por partes', cx, cy - 40, 60, C.ink, { w: 800, align: 'center', alpha: al });
  txt('¡como un collage de fotos! 📸', cx, cy + 45, 38, C.p2, { w: 700, align: 'center', alpha: al });
}

// ---------- cuadro ----------
function render(T) {
  g.setTransform(1, 0, 0, 1, 0, 0);
  g.fillStyle = C.bg; g.fillRect(0, 0, 1920, 1080);
  drawPlane(T);
  drawStrips(T);
  g.save(); g.beginPath(); g.rect(PL.x0 - 30, PL.y0 - 30, PL.x1 - PL.x0 + 60, PL.y1 - PL.y0 + 30); g.clip();
  drawPreview(T);
  drawParabolaHelpers(T);
  drawPieces(T);
  tabPoint(T, 1, 3, C.p1, 85.2, 150.2, '(1; 3)');
  tabPoint(T, 2, 6, C.p1, 93.8, 150.2, '(2; 6)');
  tabPoint(T, 1, 6, C.p3, 268.3, 999, '(1; 6)', 282);
  tabPoint(T, 2, 7.5, C.p3, 269.3, 999, '(2; 7,5)', 282);
  if (T > 285.7) { const a = P(T, 285.7, 286.3); dot(0, 0, C.p1, { alpha: a, r: 12 }); dot(11, 21, C.p3, { alpha: a, r: 12 }); }
  drawQuestions(T);
  g.restore();
  for (const k of CORTES) drawCut(T, k);
  intro(T);
  collageTiles(T);
  formulaCard(T);
  noteCard(T);
  lowerCard(T);
  subtitle(T);
}

window.ready = false;
Promise.all(['500', '600', '700', '800'].map(w => document.fonts.load(`${w} 40px Inter`)).concat(document.fonts.load('40px "Noto Color Emoji"', '📸')))
  .then(() => { render(0); window.ready = true; });
