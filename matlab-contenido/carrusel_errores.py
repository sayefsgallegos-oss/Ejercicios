"""Carrusel Instagram 1080x1350 'Errores comunes' en la línea gráfica de matLab, con ejemplos didácticos."""
import math, os
import cairo
from render import hexc, rrect, NAVY, YEL, PINK, GREEN, RED, WHITE

W, H = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "carrusel")
LIME = "#C8F25A"; BG1, BG2 = "#2E9BF0", "#5CC2FA"; DGREEN = "#3F7A2E"
LOGO = cairo.ImageSurface.create_from_png(os.path.join(HERE, "assets", "logo.png"))

# ---------- texto ----------
FAM = {"light": ("Poppins Light", False), "reg": ("Poppins", False), "semi": ("Poppins SemiBold", False),
       "bold": ("Poppins", True), "xbold": ("Poppins ExtraBold", False)}

def setf(c, w, size):
    fam, bold = FAM[w]
    c.select_font_face(fam, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)

def width(c, parts, size):
    tot = 0
    for s, w, col in parts:
        setf(c, w, size); tot += c.text_extents(s).x_advance
    return tot

def line(c, parts, x, y, size, align="c", shadow=True):
    """parts: [(texto, peso, color)]; y = línea base."""
    tw = width(c, parts, size)
    cx = x - tw / 2 if align == "c" else x
    for s, w, col in parts:
        setf(c, w, size)
        if shadow:
            c.move_to(cx, y + 4); c.text_path(s); c.set_source_rgba(0.05, 0.25, 0.55, 0.25); c.fill()
        c.move_to(cx, y); c.text_path(s); c.set_source_rgba(*hexc(col)); c.fill()
        cx += c.text_extents(s).x_advance
    return tw

def sparks(c, x, y, ang, col=YEL, n=3, r0=20, r1=58, lw=9):
    c.save(); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(lw); c.set_source_rgba(*hexc(col))
    for i in range(n):
        a = ang + (i - (n - 1) / 2) * 0.55
        c.move_to(x + r0 * math.cos(a), y + r0 * math.sin(a)); c.line_to(x + r1 * math.cos(a), y + r1 * math.sin(a))
    c.stroke(); c.restore()

# ---------- fondo y marca ----------
def base(c, page, total):
    g = cairo.LinearGradient(0, 0, W, H); g.add_color_stop_rgb(0, *hexc(BG1)[:3]); g.add_color_stop_rgb(1, *hexc(BG2)[:3])
    c.set_source(g); c.paint()
    # formas grandes de marca (suaves)
    c.set_source_rgba(1, 1, 1, 0.10)
    c.arc(130, 520, 330, 0, 2 * math.pi); c.fill()
    c.arc(160, 1100, 260, 0, 2 * math.pi); c.fill()
    c.arc(W + 40, 120, 220, 0, 2 * math.pi); c.fill()
    # cuadrícula
    c.set_line_width(2); c.set_source_rgba(1, 1, 1, 0.13)
    for x in range(60, W - 40, 54): c.move_to(x, 60); c.line_to(x, H - 60)
    for y in range(60, H - 40, 54): c.move_to(60, y); c.line_to(W - 60, y)
    c.stroke()
    # pestaña con logo
    c.save(); rrect(c, 80, -60, 200, 280, 50); c.set_source_rgba(0.1, 0.3, 0.6, 0.18); c.translate(0, 8); c.fill(); c.restore()
    rrect(c, 80, -60, 200, 270, 50); c.set_source_rgb(1, 1, 1); c.fill()
    s = 150 / LOGO.get_width()
    c.save(); c.translate(105, 50); c.scale(s, s); c.set_source_surface(LOGO); c.paint(); c.restore()
    # indicador de página
    for i in range(total):
        c.arc(W / 2 + (i - (total - 1) / 2) * 26, H - 40, 7 if i == page else 5, 0, 2 * math.pi)
        c.set_source_rgba(1, 1, 1, 1 if i == page else 0.5); c.fill()

def soft_shadow(c, x, y, rx, ry, a=0.22):
    for i in range(10):
        c.save(); c.translate(x, y); c.scale(rx * (1 + i * 0.06), ry * (1 + i * 0.06))
        c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(0.03, 0.2, 0.45, a / 10); c.fill()

def grad_v(y0, y1, top, bot):
    g = cairo.LinearGradient(0, y0, 0, y1); g.add_color_stop_rgb(0, *hexc(top)[:3]); g.add_color_stop_rgb(1, *hexc(bot)[:3])
    return g

