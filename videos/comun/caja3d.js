// Caja de cartón en 3D (proyección ortogonal dibujada a mano), compartida por los videos de la caja.
// Medidas de la caja óptima: ancho x = 10, largo y = 20, alto 10.
const BX = 10, BY = 20, H = 10;

// ---------- caras de la plancha en coordenadas (u, v) en cm ----------
const R = Math.PI / 2;
const FACES = [
  { id: 'base', r: [0, BX, 0, BY], m: (u, v) => [u, v, 0] },
  { id: 'izq', r: [-H, 0, 0, BY], m: (u, v, th) => [u * Math.cos(th), v, -u * Math.sin(th)] },
  { id: 'der', r: [BX, BX + H, 0, BY], m: (u, v, th) => [BX + (u - BX) * Math.cos(th), v, (u - BX) * Math.sin(th)] },
  { id: 'frente', r: [0, BX, -H, 0], m: (u, v, th) => [u, v * Math.cos(th), -v * Math.sin(th)] },
  { id: 'fondo', r: [0, BX, BY, BY + H], m: (u, v, th) => [u, BY + (v - BY) * Math.cos(th), (v - BY) * Math.sin(th)] },
  { id: 'tapa', r: [BX + H, 2 * BX + H, 0, BY], m: (u, v, th, ph) => { const e = u - BX - H, a = th + ph; return [BX + H * Math.cos(th) + e * Math.cos(a), v, H * Math.sin(th) + e * Math.sin(a)]; } },
];
// recortes de las esquinas (desperdicio), solo en la plancha plana
const WASTE = [[-H, 0, BY, BY + H], [BX, BX + H, BY, BY + H], [BX + H, 2 * BX + H, BY, BY + H], [-H, 0, -H, 0], [BX, BX + H, -H, 0], [BX + H, 2 * BX + H, -H, 0]];

// ---------- cámara ----------
function camera(T, f, view = {}) {
  const k = f.w;
  const yaw = (-34 + 8 * Math.sin(T * .35)) * k * Math.PI / 180;
  const pitch = (90 - 58 * k) * Math.PI / 180;
  const s = (view.sFlat ?? 15) + ((view.sBox ?? 23) - (view.sFlat ?? 15)) * k;
  // armada se centra en la caja; plana, en el centro de la plancha (u = x/2 + 5)
  const c = [BX / 2 + 5 * (1 - k), BY / 2, H / 2 * k];
  return { yaw, pitch, s, c, cx: view.cx ?? 620, cy: view.cy ?? 480 };
}
function proj(cam, p) {
  const dx = p[0] - cam.c[0], dy = p[1] - cam.c[1], dz = p[2] - cam.c[2];
  const u1 = dx * Math.cos(cam.yaw) - dy * Math.sin(cam.yaw), v1 = dx * Math.sin(cam.yaw) + dy * Math.cos(cam.yaw);
  const up = v1 * Math.sin(cam.pitch) + dz * Math.cos(cam.pitch);
  const depth = -v1 * Math.cos(cam.pitch) + dz * Math.sin(cam.pitch);
  return { x: cam.cx + cam.s * u1, y: cam.cy - cam.s * up, d: depth };
}

