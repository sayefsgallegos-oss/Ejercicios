// Video sin audio: TecnoGlobal, función por partes (collage) + evaluar.
const DURATION = 248;
const PL = makePlane({ x0: 110, x1: 1170, y0: 70, y1: 890, xmin: -1.3, xmax: 7.9, ymin: 18.75, ymax: 29 });
const { X, Y } = PL;
const AX = 19.2; // altura donde va el eje x (el eje y está cortado: salta de 0 a 20)
const raiz = x => 26 + Math.sqrt(Math.max(0, x - 4));
const F = [x => 3 * x + 20, () => 26, raiz];

// ---------- plano ----------
function drawPlane(T) {
  rr(40, 40, 1160, 880, 26, C.card, C.line, 2);
  g.save(); PL.clip();
  g.lineWidth = 1.5;
  for (let x = -1; x <= 7; x++) { g.strokeStyle = x < 0 ? C.gridNeg : C.grid; g.beginPath(); g.moveTo(X(x), PL.y0); g.lineTo(X(x), Y(AX)); g.stroke(); }
  for (let f = 20; f <= 28; f++) { g.strokeStyle = C.grid; g.beginPath(); g.moveTo(PL.x0, Y(f)); g.lineTo(PL.x1, Y(f)); g.stroke(); }
  g.restore();
  arrow(PL.x0, Y(AX), PL.x1 + 12, Y(AX), C.axis, 3);
  arrow(X(0), PL.y1, X(0), PL.y0 - 14, C.axis, 3);
  // corte del eje y (de 0 salta a 20)
  const zy = Y(19.6), zx = X(0);
  g.save(); g.fillStyle = C.card; g.fillRect(zx - 14, zy - 12, 28, 24);
  g.strokeStyle = C.axis; g.lineWidth = 3; g.beginPath();
  g.moveTo(zx, zy - 14); g.lineTo(zx - 10, zy - 6); g.lineTo(zx + 10, zy + 2); g.lineTo(zx - 10, zy + 10); g.lineTo(zx, zy + 16); g.stroke(); g.restore();
  const zh = win(T, 18, 22.5) * (.6 + .4 * Math.sin(T * 6));
  if (zh > 0) { g.save(); g.globalAlpha = zh; g.strokeStyle = C.hi; g.lineWidth = 5; g.beginPath(); g.arc(zx, zy, 30, 0, 7); g.stroke(); g.restore(); }
  for (let x = 1; x <= 7; x++) txt(String(x), X(x), Y(AX) + 26, 22, C.soft, { align: 'center', w: 600 });
  for (let f = 20; f <= 28; f++) txt(String(f), X(0) - 14, Y(f), 22, C.soft, { align: 'right', w: 600 });
  txt('0', X(0) - 14, Y(AX) + 22, 22, C.soft, { align: 'right', w: 600 });
  const hl = Math.max(win(T, 14, 18), win(T, 172, 176)) * (.6 + .4 * Math.sin(T * 6));
  const n1 = 'x: horas desde las 9:00 a.m.', n2 = 'f(x): Precio (US$)';
  const w1 = tw(n1, 26, 700), w2 = tw(n2, 26, 700);
  const x1 = PL.x1 - w1 - 6, y1 = Y(AX) - 30, x2 = X(0) + 16, y2 = PL.y0 + 6;
  if (hl > 0) rr(x1 - 10, y1 - 22, w1 + 20, 44, 10, hexA(C.hi, .35 * hl), C.hi, 3, hl);
  if (win(T, 14, 18) > 0) rr(x2 - 10, y2 - 22, w2 + 20, 44, 10, hexA(C.hi, .35 * hl), C.hi, 3, hl);
  txt(n1, x1, y1, 26, C.ink, { w: 700 });
  txt(n2, x2, y2, 26, C.ink, { w: 700 });
}

