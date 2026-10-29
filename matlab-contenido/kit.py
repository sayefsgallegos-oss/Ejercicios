"""Kit reutilizable para retos matemáticos: logo real, escenas comunes, música pop y render.

Cada video (v_*.py) define su guion `T`, sus escenas propias y sus efectos, y llama a `run()`.
"""
import math, os, subprocess, sys, wave
import cairo
import numpy as np
from render import (W, H, FPS, OUT, hexc, NAVY, BLUE, SKY, YEL, PINK, GREEN, PURPLE, ORANGE, RED, WHITE, TEAL,
                    PEOPLE, clamp, prog, ease_out, ease_in_out, ease_back, pop, fade, font, text, text_w, rrect,
                    card, pill, person, check, bulb, make_background, draw_symbols, CONF)
from audio import SR, midi, env, tone, lowpass, noise, add, sfx

HERE = os.path.dirname(os.path.abspath(__file__))
GREY = "#5A6E8C"
_LOGO = None

def sc(ctx, k):
    k = max(k, 1e-3); ctx.scale(k, k)

def segs(ctx, parts, x, y, size, alpha=1.0, scale=1.0):
    """Línea centrada de tramos [(texto, color) o (texto, color, familia)]."""
    if alpha <= 0.001 or scale <= 0.001: return
    parts = [(p[0], p[1], p[2] if len(p) > 2 else "Fredoka") for p in parts]
    total = sum(text_w(ctx, s, size, f) for s, _, f in parts)
    ctx.save(); ctx.translate(x, y); sc(ctx, scale)
    cx = -total / 2
    for s, c, f in parts:
        cx += text(ctx, s, cx, 0, size, c, f, alpha=alpha, align="l")
    ctx.restore()

def arrow(ctx, x1, y1, x2, y2, color, width=10, alpha=1.0, head=26):
    ctx.save(); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(*hexc(color, alpha)); ctx.set_line_width(width)
    ctx.move_to(x1, y1); ctx.line_to(x2, y2); ctx.stroke()
    a = math.atan2(y2 - y1, x2 - x1)
    for s in (1, -1):
        ctx.move_to(x2, y2); ctx.line_to(x2 - head * math.cos(a + s * 0.5), y2 - head * math.sin(a + s * 0.5))
    ctx.stroke(); ctx.restore()

def strike(ctx, cx, cy, half, p, alpha=1.0):
    if p <= 0: return
    ctx.move_to(cx - half, cy + 5); ctx.line_to(cx - half + 2 * half * p, cy - 10)
    ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgba(*hexc(RED, alpha)); ctx.stroke()


# ---------- marca ----------
def logo(ctx, t, alpha=1.0):
    global _LOGO
    if _LOGO is None:
        _LOGO = cairo.ImageSurface.create_from_png(os.path.join(HERE, "assets", "logo.png"))
    s = 210 / _LOGO.get_width()
    ctx.save(); ctx.translate(W / 2, 150 + 6 * math.sin(t * 2.2)); ctx.rotate(0.03 * math.sin(t * 1.3))
    ctx.scale(s, s); ctx.translate(-_LOGO.get_width() / 2, -_LOGO.get_height() / 2)
    ctx.set_source_surface(_LOGO); ctx.paint_with_alpha(alpha); ctx.restore()


# ---------- escenas comunes ----------
def scene_title(ctx, t, a, b):
    if not (a <= t < b + 0.4): return
    out = 1 - ease_in_out(prog(t, b - 0.35, b + 0.2))
    y0 = 940 - 200 * (1 - out)
    pill(ctx, W / 2, y0 - 330, "RETO DEL DÍA", 44, YEL, NAVY, out, pop(t, a + 0.15), padx=40)
    wob = 1 + 0.025 * math.sin(t * 6)
    text(ctx, "MATH", W / 2, y0 - 110, 230, YEL, scale=pop(t, a + 0.45, 0.55) * wob, alpha=out, outline=NAVY, ow=34, rot=-0.06)
    text(ctx, "QUIZ", W / 2, y0 + 110, 230, YEL, scale=pop(t, a + 0.7, 0.55) * wob, alpha=out, outline=NAVY, ow=34, rot=-0.06)
    p = prog(t, a + 1.3, a + 1.8)
    text(ctx, "¿Podrás resolverlo?", W / 2, y0 + 340 + 30 * (1 - ease_out(p)), 72, WHITE, alpha=ease_out(p) * out)
    for i, (dx, dy, s) in enumerate([(-360, -250, 40), (370, -60, 30), (-330, 220, 26), (340, 260, 44)]):
        k = pop(t, a + 0.9 + i * 0.12) * out
        text(ctx, "✦", W / 2 + dx, y0 + dy, s * 2, WHITE, "DejaVu Sans", scale=k * (1 + 0.15 * math.sin(t * 5 + i)), alpha=out)

