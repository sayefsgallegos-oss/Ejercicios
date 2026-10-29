"""Reto: un número sube 20% y luego baja 20%. ¿Vuelve al original?  -> No, queda en 96%."""
from kit import *

DUR = 45.5
T = dict(title=(0.0, 3.2), problem=(3.2, 10.4), think=(10.4, 15.8), trap=(15.8, 20.6),
         solve=(20.6, 33.6), formula=(33.6, 39.6), answer=(39.6, DUR))
S = T["solve"][0]
S1, S2, S3, S4 = S + 0.6, S + 2.4, S + 5.4, S + 9.6

LINES = [(0.55, [("Un número ", NAVY), ("aumenta 20%", GREEN)], 130, 64),
         (1.6, [("y luego ", NAVY), ("disminuye 20%", RED)], 220, 64)]
QUESTION = (3.4, "¿Vuelve al número original?")
SUMMARY = [[("Sube ", NAVY), ("20%", GREEN), (" y baja ", NAVY), ("20%", RED)],
           [("¿Vuelve al original?", NAVY)]]
TRAP = [(0.6, "+20% − 20% = 0%", "los dos 20% no son del mismo número")]

def flow(ctx, t, cx, cy, al):
    a = T["problem"][0]
    y = cy + 420
    xs = [W / 2 - 300, W / 2, W / 2 + 300]
    for i, (x, lab, col) in enumerate(zip(xs, ["N", "?", "¿N?"], [BLUE, GREEN, PINK])):
        k = pop(t, a + 1.0 + i * 0.8, 0.45)
        ctx.save(); ctx.translate(x, y); sc(ctx, k)
        ctx.arc(0, 0, 80, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(col, al)); ctx.fill()
        text(ctx, lab, 0, 0, 60 if len(lab) < 3 else 48, WHITE, alpha=al)
        ctx.restore()
    for i, (lab, col) in enumerate([("+20%", GREEN), ("−20%", RED)]):
        p = ease_out(prog(t, a + 1.4 + i * 0.8, a + 1.7 + i * 0.8))
        if p <= 0: continue
        x1 = xs[i] + 95; x2 = x1 + (xs[i + 1] - 95 - x1) * p
        arrow(ctx, x1, y, x2, y, col, 9, al * p, 22)
        text(ctx, lab, (xs[i] + xs[i + 1]) / 2, y - 60, 44, col, alpha=al * p)

BASE, UNIT, BW = 1560, 5.8, 200
BX = [W / 2 - 300, W / 2, W / 2 + 300]

def bar(ctx, x, v0, v1, col, al):
    if v1 <= v0: return
    rrect(ctx, x - BW / 2, BASE - v1 * UNIT, BW, (v1 - v0) * UNIT, 14 if v0 == 0 else 6)
    ctx.set_source_rgba(*hexc(col, al)); ctx.fill()

