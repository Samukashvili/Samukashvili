"""Work-led banner animation: real project workflows replace decorative geometry."""
from pathlib import Path
import math
from illustrate_projects import text, box, circle, path, group, leaf, rotating_cube, iso_cube, flow, ease, MINT, WHITE, MUTED, BLUE, PURPLE

ROOT=Path(__file__).resolve().parents[1]
BG='#101827'

def project(t):
    stage=int(t//4)%3; local=t%4
    names=['LUMEN-PS','WebGL SceneBuilder','Collection Zones']
    descriptions=['Ordinary scans → relightable materials','Scene editor → standalone WebGL','Objects by position → collections']
    s=text(0,27,f'0{stage+1}',18,MINT,mono=True)+text(46,27,names[stage],27,WHITE,600)
    if stage==0:
        angle=90*int(local)+90*ease((local%1-.8)/.2)
        s+=box(0,65,196,175,'#101e2a','#597782',12)
        s+=box(13,77,170,150,'#172f35','#29464c',5)+leaf(98,151,110,angle)
        sy=92+118*min(1,(local%1)/.8)
        s+=path(f'M18 {sy:.2f}H178',MINT,2)+text(32,262,'ROTATE + SCAN',14,MUTED,mono=True)
        s+=flow(210,153,250,local)
        s+=text(281,58,'MATERIAL MAPS',13,MUTED,mono=True)
        for i,(fill,label) in enumerate([('#789e68','ALBEDO'),('url(#normal)','NORMAL'),('#a3b2b0','HEIGHT'),('#eef3ef','ALPHA')]):
            x=274+(i%2)*111; y=76+(i//2)*102
            s+=box(x,y,97,93,'#121e2d','#304856',7)+leaf(x+48,y+42,72,0,fill)
            s+=text(x+49,y+84,label,10,MUTED,mono=True,anchor='middle')
    elif stage==1:
        yaw=.55+.65*math.sin(local*math.pi/2)
        for x,label in [(0,'EDITOR'),(273,'BROWSER')]:
            s+=box(x,65,196,175,'#111f2d','#4b6978',12)+box(x,65,196,28,'#203144','#4b6978',10)
            s+=text(x+18,84,label,12,MUTED,mono=True)
            s+=''.join(circle(x+148+i*11,79,2.5,'#698b98') for i in range(3))
            s+='<ellipse cx="'+str(x+99)+'" cy="221" rx="52" ry="7" fill="#263f42"/>'
            s+=rotating_cube(x+98,158,36,yaw,BLUE if x==0 else MINT)
        # The editor-only floor grid does not travel into the browser export.
        s+=path('M20 206H177M30 221H167M58 229L98 191L138 229','#38515d',1,opacity=.6)
        s+=flow(210,153,250,local)+text(34,262,'ASSEMBLE + LIGHT',14,MUTED,mono=True)+text(305,262,'EMBED ANYWHERE',14,MUTED,mono=True)
    else:
        s+=path('M0 215L99 260L231 211L132 166Z','#304653')
        s+=iso_cube(67,113,37,PURPLE)+iso_cube(182,113,37,MINT)
        progress=ease(local/1.7) if local<2 else 1-ease((local-2)/1.7)
        in_b=progress>=(182-37-62)/(180-62)
        s+=circle(62+118*progress,143,11,MINT if in_b else PURPLE)+circle(62+118*progress-3,140,2.5,WHITE,.5)
        s+=circle(78,151,7,PURPLE,.5)+circle(195,151,7,MINT,.5)
        s+=flow(232,153,268,local)+box(284,65,185,180,'#101d2b','#4b6978',12)
        s+=text(302,88,'COLLECTIONS',12,MUTED,mono=True)
        for i,(name,color) in enumerate([('Zone A',PURPLE),('Zone B',MINT)]):
            y=111+i*65
            s+=path(f'M302 {y-5}h7l4 3h8v12h-19Z',color,1.3)
            s+=text(330,y+6,name,14,color,600)
            s+=path(f'M310 {y+17}v16h12',color,1.4)
            occupied=(i==1)==in_b
            s+=circle(324,y+33,2.5,color)+text(333,y+38,'Object A' if occupied else '—',13,WHITE if occupied else MUTED)
        s+=text(33,282,'SPATIAL AUTOMATION',14,MUTED,mono=True)
    s+=text(0,318,descriptions[stage],19,WHITE)
    for i in range(3):
        s+=path(f'M{i*163} 344h147','#324250',2)
        if i==stage: s+=path(f'M{i*163} 344h{max(3,147*local/4):.2f}',MINT,2.5)
    return s

def banner_svg(t=2.1,mobile=False):
    w,h=(720,828) if mobile else (1200,470)
    defs='''<defs><linearGradient id="normal"><stop stop-color="#9bbbe9"/><stop offset=".45" stop-color="#b59ce0"/><stop offset="1" stop-color="#81d4d6"/></linearGradient>
    <linearGradient id="back" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#101827"/><stop offset="1" stop-color="#10292f"/></linearGradient></defs>'''
    s=f'<rect width="{w}" height="{h}" rx="16" fill="url(#back)"/>'
    if mobile:
        s+=text(38,46,'COMPUTER VISION / CREATIVE SOFTWARE',17,MINT,mono=True)
        s+=text(35,124,'Giorgi',70,WHITE,600)+text(35,203,'Samukashvili',68,WHITE,600)
        s+=text(38,248,'Software developer',26,MUTED)
        s+=text(38,285,'Python · TypeScript · C# · Java · HLSL',20,MUTED)
        s+=path('M38 310H682','#38505a',1)
        s+=group(project(t),60,326,1.25)
        s+=path('M38 780H682','#38505a',1)
        s+=text(38,808,'TBILISI, GEORGIA',17,MUTED,mono=True)+text(485,808,'samukashvili.ge',17,MINT,mono=True)
    else:
        s+=text(52,62,'COMPUTER VISION / CREATIVE SOFTWARE',16,MINT,mono=True)
        s+=text(48,167,'Giorgi',84,WHITE,600)+text(48,251,'Samukashvili',75,WHITE,600)
        s+=text(52,304,'Software developer',27,MUTED)
        s+=text(52,351,'Python · TypeScript · C# · Java · HLSL',20,MUTED)
        s+=path('M603 50V401','#38505a',1)
        s+=group(project(t),655,54)
        s+=path('M52 421H1148','#38505a',1)
        s+=text(52,452,'TBILISI, GEORGIA',17,MUTED,mono=True)+text(1002,452,'samukashvili.ge',17,MINT,mono=True)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>Giorgi Samukashvili — software that sees, renders, and organizes</title>{defs}{s}</svg>'

def write_frames():
    for mobile in [False,True]:
        stem='header-mobile' if mobile else 'header'
        folder=ROOT/'.preview/animation-frames'/stem
        folder.mkdir(parents=True,exist_ok=True)
        (ROOT/'assets'/f'{stem}.svg').write_text(banner_svg(2.1,mobile),encoding='utf-8')
        for i in range(96): (folder/f'{i:03}.svg').write_text(banner_svg(i/8,mobile),encoding='utf-8')
        print(f'{stem}: 96 workflow frames')

if __name__=='__main__': write_frames()
