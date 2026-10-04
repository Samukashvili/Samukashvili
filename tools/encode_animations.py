"""Encode deterministic SVG renders into GitHub-friendly GIF animations (Pillow)."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parents[1]
for name in ['lumen-process','lumen-process-mobile','project-systems','project-systems-mobile']:
    sources=sorted((ROOT/'.preview/animation-frames'/name).glob('[0-9][0-9][0-9].png'))
    assert len(sources)==96, f'{name}: expected the complete 12-second storyboard'
    # Build one palette from the whole loop so colors never change between frames.
    board=Image.new('RGB',(1200,1200),'#0b1218')
    for i,source in enumerate(sources[::3]):
        with Image.open(source) as im:
            sample=ImageOps.contain(im.convert('RGB'),(200,200),Image.Resampling.LANCZOS)
            board.paste(sample,((i%6)*200,(i//6)*200))
    palette=board.quantize(colors=256)
    frames=[]
    for source in sources:
        with Image.open(source) as im:
            # Flat graphic colors need no error diffusion across moving edges.
            frames.append(im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE))
    target=ROOT/'assets'/f'{name}.gif'
    # GIF delay precision is 10 ms: alternating delays preserve an 8 fps loop.
    durations=[120 if i%2==0 else 130 for i in range(len(frames))]
    frames[0].save(target,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=1,optimize=True)
    print(f'{target.name}: {target.stat().st_size:,} bytes')
