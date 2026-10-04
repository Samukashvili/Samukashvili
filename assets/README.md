# Profile artwork

All profile images are stored in this repository. The README does not depend on image widgets, external badge services, or portfolio image URLs.

- `header.svg` and `header-mobile.svg`: original procedural graphics created for this profile. No scripts, external images, or embedded fonts.
- `lumen-showcase*`: composed from the real kiwi leaf relighting animation and recovered albedo, normal, and height previews in Giorgi's portfolio. The original frame durations and all 36 animation frames are preserved. JPEG alternatives are selected for visitors who request reduced motion.
- `project-systems*`: original SVG illustrations of WebGL SceneBuilder's editor/export workflow, MarchingWorld's terrain LOD, Live Stereo Depth's dual-camera reconstruction, and Collection Zones' spatial grouping. These are conceptual diagrams, not application screenshots or measured results.

The desktop and mobile artwork layouts are selected with native HTML `picture` elements. Narrative text, project descriptions, and links remain ordinary GitHub Markdown.

To rebuild using a local copy of the portfolio, install Pillow and run:

```powershell
python tools/build_assets.py --portfolio 'E:\CodingProjects\MyPortfolio'
```

The builder uses the Windows Segoe UI and Consolas fonts for raster captions. It does not change the source portfolio files.

Content references: [portfolio](https://samukashvili.ge/about.html), [products](https://samukashvili.ge/products.html), [LUMEN-PS](https://github.com/Samukashvili/LUMEN-PS), and the author's public GitHub repositories. Local portfolio pages were also consulted for current project details and the published contact address.
