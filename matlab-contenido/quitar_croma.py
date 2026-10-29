"""Quita un fondo de color sólido tipo pantalla (magenta o verde) conectado a los bordes,
con borde suave y limpieza del tinte del fondo en los contornos."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

src, dst, key = sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "magenta"
a = np.array(Image.open(src).convert("RGB")).astype(float)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
# "cuánto se parece al fondo": 1 = fondo puro, 0 = nada
# se mide el tono (no el brillo), así el fondo que cae en sombra también se detecta
if key == "magenta":
    ratio = (np.minimum(r, b) - g) / np.maximum(1, np.maximum(r, b))
else:
    ratio = (g - np.maximum(r, b)) / np.maximum(1, g)
keyness = np.clip((ratio - 0.45) / 0.35, 0, 1) * np.clip((np.maximum(r, b) if key == "magenta" else g) / 60, 0, 1)
core = keyness > 0.5
lab, n = ndimage.label(core)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
sizes = ndimage.sum(core, lab, range(1, n + 1))
# fondo = lo conectado al borde + huecos interiores grandes (los chicos, como un pétalo del logo, se respetan)
keep = [i + 1 for i in range(n) if (i + 1) in border or sizes[i] > 8]
bg = np.isin(lab, keep)
zone = ndimage.binary_dilation(bg, iterations=5)
alpha = np.ones_like(r)
alpha[bg] = 0
edge = zone & ~bg
alpha[edge] = 1 - keyness[edge]
# quitar tinte del fondo en los contornos
if key == "magenta":
    m = np.minimum(r, b); spill = np.clip(m - g, 0, None) * edge
    a[..., 0] -= spill * 0.8; a[..., 2] -= spill * 0.8
else:
    spill = np.clip(g - np.maximum(r, b), 0, None) * edge
    a[..., 1] -= spill * 0.8
out = np.dstack([np.clip(a, 0, 255), alpha * 255]).astype(np.uint8)
Image.fromarray(out, "RGBA").save(dst)
