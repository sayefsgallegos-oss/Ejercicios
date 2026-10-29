"""Separa cada pose de una hoja PNG con transparencia real en archivos individuales."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

src, out_dir, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
DIL = int(sys.argv[4]) if len(sys.argv) > 4 else 6  # cuánto se "engordan" las piezas para unir partes sueltas
A = np.array(Image.open(src).convert("RGBA"))
m = A[:, :, 3] > 30
lab, n = ndimage.label(ndimage.binary_dilation(m, iterations=DIL))
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
