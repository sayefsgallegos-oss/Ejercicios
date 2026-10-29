"""Reto: x² = 25, y³ = 27, ¿2(x + y)?  -> 16 (o −4 si x = −5)."""
from kit import *

DUR = 45.5
T = dict(title=(0.0, 3.2), problem=(3.2, 9.8), think=(9.8, 15.2), trap=(15.2, 20.8),
         solve=(20.8, 33.4), formula=(33.4, 39.6), answer=(39.6, DUR))
S = T["solve"][0]
P2 = S + 6.6          # inicio del paso 2 (el cubo)

LINES = [(0.5, [("x² = 25", NAVY)], 150, 100),
         (1.2, [("y³ = 27", NAVY)], 290, 100),
         (1.9, [("2(x + y) = ", NAVY), ("?", PINK)], 430, 100)]
QUESTION = (3.0, "¿Cuánto vale?")
SUMMARY = [[("x² = 25", BLUE), ("     ", NAVY), ("y³ = 27", ORANGE)], [("2(x + y) = ", NAVY), ("?", PINK)]]
TRAP = [(0.6, "x = 25 ÷ 2", "x² no es x por 2: es x por x"),
        (2.1, "y = 27 ÷ 3 = 9", "y³ es y × y × y, no y × 3")]

def tiles(ctx, t, al):
    n, s = 5, 110
    x0, y0 = W / 2 - n * s / 2, 640
    for r in range(n):
        for c in range(n):
            k = pop(t, S + 0.6 + (r * n + c) * 0.05, 0.35)
            if k <= 0: continue
            ctx.save(); ctx.translate(x0 + c * s + s / 2, y0 + r * s + s / 2); sc(ctx, k)
            rrect(ctx, -s / 2 + 5, -s / 2 + 5, s - 10, s - 10, 14)
            ctx.set_source_rgba(*hexc(GREEN if (r + c) % 2 else "#2ED18E", al)); ctx.fill(); ctx.restore()
    p = ease_out(prog(t, S + 2.4, S + 2.9))
    if p > 0:
        ctx.set_source_rgba(*hexc(YEL, al * p)); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(x0, y0 + n * s + 30); ctx.line_to(x0 + n * s * p, y0 + n * s + 30); ctx.stroke()
        ctx.move_to(x0 - 30, y0); ctx.line_to(x0 - 30, y0 + n * s * p); ctx.stroke()
        text(ctx, "5", W / 2, y0 + n * s + 85, 64, YEL, alpha=al * p, outline=NAVY, ow=10)
        text(ctx, "5", x0 - 80, y0 + n * s / 2, 64, YEL, alpha=al * p, outline=NAVY, ow=10)

def cube(ctx, t, al):
    s = 120; ca, sa = math.cos(math.pi / 6) * s, math.sin(math.pi / 6) * s
    ox, oy = W / 2, 1010
    cubes = [(i, j, k) for k in range(3) for i in range(3) for j in range(3)]
    order = sorted(cubes, key=lambda c: (c[2], c[0] + c[1]))
    for idx, (i, j, k) in enumerate(order):
        st = P2 + 0.5 + idx * 0.06
        p = ease_out(prog(t, st, st + 0.3))
        if p <= 0: continue
        x = ox + (i - j) * ca
        y = oy + (i + j) * sa - k * s - 120 * (1 - p)
        a = al * p
        top = [(x, y - s), (x + ca, y - s + sa), (x, y - s + 2 * sa), (x - ca, y - s + sa)]
        left = [(x - ca, y - s + sa), (x, y - s + 2 * sa), (x, y + 2 * sa), (x - ca, y + sa)]
        right = [(x + ca, y - s + sa), (x, y - s + 2 * sa), (x, y + 2 * sa), (x + ca, y + sa)]
        for face, col in [(top, "#FFC183"), (left, ORANGE), (right, "#D9661E")]:
            ctx.move_to(*face[0])
            for pt in face[1:]: ctx.line_to(*pt)
            ctx.close_path(); ctx.set_source_rgba(*hexc(col, a)); ctx.fill_preserve()
            ctx.set_source_rgba(1, 1, 1, 0.55 * a); ctx.set_line_width(3); ctx.stroke()
    p = ease_out(prog(t, P2 + 2.6, P2 + 3.0))
    if p > 0:   # arista frontal-derecha
        text(ctx, "3", ox + 2.1 * ca + 60, oy + 3.6 * sa + 50, 64, YEL, alpha=al * p, outline=NAVY, ow=10)
        text(ctx, "3", ox - 2.1 * ca - 60, oy + 3.6 * sa + 50, 64, YEL, alpha=al * p, outline=NAVY, ow=10)
        text(ctx, "3", ox + 3 * ca + 50, oy - 1.3 * s + 2 * sa, 64, YEL, alpha=al * p, outline=NAVY, ow=10)

