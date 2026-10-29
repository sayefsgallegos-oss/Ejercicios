"""Matti y Numi: La señal perdida — Capítulo 2: ¿Dónde está Numi?
Cuadrados perfectos (pista 25), Matemópolis, el Señor Cero (n × 0 = 0) y la clave 7 × 8 − 6 × 9."""
import io
import random
from PIL import Image
from robots import *
import robots
from rr_novela_cap1 import night
from mision import mission, answer_box, frac

DUR = 71.0
USER = "@gustavo.alvarado4"
LAB, SQ, TP, CITY, MEET, SPELL, MISSION, TOWER, END = 6.5, 14.0, 22.0, 27.0, 36.0, 41.8, 47.6, 54.0, 63.0
GROUND = 1520
FLOOR = 1660
rng = random.Random(4)

DIALOG = [
    (7.0, 10.0, "matti", ["La pista…", "¡ustedes la resolvieron!"]),
    (14.4, 17.4, "matti", ["Son cuadrados", "perfectos."]),
    (19.0, 21.8, "matti", ["5 × 5 = 25.", "¡Esa es la clave!"]),
    (22.4, 24.4, "matti", ["Clave 25…", "¡activando!"]),
    (28.8, 31.4, "matti", ["¿Esto es…", "Matemópolis?"]),
    (32.4, 35.8, "equis", ["¡Shh! ¡Escóndete,", "viene el Señor Cero!"]),
    (36.8, 38.2, "siete", ["¡Buen día!"]),
    (38.8, 41.6, "cero", ["Ja, ja… ¡todo lo que", "toco se vuelve cero!"]),
    (44.4, 47.4, "equis", ["Cualquier número", "por cero… ¡es cero!"]),
    (48.2, 51.0, "equis", ["Tiene a tu amigo", "en su torre."]),
    (51.4, 53.6, "matti", ["¡Vamos por Numi!"]),
    (55.2, 57.0, "numi", ["¡MATTI!"]),
    (59.4, 62.6, "cero", ["Nadie escapa", "de mí…"]),
]
cast = Cast(DIALOG)
robots.VOICE.update(equis=62, cero=45, siete=72)

# ---------- sprites nuevos (assets/robots_v2), con variantes "@gray" y "@shadow" ----------
V2 = os.path.join(HERE, "assets", "robots_v2")
_S2 = {}

def s2(key):
    if key not in _S2:
        name, _, var = key.partition("@")
        path = os.path.join(V2, name + ".png")
        if not var:
            _S2[key] = cairo.ImageSurface.create_from_png(path)
        else:
            a = np.array(Image.open(path).convert("RGBA")).astype(float)
            if var == "gray":
                a[..., :3] = a[..., :3].mean(2, keepdims=True) * 0.85 + 25
            elif var == "shadow":
                a[..., :3] = 12
            buf = io.BytesIO(); Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(buf, "PNG"); buf.seek(0)
            _S2[key] = cairo.ImageSurface.create_from_png(buf)
    return _S2[key]

def put(ctx, key, cx, bottom, h, alpha=1.0, rot=0.0, flip=False, sx=1.0, sy=1.0):
    if alpha <= 0.001 or h <= 1: return
    s = s2(key); k = h / s.get_height()
    ctx.save(); ctx.translate(cx, bottom); ctx.rotate(rot)
    ctx.scale(k * sx * (-1 if flip else 1), k * sy)
    ctx.translate(-s.get_width() / 2, -s.get_height())
    ctx.set_source_surface(s); ctx.get_source().set_filter(cairo.FILTER_BEST)
    ctx.paint_with_alpha(alpha); ctx.restore()

def actor(ctx, t, key, x, floor, h, alpha=1.0, who=None, fly=False, ph=0.0, flip=False, rot=0.0):
    """Personaje en escena: los robots flotan, los números se apoyan en el piso. Devuelve su cabeza."""
    hov = 12 * math.sin(t * 2.3 + ph) if fly else 0
    tk = cast.talking(who, t) if who else False
    sy = 1 + (0.035 * abs(math.sin(t * 14)) if tk else 0) + (0 if fly else 0.012 * math.sin(t * 3 + ph))
    floor_shadow(ctx, x, floor, h * 0.3, alpha)
    lift = 26 + hov if fly else 4
    put(ctx, key, x, floor - lift, h, alpha, rot, flip, 1 / sy ** 0.5, sy)
    return (x, floor - lift - h * 0.98)

