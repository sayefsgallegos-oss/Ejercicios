"""Campañas estáticas de fin de año y verano:
- Misión Rescate en un solo flyer (feed 1080x1350 y A5 para imprenta en PDF con 3 mm de sangrado).
- Verano 2027: 2 posts 1080x1350 + 1 historia 1080x1920."""
import math, os
import cairo
from render import hexc, rrect, NAVY, YEL, GREEN, RED, WHITE, BLUE, ORANGE, PINK
from carrusel_errores import LOGO, width, line, sparks, white_card, badge, soft_shadow
from campana_rescate import base, put, highlight, cta_bar, qr_block, libreta, PHONE, WEB, IG

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "campana_verano")
SKY1, SKY2, SEA = "#1AA7EC", "#5ED3F3", "#0E86C9"


# ---------- Misión Rescate: flyer único ----------
def flyer_rescate(c, W, H):
    base(c, W, H)
    e = (H - 1350) / 4          # espacio extra cuando el formato es más alto (A5)
    line(c, [("¿Tu hijo va a", "light", WHITE)], W / 2, 300 + e * 0.3, 72)
    wj = width(c, [("jalar", "xbold", NAVY)], 76); wm = width(c, [(" matemática?", "bold", WHITE)], 70)
    x0 = W / 2 - (wj + wm) / 2 + 9
    highlight(c, x0, 395 + e * 0.3, wj, 76)
    line(c, [("jalar", "xbold", NAVY)], x0, 395 + e * 0.3, 76, align="l", shadow=False)
    line(c, [(" matemática?", "bold", WHITE)], x0 + wj + 12, 395 + e * 0.3, 70, align="l")
    y = 470 + e * 0.8
    white_card(c, 90, y, W - 180, 470, 44)
    line(c, [("Activamos la", "reg", NAVY)], W / 2 - 110, y + 70, 40, shadow=False)
    line(c, [("MISIÓN RESCATE", "xbold", RED)], W / 2 - 110, y + 135, 58, shadow=False)
    items = [[("Clases ", "reg", NAVY), ("1 a 1", "bold", RED)], [("por videollamada", "reg", NAVY)],
             [("Horarios ", "bold", RED), ("a tu medida", "reg", NAVY)],
             [("Reforzamos ", "reg", NAVY), ("el tema exacto", "bold", RED)],
             [("Tareas y exámenes", "bold", RED)]]
    yy = y + 215
    for i, it in enumerate(items):
        if i != 1: badge(c, 160, yy - 13, True, 22)
        line(c, it, 200, yy, 34, align="l", shadow=False)
        yy += 44 if i == 0 else 62
    put(c, "v2:numi_d00", W - 230, y + 455, 330, 0.05)
    put(c, "v2:matti_emo04", W - 140, y + 290, 230, -0.08, shadow=False)
    yb = 975 + e * 2.2
    rrect(c, 90, yb, W - 180, 86, 43); c.set_source_rgba(*hexc(NAVY, 0.92)); c.fill()
    line(c, [("Los exámenes finales ", "reg", WHITE), ("ya llegan", "bold", YEL)], W / 2, yb + 56, 36, shadow=False)
    cta_bar(c, W, 1078 + e * 3, 185)
    line(c, [(f"{WEB}  ·  {IG}", "semi", "#FFE1D6")], W / 2, H - 38, 30, shadow=False)


def flyer_pdf(path, fn, bleed_mm=3):
    """A5 (148 × 210 mm) con sangrado: el diseño se dibuja a 1080 de ancho y se escala al tamaño de imprenta."""
    mm = 72 / 25.4
    pw, ph = (148 + 2 * bleed_mm) * mm, (210 + 2 * bleed_mm) * mm
    W = 1080; H = round(W * ph / pw)
    surf = cairo.PDFSurface(path, pw, ph)
    c = cairo.Context(surf); c.scale(pw / W, ph / H)
    fn(c, W, H)
    surf.finish()
    return W, H


# ---------- Verano 2027 ----------
def base_verano(c, W, H):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hexc(SKY1)[:3]); g.add_color_stop_rgb(1, *hexc(SKY2)[:3])
    c.set_source(g); c.paint()
    c.set_line_width(2); c.set_source_rgba(1, 1, 1, 0.12)
    for x in range(60, W - 40, 54): c.move_to(x, 60); c.line_to(x, H - 60)
    for y in range(60, H - 40, 54): c.move_to(60, y); c.line_to(W - 60, y)
    c.stroke()
    c.save(); rrect(c, 80, -60, 200, 280, 50); c.translate(0, 8); c.set_source_rgba(0.02, 0.2, 0.4, 0.2); c.fill(); c.restore()
    rrect(c, 80, -60, 200, 270, 50); c.set_source_rgb(1, 1, 1); c.fill()
    s = 150 / LOGO.get_width()
    c.save(); c.translate(105, 50); c.scale(s, s); c.set_source_surface(LOGO); c.paint(); c.restore()

def sun(c, x, y, r):
    c.save(); c.translate(x, y); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(12):
        a = i * math.pi / 6
        c.move_to(math.cos(a) * r * 1.25, math.sin(a) * r * 1.25); c.line_to(math.cos(a) * r * 1.55, math.sin(a) * r * 1.55)
    c.set_line_width(r * 0.14); c.set_source_rgba(*hexc(YEL)); c.stroke()
    g = cairo.RadialGradient(-r * 0.3, -r * 0.3, r * 0.1, 0, 0, r)
    g.add_color_stop_rgb(0, 1, 0.93, 0.5); g.add_color_stop_rgb(1, 1, 0.75, 0.15)
    c.arc(0, 0, r, 0, 2 * math.pi); c.set_source(g); c.fill(); c.restore()

