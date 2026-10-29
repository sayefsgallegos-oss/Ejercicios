"""Quita un fondo de cuadritos 'dibujado' (falsa transparencia) y separa cada pose en un PNG."""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

src, out_dir, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
im = Image.open(src).convert("RGB")
a = np.array(im).astype(int)
mx, mn = a.max(2), a.min(2)
sat = mx - mn
# píxel "tipo cuadrito": gris sin color, ni muy oscuro ni blanco brillante
bgish = (sat < 22) & (mx > 105) & (mx < 218)
bgish = ndimage.binary_opening(bgish, iterations=1)
lab, n = ndimage.label(bgish)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(border))
# huecos chicos dentro del fondo (bordes entre cuadritos) también son fondo
bg = ndimage.binary_closing(bg, iterations=2)
fg = ~bg
fg = ndimage.binary_opening(fg, iterations=1)
fg = ndimage.binary_fill_holes(fg)
alpha = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
rgba = im.convert("RGBA"); rgba.putalpha(alpha)
# separar poses
A = np.array(rgba)
m = A[:, :, 3] > 40
lab, n = ndimage.label(ndimage.binary_dilation(m, iterations=6))
sizes = ndimage.sum(m, lab, range(1, n + 1))
big = [i + 1 for i in range(n) if sizes[i] > 20000]
cents = {i: ndimage.center_of_mass(m, lab, i) for i in range(1, n + 1)}
owner = np.zeros(n + 1, int)
for i in range(1, n + 1):
    if i in big: owner[i] = i; continue
    if sizes[i - 1] < 150: continue
    cy, cx = cents[i]; owner[i] = min(big, key=lambda j: (cents[j][0] - cy) ** 2 + (cents[j][1] - cx) ** 2)
lab = owner[lab] * (lab > 0)
items = sorted(big, key=lambda i: (round(cents[i][0] / 300), cents[i][1]))
for k, i in enumerate(items):
    ys, xs = np.where(lab == i)
    sl = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
    crop = A[sl].copy(); crop[lab[sl] != i, 3] = 0
    Image.fromarray(crop).save(f"{out_dir}/{prefix}{k:02d}.png")
print(len(items), "poses")
