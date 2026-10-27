// Video sin audio: las 3 R para hallar el precio (TecnoGlobal, preguntas 4 y 5). Sin gráfica.
const DURATION = 112;
const PX = 1230, PW = 650, WX = 40, WY = 240, WW = 1160, WH = 680;
const R3 = [
  { n: '① RESTA', d: 'x = horas desde las 9', col: C.hi, on: [[21, 30], [55, 68]] },
  { n: '② REVISA', d: '¿en qué fila cae x?', col: C.p1, on: [[30, 40], [68, 79]] },
  { n: '③ REEMPLAZA', d: 'pongo x en esa fila', col: C.p3, on: [[40, 52], [79, 100]] },
];
const ROWS = [
  { expr: '3x + 20', dom: '0 ≤ x ≤ 2', a: 0, b: 2 },
  { expr: '26', dom: '2 < x < 4', a: 2, b: 4 },
  { expr: '26 + √(x − 4)', dom: '4 ≤ x ≤ 7', a: 4, b: 7 },
];
// revisión fila por fila: [desde, fila, ok]
const CHECKS = [[31.5, 0, false], [34, 1, true], [69.5, 0, false], [72, 1, false], [74.5, 2, true]];
const QS = [[18, 52, 'Pregunta 4: ¿cuál es el precio a las 11:30 a.m.?'], [52, 100, 'Pregunta 5: ¿cuál es el precio a la 1:30 p.m.?']];

function chips(T) {
  R3.forEach((r, i) => {
    const x = 40 + i * 620, w = 600, act = Math.max(...r.on.map(([a, b]) => win(T, a, b, .4)));
    rr(x, 40, w, 80, 18, act > 0 ? hexA(r.col, .15 + .85 * act) : '#fff', r.col, 3);
    txt(r.n, x + 24, 80, 34, act > .5 ? '#fff' : r.col, { w: 800 });
    txt(r.d, x + w - 20, 80, 22, act > .5 ? '#fff' : C.soft, { w: 700, align: 'right' });
  });
}
function banner(T) {
  for (const [a, b, s] of QS) {
    const w = win(T, a, b, .5); if (w <= 0) continue;
    rr(40, 140, 1840, 80, 18, hexA(C.p2, .1), C.p2, 2, w);
    txt(s, 70, 181, 36, C.ink, { w: 800, alpha: w });
  }
}
function funcCard(T) {
  const vis = win(T, 18, 100, .5);
  if (vis <= 0) return;
  g.save(); g.globalAlpha = vis;
  const y0 = 240, h = 420;
  rr(PX, y0, PW, h, 22, C.card, C.line, 2);
  txt('La función', PX + 24, y0 + 40, 26, C.soft, { w: 700 });
  txt('f(x) =', PX + 22, y0 + 240, 38, C.ink, { w: 700 });
  const bx = PX + 155, top = y0 + 90, bot = y0 + h - 30, mid = (top + bot) / 2;
  g.save(); g.strokeStyle = C.ink; g.lineWidth = 4; g.lineCap = 'round'; g.beginPath();
  g.moveTo(bx + 16, top); g.quadraticCurveTo(bx, top, bx, top + 18); g.lineTo(bx, mid - 18);
  g.quadraticCurveTo(bx, mid, bx - 14, mid); g.quadraticCurveTo(bx, mid, bx, mid + 18);
  g.lineTo(bx, bot - 18); g.quadraticCurveTo(bx, bot, bx + 16, bot); g.stroke(); g.restore();
  // los números de la derecha brillan mientras se revisa
  const dh = Math.max(win(T, 30, 40, .4), win(T, 68, 79, .4));
  ROWS.forEach((r, i) => {
    const yc = y0 + 130 + i * 100, ex = PX + 190, dx = PX + 455;
    let st = 0, ok = null;
    for (const [t, k, good] of CHECKS) if (k === i && T >= t) { const end = QS.find(([a, b]) => t >= a && t < b)[1]; if (T < end) { st = P(T, t, t + .4); ok = good; } }
    const sel = Math.max(win(T, 40, 52, .4) * (i === 1), win(T, 79, 100, .4) * (i === 2));
    if (sel > 0) rr(ex - 14, yc - 38, PW - (ex - PX) + 2, 76, 14, hexA(C.p3, .16 * sel), C.p3, 4, sel);
    else if (st > 0) rr(ex - 14, yc - 38, PW - (ex - PX) + 2, 76, 14, hexA(ok ? C.p3 : C.cut, .1 * st), ok ? C.p3 : C.cut, 3, st);
    txt(r.expr, ex + 6, yc, 36, C.ink, { w: 700, alpha: ok === false ? .45 : 1 });
    if (dh > 0) rr(dx - 8, yc - 24, tw(r.dom, 32, 800) + 16, 48, 8, hexA(C.hi, .4 * dh));
    txt(r.dom, dx, yc, 32, C.ink, { w: dh > .5 ? 800 : 600, alpha: ok === false ? .45 : 1 });
  });
  if (dh > 0) label('mira de dónde a dónde va x 👇', PX + PW - 20, y0 + 70, C.hiInk, { size: 22, align: 'right', alpha: dh });
  g.restore();
}
function answerCard(T) {
  const y0 = 680, h = 240;
  for (const [a, b, s, at] of [[18, 52, 'US$ 26', 46], [52, 100, 'US$ 26,71', 92]]) {
    const w = win(T, a, b, .5); if (w <= 0) continue;
    g.save(); g.globalAlpha = w;
    rr(PX, y0, PW, h, 22, C.card, C.line, 2);
    txt('Respuesta', PX + 24, y0 + 40, 26, C.soft, { w: 700 });
    const r = P(T, at, at + .5);
    if (r > 0) { rr(PX + 30, y0 + 80, PW - 60, 120, 18, hexA(C.p3, .15), C.p3, 4, r); txt('Precio: ' + s, PX + PW / 2, y0 + 141, 46, C.ink, { w: 800, align: 'center', alpha: r }); }
    else txt('…', PX + PW / 2, y0 + 141, 46, C.line, { w: 800, align: 'center' });
    g.restore();
  }
}