const CART = { out: [217, 160, 102], in: [196, 140, 86] };
// f = {w: paredes, t: tapa} entre 0 (plano) y 1 (armado); hilite = [[cara, color, desde, hasta], ...]
function drawBox(T, alpha, f, hilite = [], view = {}) {
  const cam = camera(T, f, view);
  if (alpha <= 0) return cam;
  const th = f.w * R, ph = f.t * R;
  g.save(); g.globalAlpha = alpha;
  // recortes de las esquinas
  const wa = (1 - clamp(f.w * 4)) * .9;
  if (wa > 0) for (const [u0, u1, v0, v1] of WASTE) {
    const q = [[u0, v0], [u1, v0], [u1, v1], [u0, v1]].map(([u, v]) => proj(cam, [u, v, 0]));
    g.save(); g.globalAlpha = alpha * wa; g.beginPath(); q.forEach((p, i) => i ? g.lineTo(p.x, p.y) : g.moveTo(p.x, p.y)); g.closePath();
    g.fillStyle = '#efe8dc'; g.fill(); g.setLineDash([8, 7]); g.strokeStyle = '#b9ad99'; g.lineWidth = 2; g.stroke(); g.restore();
  }
  const list = FACES.map(F => {
    const [u0, u1, v0, v1] = F.r;
    const P3 = [[u0, v0], [u1, v0], [u1, v1], [u0, v1]].map(([u, v]) => F.m(u, v, th, ph));
    const q = P3.map(p => proj(cam, p));
    const depth = q.reduce((a, p) => a + p.d, 0) / 4;
    // normal "de adentro" (en la plancha apunta hacia arriba)
    const e1 = P3[1].map((x, i) => x - P3[0][i]), e2 = P3[3].map((x, i) => x - P3[0][i]);
    const n = [e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0]];
    const nl = Math.hypot(...n); n.forEach((_, i) => n[i] /= nl);
    const nc = proj(cam, P3[0].map((x, i) => x + n[i])), oc = proj(cam, P3[0]);
    const inside = nc.d - oc.d > 0;
    const light = .78 + .22 * Math.abs(n[2]) - .1 * Math.abs(n[0]);
    return { F, q, depth, inside, light };
  }).sort((a, b) => a.depth - b.depth);
  for (const { F, q, inside, light } of list) {
    const c = inside ? CART.in : CART.out, l = light;
    g.beginPath(); q.forEach((p, i) => i ? g.lineTo(p.x, p.y) : g.moveTo(p.x, p.y)); g.closePath();
    g.fillStyle = `rgb(${c[0] * l | 0},${c[1] * l | 0},${c[2] * l | 0})`; g.fill();
    for (const [id, col, a, b] of hilite) if (id === F.id) { const w = win(T, a, b, .4); if (w > 0) { g.fillStyle = hexA(col, .45 * w); g.fill(); } }
    g.lineJoin = 'round'; g.strokeStyle = '#7a5530'; g.lineWidth = 2.5; g.stroke();
    // nombre sobre la cara (solo con la plancha casi plana)
    const ta = 1 - clamp(f.w * 3);
    if (ta > 0 && (F.id === 'base' || F.id === 'tapa')) faceText(q, F.id === 'base' ? 'Base' : 'Tapa', ta);
  }
  g.restore();
  return cam;
}
function faceText(q, s, a) {
  const cx = (q[0].x + q[2].x) / 2, cy = (q[0].y + q[2].y) / 2;
  txt(s, cx, cy, 36, '#5b3a1a', { w: 800, align: 'center', alpha: a });
}
// cota entre dos puntos 3D, desplazada por off (3D)
function cota(cam, a, b, off, s, col, alpha) {
  if (alpha <= 0) return;
  const A = proj(cam, a.map((x, i) => x + off[i])), B = proj(cam, b.map((x, i) => x + off[i]));
  g.save(); g.globalAlpha = alpha; g.strokeStyle = col; g.lineWidth = 3;
  g.beginPath(); g.moveTo(A.x, A.y); g.lineTo(B.x, B.y); g.stroke();
  const ang = Math.atan2(B.y - A.y, B.x - A.x) + Math.PI / 2;
  for (const P0 of [A, B]) { g.beginPath(); g.moveTo(P0.x - Math.cos(ang) * 10, P0.y - Math.sin(ang) * 10); g.lineTo(P0.x + Math.cos(ang) * 10, P0.y + Math.sin(ang) * 10); g.stroke(); }
  g.restore();
  label(s, (A.x + B.x) / 2, (A.y + B.y) / 2, col, { size: 26, align: 'center', alpha });
}
