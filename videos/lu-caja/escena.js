// Video sin audio: la caja de cartón (perímetro → volumen → máximo).
// La caja se arma y desarma en 3D (proyección ortogonal dibujada a mano).
const DURATION = 180;
const PX = 1230, PW = 650;

// ---------- armado: [t, paredes, tapa] (0 = plano, 1 = armado) ----------
const KEYS = [
  [0, 1, 1], [12, 1, 1], [13.8, 1, 0], [16.5, 0, 0], [17, 0, 0], [19.5, 1, 0], [21, 1, 1],
  [21.5, 1, 1], [23, 1, 0], [25.5, 0, 0], [75, 0, 0], [78, 1, 0], [79.5, 1, 1],
  [165, 1, 1], [166.5, 1, 0], [169, 0, 0], [170, 0, 0], [172.5, 1, 0], [174, 1, 1],
];
function fold(T) {
  let i = 0; while (i + 1 < KEYS.length && KEYS[i + 1][0] <= T) i++;
  const a = KEYS[i], b = KEYS[i + 1] || a, p = b === a ? 0 : P(T, a[0], b[0]);
  return { w: a[1] + (b[1] - a[1]) * p, t: a[2] + (b[2] - a[2]) * p };
}

const HILITE = [['base', C.p1, 26, 29.5], ['tapa', C.p2, 29.5, 32.5], ['izq', C.hi, 32.5, 36], ['der', C.hi, 32.5, 36], ['frente', C.hi, 32.5, 36], ['fondo', C.hi, 32.5, 36]];
function netDims(T, cam) {
  const a = win(T, 26, 36, .5), ink = '#7a5530';
  cota(cam, [0, -H, 0], [BX, -H, 0], [0, -3, 0], 'x', C.p1, a);
  cota(cam, [2 * BX + H, 0, 0], [2 * BX + H, BY, 0], [3, 0, 0], 'y', C.p1, a);
  cota(cam, [-H, 0, 0], [0, 0, 0], [0, -3, 0], '10', ink, win(T, 32.5, 36, .5));
  // ancho y alto de la plancha (perímetro)
  const W = [[-H, 0, '10'], [0, BX, 'x'], [BX, BX + H, '10'], [BX + H, 2 * BX + H, 'x']];
  W.forEach(([u0, u1, s], i) => cota(cam, [u0, BY + H, 0], [u1, BY + H, 0], [0, 3.2, 0], s, C.hiInk, P(T, 45 + i * .7, 45.4 + i * .7) * (1 - P(T, 74, 75))));
  const Hh = [[-H, 0, '10'], [0, BY, 'y'], [BY, BY + H, '10']];
  Hh.forEach(([v0, v1, s], i) => cota(cam, [2 * BX + H, v0, 0], [2 * BX + H, v1, 0], [3.2, 0, 0], s, C.hiInk, P(T, 50 + i * .7, 50.4 + i * .7) * (1 - P(T, 74, 75))));
}
function perimetro(T, cam) {
  const al = win(T, 40, 75, .5); if (al <= 0) return;
  const pts = [[-H, -H], [2 * BX + H, -H], [2 * BX + H, BY + H], [-H, BY + H], [-H, -H]].map(([u, v]) => proj(cam, [u, v, 0]));
  const lens = [40, 40, 40, 40], p = lin(T, 40, 44.5) * 160;
  g.save(); g.globalAlpha = al; g.strokeStyle = C.hi; g.lineWidth = 7; g.lineCap = 'round'; g.lineJoin = 'round';
  g.beginPath(); g.moveTo(pts[0].x, pts[0].y);
  let acc = 0, end = pts[0];
  for (let i = 0; i < 4; i++) {
    const r = clamp((p - acc) / lens[i]); if (r <= 0) break;
    end = { x: pts[i].x + (pts[i + 1].x - pts[i].x) * r, y: pts[i].y + (pts[i + 1].y - pts[i].y) * r };
    g.lineTo(end.x, end.y); acc += lens[i];
  }
  g.stroke(); g.restore();
  if (T < 45) { g.save(); g.globalAlpha = al; g.fillStyle = C.hi; g.beginPath(); g.arc(end.x, end.y, 11, 0, 7); g.fill(); g.restore(); }
  label(`borde: ${Math.round(p)} cm`, pts[0].x, pts[0].y + 40, C.hiInk, { size: 24, alpha: al * (T < 45 ? 1 : 0) });
}
function boxDims(T, cam) {
  const a1 = win(T, 80, 108, .5), a2 = win(T, 146, 165, .5);
  for (const [a, sx, sy, sh] of [[a1, 'x', 'y', '10'], [a2, '10', '20', '10']]) {
    if (a <= 0) continue;
    cota(cam, [0, 0, 0], [BX, 0, 0], [0, -3, 0], sx, C.p1, a);
    cota(cam, [BX, 0, 0], [BX, BY, 0], [3, 0, 0], sy, C.p1, a);
    cota(cam, [0, 0, 0], [0, 0, H], [-2.2, -2.2, 0], sh, '#7a5530', a);
  }
}

