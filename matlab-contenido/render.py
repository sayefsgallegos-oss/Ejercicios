"""Reto matemático 'saludos' — video vertical 1080x1920 generado 100% en código.

Uso:  python3 render.py            -> video final (out/reto_saludos.mp4)
      python3 render.py --frame 22 -> PNG de prueba en el segundo 22
"""
import math, random, subprocess, sys, os
import cairo
import numpy as np
from audio import build_audio

W, H, FPS = 1080, 1920, 30
DUR = 46.0
OUT = os.path.join(os.path.dirname(__file__), "out")

# ---------- paleta ----------
def hexc(h, a=1.0):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (a,)

NAVY = "#0B2A5B"; BLUE = "#1673E6"; SKY = "#3FB4FF"; YEL = "#FFC93C"
PINK = "#FF4F81"; GREEN = "#22C17E"; PURPLE = "#7B5CFF"; ORANGE = "#FF8A3D"
RED = "#F0334B"; WHITE = "#FFFFFF"; TEAL = "#14B8C4"
PEOPLE = [PINK, ORANGE, YEL, GREEN, TEAL, SKY, BLUE, PURPLE, "#E25BD6", "#8BD346"]

# ---------- guion (tiempos en segundos) ----------
T_TITLE = (0.0, 3.2)
T_PROBLEM = (3.2, 10.4)
T_THINK = (10.4, 15.8)
T_TRAP = (15.8, 20.6)
T_SOLVE = (20.6, 34.4)
T_FORMULA = (34.4, 40.4)
T_ANSWER = (40.4, DUR)

STEP_DUR = [1.7, 1.5, 1.35, 1.2, 1.1, 1.0, 0.95, 0.9, 0.9]
SOLVE_START = T_SOLVE[0] + 0.9
STEP_START = [SOLVE_START + sum(STEP_DUR[:i]) for i in range(9)]
SUM_TIME = STEP_START[-1] + STEP_DUR[-1] + 0.3


# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def ease_out(x): return 1 - (1 - x) ** 3
def ease_in_out(x): return 3 * x * x - 2 * x * x * x
def ease_back(x, s=1.9):
    x -= 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2
def pop(t, start, d=0.45): return ease_back(prog(t, start, start + d))
def fade(t, a, b, d=0.35):
    """1 dentro de [a,b] con fundido de entrada/salida."""
    return min(prog(t, a, a + d), 1 - prog(t, b - d, b))


