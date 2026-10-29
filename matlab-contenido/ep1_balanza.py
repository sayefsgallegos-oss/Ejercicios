"""'Equis busca su valor' — Episodio 1: La balanza  (x + 3 = 11  ->  x = 8)."""
import random
from kit import *
from audio import SR, midi, env, tone, lowpass, noise, add, sfx

DUR = 51.2
EQ_C, TRES_C, ONCE_C, OCHO_C = PURPLE, ORANGE, BLUE, GREEN
PIV = (W / 2, 1200); L = 350; HANG = 170

# ---------- guion ----------
JUMP3, SPLIT, LESSON, TEASER = 17.2, 28.6, 40.6, 45.8
J2 = SPLIT + 1.8      # el 3 se baja del lado derecho
X8 = 32.0             # aparece x = 8
DIALOG = [  # (inicio, fin, quién, líneas)
    (6.2, 10.0, "x", ["Todos saben cuánto valen…", "¿y yo?"]),
    (13.6, 17.0, "3", ["¡Yo te ayudo!", "Me bajo y listo."]),
    (17.9, 20.6, "x", ["¡Aaah! ¡Nos caemos!"]),
    (21.0, 24.6, "11", ["¡Tranquilos! Si el 3", "se va de un lado…"]),
    (24.8, 28.4, "11", ["…también me quitan", "3 a mí."]),
    (31.4, 34.4, "x", ["Entonces…", "¿yo valgo 8?"]),
    (34.6, 36.8, "8", ["¡Igualito a mí!"]),
]
VOICE = {"x": 64, "3": 74, "11": 50, "8": 57}
CPS = 24  # letras por segundo al escribir

def spring(t, t0, frm, to, k=5.0, w=9.0):
    if t < t0: return frm
    d = t - t0
    return to + (frm - to) * math.exp(-k * d) * math.cos(w * d)

def theta(t):
    """Ángulo de la viga: se inclina cuando el 3 se baja y vuelve al equilibrio tras quitar 3 al 11."""
    if t < J2 + 0.3: return spring(t, JUMP3 + 0.2, 0.0, 0.24)
    return spring(t, J2 + 0.3, spring(J2 + 0.3, JUMP3 + 0.2, 0.0, 0.24), 0.0)

def ends(t):
    th = theta(t)
    return ((PIV[0] - L * math.cos(th), PIV[1] - L * math.sin(th)), (PIV[0] + L * math.cos(th), PIV[1] + L * math.sin(th)))


# ---------- personajes ----------
def talking(who, t):
    for st, en, w, lines in DIALOG:
        n = sum(len(l) for l in lines)
        if w == who and st <= t < st + n / CPS: return True
    return False

def mood(who, t):
    if who == "x":
        if 6.2 <= t < 10.0: return "sad"
        if JUMP3 + 0.3 <= t < 21.0: return "scared"
        if t >= 33.2: return "happy"
    if who == "3" and t >= JUMP3 - 0.3: return "happy"
    return "ok"