def fade_black(ctx, t, at, d=0.35):
    a = 1 - abs(t - at) / d
    if a > 0:
        ctx.rectangle(-20, -20, W + 40, H + 40); ctx.set_source_rgba(0, 0, 0, a); ctx.fill()

def mix(col, g, to=(0.62, 0.65, 0.70)):
    r, gg, b, _ = hexc(col)
    return tuple(c * (1 - g) + d * g for c, d in zip((r, gg, b), to))

# ---------- escenarios ----------
BUILD = [(130, "4", 560, "#F2C230", False), (330, "9", 690, "#4FA8F5", True), (560, "2", 600, "#E8503A", False),
         (790, "6", 720, "#B5763E", True), (990, "5", 580, "#2FD3D3", False)]

def city(ctx, t, tower=0.0):
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0, 0.55, 0.62, 0.72); g.add_color_stop_rgb(1, 0.82, 0.85, 0.88)
    ctx.set_source(g); ctx.paint()
    ctx.arc(820, 420, 90, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.35); ctx.fill()
    for i in range(14):   # skyline lejano
        x = i * 85 - 20; h = 180 + 140 * ((i * 37) % 5) / 4
        ctx.rectangle(x, GROUND - h - 120, 70, h + 120); ctx.set_source_rgba(0.45, 0.5, 0.58, 0.35); ctx.fill()
    if tower > 0:   # la torre del Señor Cero, a lo lejos
        a = tower; tx = 900
        ctx.rectangle(tx - 70, 560, 140, GROUND - 560); ctx.set_source_rgba(0.12, 0.12, 0.15, a); ctx.fill()
        ctx.move_to(tx - 100, 570); ctx.line_to(tx, 380); ctx.line_to(tx + 100, 570); ctx.close_path(); ctx.fill()
        for yy in (650, 820, 990):
            rrect(ctx, tx - 22, yy, 44, 70, 22); ctx.set_source_rgba(1, 0.25, 0.3, a * (0.6 + 0.4 * math.sin(t * 4 + yy))); ctx.fill()
    for x, gl, size, col, missing in BUILD:
        font(ctx, size, "Fredoka"); ext = ctx.text_extents(gl)
        tx = x - ext.x_advance / 2
        ctx.save(); ctx.move_to(tx, GROUND); ctx.text_path(gl)
        if missing:
            ctx.set_dash([22, 16]); ctx.set_line_width(7); ctx.set_source_rgba(1, 1, 1, 0.55); ctx.stroke()
        else:
            path = ctx.copy_path()
            ctx.set_source_rgb(*mix(col, 0.6)); ctx.fill_preserve(); ctx.clip()
            for wy in range(int(GROUND - ext.height), GROUND - 40, 70):
                for wx in range(int(tx), int(tx + ext.x_advance), 56):
                    ctx.rectangle(wx + 14, wy + 16, 24, 34)
            ctx.set_source_rgba(0.95, 0.92, 0.75, 0.35); ctx.fill()
            ctx.reset_clip(); ctx.new_path(); ctx.append_path(path)
            ctx.set_line_width(6); ctx.set_source_rgba(0.2, 0.22, 0.28, 0.6); ctx.stroke()
        ctx.restore()
    ctx.rectangle(0, GROUND, W, H - GROUND); ctx.set_source_rgb(0.42, 0.44, 0.48); ctx.fill()
    ctx.rectangle(0, GROUND, W, 26); ctx.set_source_rgb(0.62, 0.64, 0.68); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.5)
    for x in range(-40, W, 160):
        ctx.rectangle(x + (t * 0) % 160, 1790, 90, 14); ctx.fill()

