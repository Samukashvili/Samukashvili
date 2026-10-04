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
    output = ['<g transform="translate(165 25) scale(.9)">']
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
    # Quantize the animated panel independently: diffusion from its changing
    # pixels must not alter the index values of the static recovered maps.
    indexed=[]
    static=canvas.quantize(palette=palette,dither=Image.Dither.FLOYDSTEINBERG)
    x,y,w,h=boxes[0]
    for im in frames:
        result=static.copy()
        animated=im.crop((x,y,x+w,y+h)).quantize(palette=palette,dither=Image.Dither.FLOYDSTEINBERG)
        result.paste(animated,(x,y))
        indexed.append(result)
    indexed[0].save(OUT/f'lumen-showcase{suffix}.gif',save_all=True,append_images=indexed[1:],duration=durations,loop=0,optimize=True,disposal=1)

def box(x,y,w,h,fill='#0b1218',stroke='#36464d',radius=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'

def arrow(x,y,end):
    return f'<path d="M{x} {y}H{end}m-7 -6 7 6-7 6" fill="none" stroke="{MINT}" stroke-width="2"/>'

def cube(x,y,s,color):
    points=f'{x},{y-s*.5} {x+s},{y} {x+s},{y+s} {x},{y+s*1.5} {x-s},{y+s} {x-s},{y}'
    return f'<polygon points="{points}" fill="{color}" fill-opacity=".10" stroke="{color}" stroke-width="1.7"/><path d="M{x-s} {y}l{s} {s*.5} {s} {-s*.5}M{x} {y+s*.5}v{s}m0 {-s}v{-s}" fill="none" stroke="{color}" stroke-width="1.7"/>'

def systems(mobile=False):
    w,h=(720,1820) if mobile else (1200,834)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
           '<title id="title">The systems behind the software</title>',
           '<desc id="desc">Conceptual illustrations of four projects: a WebGL editor exports to the browser; terrain streams with levels of detail; two cameras reconstruct metric depth; spatial zones group scene objects.</desc>',
           '<defs><linearGradient id="depth" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#5675e2"/><stop offset=".4" stop-color="#67d3db"/><stop offset=".7" stop-color="#b1f4cf"/><stop offset="1" stop-color="#e9c989"/></linearGradient><linearGradient id="screen" x2="1" y2="1"><stop stop-color="#193038"/><stop offset="1" stop-color="#121a26"/></linearGradient></defs>',
           f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>',
           text(26,38,'THE SYSTEMS BEHIND THE SOFTWARE',20,MINT,spacing=1.5,mono=True)]
    titles=[('WebGL SceneBuilder','TYPESCRIPT / WEBGL'),('MarchingWorld','C# / HLSL / UNITY'),('Live Stereo Depth','JAVA / OPENGL ES'),('Collection Zones','PYTHON / BLENDER')]
    scale=1.2 if mobile else 1
    positions=[(24,70+i*434) for i in range(4)] if mobile else [(24,72),(616,72),(24,454),(616,454)]
    for index,((title,stack),(x,y)) in enumerate(zip(titles,positions)):
        card=[f'<g transform="translate({x} {y}) scale({scale})">',box(0,0,560,354,'#111a22','#26383f',12),
              text(24,38,title,27,weight=600),text(24,67,stack,15,MUTED,spacing=1,mono=True)]
        if index==0:
            card += [box(24,101,248,182),box(24,101,248,27,'#1c2932'),
                     text(35,119,'scene.editor',12,MUTED,mono=True),
                     '<circle cx="250" cy="114" r="3" fill="#b1f4cf"/>',
                     box(35,139,62,130,'#121d25','#26353e',3),
                     text(44,157,'SCENE',10,MUTED,mono=True),
                     '<g stroke="#577581" stroke-width="3"><path d="M46 176H83M53 193H83M53 210H76M46 238H81M46 256H69"/></g>',
                     box(107,138,154,131,'url(#screen)','#26353e',3),
                     '<path d="M109 235H259M109 251H259M143 269L179 208L213 269" fill="none" stroke="#426065" stroke-opacity=".5"/>',
                     cube(181,177,33,'#a4ccf0'),
                     '<path d="M228 247h17m-8 -8v17" stroke="#b1f4cf" stroke-width="1.5"/>',
                     arrow(284,193,311),box(323,112,213,160),box(323,112,213,26,'#1c2932'),
                     '<g fill="#74938e"><circle cx="337" cy="125" r="3"/><circle cx="347" cy="125" r="3"/><circle cx="357" cy="125" r="3"/></g>',
                     text(387,130,'your.site',11,MUTED,mono=True),
                     '<ellipse cx="430" cy="242" rx="57" ry="8" fill="#244940" opacity=".4"/>',
                     cube(430,181,36,MINT),text(347,254,'self-contained bundle',12,MUTED,mono=True),
                     text(24,329,'EDIT → OPTIMIZE → EXPORT',17,MINT,mono=True)]
        elif index==1:
            # Chunk spacing illustrates LOD; heights are decorative, not benchmark data.
            def point(i,j):
                u,v=i/12,j/12
                z=38*math.sin(u*math.pi)*math.sin(v*math.pi)+15*math.cos(u*7+v*4)
                return 282+(u-v)*224,116+(u+v)*87-z
            for j in range(12):
                for i in range(12):
                    p=[point(i,j),point(i+1,j),point(i+1,j+1),point(i,j+1)]
                    fine=3<=i<9 and 3<=j<9
                    color='#5b8e84' if fine else '#384f65'
                    pts=' '.join(f'{a:.1f},{b:.1f}' for a,b in p)
                    card.append(f'<polygon points="{pts}" fill="{color}" fill-opacity=".23" stroke="{MINT if fine else "#7d96b4"}" stroke-opacity=".55" stroke-width=".75"/>')
                    if fine:
                        a,b=p[0],p[2]
                        card.append(f'<path d="M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}" stroke="{MINT}" stroke-opacity=".24"/>')
            card += ['<ellipse cx="282" cy="196" rx="108" ry="38" fill="none" stroke="#b1f4cf" stroke-dasharray="5 6" opacity=".6"/>',
                     '<path d="M282 180v-26" stroke="#edf3ee"/><circle cx="282" cy="180" r="4" fill="#edf3ee"/>',
                     text(246,145,'VIEWER',13,WHITE,mono=True),
                     text(31,142,'COARSE',12,MUTED,mono=True),text(366,268,'FINE',13,MINT,mono=True),
                     text(24,329,'STREAM CHUNKS / REUSE TOPOLOGY',17,MINT,mono=True)]
        elif index==2:
            for cx,label in [(79,'WIDE'),(204,'ULTRAWIDE')]:
                card += [box(cx-46,116,92,88,'#172b33','#628080',9),
                         f'<circle cx="{cx}" cy="157" r="26" fill="#0b151b" stroke="#7a9eab"/><circle cx="{cx}" cy="157" r="15" fill="#1e3c4d" stroke="#b1f4cf"/>',
                         f'<circle cx="{cx-5}" cy="152" r="4" fill="#edf3ee" opacity=".55"/>',
                         text(cx-42,224,label,12,MUTED,mono=True),
                         f'<path d="M{cx} 206L140 273" fill="none" stroke="#87b1a6" stroke-dasharray="4 4"/>']
            card += ['<circle cx="140" cy="273" r="6" fill="#b1f4cf"/>',arrow(267,187,306),
                     box(318,103,218,182,'url(#screen)'),
                     '<g fill="#315f82" opacity=".6"><rect x="335" y="136" width="26" height="32"/><rect x="490" y="124" width="26" height="55"/><rect x="342" y="230" width="38" height="31"/></g>',
                     '<circle cx="425" cy="150" r="23" fill="url(#depth)"/><path d="M398 179Q425 164 452 179L469 252Q425 275 381 252Z" fill="url(#depth)"/>',
                     '<rect x="517" y="147" width="6" height="105" rx="3" fill="url(#depth)"/>',
                     text(332,276,'METRIC DEPTH',12,MUTED,mono=True),text(24,329,'PAIR → RECTIFY → MATCH → FILTER',17,MINT,mono=True)]
        else:
            card += ['<path d="M24 245L150 291L279 237L151 191Z" fill="none" stroke="#32474f"/>',
                     cube(101,155,49,'#a7b2ed'),cube(227,147,39,MINT),
                     '<circle cx="89" cy="187" r="12" fill="#a7b2ed"/><path d="M115 175l12 7v15l-12 7-12-7v-15Z" fill="#a7b2ed" opacity=".6"/>',
                     '<circle cx="224" cy="173" r="10" fill="#b1f4cf"/><path d="M236 187l10 15h-20Z" fill="#b1f4cf" opacity=".65"/>',
                     arrow(285,188,317),box(331,109,205,176),
                     text(346,132,'COLLECTIONS',12,MUTED,mono=True),
                     '<path d="M350 159h11m-6 -5v10M364 160H511M365 170v25h15M365 190h15" stroke="#a7b2ed" stroke-width="2"/>',
                     text(387,182,'Object A',14,WHITE),text(387,203,'Object B',14,MUTED),
                     '<path d="M350 224h11m-6 -5v10M364 225H511M365 235v25h15M365 252h15" stroke="#b1f4cf" stroke-width="2"/>',
                     text(387,247,'Object C',14,WHITE),text(387,268,'Object D',14,MUTED),
                     text(24,329,'POSITION → ZONE → COLLECTION',17,MINT,mono=True)]
        parts += card+['</g>']
    parts.append('</svg>')
    (OUT/('project-systems-mobile.svg' if mobile else 'project-systems.svg')).write_text('\n'.join(parts),encoding='utf-8')

if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--portfolio',type=Path,required=True)
    args=parser.parse_args()
    OUT.mkdir(exist_ok=True)
    for mobile in [False,True]:
        header(mobile)
        showcase(args.portfolio,mobile)
        systems(mobile)
    for f in sorted(OUT.iterdir()):
        if f.is_file(): print(f'{f.name}: {f.stat().st_size:,} bytes')
