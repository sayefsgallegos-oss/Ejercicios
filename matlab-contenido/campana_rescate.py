"""Campaña estática 'Misión Rescate' (fin de año): 3 posts 1080x1350 + 1 historia 1080x1920."""
import io, math, os
import cairo
import qrcode
from render import hexc, rrect, NAVY, YEL, GREEN, RED, WHITE, BLUE
from carrusel_errores import LOGO, setf, width, line, sparks, white_card, badge, soft_shadow
from robots import spr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "campana_rescate")
WA_LINK = "https://wa.link/r6bm5p"
PHONE = "920 000 506"
WEB, IG = "matlab.com.pe", "@matlab_peru"
R1, R2 = "#E5323B", "#F4603E"
WA = "#25D366"

def qr_surface(url):
    img = qrcode.make(url, border=1, box_size=12).convert("RGBA")
    buf = io.BytesIO(); img.save(buf, "PNG"); buf.seek(0)
    return cairo.ImageSurface.create_from_png(buf)
QR = qr_surface(WA_LINK)

def base(c, W, H, page=None, total=0):
    g = cairo.LinearGradient(0, 0, W, H); g.add_color_stop_rgb(0, *hexc(R1)[:3]); g.add_color_stop_rgb(1, *hexc(R2)[:3])
    c.set_source(g); c.paint()
    c.set_source_rgba(1, 1, 1, 0.09)
    c.arc(W + 60, H * 0.35, 330, 0, 2 * math.pi); c.fill()
    c.arc(-80, H * 0.78, 300, 0, 2 * math.pi); c.fill()
    c.set_line_width(2); c.set_source_rgba(1, 1, 1, 0.12)
    for x in range(60, W - 40, 54): c.move_to(x, 60); c.line_to(x, H - 60)
    for y in range(60, H - 40, 54): c.move_to(60, y); c.line_to(W - 60, y)
    c.stroke()
    c.save(); rrect(c, 80, -60, 200, 280, 50); c.translate(0, 8); c.set_source_rgba(0.4, 0.05, 0.05, 0.2); c.fill(); c.restore()
    rrect(c, 80, -60, 200, 270, 50); c.set_source_rgb(1, 1, 1); c.fill()
    s = 150 / LOGO.get_width()
    c.save(); c.translate(105, 50); c.scale(s, s); c.set_source_surface(LOGO); c.paint(); c.restore()
    if total:
        for i in range(total):
            c.arc(W / 2 + (i - (total - 1) / 2) * 26, H - 40, 7 if i == page else 5, 0, 2 * math.pi)
            c.set_source_rgba(1, 1, 1, 1 if i == page else 0.5); c.fill()

def put(c, name, cx, bottom, h, rot=0.0, shadow=True):
    # "v2:nombre" = poses nuevas generadas con IA (assets/robots_v2)
    s = cairo.ImageSurface.create_from_png(os.path.join(HERE, "assets", "robots_v2", name[3:] + ".png")) if name.startswith("v2:") else spr(name)
    k = h / s.get_height()
    if shadow: soft_shadow(c, cx, bottom - 6, s.get_width() * k * 0.36, 18, 0.35)
    c.save(); c.translate(cx, bottom); c.rotate(rot); c.scale(k, k); c.translate(-s.get_width() / 2, -s.get_height())
    c.set_source_surface(s); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()

def highlight(c, x, y, w, size, col=YEL):
    rrect(c, x - 18, y - size * 0.78, w + 36, size * 1.02, size * 0.3); c.set_source_rgba(*hexc(col)); c.fill()

def wa_icon(c, x, y, r):
    c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(*hexc(WA)); c.fill()
    c.save(); c.translate(x, y)
    c.arc(0, -r * 0.05, r * 0.55, 0, 2 * math.pi); c.set_source_rgb(1, 1, 1); c.fill()
    c.move_to(-r * 0.45, r * 0.25); c.line_to(-r * 0.6, r * 0.62); c.line_to(-r * 0.15, r * 0.45); c.fill()
    c.arc(0, -r * 0.05, r * 0.38, 0, 2 * math.pi); c.set_source_rgba(*hexc(WA)); c.fill()
    c.restore()