def tower_room(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.10, 0.08, 0.16); g.add_color_stop_rgb(1, 0.20, 0.14, 0.26)
    ctx.set_source(g); ctx.paint()
    ctx.set_line_width(3); ctx.set_source_rgba(1, 1, 1, 0.06)
    for r, y in enumerate(range(200, H, 90)):
        ctx.move_to(0, y); ctx.line_to(W, y)
        for x in range(-90 + (r % 2) * 90, W, 180): ctx.move_to(x, y); ctx.line_to(x, y + 90)
    ctx.stroke()
    rrect(ctx, W / 2 - 110, 300, 220, 300, 110); ctx.set_source_rgba(0.05, 0.05, 0.12, 1); ctx.fill()
    ctx.arc(W / 2 + 30, 400, 50, 0, 2 * math.pi); ctx.set_source_rgba(0.95, 0.95, 0.85, 0.9); ctx.fill()
    for i in range(3):
        ctx.move_to(W / 2 - 110 + i * 110 + 55, 300); ctx.line_to(W / 2 - 110 + i * 110 + 55, 600)
    ctx.set_line_width(10); ctx.set_source_rgb(0.12, 0.1, 0.18); ctx.stroke()
    ctx.rectangle(0, 1640, W, H - 1640); ctx.set_source_rgb(0.14, 0.11, 0.2); ctx.fill()

def cage(ctx, cx, top, bottom, w, alpha=1.0):
    ctx.save(); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgba(0.25, 0.24, 0.3, alpha); ctx.set_line_width(18)
    for i in range(7):
        x = cx - w / 2 + i * w / 6
        ctx.move_to(x, top + 40); ctx.line_to(x, bottom)
    ctx.stroke()
    ctx.set_source_rgba(0.6, 0.6, 0.68, 0.5 * alpha); ctx.set_line_width(5)
    for i in range(7):
        x = cx - w / 2 + i * w / 6 - 4
        ctx.move_to(x, top + 50); ctx.line_to(x, bottom - 10)
    ctx.stroke()
    ctx.set_source_rgba(0.25, 0.24, 0.3, alpha)
    ctx.save(); ctx.translate(cx, top + 40); ctx.scale(w / 2, 90)
    ctx.arc(0, 0, 1, math.pi, 2 * math.pi); ctx.restore(); ctx.set_line_width(22); ctx.stroke()
    rrect(ctx, cx - w / 2 - 20, bottom - 10, w + 40, 40, 16); ctx.fill()
    ctx.restore()

def padlock(ctx, x, y, k, alpha=1.0):
    if k <= 0.001: return
    ctx.save(); ctx.translate(x, y); sc(ctx, k)
    ctx.arc(0, -70, 60, math.pi, 2 * math.pi); ctx.set_line_width(22); ctx.set_source_rgba(0.75, 0.6, 0.2, alpha); ctx.stroke()
    rrect(ctx, -90, -70, 180, 150, 26); ctx.set_source_rgba(*hexc("#F2C230", alpha)); ctx.fill()
    ctx.arc(0, -10, 16, 0, 2 * math.pi); ctx.set_source_rgba(0.2, 0.15, 0.05, alpha); ctx.fill()
    ctx.rectangle(-7, -5, 14, 40); ctx.fill()
    ctx.restore()

def gray_zero(ctx, x, floor, h, alpha):
    """El 7 convertido en un 0 gris y triste."""
    if alpha <= 0: return
    floor_shadow(ctx, x, floor, h * 0.3, alpha)
    font(ctx, h, "Fredoka"); ext = ctx.text_extents("0")
    ctx.save(); ctx.move_to(x - ext.x_advance / 2, floor - 40); ctx.text_path("0")
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_line_width(12)
    ctx.set_source_rgba(0.25, 0.27, 0.32, alpha); ctx.stroke_preserve()
    ctx.set_source_rgba(0.68, 0.70, 0.74, alpha); ctx.fill(); ctx.restore()
    cy = floor - 40 - ext.height * 0.62
    for dx in (-38, 38):
        ctx.arc(x + dx, cy, 22, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, alpha); ctx.fill()
        ctx.arc(x + dx, cy + 6, 10, 0, 2 * math.pi); ctx.set_source_rgba(0.1, 0.1, 0.15, alpha); ctx.fill()
    for dx in (-60, 60):
        ctx.save(); ctx.translate(x + dx, floor - 20); ctx.scale(1.8, 1)
        ctx.arc(0, 0, 22, 0, 2 * math.pi); ctx.restore(); ctx.set_source_rgba(0.9, 0.9, 0.9, alpha); ctx.fill()

def puff(ctx, x, y, p, alpha=1.0):
    if not (0 < p < 1): return
    for i in range(10):
        a = i * 2 * math.pi / 10
        rr = 40 + 170 * ease_out(p)
        ctx.arc(x + math.cos(a) * rr, y + math.sin(a) * rr * 0.7, 80 * (1 - p * 0.6), 0, 2 * math.pi)
        ctx.set_source_rgba(0.85, 0.86, 0.9, 0.9 * (1 - p) * alpha); ctx.fill()