// ---------- las tres partes ----------
const PIEZAS = [
  { col: C.p1, f: F[0], from: PL.xmin, a: 0, b: 2, draw: [37, 39.5], fallA: 46.8, fallB: 50.8, glow: 53, join: 57 },
  { col: C.p2, f: F[1], from: PL.xmin, a: 2, b: 4, draw: [67.5, 69.5], fallA: 79, fallB: 79, glow: 81, join: 88 },
  { col: C.p3, f: F[2], from: 4, a: 4, b: 7, draw: [110, 112.5], fallA: 0, fallB: 123.6, glow: 124, join: 133 },
];
const CORTES = [
  { c: 0, g0: 44, s0: 44.8, s1: 46.5, end: 52 },
  { c: 2, g0: 48, s0: 48.8, s1: 50.5, end: 52 },
  { c: 2, g0: 74, s0: 74.8, s1: 76.3, end: 80.5 },
  { c: 4, g0: 76.5, s0: 77.3, s1: 78.8, end: 80.5 },
  { c: 7, g0: 121, s0: 121.8, s1: 123.3, end: 125 },
];
function collageAlpha(T) {
  const dim = (a, b) => P(T, a, a + .6) * (1 - P(T, b, b + .6));
  return 1 - .7 * Math.max(dim(62, 88), dim(92, 133));
}
// brillo de un tramo ya pegado (preguntas)
const GLOWS = [[1, 143, 152], [2, 152, 172], [1, 182, 205], [2, 215, 236]];
function drawPieces(T) {
  g.save(); g.beginPath(); g.rect(PL.x0, PL.y0, PL.x1 - PL.x0, Y(AX) - PL.y0); g.clip();
  const ca = collageAlpha(T);
  PIEZAS.forEach((p, i) => {
    if (T < p.draw[0]) return;
    const xEnd = p.from + (PL.xmax - p.from) * lin(T, p.draw[0], p.draw[1]);
    if (T >= p.join) {
      let gl = 1 - P(T, p.join, p.join + 1.5);
      for (const [k, a, b] of GLOWS) if (k === i) gl = Math.max(gl, win(T, a, b, .5));
      if (gl > 0) curve(PL, p.f, p.a, p.b, p.col, 30, { alpha: .3 * gl });
      curve(PL, p.f, p.a, p.b, '#fff', 13, { alpha: ca });
      curve(PL, p.f, p.a, p.b, p.col, 8, { alpha: ca });
      return;
    }
    const gl = P(T, p.glow, p.glow + .5);
    if (gl > 0) curve(PL, p.f, p.a, p.b, p.col, 24, { alpha: .22 * gl });
    curve(PL, p.f, Math.max(p.a, p.from), Math.min(p.b, xEnd), p.col, 6);
    for (const [s0, s1, ft] of [[p.from, p.a, p.fallA], [p.b, PL.xmax, p.fallB]]) {
      const fd = T >= ft ? fallDy(T, ft) : { dy: 0, alpha: 1 };
      if (fd.gone) continue;
      curve(PL, p.f, s0, Math.min(s1, xEnd), p.col, 6, { dy: fd.dy, alpha: fd.alpha });
    }
  });
  g.restore();
}
function drawEndpoints(T) {
  const p1 = P(T, 53.5, 54), p2 = P(T, 81.5, 82), p3 = P(T, 126.5, 127);
  const tapa2 = T >= 85.5, tapa4 = T >= 126.5;
  if (p1 > 0) dot(PL, 0, 20, C.p1, { scale: pop(T, 53.5) });
  if (p1 > 0 && !tapa2) dot(PL, 2, 26, C.p1, { scale: pop(T, 53.5) });
  if (p2 > 0 && T < 133) { dot(PL, 2, 26, C.p2, { hollow: true, scale: pop(T, 81.5) }); dot(PL, 4, 26, C.p2, { hollow: true, scale: pop(T, 81.5) }); }
  if (tapa2) {
    const pu = 1 - P(T, 85.5, 87.5);
    if (pu > 0) { g.save(); g.globalAlpha = pu; g.strokeStyle = C.p1; g.lineWidth = 5; g.beginPath(); g.arc(X(2), Y(26), 20 + 20 * (1 - pu), 0, 7); g.stroke(); g.restore(); }
    dot(PL, 2, 26, C.p1, { scale: pop(T, 85.5) });
  }
  if (tapa4) { dot(PL, 4, 26, C.p3, { scale: pop(T, 126.5) }); dot(PL, 7, raiz(7), C.p3, { scale: pop(T, 126.5) }); }
  if (p2 > 0) {
    const a = win(T, 81.5, 88);
    if (a > 0) { label('○ vacío', X(2) - 16, Y(26) - 40, C.p2, { size: 22, align: 'right', alpha: a }); label('○ vacío', X(4) + 16, Y(26) + 40, C.p2, { size: 22, alpha: a }); }
    const b = win(T, 85.5, 92);
    if (b > 0) label('● lo tapa el tramo 1', X(2) - 16, Y(26) - 40, C.p1, { size: 22, align: 'right', alpha: b });
  }
  const c = win(T, 129, 136);
  if (c > 0) label('● lo tapa el tramo 3', X(4) + 16, Y(26) + 40, C.p3, { size: 22, alpha: c });
}