# ---------- dibujo ----------
def font(ctx, size, family="Fredoka", bold=True):
    ctx.select_font_face(family, cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

def text(ctx, s, x, y, size, color, family="Fredoka", scale=1.0, alpha=1.0,
         outline=None, ow=0, align="c", rot=0.0):
    if alpha <= 0.001 or scale <= 0.001: return 0
    ctx.save()
    font(ctx, size, family)
    ext = ctx.text_extents(s)
    fe = ctx.font_extents()
    w = ext.x_advance
    ox = {"c": -w / 2, "l": 0, "r": -w}[align]
    ctx.translate(x, y); ctx.rotate(rot); ctx.scale(scale, scale)
    ctx.move_to(ox, (fe[0] - fe[1]) / 2)
    ctx.text_path(s)
    if outline:
        ctx.set_source_rgba(*hexc(outline, alpha)); ctx.set_line_width(ow)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    ctx.set_source_rgba(*hexc(color, alpha)); ctx.fill()
    ctx.restore()
    return w

def text_w(ctx, s, size, family="Fredoka"):
    font(ctx, size, family); return ctx.text_extents(s).x_advance

def segments(ctx, segs, x, y, size, alpha=1.0, scale=1.0, family="Fredoka"):
    """Línea centrada con tramos de distinto color: [(texto, color), ...]."""
    if alpha <= 0.001 or scale <= 0.001: return
    total = sum(text_w(ctx, s, size, family) for s, _ in segs)
    ctx.save(); ctx.translate(x, y); ctx.scale(scale, scale)
    cx = -total / 2
    for s, c in segs:
        cx += text(ctx, s, cx, 0, size, c, family, alpha=alpha, align="l")
    ctx.restore()

def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()

def card(ctx, x, y, w, h, r=48, color=WHITE, alpha=1.0, shadow=True):
    if shadow:
        for i in range(8):
            rrect(ctx, x - i * 2, y + 14 - i * 2 + 10, w + i * 4, h + i * 4, r + i * 2)
            ctx.set_source_rgba(0.02, 0.1, 0.3, 0.035 * alpha); ctx.fill()
    rrect(ctx, x, y, w, h, r); ctx.set_source_rgba(*hexc(color, alpha)); ctx.fill()

def pill(ctx, cx, cy, label, size, bg, fg, alpha=1.0, scale=1.0, padx=34, pady=18):
    if scale <= 0.001: return
    w = text_w(ctx, label, size) + padx * 2; h = size + pady * 2
    ctx.save(); ctx.translate(cx, cy); ctx.scale(scale, scale)
    card(ctx, -w / 2, -h / 2, w, h, h / 2, bg, alpha, shadow=False)
    text(ctx, label, 0, 0, size, fg, alpha=alpha)
    ctx.restore()

def person(ctx, x, y, r, color, num, alpha=1.0, scale=1.0, glow=0.0):
    if scale <= 0.001: return
    ctx.save(); ctx.translate(x, y); ctx.scale(scale, scale)
    if glow > 0:
        for i in range(6, 0, -1):
            ctx.arc(0, 0, r * (1 + 0.12 * i * glow), 0, 2 * math.pi)
            ctx.set_source_rgba(*hexc(color, 0.07 * glow * alpha)); ctx.fill()
    ctx.arc(0, 0, r, 0, 2 * math.pi)
    ctx.set_source_rgba(*hexc(WHITE, alpha)); ctx.fill()
    ctx.arc(0, 0, r * 0.86, 0, 2 * math.pi)
    ctx.set_source_rgba(*hexc(color, alpha)); ctx.fill()
    # silueta: cabeza + hombros
    ctx.save(); ctx.arc(0, 0, r * 0.86, 0, 2 * math.pi); ctx.clip()
    ctx.arc(0, -r * 0.18, r * 0.30, 0, 2 * math.pi)
    ctx.set_source_rgba(1, 1, 1, 0.92 * alpha); ctx.fill()
    ctx.arc(0, r * 0.62, r * 0.52, math.pi, 2 * math.pi)
    ctx.fill()
    ctx.restore()
    if num is not None:
        bx, by = r * 0.68, -r * 0.68
        ctx.arc(bx, by, r * 0.36, 0, 2 * math.pi)
        ctx.set_source_rgba(*hexc(NAVY, alpha)); ctx.fill()
        text(ctx, str(num), bx, by, r * 0.42, WHITE, alpha=alpha)
    ctx.restore()

def check(ctx, x, y, s, color, p):
    if p <= 0: return
    ctx.save(); ctx.set_line_width(s * 0.22); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    pts = [(x - s * 0.5, y), (x - s * 0.12, y + s * 0.38), (x + s * 0.55, y - s * 0.4)]
    ctx.move_to(*pts[0])
    if p < 0.4:
        q = p / 0.4; ctx.line_to(pts[0][0] + (pts[1][0] - pts[0][0]) * q, pts[0][1] + (pts[1][1] - pts[0][1]) * q)
    else:
        q = (p - 0.4) / 0.6; ctx.line_to(*pts[1])
        ctx.line_to(pts[1][0] + (pts[2][0] - pts[1][0]) * q, pts[1][1] + (pts[2][1] - pts[1][1]) * q)
    ctx.set_source_rgba(*hexc(color)); ctx.stroke(); ctx.restore()

def bulb(ctx, x, y, s, alpha=1.0):
    ctx.save(); ctx.translate(x, y)
    for i in range(8):
        a = i * math.pi / 4 - math.pi / 2
        ctx.move_to(math.cos(a) * s * 0.75, math.sin(a) * s * 0.75 - s * 0.1)
        ctx.line_to(math.cos(a) * s * 0.95, math.sin(a) * s * 0.95 - s * 0.1)
    ctx.set_line_width(s * 0.08); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgba(*hexc(YEL, alpha)); ctx.stroke()
    ctx.arc(0, -s * 0.1, s * 0.48, 0, 2 * math.pi); ctx.fill()
    rrect(ctx, -s * 0.22, s * 0.3, s * 0.44, s * 0.3, s * 0.08)
    ctx.set_source_rgba(*hexc(NAVY, alpha)); ctx.fill()
    ctx.restore()


# ---------- fondo ----------
def make_background():
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(surf)
    g = cairo.LinearGradient(0, 0, W * 0.4, H)
    g.add_color_stop_rgb(0, *hexc("#0F63D6")[:3]); g.add_color_stop_rgb(1, *hexc("#29A8F5")[:3])
    c.set_source(g); c.paint()
    c.set_line_width(2); c.set_source_rgba(1, 1, 1, 0.06)
    for x in range(0, W + 1, 60): c.move_to(x, 0); c.line_to(x, H)
    for y in range(0, H + 1, 60): c.move_to(0, y); c.line_to(W, y)
    c.stroke()
    rg = cairo.RadialGradient(W / 2, H * 0.45, 100, W / 2, H * 0.45, H * 0.75)
    rg.add_color_stop_rgba(0, 1, 1, 1, 0.10); rg.add_color_stop_rgba(1, 0, 0.05, 0.25, 0.25)
    c.set_source(rg); c.paint()
    return surf

rng = random.Random(7)
SYMBOLS = [dict(s=rng.choice(["+", "×", "÷", "=", "π", "%", "√", "∑"]), x=rng.uniform(0, W), y=rng.uniform(0, H),
                size=rng.uniform(50, 120), sp=rng.uniform(12, 30), rot=rng.uniform(-0.5, 0.5),
                ph=rng.uniform(0, 6.28)) for _ in range(18)]

def draw_symbols(ctx, t):
    for s in SYMBOLS:
        y = (s["y"] - s["sp"] * t) % (H + 200) - 100
        x = s["x"] + math.sin(t * 0.6 + s["ph"]) * 20
        text(ctx, s["s"], x, y, s["size"], WHITE, "DejaVu Sans", alpha=0.10, rot=s["rot"] + 0.1 * math.sin(t + s["ph"]))

def brand(ctx, t, alpha=1.0):
    """Marca superior (reemplazable por el logo real del laboratorio)."""
    cx, cy = W / 2, 150
    for i, col in enumerate([PINK, YEL, GREEN, PURPLE]):
        a = i * math.pi / 4 + 0.785 + 0.05 * math.sin(t * 2 + i)
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(a)
        rrect(ctx, -70, -16, 140, 32, 16); ctx.set_source_rgba(*hexc(col, alpha * 0.95)); ctx.fill()
        ctx.restore()
    pill(ctx, cx, cy, "matLab", 34, RED, WHITE, alpha, padx=28, pady=10)


# ---------- escenas ----------
def scene_title(ctx, t):
    a, b = T_TITLE
    if not (a <= t < b + 0.4): return
    out = 1 - ease_in_out(prog(t, b - 0.35, b + 0.2))
    y0 = 940 - 200 * (1 - out)
    pill(ctx, W / 2, y0 - 330, "RETO DEL DÍA", 44, YEL, NAVY, out, pop(t, 0.15), padx=40)
    sc = pop(t, 0.45, 0.55)
    wob = 1 + 0.025 * math.sin(t * 6)
    text(ctx, "MATH", W / 2, y0 - 110, 230, YEL, scale=sc * wob, alpha=out, outline=NAVY, ow=34, rot=-0.06)
    sc2 = pop(t, 0.7, 0.55)
    text(ctx, "QUIZ", W / 2, y0 + 110, 230, YEL, scale=sc2 * wob, alpha=out, outline=NAVY, ow=34, rot=-0.06)
    p = prog(t, 1.3, 1.8)
    text(ctx, "¿Podrás resolverlo?", W / 2, y0 + 340 + 30 * (1 - ease_out(p)), 72, WHITE, alpha=ease_out(p) * out)
    for i, (dx, dy, s) in enumerate([(-360, -250, 40), (370, -60, 30), (-330, 220, 26), (340, 260, 44)]):
        k = pop(t, 0.9 + i * 0.12) * out
        text(ctx, "✦", W / 2 + dx, y0 + dy, s * 2, WHITE, "DejaVu Sans", scale=k * (1 + 0.15 * math.sin(t * 5 + i)), alpha=out)

PROB_LINES = [  # (tiempo de aparición, tramos)
    (0.55, [("Hay ", NAVY), ("10 personas", BLUE)]),
    (0.95, [("en una sala.", NAVY)]),
    (2.2, [("Cada una saluda ", NAVY), ("UNA", PINK)]),
    (2.6, [("sola vez a todas", NAVY)]),
    (3.0, [("las demás.", NAVY)]),
]

def problem_card(ctx, t, rel, alpha, compact=0.0):
    """Tarjeta del enunciado; compact=1 la encoge arriba para dejar espacio."""
    cw, ch = 900, 1040 - 560 * compact
    cx, cy = (W - cw) / 2, 330 - 40 * compact
    card(ctx, cx, cy, cw, ch, 56, alpha=alpha)
    rrect(ctx, cx, cy, cw, 16, 8); ctx.set_source_rgba(*hexc(YEL, alpha)); ctx.fill()
    if compact < 0.5:
        a2 = alpha * (1 - compact * 2)
        y = cy + 120
        for i, (st, segs) in enumerate(PROB_LINES):
            k = pop(t, T_PROBLEM[0] + st, 0.4) if rel else 1
            segments(ctx, segs, W / 2, y + i * 84 + (i >= 2) * 230, 64, alpha=a2 * clamp(k), scale=k)
        # fila de 10 personas
        for i in range(10):
            k = pop(t, T_PROBLEM[0] + 1.2 + i * 0.07, 0.4) if rel else 1
            person(ctx, cx + 92 + i * 79.5, cy + 360, 34, PEOPLE[i], None, a2, k)
        k = pop(t, T_PROBLEM[0] + 3.7, 0.5) if rel else 1
        wig = 0.04 * math.sin(t * 7) * prog(t, T_PROBLEM[0] + 4.2, T_PROBLEM[0] + 4.4)
        ctx.save(); ctx.translate(W / 2, cy + ch - 120); ctx.rotate(wig)
        pill(ctx, 0, 0, "¿Cuántos saludos hay?", 66, PINK, WHITE, a2, k, padx=44, pady=26)
        ctx.restore()
    else:
        a2 = alpha * (compact - 0.5) * 2
        segments(ctx, [("10 personas", BLUE), (" · todos se saludan", NAVY)], W / 2, cy + 110, 54, alpha=a2)
        segments(ctx, [("1 vez", PINK), (" · ¿cuántos saludos?", NAVY)], W / 2, cy + 190, 54, alpha=a2)
        for i in range(10):
            person(ctx, cx + 92 + i * 79.5, cy + 320, 30, PEOPLE[i], None, a2)

def scene_problem(ctx, t):
    a = T_PROBLEM[0]
    if not (a <= t < T_TRAP[1] + 0.3): return
    enter = ease_out(prog(t, a, a + 0.55))
    leave = 1 - ease_in_out(prog(t, T_TRAP[1] - 0.3, T_TRAP[1] + 0.2))
    compact = ease_in_out(prog(t, T_THINK[0], T_THINK[0] + 0.6))
    ctx.save(); ctx.translate(0, 900 * (1 - enter) - 300 * (1 - leave))
    problem_card(ctx, t, True, leave, compact)
    ctx.restore()

def scene_think(ctx, t):
    a, b = T_THINK
    if not (a <= t < b + 0.3): return
    al = fade(t, a + 0.3, b + 0.2)
    cx, cy, r = W / 2, 1180, 230
    pill(ctx, W / 2, 870, "Piensa tu respuesta…", 56, NAVY, WHITE, al, pop(t, a + 0.35))
    ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.22 * al); ctx.fill()
    ctx.arc(cx, cy, r - 26, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(WHITE, al)); ctx.fill()
    t0 = a + 0.4
    left = clamp(1 - (t - t0) / 5.0)
    ctx.set_line_width(30); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    if left > 0:
        ctx.arc(cx, cy, r - 13, -math.pi / 2, -math.pi / 2 + 2 * math.pi * left)
        ctx.set_source_rgba(*hexc(YEL if left > 0.4 else ORANGE if left > 0.2 else RED, al)); ctx.stroke()
    n = max(1, math.ceil(5 - (t - t0) - 1e-6))
    beat = 1 - (t - t0) % 1
    text(ctx, str(n), cx, cy, 220, NAVY, alpha=al, scale=1 + 0.18 * ease_out(beat) ** 3)