def scene_problem(ctx, t, T, lines, question, summary, visual=None, card_h=1040, q_size=62):
    """Tarjeta del enunciado. lines: [(t_rel, tramos, y_rel, tamaño)]. Al pensar se encoge a `summary`."""
    a = T["problem"][0]; end = T["trap"][1]
    if not (a <= t < end + 0.3): return
    enter = ease_out(prog(t, a, a + 0.55))
    leave = 1 - ease_in_out(prog(t, end - 0.3, end + 0.2))
    compact = ease_in_out(prog(t, T["think"][0], T["think"][0] + 0.6))
    ctx.save(); ctx.translate(0, 900 * (1 - enter) - 300 * (1 - leave))
    cw, ch = 900, card_h - (card_h - 480) * compact
    cx, cy = (W - cw) / 2, 330 - 40 * compact
    card(ctx, cx, cy, cw, ch, 56, alpha=leave)
    rrect(ctx, cx, cy, cw, 16, 8); ctx.set_source_rgba(*hexc(YEL, leave)); ctx.fill()
    if compact < 0.5:
        al = leave * (1 - compact * 2)
        for st, parts, yr, size in lines:
            k = pop(t, a + st, 0.4)
            segs(ctx, parts, W / 2, cy + yr, size, alpha=al * clamp(k), scale=k)
        if visual: visual(ctx, t, cx, cy, al)
        qt, qtext = question
        k = pop(t, a + qt, 0.5)
        wig = 0.04 * math.sin(t * 7) * prog(t, a + qt + 0.5, a + qt + 0.7)
        ctx.save(); ctx.translate(W / 2, cy + ch - 120); ctx.rotate(wig)
        pill(ctx, 0, 0, qtext, q_size, PINK, WHITE, al, k, padx=44, pady=26)
        ctx.restore()
    else:
        al = leave * (compact - 0.5) * 2
        for i, parts in enumerate(summary):
            segs(ctx, parts, W / 2, cy + 110 + i * 92, 58, alpha=al)
    ctx.restore()

def scene_think(ctx, t, a, b):
    if not (a <= t < b + 0.3): return
    al = fade(t, a + 0.3, b + 0.2)
    cx, cy, r = W / 2, 1200, 230
    pill(ctx, W / 2, 900, "Piensa tu respuesta…", 56, NAVY, WHITE, al, pop(t, a + 0.35))
    ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_source_rgba(1, 1, 1, 0.22 * al); ctx.fill()
    ctx.arc(cx, cy, r - 26, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(WHITE, al)); ctx.fill()
    t0 = a + 0.4
    left = clamp(1 - (t - t0) / 5.0)
    ctx.set_line_width(30); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    if left > 0:
        ctx.arc(cx, cy, r - 13, -math.pi / 2, -math.pi / 2 + 2 * math.pi * left)
        ctx.set_source_rgba(*hexc(YEL if left > 0.4 else ORANGE if left > 0.2 else RED, al)); ctx.stroke()
    n = max(1, math.ceil(5 - (t - t0) - 1e-6))
    beat = 1 - (t - t0) % 1
    text(ctx, str(n), cx, cy, 220, NAVY, alpha=al, scale=1 + 0.18 * ease_out(beat) ** 3)

def scene_trap(ctx, t, a, b, rows, title="¡Cuidado con la trampa!", eq_size=84):
    """rows: [(t_rel, ecuación, por qué)] — cada ecuación se tacha."""
    if not (a <= t < b + 0.3): return
    al = fade(t, a, b + 0.2)
    pill(ctx, W / 2, 900, title, 58, YEL, NAVY, al, pop(t, a + 0.1))
    for i, (st, eq, why) in enumerate(rows):
        st += a
        y = 1120 + i * 290
        k = pop(t, st, 0.45)
        card(ctx, 90, y - 95, 900, 230, 40, alpha=al * clamp(k))
        text(ctx, eq, W / 2, y - 15, eq_size, NAVY, alpha=al * clamp(k), scale=k)
        strike(ctx, W / 2, y - 15, text_w(ctx, eq, eq_size) / 2 + 30, ease_out(prog(t, st + 0.55, st + 0.8)), al)
        text(ctx, why, W / 2, y + 75, 42, RED, alpha=al * ease_out(prog(t, st + 0.75, st + 1.05)))

def caption(ctx, t, st, parts, y=470, size=52, alpha=1.0, end=None):
    k = ease_out(prog(t, st, st + 0.3))
    if end is not None: k *= 1 - prog(t, end - 0.2, end)
    segs(ctx, parts, W / 2, y + 20 * (1 - k), size, alpha=alpha * k)