const FRANJAS = [[0, 2, C.p1, 41, 57], [2, 4, C.p2, 71, 88], [4, 7, C.p3, 118, 133], [2, 4, C.p2, 182, 205], [4, 7, C.p3, 215, 236]];
function drawStrips(T) {
  for (const [a, b, col, t0, t1] of FRANJAS) {
    const al = win(T, t0, t1, .5); if (al <= 0) continue;
    g.save(); g.globalAlpha = al; g.fillStyle = hexA(col, .09);
    g.fillRect(X(a), PL.y0, X(b) - X(a), Y(AX) - PL.y0);
    g.fillStyle = hexA(col, .55); g.fillRect(X(a), Y(AX) - 5, X(b) - X(a), 10);
    g.restore();
  }
}
function tabPoint(T, x, f, col, at, gone, lab) {
  if (T < at || T > gone + .5) return;
  const al = 1 - P(T, gone, gone + .5), pr = P(T, at, at + .8);
  dashLine(X(x), Y(AX), X(x), Y(AX) + (Y(f) - Y(AX)) * pr, hexA(col, .7), al);
  dashLine(X(0), Y(f), X(0) + (X(x) - X(0)) * pr, Y(f), hexA(col, .7), al);
  dot(PL, x, f, col, { scale: pop(T, at + .5), alpha: al });
  if (T > at + .7) label(lab, X(x) + 22, Y(f) + 32, col, { size: 24, alpha: al * P(T, at + .7, at + 1.1) });
}

// ---------- evaluar: marcador en x, subir a la curva, leer el precio ----------
function evaluar(T, xv, t0, t1, tUp, tEnd, col, lab) {
  const al = win(T, t0, tEnd, .5); if (al <= 0) return;
  const x = xv * P(T, t0, t1);
  g.save(); g.globalAlpha = al; g.fillStyle = C.hi;
  g.beginPath(); g.moveTo(X(x), Y(AX) - 4); g.lineTo(X(x) - 13, Y(AX) + 20); g.lineTo(X(x) + 13, Y(AX) + 20); g.closePath(); g.fill(); g.restore();
  label('x = ' + coma(x), X(x) + 18, Y(AX) - 32, C.hiInk, { size: 24, alpha: al });
  if (T < tUp) return;
  const f = (xv < 4 ? 26 : raiz(xv)), up = P(T, tUp, tUp + 1), side = P(T, tUp + 1.2, tUp + 2.2);
  dashLine(X(xv), Y(AX), X(xv), Y(AX) + (Y(f) - Y(AX)) * up, C.hiInk, al, 4);
  if (up >= 1) dot(PL, xv, f, C.hi, { scale: pop(T, tUp + 1), alpha: al });
  if (side > 0) {
    dashLine(X(xv), Y(f), X(xv) + (X(0) - X(xv)) * side, Y(f), C.hiInk, al, 4);
    if (side >= 1) label(lab, X(0) + 12, Y(f) - 32, C.hiInk, { size: 26, alpha: al });
  }
}
function coma(v) { return (Math.round(v * 10) / 10).toFixed(1).replace('.', ',').replace(',0', ''); }
function errorTramo1(T) {
  const al = win(T, 195, 204, .5); if (al <= 0) return;
  g.save(); PL.clip();
  curve(PL, F[0], 2, 2.5 * 1, C.cut, 4, { dash: [8, 8], alpha: al * P(T, 195, 196) });
  g.restore();
  const x = X(2.5), y = Y(27.5), a = al * P(T, 196, 196.5);
  g.save(); g.globalAlpha = a; g.strokeStyle = C.cut; g.lineWidth = 6; g.lineCap = 'round';
  g.beginPath(); g.moveTo(x - 14, y - 14); g.lineTo(x + 14, y + 14); g.moveTo(x + 14, y - 14); g.lineTo(x - 14, y + 14); g.stroke(); g.restore();
  label('27,5 ✗', x + 26, y - 26, C.cut, { size: 24, alpha: a });
}

