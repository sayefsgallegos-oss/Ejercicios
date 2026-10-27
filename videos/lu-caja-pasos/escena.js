// Video sin audio: la caja en 4 pasos (Borde → Caja → Mejor → Comparo), para memorizar.
const DURATION = 135;
const PX = 1230, PW = 650, WX = 40, WY = 240, WW = 1160, WH = 680;
const VIEW = { cx: 620, cy: 590, sFlat: 12.5, sBox: 21 };
const PASOS4 = [
  { n: '① BORDE', d: 'el perímetro', col: C.hi, on: [18, 52] },
  { n: '② CAJA', d: 'el volumen', col: C.p1, on: [52, 80] },
  { n: '③ MEJOR', d: 'la fórmula', col: C.p2, on: [80, 108] },
  { n: '④ COMPARO', d: 'con 1950', col: C.p3, on: [108, 124] },
];
const BANNERS = [
  [18, 52, 'Pregunta 1 · El perímetro de la plancha es 160 cm'],
  [52, 80, 'Pregunta 2 · ¿Qué función da el volumen V(x)?'],
  [80, 108, 'Pregunta 3 · ¿Qué medidas dan el volumen máximo?'],
  [108, 124, '¿Es correcta la afirmación? (volumen mayor que 1950 cm³)'],
];
const KEYS = [[0, 0, 0], [52, 0, 0], [54.8, 1, 0], [56, 1, 1]];
function fold(T) {
  let i = 0; while (i + 1 < KEYS.length && KEYS[i + 1][0] <= T) i++;
  const a = KEYS[i], b = KEYS[i + 1] || a, p = b === a ? 0 : P(T, a[0], b[0]);
  return { w: a[1] + (b[1] - a[1]) * p, t: a[2] + (b[2] - a[2]) * p };
}

function chips(T) {
  PASOS4.forEach((r, i) => {
    const x = 40 + i * 465, w = 445, act = win(T, r.on[0], r.on[1], .4);
    rr(x, 40, w, 80, 18, act > 0 ? hexA(r.col, .15 + .85 * act) : '#fff', r.col, 3);
    txt(r.n, x + 22, 80, 32, act > .5 ? '#fff' : r.col, { w: 800 });
    txt(r.d, x + w - 18, 80, 22, act > .5 ? '#fff' : C.soft, { w: 700, align: 'right' });
  });
}
function banner(T) {
  for (const [a, b, s] of BANNERS) {
    const w = win(T, a, b, .5); if (w <= 0) continue;
    rr(40, 140, 1840, 80, 18, hexA(C.p2, .1), C.p2, 2, w);
    txt(s, 70, 181, 34, C.ink, { w: 800, alpha: w });
  }
}

// ---------- visual de la caja ----------
function perimetro(T, cam, t0, t1, end) {
  const al = win(T, t0, end, .5); if (al <= 0) return;
  const pts = [[-H, -H], [2 * BX + H, -H], [2 * BX + H, BY + H], [-H, BY + H], [-H, -H]].map(([u, v]) => proj(cam, [u, v, 0]));
  const p = lin(T, t0, t1) * 4;
  g.save(); g.globalAlpha = al; g.strokeStyle = C.hi; g.lineWidth = 7; g.lineCap = 'round'; g.lineJoin = 'round';
  g.beginPath(); g.moveTo(pts[0].x, pts[0].y);
  for (let i = 0; i < 4; i++) { const r = clamp(p - i); if (r <= 0) break; g.lineTo(pts[i].x + (pts[i + 1].x - pts[i].x) * r, pts[i].y + (pts[i + 1].y - pts[i].y) * r); }
  g.stroke(); g.restore();
}
function cotasPlancha(T, cam) {
  const out = 1 - P(T, 51, 52);
  const W = [[-H, 0, '10'], [0, BX, 'x'], [BX, BX + H, '10'], [BX + H, 2 * BX + H, 'x']];
  W.forEach(([u0, u1, s], i) => cota(cam, [u0, BY + H, 0], [u1, BY + H, 0], [0, 3.2, 0], s, C.hiInk, P(T, 25 + i * .6, 25.4 + i * .6) * out));
  const Hh = [[-H, 0, '10'], [0, BY, 'y'], [BY, BY + H, '10']];
  Hh.forEach(([v0, v1, s], i) => cota(cam, [2 * BX + H, v0, 0], [2 * BX + H, v1, 0], [3.2, 0, 0], s, C.hiInk, P(T, 30.5 + i * .6, 30.9 + i * .6) * out));
}
function cotasCaja(T, cam) {
  for (const [a, sx, sy] of [[win(T, 56.5, 80, .5), 'x', 'y'], [win(T, 109, 124, .5), '10', '20']]) {
    if (a <= 0) continue;
    cota(cam, [0, 0, 0], [BX, 0, 0], [0, -3, 0], sx, C.p1, a);
    cota(cam, [BX, 0, 0], [BX, BY, 0], [3, 0, 0], sy, C.p1, a);
    cota(cam, [0, 0, 0], [0, 0, H], [-2.2, -2.2, 0], '10', '#7a5530', a);
  }
}

