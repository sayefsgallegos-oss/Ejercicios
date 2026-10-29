"""Matti y Numi: La señal perdida — Capítulo 3: La torre del Señor Cero.
Clave 7 × 8 − 6 × 9 = 2, rescate de Numi, 'no se puede dividir entre cero', el 7 vuelve y el mapa al Barrio Fracciones."""
import random
from robots import *
import robots
import rr_novela_cap2 as cap2
from rr_novela_cap2 import put, floor_shadow, cage, tower_room, gray_zero, puff, big_card, BUILD, GROUND, mix
from mision import mission, answer_box, frac

DUR = 74.0
RECAP, ARRIVE, WIN, KEY, REUNION, CERO, PLAN, THROW, HIT, DIZZY, SEVEN, RECOVER, ROPE, MAP, CONT, ASK = (
    0.0, 6.8, 11.4, 16.4, 24.0, 28.6, 33.6, 36.4, 37.6, 40.6, 44.6, 49.6, 52.4, 56.0, 62.0, 64.6)
FLOOR = 1660
CAGE_X = 560
rng = random.Random(8)

DIALOG = [
    (7.0, 9.2, "matti", ["¡Numi!", "¡Vine a rescatarte!"]),
    (9.4, 11.2, "numi", ["¡Matti! ¡La clave!"]),
    (16.6, 18.6, "matti", ["Primero multiplico…"]),
    (20.2, 22.0, "matti", ["…y luego resto: ¡2!"]),
    (24.6, 26.8, "numi", ["¡Sabía que vendrías!"]),
    (27.0, 28.4, "matti", ["¡Equipo matLab!"]),
    (29.2, 32.6, "cero", ["¡Los convertiré a", "todos en cero!"]),
    (33.8, 36.2, "matti", ["Tranquila, Numi…", "tengo algo contra él."]),
    (38.0, 40.4, "cero", ["¿Cómo? ¡No puedo", "dividir a nadie!"]),
    (41.0, 44.2, "matti", ["¡Nadie puede dividir", "entre cero!"]),
    (45.4, 47.6, "siete", ["¡Volví a ser 7!"]),
    (47.8, 49.4, "equis", ["¡Lo lograron!"]),
    (50.0, 52.2, "cero", ["¡Esto no ha", "terminado!"]),
    (57.4, 60.8, "matti", ["Su próximo destino…", "¡el Barrio Fracciones!"]),
]
cast = Cast(DIALOG)


def actor(ctx, t, key, x, floor, h, alpha=1.0, who=None, fly=False, ph=0.0, flip=False, rot=0.0):
    hov = 12 * math.sin(t * 2.3 + ph) if fly else 0
    tk = cast.talking(who, t) if who else False
    sy = 1 + (0.035 * abs(math.sin(t * 14)) if tk else 0) + (0 if fly else 0.012 * math.sin(t * 3 + ph))
    floor_shadow(ctx, x, floor, h * 0.3, alpha)
    lift = 26 + hov if fly else 4
    put(ctx, key, x, floor - lift, h, alpha, rot, flip, 1 / sy ** 0.5, sy)
    return (x, floor - lift - h * 0.98)


def pick(sched, t):
    cur = sched[0][1]
    for st, k in sched:
        if t >= st: cur = k
    return cur


# ---------- anteriormente: el final del capítulo 2 en blanco y negro ----------
CLIPS = [(0.0, 2.2, 41.4), (2.2, 4.4, 55.0), (4.4, 6.2, 59.2)]   # (desde, hasta, segundo del cap. 2)