def scene_solve(ctx, t):
    a, b = T["solve"]
    if not (a <= t < b + 0.3): return
    al = fade(t, a, b + 0.2)
    pill(ctx, W / 2, 330, "Probemos con 100", 54, NAVY, WHITE, al, pop(t, a + 0.1))
    caption(ctx, t, S1, [("Empezamos con ", WHITE), ("100", YEL)], end=S2, alpha=al)
    caption(ctx, t, S2, [("20% de 100 = ", WHITE), ("+20", YEL)], end=S3, alpha=al)
    caption(ctx, t, S3, [("Ahora el 20% es de ", WHITE), ("120", YEL)], end=S3 + 2.0, alpha=al)
    caption(ctx, t, S3 + 2.0, [("20% de 120 = ", WHITE), ("−24", YEL)], end=S4, alpha=al)
    caption(ctx, t, S4, [("¡Quedó en ", WHITE), ("96", YEL), (", no en 100!", WHITE)], alpha=al)
    # piso
    ctx.rectangle(80, BASE, W - 160, 6); ctx.set_source_rgba(1, 1, 1, 0.8 * al); ctx.fill()
    # barra 1
    g = ease_out(prog(t, S1, S1 + 0.7))
    bar(ctx, BX[0], 0, 100 * g, WHITE, al)
    # barra 2
    g2 = ease_out(prog(t, S2 + 0.1, S2 + 0.6)); g3 = ease_out(prog(t, S2 + 0.8, S2 + 1.4))
    bar(ctx, BX[1], 0, 100 * g2, WHITE, al)
    bar(ctx, BX[1], 100, 100 + 20 * g3, GREEN, al)
    if g3 > 0: text(ctx, "+20", BX[1], BASE - 110 * UNIT, 44, WHITE, alpha=al * g3)
    # barra 3: 120 en 5 tajadas de 24, la de arriba sale volando
    g4 = ease_out(prog(t, S3 + 0.1, S3 + 0.7))
    sl = prog(t, S3 + 0.9, S3 + 1.6)
    fly = ease_in_out(prog(t, S3 + 2.4, S3 + 3.2))
    for i in range(5):
        v0, v1 = i * 24 * g4, (i + 1) * 24 * g4
        top = i == 4
        col = WHITE if not top or t < S3 + 2.0 else RED
        if top and fly > 0:
            ctx.save(); ctx.translate(160 * fly, -260 * fly); ctx.rotate(0.3 * fly)
            bar(ctx, BX[2], v0, v1, col, al * (1 - fly)); ctx.restore()
        else:
            bar(ctx, BX[2], v0, v1, col, al)
        if i and sl > 0 and not (top and fly > 0):
            ctx.rectangle(BX[2] - BW / 2, BASE - v0 * UNIT - 3, BW, 6); ctx.set_source_rgba(*hexc(SKY, al * sl)); ctx.fill()
        if sl > 0 and not (top and fly > 0.05):
            text(ctx, "24", BX[2], BASE - (v0 + 12 * g4) * UNIT, 38, NAVY if not (top and t >= S3 + 2.0) else WHITE, alpha=al * sl)
    # valores y etiquetas
    for x, val, lab, lc, st in [(BX[0], "100", "Inicio", WHITE, S1 + 0.5), (BX[1], "120", "+20%", YEL, S2 + 1.3),
                                (BX[2], "96", "−20%", YEL, S3 + 3.2)]:
        k = pop(t, st, 0.4)
        h = {"100": 100, "120": 120, "96": 96}[val]
        text(ctx, val, x, BASE - h * UNIT - 55, 70, WHITE, scale=k, alpha=al * clamp(k), outline=NAVY, ow=10)
        text(ctx, lab, x, BASE + 60, 46, lc, alpha=al * clamp(k))
    # comparación final
    p = ease_out(prog(t, S4, S4 + 0.8))
    if p > 0:
        ctx.save(); ctx.set_dash([18, 14]); ctx.set_line_width(5)
        ctx.move_to(BX[0] - BW / 2, BASE - 100 * UNIT); ctx.line_to(BX[0] - BW / 2 + (BX[2] + BW / 2 - BX[0] + BW / 2) * p, BASE - 100 * UNIT)
        ctx.set_source_rgba(*hexc(YEL, al)); ctx.stroke(); ctx.restore()
        k = pop(t, S4 + 0.8, 0.5)
        ctx.save(); ctx.translate(BX[2] + BW / 2 + 10, BASE - 98 * UNIT); sc(ctx, k)
        rrect(ctx, -20, -36, 110, 72, 36); ctx.set_source_rgba(*hexc(RED, al)); ctx.fill()
        text(ctx, "−4", 35, 0, 46, WHITE, alpha=al); ctx.restore()

