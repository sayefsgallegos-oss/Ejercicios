"""Matti y Numi: La señal perdida — Capítulo 1. Un mensaje en clave (2, 4, 8, 16, ?) y Numi es abducido."""
from robots import *
import random
rng = random.Random(9)

DUR = 57.0
MX, NX, FLOOR = 280, 800, 1700
BEEP, MSG, BEAM, FLASH, CLUE, END, ASK = 11.0, 21.8, 30.4, 32.8, 37.4, 42.8, 47.6
DIALOG = [
    (5.8, 8.8, "numi", ["Matti… ya es tarde.", "¿Seguimos estudiando?"]),
    (9.0, 10.8, "matti", ["Un ejercicio más…"]),
    (12.0, 14.8, "numi", ["¡Matti! Llegó un", "mensaje en código."]),
    (15.0, 18.4, "matti", ["Es una secuencia:", "cada número es el doble."]),
    (18.6, 21.0, "numi", ["Entonces… 16 × 2…", "¡32!"]),
    (27.8, 30.2, "matti", ["¿Matemópolis?", "Eso no existe…"]),
    (30.8, 32.6, "numi", ["¿Qué es esa luz?"]),
    (33.0, 34.6, "numi", ["¡MATTI!"]),
    (35.2, 37.0, "matti", ["¡NUUUMI!"]),
    (39.2, 42.6, "matti", ["Dejó una pista…", "Te voy a encontrar, Numi."]),
]
cast = Cast(DIALOG)
MATTI = [(0, "b00"), (15.0, "b02"), (27.6, "a00"), (FLASH, "b03"), (38.6, "a00")]
NUMI = [(0, "c07"), (11.2, "c00"), (20.8, "c01"), (27.6, "c00")]
STARS = [(rng.uniform(40, W - 40), rng.uniform(260, 1100), rng.uniform(2, 5), rng.uniform(0, 6)) for _ in range(60)]
MESSAGE = ["Los números están", "desapareciendo de", "Matemópolis.", "Vengan pronto. Sigan la…"]

def pose_at(sched, t):
    cur = sched[0]
    for s in sched:
        if t >= s[0]: cur = s
    return cur[1], (1 + 0.08 * (1 - prog(t, cur[0], cur[0] + 0.25))) if cur[0] > 0 else 1

def night(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, 0.02, 0.04, 0.16, 0.82); g.add_color_stop_rgba(1, 0.03, 0.10, 0.30, 0.62)
    ctx.set_source(g); ctx.paint()
    for x, y, r, ph in STARS:
        ctx.arc(x, y, r * (0.7 + 0.3 * math.sin(t * 2 + ph)), 0, 2 * math.pi)
        ctx.set_source_rgba(1, 1, 1, 0.35 + 0.3 * math.sin(t * 1.7 + ph)); ctx.fill()
    rg = cairo.RadialGradient(W / 2, FLOOR, 50, W / 2, FLOOR, 700)
    rg.add_color_stop_rgba(0, 0.3, 0.6, 1, 0.22); rg.add_color_stop_rgba(1, 0.3, 0.6, 1, 0)
    ctx.set_source(rg); ctx.rectangle(0, FLOOR - 300, W, 600); ctx.fill()

def holo(ctx, t, cx, cy, w, h, alpha, tint=(0.25, 0.95, 1.0)):
    if alpha <= 0: return
    fl = 0.85 + 0.15 * math.sin(t * 40) * math.sin(t * 7)
    a = alpha * fl
    r, g, b = tint
    rrect(ctx, cx - w / 2, cy - h / 2, w, h, 30); ctx.set_source_rgba(r * 0.3, g * 0.5, b * 0.7, 0.35 * a); ctx.fill_preserve()
    ctx.set_line_width(5); ctx.set_source_rgba(r, g, b, 0.9 * a); ctx.stroke()
    ctx.save(); rrect(ctx, cx - w / 2, cy - h / 2, w, h, 30); ctx.clip()
    for yy in range(int(cy - h / 2), int(cy + h / 2), 8):
        ctx.rectangle(cx - w / 2, yy + (t * 40) % 8, w, 2)
    ctx.set_source_rgba(r, g, b, 0.08 * a); ctx.fill(); ctx.restore()
    # haz desde el proyector
    ctx.move_to(cx - 40, cy + h / 2 + 260); ctx.line_to(cx - w / 2 + 40, cy + h / 2); ctx.line_to(cx + w / 2 - 40, cy + h / 2); ctx.line_to(cx + 40, cy + h / 2 + 260)
    ctx.close_path(); ctx.set_source_rgba(r, g, b, 0.08 * a); ctx.fill()