def qr_block(c, x, y, size):
    rrect(c, x - 14, y - 14, size + 28, size + 28, 22); c.set_source_rgb(1, 1, 1); c.fill()
    k = size / QR.get_width()
    c.save(); c.translate(x, y); c.scale(k, k); c.set_source_surface(QR); c.get_source().set_filter(cairo.FILTER_NEAREST); c.paint(); c.restore()

def cta_bar(c, W, y, h=210):
    rrect(c, 90, y + 10, W - 180, h, 44); c.set_source_rgba(0.35, 0.03, 0.03, 0.25); c.fill()
    rrect(c, 90, y, W - 180, h, 44); c.set_source_rgba(*hexc(YEL)); c.fill()
    wa_icon(c, 170, y + h / 2, 46)
    line(c, [("Escríbenos ahora", "semi", NAVY)], 240, y + h / 2 - 18, 40, align="l", shadow=False)
    line(c, [(PHONE, "xbold", NAVY)], 240, y + h / 2 + 44, 62, align="l", shadow=False)
    qr_block(c, W - 90 - h + 22, y + 22, h - 44)

# ---------- libreta ----------
def libreta(c, cx, cy):
    c.save(); c.translate(cx, cy); c.rotate(-0.05)
    w, h = 620, 600
    soft_shadow(c, 0, h / 2 + 10, w * 0.45, 30, 0.4)
    rrect(c, -w / 2, -h / 2, w, h, 30); c.set_source_rgb(1, 1, 1); c.fill()
    rrect(c, -w / 2, -h / 2, w, 120, 30); c.set_source_rgba(*hexc(BLUE)); c.fill()
    c.rectangle(-w / 2, -h / 2 + 90, w, 30); c.fill()
    line(c, [("LIBRETA DE NOTAS", "bold", WHITE)], 0, -h / 2 + 62, 40, shadow=False)
    line(c, [("IV bimestre", "reg", "#D6E6FF")], 0, -h / 2 + 102, 26, shadow=False)
    rows = [("Comunicación", "15"), ("Ciencia y Tec.", "14"), ("Matemática", "09"), ("Inglés", "16"), ("Arte", "17")]
    for i, (curso, nota) in enumerate(rows):
        y = -h / 2 + 185 + i * 84
        bad = nota == "09"
        if i: c.move_to(-w / 2 + 40, y - 52); c.line_to(w / 2 - 40, y - 52); c.set_source_rgba(0.8, 0.85, 0.92, 1); c.set_line_width(2); c.stroke()
        line(c, [(curso, "semi" if not bad else "bold", NAVY)], -w / 2 + 50, y, 38, align="l", shadow=False)
        line(c, [(nota, "xbold", "#1F5FD0" if not bad else RED)], w / 2 - 90, y, 50, shadow=False)
        if bad:
            c.save(); c.translate(w / 2 - 92, y - 18); c.rotate(-0.15); c.scale(1.5, 1)
            c.arc(0, 0, 48, 0.2, 2 * math.pi + 0.5); c.restore()
            c.set_line_width(7); c.set_source_rgba(*hexc(RED)); c.stroke()
    c.restore()

# ---------- piezas ----------
def p1_gancho(c, W, H):
    base(c, W, H, 0, 3)
    line(c, [("¿Tu hijo va a", "light", WHITE)], W / 2, 330, 84)
    wj = width(c, [("jalar", "xbold", NAVY)], 84); wm = width(c, [(" matemática?", "bold", WHITE)], 78)
    x0 = W / 2 - (wj + wm) / 2 + 9
    highlight(c, x0, 450, wj, 84)
    line(c, [("jalar", "xbold", NAVY)], x0, 450, 84, align="l", shadow=False)
    line(c, [(" matemática?", "bold", WHITE)], x0 + wj + 12, 450, 78, align="l")
    libreta(c, W / 2 - 60, 850)
    put(c, "v2:numi_d00", W - 190, 1190, 360, 0.06)
    rrect(c, 90, 1180, W - 180, 110, 55); c.set_source_rgba(*hexc(NAVY, 0.92)); c.fill()
    line(c, [("Los exámenes finales ", "reg", WHITE), ("ya llegan", "bold", YEL)], W / 2, 1220, 38, shadow=False)
    line(c, [("Desliza y conoce la solución  »", "semi", "#BFD6FF")], W / 2, 1268, 30, shadow=False)

