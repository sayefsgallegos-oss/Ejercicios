"""Motor para videos con Matti (azul) y Numi (naranja): poses recortadas, globos de diálogo y voces tipo videojuego."""
import wave
from kit import *
from audio import SR, midi, env, tone, lowpass, noise, add, sfx

SPR_DIR = os.path.join(HERE, "assets", "robots")
_SPR = {}
VOICE = {"matti": 55, "numi": 67}
CPS = 24

def spr(name):
    if name not in _SPR:
        _SPR[name] = cairo.ImageSurface.create_from_png(os.path.join(SPR_DIR, name + ".png"))
    return _SPR[name]

def sprite(ctx, name, cx, bottom, h, alpha=1.0, rot=0.0, flip=False, sx=1.0, sy=1.0):
    if alpha <= 0.001 or h <= 1: return
    s = spr(name); k = h / s.get_height()
    ctx.save(); ctx.translate(cx, bottom); ctx.rotate(rot)
    ctx.scale(k * sx * (-1 if flip else 1), k * sy)
    ctx.translate(-s.get_width() / 2, -s.get_height())
    ctx.set_source_surface(s); ctx.get_source().set_filter(cairo.FILTER_BEST)
    ctx.paint_with_alpha(alpha); ctx.restore()

def floor_shadow(ctx, cx, y, w, alpha=1.0):
    ctx.save(); ctx.translate(cx, y); ctx.scale(w, w * 0.16)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, 1)
    g.add_color_stop_rgba(0, 0.02, 0.1, 0.3, 0.35 * alpha); g.add_color_stop_rgba(1, 0.02, 0.1, 0.3, 0)
    ctx.set_source(g); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.fill(); ctx.restore()

class Cast:
    """Diálogos de un video: [(inicio, fin, quién, [líneas])]."""
    def __init__(self, dialog): self.dialog = dialog
    def talking(self, who, t):
        for st, en, w, lines in self.dialog:
            if w == who and st <= t < st + sum(len(l) for l in lines) / CPS: return True
        return False
    def bubbles(self, ctx, t, heads):
        for st, en, who, lines in self.dialog:
            if st <= t < en and who in heads: bubble(ctx, t, st, en, lines, *heads[who])

def robot(ctx, t, cast, who, pose, x, floor, h, alpha=1.0, scale=1.0, rot=0.0, flip=False, ph=0.0):
    """Robot flotando sobre su sombra; rebota un poco al hablar. Devuelve la posición de su cabeza."""
    hov = 12 * math.sin(t * 2.3 + ph)
    tk = cast.talking(who, t) if cast else False
    sy = 1 + (0.035 * abs(math.sin(t * 14)) if tk else 0)
    floor_shadow(ctx, x, floor, h * 0.32 * scale * (1 - hov / 150), alpha)
    sprite(ctx, pose, x, floor - 26 - hov, h * scale, alpha, rot, flip, 1 / sy ** 0.5, sy)
    return (x, floor - 26 - hov - h * scale * 0.98)

def sweat(ctx, x, y, t, alpha=1.0):
    k = (t * 1.5) % 1
    ctx.save(); ctx.translate(x, y + 30 * k)
    ctx.move_to(0, -26); ctx.curve_to(14, -4, 16, 12, 0, 14); ctx.curve_to(-16, 12, -14, -4, 0, -26)
    ctx.set_source_rgba(0.55, 0.85, 1, alpha * (1 - k)); ctx.fill_preserve()
    ctx.set_source_rgba(*hexc(NAVY, alpha * (1 - k))); ctx.set_line_width(3); ctx.stroke(); ctx.restore()

def bubble(ctx, t, st, en, lines, ax, ay, size=46):
    k = pop(t, st, 0.3) * (1 - prog(t, en - 0.15, en))
    if k <= 0: return
    n = int((t - st) * CPS)
    wmax = max(text_w(ctx, l, size) for l in lines) + 70
    h = len(lines) * 60 + 42
    bx = clamp(ax - wmax / 2, 40, W - 40 - wmax)
    by = ay - h - 46
    ctx.save(); ctx.translate(ax, ay); sc(ctx, k); ctx.translate(-ax, -ay)
    rrect(ctx, bx, by + 8, wmax, h, 32); ctx.set_source_rgba(0.03, 0.15, 0.4, 0.22); ctx.fill()
    rrect(ctx, bx, by, wmax, h, 32); ctx.set_source_rgb(1, 1, 1); ctx.fill()
    tx = clamp(ax, bx + 50, bx + wmax - 50)
    ctx.move_to(tx - 20, by + h - 2); ctx.line_to(clamp(ax, bx + 30, bx + wmax - 30), ay - 8); ctx.line_to(tx + 22, by + h - 2); ctx.fill()
    shown = n
    for i, l in enumerate(lines):
        text(ctx, l[:max(0, shown)], bx + 35, by + 50 + i * 60, size, NAVY, align="l"); shown -= len(l)
    ctx.restore()

def name_tag(ctx, x, y, label, color, alpha=1.0, scale=1.0):
    pill(ctx, x, y, label, 36, color, WHITE, alpha, scale, padx=24, pady=10)

def confetti(ctx, t, t0, cx, cy, alpha=1.0):
    tc = t - t0
    if not (0 < tc < 3.5): return
    for c in CONF:
        tt = tc - c["d"]
        if tt <= 0: continue
        x = cx + math.cos(c["a"]) * c["v"] * tt * 0.8
        y = cy + math.sin(c["a"]) * c["v"] * tt * 0.8 + 900 * tt * tt
        ctx.save(); ctx.translate(x, y); ctx.rotate(c["rs"] * tt)
        ctx.rectangle(-c["w"] / 2, -c["w"] / 4, c["w"], c["w"] / 2)
        ctx.set_source_rgba(*hexc(c["c"], clamp(1.4 - tt / 3) * alpha)); ctx.fill(); ctx.restore()


