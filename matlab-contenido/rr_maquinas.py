"""Matti y Numi presentan el reto del día: 5 máquinas, 5 piezas, 5 minutos -> 100 máquinas, 100 piezas = 5 minutos."""
from robots import *

DUR = 46.0
CARD = (90, 300, 900, 780)          # x, y, ancho, alto
MX, NX, FLOOR = 270, 810, 1730
DIALOG = [
    (3.4, 6.6, "numi", ["¡Matti! Te traje", "un reto de máquinas."]),
    (6.8, 8.8, "matti", ["A ver, dime…"]),
    (18.6, 21.0, "numi", ["¡Fácil!", "¡100 minutos!"]),
    (21.6, 24.6, "matti", ["Casi, Numi.", "Mira con calma…"]),
    (25.0, 28.2, "matti", ["Cada máquina hace", "1 pieza en 5 minutos."]),
    (30.2, 33.4, "matti", ["Si hay 100 máquinas,", "¡trabajan a la vez!"]),
    (36.6, 39.4, "numi", ["¡Ahh! ¡Solo", "5 minutos!"]),
]
cast = Cast(DIALOG)
MATTI = [(0, "a00"), (9.0, "b07"), (18.4, "a00"), (21.6, "b04"), (35.8, "b05"), (41.0, "b10")]
NUMI = [(0, "d10"), (6.8, "d01"), (13.0, "d17"), (18.4, "d08"), (21.2, "d17"), (25.0, "d15"), (35.8, "d10"), (41.0, "d01")]
WRONG = 21.2
A1, A2, ANS, CTA = 25.0, 30.0, 35.8, 41.0

def pose_at(sched, t):
    cur = sched[0]
    for s in sched:
        if t >= s[0]: cur = s
    return cur[1], 1 + 0.08 * (1 - prog(t, cur[0], cur[0] + 0.25)) if cur[0] > 0 else 1

def machine(ctx, cx, cy, s, p, t, alpha=1.0, k=1.0):
    if k <= 0.001: return
    ctx.save(); ctx.translate(cx, cy); sc(ctx, k)
    rrect(ctx, -s / 2, -s * 0.45, s, s * 0.8, s * 0.14); ctx.set_source_rgba(*hexc("#DDE7F5", alpha)); ctx.fill_preserve()
    ctx.set_line_width(max(2, s * 0.04)); ctx.set_source_rgba(*hexc(NAVY, alpha)); ctx.stroke()
    # engranaje
    ang = t * 6 if 0 < p < 1 else 0
    ctx.save(); ctx.translate(0, -s * 0.1); ctx.rotate(ang)
    for i in range(8):
        ctx.save(); ctx.rotate(i * math.pi / 4); ctx.rectangle(-s * 0.04, -s * 0.24, s * 0.08, s * 0.1); ctx.restore()
    ctx.set_source_rgba(*hexc(BLUE, alpha)); ctx.fill()
    ctx.arc(0, 0, s * 0.17, 0, 2 * math.pi); ctx.fill()
    ctx.arc(0, 0, s * 0.06, 0, 2 * math.pi); ctx.set_source_rgba(*hexc("#DDE7F5", alpha)); ctx.fill()
    ctx.restore()
    # barra de progreso
    rrect(ctx, -s * 0.36, s * 0.17, s * 0.72, s * 0.11, s * 0.05); ctx.set_source_rgba(*hexc("#B8C6DA", alpha)); ctx.fill()
    if p > 0:
        rrect(ctx, -s * 0.36, s * 0.17, s * 0.72 * p, s * 0.11, s * 0.05); ctx.set_source_rgba(*hexc(GREEN, alpha)); ctx.fill()
    ctx.restore()