def character(ctx, glyph, x, feet, size, color, t, who=None, alpha=1.0, scale=1.0, look=0.0):
    if alpha <= 0 or scale <= 0.001: return
    m = mood(who, t) if who else "ok"
    tk = talking(who, t) if who else False
    bob = math.sin(t * 4 + x * 0.01)
    sq = 1 + 0.03 * bob + (0.05 * math.sin(t * 22) if tk else 0)
    if m == "scared": x += 4 * math.sin(t * 60)
    u = size / 260; size = 260
    ctx.save(); ctx.translate(x, feet); ctx.scale(u * scale / sq ** 0.5, u * scale * sq)
    # piernas
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_width(12); ctx.set_source_rgba(*hexc(NAVY, alpha))
    for dx in (-26, 26):
        ctx.move_to(dx, -48); ctx.line_to(dx, -8); ctx.stroke()
        ctx.save(); ctx.translate(dx + (8 if dx > 0 else -8), -6); ctx.scale(1.6, 1); ctx.arc(0, 0, 11, 0, 2 * math.pi); ctx.restore(); ctx.fill()
    # cuerpo = el propio símbolo
    font(ctx, size, "Fredoka")
    ext = ctx.text_extents(glyph)
    gx, gy = -ext.x_advance / 2, -40
    ctx.move_to(gx, gy); ctx.text_path(glyph)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_line_width(14)
    ctx.set_source_rgba(*hexc(NAVY, alpha)); ctx.stroke_preserve()
    ctx.set_source_rgba(*hexc(color, alpha)); ctx.fill()
    fx, fy, fw = face_anchor(glyph)
    fx += gx; fy += gy
    r = clamp(fw * 0.13, 8, 14); sp = clamp(fw * 0.24, 13, 25)
    # ojos (pequeños y dentro del número)
    blink = (t * 1.0 + len(glyph) * 0.9 + ord(glyph[0]) % 7 * 0.37) % 3.3 < 0.13
    for dx in (-sp, sp):
        ctx.save(); ctx.translate(fx + dx, fy)
        if blink:
            ctx.move_to(-r, 0); ctx.line_to(r, 0); ctx.set_line_width(5); ctx.set_source_rgba(*hexc(NAVY, alpha)); ctx.stroke()
        else:
            rr = r * (1.2 if m == "scared" else 1)
            ctx.save(); ctx.scale(1, 1.15); ctx.arc(0, 0, rr, 0, 2 * math.pi); ctx.restore()
            ctx.set_source_rgba(1, 1, 1, alpha); ctx.fill_preserve()
            ctx.set_line_width(3.5); ctx.set_source_rgba(*hexc(NAVY, alpha)); ctx.stroke()
            ctx.arc(r * 0.3 * look, r * 0.15, r * (0.5 if m != "scared" else 0.32), 0, 2 * math.pi)
            ctx.set_source_rgba(*hexc(NAVY, alpha)); ctx.fill()
        ctx.restore()
        if m == "sad":
            tilt = 5 if dx < 0 else -5
            ctx.move_to(fx + dx - r, fy - r * 1.9 - tilt); ctx.line_to(fx + dx + r, fy - r * 1.9 + tilt)
            ctx.set_line_width(5); ctx.set_source_rgba(*hexc(NAVY, alpha)); ctx.stroke()
    # boca (pequeña, dentro del número)
    my = fy + r * 2.3
    mw = sp * 0.75
    ctx.set_source_rgba(*hexc(NAVY, alpha)); ctx.set_line_width(5); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    if tk:
        o = 0.35 + 0.65 * abs(math.sin(t * 18))
        ctx.save(); ctx.translate(fx, my); ctx.scale(1, o * 0.8); ctx.arc(0, 0, mw * 0.7, 0, 2 * math.pi); ctx.restore(); ctx.fill()
    elif m == "scared":
        ctx.arc(fx, my, mw * 0.5, 0, 2 * math.pi); ctx.fill()
    elif m == "sad":
        ctx.arc(fx, my + mw * 0.8, mw, math.pi * 1.25, math.pi * 1.75); ctx.stroke()
    else:
        ctx.arc(fx, my - mw * 0.5, mw * (1.1 if m == "happy" else 0.9), math.pi * 0.2, math.pi * 0.8); ctx.stroke()
    ctx.restore()

_FACE = {}
def face_anchor(glyph):
    """Busca dentro del número la franja con más 'tinta' para poner la cara sin tapar la forma del dígito."""
    if glyph in _FACE: return _FACE[glyph]
    surf = cairo.ImageSurface(cairo.FORMAT_A8, 600, 400)
    c = cairo.Context(surf); font(c, 260, "Fredoka")
    ext = c.text_extents(glyph)
    ox, oy = 300 - ext.x_advance / 2, 330
    c.move_to(ox, oy); c.text_path(glyph); c.fill(); surf.flush()
    m = np.ndarray((400, surf.get_stride()), np.uint8, surf.get_data())[:, :600] > 128
    top, h = oy + ext.y_bearing, ext.height
    best = None
    for y in range(int(top + 0.30 * h), int(top + 0.58 * h)):
        row = m[y]; x = 0
        while x < 600:
            if row[x]:
                x0 = x
                while x < 600 and row[x]: x += 1
                w = x - x0
                score = w - abs((x0 + x) / 2 - 300) * 0.05
                if best is None or score > best[0]: best = (score, (x0 + x) / 2, y, w)
            x += 1
    _, cx, cy, w = best
    _FACE[glyph] = (cx - ox, cy - oy - 0.1 * w, w)
    return _FACE[glyph]