def big_card(ctx, t, st, en, parts_lines, y=760, w=820):
    k = pop(t, st, 0.45) * (1 - prog(t, en - 0.25, en))
    if k <= 0.001: return
    h = 70 + sum(s for _, s in parts_lines) * 1.25
    ctx.save(); ctx.translate(W / 2, y); sc(ctx, k)
    rrect(ctx, -w / 2, -h / 2 + 10, w, h, 40); ctx.set_source_rgba(0.02, 0.05, 0.2, 0.25); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, 40); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    yy = -h / 2 + 35
    for parts, size in parts_lines:
        yy += size * 0.62
        segs(ctx, parts, 0, yy, size)
        yy += size * 0.63
    ctx.restore()

_WIN = None
def winner_card(ctx, t, st, en):
    """'¡El primer lector en resolverlo!' con la captura del perfil de TikTok tal cual."""
    global _WIN
    if _WIN is None: _WIN = cairo.ImageSurface.create_from_png(os.path.join(HERE, "assets", "ganador_cap1.png"))
    k = pop(t, st, 0.5) * (1 - prog(t, en - 0.25, en))
    if k <= 0.001: return
    iw = 880; ih = iw * _WIN.get_height() / _WIN.get_width()
    w, h = iw + 60, ih + 330
    ctx.save(); ctx.translate(W / 2, 760); sc(ctx, k)
    rrect(ctx, -w / 2, -h / 2 + 12, w, h, 44); ctx.set_source_rgba(0.02, 0.05, 0.2, 0.3); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, 44); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, 44); ctx.set_line_width(10); ctx.set_source_rgba(*hexc("#F2C230")); ctx.stroke()
    pill(ctx, 0, -h / 2, "PRIMERO EN ACERTAR", 40, "#F2C230", NAVY, 1, 1, padx=30, pady=14)
    segs(ctx, [("¡El primer lector", NAVY)], 0, -h / 2 + 95, 58)
    segs(ctx, [("en resolverlo!", NAVY), ("  La clave era ", GREY), ("25", PINK)], 0, -h / 2 + 165, 46)
    y0 = -h / 2 + 220
    ctx.save(); rrect(ctx, -iw / 2, y0, iw, ih, 24); ctx.clip()
    ctx.translate(-iw / 2, y0); ctx.scale(iw / _WIN.get_width(), iw / _WIN.get_width())
    ctx.set_source_surface(_WIN); ctx.get_source().set_filter(cairo.FILTER_BEST); ctx.paint(); ctx.restore()
    rrect(ctx, -iw / 2, y0, iw, ih, 24); ctx.set_line_width(3); ctx.set_source_rgba(0.85, 0.88, 0.93, 1); ctx.stroke()
    ctx.restore()

# ---------- escenas ----------
CLIPS = [(0.0, 2.2, 23.6), (2.2, 4.4, 33.0), (4.4, 6.0, 38.8)]   # (desde, hasta, segundo del cap. 1)

def scene_recap(ctx, t):
    """'Anteriormente…': momentos reales del capítulo 1 en blanco y negro, con viñeta, grano y rebobinado."""
    if t >= LAB: return
    import rr_novela_cap1 as cap1
    t1 = None
    for a, b, src in CLIPS:
        if a <= t < b: t1 = src + (t - a)
    if t1 is None: t1 = 40.6
    cap1.draw(ctx, t1)
    ctx.set_operator(cairo.OPERATOR_HSL_SATURATION); ctx.set_source_rgb(0.5, 0.5, 0.5); ctx.paint()
    ctx.set_operator(cairo.OPERATOR_OVER)
    rg = cairo.RadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1150)
    rg.add_color_stop_rgba(0, 0, 0, 0, 0); rg.add_color_stop_rgba(1, 0, 0, 0, 0.75)
    ctx.set_source(rg); ctx.paint()
    r = random.Random(int(t * 24))
    for _ in range(500):
        ctx.rectangle(r.uniform(0, W), r.uniform(0, H), 3, 3)
    ctx.set_source_rgba(1, 1, 1, 0.12); ctx.fill()
    for a, b, src in CLIPS[1:]:
        f = 1 - abs(t - a) / 0.12
        if f > 0: ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(1, 1, 1, 0.6 * f); ctx.fill()
    text(ctx, "Anteriormente…", W / 2, 300, 66, WHITE, "Nunito ExtraBold", alpha=ease_out(prog(t, 0.2, 0.6)), outline=NAVY, ow=10)
    if t >= 6.0:   # rebobinado
        p = prog(t, 6.0, LAB)
        r = random.Random(int(t * 60))
        for _ in range(14):
            y = r.uniform(0, H); ctx.rectangle(0, y, W, r.uniform(4, 30))
            ctx.set_source_rgba(1, 1, 1, 0.35); ctx.fill()
        for i in range(2):
            x = W / 2 - 60 + i * 80
            ctx.move_to(x + 40, 860); ctx.line_to(x - 30, 960); ctx.line_to(x + 40, 1060); ctx.close_path()
            ctx.set_source_rgba(1, 1, 1, 0.9 * (1 - p)); ctx.fill()