def scene_trap(ctx, t):
    a, b = T_TRAP
    if not (a <= t < b + 0.3): return
    al = fade(t, a, b + 0.2)
    pill(ctx, W / 2, 860, "¡Cuidado con la trampa!", 58, YEL, NAVY, al, pop(t, a + 0.1))
    rows = [(a + 0.6, "10 × 10 = 100", "nadie se saluda a sí mismo"),
            (a + 2.0, "10 × 9 = 90", "¡cada saludo se cuenta 2 veces!")]
    for i, (st, eq, why) in enumerate(rows):
        y = 1080 + i * 290
        k = pop(t, st, 0.45)
        card(ctx, 110, y - 95, 860, 230, 40, alpha=al * clamp(k))
        text(ctx, eq, W / 2, y - 15, 92, NAVY, alpha=al * clamp(k), scale=k)
        sp = ease_out(prog(t, st + 0.55, st + 0.8))
        if sp > 0:
            wq = text_w(ctx, eq, 92) / 2 + 30
            ctx.move_to(W / 2 - wq, y - 10); ctx.line_to(W / 2 - wq + 2 * wq * sp, y - 25)
            ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgba(*hexc(RED, al)); ctx.stroke()
        text(ctx, why, W / 2, y + 75, 44, RED, alpha=al * ease_out(prog(t, st + 0.75, st + 1.05)))