// ---------- gráfica V(x) ----------
const GP = makePlane({ x0: 170, x1: 1150, y0: 90, y1: 850, xmin: -1.2, xmax: 21.5, ymin: -180, ymax: 2350 });
const V = x => -20 * x * x + 400 * x;
function drawGraph(T, alpha) {
  if (alpha <= 0) return;
  g.save(); g.globalAlpha = alpha;
  const { X, Y } = GP;
  g.lineWidth = 1.5; g.strokeStyle = C.grid;
  for (let x = 0; x <= 20; x += 2) { g.beginPath(); g.moveTo(X(x), GP.y0); g.lineTo(X(x), Y(GP.ymin)); g.stroke(); }
  for (let v = 500; v <= 2000; v += 500) { g.beginPath(); g.moveTo(GP.x0, Y(v)); g.lineTo(GP.x1, Y(v)); g.stroke(); }
  arrow(GP.x0, Y(0), GP.x1 + 12, Y(0), C.axis, 3);
  arrow(X(0), GP.y1, X(0), GP.y0 - 14, C.axis, 3);
  for (let x = 2; x <= 20; x += 2) txt(String(x), X(x), Y(0) + 26, 22, C.soft, { align: 'center', w: 600 });
  for (let v = 500; v <= 2000; v += 500) txt(String(v), X(0) - 12, Y(v), 22, C.soft, { align: 'right', w: 600 });
  txt('x: ancho (cm)', GP.x1, Y(0) + 58, 26, C.ink, { w: 700, align: 'right' });
  txt('V: volumen (cm³)', X(0) + 16, GP.y0 + 4, 26, C.ink, { w: 700 });
  g.save(); GP.clip(); curve(GP, V, 0, 20 * lin(T, 110, 113), C.p2, 7); g.restore();
  const vx = win(T, 117, 140, .5);
  if (vx > 0) {
    const pu = .5 + .5 * Math.sin(T * 6);
    g.save(); g.globalAlpha = alpha * vx; g.strokeStyle = C.hi; g.lineWidth = 5; g.beginPath(); g.arc(X(10), Y(2000), 24 + 6 * pu, 0, 7); g.stroke(); g.restore();
    dot(GP, 10, 2000, C.p2, { alpha: vx });
    label('vértice: lo más alto', X(10) + 34, Y(2000) - 30, C.p2, { size: 24, alpha: vx });
  }
  const d = win(T, 127, 140, .5);
  if (d > 0) {
    dashLine(X(10), Y(0), X(10), Y(0) + (Y(2000) - Y(0)) * P(T, 127, 128), C.hiInk, d, 4);
    dashLine(X(10), Y(2000), X(10) + (X(0) - X(10)) * P(T, 128.5, 129.5), Y(2000), C.hiInk, d * P(T, 128.5, 128.6), 4);
    label('x = 10', X(10) + 14, Y(0) - 30, C.hiInk, { size: 24, alpha: d });
    if (T > 129.5) label('2000', X(0) + 12, Y(2000) - 30, C.hiInk, { size: 24, alpha: d });
  }
  const bocaAbajo = win(T, 113, 117, .4);
  if (bocaAbajo > 0) label('boca abajo ∩', X(16.5), Y(1500), C.p2, { size: 28, alpha: bocaAbajo });
  g.restore();
}