def scene_recap(ctx, t):
    if t >= ARRIVE: return
    t2 = None
    for a, b, src in CLIPS:
        if a <= t < b: t2 = src + (t - a)
    if t2 is None: t2 = 61.0
    cap2.draw(ctx, t2)
    ctx.set_operator(cairo.OPERATOR_HSL_SATURATION); ctx.set_source_rgb(0.5, 0.5, 0.5); ctx.paint()
    ctx.set_operator(cairo.OPERATOR_OVER)
    rg = cairo.RadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1150)
    rg.add_color_stop_rgba(0, 0, 0, 0, 0); rg.add_color_stop_rgba(1, 0, 0, 0, 0.75)
    ctx.set_source(rg); ctx.paint()
    r = random.Random(int(t * 24))
    for _ in range(500):
        ctx.rectangle(r.uniform(0, W), r.uniform(0, H), 3, 3)
    ctx.set_source_rgba(1, 1, 1, 0.12); ctx.fill()
    for a, b, src in CLIPS[1:]:   # corte con destello
        f = 1 - abs(t - a) / 0.12
        if f > 0: ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(1, 1, 1, 0.6 * f); ctx.fill()
    text(ctx, "Anteriormente…", W / 2, 300, 66, WHITE, "Nunito ExtraBold", alpha=ease_out(prog(t, 0.2, 0.6)), outline=NAVY, ow=10)
    if t >= 6.2:   # rebobinado
        p = prog(t, 6.2, ARRIVE)
        r = random.Random(int(t * 60))
        for _ in range(14):
            y = r.uniform(0, H); ctx.rectangle(0, y, W, r.uniform(4, 30))
            ctx.set_source_rgba(1, 1, 1, 0.35); ctx.fill()
        for i in range(2):
            x = W / 2 - 60 + i * 80
            ctx.move_to(x + 40, 860); ctx.line_to(x - 30, 960); ctx.line_to(x + 40, 1060); ctx.close_path()
            ctx.set_source_rgba(1, 1, 1, 0.9 * (1 - p)); ctx.fill()


# ---------- tarjeta de la ganadora del capítulo 2 ----------
_WIN = None
def winner_card(ctx, t, st, en):
    global _WIN
    if _WIN is None: _WIN = cairo.ImageSurface.create_from_png(os.path.join(HERE, "assets", "ganador_cap2.png"))
    k = pop(t, st, 0.5) * (1 - prog(t, en - 0.25, en))
    if k <= 0.001: return
    iw = 880; ih = iw * _WIN.get_height() / _WIN.get_width()
    w, h = iw + 60, ih + 330
    ctx.save(); ctx.translate(W / 2, 760); sc(ctx, k)
    rrect(ctx, -w / 2, -h / 2 + 12, w, h, 44); ctx.set_source_rgba(0.02, 0.05, 0.2, 0.3); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, 44); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, 44); ctx.set_line_width(10); ctx.set_source_rgba(*hexc("#F2C230")); ctx.stroke()
    pill(ctx, 0, -h / 2, "PRIMERA EN ACERTAR", 40, "#F2C230", NAVY, 1, 1, padx=30, pady=14)
    segs(ctx, [("¡La primera lectora", NAVY)], 0, -h / 2 + 95, 58)
    segs(ctx, [("en resolverlo!", NAVY), ("  La clave era ", GREY), ("2", PINK)], 0, -h / 2 + 165, 46)
    y0 = -h / 2 + 220
    ctx.save(); rrect(ctx, -iw / 2, y0, iw, ih, 24); ctx.clip()
    ctx.translate(-iw / 2, y0); ctx.scale(iw / _WIN.get_width(), iw / _WIN.get_width())
    ctx.set_source_surface(_WIN); ctx.get_source().set_filter(cairo.FILTER_BEST); ctx.paint(); ctx.restore()
    rrect(ctx, -iw / 2, y0, iw, ih, 24); ctx.set_line_width(3); ctx.set_source_rgba(0.85, 0.88, 0.93, 1); ctx.stroke()
    ctx.restore()


