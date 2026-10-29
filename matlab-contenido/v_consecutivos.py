"""Reto: 3 números consecutivos suman 36. ¿Cuáles son?  -> 11, 12, 13."""
from kit import *

DUR = 45.5
T = dict(title=(0.0, 3.2), problem=(3.2, 9.8), think=(9.8, 15.2), trap=(15.2, 20.8),
         solve=(20.8, 33.0), formula=(33.0, 39.4), answer=(39.4, DUR))
S = T["solve"][0]
SPLIT, MOVE, DONE = S + 2.6, S + 6.4, S + 7.6

LINES = [(0.5, [("Tienes ", NAVY), ("3 números", BLUE)], 130, 64),
         (1.1, [("consecutivos", PURPLE), (" que", NAVY)], 220, 64),
         (1.7, [("suman ", NAVY), ("36", PINK)], 310, 64)]
QUESTION = (3.0, "¿Cuáles son?")
SUMMARY = [[("3 números ", NAVY), ("consecutivos", PURPLE)], [("suman ", NAVY), ("36", PINK), (" ¿cuáles son?", NAVY)]]
TRAP = [(0.6, "12 + 12 + 12 = 36", "¡son iguales, no consecutivos!"),
        (2.1, "10 + 12 + 14 = 36", "esos saltan de 2 en 2")]
TOWER_C = [SKY, PURPLE, PINK]

def boxes(ctx, t, cx, cy, al):
    a = T["problem"][0]
    y = cy + 470
    k = pop(t, a + 2.2, 0.5)
    ctx.save(); ctx.translate(W / 2, y); sc(ctx, k)
    for i, x in enumerate([-300, -90, 120]):
        rrect(ctx, x - 70, -70, 140, 140, 28); ctx.set_source_rgba(*hexc("#EAF4FF", al)); ctx.fill_preserve()
        ctx.set_source_rgba(*hexc(TOWER_C[i], al)); ctx.set_line_width(7); ctx.stroke()
        text(ctx, "?", x, 0, 80, TOWER_C[i], alpha=al)
    for x in (-195, 15):
        text(ctx, "+", x, 0, 70, NAVY, alpha=al)
    text(ctx, "= 36", 290, 0, 70, NAVY, alpha=al)
    ctx.restore()

BASE, BW, BH = 1420, 170, 46
TX = [W / 2 - 280, W / 2, W / 2 + 280]

def block_pos(b, t):
    gx, gy = b % 6, b // 6
    g = (W / 2 + (gx - 2.5) * 80, 760 + (gy - 2.5) * 80, 70, 70)
    tw, slot = b // 12, b % 12
    tow = (TX[tw], BASE - (slot + 0.5) * BH, BW, BH - 6)
    p = ease_in_out(prog(t, SPLIT + b * 0.025, SPLIT + 0.8 + b * 0.025))
    x, y, w, h = (g[i] + (tow[i] - g[i]) * p for i in range(4))
    col = YEL if p < 0.5 else TOWER_C[tw]
    if b == 11:   # el bloque de arriba de la 1.ª torre pasa a la 3.ª
        m = ease_in_out(prog(t, MOVE, MOVE + 0.9))
        if m > 0:
            ex, ey = TX[2], BASE - 12.5 * BH
            x = tow[0] + (ex - tow[0]) * m
            y = tow[1] + (ey - tow[1]) * m - 260 * math.sin(math.pi * m)
    return x, y, w, h, col

def scene_solve(ctx, t):
    a, b = T["solve"]
    if not (a <= t < b + 0.3): return
    al = fade(t, a, b + 0.2)
    pill(ctx, W / 2, 330, "Con bloques", 54, NAVY, WHITE, al, pop(t, a + 0.1))
    caption(ctx, t, S + 0.6, [("Tenemos ", WHITE), ("36", YEL), (" bloques", WHITE)], end=SPLIT, alpha=al)
    caption(ctx, t, SPLIT, [("En 3 partes iguales: ", WHITE), ("12", YEL), (" cada una", WHITE)], end=S + 5.2, alpha=al)
    caption(ctx, t, S + 5.2, [("Pero deben ser ", WHITE), ("consecutivos", YEL), ("…", WHITE)], end=DONE, alpha=al)
    caption(ctx, t, DONE, [("Pasamos 1 bloque: ", WHITE), ("11, 12, 13", YEL)], alpha=al)
    p0 = prog(t, SPLIT + 0.4, SPLIT + 0.8)
    if p0 > 0:
        ctx.rectangle(110, BASE, W - 220, 6); ctx.set_source_rgba(1, 1, 1, 0.8 * al * p0); ctx.fill()
    for bidx in range(36):
        k = pop(t, S + 0.6 + bidx * 0.03, 0.3)
        if k <= 0: continue
        x, y, w, h, col = block_pos(bidx, t)
        ctx.save(); ctx.translate(x, y); sc(ctx, k)
        rrect(ctx, -w / 2, -h / 2, w, h, 10); ctx.set_source_rgba(*hexc(col, al)); ctx.fill()
        ctx.restore()
    counts = [12, 12, 12] if t < MOVE + 0.9 else [11, 12, 13]
    for i in range(3):
        k = pop(t, SPLIT + 1.4, 0.4) if t < MOVE + 0.9 else pop(t, MOVE + 0.9, 0.45)
        text(ctx, str(counts[i]), TX[i], BASE + 70, 76, WHITE, alpha=al * clamp(k), scale=k, outline=NAVY, ow=10)
    p = ease_out(prog(t, S + 9.0, S + 9.5))
    if p > 0:
        for i in range(2):
            x1, x2 = TX[i] + 60, TX[i + 1] - 60
            arrow(ctx, x1, BASE + 160, x1 + (x2 - x1) * p, BASE + 160, YEL, 8, al * p, 20)
            text(ctx, "+1", (TX[i] + TX[i + 1]) / 2, BASE + 205, 44, YEL, alpha=al * p)