def p2_solucion(c, W, H):
    base(c, W, H, 1, 3)
    line(c, [("Activamos la", "light", WHITE)], W / 2, 300, 78)
    line(c, [("MISIÓN RESCATE", "xbold", YEL)], W / 2, 410, 100)
    white_card(c, 90, 480, W - 180, 560, 44)
    items = [[("Clases ", "reg", NAVY), ("1 a 1", "bold", RED), (" por videollamada", "reg", NAVY)],
             [("Horarios ", "bold", RED), ("a tu medida", "reg", NAVY)],
             [("Reforzamos ", "reg", NAVY), ("el tema exacto", "bold", RED)],
             [("que le está costando", "reg", NAVY)],
             [("Tareas y exámenes", "bold", RED)],
             [("con acompañamiento", "reg", NAVY)]]
    y = 580
    for i, it in enumerate(items):
        cont = i in (3, 5)
        if not cont: badge(c, 170, y - 14, True, 26)
        line(c, it, 220, y, 38, align="l", shadow=False)
        y += 52 if i in (2, 4) else 88
    put(c, "b02", W - 200, 1045, 270)
    cta_bar(c, W, 1080)

def p3_pasos(c, W, H):
    base(c, W, H, 2, 3)
    line(c, [("¿Cómo funciona la", "light", WHITE)], W / 2, 300, 72)
    line(c, [("Misión Rescate?", "bold", WHITE)], W / 2, 395, 84)
    steps = [("Diagnóstico", "vemos qué tema le falta"), ("Plan a medida", "según su colegio y su examen"),
             ("Clases 1 a 1", "por videollamada, en tu horario"), ("¡A rendir tranquilo!", "llega preparado al examen")]
    for i, (a, b) in enumerate(steps):
        y = 520 + i * 150
        white_card(c, 130, y - 60, W - 380, 120, 60)
        c.arc(200, y, 44, 0, 2 * math.pi); c.set_source_rgba(*hexc(YEL if i < 3 else GREEN)); c.fill()
        line(c, [(str(i + 1), "xbold", NAVY)], 200, y + 18, 50, shadow=False)
        line(c, [(a, "bold", NAVY)], 265, y - 6, 40, align="l", shadow=False)
        line(c, [(b, "reg", "#5A6E8C")], 265, y + 36, 28, align="l", shadow=False)
    put(c, "d04", W - 135, 1000, 260, 0.04, shadow=False)
    cta_bar(c, W, 1100, 190)

def story(c, W, H):
    base(c, W, H)
    line(c, [("Activamos la", "light", WHITE)], W / 2, 400, 80)
    line(c, [("MISIÓN", "xbold", YEL)], W / 2, 540, 150)
    line(c, [("RESCATE", "xbold", YEL)], W / 2, 690, 150)
    put(c, "b02", W / 2 - 180, 1130, 380)
    put(c, "d16", W / 2 + 200, 1130, 330)
    for i, it in enumerate([[("Clases ", "reg", WHITE), ("1 a 1", "bold", YEL), (" remotas", "reg", WHITE)],
                            [("Horarios ", "reg", WHITE), ("a tu medida", "bold", YEL)]]):
        line(c, it, W / 2, 1220 + i * 70, 48)
    qr_block(c, W / 2 - 160, 1360, 320)
    line(c, [("Escanea y escríbenos", "bold", WHITE)], W / 2, 1760, 48)
    line(c, [(f"{PHONE}  ·  {IG}", "semi", "#FFE1D6")], W / 2, 1830, 36)

PIECES = [("1_gancho", p1_gancho, 1080, 1350), ("2_solucion", p2_solucion, 1080, 1350),
          ("3_como_funciona", p3_pasos, 1080, 1350), ("4_historia", story, 1080, 1920)]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn, W, H in PIECES:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
        fn(c, W, H); s.write_to_png(f"{OUT}/rescate_{name}.png")
    print("listo", OUT)