CIRCLE_C, CIRCLE_R = (W / 2, 1000), 360
def ppos(i):
    a = -math.pi / 2 + i * 2 * math.pi / 10
    return CIRCLE_C[0] + CIRCLE_R * math.cos(a), CIRCLE_C[1] + CIRCLE_R * math.sin(a)

def count_at(t):
    """Saludos contados hasta el tiempo t (con animación de cada línea)."""
    total, lines = 0, []
    for k in range(9):
        st, d = STEP_START[k], STEP_DUR[k]
        n = 9 - k
        for j, other in enumerate(range(k + 1, 10)):
            ls = st + 0.25 + (d - 0.45) * j / n
            p = ease_out(prog(t, ls, ls + 0.22))
            if p > 0: lines.append((k, other, p, ls))
            if p >= 1: total += 1
    return total, lines

def scene_solve(ctx, t):
    a, b = T_SOLVE
    if not (a <= t < b + 0.3): return
    al = fade(t, a, b + 0.2)
    pill(ctx, W / 2, 330, "Vamos paso a paso", 54, NAVY, WHITE, al, pop(t, a + 0.1))
    total, lines = count_at(t)
    cur = max([k for k in range(9) if t >= STEP_START[k]], default=-1)
    if t >= SUM_TIME: cur = -1
    # líneas
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for k, o, p, ls in lines:
        (x1, y1), (x2, y2) = ppos(k), ppos(o)
        active = (k == cur)
        ctx.move_to(x1, y1); ctx.line_to(x1 + (x2 - x1) * p, y1 + (y2 - y1) * p)
        ctx.set_line_width(9 if active else 5)
        ctx.set_source_rgba(*hexc(PEOPLE[k], al * (1.0 if active else 0.55))); ctx.stroke()
    # personas
    for i in range(10):
        x, y = ppos(i)
        k = pop(t, a + 0.3 + i * 0.05, 0.45)
        g = 1.0 if i == cur else 0.0
        done = cur > i or (cur == -1 and t >= SUM_TIME)
        person(ctx, x, y, 62 if i == cur else 52, PEOPLE[i], i + 1, al * (0.6 if done and cur != -1 else 1), k, g)
    # contador central
    sc = 1 + 0.12 * max(0.0, 1 - min(abs(t - l[3] - 0.22) for l in lines) * 8) if lines else 1
    ctx.arc(*CIRCLE_C, 120, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(WHITE, al * 0.95)); ctx.fill()
    text(ctx, str(total), CIRCLE_C[0], CIRCLE_C[1] - 12, 120, NAVY, alpha=al, scale=sc)
    text(ctx, "saludos", CIRCLE_C[0], CIRCLE_C[1] + 62, 36, BLUE, alpha=al)
    # explicación del paso
    if 0 <= cur:
        n = 9 - cur
        st = STEP_START[cur]
        k = ease_out(prog(t, st, st + 0.25))
        if cur == 0:
            segs = [("La persona 1 saluda a ", WHITE), ("9", YEL)]
        elif cur == 1:
            segs = [("La 2 ya saludó a la 1: ", WHITE), ("8", YEL), (" nuevos", WHITE)]
        else:
            segs = [(f"La {cur + 1}: ", WHITE), (str(n), YEL), (" saludo" + ("s" if n > 1 else "") + " nuevo" + ("s" if n > 1 else ""), WHITE)]
        segments(ctx, segs, W / 2, 470 + 20 * (1 - k), 52, alpha=al * k)
    # suma acumulada
    terms = [str(9 - k) for k in range(9) if t >= STEP_START[k] + STEP_DUR[k] * 0.8]
    y = 1560
    card(ctx, 70, y - 90, 940, 180, 44, alpha=al * ease_out(prog(t, STEP_START[0], STEP_START[0] + 0.4)))
    if terms:
        segs = []
        for i, s in enumerate(terms):
            if i: segs.append((" + ", "#8AA0C0"))
            segs.append((s, PEOPLE[i]))
        if t >= SUM_TIME:
            segs.append((" = ", NAVY)); segs.append(("45", PINK))
        fs = 64 if t < SUM_TIME else 58
        segments(ctx, segs, W / 2, y, fs, alpha=al, scale=pop(t, SUM_TIME, 0.5) * 0.08 + 0.92 if t >= SUM_TIME else 1)