def bubble(ctx, t, st, en, lines, ax, ay):
    if not (st <= t < en): return
    k = pop(t, st, 0.3) * (1 - prog(t, en - 0.15, en))
    n = int((t - st) * CPS)
    size = 48
    wmax = max(text_w(ctx, l, size) for l in lines) + 70
    h = len(lines) * 62 + 44
    bx = clamp(ax - wmax / 2, 50, W - 50 - wmax)
    by = ay - h - 50
    ctx.save(); ctx.translate(ax, ay); sc(ctx, k); ctx.translate(-ax, -ay)
    rrect(ctx, bx, by + 8, wmax, h, 34); ctx.set_source_rgba(0.03, 0.15, 0.4, 0.2); ctx.fill()
    rrect(ctx, bx, by, wmax, h, 34); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    ctx.move_to(ax - 22, by + h - 2); ctx.line_to(ax, ay - 12); ctx.line_to(ax + 24, by + h - 2); ctx.fill()
    shown = n
    for i, l in enumerate(lines):
        part = l[:max(0, shown)]; shown -= len(l)
        text(ctx, part, bx + 35, by + 52 + i * 62, size, NAVY, align="l")
    ctx.restore()


# ---------- escenas ----------
def scene_title(ctx, t):
    if t > 4.2: return
    out = 1 - ease_in_out(prog(t, 3.5, 4.1))
    k = pop(t, 0.2, 0.55)
    text(ctx, "EQUIS", W / 2, 560, 200, EQ_C, scale=k, alpha=out, outline=WHITE, ow=26, rot=-0.04)
    text(ctx, "busca su valor", W / 2, 740, 84, WHITE, alpha=out * ease_out(prog(t, 0.6, 1.0)), outline=NAVY, ow=12)
    pill(ctx, W / 2, 880, "Episodio 1:  La balanza", 50, YEL, NAVY, out, pop(t, 1.0))
    character(ctx, "x", W / 2, 1500 + 300 * (1 - ease_out(prog(t, 1.4, 2.0))), 520, EQ_C, t, "x", out)

