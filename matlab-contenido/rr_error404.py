"""Error 404: Numi se equivocó — 2 + 3 × 4 (Numi dice 20; Matti depura: 14)."""
from robots import *

DUR = 42.0
CARD = (90, 300, 900, 780)
MX, NX, FLOOR = 270, 810, 1730
ALARM, MATTI_IN, SCAN, BUG, RULE, FIX, HAPPY, CTA = 10.4, 12.6, 15.8, 17.0, 21.0, 25.0, 31.0, 34.6
DIALOG = [
    (3.8, 6.4, "numi", ["¡Este es fácil!", "Yo lo resuelvo."]),
    (8.4, 10.2, "numi", ["¡Listo! Es 20."]),
    (13.0, 15.6, "matti", ["Modo depuración", "activado."]),
    (17.2, 20.8, "matti", ["El bug está aquí:", "sumaste antes de multiplicar."]),
    (21.2, 24.6, "matti", ["Primero se multiplica,", "después se suma."]),
    (25.4, 28.2, "matti", ["Primero 3 × 4 = 12…"]),
    (28.4, 30.8, "matti", ["…luego 2 + 12 = 14."]),
    (31.2, 34.2, "numi", ["¡Bug corregido!", "¡Gracias, Matti!"]),
]
cast = Cast(DIALOG)
MATTI = [(0, "b00"), (BUG, "b02"), (RULE, "b04"), (HAPPY, "b01"), (CTA, "b10")]
NUMI = [(0, "d17"), (3.6, "d15"), (8.2, "d16"), (ALARM, "d17"), (HAPPY, "d10"), (CTA, "d01")]

def pose_at(sched, t):
    cur = sched[0]
    for s in sched:
        if t >= s[0]: cur = s
    return cur[1], (1 + 0.08 * (1 - prog(t, cur[0], cur[0] + 0.25))) if cur[0] > 0 else 1

def written(ctx, s, x, y, size, color, t, st, alpha=1.0, cps=10):
    """Texto que se va escribiendo, alineado a la izquierda desde x."""
    n = int((t - st) * cps)
    if n <= 0: return
    text(ctx, s[:n], x, y, size, color, alpha=alpha, align="l")

def box_around(ctx, full, part_start, part, x, y, size, color, alpha, lw=7):
    x0 = x + text_w(ctx, full[:part_start], size); w = text_w(ctx, part, size)
    rrect(ctx, x0 - 14, y - size * 0.62, w + 28, size * 1.2, 22)
    ctx.set_line_width(lw); ctx.set_source_rgba(*hexc(color, alpha)); ctx.stroke()