# ---------- sonido ----------
def blip(f, rng):
    n = int(0.055 * SR); tt = np.arange(n) / SR
    f = f * (1 + rng.uniform(-0.05, 0.05))
    s = np.sign(np.sin(2 * np.pi * f * tt)) * 0.3 + np.sin(2 * np.pi * f * 2 * tt) * 0.45
    return lowpass(s, 2800) * env(n, 0.004, 0.055, 3) * 0.2

def fx(kind):
    if kind == "siren":
        n = int(1.6 * SR); tt = np.arange(n) / SR
        f = 700 + 300 * np.sign(np.sin(2 * np.pi * 2.5 * tt))
        s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR))
        return lowpass(s, 2500) * env(n, 0.01, 1.6, 0.6) * 0.14
    if kind == "beep":
        out = np.zeros(int(0.6 * SR))
        for i in range(3): add(out, tone(1320, 0.09, (1, 0.3), d=0.09, curve=2) * 0.22, i * 0.17)
        return out
    if kind == "glitch":
        rng = np.random.default_rng(2); out = np.zeros(int(1.0 * SR))
        for i in range(10):
            d = rng.uniform(0.02, 0.08); add(out, noise(d) * rng.uniform(0.1, 0.3) * env(int(d * SR), 0.001, d, 1), rng.uniform(0, 0.9))
        return out
    if kind == "hum":
        n = int(2.6 * SR); tt = np.arange(n) / SR
        s = sum(np.sin(2 * np.pi * f * tt) / k for k, f in enumerate([55, 110, 165, 220], 1))
        s *= 0.6 + 0.4 * np.sin(2 * np.pi * 6 * tt)
        return s * np.clip(tt / 1.2, 0, 1) * np.clip((2.6 - tt) / 0.3, 0, 1) * 0.18
    if kind == "flash":
        x = noise(0.7); x = x - lowpass(x, 3000)
        return x * env(len(x), 0.002, 0.7, 4) * 0.4
    if kind == "unlock":
        out = np.zeros(int(0.6 * SR))
        add(out, tone(midi(76), 0.15, (1, 0.4), d=0.15) * 0.25, 0); add(out, tone(midi(83), 0.35, (1, 0.4), d=0.35) * 0.25, 0.12)
        return out
    if kind == "rise":
        n = int(2.0 * SR); tt = np.arange(n) / SR
        f = 200 * 2 ** (tt * 1.6)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.05, 2.0, 1.5) * 0.15
    if kind == "heart":
        out = np.zeros(int(0.8 * SR))
        for d, g in ((0, 0.5), (0.22, 0.35)):
            nk = int(0.18 * SR); tt = np.arange(nk) / SR
            add(out, np.sin(2 * np.pi * np.cumsum(40 + 50 * np.exp(-tt * 25)) / SR) * env(nk, 0.002, 0.18, 5) * g, d)
        return out
    return sfx(kind, 0)

def music_mystery(dur, tension=()):
    """Fondo de misterio: acordes largos en menor, bajo pedal y arpegio suave; latidos en la tensión."""
    out = np.zeros(int(dur * SR) + 2 * SR)
    chords = [[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 56, 59]]
    bar = 2.6
    for b in range(int(dur / bar) + 1):
        ch = chords[b % 4]; t0 = b * bar
        for nn in ch:
            add(out, tone(midi(nn), bar * 1.2, (1, 0.3, 0.1), a=0.8, d=bar * 1.2, curve=1.0, detune=0.003) * 0.05, t0)
        add(out, tone(midi(ch[0] - 24), bar, (1, 0.5), a=0.3, d=bar, curve=1.0) * 0.12, t0)
        for k, nn in enumerate([ch[0] + 12, ch[2] + 12, ch[1] + 24, ch[2] + 12]):
            add(out, tone(midi(nn), 0.6, (1, 0, 0.2), d=0.5, curve=5) * 0.04, t0 + k * bar / 4)
    for a, b in tension:
        t = a
        while t < b: add(out, fx("heart"), t); t += 0.75
    return out[: int(dur * SR)]

def build_audio(path, dur, events, dialog, music="pop", transpose=0, breaks=(), tension=(), mgain=0.4, extra=()):
    n = int(dur * SR); t = np.arange(n) / SR
    mus = music_pop(dur, transpose, breaks=breaks) if music == "pop" else music_mystery(dur, tension)
    fade_ = np.clip(t / 0.6, 0, 1) * np.clip((dur - t) / 1.5, 0, 1)
    fxb = np.zeros(n + 4 * SR)
    for tm, kind, p in events:
        add(fxb, fx(kind) if kind in ("siren", "beep", "glitch", "hum", "flash", "unlock", "rise", "heart") else sfx(kind, p), tm)
    rng = np.random.default_rng(5)
    for st, en, who, lines in dialog:
        base = midi(VOICE[who])
        for i in range(0, sum(len(l) for l in lines), 2):
            add(fxb, blip(base * 2 ** (rng.choice([0, 2, 4, 7]) / 12), rng), st + i / CPS)
    for tm, arr in extra: add(fxb, arr, tm)
    mix = mus * fade_ * mgain + fxb[:n]
    mix = np.tanh(mix * 1.4) / np.tanh(1.4)
    mix *= 0.89 / np.abs(mix).max()
    pcm = (mix * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.stack([pcm, pcm], 1).tobytes())

def render(name, dur, draw, events, dialog, **audio_kw):
    import kit
    kit.build_audio = lambda path, d, ev, tr, br: build_audio(path, d, events, dialog, **audio_kw)
    kit.run(name, dur, draw, events)