def htext(ctx, s, x, y, size, alpha, color="#9FF6FF", align="c"):
    text(ctx, s, x, y, size, color, alpha=alpha, align=align)

def scene_holo(ctx, t):
    if not (BEEP <= t < MSG + 6.2): return
    on = ease_out(prog(t, BEEP, BEEP + 0.5)) * (1 - prog(t, MSG + 5.6, MSG + 6.0))
    glitch = MSG + 4.8 <= t < MSG + 6.0
    cx, cy, w, h = W / 2, 760, 860, 560
    jx = (rng.uniform(-14, 14) if glitch and int(t * 30) % 3 == 0 else 0)
    ok = t >= 20.8
    tint = (0.3, 1.0, 0.55) if ok and t < MSG else (0.25, 0.95, 1.0)
    if glitch and int(t * 20) % 2: tint = (1, 0.3, 0.45)
    holo(ctx, t, cx + jx, cy, w, h, on, tint)
    hc = "#B6FFCF" if ok and t < MSG else "#9FF6FF"
    if t < MSG:
        htext(ctx, "MENSAJE ENTRANTE" if not ok else "CLAVE CORRECTA", cx + jx, cy - 210, 46, on, hc)
        htext(ctx, "Introduce la clave:", cx + jx, cy - 120, 44, on * prog(t, 11.8, 12.2), hc)
        for i, s in enumerate(["2", "4", "8", "16", "?"]):
            k = pop(t, 12.0 + i * 0.15, 0.4)
            x = cx + jx + (i - 2) * 165
            if s == "?" and t >= 20.6:
                text(ctx, "32", x, cy + 20, 100, GREEN, alpha=on, scale=pop(t, 20.6, 0.5), outline=WHITE, ow=8)
            else:
                text(ctx, s, x, cy + 20, 100, "#FFFFFF" if s != "?" else YEL, alpha=on * clamp(k), scale=k)
        for i in range(4):
            p = ease_out(prog(t, 16.0 + i * 0.45, 16.3 + i * 0.45))
            if p <= 0: continue
            x1 = cx + jx + (i - 2) * 165 + 20; x2 = x1 + 125 * p
            ctx.move_to(x1, cy + 110); ctx.curve_to(x1 + 30, cy + 150, x2 - 30, cy + 150, x2, cy + 110)
            ctx.set_line_width(5); ctx.set_source_rgba(1, 0.8, 0.25, on * p); ctx.stroke()
            text(ctx, "×2", (x1 + x1 + 125) / 2, cy + 175, 40, YEL, alpha=on * p)
    else:
        htext(ctx, "MENSAJE", cx + jx, cy - 210, 46, on)
        n = int((t - MSG - 0.3) * 18)
        for i, line in enumerate(MESSAGE):
            htext(ctx, line[:max(0, n)], cx + jx, cy - 100 + i * 80, 56, on, "#FFFFFF")
            n -= len(line)

def beam(ctx, t, x):
    a = ease_out(prog(t, BEAM, BEAM + 1.2)) * (1 - prog(t, FLASH, FLASH + 0.2))
    if a <= 0: return
    g = cairo.LinearGradient(0, 0, 0, FLOOR)
    g.add_color_stop_rgba(0, 0.7, 1, 0.6, 0.0); g.add_color_stop_rgba(1, 0.7, 1, 0.6, 0.45 * a)
    ctx.move_to(x - 60, 0); ctx.line_to(x + 60, 0); ctx.line_to(x + 230, FLOOR); ctx.line_to(x - 230, FLOOR); ctx.close_path()
    ctx.set_source(g); ctx.fill()
    for i in range(14):
        yy = (t * 300 + i * 140) % FLOOR
        ctx.arc(x + 120 * math.sin(i * 7.1 + t), FLOOR - yy, 5, 0, 2 * math.pi); ctx.set_source_rgba(0.8, 1, 0.8, 0.6 * a); ctx.fill()