// ---------- ① regla de horas con saltos pasito a pasito ----------
function regla(T, t0, saltos, extra) {
  const x0 = WX + 90, x1 = WX + WW - 70, y = WY + 210, hx = h => x0 + (h - 9) / 7 * (x1 - x0);
  g.save(); g.strokeStyle = C.axis; g.lineWidth = 4; g.beginPath(); g.moveTo(x0 - 20, y); g.lineTo(x1 + 20, y); g.stroke(); g.restore();
  for (let h = 9; h <= 16; h++) {
    g.save(); g.strokeStyle = C.axis; g.lineWidth = 3; g.beginPath(); g.moveTo(hx(h), y - 12); g.lineTo(hx(h), y + 12); g.stroke(); g.restore();
    const lab = h <= 12 ? String(h) : String(h - 12);
    txt(lab, hx(h), y + 42, 34, C.ink, { w: 800, align: 'center' });
    txt(h < 12 ? 'a.m.' : 'p.m.', hx(h), y + 76, 20, C.soft, { w: 600, align: 'center' });
  }
  let pos = 9, cnt = 0;
  saltos.forEach((d, k) => {
    const at = t0 + k * 1.2, p = P(T, at, at + .9); if (p <= 0) return;
    const a = hx(pos), b = hx(pos + d * p), m = (a + hx(pos + d)) / 2, r = (hx(pos + d) - a) / 2;
    g.save(); g.strokeStyle = C.hi; g.lineWidth = 6; g.lineCap = 'round';
    g.beginPath(); g.arc(m, y - 6, r, Math.PI, Math.PI + Math.PI * p); g.stroke(); g.restore();
    label(d === 1 ? '+1' : '+½', m, y - r - 34, C.hiInk, { size: 26, align: 'center', alpha: P(T, at + .5, at + .9) });
    if (p >= 1) cnt += d;
    pos += d;
  });
  const fin = t0 + saltos.length * 1.2 + .3;
  if (T > t0) txt('x = ' + String(cnt).replace('.', ','), WX + 60, WY + 420, 64, C.hiInk, { w: 800 });
  if (T > fin) { const a = P(T, fin, fin + .5); rr(WX + 40, WY + 360, 330, 120, 18, null, C.hi, 5, a); }
  if (extra) extra(T, fin);
}
const resta4 = (T, fin) => {
  [['11:30 − 9:00 = 2 h y 30 min', fin + 1], ['30 min = 0,5  →  x = 2,5', fin + 2.5]].forEach(([s, at], k) =>
    txt(s, WX + 420, WY + 395 + k * 56, 34, C.ink, { w: 700, alpha: P(T, at, at + .4) }));
};
const pm5 = (T, fin) => {
  txt('p.m. → cuento pasito a pasito 👣', WX + 420, WY + 395, 34, C.ink, { w: 700, alpha: P(T, 55.5, 56) });
  txt('4 saltos de 1 + medio = 4,5', WX + 420, WY + 451, 34, C.ink, { w: 700, alpha: P(T, fin + 1, fin + 1.4) });
};

// ---------- ② revisar fila por fila ----------
function revisa(T, xs, t0, items) {
  txt('x = ' + xs, WX + 60, WY + 80, 56, C.hiInk, { w: 800 });
  txt('Pregunto fila por fila, de arriba a abajo:', WX + 60, WY + 160, 30, C.soft, { w: 700, alpha: P(T, t0, t0 + .4) });
  items.forEach(([s, at, ok], k) => {
    const y = WY + 250 + k * 100, a = P(T, at, at + .4); if (a <= 0) return;
    rr(WX + 50, y - 40, WW - 100, 80, 16, hexA(ok ? C.p3 : C.cut, .08), ok ? C.p3 : C.cut, 3, a);
    txt(s, WX + 80, y, 36, C.ink, { w: 700, alpha: a });
    txt(ok ? '✅ Sí' : '❌ No', WX + WW - 80, y, 36, ok ? C.p3 : C.cut, { w: 800, align: 'right', alpha: a });
  });
}
// ---------- ③ reemplazar ----------
function lineas(T, L, x = WX + 60, y0 = WY + 80, gap = 92) {
  L.forEach(([s, at, o = {}], k) => {
    const a = P(T, at, at + .4); if (a <= 0) return;
    if (o.box) rr(x - 20, y0 + k * gap - 42, WW - 80, 84, 16, hexA(o.box, .13), o.box, 3, a);
    txt(s, x, y0 + k * gap, o.size || 46, o.col || C.ink, { w: 800, alpha: a });
  });
}