// ---------- panel derecho ----------
const NOTAS = [
  [0, 'La caja de cartón 📦\n¿qué medidas guardan más?'],
  [6, 'Una caja con tapa.\nLa altura es 10 cm'],
  [12, 'La desarmamos →\nqueda una plancha plana'],
  [17, 'La armamos otra vez'],
  [21.5, 'La desarmamos de nuevo\ny vemos sus partes'],
  [26, 'Base: x de ancho, y de largo'],
  [29.5, 'Tapa: igualita a la base'],
  [32.5, 'Pestañas de 10 cm\n= la altura de la caja'],
  [36, 'Pregunta 1\nPerímetro de la plancha = 160 cm'],
  [40, 'Perímetro = recorrer\ntodo el borde'],
  [45, 'Ancho de la plancha'],
  [50, 'Alto de la plancha'],
  [55, '2 anchos + 2 altos = 160'],
  [63, '✓ Pregunta 1: alternativa d'],
  [67, 'Saco mitad y despejo y\n📌 guárdalo'],
  [75, 'Pregunta 2\nArmamos la caja'],
  [80, 'Volumen de una caja =\nlargo × ancho × alto'],
  [88, 'Reemplazo y = 40 − 2x'],
  [95, 'Multiplico'],
  [99, '✓ Pregunta 2: alternativa a'],
  [108, 'Pregunta 3: ¿qué medidas\ndan el volumen máximo?'],
  [113, 'x² con número negativo\n→ parábola boca abajo'],
  [117, 'Lo más alto de la parábola:\nel vértice'],
  [121, 'Fórmula del vértice'],
  [131, 'Con x = 10 hallo y'],
  [135, '✓ Pregunta 3: alternativa b'],
  [140, '¿Es correcta la afirmación?\n¿V > 1950 cm³?'],
  [146, 'Armo la caja óptima:\n10 × 20 × 10'],
  [156, '✓ Sí: 2000 > 1950'],
  [165, 'Resumen'],
  [176, '¡Tú puedes, Lu! 💪'],
];
// pasos: [t, texto, tipo] — cada sección empieza con su título
const PASOS = [
  [36, 'Pregunta 1 · Perímetro', 'h'],
  [37, 'Perímetro de la plancha = 160'],
  [45, 'Ancho: 10 + x + 10 + x = 2x + 20'],
  [50, 'Alto: 10 + y + 10 = y + 20'],
  [55, '2(2x + 20) + 2(y + 20) = 160'],
  [59, '4x + 2y + 80 = 160'],
  [63, '4x + 2y = 80   ✓ alternativa d', 'ok'],
  [67, '÷ 2  →  2x + y = 40'],
  [70, 'y = 40 − 2x   📌', 'key'],
  [75, 'Pregunta 2 · Volumen', 'h'],
  [80, 'V = largo · ancho · alto'],
  [84, 'V = 10 · x · y'],
  [88, 'y = 40 − 2x  → reemplazo'],
  [91, 'V = 10 · x · (40 − 2x)'],
  [95, 'V = 400x − 20x²'],
  [99, 'V(x) = −20x² + 400x   ✓ alternativa a', 'ok'],
  [108, 'Pregunta 3 · Máximo', 'h'],
  [113, '−20x² → parábola boca abajo ∩'],
  [117, 'Lo más alto = vértice = V máximo'],
  [121, 'x = −b / (2a)', 'key'],
  [124, 'a = −20     b = 400'],
  [127, 'x = −400 / (−40) = 10'],
  [131, 'y = 40 − 2(10) = 20'],
  [135, 'x = 10 cm; y = 20 cm   ✓ alternativa b', 'ok'],
  [140, '¿Es correcta la afirmación?', 'h'],
  [146, 'V = 10 · 10 · 20'],
  [149, 'V = 2000 cm³'],
  [153, '¿2000 > 1950?'],
  [156, '✓ Sí, la afirmación es correcta', 'ok'],
  [165, 'Resumen', 'h'],
  [166, 'Perímetro → relación entre x e y'],
  [168, 'Volumen → la función V(x)'],
  [170, 'Vértice → el máximo'],
];
function pasosCard(T) {
  const y0 = 290, h = 630;
  rr(PX, y0, PW, h, 22, C.card, C.line, 2);
  let s = -1; PASOS.forEach((p, i) => { if (p[2] === 'h' && p[0] <= T) s = i; });
  if (s < 0) { txt('Datos', PX + 28, y0 + 50, 30, C.ink, { w: 800 }); ['Altura de la caja: 10 cm', 'Perímetro de la plancha: 160 cm', '¿Volumen mayor que 1950 cm³?'].forEach((t, k) => txt('• ' + t, PX + 28, y0 + 110 + k * 56, 28, C.ink, { w: 600, alpha: P(T, 6 + k, 6.5 + k) })); return; }
  const sec = PASOS[s], fin = PASOS.findIndex((p, i) => i > s && p[2] === 'h'), out = fin > 0 ? 1 - P(T, PASOS[fin][0] - .4, PASOS[fin][0]) : 1;
  g.save(); g.globalAlpha = out * P(T, sec[0], sec[0] + .4);
  txt(sec[1], PX + 28, y0 + 48, 30, C.p2, { w: 800 });
  const lines = PASOS.slice(s + 1, fin > 0 ? fin : undefined).filter(p => p[0] <= T);
  lines.forEach(([t, s2, kind], k) => {
    const y = y0 + 112 + k * 64, a = P(T, t, t + .4), last = k === lines.length - 1;
    if (kind === 'ok') rr(PX + 16, y - 27, PW - 32, 54, 12, hexA(C.p3, .13), C.p3, 2, a);
    else if (kind === 'key') rr(PX + 16, y - 27, PW - 32, 54, 12, hexA(C.hi, .18), C.hi, 2, a);
    else if (last) rr(PX + 16, y - 27, PW - 32, 54, 12, hexA(C.p2, .07), null, 0, a);
    txt(s2, PX + 30, y, 29, C.ink, { w: kind ? 800 : 600, alpha: a });
  });
  // barras: pedido vs caja
  const b = P(T, 151, 152);
  if (sec[0] === 140 && b > 0) {
    const yb = y0 + h - 150, W = 380;
    [['pedido', 1950, C.soft], ['caja', 2000, C.p3]].forEach(([n, v, col], k) => {
      txt(n, PX + 30, yb + k * 62, 26, C.ink, { w: 700, alpha: b });
      rr(PX + 140, yb - 20 + k * 62, W * v / 2000 * P(T, 151 + k * .6, 152.2 + k * .6), 40, 8, col, null, 0, b);
      txt(String(v), PX + 150 + W * v / 2000 + 4, yb + k * 62, 26, col, { w: 800, alpha: P(T, 152.2 + k * .6, 152.6 + k * .6) });
    });
  }
  g.restore();
}