def piece(ctx, cx, cy, s, k, alpha=1.0):
    if k <= 0.001: return
    ctx.save(); ctx.translate(cx, cy); sc(ctx, k)
    a = s / 2
    for pts, col in [([(0, -a), (a, -a / 2), (0, 0), (-a, -a / 2)], "#FFC183"), ([(-a, -a / 2), (0, 0), (0, a), (-a, a / 2)], ORANGE),
                     ([(a, -a / 2), (0, 0), (0, a), (a, a / 2)], "#D9661E")]:
        ctx.move_to(*pts[0])
        for q in pts[1:]: ctx.line_to(*q)
        ctx.close_path(); ctx.set_source_rgba(*hexc(col, alpha)); ctx.fill()
    ctx.restore()

def clock(ctx, x, y, minutes, alpha):
    pill(ctx, x, y, f"Tiempo: {minutes} min", 44, NAVY, WHITE, alpha, padx=30, pady=14)

def card_content(ctx, t):
    x, y, w, h = CARD
    # 1) enunciado
    a = fade(t, 9.0, A1)
    if a > 0:
        for st, parts, yy, size in [(9.3, [("5 máquinas", BLUE), (" hacen", NAVY)], 110, 62),
                                    (9.9, [("5 piezas", ORANGE), (" en ", NAVY), ("5 minutos", PINK)], 195, 62),
                                    (11.4, [("¿Cuánto tardan ", NAVY), ("100 máquinas", BLUE)], 520, 54),
                                    (11.9, [("en hacer ", NAVY), ("100 piezas", ORANGE), ("?", PINK)], 600, 54)]:
            k = pop(t, st, 0.4)
            segs(ctx, parts, W / 2, y + yy, size, alpha=a * clamp(k), scale=k)
        for i in range(5):
            machine(ctx, W / 2 + (i - 2) * 160, y + 345, 120, 0, t, a, pop(t, 10.4 + i * 0.08, 0.4))
        st = ease_out(prog(t, WRONG, WRONG + 0.25))
        if st > 0:
            ctx.save(); ctx.translate(W / 2, y + 400); ctx.rotate(-0.12); sc(ctx, 1.6 - 0.6 * st)
            rrect(ctx, -270, -80, 540, 160, 30); ctx.set_source_rgba(1, 1, 1, 0.92 * a * st); ctx.fill_preserve()
            ctx.set_line_width(12); ctx.set_source_rgba(*hexc(RED, a * st)); ctx.stroke()
            text(ctx, "100 minutos", 0, 0, 84, RED, alpha=a * st)
            strike(ctx, 0, 0, 230, 1, a * st)
            ctx.restore()
    # 2) una máquina, una pieza, 5 minutos
    a = fade(t, A1, A2)
    if a > 0:
        segs(ctx, [("Cada máquina: ", NAVY), ("1 pieza", ORANGE), (" en ", NAVY), ("5 min", PINK)], W / 2, y + 100, 54, alpha=a)
        p = prog(t, A1 + 0.8, A1 + 3.6)
        clock(ctx, W / 2, y + 200, int(p * 5), a)
        for i in range(5):
            cx = W / 2 + (i - 2) * 165
            machine(ctx, cx, y + 400, 140, p, t, a, pop(t, A1 + 0.1 + i * 0.08, 0.4))
            piece(ctx, cx, y + 590, 70, pop(t, A1 + 3.6 + i * 0.05, 0.4), a)
        segs(ctx, [("5 máquinas = ", NAVY), ("5 piezas", ORANGE), (" en ", NAVY), ("5 min", PINK)], W / 2, y + 700, 50,
             alpha=a * ease_out(prog(t, A1 + 4.0, A1 + 4.3)))
    # 3) cien máquinas a la vez
    a = fade(t, A2, ANS)
    if a > 0:
        segs(ctx, [("¡", NAVY), ("100 máquinas", BLUE), (" a la vez!", NAVY)], W / 2, y + 85, 56, alpha=a)
        p = prog(t, A2 + 1.2, A2 + 4.2)
        clock(ctx, W / 2, y + 170, int(p * 5), a)
        for r in range(10):
            for c in range(10):
                cx = W / 2 + (c - 4.5) * 66; cy = y + 255 + r * 50
                machine(ctx, cx, cy, 44, p, t, a, pop(t, A2 + 0.1 + (r + c) * 0.03, 0.3))
                piece(ctx, cx + 18, cy - 14, 22, pop(t, A2 + 4.2 + (r + c) * 0.015, 0.3), a)
        k = pop(t, A2 + 4.5, 0.45)
        pill(ctx, W / 2, y + h - 40, "100 piezas en 5 minutos", 46, GREEN, WHITE, a, k, padx=34, pady=16)
    # 4) respuesta
    a = fade(t, ANS, CTA)
    if a > 0:
        k = pop(t, ANS + 0.1, 0.55)
        text(ctx, "Respuesta:", W / 2, y + 150, 60, BLUE, alpha=a)
        text(ctx, "5 minutos", W / 2, y + 360, 170, PINK, alpha=a, scale=k * (1 + 0.02 * math.sin(t * 5)))
        ctx.arc(W / 2 + 330, y + 210, 60, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(GREEN, a * clamp(k))); ctx.fill()
        check(ctx, W / 2 + 330, y + 210, 60 * clamp(k), WHITE, prog(t, ANS + 0.4, ANS + 0.8))
        segs(ctx, [("Más máquinas ", NAVY), ("no", PINK), (" es más tiempo:", NAVY)], W / 2, y + 560, 48, alpha=a * ease_out(prog(t, ANS + 1, ANS + 1.4)))
        segs(ctx, [("cada una hace ", NAVY), ("su", PINK), (" pieza", NAVY)], W / 2, y + 630, 48, alpha=a * ease_out(prog(t, ANS + 1.2, ANS + 1.6)))
    # 5) próximo reto
    a = fade(t, CTA, DUR + 1)
    if a > 0:
        text(ctx, "Próximo reto:", W / 2, y + 100, 56, BLUE, alpha=a)
        for i, (parts, yy) in enumerate([([("3 gatos", PURPLE), (" cazan ", NAVY), ("3 ratones", ORANGE)], 200),
                                         ([("en ", NAVY), ("3 minutos", PINK), (".", NAVY)], 270),
                                         ([("¿Cuántos gatos cazan", NAVY)], 380),
                                         ([("100 ratones", ORANGE), (" en ", NAVY), ("100 min", PINK), ("?", NAVY)], 450)]):
            k = pop(t, CTA + 0.3 + i * 0.25, 0.4)
            segs(ctx, parts, W / 2, y + yy, 54, alpha=a * clamp(k), scale=k)
        sprite(ctx, "d19", W / 2 + 250, y + h - 30, 200, a * clamp(pop(t, CTA + 1.4, 0.5)))
        text(ctx, "Comenta tu respuesta", W / 2 - 90, y + h - 110, 44, GREY, "Nunito ExtraBold", alpha=a * ease_out(prog(t, CTA + 1.6, CTA + 2)))