def white_card(c, x, y, w, h, r=40):
    c.save(); rrect(c, x, y + 14, w, h, r); c.set_source_rgba(0.03, 0.2, 0.5, 0.18); c.fill(); c.restore()
    rrect(c, x, y, w, h, r); c.set_source_rgb(1, 1, 1); c.fill()

def badge(c, x, y, ok, r=34):
    c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(*hexc(GREEN if ok else RED)); c.fill()
    c.set_source_rgb(1, 1, 1); c.set_line_width(r * 0.22); c.set_line_cap(cairo.LINE_CAP_ROUND)
    if ok:
        c.move_to(x - r * 0.42, y); c.line_to(x - r * 0.1, y + r * 0.33); c.line_to(x + r * 0.45, y - r * 0.35)
    else:
        d = r * 0.36
        c.move_to(x - d, y - d); c.line_to(x + d, y + d); c.move_to(x + d, y - d); c.line_to(x - d, y + d)
    c.stroke()

# ---------- ilustraciones ----------
def icon_warning(c, cx, cy):
    soft_shadow(c, cx + 20, cy + 250, 260, 40)
    # triángulo rojo redondeado con volumen
    pts = [(cx - 40, cy - 250), (cx + 190, cy + 170), (cx - 270, cy + 170)]
    def tri(off, grow):
        c.new_path()
        (x1, y1), (x2, y2), (x3, y3) = [(px + (px - cx + 40) * grow, py + (py - cy) * grow + off) for px, py in pts]
        c.move_to(x1, y1); c.line_to(x2, y2); c.line_to(x3, y3); c.close_path()
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    tri(22, 0); c.set_line_width(70); c.set_source_rgba(*hexc("#A3121F")); c.stroke_preserve(); c.fill()
    tri(0, 0); c.set_line_width(70); g = grad_v(cy - 260, cy + 200, "#FF5A5F", "#D91E2A"); c.set_source(g); c.stroke_preserve(); c.fill()
    tri(0, -0.32); c.set_line_width(30); c.set_source(grad_v(cy - 150, cy + 150, "#FFFFFF", "#E6ECF2")); c.stroke_preserve(); c.fill()
    # lupa
    mx, my, R = cx + 30, cy + 20, 150
    c.arc(mx, my, R, 0, 2 * math.pi); g = cairo.RadialGradient(mx - 50, my - 60, 10, mx, my, R)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.75); g.add_color_stop_rgba(1, 0.75, 0.88, 1, 0.35); c.set_source(g); c.fill()
    # signo de exclamación (visto a través de la lupa)
    rrect(c, mx - 26, my - 110, 52, 140, 26); c.set_source_rgb(0.08, 0.1, 0.15); c.fill()
    c.arc(mx, my + 75, 28, 0, 2 * math.pi); c.fill()
    c.arc(mx, my, R, 0, 2 * math.pi); c.set_line_width(36); c.set_source(grad_v(my - R, my + R, "#4A4F5C", "#15171D")); c.stroke()
    c.arc(mx, my, R - 8, math.pi * 1.1, math.pi * 1.45); c.set_line_width(8); c.set_source_rgba(1, 1, 1, 0.5); c.stroke()
    c.save(); c.translate(mx + R * 0.72, my + R * 0.72); c.rotate(math.pi / 4)
    rrect(c, 0, -26, 60, 52, 10); c.set_source_rgb(0.12, 0.13, 0.17); c.fill()
    rrect(c, 50, -36, 190, 72, 36); c.set_source(grad_v(-36, 36, "#FF5A5F", "#C81623")); c.fill()
    rrect(c, 70, -26, 150, 16, 8); c.set_source_rgba(1, 1, 1, 0.35); c.fill()
    c.restore()

