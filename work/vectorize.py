from PIL import Image
from collections import defaultdict
from pathlib import Path
im = Image.open('work/mona-lisa-reference.webp').convert('RGB')
w=500
h=round(im.height*w/im.width)
im=im.resize((w,h),Image.Resampling.LANCZOS)
q=im.quantize(colors=96, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
palette=q.getpalette()
pixels=q.load()
paths=defaultdict(list)
for y in range(h):
    start=0
    color=pixels[0,y]
    for x in range(1,w+1):
        c=pixels[x,y] if x<w else -1
        if c != color:
            width=x-start
            paths[color].append(f'M{start} {y}h{width}v1h-{width}z')
            start=x
            color=c
out=Path('outputs/mona-lisa.svg')
with out.open('w') as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc" shape-rendering="crispEdges">\n')
    f.write('<title id="title">Mona Lisa</title><desc id="desc">A vector mosaic of Leonardo da Vinci’s Mona Lisa, made from colored shapes based on a public-domain reproduction from Wikimedia Commons.</desc>\n')
    f.write('<!-- Source: https://commons.wikimedia.org/wiki/File:Mona_Lisa.jpg -->\n')
    for color, segments in paths.items():
        rgb=palette[color*3:color*3+3]
        f.write(f'<path fill="#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}" d="')
        f.write(''.join(segments))
        f.write('"/>\n')
    f.write('</svg>\n')
print(im.size, len(paths), out.stat().st_size)
q.convert('RGB').save('work/preview.png')