def scene_answer(ctx, t, a, dur, big, unit, nxt, big_size=250, note=None):
    if t < a: return
    al = fade(t, a, dur + 1)
    k = pop(t, a + 0.15, 0.6)
    ctx.save(); ctx.translate(W / 2, 760); sc(ctx, k)
    for i in range(10, 0, -1):
        ctx.arc(0, 0, 250 + i * 9, 0, 2 * math.pi); ctx.set_source_rgba(1, 0.95, 0.6, 0.03 * al); ctx.fill()
    ctx.arc(0, 0, 250, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(WHITE, al)); ctx.fill()
    big_size = min(big_size, big_size * 420 / max(1, text_w(ctx, big, big_size)))
    text(ctx, big, 0, -20, big_size, PINK, alpha=al, scale=1 + 0.03 * math.sin(t * 5))
    text(ctx, unit, 0, 120, 44 if len(unit) > 12 else 52, NAVY, alpha=al)
    ctx.restore()
    pk = pop(t, a + 0.5)
    ctx.save(); ctx.translate(W / 2 + 200, 560); sc(ctx, pk)
    ctx.arc(0, 0, 70, 0, 2 * math.pi); ctx.set_source_rgba(*hexc(GREEN, al)); ctx.fill(); ctx.restore()
    check(ctx, W / 2 + 200, 560, 70 * pk, WHITE, prog(t, a + 0.6, a + 0.95))
    if note:
        text(ctx, note, W / 2, 1065, 40, WHITE, alpha=ease_out(prog(t, a + 0.9, a + 1.3)))
    tc = t - a - 0.15
    if 0 < tc < 4:
        for c in CONF:
            tt = tc - c["d"]
            if tt <= 0: continue
            x = W / 2 + math.cos(c["a"]) * c["v"] * tt * 0.9
            y = 760 + math.sin(c["a"]) * c["v"] * tt * 0.9 + 900 * tt * tt
            ctx.save(); ctx.translate(x, y); ctx.rotate(c["rs"] * tt)
            ctx.rectangle(-c["w"] / 2, -c["w"] / 4, c["w"], c["w"] / 2)
            ctx.set_source_rgba(*hexc(c["c"], clamp(1.4 - tt / 3))); ctx.fill(); ctx.restore()
    k2 = ease_out(prog(t, a + 1.6, a + 2.1))
    yb = 1180 + 80 * (1 - k2)
    card(ctx, 90, yb, 900, 330, 50, alpha=k2)
    text(ctx, "Próximo reto:", W / 2, yb + 90, 50, BLUE, alpha=k2)
    segs(ctx, nxt, W / 2, yb + 180, 60, alpha=k2)
    text(ctx, "Déjalo en los comentarios", W / 2, yb + 262, 40, GREY, "Nunito ExtraBold", alpha=k2)
    k3 = pop(t, a + 2.6)
    pill(ctx, W / 2, 1640, "Síguenos para más retos", 50, YEL, NAVY, 1, k3 * (1 + 0.03 * math.sin(t * 6)), padx=44, pady=24)

def title_events(a=0.0):
    return [(a + 0.15, "pop", 0), (a + 0.45, "boom", 0), (a + 0.7, "boom", 1), (a + 1.3, "whoosh", 0)]

def think_events(a):
    return [(a + 0.4 + i, "tick", i) for i in range(5)]

def trap_events(a, rows):
    ev = [(a + 0.1, "pop", 0)]
    for i, (st, *_r) in enumerate(rows):
        ev += [(a + st, "pop", i + 1), (a + st + 0.6, "wrong", 0)]
    return ev

def answer_events(a):
    return [(a, "whoosh", 0), (a + 0.15, "fanfare", 0), (a + 0.6, "pop", 2), (a + 2.6, "pop", 3)]


# ---------- música pop (original, sin derechos de terceros) ----------
def _pluck(f, dur, bright=8, decay=0.25, cutoff=None):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for k in range(1, bright + 1):
        if f * k > 12000: break
        s += np.sin(2 * np.pi * f * k * t + k) / k * np.exp(-t * (3 + k * 1.2) / decay)
    s *= env(n, 0.003, dur, 1.0)
    return lowpass(s, cutoff) if cutoff else s