# ---------- piezas dibujadas ----------
def padlock(ctx, x, y, k, open_=0.0, alpha=1.0):
    if k <= 0.001 or alpha <= 0: return
    ctx.save(); ctx.translate(x, y); sc(ctx, k)
    ctx.save(); ctx.translate(30 * open_, -60 * open_)
    ctx.arc(0, -70, 60, math.pi, 2 * math.pi); ctx.set_line_width(22); ctx.set_source_rgba(0.75, 0.6, 0.2, alpha); ctx.stroke()
    ctx.restore()
    rrect(ctx, -90, -70, 180, 150, 26); ctx.set_source_rgba(*hexc("#F2C230", alpha)); ctx.fill()
    ctx.arc(0, -10, 16, 0, 2 * math.pi); ctx.set_source_rgba(0.2, 0.15, 0.05, alpha); ctx.fill()
    ctx.rectangle(-7, -5, 14, 40); ctx.fill()
    ctx.restore()

def city3(ctx, t, restore):
    """Matemópolis recuperando su color: los edificios borrados vuelven a llenarse."""
    g = cairo.LinearGradient(0, 0, 0, GROUND)
    g.add_color_stop_rgb(0, 0.55 - 0.25 * restore, 0.62 - 0.05 * restore, 0.72 + 0.2 * restore)
    g.add_color_stop_rgb(1, 0.82, 0.85 + 0.05 * restore, 0.88 + 0.08 * restore)
    ctx.set_source(g); ctx.paint()
    ctx.arc(820, 420, 90, 0, 2 * math.pi); ctx.set_source_rgba(1, 0.95, 0.6, 0.35 + 0.5 * restore); ctx.fill()
    for x, gl, size, col, missing in BUILD:
        font(ctx, size, "Fredoka"); ext = ctx.text_extents(gl)
        tx = x - ext.x_advance / 2
        ctx.move_to(tx, GROUND); ctx.text_path(gl)
        fill = restore if missing else 1
        ctx.set_source_rgba(*mix(col, 0.6 * (1 - restore)), fill); ctx.fill_preserve()
        ctx.set_line_width(6); ctx.set_source_rgba(0.2, 0.22, 0.28, 0.6); ctx.stroke()
    ctx.rectangle(0, GROUND, W, H - GROUND); ctx.set_source_rgb(0.42, 0.44, 0.48); ctx.fill()
    ctx.rectangle(0, GROUND, W, 26); ctx.set_source_rgb(0.62, 0.64, 0.68); ctx.fill()

def rope(ctx, x, top, bottom, alpha=1.0):
    ctx.save(); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(x, top); ctx.line_to(x, bottom); ctx.set_line_width(14); ctx.set_source_rgba(0.55, 0.4, 0.22, alpha); ctx.stroke()
    ctx.set_dash([10, 14]); ctx.move_to(x, top); ctx.line_to(x, bottom); ctx.set_line_width(14)
    ctx.set_source_rgba(0.38, 0.26, 0.13, alpha); ctx.stroke(); ctx.restore()

