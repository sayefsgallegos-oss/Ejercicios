"""Música de fondo y efectos sintetizados con numpy (sin samples ni licencias)."""
import wave
import numpy as np

SR = 44100
rng = np.random.default_rng(3)

def midi(n): return 440.0 * 2 ** ((n - 69) / 12)

def env(n, a=0.005, d=0.3, curve=6.0):
    t = np.arange(n) / SR
    e = np.exp(-curve * t / max(d, 1e-3))
    na = int(a * SR)
    if na: e[:na] *= np.linspace(0, 1, na)
    return e

def tone(f, dur, harm=(1.0,), a=0.005, d=None, curve=6.0, detune=0.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for i, h in enumerate(harm):
        s += h * np.sin(2 * np.pi * f * (i + 1) * t)
        if detune: s += h * 0.5 * np.sin(2 * np.pi * f * (i + 1) * (1 + detune) * t)
    return s * env(n, a, d or dur, curve)

def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x); acc = 0.0
    # filtro de un polo (vectorizado por bloques sería más rápido; suficiente para este largo)
    from scipy.signal import lfilter
    return lfilter([1 - a], [1, -a], x)

def noise(dur): return rng.uniform(-1, 1, int(dur * SR))

def add(buf, x, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf): return
    x = x[: len(buf) - i]
    buf[i:i + len(x)] += x * gain

# ---------- efectos ----------
def sfx(kind, p):
    if kind == "pop":
        n = int(0.12 * SR); t = np.arange(n) / SR
        f = 500 + 180 * (p % 4) + 900 * t / 0.12
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.12, 5) * 0.5
    if kind == "blip":
        return tone(midi(72 + [0, 2, 4, 7, 9][p % 5] + 12 * (p // 5)), 0.15, (1, 0.3), d=0.15) * 0.25
    if kind == "boom":
        n = int(0.5 * SR); t = np.arange(n) / SR
        f = 120 * np.exp(-t * 8) + 45
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.5, 5)
        return s * 0.8 + tone(midi(76 + 4 * p), 0.5, (1, 0.4, 0.2), d=0.5) * 0.25
    if kind == "whoosh":
        x = lowpass(noise(0.45), 2500)
        n = len(x); e = np.sin(np.linspace(0, np.pi, n)) ** 2
        return x * e * 0.35
    if kind == "question":
        out = np.zeros(int(0.5 * SR))
        add(out, tone(midi(79), 0.18, (1, 0.3), d=0.18) * 0.3, 0)
        add(out, tone(midi(84), 0.35, (1, 0.3), d=0.35) * 0.3, 0.12)
        return out
    if kind == "tick":
        f = 1700 if p < 4 else 2300
        out = tone(f, 0.06, (1,), a=0.001, d=0.05, curve=8) * 0.35
        add(out, lowpass(noise(0.03), 6000) * env(int(0.03 * SR), 0.001, 0.03) * 0.2, 0)
        return out
    if kind == "wrong":
        n = int(0.22 * SR); t = np.arange(n) / SR
        sq = np.sign(np.sin(2 * np.pi * 150 * t)) * 0.5 + np.sign(np.sin(2 * np.pi * 157 * t)) * 0.5
        a = lowpass(sq, 1400) * env(n, 0.005, 0.22, 2) * 0.25
        return np.concatenate([a, np.zeros(int(0.04 * SR)), a * 0.9])
    if kind == "note":  # marimba
        scale = [0, 2, 4, 7, 9]
        n = 72 + scale[p % 5] + 12 * ((p % 10) // 5)
        return tone(midi(n), 0.4, (1, 0, 0, 0.35), d=0.35, curve=7) * 0.28
    if kind == "success":
        out = np.zeros(int(1.4 * SR))
        for i, n in enumerate([72, 76, 79, 84]):
            add(out, tone(midi(n + 2 * p), 1.2, (1, 0.5, 0.25, 0.1), d=1.2, curve=4) * 0.18, i * 0.07)
        return out
    if kind == "fanfare":
        out = np.zeros(int(2.6 * SR))
        for i, n in enumerate([67, 72, 76, 79]):
            add(out, tone(midi(n), 0.25, (1, 0.6, 0.3), d=0.25, curve=3) * 0.2, i * 0.09)
        for n in [72, 76, 79, 84]:
            add(out, tone(midi(n), 2.0, (1, 0.5, 0.3, 0.15), d=2.0, curve=3, detune=0.003) * 0.13, 0.36)
        add(out, lowpass(noise(1.2), 9000) * env(int(1.2 * SR), 0.01, 1.2, 4) * 0.12, 0.36)
        return out
    raise ValueError(kind)

# ---------- música ----------
def music(dur, bpm=104):
    out = np.zeros(int(dur * SR) + SR)
    beat = 60 / bpm
    prog = [(60, [60, 64, 67]), (55, [59, 62, 67]), (57, [57, 60, 64]), (53, [57, 60, 65])]  # C G Am F
    bar = 4 * beat
    nb = int(dur / bar) + 1
    for b in range(nb):
        t0 = b * bar
        root, chord = prog[b % 4]
        for n in chord:  # pad
            add(out, tone(midi(n), bar * 1.05, (1, 0.25), a=0.25, d=bar, curve=1.2, detune=0.004) * 0.045, t0)
        for k in (0, 2, 2.5):  # bajo
            add(out, tone(midi(root - 24), beat * 0.9, (1, 0.5), a=0.01, d=beat, curve=3) * 0.16, t0 + k * beat)
        arp = [chord[0] + 12, chord[1] + 12, chord[2] + 12, chord[1] + 12]
        for k in range(8):  # arpegio en corcheas
            add(out, tone(midi(arp[k % 4]), 0.25, (1, 0, 0.2), d=0.22, curve=6) * 0.05, t0 + k * beat / 2)
        for k in range(4):  # batería suave
            if k in (0, 2):
                n = int(0.25 * SR); tt = np.arange(n) / SR
                kick = np.sin(2 * np.pi * np.cumsum(55 + 90 * np.exp(-tt * 30)) / SR) * env(n, 0.001, 0.25, 6)
                add(out, kick * 0.32, t0 + k * beat)
            else:
                add(out, lowpass(noise(0.15), 4000) * env(int(0.15 * SR), 0.002, 0.15, 7) * 0.12, t0 + k * beat)
            add(out, (noise(0.04) - lowpass(noise(0.04), 6000)) * env(int(0.04 * SR), 0.001, 0.04, 6) * 0.05, t0 + k * beat + beat / 2)
    return out[: int(dur * SR)]

def build_audio(path, dur, events):
    n = int(dur * SR)
    mus = music(dur)
    t = np.arange(n) / SR
    fade = np.clip(t / 1.0, 0, 1) * np.clip((dur - t) / 1.5, 0, 1)
    fx = np.zeros(n + 3 * SR)
    for tm, kind, p in events:
        add(fx, sfx(kind, p), tm)
    mix = mus * fade * 0.9 + fx[:n]
    mix = np.tanh(mix * 1.6) / np.tanh(1.6)  # suave limitador
    mix *= 0.89 / max(1e-6, np.abs(mix).max())
    pcm = (mix * 32767).astype(np.int16)
    st = np.stack([pcm, pcm], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
