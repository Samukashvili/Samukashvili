"""Build profile assets: python tools/build_assets.py --portfolio PATH (Pillow required)."""
from argparse import ArgumentParser
from pathlib import Path
import math
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageSequence

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
BG, MINT, WHITE, MUTED = '#0b1218', '#b1f4cf', '#edf3ee', '#9aacb5'

def font(size, bold=False, mono=False):
    name = 'consola.ttf' if mono else 'segoeuib.ttf' if bold else 'segoeui.ttf'
    return ImageFont.truetype(str(Path('C:/Windows/Fonts') / name), size)

def text(x, y, value, size=20, color=WHITE, weight=400, spacing=None, mono=False):
    family = 'Consolas, monospace' if mono else 'Segoe UI, Arial, sans-serif'
    tracking = f' letter-spacing="{spacing}"' if spacing else ''
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" font-weight="{weight}"{tracking}>{escape(value)}</text>'

def terrain():
    """A shaded height field with normal-map-inspired colors."""
    n = 28
    def p(i,j):
        u,v = i/n,j/n
        h = math.exp(-((u-.43)**2/.06+(v-.45)**2/.10))
        h += .63*math.exp(-((u-.80)**2/.034+(v-.72)**2/.06))
        h += .25*math.sin(u*10+v*5)*math.sin(v*7)
        return 790+(u-v)*245,174+(u+v)*107-h*139
    output = ['<g transform="translate(86 55)">']
    for j in range(n):
        for i in range(n):
            points=[p(i,j),p(i+1,j),p(i+1,j+1),p(i,j+1)]
            bright=max(0,min(1,.45+(p(i,j)[1]-p(i+1,j)[1])*.065))
            a,b=((93,107,165),(183,169,228)) if j/n>.54 else ((88,148,180),(177,244,207))
            c=tuple(int(a[k]*(1-bright)+b[k]*bright) for k in range(3))
            color='#%02x%02x%02x'%c
            pts=' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
            output.append(f'<polygon points="{pts}" fill="{color}" stroke="#0b1822" stroke-opacity=".42" stroke-width=".7"/>')
    return ''.join(output)+ '</g>'

def header(mobile=False):
    w,h=(720,490) if mobile else (1200,440)
    body=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
          '<title id="title">Giorgi Samukashvili — Ideas, engineered.</title>',
          '<desc id="desc">Software developer based in Tbilisi, Georgia. A procedural terrain surface represents GPU programming and real-time systems.</desc>',
          '<defs><radialGradient id="glow"><stop stop-color="#224b45" stop-opacity=".55"/><stop offset="1" stop-color="#0b1218" stop-opacity="0"/></radialGradient><pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#98b8b5" opacity=".12"/></pattern></defs>',
          f'<rect width="{w}" height="{h}" rx="16" fill="{BG}"/>',
          f'<rect width="{w}" height="{h}" rx="16" fill="url(#dots)"/>']
    if mobile:
        body += ['<ellipse cx="555" cy="175" rx="235" ry="180" fill="url(#glow)"/>',
                 '<g opacity=".50" transform="translate(-180 -11) scale(.78)">'+terrain()+'</g>',
                 f'<path d="M36 46H62" stroke="{MINT}" stroke-width="3"/>',
                 text(76,52,'IDEAS, ENGINEERED.',19,MINT,spacing=3,mono=True),
                 text(36,161,'Giorgi',77,weight=600,spacing=-3),
                 text(36,247,'Samukashvili',76,weight=600,spacing=-3),
                 text(38,309,'Software developer',27,MINT),
                 text(38,357,'Computer vision. Real-time systems.',21,MUTED),
                 text(38,389,'Turning complex problems into tools.',21,MUTED),
                 '<path d="M36 422H684" stroke="#30413f"/>',
                 text(38,456,'TBILISI, GEORGIA',17,MUTED,spacing=1,mono=True),
                 text(456,456,'samukashvili.ge',18,MINT,mono=True)]
    else:
        body += ['<ellipse cx="910" cy="220" rx="360" ry="230" fill="url(#glow)"/>',
                 '<g fill="none" stroke="#809d94" stroke-opacity=".17"><path d="M666 247L876 345L1160 227L950 129Z"/><path d="M666 273L876 371L1160 253"/><path d="M666 299L876 397L1160 279"/></g>',
                 terrain(),
                 f'<path d="M52 54H82" stroke="{MINT}" stroke-width="3"/>',
                 text(96,60,'IDEAS, ENGINEERED.',19,MINT,spacing=3,mono=True),
                 text(50,167,'Giorgi',82,weight=600,spacing=-3),
                 text(50,253,'Samukashvili',80,weight=600,spacing=-4),
                 text(54,305,'Software developer',27,MINT),
                 text(54,351,'Computer vision. GPU systems. Developer tools.',20,MUTED),
                 text(726,63,'CODE / VISION / SYSTEMS',15,MUTED,spacing=1.4,mono=True),
                 '<path d="M52 381H1148" stroke="#30413f"/>',
                 text(54,412,'TBILISI, GEORGIA',16,MUTED,spacing=1,mono=True),
                 text(940,412,'samukashvili.ge',18,MINT,mono=True)]
    (OUT/('header-mobile.svg' if mobile else 'header.svg')).write_text('\n'.join(body+['</svg>']),encoding='utf-8')