def key3d(c, x, y, s, sym):
    rrect(c, x - s / 2, y - s / 2 + 18, s, s, s * 0.22); c.set_source(grad_v(y, y + s, "#4E8A3A", "#2F5E22")); c.fill()
    rrect(c, x - s / 2, y - s / 2, s, s, s * 0.22); c.set_source(grad_v(y - s / 2, y + s / 2, "#7DB85E", "#4F8F3A")); c.fill()
    rrect(c, x - s * 0.38, y - s * 0.38, s * 0.76, s * 0.76, s * 0.16); c.set_source(grad_v(y - s / 2, y + s / 2, "#E3F2C6", "#BFDD98")); c.fill()
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(s * 0.12)
    for off, col in [(5, "#2F5E22"), (0, "#5C9A41")]:
        c.set_source_rgba(*hexc(col)); d = s * 0.2
        if sym in "+−×":
            c.save(); c.translate(x, y + off)
            if sym == "×": c.rotate(math.pi / 4)
            c.move_to(-d, 0); c.line_to(d, 0)
            if sym != "−": c.move_to(0, -d); c.line_to(0, d)
            c.stroke(); c.restore()
        else:
            c.move_to(x - d, y + off); c.line_to(x + d, y + off); c.stroke()
            for dy in (-d * 0.85, d * 0.85):
                c.arc(x, y + off + dy, s * 0.065, 0, 2 * math.pi); c.fill()

def icon_book(c, cx, cy):
    soft_shadow(c, cx, cy + 210, 200, 32)
    c.save(); c.translate(cx, cy); c.rotate(-0.06)
    rrect(c, -150, -190, 300, 380, 26); c.set_source(grad_v(-190, 190, "#3D7BEA", "#2251B8")); c.fill()
    rrect(c, -125, -165, 250, 330, 18); c.set_source_rgba(1, 1, 1, 0.12); c.fill()
    rrect(c, 120, -175, 26, 355, 10); c.set_source_rgb(0.96, 0.96, 0.98); c.fill()
    setf(c, "xbold", 210); e = c.text_extents("?"); c.move_to(-e.x_advance / 2, 75); c.text_path("?")
    c.set_source_rgb(1, 1, 1); c.fill()
    c.restore()
    for s, x, y, col, rot in [("1", cx - 230, cy - 130, YEL, -0.2), ("2", cx - 40, cy - 250, "#FF9BC3", 0.1),
                               ("+", cx + 130, cy - 240, "#7DDC4A", 0), ("5", cx + 240, cy - 170, "#FF6B5B", 0.2),
                               ("÷", cx - 250, cy + 60, WHITE, 0), ("8", cx + 250, cy + 40, "#FF9BC3", 0.15)]:
        c.save(); c.translate(x, y); c.rotate(rot); setf(c, "xbold", 90)
        e = c.text_extents(s); c.move_to(-e.x_advance / 2, 32); c.text_path(s)
        c.set_source_rgba(0.1, 0.3, 0.6, 0.25); c.save(); c.translate(0, 6); c.restore(); c.fill_preserve()
        c.set_source_rgba(*hexc(col)); c.fill(); c.restore()

# ---------- láminas ----------
def slide_cover(c):
    line(c, [("Errores comunes", "bold", WHITE)], W / 2, 370, 92)
    line(c, [("que vemos en", "light", WHITE)], W / 2, 480, 86)
    line(c, [("nuestros estudiantes", "light", WHITE)], W / 2, 590, 86)
    c.save(); c.translate(W / 2 + 20, 990); c.scale(0.72, 0.72); icon_warning(c, 0, 0); c.restore()
    line(c, [("Desliza ", "semi", WHITE), ("»", "bold", YEL)], W - 200, H - 100, 40)

def example(c, y, wrong, right, note):
    white_card(c, 110, y, 860, 330)
    for i, (txt, ok) in enumerate([(wrong, False), (right, True)]):
        yy = y + 95 + i * 115
        badge(c, 200, yy - 18, ok)
        line(c, [(txt, "bold", NAVY if ok else "#9AA7B8")], 260, yy, 62, align="l", shadow=False)
        if not ok:
            tw = width(c, [(txt, "bold", NAVY)], 62)
            c.move_to(255, yy - 20); c.line_to(265 + tw, yy - 20); c.set_line_width(7); c.set_source_rgba(*hexc(RED)); c.stroke()
    line(c, [(note, "semi", "#2E6FD6")], W / 2, y + 300, 34, shadow=False)

def slide_base(c):
    line(c, [("Falta de", "light", WHITE)], W / 2, 330, 80)
    line(c, [("base matemática", "bold", WHITE)], W / 2, 440, 90)
    for i, sym in enumerate("+−×÷"):
        key3d(c, W / 2 - 285 + i * 190, 610, 165, sym)
    line(c, [("Ejemplo típico:", "semi", YEL)], W / 2, 820, 44)
    example(c, 860, "−3² = 9", "−3² = −9", "El exponente afecta al 3, no al signo")