def board(ctx, t):
    x, y, w, h = CARD
    LX = x + 185
    # 1) lo que escribe Numi
    a = fade(t, 3.4, RULE)
    if a > 0:
        text(ctx, "Pizarra de Numi", W / 2, y + 70, 40, GREY, "Nunito ExtraBold", alpha=a)
        written(ctx, "2 + 3 × 4", LX, y + 200, 100, NAVY, t, 3.8, a)
        written(ctx, "= 5 × 4", LX, y + 360, 100, NAVY, t, 6.8, a)
        written(ctx, "= 20", LX, y + 520, 100, NAVY, t, 7.8, a)
        # escaneo
        p = prog(t, SCAN, SCAN + 1.2)
        if 0 < p < 1:
            yy = y + 110 + 480 * p
            ctx.rectangle(x + 20, y + 110, w - 40, yy - y - 110); ctx.set_source_rgba(0.13, 0.76, 0.5, 0.12 * a); ctx.fill()
            ctx.rectangle(x + 20, yy - 4, w - 40, 8); ctx.set_source_rgba(0.13, 0.76, 0.5, 0.9 * a); ctx.fill()
        if t >= BUG:
            k = pop(t, BUG, 0.4)
            box_around(ctx, "= 5 × 4", 2, "5", LX, y + 360, 100, RED, a * clamp(k), 9)
            pill(ctx, x + 85, y + 360, "BUG", 40, RED, WHITE, a, k, padx=18, pady=10)
            segs(ctx, [("2 + 3 = 5 ", RED), ("se hizo primero", GREY)], W / 2, y + 650, 44, alpha=a * ease_out(prog(t, BUG + 0.6, BUG + 1.0)))
            strike(ctx, LX + text_w(ctx, "= 20", 100) / 2, y + 520, text_w(ctx, "= 20", 100) / 2 + 20, ease_out(prog(t, BUG + 1.2, BUG + 1.5)), a)
    # 2) la regla
    a = fade(t, RULE, FIX)
    if a > 0:
        text(ctx, "Orden de operaciones", W / 2, y + 110, 62, BLUE, alpha=a)
        for i, (n, ops, desc, col) in enumerate([("1º", "×  ÷", "multiplica y divide", PINK), ("2º", "+  −", "suma y resta", GREEN)]):
            k = pop(t, RULE + 0.5 + i * 0.9, 0.45)
            yy = y + 290 + i * 230
            ctx.save(); ctx.translate(W / 2, yy); sc(ctx, k)
            rrect(ctx, -390, -90, 780, 180, 40); ctx.set_source_rgba(*hexc("#EAF4FF", a)); ctx.fill()
            text(ctx, n, -300, 0, 80, col, alpha=a)
            text(ctx, ops, -110, 0, 90, NAVY, alpha=a)
            text(ctx, desc, 180, 0, 42, GREY, "Nunito ExtraBold", alpha=a)
            ctx.restore()
    # 3) la corrección
    a = fade(t, FIX, CTA)
    if a > 0:
        text(ctx, "Corrección de Matti", W / 2, y + 70, 40, GREY, "Nunito ExtraBold", alpha=a)
        text(ctx, "2 + 3 × 4", LX, y + 200, 100, NAVY, alpha=a, align="l")
        if t >= FIX + 0.6:
            box_around(ctx, "2 + 3 × 4", 4, "3 × 4", LX, y + 200, 100, BLUE, a * clamp(pop(t, FIX + 0.6, 0.4)))
        written(ctx, "= 2 + 12", LX, y + 360, 100, NAVY, t, FIX + 1.6, a)
        written(ctx, "= 14", LX, y + 520, 100, GREEN, t, FIX + 3.4, a)
        k = pop(t, FIX + 3.9, 0.45)
        cx = LX + text_w(ctx, "= 14", 100) + 90
        ctx.arc(cx, y + 515, 50, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(GREEN, a * clamp(k))); ctx.fill()
        check(ctx, cx, y + 515, 50 * clamp(k), WHITE, prog(t, FIX + 4.1, FIX + 4.4))
        if t >= HAPPY:
            pill(ctx, W / 2, y + 670, "BUG CORREGIDO", 52, GREEN, WHITE, a, pop(t, HAPPY + 0.2), padx=40, pady=18)
    # 4) cierre
    a = fade(t, CTA, DUR + 1)
    if a > 0:
        for i, (parts, yy, size) in enumerate([([("¿Tu hijo también", NAVY)], 110, 60), ([("se equivoca aquí?", NAVY)], 185, 60),
                                                ([("En matLab ", BLUE), ("encontramos el bug", PINK)], 290, 50)]):
            k = pop(t, CTA + 0.2 + i * 0.3, 0.4)
            segs(ctx, parts, W / 2, y + yy, size, alpha=a * clamp(k), scale=k)
        k = pop(t, CTA + 1.4, 0.5)
        ctx.save(); ctx.translate(W / 2, y + 500); sc(ctx, k)
        rrect(ctx, -380, -110, 760, 220, 40); ctx.set_source_rgba(*hexc("#EAF4FF", a)); ctx.fill()
        text(ctx, "Reto:", 0, -55, 46, BLUE, alpha=a)
        segs(ctx, [("10 − 2 × 3 = ", NAVY), ("?", PINK)], 0, 30, 90, alpha=a)
        ctx.restore()
        text(ctx, "Comenta tu respuesta", W / 2, y + 690, 44, GREY, "Nunito ExtraBold", alpha=a * ease_out(prog(t, CTA + 1.9, CTA + 2.3)))

def glitch_title(ctx, t, s, x, y, size, alpha):
    j = 1 if int(t * 12) % 4 == 0 else 0
    for dx, col in [(-8 - 10 * j, "#22E3FF"), (8 + 10 * j, "#FF2D55")]:
        text(ctx, s, x + dx, y, size, col, alpha=alpha * 0.8)
    text(ctx, s, x, y, size, WHITE, alpha=alpha, outline=NAVY, ow=16)
    if j:
        ctx.rectangle(x - 420, y - 20, 840, 18); ctx.set_source_rgba(1, 1, 1, 0.5 * alpha); ctx.fill()

def warn_icon(ctx, x, y, s, alpha):
    ctx.move_to(x, y - s); ctx.line_to(x + s * 1.1, y + s * 0.8); ctx.line_to(x - s * 1.1, y + s * 0.8); ctx.close_path()
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_line_width(s * 0.25)
    ctx.set_source_rgba(*hexc(YEL, alpha)); ctx.stroke_preserve(); ctx.fill()
    rrect(ctx, x - s * 0.1, y - s * 0.45, s * 0.2, s * 0.75, s * 0.1); ctx.set_source_rgba(*hexc(NAVY, alpha)); ctx.fill()
    ctx.arc(x, y + s * 0.5, s * 0.12, 0, 2 * math.pi); ctx.fill()

