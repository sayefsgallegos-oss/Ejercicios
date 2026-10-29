"""Quita un fondo negro sólido: rellena desde los bordes solo los píxeles casi negros conectados al borde.
Los brillos (hologramas) sobre negro se convierten en semitransparencia según su luminosidad."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

src, dst = sys.argv[1], sys.argv[2]
a = np.array(Image.open(src).convert("RGB")).astype(float)
mx = a.max(2)
dark = mx < 14
lab, n = ndimage.label(dark)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(border))
# zona de transición: píxeles cerca del fondo y poco brillantes -> alfa proporcional al brillo (brillos y bordes suaves)
near = ndimage.binary_dilation(bg, iterations=3) & ~bg
alpha = np.where(bg, 0.0, 1.0)
soft = near & (mx < 120)
alpha[soft] = np.clip(mx[soft] / 120, 0, 1)
rgb = a.copy()
# des-premultiplicar en los bordes suaves para no dejar halo negro
k = soft & (alpha > 0.05)
rgb[k] = np.clip(a[k] / alpha[k, None], 0, 255)
out = np.dstack([rgb, alpha * 255]).astype(np.uint8)
Image.fromarray(out, "RGBA").save(dst)
