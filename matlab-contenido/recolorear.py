"""Cambia el color del cuerpo morado de un personaje (por tono), sin tocar negro, blanco ni dorado."""
import sys
import numpy as np
from PIL import Image

src, dst, mode = sys.argv[1], sys.argv[2], sys.argv[3]
im = Image.open(src).convert("RGBA")
hsv = np.array(im.convert("RGB").convert("HSV")).astype(float)
a = np.array(im)
h, s, v = hsv[..., 0] * 360 / 255, hsv[..., 1] / 255, hsv[..., 2] / 255
purple = (h > 245) & (h < 300) & (s > 0.3)
if mode == "carbon":      # gris carbón con un leve tono rojizo
    nh, ns, nv = 355 / 360, 0.18, v * 0.42
elif mode == "rojo":      # rojo vino
    nh, ns, nv = 352 / 360, s * 0.85, v * 0.75
out = hsv.copy()
out[..., 0] = np.where(purple, nh * 255, hsv[..., 0])
out[..., 1] = np.where(purple, (ns if np.isscalar(ns) else ns) * 255, hsv[..., 1])
out[..., 2] = np.where(purple, np.clip(nv, 0, 1) * 255, hsv[..., 2])
rgb = Image.fromarray(out.astype(np.uint8), "HSV").convert("RGB")
res = np.dstack([np.array(rgb), a[..., 3]])
Image.fromarray(res.astype(np.uint8), "RGBA").save(dst)