def draw(ctx, t):
    shake = (6 * math.sin(t * 47), 5 * math.cos(t * 53)) if BEAM + 0.6 <= t < FLASH + 1.2 else (0, 0)
    ctx.save(); ctx.translate(*shake)
    night(ctx, t)
    logo(ctx, t, 0.9)
    # portada
    if t < 4.9:
        out = 1 - ease_in_out(prog(t, 4.2, 4.8))
        text(ctx, "MATTI Y NUMI", W / 2, 640, 120, WHITE, alpha=out * ease_out(prog(t, 0.3, 1.0)), outline=NAVY, ow=18)
        text(ctx, "La señal perdida", W / 2, 790, 92, YEL, alpha=out * ease_out(prog(t, 1.0, 1.6)), outline=NAVY, ow=14)
        pill(ctx, W / 2, 930, "Capítulo 1", 52, "#22E3FF", NAVY, out, pop(t, 1.8))
    # rótulo de lugar
    if 4.6 <= t < 11.0:
        s = "Laboratorio matLab · 11:58 p. m."
        n = int((t - 4.8) * 22)
        text(ctx, s[:max(0, n)], W / 2, 340, 44, "#BFD6FF", "Nunito ExtraBold", alpha=fade(t, 4.6, 11.0))
    scene_holo(ctx, t)
    beam(ctx, t, NX)
    # robots
    ra = ease_out(prog(t, 4.6, 5.4))
    mp, ms = pose_at(MATTI, t); np_, ns = pose_at(NUMI, t)
    heads = {}
    if t < END + 4.8:
        heads["matti"] = robot(ctx, t, cast, "matti", mp, MX, FLOOR, 370, ra * (1 - prog(t, END + 4.2, END + 4.8)), ms)
    if t < FLASH:
        lift = 60 * ease_in_out(prog(t, BEAM + 0.8, FLASH))
        heads["numi"] = robot(ctx, t, cast, "numi", np_, NX, FLOOR - lift, 360, ra, ns, rot=0.06 * math.sin(t * 9) * prog(t, BEAM, FLASH), ph=1.3)
    else:
        up = ease_in_out(prog(t, FLASH + 0.8, FLASH + 3.0))
        bottom = FLOOR + 20 - 2400 * up
        sprite(ctx, "c03", NX - 20 + 30 * math.sin(t * 3), bottom, 640, 1, 0.05 * math.sin(t * 2.5))
        heads["numi"] = (NX - 90, bottom - 330)
    # pista
    if t >= CLUE:
        p = ease_out(prog(t, CLUE, CLUE + 1.2))
        y = -200 + (FLOOR - 120 + 200) * p
        a = 1 - prog(t, END + 4.2, END + 4.8)
        ctx.save(); ctx.translate(660, y); ctx.rotate(0.3 * (1 - p) + 0.05)
        for i in range(6, 0, -1):
            rrect(ctx, -150 - i * 6, -55 - i * 6, 300 + i * 12, 110 + i * 12, 30); ctx.set_source_rgba(0.3, 1, 0.6, 0.04 * a); ctx.fill()
        rrect(ctx, -150, -55, 300, 110, 26); ctx.set_source_rgba(0.08, 0.2, 0.25, 0.92 * a); ctx.fill_preserve()
        ctx.set_line_width(4); ctx.set_source_rgba(0.4, 1, 0.65, a); ctx.stroke()
        text(ctx, "1 · 4 · 9 · 16 · ?", 0, 0, 44, "#B6FFCF", alpha=a)
        ctx.restore()
    cast.bubbles(ctx, t, heads)
    # destello
    if FLASH <= t < FLASH + 0.8:
        ctx.rectangle(-20, -20, W + 40, H + 40); ctx.set_source_rgba(1, 1, 1, 1 - prog(t, FLASH, FLASH + 0.8)); ctx.fill()
    ctx.restore()
    # continuará
    if t >= END:
        d = ease_in_out(prog(t, END, END + 1.0)) * (1 - prog(t, ASK - 0.2, ASK + 0.4) * 0.6)
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.01, 0.02, 0.08, 0.75 * d); ctx.fill()
        if t < ASK + 0.3:
            s = "Continuará…"
            n = int((t - END - 1.0) * 10)
            a = 1 - prog(t, ASK - 0.2, ASK + 0.3)
            text(ctx, s[:max(0, n)], W / 2, 860, 120, YEL, alpha=a, outline=NAVY, ow=14)
            pill(ctx, W / 2, 1040, "Capítulo 2:  ¿Dónde está Numi?", 50, WHITE, NAVY, a, pop(t, END + 2.8), padx=36, pady=20)
    if t >= ASK:
        k = ease_out(prog(t, ASK, ASK + 0.5))
        card(ctx, 90, 420 + 60 * (1 - k), 900, 860, 56, alpha=k)
        y0 = 420 + 60 * (1 - k)
        text(ctx, "Ayuda a Matti", W / 2, y0 + 110, 76, BLUE, alpha=k)
        text(ctx, "¿Qué número sigue en la pista?", W / 2, y0 + 210, 46, NAVY, alpha=k)
        kk = pop(t, ASK + 0.6, 0.5)
        ctx.save(); ctx.translate(W / 2, y0 + 400); sc(ctx, kk)
        rrect(ctx, -390, -100, 780, 200, 40); ctx.set_source_rgba(*hexc("#0E2A3A", k)); ctx.fill()
        segs(ctx, [("1 · 4 · 9 · 16 · ", "#B6FFCF"), ("?", YEL)], 0, 0, 92, alpha=k)
        ctx.restore()
        text(ctx, "Comenta la clave", W / 2, y0 + 600, 54, PINK, alpha=k * ease_out(prog(t, ASK + 1.2, ASK + 1.6)))
        text(ctx, "y descubre dónde está Numi", W / 2, y0 + 675, 44, GREY, "Nunito ExtraBold", alpha=k * ease_out(prog(t, ASK + 1.4, ASK + 1.8)))
        pill(ctx, W / 2, 1420, "Síguenos para ver el capítulo 2", 48, YEL, NAVY, 1, pop(t, ASK + 2.2) * (1 + 0.03 * math.sin(t * 6)), padx=40, pady=22)
        sprite(ctx, "a00", W / 2, 1880, 300, k, 0.04 * math.sin(t * 2))

def events():
    ev = [(0.3, "boom", 0), (1.8, "pop", 0), (4.6, "whoosh", 0), (BEEP, "beep", 0), (BEEP + 0.1, "glitch", 0)]
    ev += [(12.0 + i * 0.15, "blip", i) for i in range(5)] + [(16.0 + i * 0.45, "note", i) for i in range(4)]
    ev += [(20.6, "success", 0), (20.9, "unlock", 0), (MSG, "beep", 0), (MSG + 4.8, "glitch", 0), (MSG + 5.3, "glitch", 0)]
    ev += [(BEAM, "hum", 0), (BEAM + 1.0, "rise", 0), (FLASH, "flash", 0), (FLASH + 0.8, "rise", 0)]
    ev += [(CLUE, "whoosh", 0), (CLUE + 1.2, "pop", 0), (END, "boom", 0), (END + 2.8, "pop", 1), (ASK, "whoosh", 0), (ASK + 0.6, "question", 0), (ASK + 2.2, "pop", 3)]
    return ev

if __name__ == "__main__":
    render("robots_novela_cap1", DUR, draw, events(), DIALOG, music="mystery", tension=[(BEAM, FLASH + 3.0)], mgain=0.6)