def scene_story(ctx, t):
    if not (3.8 <= t < LESSON + 0.3): return
    al = fade(t, 3.8, LESSON + 0.2)
    th = theta(t)
    (lx, ly), (rx, ry) = ends(t)
    k0 = pop(t, 4.0, 0.5)
    # piso y soporte
    ctx.save(); ctx.translate(PIV[0], 1560); sc(ctx, k0); ctx.translate(-PIV[0], -1560)
    rrect(ctx, 80, 1560, W - 160, 22, 11); ctx.set_source_rgba(1, 1, 1, 0.7 * al); ctx.fill()
    ctx.move_to(PIV[0] - 120, 1562); ctx.line_to(PIV[0] - 26, PIV[1]); ctx.line_to(PIV[0] + 26, PIV[1]); ctx.line_to(PIV[0] + 120, 1562); ctx.close_path()
    ctx.set_source_rgba(*hexc(NAVY, al)); ctx.fill()
    # viga
    ctx.save(); ctx.translate(*PIV); ctx.rotate(th)
    rrect(ctx, -L - 20, -16, 2 * L + 40, 32, 16); ctx.set_source_rgba(*hexc(YEL, al)); ctx.fill_preserve()
    ctx.set_line_width(6); ctx.set_source_rgba(*hexc(NAVY, al)); ctx.stroke(); ctx.restore()
    ctx.arc(*PIV, 26, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(NAVY, al)); ctx.fill()
    ctx.arc(*PIV, 11, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(YEL, al)); ctx.fill()
    # platillos
    for ex, ey in ((lx, ly), (rx, ry)):
        py = ey + HANG
        ctx.set_line_width(5); ctx.set_source_rgba(*hexc(NAVY, al))
        ctx.move_to(ex, ey); ctx.line_to(ex - 140, py); ctx.move_to(ex, ey); ctx.line_to(ex + 140, py); ctx.stroke()
        ctx.move_to(ex - 160, py); ctx.curve_to(ex - 120, py + 46, ex + 120, py + 46, ex + 160, py); ctx.close_path()
        ctx.set_source_rgba(*hexc(WHITE, al)); ctx.fill_preserve(); ctx.set_line_width(6); ctx.set_source_rgba(*hexc(NAVY, al)); ctx.stroke()
        ctx.arc(ex, ey, 12, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(NAVY, al)); ctx.fill()
    ctx.restore()
    lp, rp = ly + HANG, ry + HANG
    # Equis
    character(ctx, "x", lx - 75, lp, 360, EQ_C, t, "x", al, pop(t, 4.5, 0.5), look=1 if t < 21 else 0)
    # 3 (salta fuera por la izquierda)
    j = prog(t, JUMP3, JUMP3 + 0.9)
    x3 = lx + 135 + (-260 - lx - 135) * j
    y3 = lp + (1700 - lp) * j - 420 * math.sin(math.pi * j)
    if j < 1: character(ctx, "3", x3, y3, 290, TRES_C, t, "3", al, pop(t, 4.9, 0.5), look=-1)
    # 11 -> 8 y 3
    if t < SPLIT + 0.3:
        shake = 6 * math.sin(t * 50) * prog(t, SPLIT - 0.5, SPLIT)
        character(ctx, "11", rx + shake, rp, 290, ONCE_C, t, "11", al, pop(t, 5.3, 0.5), look=-1)
    if t >= SPLIT + 0.3:
        character(ctx, "8", rx - 55, rp, 300, OCHO_C, t, "8", al, pop(t, SPLIT + 0.3, 0.5), look=-1)
        j2 = prog(t, J2, J2 + 0.9)
        x3b = rx + 115 + (W + 260 - rx - 115) * j2
        y3b = rp + (1700 - rp) * j2 - 380 * math.sin(math.pi * j2)
        if j2 < 1: character(ctx, "3", x3b, y3b, 240, TRES_C, t, None, al, pop(t, SPLIT + 0.4, 0.5), look=1)
    # nube "¡puf!"
    pf = prog(t, SPLIT, SPLIT + 0.7)
    if 0 < pf < 1:
        for i in range(9):
            a = i * 2 * math.pi / 9
            rr = 60 + 140 * ease_out(pf)
            ctx.arc(rx + math.cos(a) * rr * 0.8, rp - 130 + math.sin(a) * rr * 0.6, 70 * (1 - pf * 0.6), 0, 2 * math.pi)
            ctx.set_source_rgba(1, 1, 1, 0.9 * (1 - pf) * al); ctx.fill()
    # rótulo 11 = 8 + 3
    lb = min(pop(t, SPLIT + 0.5, 0.45), 1 - prog(t, J2 + 0.4, J2 + 0.8))
    if lb > 0:
        ctx.save(); ctx.translate(rx - 90, rp - 470); sc(ctx, lb)
        rrect(ctx, -170, -60, 340, 120, 40); ctx.set_source_rgba(1, 1, 1, al); ctx.fill()
        segs(ctx, [("11", ONCE_C), (" = ", NAVY), ("8", OCHO_C), (" + ", NAVY), ("3", TRES_C)], 0, 0, 70, alpha=al)
        ctx.restore()
    # globos
    heads = {"x": (lx - 75, lp - 400), "3": (lx + 135, lp - 330), "11": (rx, rp - 330), "8": (rx - 40, rp - 360)}
    for st, en, who, lines in DIALOG:
        bubble(ctx, t, st, en, lines, *heads[who])
    # recuadro de la ecuación (abajo)
    k = ease_out(prog(t, 10.4, 10.8))
    if k > 0:
        y = 1720
        card(ctx, 90, y - 80, 900, 160, 40, alpha=al * k)
        if t < JUMP3:
            segs(ctx, [("x", EQ_C), (" + ", NAVY), ("3", TRES_C), (" = ", NAVY), ("11", ONCE_C)], W / 2, y, 84, alpha=al * k)
            text(ctx, "¡Equilibrio!", W / 2, y - 120, 46, WHITE, alpha=al * k * (1 - prog(t, 13.4, 13.6)), outline=NAVY, ow=8)
        elif t < SPLIT + 0.4:
            segs(ctx, [("x", EQ_C), ("  ≠  ", NAVY, "DejaVu Sans"), ("11", ONCE_C)], W / 2, y, 84, alpha=al)
            text(ctx, "¡Desequilibrio!", W / 2, y - 120, 46, RED, alpha=al * ease_out(prog(t, JUMP3 + 0.4, JUMP3 + 0.7)), outline=WHITE, ow=10)
        elif t < X8:
            segs(ctx, [("x", EQ_C), (" + 3 − 3", "#9AA7B8"), (" = ", NAVY), ("11", ONCE_C), (" − 3", "#9AA7B8")], W / 2, y, 72, alpha=al)
        else:
            kk = pop(t, X8, 0.5)
            segs(ctx, [("x", EQ_C), (" = ", NAVY), ("8", OCHO_C)], W / 2, y, 96, alpha=al, scale=kk)
    # celebración
    if t >= 37.0:
        kk = pop(t, 37.0, 0.5)
        pill(ctx, W / 2, 470, "¡Equis vale 8!", 70, YEL, NAVY, al, kk, padx=50, pady=28)
        tc = t - 37.0
        if tc < 3.5:
            for c in CONF:
                tt = tc - c["d"]
                if tt <= 0: continue
                x = W / 2 + math.cos(c["a"]) * c["v"] * tt * 0.8
                y = 470 + math.sin(c["a"]) * c["v"] * tt * 0.8 + 900 * tt * tt
                ctx.save(); ctx.translate(x, y); ctx.rotate(c["rs"] * tt)
                ctx.rectangle(-c["w"] / 2, -c["w"] / 4, c["w"], c["w"] / 2)
                ctx.set_source_rgba(*hexc(c["c"], clamp(1.4 - tt / 3) * al)); ctx.fill(); ctx.restore()