def map_sheet(ctx, cx, cy, w, h, rot=0.0, alpha=1.0, detail=True, t=0.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot)
    rrect(ctx, -w / 2, -h / 2 + 10, w, h, 18); ctx.set_source_rgba(0, 0, 0, 0.25 * alpha); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, 18); ctx.set_source_rgba(0.96, 0.89, 0.72, alpha); ctx.fill_preserve()
    ctx.set_line_width(max(3, w * 0.008)); ctx.set_source_rgba(0.55, 0.4, 0.2, alpha); ctx.stroke()
    if detail:
        u = w / 900
        ctx.set_line_width(10 * u); ctx.set_source_rgba(0.75, 0.62, 0.42, alpha)
        for (x1, y1, x2, y2) in [(-380, 150, 380, 120), (-100, -280, -60, 300), (150, -250, 220, 280)]:
            ctx.move_to(x1 * u, y1 * u); ctx.line_to(x2 * u, y2 * u)
        ctx.stroke()
        # torre (origen)
        ctx.rectangle(-330 * u, 40 * u, 60 * u, 130 * u); ctx.set_source_rgba(0.15, 0.15, 0.2, alpha); ctx.fill()
        ctx.move_to(-345 * u, 45 * u); ctx.line_to(-300 * u, -20 * u); ctx.line_to(-255 * u, 45 * u); ctx.fill()
        text(ctx, "Torre", -300 * u, 210 * u, 34 * u, NAVY, alpha=alpha)
        # ruta punteada
        p = clamp((t - (MAP + 1.0)) / 1.6)
        pts = [(-300, 60), (-150, 30), (0, -60), (150, -110), (290, -170)]
        ctx.set_dash([18 * u, 14 * u]); ctx.set_line_width(9 * u); ctx.set_source_rgba(0.9, 0.2, 0.25, alpha)
        n = int(p * (len(pts) - 1) * 10)
        ctx.move_to(pts[0][0] * u, pts[0][1] * u)
        for i in range(1, n + 1):
            f = i / 10; j = int(f); fr = f - j
            if j + 1 >= len(pts): break
            x = pts[j][0] + (pts[j + 1][0] - pts[j][0]) * fr; y = pts[j][1] + (pts[j + 1][1] - pts[j][1]) * fr
            ctx.line_to(x * u, y * u)
        ctx.stroke(); ctx.set_dash([])
        # Barrio Fracciones: una pizza con una porción menos
        k = pop(t, MAP + 2.6, 0.5)
        if k > 0:
            ctx.save(); ctx.translate(290 * u, -230 * u); sc(ctx, k)
            r = 95 * u
            ctx.move_to(0, 0); ctx.arc(0, 0, r, -math.pi / 2 + math.pi / 2, -math.pi / 2 + 2 * math.pi); ctx.close_path()
            ctx.set_source_rgba(0.98, 0.75, 0.3, alpha); ctx.fill_preserve()
            ctx.set_line_width(8 * u); ctx.set_source_rgba(0.85, 0.45, 0.15, alpha); ctx.stroke()
            for i in range(1, 4):
                a = -math.pi / 2 + i * math.pi / 2
                ctx.move_to(0, 0); ctx.line_to(r * math.cos(a), r * math.sin(a))
            ctx.set_line_width(5 * u); ctx.stroke()
            ctx.restore()
            text(ctx, "Barrio Fracciones", 250 * u, -80 * u, 44 * u, RED, alpha=alpha * clamp(k))
    ctx.restore()

def glitch(ctx, t, a, b):
    if not (a <= t < b): return
    r = random.Random(int(t * 30))
    for _ in range(9):
        y = r.uniform(300, 1700); h = r.uniform(8, 50)
        ctx.rectangle(0, y, W, h)
        ctx.set_source_rgba(*(r.choice([(0.2, 1, 1), (1, 0.2, 0.8), (1, 1, 1)])), 0.35); ctx.fill()