def scene_formula(ctx, t):
    a, b = T_FORMULA
    if not (a <= t < b + 0.3): return
    al = fade(t, a, b + 0.2)
    k0 = pop(t, a + 0.1)
    bulb(ctx, W / 2, 400, 90 * k0, al)
    text(ctx, "El atajo", W / 2, 540, 84, WHITE, alpha=al, scale=k0, outline=NAVY, ow=14)
    k1 = ease_out(prog(t, a + 0.4, a + 0.8))
    card(ctx, 90, 660 + 60 * (1 - k1), 900, 860, 56, alpha=al * k1)
    yb = 660 + 60 * (1 - k1)
    rows = [
        (a + 0.8, [("Cada persona saluda a ", NAVY), ("n − 1", BLUE)], 50),
        (a + 1.6, [("pero cada saludo ", NAVY), ("une a 2", PINK)], 50),
        (a + 2.0, [("así que dividimos entre 2", NAVY)], 50),
    ]
    for i, (st, segs, fs) in enumerate(rows):
        k = pop(t, st, 0.4)
        segments(ctx, segs, W / 2, yb + 110 + i * 78, fs, alpha=al * clamp(k), scale=k)
    k = pop(t, a + 2.6, 0.5)
    ctx.save(); ctx.translate(W / 2, yb + 450); ctx.scale(max(k, 1e-3), max(k, 1e-3))
    rrect(ctx, -380, -90, 760, 180, 40); ctx.set_source_rgba(*hexc("#EAF4FF", al)); ctx.fill()
    segments(ctx, [("n × (n − 1)", NAVY)], 0, -30, 72, alpha=al)
    ctx.move_to(-200, 18); ctx.line_to(200, 18); ctx.set_line_width(7)
    ctx.set_source_rgba(*hexc(NAVY, al)); ctx.stroke()
    text(ctx, "2", 0, 60, 60, NAVY, alpha=al)
    ctx.restore()
    k = pop(t, a + 3.6, 0.5)
    segments(ctx, [("10 × 9 ÷ 2 = ", NAVY), ("45", PINK)], W / 2, yb + 700, 84, alpha=al * clamp(k), scale=k)