// ---------- panel derecho ----------
const PX = 1230, PW = 650, LY0 = 645, LH = 275;
const ROWS = [
  { col: C.p1, expr: '3x + 20', dom: '0 ≤ x ≤ 2' },
  { col: C.p2, expr: '26', dom: '2 < x < 4' },
  { col: C.p3, expr: '26 + √(x − 4)', dom: '4 ≤ x ≤ 7' },
];
const FOCO = [[22, 62, 0], [62, 92, 1], [92, 137, 2], [143, 152, 1], [152, 172, 2], [182, 205, 1], [215, 236, 2]];
const DOMHI = [[41, 57, 0], [71, 88, 1], [118, 133, 2], [182, 191, 1], [215, 219, 2]];
function rowState(T, i) {
  let focus = 0, dim = 0;
  for (const [a, b, r] of FOCO) { const w = win(T, a, b, .4); if (r === i) focus = Math.max(focus, w); else dim = Math.max(dim, w); }
  for (let k = 0; k < 3; k++) if (k === i) focus = Math.max(focus, win(T, 7 + k * 1.6, 7 + k * 1.6 + 1.8, .3));
  return { focus, alpha: 1 - .72 * dim * (1 - focus) };
}
function formulaCard(T) {
  const y0 = 130, h = 270;
  rr(PX, y0, PW, h, 22, C.card, C.line, 2);
  txt('f(x) =', PX + 22, y0 + h / 2, 38, C.ink, { w: 700 });
  const bx = PX + 155, top = y0 + 26, bot = y0 + h - 26, mid = (top + bot) / 2;
  g.save(); g.strokeStyle = C.ink; g.lineWidth = 4; g.lineCap = 'round'; g.beginPath();
  g.moveTo(bx + 16, top); g.quadraticCurveTo(bx, top, bx, top + 18); g.lineTo(bx, mid - 18);
  g.quadraticCurveTo(bx, mid, bx - 14, mid); g.quadraticCurveTo(bx, mid, bx, mid + 18);
  g.lineTo(bx, bot - 18); g.quadraticCurveTo(bx, bot, bx + 16, bot); g.stroke(); g.restore();
  const ex = PX + 190, dx = PX + 465;
  ROWS.forEach((r, i) => {
    const yc = y0 + 55 + i * 80, st = rowState(T, i);
    if (st.focus > 0) rr(ex - 14, yc - 34, PW - (ex - PX) + 2, 68, 14, hexA(r.col, .14 * st.focus), hexA(r.col, st.focus), 3);
    g.save(); g.globalAlpha = st.alpha;
    g.fillStyle = r.col; g.beginPath(); g.roundRect(ex - 14, yc - 26, 6, 52, 3); g.fill();
    txt(r.expr, ex + 6, yc, 34, C.ink, { w: 600 });
    let dh = 0; for (const [a, b, k] of DOMHI) if (k === i) dh = Math.max(dh, win(T, a, b, .4));
    if (dh > 0) rr(dx - 8, yc - 22, tw(r.dom, 30, 600) + 16, 44, 8, hexA(C.hi, .45 * dh));
    txt(r.dom, dx, yc, 30, dh > .5 ? C.ink : C.soft, { w: dh > .5 ? 800 : 600 });
    g.restore();
  });
}
const TILES = [['0 a 2', C.p1, 57], ['2 a 4', C.p2, 88], ['4 a 7', C.p3, 133]];
function collageTiles(T) {
  txt('Mi collage', PX + 4, 84, 30, C.ink, { w: 800 });
  const pulse = win(T, 6, 13) * (.5 + .5 * Math.sin(T * 5));
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
  [0, 'Precio de una acción 📈\nfunción por partes'],
  [6, 'Otra vez está partida en 3\n→ hacemos un collage 📸'],
  [14, 'x: horas desde las 9:00 a.m.\nf(x): precio en dólares'],
  [18, 'Ojo: el eje vertical\nempieza en 20 ≈'],
  [22, 'Tramo 1: 3x + 20\nlineal → recta inclinada'],
  [27, 'Tabulamos:\n2 valores de x → f(x)'],
  [36.5, '2 puntos → trazo la recta'],
  [41, 'Solo me importa\n0 ≤ x ≤ 2'],
  [44, '✂ Corto en 0 y en 2'],
  [53, '≤ → puntos rellenos ●'],
  [57, '→ ¡va al collage! 📌'],
  [62, 'Tramo 2: 26\nno hay x → función constante'],
  [67, 'Constante → línea horizontal'],
  [71, 'Solo me importa\n2 < x < 4'],
  [74, '✂ Corto en 2 y en 4'],
  [81, '< sin igual → puntos vacíos ○'],
  [85.5, 'Pero en 2 el tramo 1\ntapa el hueco ●'],
  [88, '→ ¡va al collage! 📌'],
  [92, 'Tramo 3: 26 + √(x − 4)\nfunción raíz cuadrada'],
  [97, 'Empiezo con la original: √x'],
  [102, '− 4 adentro\n→ 4 a la DERECHA'],
  [108, '+ 26 afuera\n→ 26 ARRIBA'],
  [114, 'Ahora arranca en (4; 26)'],
  [118, 'Solo me importa\n4 ≤ x ≤ 7'],
  [121, '✂ Corto en 7'],
  [126, '≤ → puntos rellenos ●'],
  [129, 'En 4 el tramo 3\ntapa el otro hueco ●'],
  [133, '→ ¡va al collage! 📌'],
  [137, '¡Collage listo! 🎉\nEsta es la gráfica de f'],
  [143, 'Pregunta 1: ¿función básica\ndel tramo 2?'],
  [152, 'Pregunta 2: ¿función básica\ndel tramo 3?'],
  [161, 'Pregunta 3: ¿qué técnicas\nusa el tramo 3?'],
  [172, 'Pregunta 4: ¿precio\na las 11:30 a.m.?'],
  [176, 'x = horas desde las 9:00\n9:00 → 11:30 = 2,5 h'],
  [182, '¿En qué tramo cae 2,5?\nEntre 2 y 4 → tramo 2'],
  [187, 'Subo hasta la gráfica\ny leo el precio'],
  [195, '⚠ Si usas el tramo 1 sale 27,5 ✗\n¡Primero busca el tramo!'],
  [205, 'Pregunta 5: ¿precio\na la 1:30 p.m.?'],
  [209, '9:00 a.m. → 1:30 p.m.\n= 4,5 h'],
  [215, '¿En qué tramo cae 4,5?\nEntre 4 y 7 → tramo 3'],
  [219, 'Reemplazo en el tramo 3'],
  [227, 'En la gráfica también\nse ve: ≈ 26,7'],
  [236, 'Para evaluar:\nprimero el tramo, luego reemplazo'],
  [244, '¡Tú puedes, Lu! 💪'],
];