def scene_lesson(ctx, t):
    a, b = LESSON, TEASER
    if not (a <= t < b + 0.3): return
    al = fade(t, a, b + 0.2)
    k0 = pop(t, a + 0.1)
    bulb(ctx, W / 2, 420, 90 * k0, al)
    text(ctx, "La regla de la balanza", W / 2, 560, 70, WHITE, alpha=al, scale=k0, outline=NAVY, ow=12)
    k1 = ease_out(prog(t, a + 0.3, a + 0.7))
    yb = 660 + 60 * (1 - k1)
    card(ctx, 90, yb, 900, 900, 56, alpha=al * k1)
    for st, parts, y, size in [(0.6, [("Lo que quitas de un lado,", NAVY)], 110, 52),
                               (1.1, [("lo quitas del ", NAVY), ("otro", PINK)], 180, 52),
                               (1.9, [("x", EQ_C), (" + 3 = ", NAVY), ("11", ONCE_C)], 360, 84),
                               (2.6, [("x", EQ_C), (" + 3 ", NAVY), ("− 3", RED), (" = ", NAVY), ("11 ", ONCE_C), ("− 3", RED)], 500, 76),
                               (3.4, [("x", EQ_C), (" = ", NAVY), ("8", OCHO_C)], 680, 120)]:
        k = pop(t, a + st, 0.4)
        segs(ctx, parts, W / 2, yb + y, size, alpha=al * clamp(k), scale=k)