CONF = [dict(a=rng.uniform(0, 2 * math.pi), v=rng.uniform(700, 1500), c=rng.choice(PEOPLE),
             w=rng.uniform(14, 26), rs=rng.uniform(-8, 8), d=rng.uniform(0, 0.15)) for _ in range(140)]

def scene_answer(ctx, t):
    a, b = T_ANSWER
    if t < a: return
    al = fade(t, a, b + 1)
    k = pop(t, a + 0.15, 0.6)
    ctx.save(); ctx.translate(W / 2, 760); ctx.scale(max(k, 1e-3), max(k, 1e-3))
    for i in range(10, 0, -1):
        ctx.arc(0, 0, 250 + i * 9, 0, 2 * math.pi); ctx.set_source_rgba(1, 0.95, 0.6, 0.03 * al); ctx.fill()
    ctx.arc(0, 0, 250, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(WHITE, al)); ctx.fill()
    text(ctx, "45", 0, -20, 250, PINK, alpha=al, scale=1 + 0.03 * math.sin(t * 5))
    text(ctx, "saludos", 0, 120, 60, NAVY, alpha=al)
    ctx.restore()
    pk = pop(t, a + 0.5)
    ctx.save(); ctx.translate(W / 2 + 200, 560); ctx.scale(max(pk, 1e-3), max(pk, 1e-3))
    ctx.arc(0, 0, 70, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(GREEN, al)); ctx.fill()
    ctx.restore()
    check(ctx, W / 2 + 200, 560, 70 * pk, WHITE, prog(t, a + 0.6, a + 0.95))
    # confeti
    tc = t - a - 0.15
    if 0 < tc < 4:
        for c in CONF:
            tt = tc - c["d"]
            if tt <= 0: continue
            x = W / 2 + math.cos(c["a"]) * c["v"] * tt * 0.9
            y = 760 + math.sin(c["a"]) * c["v"] * tt * 0.9 + 900 * tt * tt
            ctx.save(); ctx.translate(x, y); ctx.rotate(c["rs"] * tt)
            ctx.rectangle(-c["w"] / 2, -c["w"] / 4, c["w"], c["w"] / 2)
            ctx.set_source_rgba(*hexc(c["c"], clamp(1.4 - tt / 3))); ctx.fill(); ctx.restore()
    # cierre
    k2 = ease_out(prog(t, a + 1.6, a + 2.1))
    card(ctx, 90, 1180 + 80 * (1 - k2), 900, 330, 50, alpha=k2)
    yb = 1180 + 80 * (1 - k2)
    text(ctx, "Próximo reto:", W / 2, yb + 90, 50, BLUE, alpha=k2)
    segments(ctx, [("¿Y con ", NAVY), ("20", PINK), (" personas?", NAVY)], W / 2, yb + 180, 72, alpha=k2)
    text(ctx, "Déjalo en los comentarios", W / 2, yb + 262, 40, "#5A6E8C", "Nunito ExtraBold", alpha=k2)
    k3 = pop(t, a + 2.6)
    pill(ctx, W / 2, 1640, "Síguenos para más retos", 50, YEL, NAVY, 1, k3 * (1 + 0.03 * math.sin(t * 6)), padx=44, pady=24)