def scene_formula(ctx, t):
    a, b = T["formula"]
    if not (a <= t < b + 0.3): return
    al = fade(t, a, b + 0.2)
    pill(ctx, W / 2, 330, "Con álgebra", 54, NAVY, WHITE, al, pop(t, a + 0.1))
    k1 = ease_out(prog(t, a + 0.3, a + 0.7))
    yb = 460 + 60 * (1 - k1)
    card(ctx, 90, yb, 900, 1000, 56, alpha=al * k1)
    for st, parts, y, size in [(0.6, [("n", BLUE), (" + ", NAVY), ("(n+1)", PURPLE), (" + ", NAVY), ("(n+2)", PINK), (" = 36", NAVY)], 120, 60),
                               (1.5, [("3n + 3 = 36", NAVY)], 250, 84),
                               (2.3, [("3n = 33", NAVY)], 370, 84),
                               (3.1, [("n = ", NAVY), ("11", PINK)], 510, 110)]:
        k = pop(t, a + st, 0.4)
        segs(ctx, parts, W / 2, yb + y, size, alpha=al * clamp(k), scale=k)
    k = pop(t, a + 4.0, 0.5)
    ctx.save(); ctx.translate(W / 2, yb + 820); sc(ctx, k)
    rrect(ctx, -400, -110, 800, 220, 40); ctx.set_source_rgba(*hexc("#EAF4FF", al)); ctx.fill()
    segs(ctx, [("Atajo: ", BLUE), ("36 ÷ 3 = ", NAVY), ("12", PURPLE)], 0, -40, 60, alpha=al)
    segs(ctx, [("es el número del medio", NAVY)], 0, 40, 46, alpha=al)
    ctx.restore()

def draw(ctx, t):
    scene_title(ctx, t, *T["title"])
    scene_problem(ctx, t, T, LINES, QUESTION, SUMMARY, boxes, card_h=780, q_size=60)
    scene_think(ctx, t, *T["think"])
    scene_trap(ctx, t, *T["trap"], TRAP, eq_size=76)
    scene_solve(ctx, t)
    scene_formula(ctx, t)
    scene_answer(ctx, t, T["answer"][0], DUR, "11, 12, 13", "11 + 12 + 13 = 36",
                 [("¿Y si suman ", NAVY), ("75", PINK), ("?", NAVY)], big_size=110)

def events():
    a = T["problem"][0]
    ev = title_events() + [(a, "whoosh", 0)] + [(a + st, "pop", i) for i, (st, *_r) in enumerate(LINES)]
    ev += [(a + 2.2, "pop", 3), (a + QUESTION[0], "question", 0)]
    ev += think_events(T["think"][0]) + trap_events(T["trap"][0], TRAP)
    ev += [(T["solve"][0], "whoosh", 0)] + [(S + 0.6 + i * 0.09, "blip", i % 10) for i in range(12)]
    ev += [(SPLIT, "whoosh", 0), (SPLIT + 1.4, "pop", 1), (S + 5.2, "question", 0), (MOVE, "whoosh", 0),
           (MOVE + 0.9, "success", 0), (S + 9.0, "note", 0), (S + 9.2, "note", 2)]
    a = T["formula"][0]
    ev += [(a, "whoosh", 0), (a + 0.1, "pop", 0)] + [(a + st, "pop", i) for i, st in enumerate([0.6, 1.5, 2.3])]
    ev += [(a + 3.1, "success", 1), (a + 4.0, "pop", 3)]
    return ev + answer_events(T["answer"][0])

if __name__ == "__main__":
    run("reto_consecutivos", DUR, draw, events(), transpose=-3, breaks=[T["think"]])