function lowerCard(T) {
  const modes = [[27, 60, tabla1], [62, 90, constante], [95, 137, inset], [143, 172, preg123], [172, 205, preg4], [205, 219, preg5a], [219, 236, preg5b], [236, 248, cierre]];
  let any = 0;
  for (const [a, b, fn] of modes) { const w = win(T, a, b, .4); if (w > 0) { any = Math.max(any, w); g.save(); g.globalAlpha = w; rr(PX, LY0, PW, LH, 22, C.card, C.line, 2); fn(T); g.restore(); } }
  if (any < 1) { g.save(); g.globalAlpha = 1 - any; rr(PX, LY0, PW, LH, 22, null, C.line, 2); g.restore(); }
}
function tabla(T, col, heads, cw, rows) {
  const x0 = PX + 24, y0 = LY0 + 46, rh = 72, W = cw.reduce((a, b) => a + b);
  rr(x0, y0 - 28, W, 56, 10, hexA(col, .12));
  const hx = [x0 + cw[0] / 2, x0 + cw[0] + 16, x0 + cw[0] + cw[1] + 14];
  txt(heads[0], hx[0], y0, 30, col, { w: 800, align: 'center' });
  txt(heads[1], hx[1], y0, 28, col, { w: 800 });
  if (heads[2]) txt(heads[2], hx[2], y0, 28, col, { w: 800 });
  g.save(); g.strokeStyle = C.line; g.lineWidth = 2;
  for (const xx of [x0 + cw[0], x0 + cw[0] + cw[1]].slice(0, cw.length - 1)) { g.beginPath(); g.moveTo(xx, y0 - 28); g.lineTo(xx, y0 + rows.length * rh + 36); g.stroke(); }
  g.restore();
  rows.forEach(([t, at, calc, ac, pt, ap], k) => {
    const y = y0 + (k + 1) * rh;
    txt(t, hx[0], y, 32, C.ink, { w: 700, align: 'center', alpha: P(T, at, at + .4) });
    txt(calc, hx[1], y, 30, C.ink, { w: 600, alpha: P(T, ac, ac + .4) });
    if (pt) txt(pt, hx[2], y, 30, col, { w: 800, alpha: P(T, ap, ap + .4) });
  });
}
const tabla1 = T => tabla(T, C.p1, ['x', 'f(x) = 3x + 20', 'punto'], [90, 340, 170],
  [['0', 29, '3·0 + 20 = 20', 30, '(0; 20)', 31], ['1', 33, '3·1 + 20 = 23', 34, '(1; 23)', 35]]);