def slide_explain(c):
    line(c, [("Saben resolver un", "light", WHITE)], W / 2, 330, 76)
    line(c, [("problema pero", "light", WHITE)], W / 2, 430, 76)
    line(c, [("no explicarlo", "bold", WHITE)], W / 2, 545, 92)
    sparks(c, 135, 520, math.pi, YEL); sparks(c, W - 135, 520, 0, YEL)
    white_card(c, 110, 640, 860, 520)
    line(c, [("2x + 3 = 11", "bold", NAVY)], W / 2, 735, 64, shadow=False)
    line(c, [("Resultado:  ", "semi", "#7A8AA0"), ("x = 4", "bold", NAVY)], 200, 800, 50, align="l", shadow=False)
    badge(c, 860, 784, True, 30)
    # burbuja de pregunta
    c.save(); rrect(c, 190, 840, 700, 140, 70); c.set_source_rgba(*hexc("#EAF4FF")); c.fill()
    c.move_to(260, 970); c.line_to(240, 1020); c.line_to(320, 975); c.fill(); c.restore()
    line(c, [("“¿Y por qué es 4?”", "bold", "#2E6FD6")], W / 2 - 10, 930, 56, shadow=False)
    line(c, [("…", "bold", "#9AA7B8")], W / 2, 1055, 80, shadow=False)
    line(c, [("Entender el ", "reg", NAVY), ("porqué", "bold", PINK), (" es lo que se evalúa", "reg", NAVY)], W / 2, 1125, 38, shadow=False)

def slide_notion(c):
    line(c, [("No tienen", "light", WHITE)], W / 2, 320, 86)
    tw = line(c, [("noción", "bold", WHITE)], W / 2, 440, 104)
    rrect(c, W / 2 - tw / 2 - 30, 420, tw + 60, 40, 20); c.set_source_rgba(1, 1, 1, 0.25); c.fill()
    line(c, [("noción", "bold", WHITE)], W / 2, 440, 104, shadow=False)
    sparks(c, W / 2 - tw / 2 - 60, 400, math.pi, WHITE, lw=8); sparks(c, W / 2 + tw / 2 + 60, 400, 0, WHITE, lw=8)
    line(c, [("del tema a desarrollar", "light", WHITE)], W / 2, 540, 70)
    icon_book(c, W / 2, 870)
    rrect(c, 140, 1115, 800, 110, 55); c.set_source_rgba(*hexc(NAVY, 0.9)); c.fill()
    line(c, [("Memorizan pasos sin ", "reg", WHITE), ("entender la idea", "bold", YEL)], W / 2, 1185, 40, shadow=False)

def slide_offer(c):
    line(c, [("En matLab", "light", WHITE)], 140, 330, 96, align="l")
    line(c, [("obtienes:", "bold", WHITE)], 140, 445, 110, align="l")
    sparks(c, 720, 380, -0.3, LIME, lw=9)
    items = [[("Clases ", "reg", WHITE), ("personalizadas", "bold", LIME)],
             [("Clases ", "reg", WHITE), ("interactivas", "bold", LIME)],
             [("Acompañamiento", "bold", LIME), (" constante", "reg", WHITE)],
             [("Tecnología", "bold", LIME), (" que potencia", "reg", WHITE)],
             [("su aprendizaje", "reg", WHITE)],
             [("Seguimiento", "bold", LIME), (" diario", "reg", WHITE)]]
    y = 490
    for i, it in enumerate(items):
        cont = i == 4
        y += 62 if cont else 92
        if cont:
            line(c, it, 210, y, 44, align="l"); continue
        c.arc(165, y - 16, 24, 0, 2 * math.pi); c.set_source_rgb(1, 1, 1); c.fill()
        c.set_source_rgba(*hexc("#2E9BF0")); c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(154, y - 16); c.line_to(162, y - 7); c.line_to(177, y - 26); c.stroke()
        line(c, it, 210, y, 44, align="l")
    rrect(c, 140, 1070, 800, 150, 75); c.set_source_rgba(*hexc(YEL)); c.fill()
    line(c, [("Separa tu clase de prueba", "bold", NAVY)], W / 2, 1135, 46, shadow=False)
    line(c, [("WhatsApp: 999 999 999", "semi", NAVY)], W / 2, 1190, 36, shadow=False)

SLIDES = [slide_cover, slide_base, slide_explain, slide_notion, slide_offer]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate(SLIDES):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
        base(c, i, len(SLIDES)); fn(c)
        s.write_to_png(f"{OUT}/errores_{i + 1}.png")
    print("listo", OUT)