def scene_lab(ctx, t):
    if not (LAB <= t < CITY): return
    night(ctx, t)
    heads = {}
    if t < SQ:
        key = "matti_nov_a00" if t < 10.4 else "matti_prof03"
        heads["matti"] = actor(ctx, t, key, W / 2, 1720, 430, ease_out(prog(t, LAB, LAB + 0.5)), "matti", True)
        if t >= 10.4: confetti(ctx, t, 10.5, W / 2, 560)
        winner_card(ctx, t, 10.4, SQ)
    elif t < TP:
        heads["matti"] = actor(ctx, t, "matti_prof04", 200, 1760, 360, 1, "matti", True)
        seq = [1, 4, 9, 16, 25]
        step = sum(1 for k in range(5) if t >= SQ + 1.0 + k * 1.1)
        for i, v in enumerate(seq):
            on = i < step
            pill(ctx, W / 2 - 340 + i * 170, 380, str(v), 54, PINK if i == step - 1 else (WHITE if on else "#5A6E8C"),
                 WHITE if i == step - 1 else NAVY, 1, 1, padx=26, pady=12)
        s = 96; n = max(1, step)
        x0, y0 = W / 2 - 5 * s / 2 + 60, 500
        for r in range(n):
            for c in range(n):
                new = r == n - 1 or c == n - 1
                k = pop(t, SQ + 1.0 + (n - 1) * 1.1 + (r + c) * 0.03, 0.3) if new and step else 1
                if step == 0: continue
                ctx.save(); ctx.translate(x0 + c * s + s / 2, y0 + r * s + s / 2); sc(ctx, k)
                rrect(ctx, -s / 2 + 5, -s / 2 + 5, s - 10, s - 10, 14)
                ctx.set_source_rgba(*hexc(GREEN if not new else "#7DE3A8")); ctx.fill(); ctx.restore()
        if step:
            text(ctx, f"{n} × {n} = {n * n}", x0 + 5 * s / 2, y0 + 5 * s + 80, 80, YEL if n == 5 else WHITE, outline=NAVY, ow=12)
    else:
        a = 1 - prog(t, 25.2, 26.2)
        key = "matti_nov_a00" if t < 23.6 else "matti_nov_a01"
        heads["matti"] = actor(ctx, t, key, W / 2, 1720, 440, a, "matti", True)
        for i in range(40):
            p = (t * 0.8 + i / 40) % 1
            if t < 23.6: break
            x = W / 2 + 230 * math.sin(i * 7.3) * (1 - p * 0.3)
            y = 1650 - p * 900
            ctx.rectangle(x, y, 18, 18); ctx.set_source_rgba(0.3, 0.95, 1, (1 - p) * prog(t, 23.6, 24.2)); ctx.fill()
        fl = 1 - abs(t - 26.9) / 0.6
        if fl > 0:
            ctx.rectangle(-20, -20, W + 40, H + 40); ctx.set_source_rgba(1, 1, 1, fl); ctx.fill()
    cast.bubbles(ctx, t, heads)