// ---------- paso 3: la fórmula en grande ----------
function formula(T, al) {
  if (al <= 0) return;
  g.save(); g.globalAlpha = al;
  const cx = WX + WW / 2;
  txt('La función del paso ②', cx, WY + 60, 28, C.soft, { w: 700, align: 'center' });
  // V = −20x² + 400x con a y b marcados
  const parts = [['V = ', null], ['−20', 'a'], ['x² + ', null], ['400', 'b'], ['x', null]];
  const size = 64, total = parts.reduce((s, [p]) => s + tw(p, size, 800), 0);
  let x = cx - total / 2; const y = WY + 150;
  for (const [p, k] of parts) {
    const w = tw(p, size, 800);
    if (k) {
      const at = k === 'a' ? 84 : 86.5, a = P(T, at, at + .4), col = k === 'a' ? C.cut : C.p1;
      if (a > 0) {
        rr(x - 8, y - 44, w + 16, 88, 12, hexA(col, .13), col, 4, a);
        arrow(x + w / 2, y + 52, x + w / 2, y + 110, col, 4, a);
        txt(k === 'a' ? 'a = −20' : 'b = 400', x + w / 2, y + 140, 34, col, { w: 800, align: 'center', alpha: a });
        txt(k === 'a' ? '(va con x²)' : '(va con x)', x + w / 2, y + 180, 24, C.soft, { w: 700, align: 'center', alpha: a });
      }
    }
    txt(p, x, y, size, C.ink, { w: 800 }); x += w;
  }
  const f = P(T, 81, 81.5);
  if (f > 0) { rr(cx - 330, WY + 390, 660, 110, 22, hexA(C.hi, .18), C.hi, 4, f); txt('x = −b ÷ (2·a)', cx, WY + 446, 62, C.ink, { w: 800, align: 'center', alpha: f }); }
  // alternativas con su x: se busca x = 10
  const op = P(T, 99, 99.5);
  if (op > 0) {
    [['a', 5], ['b', 10], ['c', 8], ['d', 12], ['e', 15]].forEach(([l, v], k) => {
      const bx = WX + 75 + k * 210, ok = l === 'b';
      rr(bx, WY + 560, 190, 80, 16, ok ? hexA(C.p3, .15) : '#fff', ok ? C.p3 : C.line, ok ? 4 : 2, op);
      txt(`${l})  x = ${v}`, bx + 95, WY + 600, 30, ok ? C.p3 : C.soft, { w: 800, align: 'center', alpha: op });
    });
  }
  g.restore();
}