def music_pop(dur, transpose=0, bpm=120, breaks=()):
    """Pista pop tipo 'TikTok': Am–F–C–G, bombo, palmas, hi-hats en semicorcheas,
    bajo sincopado, acordes con efecto 'pump' y un gancho melódico pegajoso."""
    beat = 60 / bpm; bar = 4 * beat
    n = int(dur * SR) + SR
    drums, bass, chords, lead = (np.zeros(n) for _ in range(4))
    tr = transpose
    prog_ = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]
    hook = [76, None, 74, 76, None, 79, 76, None, 74, None, 72, 74, None, 72, 69, None]   # 2 compases, corcheas
    hook2 = [76, None, 74, 76, None, 79, 81, None, 79, None, 76, 74, None, 72, 74, None]
    rng = np.random.default_rng(11)
    kick = None
    for b in range(int(dur / bar) + 1):
        t0 = b * bar
        in_break = any(x <= t0 + 0.01 < y for x, y in breaks)
        root, ch = prog_[b % 4]
        # batería
        if not in_break:
            for k in range(4):
                nk = int(0.3 * SR); tt = np.arange(nk) / SR
                kick = np.sin(2 * np.pi * np.cumsum(48 + 110 * np.exp(-tt * 28)) / SR) * env(nk, 0.001, 0.3, 5)
                add(drums, kick * 0.55, t0 + k * beat)
                if k in (1, 3):
                    cl = noise(0.18); cl = cl - lowpass(cl, 900)
                    e = env(len(cl), 0.001, 0.18, 7)
                    add(drums, cl * e * 0.30, t0 + k * beat)
                    add(drums, cl * e * 0.18, t0 + k * beat + 0.012)
            for k in range(16):
                hh = noise(0.05); hh = hh - lowpass(hh, 7000)
                vel = 0.10 if k % 4 == 2 else 0.05 + 0.02 * rng.random()
                add(drums, hh * env(len(hh), 0.001, 0.05, 8) * vel, t0 + k * beat / 4)
        # bajo sincopado
        for k, d in [(0, 0.7), (1.5, 0.4), (2, 0.4), (2.75, 0.3), (3.5, 0.4)]:
            add(bass, tone(midi(root - 12 + tr), beat * d, (1, 0.6, 0.25), a=0.005, d=beat * d, curve=2.5) * (0.20 if in_break else 0.30), t0 + k * beat)
        # acordes: stabs a contratiempo
        for k in range(4):
            for nn in ch:
                add(chords, _pluck(midi(nn + tr), beat * 0.45, 6, 0.25, 5000) * 0.07, t0 + k * beat + beat / 2)
        # gancho
        if b >= 2 and not in_break:
            mel = (hook if (b // 2) % 2 == 0 else hook2)[(b % 2) * 8:(b % 2) * 8 + 8]
            for k, nn in enumerate(mel):
                if nn is None: continue
                add(lead, _pluck(midi(nn + tr), beat * 0.6, 8, 0.4, 6500) * 0.11, t0 + k * beat / 2)
                add(lead, _pluck(midi(nn + tr + 12), beat * 0.4, 3, 0.3) * 0.025, t0 + k * beat / 2)
    # efecto 'pump' (sidechain) en acordes y melodía
    t = np.arange(n) / SR
    ph = (t % beat) / beat
    pump = 0.45 + 0.55 * np.clip(ph / 0.35, 0, 1) ** 0.7
    mix = drums + bass + (chords + lead) * pump
    return mix[: int(dur * SR)]

def build_audio(path, dur, events, transpose=0, breaks=()):
    n = int(dur * SR)
    mus = music_pop(dur, transpose, breaks=breaks)
    t = np.arange(n) / SR
    fade_ = np.clip(t / 0.6, 0, 1) * np.clip((dur - t) / 1.5, 0, 1)
    fx = np.zeros(n + 3 * SR)
    for tm, kind, p in events:
        add(fx, sfx(kind, p), tm)
    mix = mus * fade_ * 0.55 + fx[:n]
    mix = np.tanh(mix * 1.4) / np.tanh(1.4)
    mix *= 0.89 / max(1e-6, np.abs(mix).max())
    pcm = (mix * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.stack([pcm, pcm], 1).tobytes())


# ---------- render ----------
def run(name, dur, draw, events, transpose=0, breaks=()):
    os.makedirs(OUT, exist_ok=True)
    bg = make_background()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)

    def frame(t):
        ctx.set_source_surface(bg); ctx.paint()
        draw_symbols(ctx, t)
        logo(ctx, t)
        draw(ctx, t)
        if t > dur - 0.5:
            ctx.set_source_rgba(0, 0, 0, prog(t, dur - 0.5, dur)); ctx.paint()

    if "--frame" in sys.argv:
        for s in sys.argv[sys.argv.index("--frame") + 1:]:
            frame(float(s)); surf.write_to_png(f"{OUT}/{name}_{s}.png")
        return
    wav = f"{OUT}/{name}.wav"
    build_audio(wav, dur, events, transpose, breaks)
    if "--audio" in sys.argv: return
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", f"{OUT}/{name}.mp4"]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(dur * FPS)):
        frame(i / FPS); surf.flush(); ff.stdin.write(surf.get_data())
    ff.stdin.close(); ff.wait()
    print("listo:", f"{OUT}/{name}.mp4")