def draw(ctx, t):
    # portada
    if t < 3.8:
        out = 1 - ease_in_out(prog(t, 3.2, 3.7))
        pill(ctx, W / 2, 420, "Matti y Numi presentan", 52, WHITE, BLUE, out, pop(t, 0.2))
        text(ctx, "EL RETO", W / 2, 640, 190, YEL, scale=pop(t, 0.5, 0.55), alpha=out, outline=NAVY, ow=30, rot=-0.05)
        text(ctx, "DEL DÍA", W / 2, 840, 190, YEL, scale=pop(t, 0.75, 0.55), alpha=out, outline=NAVY, ow=30, rot=-0.05)
        name_tag(ctx, MX, 1800, "Matti", BLUE, out, pop(t, 1.3))
        name_tag(ctx, NX, 1800, "Numi", ORANGE, out, pop(t, 1.45))
    # tarjeta
    if 9.0 <= t:
        k = ease_out(prog(t, 9.0, 9.4))
        x, y, w, h = CARD
        card(ctx, x, y + 80 * (1 - k), w, h, 56, alpha=k)
        rrect(ctx, x, y + 80 * (1 - k), w, 16, 8); ctx.set_source_rgba(*hexc(YEL, k)); ctx.fill()
        card_content(ctx, t)
    # temporizador
    if 13.2 <= t < 18.8:
        al = fade(t, 13.2, 18.6)
        cx, cy, r = W / 2, 1250, 95
        ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(WHITE, al)); ctx.fill()
        left = clamp(1 - (t - 13.4) / 5)
        ctx.set_line_width(16); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.arc(cx, cy, r - 8, -math.pi / 2, -math.pi / 2 + 2 * math.pi * left)
        ctx.set_source_rgba(*hexc(YEL if left > 0.4 else ORANGE if left > 0.2 else RED, al)); ctx.stroke()
        text(ctx, str(max(1, math.ceil(5 - (t - 13.4) - 1e-6))), cx, cy, 100, NAVY, alpha=al)
        text(ctx, "Piensa…", cx, cy - 140, 50, WHITE, alpha=al, outline=NAVY, ow=8)
    # robots
    mx = -300 + (MX + 300) * ease_out(prog(t, 0.4, 1.2))
    nx = W + 300 - (W + 300 - NX) * ease_out(prog(t, 0.6, 1.4))
    mp, ms = pose_at(MATTI, t); np_, ns = pose_at(NUMI, t)
    droop = -0.12 * prog(t, WRONG, WRONG + 0.3) * (1 - prog(t, A1 - 0.3, A1))
    heads = {"matti": robot(ctx, t, cast, "matti", mp, mx, FLOOR, 380, scale=ms),
             "numi": robot(ctx, t, cast, "numi", np_, nx, FLOOR, 350, scale=ns, rot=droop, ph=1.3)}
    if WRONG + 0.2 <= t < A1:
        sweat(ctx, nx + 120, FLOOR - 330, t)
    cast.bubbles(ctx, t, heads)
    if t >= ANS: confetti(ctx, t, ANS + 0.1, W / 2, 560)
    if t >= CTA:
        pill(ctx, W / 2, 1150, "Síguenos para más retos", 48, YEL, NAVY, 1, pop(t, CTA + 2.2) * (1 + 0.03 * math.sin(t * 6)), padx=40, pady=22)