# ---------- escenas ----------
def scene_tower(ctx, t):
    if not (ARRIVE <= t < SEVEN or RECOVER <= t < CONT): return
    tower_room(ctx, t)
    heads = {}
    caged = t < KEY + 5.8
    lift = 900 * ease_in_out(prog(t, KEY + 5.8, KEY + 7.0))
    # Numi
    if t < SEVEN:
        nk = pick([(0, "numi_c00"), (9.4, "numi_c01"), (11.2, "numi_c00"), (REUNION, "numi_c04"),
                   (CERO, "numi_c02"), (DIZZY, "numi_a00")], t)
        nx = CAGE_X if t < REUNION else CAGE_X - 80 * ease_out(prog(t, REUNION, REUNION + 0.6))
    else:
        nk = pick([(0, "numi_c02"), (MAP, "numi_a01")], t); nx = CAGE_X - 80
    heads["numi"] = actor(ctx, t, nk, nx, FLOOR, 400, 1, "numi", True, 1.3)
    if t < SEVEN and lift < 899:
        cage(ctx, CAGE_X, 1050 - lift, FLOOR - lift, 520, 1 - prog(t, KEY + 6.4, KEY + 7.0))
        op = ease_out(prog(t, KEY + 5.2, KEY + 5.6))
        padlock(ctx, CAGE_X + 200, 1560 - lift, 0.75, op, 1 - prog(t, KEY + 5.6, KEY + 6.2))
    # Matti
    if t < SEVEN:
        mk = pick([(0, "matti_acc00"), (9.4, "matti_emo01"), (KEY, "matti_prof04"), (REUNION, "matti_nov_b02"),
                   (CERO, "matti_emo00"), (PLAN, "matti_emo04"), (THROW, "matti_acc02"), (DIZZY, "matti_acc04")], t)
        mx = -260 + (230 + 260) * ease_out(prog(t, ARRIVE, ARRIVE + 0.8))
        if t >= REUNION: mx = 230 - 20 * ease_out(prog(t, REUNION, REUNION + 0.6))
    else:
        mk = pick([(0, "matti_emo00"), (MAP, "matti_nov_a02")], t); mx = 210
    heads["matti"] = actor(ctx, t, mk, mx, FLOOR, 400, 1, "matti", True)
    # Señor Cero
    if CERO <= t < SEVEN or RECOVER <= t < MAP:
        if t < SEVEN:
            ck = pick([(0, "carbon_cero_a02"), (29.2, "carbon_cero_a01"), (THROW, "carbon_cero_c00"), (DIZZY, "carbon_cero_c01")], t)
            cx = W + 260 - (W + 260 - 880) * ease_out(prog(t, CERO, CERO + 0.7))
            floor = FLOOR + 20; rot = 0.0
            shake = 10 * math.sin(t * 70) if HIT <= t < DIZZY else 0
            heads["cero"] = actor(ctx, t, ck, cx + shake, floor, 420, 1, "cero", ph=1.1, flip=True)
            if HIT <= t < DIZZY:   # imagen 'rota' por el error
                r = random.Random(int(t * 25))
                for dx, a in ((-22, 0.45), (22, 0.45)):
                    put(ctx, ck, cx + dx + r.uniform(-8, 8), floor - 4, 420, a, flip=True)
        else:
            climb = ease_in_out(prog(t, ROPE + 1.0, ROPE + 3.2))
            ck = "carbon_cero_a02" if t < ROPE + 0.8 else "carbon_cero_a00"
            cx = 880; floor = FLOOR + 20 - 1500 * climb
            if t >= ROPE:   # la cuerda cae desde arriba y él sube por ella
                drop = ease_out(prog(t, ROPE, ROPE + 0.6))
                rope(ctx, cx - 40, -20, -20 + (floor - 380 + 20) * drop)
            heads["cero"] = actor(ctx, t, ck, cx, floor, 420, 1, "cero", ph=1.1, flip=True)
    # el mapa cae
    if ROPE + 2.2 <= t < MAP:
        p = prog(t, ROPE + 2.2, MAP - 0.4)
        y = 400 + (FLOOR - 40 - 400) * ease_in_out(p)
        x = 820 - 180 * p + 40 * math.sin(p * 9)
        map_sheet(ctx, x, y, 180, 130, rot=0.6 * math.sin(p * 8) * (1 - p), detail=False)
    # el signo ÷ que lanza Matti
    if THROW <= t < HIT + 0.2:
        p = ease_in_out(prog(t, THROW + 0.2, HIT))
        x = 360 + (800 - 360) * p; y = 1300 - 260 * math.sin(math.pi * p)
        ctx.save(); ctx.translate(x, y); ctx.rotate(p * 12)
        text(ctx, "÷", 0, 0, 220, YEL, outline=NAVY, ow=16)
        ctx.restore()
    if HIT <= t < HIT + 0.3:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(1, 1, 1, 0.8 * (1 - prog(t, HIT, HIT + 0.3))); ctx.fill()
    glitch(ctx, t, HIT, DIZZY)
    if HIT + 0.3 <= t < DIZZY:
        k = pop(t, HIT + 0.3, 0.3)
        ctx.save(); ctx.translate(W / 2, 520); ctx.rotate(-0.06 + 0.04 * math.sin(t * 40)); sc(ctx, k)
        rrect(ctx, -330, -80, 660, 160, 30); ctx.set_source_rgba(*hexc(RED)); ctx.fill()
        text(ctx, "ERROR: ÷ 0", 0, 0, 92, WHITE)
        ctx.restore()
    if t < SEVEN:
        big_card(ctx, t, DIZZY + 0.3, SEVEN, [([("n", BLUE), (" ÷ ", NAVY), ("0", GREY), (" = ", NAVY), ("¡no existe!", PINK)], 96),
                                              ([("No se puede dividir entre cero", GREY)], 42)], y=560, w=900)
    if REUNION <= t < CERO:
        confetti(ctx, t, REUNION + 0.2, 430, 900)
    # la clave en el candado
    if KEY <= t < KEY + 6.0:
        a = fade(t, KEY, KEY + 6.0)
        for i, (st, parts) in enumerate([(1.0, [("7 × 8 = ", NAVY), ("56", BLUE)]), (2.4, [("6 × 9 = ", NAVY), ("54", BLUE)]),
                                         (3.8, [("56 − 54 = ", NAVY), ("2", PINK)])]):
            k = pop(t, KEY + st, 0.4)
            ctx.save(); ctx.translate(W / 2, 420 + i * 150); sc(ctx, k)
            rrect(ctx, -300, -60, 600, 120, 36); ctx.set_source_rgba(1, 1, 1, a); ctx.fill()
            segs(ctx, parts, 0, 0, 72, alpha=a)
            ctx.restore()
    if t < MAP: cast.bubbles(ctx, t, heads)

