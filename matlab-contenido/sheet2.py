import sys
from PIL import Image
name, files = sys.argv[1], sys.argv[2:]
ims = [Image.open(f).resize((360, 640)) for f in files]
cols = min(6, len(ims)); rows = (len(ims) + cols - 1) // cols
sh = Image.new("RGB", (cols * 360, rows * 640))
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 360, (i // cols) * 640))
sh.save(name)