function constante(T) {
  txt('f(x) = 26', PX + 28, LY0 + 50, 36, C.p2, { w: 800 });
  txt('No importa la x: siempre vale 26', PX + 28, LY0 + 98, 28, C.ink, { w: 600, alpha: P(T, 63, 63.5) });
  [['x = 2,5', 64], ['x = 3', 65], ['x = 3,5', 66]].forEach(([s, at], k) => {
    const x = PX + 28 + k * 205, a = P(T, at, at + .4);
    rr(x, LY0 + 140, 185, 100, 14, hexA(C.p2, .08), C.p2, 2, a);
    txt(s, x + 92, LY0 + 172, 28, C.ink, { w: 700, align: 'center', alpha: a });
    txt('f = 26', x + 92, LY0 + 212, 30, C.p2, { w: 800, align: 'center', alpha: a });
  });
}
// mini plano: √x en su lugar original y su traslación
function inset(T) {
  const mp = makePlane({ x0: PX + 70, x1: PX + PW - 40, y0: LY0 + 50, y1: LY0 + LH - 50, xmin: -.6, xmax: 8.6, ymin: -.5, ymax: 3.4 });
  txt('Mini plano: así se mueve √x', PX + 24, LY0 + 26, 24, C.soft, { w: 700 });
  g.save(); g.strokeStyle = C.grid; g.lineWidth = 1;
  for (let x = 0; x <= 8; x++) { g.beginPath(); g.moveTo(mp.X(x), mp.y0); g.lineTo(mp.X(x), mp.y1); g.stroke(); }
  g.restore();
  arrow(mp.x0, mp.Y(0), mp.x1 + 8, mp.Y(0), C.axis, 2);
  arrow(mp.X(0), mp.y1, mp.X(0), mp.y0 - 8, C.axis, 2);
  for (const x of [0, 4, 7]) txt(String(x), mp.X(x), mp.Y(0) + 20, 20, C.soft, { align: 'center', w: 700 });
  const h = 4 * P(T, 102.5, 105), dr = lin(T, 97.5, 99);
  if (h > 0) curve(mp, x => Math.sqrt(Math.max(0, x)), 0, 8.6, C.p3, 3, { dash: [8, 8], alpha: .5 });
  if (dr > 0) curve(mp, x => Math.sqrt(x - h), h, h + (8.6 - h) * dr, C.p3, 5);
  if (dr > 0) dot(mp, h, 0, C.p3, { r: 9 });
  const a1 = win(T, 102.5, 108.5);
  if (a1 > 0) { arrow(mp.X(0), mp.Y(2.6), mp.X(4), mp.Y(2.6), C.p3, 4, a1); label('4 a la derecha', mp.X(2), mp.Y(2.6) - 30, C.p3, { size: 20, align: 'center', alpha: a1 }); }
  const a2 = win(T, 108.5, 116);
  if (a2 > 0) {
    const bounce = Math.sin(T * 5) * 6;
    arrow(mp.X(4), mp.Y(0) - 10, mp.X(4), mp.y0 - 30 + bounce, C.p3, 6, a2);
    label('26 arriba ↑', mp.X(4) + 16, mp.Y(1.6), C.p3, { size: 22, alpha: a2 });
  }
}
function filas(T, L) {
  L.forEach(([q, a, at, ac], k) => {
    const y = LY0 + 42 + k * 50;
    const w = txt(q, PX + 26, y, 26, C.soft, { w: 700, alpha: P(T, at, at + .4) });
    txt(a, PX + 34 + w, y, 26, C.ink, { w: 800, alpha: P(T, ac, ac + .4) });
  });
}
const preg123 = T => filas(T, [
  ['1) Tramo 2 →', 'función constante', 143, 147],
  ['2) Tramo 3 →', 'función raíz cuadrada', 152, 156],
  ['3) Técnicas del tramo 3:', '', 161, 161],
  ['     • Traslación horizontal →', '4 a la derecha', 165, 165],
  ['     • Traslación vertical →', '26 arriba', 166.5, 166.5],
]);
function hora(h) { const H = Math.floor(h), m = Math.floor((h - H) * 60); const hh = H > 12 ? H - 12 : H; return `${hh}:${String(m).padStart(2, '0')} ${H >= 12 ? 'p.m.' : 'a.m.'}`; }
function reloj(cx, cy, r, h, alpha = 1) {
  g.save(); g.globalAlpha *= alpha;
  g.beginPath(); g.arc(cx, cy, r, 0, 7); g.fillStyle = '#fff'; g.fill(); g.lineWidth = 5; g.strokeStyle = C.ink; g.stroke();
  for (let k = 0; k < 12; k++) { const a = k / 12 * Math.PI * 2; g.lineWidth = k % 3 ? 2 : 4; g.beginPath(); g.moveTo(cx + Math.sin(a) * r * .8, cy - Math.cos(a) * r * .8); g.lineTo(cx + Math.sin(a) * r * .92, cy - Math.cos(a) * r * .92); g.stroke(); }
  const ah = (h % 12) / 12 * Math.PI * 2, am = (h % 1) * Math.PI * 2;
  g.lineCap = 'round'; g.lineWidth = 7; g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + Math.sin(ah) * r * .5, cy - Math.cos(ah) * r * .5); g.stroke();
  g.strokeStyle = C.hi; g.lineWidth = 5; g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + Math.sin(am) * r * .78, cy - Math.cos(am) * r * .78); g.stroke();
  g.fillStyle = C.ink; g.beginPath(); g.arc(cx, cy, 6, 0, 7); g.fill();
  g.restore();
}
function relojCard(T, t0, t1, hFin, tTramo, tramo, col) {
  const h = 9 + (hFin - 9) * P(T, t0, t1);
  reloj(PX + 110, LY0 + 120, 82, h);
  txt(hora(h), PX + 110, LY0 + 240, 28, C.ink, { w: 800, align: 'center' });
  txt('9:00 a.m. → ' + hora(hFin), PX + 230, LY0 + 50, 28, C.soft, { w: 700 });
  txt('x = ' + coma(h - 9) + ' horas', PX + 230, LY0 + 105, 40, C.hiInk, { w: 800 });
  const a = P(T, tTramo, tTramo + .4);
  if (a > 0) { rr(PX + 222, LY0 + 150, 400, 60, 12, hexA(col, .12), col, 3, a); txt(tramo, PX + 240, LY0 + 181, 28, C.ink, { w: 800, alpha: a }); }
}
function respuesta(T, s, at, col) {
  const a = P(T, at, at + .4); if (a <= 0) return;
  rr(PX + 20, LY0 + LH - 74, PW - 40, 58, 14, hexA(col, .15), col, 3, a);
  txt(s, PX + PW / 2, LY0 + LH - 45, 32, C.ink, { w: 800, align: 'center', alpha: a });
}
function preg4(T) {
  if (T < 191) relojCard(T, 176, 180, 11.5, 182, 'Tramo 2: 2 < x < 4', C.p2);
  else { const a = P(T, 191, 191.4); txt('f(2,5) = 26', PX + PW / 2, LY0 + 100, 52, C.p2, { w: 800, align: 'center', alpha: a }); txt('(en el tramo 2 siempre vale 26)', PX + PW / 2, LY0 + 160, 26, C.soft, { w: 600, align: 'center', alpha: a }); respuesta(T, 'Precio a las 11:30 a.m.: US$ 26', 191.5, C.hi); }
}
const preg5a = T => relojCard(T, 209, 213, 13.5, 215, 'Tramo 3: 4 ≤ x ≤ 7', C.p3);
function preg5b(T) {
  [['f(4,5) = 26 + √(4,5 − 4)', 219.5], ['= 26 + √0,5', 222.5], ['≈ 26 + 0,71 = 26,71', 225]].forEach(([s, at], k) =>
    txt(s, PX + 30 + (k ? 74 : 0), LY0 + 46 + k * 52, 32, C.ink, { w: 700, alpha: P(T, at, at + .4) }));
  respuesta(T, 'Precio a la 1:30 p.m.: ≈ US$ 26,71', 230, C.hi);
}
const cierre = T => filas(T, [
  ['1)', 'Arma el collage tramo por tramo', 236, 236],
  ['2)', 'Pasa la hora a x (horas desde 9:00)', 237.5, 237.5],
  ['3)', 'Busca en qué tramo cae x', 239, 239],
  ['4)', 'Reemplaza solo en ese tramo', 240.5, 240.5],
]);