function intro(T) {
  const al = win(T, .2, 5.8, .6); if (al <= 0) return;
  rr(220, 70, 800, 150, 28, '#fff', C.line, 3, al);
  txt('La caja de cartón 📦', 620, 125, 54, C.ink, { w: 800, align: 'center', alpha: al });
  txt('perímetro → volumen → máximo', 620, 185, 32, C.p2, { w: 700, align: 'center', alpha: al });
}

function render(T) {
  g.setTransform(1, 0, 0, 1, 0, 0);
  g.fillStyle = C.bg; g.fillRect(0, 0, 1920, 1080);
  rr(40, 40, 1160, 880, 26, C.card, C.line, 2);
  const ga = win(T, 108, 140, .8);
  const cam = drawBox(T, 1 - ga, fold(T), HILITE);
  if (ga < 1) { g.save(); g.globalAlpha = 1 - ga; netDims(T, cam); perimetro(T, cam); boxDims(T, cam); g.restore(); }
  drawGraph(T, ga);
  intro(T);
  noteCard(T, NOTAS, PX, 40, PW, 230);
  pasosCard(T);
  g.fillStyle = hexA(C.ink, .12); g.fillRect(40, 1000, 1840, 8);
  g.fillStyle = C.p2; g.fillRect(40, 1000, 1840 * T / DURATION, 8);
  const sec = current([[0, 'La caja'], [36, 'Pregunta 1'], [75, 'Pregunta 2'], [108, 'Pregunta 3'], [140, 'Afirmación'], [165, 'Resumen']], T);
  txt(sec[1], 40, 970, 26, C.soft, { w: 700 });
}