def scene_city(ctx, t):
    if not (CITY <= t < TOWER): return
    city(ctx, t, tower=ease_out(prog(t, 48.0, 49.0)))
    heads = {}
    hide = ease_in_out(prog(t, MEET - 0.4, MEET + 0.4)) * (1 - ease_in_out(prog(t, MISSION - 0.2, MISSION + 0.4)))
    # Matti
    if t < MEET:
        mk = "matti_emo00" if t < 32.0 else "matti_acc01"
    elif t < MISSION:
        mk = "matti_acc05"
    else:
        mk = "matti_emo04" if t >= 51.2 else "matti_emo01"
    mx = 300 - 140 * hide
    heads["matti"] = actor(ctx, t, mk, mx, FLOOR, 400 - 90 * hide, 1, "matti", True)
    # Equis
    if t >= 31.8:
        ex = W + 200 - (W + 200 - 640) * ease_out(prog(t, 31.8, 32.4))
        ex = ex - (640 - 380) * hide
        if t < MEET: ek = "equis03"
        elif t < 44.2: ek = "equis03"
        elif t < MISSION: ek = "equis01"
        else: ek = "equis05"
        heads["equis"] = actor(ctx, t, ek, ex, FLOOR + 20, 360 - 60 * hide, 1, "equis", ph=0.7)
    # el 7
    if MEET <= t < MISSION + 0.2:
        sx = W + 200 - (W + 200 - 640) * ease_out(prog(t, MEET, MEET + 1.0))
        frozen = prog(t, SPELL + 0.3, SPELL + 1.0)
        if t < 43.8:
            key = "siete00" if t < 38.4 else ("siete01" if t < SPELL + 0.2 else "siete03")
            shake = 6 * math.sin(t * 60) if SPELL <= t < SPELL + 0.6 else 0
            heads["siete"] = actor(ctx, t, key, sx + shake, FLOOR + 30, 380, 1, "siete", ph=2.1)
            if frozen > 0:
                put(ctx, "siete03@gray", sx, FLOOR + 30 - 4, 380, frozen)
        else:
            gray_zero(ctx, sx, FLOOR + 30, 330, pop(t, 43.8, 0.4) * (1 - prog(t, MISSION - 0.3, MISSION + 0.1)))
        puff(ctx, sx, FLOOR - 160, prog(t, 43.6, 44.4))
    # el Señor Cero
    if 38.2 <= t < MISSION:
        cx = W + 260 - (W + 260 - 920) * ease_out(prog(t, 38.2, 38.9)) + (W + 300 - 920) * ease_in_out(prog(t, 46.6, 47.4))
        if t < 38.8: ck = "carbon_cero_a00"
        elif t < SPELL: ck = "carbon_cero_a01"
        elif t < 43.6: ck = "carbon_cero_b00"
        else: ck = "carbon_cero_a01"
        heads["cero"] = actor(ctx, t, ck, cx, FLOOR + 20, 400, 1, "cero", ph=1.1, flip=True)
        # rayo del hechizo
        if SPELL <= t < SPELL + 0.9:
            p = ease_out(prog(t, SPELL, SPELL + 0.3)) * (1 - prog(t, SPELL + 0.7, SPELL + 0.9))
            x1, y1 = cx - 190, FLOOR - 330; x2, y2 = 680, FLOOR - 230
            for wdt, al in ((30, 0.25), (12, 0.9)):
                ctx.move_to(x1, y1)
                for i in range(1, 9):
                    f = i / 8
                    ctx.line_to(x1 + (x2 - x1) * f * p, y1 + (y2 - y1) * f * p + (18 * (-1) ** i if i < 8 else 0))
                ctx.set_line_width(wdt); ctx.set_source_rgba(1, 0.85, 0.3, al); ctx.stroke()
    cast.bubbles(ctx, t, heads)
    big_card(ctx, t, SPELL + 0.5, 44.2, [([("7", "#F0645A"), (" × ", NAVY), ("0", GREY), (" = ", NAVY), ("0", PINK)], 120)], y=640, w=640)
    big_card(ctx, t, 44.4, MISSION, [([("n", BLUE), (" × ", NAVY), ("0", GREY), (" = ", NAVY), ("0", PINK)], 120),
                                     ([("¡Siempre da cero!", GREY)], 44)], y=640, w=640)