def events():
    ev = [(0.2, "pop", 0), (0.5, "boom", 0), (0.75, "boom", 1), (0.4, "whoosh", 0), (0.6, "whoosh", 0), (1.3, "pop", 1), (1.45, "pop", 2)]
    ev += [(9.0, "whoosh", 0), (9.3, "pop", 0), (9.9, "pop", 1)] + [(10.4 + i * 0.08, "blip", i) for i in range(5)]
    ev += [(11.4, "pop", 2), (11.9, "question", 0)] + [(13.4 + i, "tick", i) for i in range(5)]
    ev += [(WRONG, "wrong", 0), (A1, "whoosh", 0)] + [(A1 + 0.8 + i * 0.7, "tick", 0) for i in range(4)]
    ev += [(A1 + 3.6 + i * 0.05, "blip", i) for i in range(5)] + [(A2, "whoosh", 0)] + [(A2 + 0.1 + i * 0.05, "blip", i) for i in range(10)]
    ev += [(A2 + 1.2 + i * 0.75, "tick", 0) for i in range(4)] + [(A2 + 4.2, "success", 0), (A2 + 4.5, "pop", 3)]
    ev += [(ANS, "whoosh", 0), (ANS + 0.1, "fanfare", 0), (CTA, "whoosh", 0)] + [(CTA + 0.3 + i * 0.25, "pop", i) for i in range(4)]
    ev += [(CTA + 2.2, "pop", 3)]
    return ev

if __name__ == "__main__":
    render("robots_reto_maquinas", DUR, draw, events(), DIALOG, transpose=0, breaks=[(13.0, 18.6)], mgain=0.45)
