# Profile artwork

All profile images are stored in this repository. The README does not depend on image widgets, external badge services, or portfolio image URLs.

- `header*`: a work-led animated banner featuring LUMEN-PS scanning and material maps, SceneBuilder's editor-to-browser export, and Collection Zones' spatial automation. Each workflow holds for four seconds in a 12-second loop. SVG stills support reduced motion. No scripts, external images, or embedded fonts.
- `lumen-showcase*`: composed from the real kiwi leaf relighting animation and recovered albedo, normal, and height previews in Giorgi's portfolio. The original frame durations and all 36 animation frames are preserved. JPEG alternatives are selected for visitors who request reduced motion.
- `lumen-process*`: a 12-second illustrated walkthrough of four scanner captures, registration, photometric stereo, and material-map export. GIFs play in the README; complete SVG stills serve reduced-motion readers.
- `project-systems*`: animated illustrations of WebGL SceneBuilder's synchronized editor/export, MarchingWorld's terrain LOD and Surface Nets cell vertices, Live Stereo Depth's paired observations, and Collection Zones' changing spatial membership. The collection tree uses identical branch geometry for both groups.

These are conceptual diagrams, not application screenshots or measured results. MarchingWorld's illustrative height field shows genuinely different 16×16, 8×8, and 4×4 quad grids, coarse-aligned boundary vertices, and LOD changes around a moving viewer; it is not the project's terrain mesher itself.

The desktop and mobile artwork layouts are selected with native HTML `picture` elements. Narrative text, project descriptions, and links remain ordinary GitHub Markdown.

To rebuild using a local copy of the portfolio, install Pillow and the Node.js `sharp` package, then run:

```powershell
python tools/build_assets.py --portfolio 'E:\CodingProjects\MyPortfolio'
python tools/illustrate_projects.py
python tools/banner_art.py
node tools/render_animations.cjs
python tools/encode_animations.py
```

The builder uses the Windows Segoe UI and Consolas fonts for raster captions. It does not change the source portfolio files. Animation sources and PNG frame renders are kept in the ignored `.preview/animation-frames` directory. Each storyboard is sampled at 8 fps over 12 seconds, with a shared GIF palette and delay rounding that preserves the loop duration. The SVG sources and GIF renders use the same drawing functions.

Content references: [portfolio](https://samukashvili.ge/about.html), [products](https://samukashvili.ge/products.html), [LUMEN-PS](https://github.com/Samukashvili/LUMEN-PS), and the author's public GitHub repositories. Local portfolio pages were also consulted for current project details and the published contact address.
