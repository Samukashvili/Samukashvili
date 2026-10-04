"""Build profile assets: python tools/build_assets.py --portfolio PATH (Pillow required)."""
from argparse import ArgumentParser
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageSequence

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
BG, MINT, WHITE, MUTED = '#0b1218', '#b1f4cf', '#edf3ee', '#9aacb5'

def font(size, bold=False, mono=False):
    name = 'consola.ttf' if mono else 'segoeuib.ttf' if bold else 'segoeui.ttf'
    return ImageFont.truetype(str(Path('C:/Windows/Fonts') / name), size)

def header(mobile=False):
    from banner_art import banner_svg
    (OUT/('header-mobile.svg' if mobile else 'header.svg')).write_text(banner_svg(2.1,mobile),encoding='utf-8')

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

def systems(mobile=False):
    from illustrate_projects import systems_svg, lumen_svg
    suffix='-mobile' if mobile else ''
    (OUT/f'project-systems{suffix}.svg').write_text(systems_svg(3,mobile),encoding='utf-8')
    (OUT/f'lumen-process{suffix}.svg').write_text(lumen_svg(11.5,mobile),encoding='utf-8')

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