def render_frame(ctx, bg, t):
    ctx.set_source_surface(bg); ctx.paint()
    draw_symbols(ctx, t)
    brand(ctx, t, 1 - fade(t, -1, T_TITLE[1]) if t < T_TITLE[1] + 0.5 else 1)
    for sc in (scene_title, scene_problem, scene_think, scene_trap, scene_solve, scene_formula, scene_answer):
        sc(ctx, t)
    # fundido final
    if t > DUR - 0.5:
        ctx.set_source_rgba(0, 0, 0, prog(t, DUR - 0.5, DUR)); ctx.paint()


def main():
    os.makedirs(OUT, exist_ok=True)
    bg = make_background()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    if "--frame" in sys.argv:
        for s in sys.argv[sys.argv.index("--frame") + 1:]:
            render_frame(ctx, bg, float(s)); surf.write_to_png(f"{OUT}/frame_{s}.png")
        return
    events = sfx_events()
    wav = f"{OUT}/audio.wav"
    build_audio(wav, DUR, events)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", f"{OUT}/reto_saludos.mp4"]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        render_frame(ctx, bg, i / FPS)
        surf.flush(); ff.stdin.write(surf.get_data())
        if i % 150 == 0: print(f"frame {i}/{n}", flush=True)
    ff.stdin.close(); ff.wait()
    print("listo:", f"{OUT}/reto_saludos.mp4")