def scene_seven(ctx, t):
    if not (SEVEN <= t < RECOVER): return
    restore = ease_in_out(prog(t, SEVEN + 0.4, SEVEN + 2.0))
    city3(ctx, t, restore)
    heads = {}
    if t < SEVEN + 0.8:
        gray_zero(ctx, 640, FLOOR + 30, 330, 1)
    else:
        heads["siete"] = actor(ctx, t, "siete04", 640, FLOOR + 30, 400, 1, "siete", ph=2.1)
    puff(ctx, 640, FLOOR - 160, prog(t, SEVEN + 0.5, SEVEN + 1.3))
    heads["equis"] = actor(ctx, t, "equis04", 330, FLOOR + 20, 360, 1, "equis", ph=0.7)
    confetti(ctx, t, SEVEN + 0.9, W / 2, 900)
    cast.bubbles(ctx, t, heads)

def scene_map(ctx, t):
    if not (MAP <= t < CONT): return
    k = ease_out(prog(t, MAP, MAP + 0.6))
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0, 0, 0, 0.45 * k); ctx.fill()
    pill(ctx, W / 2, 380, "PRÓXIMO DESTINO", 50, RED, WHITE, k, pop(t, MAP + 0.3), padx=40, pady=18)
    map_sheet(ctx, W / 2, 880, 900 * (0.3 + 0.7 * k), 640 * (0.3 + 0.7 * k), rot=-0.04 * k, alpha=1, detail=k > 0.95, t=t)
    cast.bubbles(ctx, t, {"matti": (W / 2, 1420)})