def scene_teaser(ctx, t):
    a = TEASER
    if t < a: return
    al = fade(t, a, DUR + 1)
    text(ctx, "Próximo episodio", W / 2, 520, 64, YEL, alpha=al * ease_out(prog(t, a + 0.1, a + 0.5)), outline=NAVY, ow=10)
    k = pop(t, a + 0.4, 0.5)
    pill(ctx, W / 2, 640, "¿Y si Equis viene en pareja?", 54, WHITE, NAVY, al, k, padx=40, pady=24)
    character(ctx, "x", W / 2 - 150, 1300, 400, EQ_C, t, None, al, pop(t, a + 0.9, 0.5), look=1)
    character(ctx, "x", W / 2 + 150, 1300, 400, PINK, t, None, al, pop(t, a + 1.2, 0.5), look=-1)
    text(ctx, "2x", W / 2, 840, 120, YEL, alpha=al, scale=pop(t, a + 1.6, 0.5), outline=NAVY, ow=14)
    k3 = pop(t, a + 2.2)
    pill(ctx, W / 2, 1520, "Síguenos para no perdértelo", 50, YEL, NAVY, al, k3 * (1 + 0.03 * math.sin(t * 6)), padx=44, pady=24)

def draw(ctx, t):
    scene_title(ctx, t)
    scene_story(ctx, t)
    scene_lesson(ctx, t)
    scene_teaser(ctx, t)


# ---------- sonido ----------
def blip(f, rng):
    n = int(0.055 * SR); tt = np.arange(n) / SR
    f = f * (1 + rng.uniform(-0.06, 0.06))
    s = np.sign(np.sin(2 * np.pi * f * tt)) * 0.35 + np.sin(2 * np.pi * f * 2 * tt) * 0.4
    return lowpass(s, 2600) * env(n, 0.004, 0.055, 3) * 0.22

def boing(up=True):
    n = int(0.45 * SR); tt = np.arange(n) / SR
    f = (220 + 500 * tt / 0.45) if up else (700 - 500 * tt / 0.45)
    f = f * (1 + 0.04 * np.sin(2 * np.pi * 18 * tt))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.005, 0.45, 2.5) * 0.3

def custom_track(dur):
    rng = np.random.default_rng(5)
    out = np.zeros(int(dur * SR) + 3 * SR)
    for st, en, who, lines in DIALOG:
        n = sum(len(l) for l in lines)
        base = midi(VOICE[who])
        for i in range(0, n, 2):
            add(out, blip(base * 2 ** (rng.choice([0, 2, 4, 7]) / 12), rng), st + i / CPS)
    add(out, boing(True), JUMP3); add(out, boing(False), JUMP3 + 0.45)
    add(out, boing(True), J2); add(out, boing(False), J2 + 0.45)
    return out[: int(dur * SR)]

def events():
    ev = [(0.2, "boom", 0), (1.0, "pop", 0), (1.4, "whoosh", 0), (4.0, "pop", 1), (4.5, "pop", 2), (4.9, "pop", 3), (5.3, "pop", 0)]
    ev += [(10.4, "pop", 1), (JUMP3 + 0.3, "wrong", 0), (SPLIT, "whoosh", 0), (SPLIT + 0.3, "pop", 2), (SPLIT + 0.5, "pop", 3)]
    ev += [(X8, "success", 0), (37.0, "fanfare", 0)]
    a = LESSON
    ev += [(a, "whoosh", 0)] + [(a + s, "pop", i) for i, s in enumerate([0.6, 1.9, 2.6])] + [(a + 3.4, "success", 1)]
    ev += [(TEASER, "whoosh", 0), (TEASER + 0.4, "pop", 0), (TEASER + 0.9, "blip", 2), (TEASER + 1.2, "blip", 5), (TEASER + 1.6, "boom", 1), (TEASER + 2.2, "pop", 3)]
    return ev

def build(path, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    mus = music_pop(dur, transpose=5, bpm=112, breaks=[(5.5, 39.5)])
    fade_ = np.clip(t / 0.6, 0, 1) * np.clip((dur - t) / 1.5, 0, 1)
    fx = np.zeros(n + 3 * SR)
    for tm, kind, p in events(): add(fx, sfx(kind, p), tm)
    mix = mus * fade_ * 0.38 + fx[:n] + custom_track(dur)
    mix = np.tanh(mix * 1.4) / np.tanh(1.4)
    mix *= 0.89 / np.abs(mix).max()
    pcm = (mix * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.stack([pcm, pcm], 1).tobytes())

if __name__ == "__main__":
    import kit
    kit.build_audio = lambda path, dur, ev, tr, br: build(path, dur)
    run("equis_ep1_balanza", DUR, draw, [], transpose=0)