def scene_solve(ctx, t):
    a, b = T["solve"]
    if not (a <= t < b + 0.3): return
    al = fade(t, a, b + 0.2)
    a1 = al * (1 - prog(t, P2 - 0.4, P2))
    a2 = al * prog(t, P2 - 0.1, P2 + 0.3)
    if a1 > 0:
        pill(ctx, W / 2, 330, "Paso 1:  x² = 25", 54, BLUE, WHITE, a1, pop(t, a + 0.1))
        caption(ctx, t, S + 0.6, [("x² es un cuadrado de ", WHITE), ("25", YEL), (" cuadritos", WHITE)], end=S + 2.4, alpha=a1, size=46)
        caption(ctx, t, S + 2.4, [("Su lado mide 5:  ", WHITE), ("x = 5", YEL)], end=S + 3.9, alpha=a1)
        caption(ctx, t, S + 3.9, [("¡Ojo! ", YEL), ("(−5) × (−5) = 25 también", WHITE)], alpha=a1, size=46)
        tiles(ctx, t, a1)
        k = pop(t, S + 4.6, 0.5)
        pill(ctx, W / 2, 1460, "x = 5   o   x = −5", 60, WHITE, BLUE, a1, k, padx=44, pady=24)
    if a2 > 0:
        pill(ctx, W / 2, 330, "Paso 2:  y³ = 27", 54, ORANGE, WHITE, a2, pop(t, P2))
        caption(ctx, t, P2 + 0.4, [("y³ es un cubo de ", WHITE), ("27", YEL), (" cubitos", WHITE)], end=P2 + 2.6, alpha=a2)
        caption(ctx, t, P2 + 2.6, [("Su arista mide 3:  ", WHITE), ("y = 3", YEL)], alpha=a2)
        cube(ctx, t, a2)
        k = pop(t, P2 + 3.6, 0.5)
        pill(ctx, W / 2, 1460, "(−3)³ = −27, así que solo y = 3", 44, WHITE, ORANGE, a2, k, padx=40, pady=22)

def scene_formula(ctx, t):
    a, b = T["formula"]
    if not (a <= t < b + 0.3): return
    al = fade(t, a, b + 0.2)
    pill(ctx, W / 2, 330, "Paso 3: reemplaza", 54, NAVY, WHITE, al, pop(t, a + 0.1))
    k1 = ease_out(prog(t, a + 0.3, a + 0.7))
    yb = 460 + 60 * (1 - k1)
    card(ctx, 90, yb, 900, 1000, 56, alpha=al * k1)
    for st, parts, y, size in [(0.6, [("x = 5", BLUE), ("      ", NAVY), ("y = 3", ORANGE)], 110, 72),
                               (1.3, [("2(", NAVY), ("5", BLUE), (" + ", NAVY), ("3", ORANGE), (")", NAVY)], 260, 96),
                               (2.0, [("= 2 × 8", NAVY)], 390, 96),
                               (2.7, [("= ", NAVY), ("16", PINK)], 540, 130)]:
        k = pop(t, a + st, 0.4)
        segs(ctx, parts, W / 2, yb + y, size, alpha=al * clamp(k), scale=k)
    k = pop(t, a + 3.9, 0.5)
    ctx.save(); ctx.translate(W / 2, yb + 830); sc(ctx, k)
    rrect(ctx, -400, -95, 800, 190, 40); ctx.set_source_rgba(*hexc("#EAF4FF", al)); ctx.fill()
    segs(ctx, [("Y si x = −5:", BLUE)], 0, -40, 46, alpha=al)
    segs(ctx, [("2(−5 + 3) = ", NAVY), ("−4", PINK)], 0, 30, 58, alpha=al)
    ctx.restore()

def draw(ctx, t):
    scene_title(ctx, t, *T["title"])
    scene_problem(ctx, t, T, LINES, QUESTION, SUMMARY, card_h=760, q_size=60)
    scene_think(ctx, t, *T["think"])
    scene_trap(ctx, t, *T["trap"], TRAP)
    scene_solve(ctx, t)
    scene_formula(ctx, t)
    scene_answer(ctx, t, T["answer"][0], DUR, "16", "con x positivo",
                 [("¿Y si ", NAVY), ("x² = 49", BLUE), (" e ", NAVY), ("y³ = 8", ORANGE), ("?", NAVY)],
                 note="(si x = −5, el resultado es −4)")

def events():
    a = T["problem"][0]
    ev = title_events() + [(a, "whoosh", 0)] + [(a + st, "pop", i) for i, (st, *_r) in enumerate(LINES)]
    ev += [(a + QUESTION[0], "question", 0)]
    ev += think_events(T["think"][0]) + trap_events(T["trap"][0], TRAP)
    ev += [(T["solve"][0], "whoosh", 0)] + [(S + 0.6 + i * 0.25, "blip", i) for i in range(5)]
    ev += [(S + 2.4, "success", 0), (S + 3.9, "pop", 1), (S + 4.6, "pop", 2), (P2, "whoosh", 0)]
    ev += [(P2 + 0.5 + i * 0.18, "note", i) for i in range(9)]
    ev += [(P2 + 2.6, "success", 0), (P2 + 3.6, "pop", 3)]
    a = T["formula"][0]
    ev += [(a, "whoosh", 0), (a + 0.1, "pop", 0)] + [(a + st, "pop", i) for i, st in enumerate([0.6, 1.3, 2.0])]
    ev += [(a + 2.7, "success", 1), (a + 3.9, "pop", 3)]
    return ev + answer_events(T["answer"][0])

if __name__ == "__main__":
    run("reto_potencias", DUR, draw, events(), transpose=2, breaks=[T["think"]])