def scene_formula(ctx, t):
    a, b = T["formula"]
    if not (a <= t < b + 0.3): return
    al = fade(t, a, b + 0.2)
    k0 = pop(t, a + 0.1)
    bulb(ctx, W / 2, 400, 90 * k0, al)
    text(ctx, "El atajo", W / 2, 540, 84, WHITE, alpha=al, scale=k0, outline=NAVY, ow=14)
    k1 = ease_out(prog(t, a + 0.4, a + 0.8))
    yb = 660 + 60 * (1 - k1)
    card(ctx, 90, yb, 900, 860, 56, alpha=al * k1)
    for st, parts, y, size in [(0.8, [("Subir 20%:  ", GREEN), ("× 1,2", NAVY)], 130, 66),
                               (1.5, [("Bajar 20%:  ", RED), ("× 0,8", NAVY)], 240, 66)]:
        k = pop(t, a + st, 0.4)
        segs(ctx, parts, W / 2, yb + y, size, alpha=al * clamp(k), scale=k)
    k = pop(t, a + 2.4, 0.5)
    ctx.save(); ctx.translate(W / 2, yb + 450); sc(ctx, k)
    rrect(ctx, -380, -90, 760, 180, 40); ctx.set_source_rgba(*hexc("#EAF4FF", al)); ctx.fill()
    segs(ctx, [("1,2 × 0,8 = ", NAVY), ("0,96", PINK)], 0, 0, 84, alpha=al)
    ctx.restore()
    k = pop(t, a + 3.6, 0.5)
    segs(ctx, [("Queda el ", NAVY), ("96%", PINK), (" del original", NAVY)], W / 2, yb + 700, 60, alpha=al * clamp(k), scale=k)

def draw(ctx, t):
    scene_title(ctx, t, *T["title"])
    scene_problem(ctx, t, T, LINES, QUESTION, SUMMARY, flow, card_h=760, q_size=52)
    scene_think(ctx, t, *T["think"])
    scene_trap(ctx, t, *T["trap"], TRAP)
    a = T["trap"][0]
    pill(ctx, W / 2, 1520, "¡Probemos con 100!", 56, NAVY, WHITE, fade(t, a + 2.4, T["trap"][1] + 0.2), pop(t, a + 2.4))
    scene_solve(ctx, t)
    scene_formula(ctx, t)
    scene_answer(ctx, t, T["answer"][0], DUR, "96%", "del número original",
                 [("¿Y si ", NAVY), ("baja", RED), (" y luego ", NAVY), ("sube", GREEN), ("?", NAVY)],
                 big_size=200, note="No vuelve: pierde el 4%")

def events():
    a = T["problem"][0]
    ev = title_events() + [(a, "whoosh", 0)] + [(a + st, "pop", i) for i, (st, *_r) in enumerate(LINES)]
    ev += [(a + 1.0 + i * 0.8, "blip", i * 2) for i in range(3)] + [(a + QUESTION[0], "question", 0)]
    ev += think_events(T["think"][0]) + trap_events(T["trap"][0], TRAP) + [(T["trap"][0] + 2.4, "pop", 3)]
    ev += [(T["solve"][0], "whoosh", 0), (S1, "note", 0), (S1 + 0.5, "pop", 0), (S2 + 0.1, "note", 1),
           (S2 + 0.8, "note", 4), (S2 + 1.3, "pop", 1), (S3 + 0.1, "note", 2)]
    ev += [(S3 + 0.9 + i * 0.12, "blip", i) for i in range(5)]
    ev += [(S3 + 2.0, "wrong", 0), (S3 + 2.4, "whoosh", 0), (S3 + 3.2, "pop", 2), (S4, "whoosh", 0), (S4 + 0.8, "success", 0)]
    a = T["formula"][0]
    ev += [(a, "whoosh", 0), (a + 0.1, "pop", 0), (a + 0.8, "pop", 1), (a + 1.5, "pop", 2), (a + 2.4, "pop", 3), (a + 3.6, "success", 1)]
    return ev + answer_events(T["answer"][0])

if __name__ == "__main__":
    run("reto_porcentaje", DUR, draw, events(), transpose=0, breaks=[T["think"]])