def draw(ctx, t):
    if t < 3.8:
        out = 1 - ease_in_out(prog(t, 3.2, 3.7))
        glitch_title(ctx, t, "ERROR 404", W / 2, 620, 170, out * clamp(pop(t, 0.2, 0.5)))
        pill(ctx, W / 2, 820, "Numi se equivocó", 60, RED, WHITE, out, pop(t, 0.9))
    if t >= 3.4:
        k = ease_out(prog(t, 3.4, 3.8)); x, y, w, h = CARD
        card(ctx, x, y + 80 * (1 - k), w, h, 56, alpha=k)
        rrect(ctx, x, y + 80 * (1 - k), w, 16, 8); ctx.set_source_rgba(*hexc(ORANGE if t < FIX else BLUE, k)); ctx.fill()
        board(ctx, t)
    # alarma
    if ALARM <= t < MATTI_IN + 0.6:
        al = fade(t, ALARM, MATTI_IN + 0.6, 0.2)
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(1, 0.1, 0.2, 0.22 * abs(math.sin(t * 9)) * al); ctx.fill()
        k = pop(t, ALARM + 0.1, 0.35)
        ctx.save(); ctx.translate(W / 2, 1200); sc(ctx, k); ctx.rotate(-0.04)
        rrect(ctx, -400, -90, 800, 180, 40); ctx.set_source_rgba(*hexc(RED, al)); ctx.fill()
        warn_icon(ctx, -290, 0, 52, al)
        text(ctx, "ERROR 404", 60, 0, 104, WHITE, alpha=al)
        ctx.restore()
    # robots
    mx = -300 + (MX + 300) * ease_out(prog(t, MATTI_IN, MATTI_IN + 0.7))
    nx = W + 300 - (W + 300 - NX) * ease_out(prog(t, 0.6, 1.3))
    mp, ms = pose_at(MATTI, t); np_, ns = pose_at(NUMI, t)
    shake = 8 * math.sin(t * 55) if ALARM <= t < MATTI_IN else 0
    heads = {"numi": robot(ctx, t, cast, "numi", np_, nx + shake, FLOOR, 360, scale=ns, ph=1.3)}
    if t >= MATTI_IN:
        heads["matti"] = robot(ctx, t, cast, "matti", mp, mx, FLOOR, 360, scale=ms)
    if ALARM <= t < HAPPY:
        sweat(ctx, nx + 120, FLOOR - 340, t)
    cast.bubbles(ctx, t, heads)
    if t >= HAPPY: confetti(ctx, t, HAPPY + 0.2, W / 2, 970)
    if t >= CTA:
        pill(ctx, W / 2, 1150, "Síguenos para más retos", 48, YEL, NAVY, 1, pop(t, CTA + 2.4) * (1 + 0.03 * math.sin(t * 6)), padx=40, pady=22)

def events():
    ev = [(0.2, "glitch", 0), (0.9, "pop", 0), (0.6, "whoosh", 0), (3.4, "whoosh", 0)]
    ev += [(s + i * 0.1, "blip", i) for s, n in ((3.8, 9), (6.8, 7), (7.8, 4)) for i in range(n)]
    ev += [(8.2, "pop", 1), (ALARM, "siren", 0), (ALARM + 0.1, "glitch", 0), (MATTI_IN, "whoosh", 0)]
    ev += [(SCAN, "rise", 0), (BUG, "wrong", 0), (BUG + 1.2, "pop", 2), (RULE, "whoosh", 0), (RULE + 0.5, "pop", 0), (RULE + 1.4, "pop", 1)]
    ev += [(FIX, "whoosh", 0), (FIX + 0.6, "pop", 3)] + [(FIX + 1.6 + i * 0.1, "blip", i) for i in range(8)]
    ev += [(FIX + 3.4 + i * 0.1, "blip", i + 3) for i in range(4)] + [(FIX + 3.9, "success", 0), (HAPPY + 0.2, "fanfare", 0)]
    ev += [(CTA, "whoosh", 0)] + [(CTA + 0.2 + i * 0.3, "pop", i) for i in range(3)] + [(CTA + 1.4, "question", 0), (CTA + 2.4, "pop", 3)]
    return ev

if __name__ == "__main__":
    render("robots_error404", DUR, draw, events(), DIALOG, transpose=-2, breaks=[(ALARM, SCAN + 1.5)], mgain=0.42)