function intro(T) {
  const al = win(T, .2, 6, .6); if (al <= 0) return;
  const cx = (PL.x0 + PL.x1) / 2, cy = 420;
  rr(cx - 400, cy - 120, 800, 240, 28, '#fff', C.line, 3, al);
  txt('TecnoGlobal 📈', cx, cy - 40, 60, C.ink, { w: 800, align: 'center', alpha: al });
  txt('función por partes + evaluar', cx, cy + 45, 38, C.p2, { w: 700, align: 'center', alpha: al });
}

function render(T) {
  g.setTransform(1, 0, 0, 1, 0, 0);
  g.fillStyle = C.bg; g.fillRect(0, 0, 1920, 1080);
  drawPlane(T);
  drawStrips(T);
  g.save(); g.beginPath(); g.rect(PL.x0 - 30, PL.y0 - 30, PL.x1 - PL.x0 + 60, PL.y1 - PL.y0 + 30); g.clip();
  drawPieces(T);
  tabPoint(T, 0, 20, C.p1, 31, 57, '(0; 20)');
  tabPoint(T, 1, 23, C.p1, 35, 57, '(1; 23)');
  if (win(T, 112.5, 118) > 0) label('(4; 26)', X(4) + 18, Y(26) - 34, C.p3, { size: 24, alpha: win(T, 112.5, 118) });
  drawEndpoints(T);
  errorTramo1(T);
  evaluar(T, 2.5, 176, 180, 187, 205, C.p2, '26');
  evaluar(T, 4.5, 209, 213, 227, 236, C.p3, '≈ 26,71');
  g.restore();
  for (const k of CORTES) drawCut(PL, T, k, 'x', PL.y0 + 250);
  intro(T);
  collageTiles(T);
  formulaCard(T);
  noteCard(T, NOTAS, PX, 420, PW, 205);
  lowerCard(T);
  // barra de progreso discreta para la clase en vivo
  g.fillStyle = hexA(C.ink, .12); g.fillRect(40, 1000, 1840, 8);
  g.fillStyle = C.p2; g.fillRect(40, 1000, 1840 * T / DURATION, 8);
  const sec = current([[0, 'Inicio'], [22, 'Tramo 1'], [62, 'Tramo 2'], [92, 'Tramo 3'], [137, 'Gráfica final'], [143, 'Preguntas 1–3'], [172, 'Pregunta 4'], [205, 'Pregunta 5'], [236, 'Resumen']], T);
  txt(sec[1], 40, 970, 26, C.soft, { w: 700 });
}