def scene_tower(ctx, t):
    if t < TOWER: return
    tower_room(ctx, t)
    sh = ease_out(prog(t, 59.0, 59.8))
    if sh > 0:
        put(ctx, "carbon_cero_a01@shadow", W / 2 + 40, 1300, 1150, 0.55 * sh, flip=True)
    cx, bottom = W / 2, 1640
    nk = "numi_c01" if 55.2 <= t < 57.2 else "numi_c00"
    heads = {"numi": actor(ctx, t, nk, cx, bottom, 400, 1, "numi", True, 1.3)}
    cage(ctx, cx, 1050, bottom, 520)
    padlock(ctx, cx + 200, 1560, 0.75 * pop(t, 57.4, 0.4))
    if t >= 57.6:
        pill(ctx, cx, 900, "Clave:  7 × 8 − 6 × 9 = ?", 54, YEL, NAVY, 1, pop(t, 57.8), padx=36, pady=20)
    heads["cero"] = (W / 2 + 120, 560)
    cast.bubbles(ctx, t, heads)

def scene_end(ctx, t):
    if t < END: return
    d = ease_in_out(prog(t, END, END + 0.8))
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.01, 0.02, 0.08, 0.8 * d); ctx.fill()
    ASK = 66.4
    if t < ASK + 0.3:
        a = 1 - prog(t, ASK - 0.2, ASK + 0.3)
        s = "Continuará…"; n = int((t - END - 0.6) * 10)
        text(ctx, s[:max(0, n)], W / 2, 860, 120, YEL, alpha=a, outline=NAVY, ow=14)
        pill(ctx, W / 2, 1040, "Capítulo 3:  La torre del Señor Cero", 46, WHITE, NAVY, a, pop(t, END + 2.0), padx=34, pady=20)
    if t >= ASK:
        def eq(c, x, y, a):
            w1 = text_w(c, "7 × 8 − 6 × 9 = ", 84)
            segs(c, [("7 × 8 − 6 × 9 = ", NAVY)], x - 50, y, 84, alpha=a)
            answer_box(c, x - 50 + w1 / 2 + 50, y, 92, t, a)
        mission(ctx, t, ASK, [[("Ingresa la clave para", WHITE)], [("rescatar a ", WHITE), ("Numi", ORANGE), (":", WHITE)]],
                eq, hint="primero multiplica")
        pill(ctx, W / 2, 1600, "Síguenos para ver el capítulo 3", 48, YEL, NAVY, 1, pop(t, ASK + 2.6) * (1 + 0.03 * math.sin(t * 6)), padx=40, pady=22)
        put(ctx, "numi_c00", W / 2 + 330, 1900, 260, ease_out(prog(t, ASK + 0.5, ASK + 1.0)))

def draw(ctx, t):
    scene_recap(ctx, t)
    scene_lab(ctx, t)
    scene_city(ctx, t)
    scene_tower(ctx, t)
    scene_end(ctx, t)
    logo(ctx, t, 0.9)
    fade_black(ctx, t, TOWER)

def events():
    ev = [(0.2, "glitch", 0), (2.2, "flash", 0), (4.4, "flash", 0), (6.0, "rise", 0), (6.1, "glitch", 0)]
    ev += [(LAB, "whoosh", 0), (10.4, "success", 0), (10.5, "fanfare", 0)]
    ev += [(SQ, "whoosh", 0)] + [(SQ + 1.0 + k * 1.1, "note", k) for k in range(5)] + [(SQ + 5.6, "success", 1)]
    ev += [(TP + 0.2, "beep", 0), (23.6, "rise", 0), (26.4, "flash", 0)]
    ev += [(CITY + 0.4, "whoosh", 0), (31.8, "whoosh", 0), (MEET, "whoosh", 0), (38.2, "boom", 0)]
    ev += [(SPELL, "glitch", 0), (SPELL, "rise", 0), (SPELL + 0.5, "wrong", 0), (43.6, "pop", 2), (44.4, "pop", 3)]
    ev += [(46.6, "whoosh", 0), (48.0, "boom", 1), (51.4, "success", 0)]
    ev += [(TOWER, "whoosh", 0), (57.4, "pop", 0), (57.8, "beep", 0), (59.0, "boom", 0)]
    ev += [(END, "boom", 0), (END + 2.0, "pop", 1), (66.4, "whoosh", 0), (67.0, "question", 0), (68.4, "pop", 3)]
    return ev

if __name__ == "__main__":
    render("robots_novela_cap2", DUR, draw, events(), DIALOG, music="mystery",
           tension=[(38.2, 47.0), (TOWER, END)], mgain=0.6)