def waves(c, W, y, H):
    for i, (col, a) in enumerate([("#FFFFFF", 0.35), (SEA, 0.9), ("#0A6FA8", 1.0)]):
        yy = y + i * 45
        c.move_to(0, H)
        c.line_to(0, yy)
        for x in range(0, W + 40, 40):
            c.line_to(x, yy + 18 * math.sin(x / 70 + i * 1.7))
        c.line_to(W, H); c.close_path(); c.set_source_rgba(*hexc(col, a)); c.fill()

def palm_ball(c, x, y, r):
    """Pelota de playa simple."""
    cols = [RED, WHITE, YEL, WHITE, BLUE, WHITE]
    for i, col in enumerate(cols):
        c.move_to(x, y); c.arc(x, y, r, i * math.pi / 3, (i + 1) * math.pi / 3); c.close_path()
        c.set_source_rgba(*hexc(col)); c.fill()
    c.arc(x, y, r * 0.18, 0, 2 * math.pi); c.set_source_rgb(1, 1, 1); c.fill()

def v1_hero(c, W, H):
    base_verano(c, W, H)
    sun(c, W - 190, 210, 95)
    rrect(c, W / 2 - 170, 270, 340, 74, 37); c.set_source_rgba(*hexc(ORANGE)); c.fill()
    line(c, [("VERANO 2027", "xbold", WHITE)], W / 2, 323, 42, shadow=False)
    line(c, [("¡Este verano,", "light", WHITE)], W / 2, 450, 84)
    wj = width(c, [("sube de nivel!", "xbold", NAVY)], 92)
    highlight(c, W / 2 - wj / 2, 570, wj, 92)
    line(c, [("sube de nivel!", "xbold", NAVY)], W / 2, 570, 92, shadow=False)
    line(c, [("Clases 1 a 1 de matemática", "semi", WHITE)], W / 2, 660, 44)
    waves(c, W, 1010, H)
    palm_ball(c, 170, 960, 58)
    put(c, "v2:matti_acc04", W / 2 - 170, 1060, 400)
    put(c, "v2:numi_a00", W / 2 + 200, 1060, 380)
    cta_bar(c, W, 1110, 190)

def v2_beneficios(c, W, H):
    base_verano(c, W, H)
    sun(c, W - 150, 150, 60)
    line(c, [("Un verano que", "light", WHITE)], W / 2, 330, 80)
    line(c, [("sí rinde", "xbold", YEL)], W / 2, 440, 100)
    white_card(c, 90, 500, W - 180, 520, 44)
    items = [[("Refuerza ", "bold", BLUE), ("lo que más le costó", "reg", NAVY)],
             [("Adelanta ", "bold", BLUE), ("el próximo grado", "reg", NAVY)],
             [("Clases ", "reg", NAVY), ("1 a 1", "bold", BLUE), (" por videollamada", "reg", NAVY)],
             [("Horarios flexibles:", "bold", BLUE)],
             [("¡y tiempo para la playa!", "reg", NAVY)]]
    y = 590
    for i, it in enumerate(items):
        if i != 4: badge(c, 160, y - 13, True, 24)
        line(c, it, 200, y, 36, align="l", shadow=False)
        y += 52 if i == 3 else 96
    put(c, "v2:numi_a05", W - 190, 1015, 250, 0.04, shadow=False)
    cta_bar(c, W, 1090, 200)

def v3_historia(c, W, H):
    base_verano(c, W, H)
    sun(c, W - 200, 300, 110)
    rrect(c, W / 2 - 180, 420, 360, 80, 40); c.set_source_rgba(*hexc(ORANGE)); c.fill()
    line(c, [("VERANO 2027", "xbold", WHITE)], W / 2, 477, 46, shadow=False)
    line(c, [("¡Sube de nivel", "xbold", WHITE)], W / 2, 640, 96)
    line(c, [("en vacaciones!", "xbold", YEL)], W / 2, 750, 96)
    line(c, [("Clases 1 a 1 · horarios flexibles", "semi", WHITE)], W / 2, 840, 42)
    waves(c, W, 1250, H)
    put(c, "v2:matti_acc04", W / 2 - 190, 1290, 420)
    put(c, "v2:numi_a00", W / 2 + 200, 1290, 400)
    qr_block(c, W / 2 - 150, 1390, 300)
    line(c, [("Inscripciones abiertas", "bold", WHITE)], W / 2, 1780, 50)
    line(c, [(f"{PHONE}  ·  {IG}", "semi", "#E6FBFF")], W / 2, 1850, 36)


PIECES = [("rescate_flyer_unico", flyer_rescate, 1080, 1350), ("verano_1_hero", v1_hero, 1080, 1350),
          ("verano_2_beneficios", v2_beneficios, 1080, 1350), ("verano_3_historia", v3_historia, 1080, 1920)]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn, W, H in PIECES:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
        fn(c, W, H); s.write_to_png(f"{OUT}/{name}.png")
    flyer_pdf(f"{OUT}/rescate_flyer_A5_imprenta.pdf", flyer_rescate)
    print("listo", OUT)