def contain(canvas,image,box):
    x,y,w,h=box
    im=ImageOps.contain(image.convert('RGB'),(w,h),Image.Resampling.LANCZOS)
    canvas.paste(im,(x+(w-im.width)//2,y+(h-im.height)//2))

def showcase(portfolio,mobile=False):
    source=portfolio/'assets/images/LUMEN-PS'
    dims=(720,730) if mobile else (1200,414)
    canvas=Image.new('RGB',dims,BG)
    draw=ImageDraw.Draw(canvas)
    draw.text((30,20),'LUMEN-PS / MATERIAL RECONSTRUCTION',font=font(18 if mobile else 19,mono=True),fill=MINT)
    draw.line((30,59,dims[0]-30,59),fill='#2d3b43',width=1)
    if mobile:
        boxes=[(22,89,333,263),(365,89,333,263),(22,395,333,263),(365,395,333,263)]
        labels=[(27,361),(370,361),(27,672),(370,672)]
    else:
        boxes=[(18,85,278,267),(312,85,278,267),(606,85,278,267),(900,85,278,267)]
        labels=[(25,369),(319,369),(613,369),(907,369)]
    for k,name in enumerate(['ALBEDO','NORMAL','HEIGHT'],1):
        contain(canvas,Image.open(source/('kiwi-'+name.lower()+'.webp')),boxes[k])
    for (x,y),label in zip(labels,['01 / RELIGHT','02 / ALBEDO','03 / NORMAL','04 / HEIGHT']):
        draw.text((x,y),label,font=font(20,mono=True),fill=WHITE)
    frames,durations=[],[]
    for frame in ImageSequence.Iterator(Image.open(source/'kiwi-relight.gif')):
        result=canvas.copy()
        contain(result,frame,boxes[0])
        frames.append(result)
        durations.append(frame.info.get('duration',80))
    suffix='-mobile' if mobile else ''
    frames[0].save(OUT/f'lumen-showcase{suffix}.jpg',quality=90,optimize=True)
    # Share one palette to prevent static maps from flickering between frames.
    palette_board=Image.new('RGB',(1200,1200),BG)
    for i,frame in enumerate(frames):
        sample=ImageOps.contain(frame,(200,200),Image.Resampling.LANCZOS)
        palette_board.paste(sample,((i%6)*200,(i//6)*200))
    palette=palette_board.quantize(colors=256)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.FLOYDSTEINBERG) for im in frames]
    indexed[0].save(OUT/f'lumen-showcase{suffix}.gif',save_all=True,append_images=indexed[1:],duration=durations,loop=0,optimize=True,disposal=1)

def products(portfolio,mobile=False):
    canvas=Image.new('RGB',(720,1240) if mobile else (1200,330),BG)
    draw=ImageDraw.Draw(canvas)
    entries=[('MarchingWorld/lod-overview-color.webp','MarchingWorld','C# / HLSL / UNITY'),
             ('StereoDepth/stereo-depth-demo-poster.webp','Live Stereo Depth','JAVA / OPENGL ES'),
             ('Collection Zones/CollectionZonesThumbnail_Black.png','Collection Zones','PYTHON / BLENDER')]
    boxes=[(20,20,680,340),(20,430,680,340),(20,840,680,340)] if mobile else [(18,18,376,215),(412,18,376,215),(806,18,376,215)]
    for (source,title,stack),(x,y,w,h) in zip(entries,boxes):
        contain(canvas,Image.open(portfolio/f'assets/images/{source}'),(x,y,w,h))
        draw.text((x+2,y+h+10),title,font=font(29 if mobile else 25,bold=True),fill=WHITE)
        draw.text((x+2,y+h+52),stack,font=font(20 if mobile else 18,mono=True),fill=MINT)
    canvas.save(OUT/('products-mobile.jpg' if mobile else 'products.jpg'),quality=90,optimize=True)

if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--portfolio',type=Path,required=True)
    args=parser.parse_args()
    OUT.mkdir(exist_ok=True)
    for mobile in [False,True]:
        header(mobile)
        showcase(args.portfolio,mobile)
        products(args.portfolio,mobile)
    for f in sorted(OUT.iterdir()):
        if f.is_file(): print(f'{f.name}: {f.stat().st_size:,} bytes')
