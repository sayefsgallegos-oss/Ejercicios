"""Separa cada pose de las hojas de stickers (PNG/WebP con transparencia) en archivos individuales."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

src_dir, out_dir = sys.argv[1], sys.argv[2]
sheets = {"11": "a", "12": "b", "13": "c", "14": "d"}
thumbs = []
for num, tag in sheets.items():
    im = Image.open(f"{src_dir}/{num}.webp").convert("RGBA")
    a = np.array(im)[:, :, 3] > 20
    lab, n = ndimage.label(ndimage.binary_dilation(a, iterations=4))
    sizes = ndimage.sum(a, lab, range(1, n + 1))
    big = [i + 1 for i in range(n) if sizes[i] > 9000]
    cents = {i: ndimage.center_of_mass(a, lab, i) for i in range(1, n + 1)}
    # las piezas chicas (antenas, monedas sueltas) se unen a la pose grande más cercana
    owner = np.zeros(n + 1, int)
    for i in range(1, n + 1):
        if i in big: owner[i] = i; continue
        cy, cx = cents[i]
        owner[i] = min(big, key=lambda j: (cents[j][0] - cy) ** 2 + (cents[j][1] - cx) ** 2)
    lab = owner[lab] * (lab > 0)
    items = []
    for i in big:
        ys, xs = np.where(lab == i)
        sl = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
        items.append((sl[0].start // 150, sl[1].start, i - 1, sl))
    for k, (_, _, i, sl) in enumerate(sorted(items)):
        crop = np.array(im)[sl].copy()
        crop[lab[sl] != i + 1, 3] = 0
        name = f"{tag}{k:02d}"
        Image.fromarray(crop).save(f"{out_dir}/{name}.png")
        thumbs.append((name, Image.fromarray(crop)))
# catálogo
cols, cw, ch = 8, 220, 250
rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cw, rows * ch), (235, 240, 248))
d = ImageDraw.Draw(sheet)
f = ImageFont.truetype("/root/.local/share/fonts/Fredoka-Bold.ttf", 26)
for j, (name, t) in enumerate(thumbs):
    t = t.copy(); t.thumbnail((cw - 20, ch - 50))
    x, y = (j % cols) * cw, (j // cols) * ch
    sheet.paste(t, (x + (cw - t.width) // 2, y + 10), t)
    d.text((x + 10, y + ch - 36), name, fill=(11, 42, 91), font=f)
sheet.save(f"{out_dir}/_catalogo.png")
print(len(thumbs), "poses")