def scene_end(ctx, t):
    if t < CONT: return
    d = ease_in_out(prog(t, CONT, CONT + 0.6))
    tower_room(ctx, t) if t < CONT + 0.6 else None
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.01, 0.02, 0.08, 0.85 * d + 0.15 * (t >= CONT + 0.6)); ctx.fill()
    if t < ASK + 0.3:
        a = 1 - prog(t, ASK - 0.2, ASK + 0.3)
        s = "Continuará…"; n = int((t - CONT - 0.4) * 10)
        text(ctx, s[:max(0, n)], W / 2, 860, 120, YEL, alpha=a, outline=NAVY, ow=14)
        pill(ctx, W / 2, 1040, "Capítulo 4:  Barrio Fracciones", 48, WHITE, NAVY, a, pop(t, CONT + 1.4), padx=34, pady=20)
    if t >= ASK:
        def eq(c, x, y, a):
            fs = 92
            cx = x - 230
            frac(c, cx, y, "1", "2", fs * 1.4, NAVY, a)
            text(c, "+", cx + 105, y, fs, NAVY, alpha=a)
            frac(c, cx + 210, y, "1", "4", fs * 1.4, NAVY, a)
            text(c, "=", cx + 320, y, fs, NAVY, alpha=a)
            answer_box(c, cx + 430, y, fs, t, a)
        mission(ctx, t, ASK, [[("Para activar la ruta al", WHITE)], [("Barrio Fracciones", YEL), (", resuelve:", WHITE)]],
                eq, hint="¼ es la mitad de ½")
        pill(ctx, W / 2, 1600, "Síguenos para ver el capítulo 4", 48, YEL, NAVY, 1, pop(t, ASK + 2.6) * (1 + 0.03 * math.sin(t * 6)), padx=40, pady=22)
        put(ctx, "matti_nov_a02", W / 2 - 230, 1900, 280, ease_out(prog(t, ASK + 0.5, ASK + 1.0)))
        put(ctx, "numi_a01", W / 2 + 240, 1900, 260, ease_out(prog(t, ASK + 0.6, ASK + 1.1)))

def draw(ctx, t):
    scene_recap(ctx, t)
    scene_tower(ctx, t)
    scene_seven(ctx, t)
    scene_map(ctx, t)
    scene_end(ctx, t)
    if t >= ARRIVE: logo(ctx, t, 0.9)
    if WIN <= t < KEY:
        winner_card(ctx, t, WIN, KEY)
    for at in (SEVEN, RECOVER):
        f = 1 - abs(t - at) / 0.3
        if f > 0: ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(1, 1, 1, f); ctx.fill()

def events():
    ev = [(0.2, "glitch", 0), (2.2, "flash", 0), (4.4, "flash", 0), (6.2, "rise", 0), (6.3, "glitch", 0)]
    ev += [(ARRIVE, "whoosh", 0), (WIN, "fanfare", 0), (WIN + 0.1, "pop", 0)]
    ev += [(KEY + 1.0, "pop", 0), (KEY + 2.4, "pop", 1), (KEY + 3.8, "success", 0), (KEY + 5.2, "unlock", 0), (KEY + 5.8, "whoosh", 0)]
    ev += [(REUNION, "fanfare", 0), (CERO, "boom", 0), (29.2, "boom", 1), (PLAN, "pop", 2)]
    ev += [(THROW + 0.2, "whoosh", 0), (HIT, "flash", 0), (HIT, "glitch", 0), (HIT + 0.3, "siren", 0), (DIZZY + 0.3, "pop", 3)]
    ev += [(SEVEN, "flash", 0), (SEVEN + 0.5, "pop", 1), (SEVEN + 0.9, "fanfare", 0)]
    ev += [(RECOVER, "flash", 0), (RECOVER + 0.4, "boom", 0), (ROPE, "whoosh", 0), (ROPE + 1.0, "rise", 0), (ROPE + 2.2, "whoosh", 0)]
    ev += [(MAP, "boom", 1), (MAP + 0.3, "pop", 0), (MAP + 2.6, "success", 0)]
    ev += [(CONT, "boom", 0), (CONT + 1.4, "pop", 1), (ASK, "whoosh", 0), (ASK + 1.0, "question", 0), (ASK + 2.6, "pop", 3)]
    return ev

if __name__ == "__main__":
    render("robots_novela_cap3", DUR, draw, events(), DIALOG, music="mystery",
           tension=[(CERO, SEVEN), (RECOVER, MAP)], mgain=0.6)
