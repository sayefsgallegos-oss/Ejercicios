"""Tarjeta de 'Misión para ti' al final de cada capítulo: panel tipo terminal que pide resolver la clave."""
from kit import *


def frac(ctx, x, y, num, den, size, color, alpha=1.0):
    """Fracción apilada centrada en (x, y). Devuelve su ancho."""
    s = size * 0.62
    w = max(text_w(ctx, num, s), text_w(ctx, den, s)) + size * 0.25
    text(ctx, num, x, y - size * 0.36, s, color, alpha=alpha)
    text(ctx, den, x, y + size * 0.40, s, color, alpha=alpha)
    rrect(ctx, x - w / 2, y - size * 0.05, w, size * 0.09, size * 0.04)
    ctx.set_source_rgba(*hexc(color, alpha)); ctx.fill()
    return w


def mission(ctx, t, st, lines, equation, hint=None, prize="¡Quien acierte primero sale en el próximo capítulo!"):
    """lines: instrucciones (lista de tramos para segs). equation: función (ctx, cx, cy, alpha) que dibuja la clave."""
    if t < st: return
    k = ease_out(prog(t, st, st + 0.5))
    x0, y0, w, h = 70, 380 + 60 * (1 - k), W - 140, 960
    # panel oscuro con borde que brilla
    for i in range(6, 0, -1):
        rrect(ctx, x0 - i * 4, y0 - i * 4, w + i * 8, h + i * 8, 50 + i * 4)
        ctx.set_source_rgba(0.25, 0.95, 1.0, 0.05 * k); ctx.fill()
    g = cairo.LinearGradient(0, y0, 0, y0 + h)
    g.add_color_stop_rgba(0, 0.04, 0.14, 0.22, 0.97 * k); g.add_color_stop_rgba(1, 0.03, 0.22, 0.30, 0.97 * k)
    rrect(ctx, x0, y0, w, h, 50); ctx.set_source(g); ctx.fill_preserve()
    ctx.set_line_width(6); ctx.set_source_rgba(0.35, 0.97, 1.0, k); ctx.stroke()
    ctx.save(); rrect(ctx, x0, y0, w, h, 50); ctx.clip()
    for yy in range(int(y0), int(y0 + h), 9):
        ctx.rectangle(x0, yy + (t * 30) % 9, w, 2)
    ctx.set_source_rgba(0.4, 1, 1, 0.05 * k); ctx.fill(); ctx.restore()
    pill(ctx, W / 2, y0, "MISIÓN PARA TI", 48, YEL, NAVY, k, pop(t, st + 0.2), padx=40, pady=18)
    # instrucciones
    for i, parts in enumerate(lines):
        kk = ease_out(prog(t, st + 0.4 + i * 0.25, st + 0.7 + i * 0.25))
        segs(ctx, parts, W / 2, y0 + 150 + i * 72, 54, alpha=k * kk)
    # caja de la clave
    ke = pop(t, st + 1.0, 0.5)
    cy = y0 + 150 + len(lines) * 72 + 170
    ctx.save(); ctx.translate(W / 2, cy); sc(ctx, ke)
    rrect(ctx, -440, -135, 880, 270, 44); ctx.set_source_rgba(1, 1, 1, k); ctx.fill()
    equation(ctx, 0, 0, k)
    ctx.restore()
    yy = cy + 230
    if hint:
        segs(ctx, [("Pista: ", YEL), (hint, "#BFF7FF")], W / 2, yy, 44, alpha=k * ease_out(prog(t, st + 1.6, st + 2.0)))
        yy += 90
    segs(ctx, [("Escribe tu respuesta en los ", WHITE), ("comentarios", PINK)], W / 2, yy, 44,
         alpha=k * ease_out(prog(t, st + 1.9, st + 2.3)))
    text(ctx, prize, W / 2, yy + 75, 34, YEL, "Nunito ExtraBold", alpha=k * ease_out(prog(t, st + 2.2, st + 2.6)))


def answer_box(ctx, x, y, size, t, alpha=1.0):
    """Recuadro '?' que late, como un campo por llenar."""
    b = 1 + 0.06 * math.sin(t * 6)
    s = size * 1.05
    ctx.save(); ctx.translate(x, y); ctx.scale(b, b)
    rrect(ctx, -s * 0.45, -s * 0.55, s * 0.9, s * 1.1, s * 0.18)
    ctx.set_source_rgba(*hexc(PINK, alpha)); ctx.fill()
    text(ctx, "?", 0, 0, size, WHITE, alpha=alpha)
    ctx.restore()