const FASES = [
  [21, 30, T => regla(T, 22, [1, 1, .5], resta4)],
  [30, 40, T => revisa(T, '2,5', 30.5, [['¿2,5 está entre 0 y 2?', 31.5, false], ['¿2,5 está entre 2 y 4?', 34, true], ['→ cae en la fila 2', 36.5, true]])],
  [40, 52, T => lineas(T, [['Fila 2:  26', 40.5], ['No tiene x → no reemplazo nada', 42.5, { size: 38, col: C.soft }], ['Sale 26 directo ✨', 44.5, { box: C.p3 }], ['Precio: US$ 26', 46.5, { box: C.p3, size: 52 }]])],
  [55, 68, T => regla(T, 56.5, [1, 1, 1, 1, .5], pm5)],
  [68, 79, T => revisa(T, '4,5', 68.5, [['¿4,5 está entre 0 y 2?', 69.5, false], ['¿4,5 está entre 2 y 4?', 72, false], ['¿4,5 está entre 4 y 7?', 74.5, true], ['→ cae en la fila 3', 76.5, true]])],
  [79, 100, T => lineas(T, [['Fila 3:  26 + √(x − 4)', 80], ['= 26 + √(4,5 − 4)', 82.5], ['= 26 + √0,5', 85], ['con calculadora: √0,5 ≈ 0,71', 87.5, { col: C.soft, size: 38 }], ['= 26,71', 90, { box: C.p3 }], ['Precio: US$ 26,71', 92, { box: C.p3, size: 52 }]], WX + 60, WY + 70, 98)],
];
function work(T) {
  rr(WX, WY, WW, WH, 22, C.card, C.line, 2);
  for (const [a, b, fn] of FASES) { const w = win(T, a, b, .4); if (w > 0) { g.save(); g.globalAlpha = w; fn(T); g.restore(); } }
  // entre fases: el nombre de la R que viene
  const nxt = [[18, 21, 0], [52, 55, 0]].find(([a, b]) => T >= a && T < b);
  if (nxt) { const r = R3[nxt[2]], w = win(T, nxt[0], nxt[1], .4); txt('Empezamos 👇', WX + WW / 2, WY + WH / 2, 52, r.col, { w: 800, align: 'center', alpha: w }); }
}

// ---------- intro y repaso ----------
function tresR(T, a, b, t0, extra) {
  const al = win(T, a, b, .6); if (al <= 0) return;
  g.save(); g.globalAlpha = al;
  rr(40, 140, 1840, 780, 26, C.card, C.line, 2);
  txt('Para hallar el precio: las 3 R', 960, 230, 54, C.ink, { w: 800, align: 'center' });
  R3.forEach((r, i) => {
    const at = t0 + i * (extra ? .8 : 4), p = P(T, at, at + .5); if (p <= 0) return;
    const x = 110 + i * 590, y = 330, sc = pop(T, at);
    g.save(); g.translate(x + 260, y + 220); g.scale(sc, sc); g.translate(-x - 260, -y - 220);
    rr(x, y, 520, 440, 26, hexA(r.col, .12), r.col, 4);
    txt(r.n, x + 260, y + 120, 56, r.col, { w: 800, align: 'center' });
    wrap(r.d, 40, 700, 460).forEach((l, k) => txt(l, x + 260, y + 250 + k * 54, 40, C.ink, { w: 700, align: 'center' }));
    g.restore();
  });
  if (extra) extra(T);
  g.restore();
}
const fin = T => { const a = P(T, 106, 106.6); if (a > 0) txt('¡Tú puedes, Lu! 💪', 960, 860, 52, C.p2, { w: 800, align: 'center', alpha: a }); };

function render(T) {
  g.setTransform(1, 0, 0, 1, 0, 0);
  g.fillStyle = C.bg; g.fillRect(0, 0, 1920, 1080);
  chips(T);
  banner(T);
  work(T);
  funcCard(T);
  answerCard(T);
  tresR(T, 2, 18, 4.5);
  tresR(T, 100, 112.5, 100.5, fin);
  g.fillStyle = hexA(C.ink, .12); g.fillRect(40, 1000, 1840, 8);
  g.fillStyle = C.p2; g.fillRect(40, 1000, 1840 * T / DURATION, 8);
  const sec = current([[0, 'Las 3 R'], [18, 'Pregunta 4'], [52, 'Pregunta 5'], [100, 'Repaso']], T);
  txt(sec[1], 40, 970, 26, C.soft, { w: 700 });
}