def sfx_events():
    """Efectos de sonido sincronizados con la animación: (tiempo, tipo, parámetro)."""
    ev = [(0.15, "pop", 0), (0.45, "boom", 0), (0.7, "boom", 1), (1.3, "whoosh", 0)]
    p0 = T_PROBLEM[0]
    ev += [(p0, "whoosh", 0)] + [(p0 + st, "pop", i) for i, (st, _) in enumerate(PROB_LINES)]
    ev += [(p0 + 1.2 + i * 0.07, "blip", i) for i in range(10)]
    ev += [(p0 + 3.7, "question", 0)]
    t0 = T_THINK[0] + 0.4
    ev += [(t0 + i, "tick", i) for i in range(5)]
    a = T_TRAP[0]
    ev += [(a + 0.1, "pop", 0), (a + 0.6, "pop", 1), (a + 1.35, "wrong", 0), (a + 2.0, "pop", 2), (a + 2.75, "wrong", 0)]
    ev += [(T_SOLVE[0], "whoosh", 0)]
    _, lines = count_at(1e9)
    for idx, (k, o, p, ls) in enumerate(lines):
        ev.append((ls, "note", idx))
    ev += [(SUM_TIME, "success", 0)]
    a = T_FORMULA[0]
    ev += [(a, "whoosh", 0), (a + 0.1, "pop", 0), (a + 2.6, "pop", 1), (a + 3.6, "success", 1)]
    a = T_ANSWER[0]
    ev += [(a, "whoosh", 0), (a + 0.15, "fanfare", 0), (a + 0.6, "pop", 2), (a + 2.6, "pop", 3)]
    return ev


if __name__ == "__main__":
    main()