// ---------- tarjeta de pasos (derecha) ----------
const LINEAS = [
  [18, 52, [
    [25, 'Ancho: 10 + x + 10 + x'], [27.5, '= 2x + 20'], [30.5, 'Alto: 10 + y + 10'], [33, '= y + 20'],
    [35.5, '2 anchos + 2 altos = 160'], [38, '2(2x + 20) + 2(y + 20) = 160'], [41, '4x + 2y + 80 = 160'],
    [44, '4x + 2y = 80    ✅ d', 'ok'], [47.5, '÷ 2 →  y = 40 − 2x   📌', 'key']]],
  [52, 80, [
    [57, 'V = 10 · x · y'], [60, '📌 y = 40 − 2x → cambio la y', 'key'], [63, 'V = 10x · (40 − 2x)'],
    [66, '10x · 40 = 400x'], [68.5, '10x · 2x = 20x²'], [71, 'V = −20x² + 400x    ✅ a', 'ok']]],
  [80, 108, [
    [81, 'x = −b ÷ (2·a)', 'key'], [84, 'a = −20   (va con x²)'], [86.5, 'b = 400   (va con x)'],
    [90, 'x = −400 ÷ (2 · −20)'], [92.5, 'x = −400 ÷ −40'], [95, 'menos ÷ menos = más'], [96.5, 'x = 10'],
    [99, 'Busco x = 10 →  b  ✅', 'ok'], [102, '(y = 40 − 2·10 = 20)']]],
  [108, 124, [
    [110, 'V = 10 · 10 · 20'], [112.5, 'V = 2000 cm³'], [115, 'El cliente pide más de 1950'],
    [118, '2000 > 1950 → ✅ Sí, es correcta', 'ok']]],
];
function pasosCard(T) {
  rr(PX, WY, PW, WH, 22, C.card, C.line, 2);
  for (const [a, b, L] of LINEAS) {
    const w = win(T, a, b, .4); if (w <= 0) continue;
    g.save(); g.globalAlpha = w;
    const vis = L.filter(l => l[0] <= T);
    vis.forEach(([t, s, kind], k) => {
      const y = WY + 50 + k * 66, al = P(T, t, t + .4), last = k === vis.length - 1;
      if (kind === 'ok') rr(PX + 14, y - 28, PW - 28, 56, 12, hexA(C.p3, .13), C.p3, 2, al);
      else if (kind === 'key') rr(PX + 14, y - 28, PW - 28, 56, 12, hexA(C.hi, .18), C.hi, 2, al);
      else if (last) rr(PX + 14, y - 28, PW - 28, 56, 12, hexA(C.p2, .07), null, 0, al);
      txt(s, PX + 30, y, 30, C.ink, { w: kind ? 800 : 600, alpha: al });
    });
    if (a === 108) {
      const bb = P(T, 116, 116.5), W = 380, yb = WY + WH - 140;
      [['pide', 1950, C.soft], ['caja', 2000, C.p3]].forEach(([n, v, col], k) => {
        if (bb <= 0) return;
        txt(n, PX + 30, yb + k * 62, 28, C.ink, { w: 700, alpha: bb });
        rr(PX + 130, yb - 20 + k * 62, W * v / 2000 * P(T, 116 + k * .6, 117.2 + k * .6), 40, 8, col, null, 0, bb);
        txt(String(v), PX + 140 + W * v / 2000, yb + k * 62, 28, col, { w: 800, alpha: P(T, 117.2 + k * .6, 117.6 + k * .6) });
      });
    }
    g.restore();
  }
}

// ---------- intro y repaso ----------
function cuatro(T, a, b, t0, gap, extra) {
  const al = win(T, a, b, .6); if (al <= 0) return;
  g.save(); g.globalAlpha = al;
  rr(40, 140, 1840, 780, 26, C.card, C.line, 2);
  txt('La caja en 4 pasos', 960, 230, 56, C.ink, { w: 800, align: 'center' });
  PASOS4.forEach((r, i) => {
    const at = t0 + i * gap; if (T < at) return;
    const x = 90 + i * 445, y = 330, sc = pop(T, at);
    g.save(); g.translate(x + 200, y + 200); g.scale(sc, sc); g.translate(-x - 200, -y - 200);
    rr(x, y, 400, 400, 26, hexA(r.col, .12), r.col, 4);
    txt(r.n, x + 200, y + 130, 48, r.col, { w: 800, align: 'center' });
    txt(r.d, x + 200, y + 250, 38, C.ink, { w: 700, align: 'center' });
    g.restore();
  });
  if (extra) extra(T);
  g.restore();
}
const fin = T => { const a = P(T, 130, 130.6); if (a > 0) txt('¡Tú puedes, Lu! 💪', 960, 830, 52, C.p2, { w: 800, align: 'center', alpha: a }); };
const flechas = T => { const a = P(T, 16, 16.5); if (a > 0) txt('cada paso usa lo que salió del anterior 👉', 960, 830, 34, C.soft, { w: 700, align: 'center', alpha: a }); };

function render(T) {
  g.setTransform(1, 0, 0, 1, 0, 0);
  g.fillStyle = C.bg; g.fillRect(0, 0, 1920, 1080);
  chips(T);
  banner(T);
  rr(WX, WY, WW, WH, 22, C.card, C.line, 2);
  const fa = win(T, 80, 108, .6), ba = 1 - fa;
  g.save(); g.beginPath(); g.rect(WX, WY, WW, WH); g.clip();
  const cam = drawBox(T, ba, fold(T), [], VIEW);
  g.save(); g.globalAlpha = ba;
  perimetro(T, cam, 20, 24.5, 52);
  cotasPlancha(T, cam);
  cotasCaja(T, cam);
  g.restore();
  formula(T, fa);
  g.restore();
  pasosCard(T);
  cuatro(T, 1, 18, 4.5, 3, flechas);
  cuatro(T, 124, 135.5, 124.5, .8, fin);
  g.fillStyle = hexA(C.ink, .12); g.fillRect(40, 1000, 1840, 8);
  g.fillStyle = C.p2; g.fillRect(40, 1000, 1840 * T / DURATION, 8);
  const sec = current([[0, 'Los 4 pasos'], [18, '① Borde'], [52, '② Caja'], [80, '③ Mejor'], [108, '④ Comparo'], [124, 'Repaso']], T);
  txt(sec[1], 40, 970, 26, C.soft, { w: 700 });
}
