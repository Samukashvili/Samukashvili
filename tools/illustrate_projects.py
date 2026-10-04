"""Deterministic SVG storyboards: one shared drawing for preview, stills, and GIFs.

These explain the projects; they are not screenshots or measured reconstruction.
Generate frame sources with this script; render with render_animations.cjs.
"""
from pathlib import Path
import math
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
FRAMES = ROOT / '.preview' / 'animation-frames'
BG, MINT, WHITE, MUTED = '#0b1218', '#b1f4cf', '#edf3ee', '#9aacb5'
BLUE, PURPLE = '#8bbeda', '#b3a6e7'
FPS, SECONDS = 8, 12

def text(x,y,value,size=16,color=WHITE,weight=400,mono=False,anchor='start'):
    family='Consolas, monospace' if mono else 'Segoe UI, Arial, sans-serif'
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'

def box(x,y,w,h,fill=BG,stroke='#30454e',r=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'

def circle(x,y,r,color,opacity=1):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{color}" opacity="{opacity:.3f}"/>'

def path(d,color=MINT,width=1.5,fill='none',opacity=1):
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" opacity="{opacity}" stroke-linejoin="round" stroke-linecap="round"/>'

def group(content,x=0,y=0,scale=1,opacity=1):
    return f'<g transform="translate({x} {y}) scale({scale})" opacity="{opacity}">{content}</g>'

def ease(t):
    t=max(0,min(1,t))
    return t*t*(3-2*t)

def arrow(x,y,end):
    return path(f'M{x} {y}H{end}m-7 -6 7 6-7 6')

def flow(x,y,end,t):
    return arrow(x,y,end)+circle(x+(end-x)*(t%1),y,3.5,MINT)

def svg(w,h,title,body):
    defs='''<defs>
      <linearGradient id="depth" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#5675e2"/><stop offset=".4" stop-color="#67d3db"/><stop offset=".7" stop-color="#b1f4cf"/><stop offset="1" stop-color="#e9c989"/></linearGradient>
      <linearGradient id="normal"><stop stop-color="#99b5ee"/><stop offset=".45" stop-color="#b398e6"/><stop offset="1" stop-color="#82d1da"/></linearGradient>
      <linearGradient id="screen" x2="1" y2="1"><stop stop-color="#17333b"/><stop offset="1" stop-color="#101a24"/></linearGradient>
    </defs>'''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>{defs}<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>{body}</svg>'

def leaf(x,y,size,angle=0,fill='#709d66',opacity=1):
    content=path('M0 -40C31 -31 39 12 0 40C-39 12 -31 -31 0 -40Z',fill,1,fill)
    content+=path('M0 -35V37M0 -20L-14 -12M0 -8L-21 2M0 5L-19 15M0 18L-11 25M0 -20L14 -12M0 -8L21 2M0 5L19 15M0 18L11 25','#e2efce',1,opacity=.42)
    return f'<g transform="translate({x} {y}) rotate({angle}) scale({size/80})" opacity="{opacity}">{content}</g>'

def iso_cube(x,y,size,color):
    d=f'M{x} {y-size*.5}l{size} {size*.5}v{size}l{-size} {size*.5} {-size} {-size*.5}v{-size}Z'
    return path(d,color,1.5,color,.18)+path(d,color,1.5)+path(f'M{x-size} {y}l{size} {size*.5} {size} {-size*.5}M{x} {y+size*.5}v{size}m0 {-size}v{-size}',color,1.5)

def rotating_cube(x,y,size,yaw,color):
    vertices=[]
    for a,b,c in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
        xx=a*math.cos(yaw)-c*math.sin(yaw)
        zz=a*math.sin(yaw)+c*math.cos(yaw)
        vertices.append((x+xx*size,y+b*size*.8+zz*size*.25))
    edges=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
    return ''.join(path(f'M{vertices[a][0]:.2f} {vertices[a][1]:.2f}L{vertices[b][0]:.2f} {vertices[b][1]:.2f}',color,1.5) for a,b in edges)

def scenebuilder(t):
    yaw=.55+.7*math.sin(t*math.tau/12)
    s=box(24,122,248,205)+box(24,122,248,27,'#1c2932')
    s+=text(35,140,'scene.editor',12,MUTED,mono=True)+circle(250,135,3,MINT)
    s+=box(35,159,62,154,'#121d25','#26353e',3)+text(44,178,'SCENE',10,MUTED,mono=True)
    s+=path('M46 197H83M53 214H83M53 231H76M46 270H81M46 292H69','#577581',3)
    s+=box(107,159,154,154,'url(#screen)','#26353e',3)
    s+=path('M109 281H259M109 298H259M143 313L179 252L213 313','#426065',1,opacity=.55)
    s+=rotating_cube(184,224,32,yaw,BLUE)
    slider=48+30*(.5+.5*math.sin(t*math.tau/12))
    s+=circle(slider,292,3,MINT)+flow(284,229,311,t/2)
    s+=box(323,132,213,180)+box(323,132,213,26,'#1c2932')
    s+=''.join(circle(x,145,3,'#74938e') for x in [337,347,357])+text(387,150,'your.site',11,MUTED,mono=True)
    s+='<ellipse cx="430" cy="280" rx="57" ry="8" fill="#244940" opacity=".4"/>'
    s+=rotating_cube(430,221,36,yaw,MINT)+text(345,298,'self-contained bundle',12,MUTED,mono=True)
    s+=text(24,360,'Editor and export, in sync',16,MUTED)
    s+=text(24,405,'EDIT → OPTIMIZE → EXPORT',17,MINT,mono=True)
    return s

def terrain_point(u,v):
    z=105*math.exp(-((u-.7)**2/.23+(v-1.7)**2/.42))
    z+=78*math.exp(-((u-2.35)**2/.36+(v-.8)**2/.26))
    z-=30*math.exp(-((u-1.5)**2/.25+(v-1.25)**2/.6))
    z+=7*math.sin(u*4+v*2)
    return (282+(u-v)*75,134+(u+v)*24-z*.56,z)

def marchingworld(t):
    # Schematic Surface Nets-style quad terrain, not a capture of the real mesher.
    viewer_u=1.5+.9*math.sin(t*math.tau/12)
    viewer_v=1.4+.35*math.cos(t*math.tau/12)
    cx,cy=int(viewer_u),int(viewer_v)
    resolutions={(i,j):(16 if (i,j)==(cx,cy) else 8 if abs(i-cx)+abs(j-cy)==1 else 4) for j in range(3) for i in range(3)}
    s=''
    colors={16:MINT,8:BLUE,4:PURPLE}
    def stitched(i,j,a,b,n):
        u,v=i+a/n,j+b/n
        # Fine boundary vertices lie on the neighboring coarse edge segments.
        neighbor=None; coordinate=None; along_u=False
        if a==0 and i>0: neighbor=(i-1,j); coordinate=b/n
        elif a==n and i<2: neighbor=(i+1,j); coordinate=b/n
        elif b==0 and j>0: neighbor=(i,j-1); coordinate=a/n; along_u=True
        elif b==n and j<2: neighbor=(i,j+1); coordinate=a/n; along_u=True
        if neighbor and resolutions[neighbor]<n:
            coarse=resolutions[neighbor]
            k=min(coarse-1,int(coordinate*coarse)); f=coordinate*coarse-k
            p=terrain_point(i+k/coarse,v) if along_u else terrain_point(u,j+k/coarse)
            q=terrain_point(i+(k+1)/coarse,v) if along_u else terrain_point(u,j+(k+1)/coarse)
            return tuple(p[k]*(1-f)+q[k]*f for k in range(3))
        return terrain_point(u,v)
    for i,j in sorted(resolutions,key=lambda ij:sum(ij)):
        n=resolutions[i,j]; color=colors[n]
        for b in range(n):
            for a in range(n):
                points=[stitched(i,j,a,b,n),stitched(i,j,a+1,b,n),stitched(i,j,a+1,b+1,n),stitched(i,j,a,b+1,n)]
                height=sum(p[2] for p in points)/4
                shade=max(0,min(1,(height+30)/145))
                fill='#%02x%02x%02x'%(int(28+shade*35),int(49+shade*53),int(54+shade*49))
                pts=' '.join(f'{x:.2f},{y:.2f}' for x,y,_ in points)
                s+=f'<polygon points="{pts}" fill="{fill}" stroke="{color}" stroke-opacity=".48" stroke-width=".6"/>'
        corners=[terrain_point(i,j),terrain_point(i+1,j),terrain_point(i+1,j+1),terrain_point(i,j+1)]
        # Use sampled perimeter rather than a straight outline across the hills.
        edge=[stitched(i,j,k,0,n) for k in range(n+1)]+[stitched(i,j,n,k,n) for k in range(1,n+1)]+[stitched(i,j,k,n,n) for k in range(n-1,-1,-1)]+[stitched(i,j,0,k,n) for k in range(n-1,-1,-1)]
        s+=path('M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y,_ in edge)+'Z',color,1.4)
    vx,vy,_=terrain_point(viewer_u,viewer_v)
    s+=path(f'M{vx:.2f} {vy:.2f}v-28',WHITE,1)+circle(vx,vy,4,WHITE)
    s+=text(vx-25,vy-35,'VIEWER',12,WHITE,mono=True)
    s+=box(24,281,194,97,'#0c151d','#30454e',6)
    for x,y in [(69,310),(105,326),(105,294),(141,310)]: s+=iso_cube(x,y,18,'#526e82')
    points=[(72,311),(107,326),(140,311),(105,295)]
    s+=path('M'+'L'.join(f'{x} {y}' for x,y in points)+'Z',MINT,2.5)
    s+=''.join(circle(x,y,3.5,MINT) for x,y in points)
    s+=text(40,365,'CELL VERTICES → QUADS',12,MUTED,mono=True)
    s+=text(240,295,'SURFACE NETS',19,WHITE,600)
    s+=text(240,318,'One vertex per active cell',14,MUTED)
    for k,(n,label) in enumerate([(16,'16×16'),(8,'8×8'),(4,'4×4')]):
        s+=circle(246+k*94,345,3,colors[n])+text(255+k*94,351,label,15,colors[n],mono=True)
    s+=text(240,376,'Stitched chunk boundaries',14,MUTED)
    s+=text(24,405,'STREAM → SELECT LOD → REUSE TOPOLOGY',16,MINT,mono=True)
    return s

def stereo(t):
    phase=t/2%1
    pulse=.6+.4*math.sin(t*math.tau/2)**2
    s=''
    for cx,label in [(79,'WIDE'),(204,'ULTRAWIDE')]:
        s+=box(cx-46,139,92,88,'#172b33','#628080',9)
        s+=circle(cx,180,26,BG)+circle(cx,180,15,'#1e3c4d')
        s+=f'<circle cx="{cx}" cy="180" r="26" fill="none" stroke="{MINT}" opacity="{pulse}"/>'
        s+=circle(cx-5,175,4,WHITE,.6)+text(cx-42,248,label,12,MUTED,mono=True)
        s+=path(f'M{cx} 230L140 302','#87b1a6',1,opacity=.5)
        s+=circle(cx+(140-cx)*phase,230+72*phase,3,MINT)
    s+=circle(140,302,6,MINT)+flow(267,208,306,t/2)
    s+=box(318,126,218,210,'url(#screen)')
    s+='<g fill="#315f82" opacity=".6"><rect x="335" y="159" width="26" height="32"/><rect x="490" y="147" width="26" height="55"/><rect x="342" y="275" width="38" height="31"/></g>'
    dx=12*math.sin(t*math.tau/6)
    silhouette=circle(425+dx,176,23,'url(#depth)')+path(f'M{398+dx} 205Q{425+dx} 190 {452+dx} 205L{469+dx} 291Q{425+dx} 312 {381+dx} 291Z','none',0,'url(#depth)')
    s+=silhouette+f'<rect x="517" y="171" width="6" height="127" rx="3" fill="url(#depth)"/>'
    s+=path(f'M330 {147+(t/4%1)*155:.2f}H506',MINT,1,opacity=.35)
    s+=text(332,324,'METRIC DEPTH',12,MUTED,mono=True)
    s+=text(24,362,'Paired views → dense correspondence',15,MUTED)
    s+=text(24,405,'PAIR → RECTIFY → MATCH → FILTER',17,MINT,mono=True)
    return s

def folder(x,y,color):
    return path(f'M{x} {y+3}v-8h7l3 3h10v14h-20Z',color,1.3,color,.2)+path(f'M{x} {y+3}v-8h7l3 3h10v14h-20Z',color,1.3)

def hierarchy(x,y,name,color,first,second,active):
    # Identical geometry for both groups: equal branch lengths and row spacing.
    s=folder(x,y,color)+text(x+28,y+6,name,14,color,600)
    s+=path(f'M{x+9} {y+17}V{y+48}M{x+9} {y+28}H{x+21}M{x+9} {y+48}H{x+21}',color,1.4)
    s+=circle(x+23,y+28,2.5,color)+circle(x+23,y+48,2.5,color)
    s+=text(x+32,y+33,first,13,WHITE if active else MUTED)
    s+=text(x+32,y+53,second,13,WHITE)
    return s

def zones(t):
    progress=ease((t%12-2)/3) if t%12<7 else 1-ease((t%12-8)/3)
    in_b=progress>.7
    s=path('M24 287L150 333L279 279L151 233Z','#32474f')
    s+=iso_cube(101,197,49,PURPLE)+iso_cube(227,189,39,MINT)
    s+=circle(115,231,9,PURPLE,.6)+path('M237 216l10 16h-20Z',MINT,1,MINT,.65)
    x=89+(224-89)*progress; y=229+(216-229)*progress
    s+=circle(x,y,12,MINT if in_b else PURPLE)+circle(x-3,y-4,3,WHITE,.45)
    s+=flow(285,230,317,t/2)+box(331,129,205,211)
    s+=text(346,152,'COLLECTIONS',12,MUTED,mono=True)
    s+=hierarchy(346,176,'Zone A',PURPLE,'Object A' if not in_b else '—','Object B',not in_b)
    s+=hierarchy(346,259,'Zone B',MINT,'Object A' if in_b else '—','Object C',in_b)
    s+=text(24,364,'Object A moves → membership updates',15,MUTED)
    s+=text(24,405,'POSITION → ZONE → COLLECTION',17,MINT,mono=True)
    return s

def systems_svg(t=3,mobile=False):
    w,h=(720,2190) if mobile else (1200,974)
    s=text(26,38,'THE SYSTEMS BEHIND THE SOFTWARE',20,MINT,mono=True)
    cards=[('WebGL SceneBuilder','TYPESCRIPT / WEBGL',scenebuilder),('MarchingWorld','C# / HLSL / UNITY',marchingworld),('Live Stereo Depth','JAVA / OPENGL ES',stereo),('Collection Zones','PYTHON / BLENDER',zones)]
    positions=[(24,70+i*527) for i in range(4)] if mobile else [(24,72),(616,72),(24,522),(616,522)]
    for (title,stack,draw),(x,y) in zip(cards,positions):
        content=box(0,0,560,430,'#111a22','#26383f',12)+text(24,38,title,27,weight=600)+text(24,67,stack,15,MUTED,mono=True)+draw(t)
        s+=group(content,x,y,1.2 if mobile else 1)
    return svg(w,h,'Animated systems: editor export, Surface Nets LOD, stereo reconstruction, spatial collections',s)

def lumen_svg(t=11.5,mobile=False):
    w,h=(720,884) if mobile else (1200,430)
    s=text(26,38,'LUMEN-PS / FOUR SCANS → MATERIAL MAPS',20,MINT,mono=True)
    phase=0 if t<6 else 1 if t<8 else 2 if t<10 else 3
    positions=[(24,70),(371,70),(24,474),(371,474)] if mobile else [(24+i*296,70) for i in range(4)]
    labels=['01 / CAPTURE','02 / ALIGN','03 / SOLVE','04 / EXPORT']
    for k,(x,y) in enumerate(positions):
        c=box(0,0,266,330,'#111a22',MINT if phase==k else '#26383f',10)+text(18,32,labels[k],19,MINT,mono=True)
        if k==0:
            step=min(3,int(t/1.5))
            current=t%1.5
            angle=step*90+90*ease((current-1.20)/.30) if t<6 else 0
            c+=box(18,65,230,155,'#0b151d','#4d6773')+box(29,78,208,129,'#14262a','#324b4e',2)
            c+=leaf(133,145,96,angle)
            scan_y=85+117*min(1,current/1.15) if t<6 else 112
            c+=path(f'M32 {scan_y:.2f}H234',MINT,2,opacity=1 if phase==0 else .25)
            c+=text(42,244,'FIXED SCANNER LIGHT',13,MUTED,mono=True)
            c+=''.join(text(43+i*57,279,f'{angle}°',16,WHITE,mono=True,anchor='middle') for i,angle in enumerate([0,90,180,270]))
            c+=''.join(circle(43+i*57,296,3.5,MINT if (i<=step or t>=6) else '#3b4b51') for i in range(4))
        elif k==1:
            alignment=ease((t-6)/2)
            for i,color in enumerate([MINT,BLUE,PURPLE,'#e2c994']):
                dx=(i-1.5)*18*(1-alignment); dy=math.sin(i)*16*(1-alignment)
                c+=leaf(133+dx,151+dy,113,(i-1.5)*12*(1-alignment),color,.18)
                c+=group(path('M0 -40C31 -31 39 12 0 40C-39 12 -31 -31 0 -40Z',color,1.2),133+dx,151+dy,113/80)
            c+=text(31,250,'Same surface point.',17,WHITE)+text(31,279,'Four light directions.',17,MUTED)
        elif k==2:
            c+=leaf(133,146,126,0,'url(#normal)')
            for i in range(4):
                a=i*math.pi/2
                xx,yy=133+91*math.cos(a),146+91*math.sin(a)
                c+=circle(xx,yy,4,[MINT,BLUE,PURPLE,'#e2c994'][i])
                c+=path(f'M{xx:.2f} {yy:.2f}L{133+30*math.cos(a):.2f} {146+30*math.sin(a):.2f}',[MINT,BLUE,PURPLE,'#e2c994'][i],1,opacity=.6)
                q=(t/1.5+i*.25)%1
                if phase==2: c+=circle(xx+(133-xx)*q,yy+(146-yy)*q,2.5,WHITE)
            c+=text(27,265,'I = ρ max(N · L, 0)',17,WHITE,mono=True)+text(27,296,'Separate color & relief',14,MUTED)
        else:
            tiles=[('ALBEDO','#709d66'),('NORMAL','url(#normal)'),('ROUGHNESS','#cad0ca'),('HEIGHT','#a2ada9'),('ALPHA',WHITE)]
            for i,(name,fill) in enumerate(tiles):
                xx=19+(i%3)*79; yy=81+(i//3)*109
                opacity=1 if t>=10+i*.3 else .25
                tile=box(xx,yy,70,72,'#0b151d','#30454e',4)+leaf(xx+35,yy+34,54,0,fill)+text(xx+1,yy+91,name,11,MUTED,mono=True)
                c+=f'<g opacity="{opacity}">{tile}</g>'
            c+=text(22,314,'READY TO RELIGHT',15,MINT,mono=True)
        s+=group(c,x,y,1.21 if mobile else 1)
    return svg(w,h,'LUMEN-PS: rotate and scan four times, align, solve photometric stereo, export material maps',s)

def write_frames():
    OUT.mkdir(exist_ok=True); FRAMES.mkdir(parents=True,exist_ok=True)
    for name,draw in [('project-systems',systems_svg),('lumen-process',lumen_svg)]:
        for mobile in [False,True]:
            suffix='-mobile' if mobile else ''
            stem=name+suffix
            # Choose an informative complete composition for reduced motion.
            (OUT/f'{stem}.svg').write_text(draw(11.5 if name=='lumen-process' else 3,mobile),encoding='utf-8')
            folder=FRAMES/stem; folder.mkdir(exist_ok=True)
            for i in range(FPS*SECONDS):
                (folder/f'{i:03}.svg').write_text(draw(i/FPS,mobile),encoding='utf-8')
            print(f'{stem}: {FPS*SECONDS} source frames')

if __name__=='__main__': write_frames()
