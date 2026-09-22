# UI THEME SPECIFICATION & MASTER PROMPT ARTIFACTS

This document archives all verified design system prompts, CSS tokens, and component specifications across the Karmic Ledger interface generations.

### Catalog of Master Themes:
1. **Observatory Dark Mode** (Minimal Celestial HUD & Glassmorphism)
2. **Vedic Temple Carving** (Sandstone Bas-Relief & Chiseled Gold Shastra)
3. **Swiss Grid Minimal** (International Typographic Style & Stark Monochrome)
4. **CRT Retro Terminal** (Phosphor Green Terminal, Scanlines & BIOS Boot)
5. **Illuminated Star Chart** (Antique Celestial Atlas, Copper Engravings & Armillary Sphere)
6. **Zen Paper Minimal** (Washi Rice-Paper, Sumi Ink Hairlines, Vermilion Hanko Seal & Dark Kuro-Washi Option)
7. **Cyber-Sacred Hybrid** (Cyberpunk HUD, Sacred Iconography, Gold Circuit Mandalas, Glitch-in Text Reveal & Rotating Yantra Canvas)

---

# OBSERVATORY DARK MODE // UI THEME SPECIFICATION & PROMPT ARTIFACT

> **System Aesthetic:** Minimal Astronomy Observatory / Celestial Reticle HUD  
> **Classification:** High-signal, sci-fi pro-lite, dark celestial glassmorphism

---

## 1. Master Generation Prompt

```text
Observatory Dark Mode
"Build minimal astronomy-observatory website, deep navy background, star-field parallax on scroll, constellation line-connect animations, silver/white typography, telescope-lens circular UI elements."
```

### Extended System Architecture Prompt
```text
Build a minimal, high-precision astronomy-observatory web application:
- Palette: Deep cosmic navy (#030712 / #060d24), stellar cyan accents (#38bdf8), silver/white typography (#f8fafc / #e2e8f0), subtle glass borders.
- Background: Interactive full-screen canvas starfield with multi-layer scroll parallax, twinkling luminance, and dynamic constellation line-connections between nearby stars (< 75px threshold).
- Component Aesthetics: Circular telescope-barrel lenses, crosshair reticles, optical aperture cards with glassmorphism (backdrop-filter: blur(12px)), thin cyan telemetry badges.
- Typography: Clean sans-serif headers (Inter / Space Grotesk) paired with stark high-contrast monospace (JetBrains Mono / Space Mono) for planetary coordinates, degrees, and ephemeris tables.
- Layout: Modular observation sectors (01 Coordinates Manifest, 02 Jaimini Reticle, 03 Stoppage Transit Console, 04 Adversarial Falsification Battery, 04B Karl Popper Comparator, 05 D-1 Telescope Kundli, 06 Dasha Lifespan Horizon, 07 VCS Milestone Matrix, 08 Shastra Protocols).
```

---

## 2. Design System Tokens & CSS Variables

```css
:root {
  /* Background & Celestial Surface */
  --obs-bg-deep: #030712;
  --obs-bg-nebula: #060d24;
  --obs-bg-void: #020510;
  --card-bg-glass: rgba(15, 23, 42, 0.75);
  
  /* Telemetry Accents */
  --stellar-cyan: #38bdf8;
  --stellar-cyan-glow: rgba(56, 189, 248, 0.35);
  --alert-crimson: #f43f5e;
  --alert-crimson-glow: rgba(244, 63, 94, 0.4);
  
  /* Typography */
  --text-pure: #ffffff;
  --text-silver: #f1f5f9;
  --text-muted: #94a3b8;
  --text-dim: #64748b;
  
  /* Borders & Reticles */
  --border-subtle: rgba(148, 163, 184, 0.18);
  --border-silver: rgba(226, 232, 240, 0.35);
  --border-lens: rgba(56, 189, 248, 0.5);

  /* Fonts */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'Space Mono', Menlo, Consolas, monospace;
}
```

---

## 3. Core Visual Components

### A. Dynamic Celestial Canvas (Parallax & Constellation Connect)
- Fullscreen fixed `z-index: 0` canvas.
- 220 star particles distributed across 3 depth velocity layers for scroll parallax.
- Euclidean distance calculation connects pairs closer than 75px with dynamic alpha line segments: `rgba(56, 189, 248, (1 - dist/75) * 0.14)`.

### B. Telescope Circular Lens Reticles
- Circular component housing with dual reticle rings (`border-radius: 50%`).
- Centered optical crosshairs (`::before` / `::after` dashed lines).
- Central digital readout for continuous metrics (e.g. Soul Antiquity Index, Degree Odometer).

### C. Optical Aperture Cards
- `background: rgba(15, 23, 42, 0.75)`
- `backdrop-filter: blur(12px)`
- `border: 1px solid rgba(226, 232, 240, 0.35)` with hover elevation to `--stellar-cyan`.
- Header layout featuring sector numbering and cyan telemetry status pills.

### D. Karl Popper Falsifiability Split Comparator (Sector 04B)
- Two-card side-by-side comparison layout:
  - Left: Observed Ground Truth (Cyan border / badge, verified 98.0% VCS).
  - Right: Corrupted Adversarial Fraud (Crimson border / badge, collapsed 24.0% VCS).
- Instant tab switcher: `[Side-by-Side Optical Comparison]`, `[Ground Truth Only]`, `[Adversarial Fraud Only]`.

---

# VEDIC TEMPLE CARVING // UI THEME SPECIFICATION & PROMPT ARTIFACT

> **System Aesthetic:** Ancient Stone Temple Carving / Khajuraho Bas-Relief / Gold-Inlaid Shastra Stele  
> **Classification:** High-signal, Vedic astronomical gravitas, chisel-cut serif typography, basalt & sandstone relief

---

## 1. Master Generation Prompt

```text
Vedic Temple Carving
"Build website styled like stone temple carving, sandstone texture background, bas-relief border patterns, deep maroon/gold palette, chisel-cut typography feel, slow stone-reveal scroll animation."
```

### Extended System Architecture Prompt
```text
Build a ceremonial yet rigorously scientific Vedic temple carving web application:
- Palette: Sedimentary Sandstone Bedrock (#110905 / #1c120b / #281911), Sacred Deep Maroon (#250707 / #3b0c0c / #521212), Antique Temple Gold (#c59b27 / #d4af37 / #fbbf24), Incised Stone White (#e8d8c8 / #f5ede4).
- Background: Interactive full-screen canvas rendering deep sandstone strata, subtle rotating Sri Yantra / Ashta Dikpala concentric sacred geometry (rgba(212, 175, 55, 0.035)), and upward-drifting amber gold-leaf incense embers with gentle sinusoidal sway.
- Bas-Relief Borders & Chisel-Cut Effects: Stepped multi-layer box shadows simulating chiseled relief (inset 1.5px highlight, inset -2.5px deep shadow, exterior drop shadows).
- Chisel-Cut Typography: Google Fonts Cinzel Decorative (Grand Titles), Cinzel (Subheaders & Labels), Marcellus (Editorial Body), Martel (Numerals & Data). Text shadows apply upper-left chisel highlight (rgba(255,235,205,0.22)) and lower-right basalt incision (-1px -1px 2px #000).
- Slow Stone-Reveal Scroll Animation: Cards start with low brightness, high contrast, slight downward displacement and blur, smoothly resolving into sharp, warm carved stone upon viewport intersection via IntersectionObserver (1.1s cubic-bezier(0.16, 1, 0.3, 1)).
- Component Aesthetics: Circular Surya Yantra dial with Ashta Dikpala cardinal ticks, carved stone plinths for control surfaces, gold-bordered shastra tablets, and temple oil lamp (diya) pulsing indicator dots.
```

---

## 2. Design System Tokens & CSS Variables

```css
:root {
  /* Sandstone Sedimentary Bedrock */
  --bg-sandstone-dark: #110905;
  --bg-sandstone-slab: #1c120b;
  --bg-sandstone-card: #24160e;
  --bg-sandstone-lift: #2e1c12;
  
  /* Sacred Deep Maroon & Kumkuma */
  --maroon-deep: #250707;
  --maroon-rich: #3b0c0c;
  --maroon-bright: #521212;
  
  /* Antique Temple Gold & Brass */
  --gold-antique: #c59b27;
  --gold-radiant: #d4af37;
  --gold-leaf: #fbbf24;
  --gold-highlight: #ffebb3;
  --gold-glow: rgba(212, 175, 55, 0.28);
  
  /* Bas-Relief Stone Borders & Shadows */
  --border-relief-stone: #422a1b;
  --border-relief-dark: #0a0503;
  --stone-chisel-high: rgba(255, 235, 205, 0.18);
  --stone-shadow-deep: rgba(0, 0, 0, 0.85);
  
  /* Chiseled Typography Palette */
  --stone-light: #f5ede4;
  --stone-incised: #e8d8c8;
  --stone-muted: #bda692;
  --stone-dim: #7d6b5c;
  
  /* Vedic Alert Accents */
  --alert-crimson: #ef4444;
  --alert-crimson-bg: rgba(69, 10, 10, 0.85);

  /* Chisel-Cut Typography System */
  --font-ornate: 'Cinzel Decorative', 'Cinzel', Georgia, serif;
  --font-display: 'Cinzel', 'Trajan Pro', Georgia, serif;
  --font-body: 'Marcellus', 'Martel', Georgia, serif;
  --font-label: 'Martel', 'Georgia', serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

---

## 3. Core Visual Components

### A. Dynamic Sandstone Bedrock & Sacred Yantra Canvas
- Fullscreen canvas rendering dark sandstone bedrock strata (`#0c0603` to `#180f0a`).
- Slowly rotating Sri Yantra concentric rings and 8-fold Ashta Dikpala cardinal rays in ultra-faint gold leaf.
- 110 upward-drifting amber gold incense embers and diya sparks with sinusoidal sway and parallax depth.

### B. Bas-Relief Stele Cards (`.stone-reveal-card`)
- Multi-layer bas-relief border system:
  `box-shadow: inset 1.5px 1.5px 0px var(--stone-chisel-high), inset -2.5px -2.5px 0px var(--border-relief-dark), 0 14px 40px rgba(0, 0, 0, 0.95);`
- Golden inscribed inner border frame via `::before` pseudo-element.
- IntersectionObserver triggers `.revealed` with smooth 1.1s stone-reveal transition.

### C. Surya Yantra Circular Kundli Housing
- Circular 420x420 carved plinth with concentric basalt rings and antique gold leaf trim.
- Reskinned Kundli diamond SVG and 120-year Vimshottari dasha SVG embedded with sandstone bedrock and gold Kendra accents.

### D. Karl Popper Falsifiability Bas-Relief Comparator (Sector 04B)
- Split comparison between Observed Ground Truth (Gold/amber bas-relief badge, 98% VCS) and Adversarial Fraud (+3 yrs shift, deep crimson relief, 24% VCS).
- Explains the mathematical falsifiability criterion: lying about the birth epoch collapses house lordship and aspectual confluence.

---

# SWISS GRID MINIMAL // UI THEME SPECIFICATION & PROMPT ARTIFACT

> **System Aesthetic:** International Typographic Style (Swiss Style / Josef Müller-Brockmann)  
> **Classification:** Ultra-minimalist, mathematical grid, high whitespace, stark monochrome with single Swiss Red accent

---

## 1. Master Generation Prompt

```text
6. Swiss Grid Minimal
"Build ultra-minimal Swiss-design website, white background, black grid lines, one accent color only, huge whitespace, Helvetica/Inter typography, no decoration, subtle fade transitions only."
```

### Extended System Architecture Prompt
```text
Build an ultra-minimal, high-precision Swiss-design web application:
- Palette: Pure White (#ffffff), Architectural Black (#000000), Slate Gray (#52525b / #71717a), Light Surface (#f4f4f5), and exactly ONE accent color: Swiss Red (#eb0028).
- Grid System: Stark 1px pure black borders, table-like modular layout, zero border-radius (border-radius: 0), zero gradients, zero box-shadows, zero drop-shadows.
- Typography: Helvetica / Inter typography with extreme weight contrasts (ExtraBold 800/900 for numbers and headings, Regular 400 for text, JetBrains Mono for exact ephemeris numbers). Tight tracking (-0.03em).
- Whitespace: Massive, deliberate whitespace with asymmetric mathematical alignment.
- Transitions: Subtle fade transitions only (transition: opacity 0.2s ease, background-color 0.15s ease).
- Visual Elements: Clean Kundli diamond chart drawn in crisp 1.5px black lines on pure white, with a single Swiss red center gnomon and active mark.
```

---

## 2. Design System Tokens & CSS Variables

```css
:root {
  /* Swiss Grid Palette */
  --swiss-bg: #ffffff;
  --swiss-surface: #fafafa;
  --swiss-surface-subtle: #f4f4f5;
  --swiss-black: #000000;
  --swiss-charcoal: #18181b;
  --swiss-text-secondary: #52525b;
  --swiss-text-muted: #71717a;
  --swiss-border-hairline: #e4e4e7;
  --swiss-border-strong: #000000;

  /* Single Accent Color: Swiss Red (RAL 3020) */
  --swiss-red: #eb0028;
  --swiss-red-subtle: rgba(235, 0, 40, 0.06);

  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-mono: 'JetBrains Mono', 'Space Mono', monospace;
}
```

---

## 3. Core Visual Components

### A. Modular Grid Framing
- Strict 1px solid black bounding boxes with `border-collapse: collapse`.
- Huge numbers (`01`, `02`, `03`) set in 52px+ heavy Helvetica/Inter bold next to clean subheadings.
- Clean rectangular tabular data with no rounded pill shapes.

### B. High-Contrast Target Switcher & Action Plinths
- Flat white rectangular buttons with crisp `1px solid #000000`.
- Active state inverts to solid black (`background: #000000; color: #ffffff`).
- Single accent red indicator for primary CTA: `[⚡ Run Adversarial Falsification Battery]`.

### C. Kundli & Dasha Architectural SVGs
- Reskinned to pure white canvas, 1px crisp black strokes, sans-serif labels, and a single `#eb0028` red focal marker.

### D. Karl Popper Falsifiability Grid (Sector 04B)
- Asymmetrical 2-column mathematical grid comparing Ground Truth (clean black bordered card with red verified stamp) against Adversarial Fraud (invert black/charcoal card with stark warning header).

---

# CRT RETRO TERMINAL // UI THEME SPECIFICATION & PROMPT ARTIFACT

> **System Aesthetic:** Vintage Cathode Ray Tube Terminal / P31 Green Phosphor / Cyberpunk Mainframe  
> **Classification:** High-signal retrocomputing, phosphor decay glow, hardware scanlines, curvature vignette, boot BIOS

---

## 1. Master Generation Prompt

```text
CRT Retro Terminal
"Build retro CRT-monitor website, green phosphor text on black, scanline overlay, screen-curvature vignette, flicker animation, boot-sequence intro animation, monospace font, terminal cursor blink."
```

### Extended System Architecture Prompt
```text
Build a retro CRT-monitor terminal web application:
- Palette: Deep cathode black (#030803 / #050a05), intense green phosphor (#00ff66 / #33ff33), dim terminal phosphor (#00772e / #004419), and amber warning phosphor (#ffb000 / #ff3333).
- Effects: Hardware scanlines overlay (repeating linear gradient), screen curvature vignette (radial barrel distortion), subtle phosphor refresh flicker (120ms cycle), and glowing text shadows (0 0 6px rgba(0, 255, 102, 0.6)).
- Boot Sequence: Authentic retro BIOS / terminal boot sequence typing out memory checks, Swiss Ephemeris subsystem mounting, and shastra matrix initialization before revealing the interactive console.
- Typography: Authentic monospace (Share Tech Mono, VT323, JetBrains Mono) with blinking block/underscore terminal cursor (_ / █).
- Interactive Elements: Terminal command prompts, bracketed ASCII frames [== SECTOR 01 ==], inverted green phosphor buttons on focus/hover, and retro telemetry tables.
- Vector Graphics: Phosphor green vector Kundli diamond charts and Vimshottari dasha progress bars with glowing neon lines on deep cathode backdrops.
```

---

## 2. Design System Tokens & CSS Variables

```css
:root {
  /* CRT Phosphor Palette */
  --crt-bg: #030803;
  --crt-screen-bg: #050b05;
  --crt-surface: #041004;
  --crt-surface-subtle: #061806;
  --crt-green: #00ff66;
  --crt-green-bright: #33ff77;
  --crt-green-dim: #008f33;
  --crt-green-dark: #004d1a;
  --crt-green-glow: 0 0 6px rgba(0, 255, 102, 0.6), 0 0 12px rgba(0, 255, 102, 0.25);
  
  /* Amber / Alert Phosphor */
  --crt-amber: #ffb000;
  --crt-amber-glow: 0 0 6px rgba(255, 176, 0, 0.7);
  --crt-red: #ff3333;
  --crt-red-glow: 0 0 6px rgba(255, 51, 51, 0.7);

  /* Borders & Grid */
  --crt-border: 1px solid #00ff66;
  --crt-border-dim: 1px solid #00551a;
  --crt-border-glow: 0 0 8px rgba(0, 255, 102, 0.4);

  /* Typography */
  --font-mono: 'Share Tech Mono', 'VT323', 'JetBrains Mono', monospace;
}
```

---

## 3. Core Visual Components

### A. Cathode Screen Curvature & Scanlines
- Global fixed scanlines overlay (`pointer-events: none`) simulating phosphor raster lines.
- Deep radial vignette simulating cathode tube glass curvature and barrel distortion.
- Subtle 120ms CSS phosphor flicker animation.

### B. Boot Sequence Subsystem
- Bios POST sequence simulating cold boot on epoch load, auto-revealing terminal within ~1.5s with instant skip on user input.

### C. Phosphor Vector Charts
- Vector Diamond Kundli and Vimshottari Lifespan timeline rendered with glowing phosphor strokes on dark cathode plates.

### D. Falsifiability & Sensitivity Terminal (Sector 04B)
- Formatted as a real-time kernel perturbation diagnostic comparing Ground Truth Channel (1917, 98% Confluence) vs Perturbed Noise Channel (1920, 24% Collapse).

---

# ILLUMINATED STAR CHART // UI THEME SPECIFICATION & PROMPT ARTIFACT

> **System Aesthetic:** Antique Star Chart / Celestial Atlas / Harmonia Macrocosmica (Andreas Cellarius 1660)  
> **Classification:** High-signal antique cartography, cream parchment vellum, copper plate engraving line art, rotating armillary sphere, serif italic typography

---

## 1. Master Generation Prompt

```text
. Illuminated Star Chart
"Build website styled as antique star chart / celestial atlas, cream parchment background, copper engraving line art, constellation diagrams, rotating armillary sphere SVG animation, serif italic typography."
```

### Extended System Architecture Prompt
```text
Build a historically grounded yet mathematically rigorous celestial atlas web application:
- Palette: Cream Parchment Vellum (#fbf8ee / #f5ecd8 / #ede1c7), Burnished Copper Plate (#b87333 / #a25828 / #8c461a / #5a2c0e), Aged Iron-Gall Ink (#24160e / #382417), Antique Gold / Brass (#c59b27 / #d4af37), Cardinal Seal Crimson (#8c2522 / #b93834).
- Background: Aged parchment canvas with subtle organic paper fiber texture, warm sepia vignetting, and an interactive celestial map canvas rendering zodiacal constellation stick figures, magnitude stellar nodes with 4-point engraving spikes, and ecliptic/equatorial grid lines.
- Armillary Sphere 3D SVG Animation: Centerpiece rotating armillary sphere in burnished copper with concentric meridian rings, ecliptic band with zodiac glyphs tilted at 23.5°, solstitial/equinoctial colures, and central golden Terra/Sol orb in continuous gyroscopic rotation.
- Copper Engraving Line Art: Double-line cartographic framing, astrolabe degree scales with Roman/Arabic tick marks, corner quadrant spandrels with engraved fleurons, cross-hatching shade fills, and sun/moon compass rose bosses.
- Typography: Newsreader (Refined Classical Serif & Italic Headings), Cormorant Garamond (Scholarly Shastra Prose), and JetBrains Mono (High-Signal Ephemeris & Coordinate Tables in antique copper ink).
- Component Aesthetics: Cartographic Folio plates with deckle-edge drop shadows, brass astrolabe control plinths, wax seal status markers, copper plate diamond Kundli charts, and antique celestial coordinate progress rulers.
```

---

## 2. Design System Tokens & CSS Variables

```css
:root {
  /* Cream Parchment & Vellum Palette */
  --parchment-base: #fbf8ee;
  --parchment-wash: #f5ecd8;
  --parchment-aged: #ede1c7;
  --parchment-deep: #e2d2b4;
  --parchment-card: #f9f5ea;
  --parchment-lift: #fcfbf5;
  --parchment-shadow: rgba(58, 42, 26, 0.14);

  /* Burnished Copper Engraving Inks */
  --copper-light: #c9803e;
  --copper-primary: #b87333;
  --copper-deep: #8c461a;
  --copper-dark: #5a2c0e;
  --copper-line: #a25828;
  --copper-glow: rgba(184, 115, 51, 0.28);

  /* Aged Iron-Gall & Sepia Typography */
  --ink-pure: #1c1109;
  --ink-primary: #2b1d14;
  --ink-secondary: #4a3525;
  --ink-muted: #6e533d;
  --ink-faint: #9c7b60;

  /* Antique Brass & Celestial Gold */
  --brass-antique: #c59b27;
  --brass-radiant: #d4af37;
  --brass-glow: rgba(212, 175, 55, 0.24);

  /* Wax Seal & Cardinal Alert Crimson */
  --seal-crimson: #8c2522;
  --seal-crimson-bright: #b93834;
  --seal-crimson-bg: rgba(140, 37, 34, 0.08);

  /* Cartographic Borders & Framing */
  --border-engraved: 1.5px solid var(--copper-primary);
  --border-double: 3px double var(--copper-deep);
  --border-subtle: 1px solid rgba(162, 88, 40, 0.35);

  /* High-Signal Typography System */
  --font-display: 'Newsreader', Georgia, serif;
  --font-serif-italic: 'Newsreader', Georgia, serif;
  --font-body: 'Newsreader', Georgia, serif;
  --font-scholarly: 'Cormorant Garamond', Georgia, serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

---

## 3. Core Visual Components

### A. Rotating Armillary Sphere SVG Animation
- High-detail vector SVG armillary sphere featuring concentric equatorial, ecliptic, and colure rings in burnished copper.
- Dynamic 3D keyframe CSS rotation (`@keyframes rotateArmillary`) creating smooth gyroscopic movement.
- Central golden sun/earth sphere with radial meridian lines.

### B. Dynamic Constellation & Celestial Map Canvas
- Fullscreen background canvas rendering antique star charts (Orion, Ursa Major, Cassiopeia, Zodiac).
- Faint celestial coordinate radials, ecliptic curve, and magnitude stellar points with subtle 4-point copper diffraction spikes.

### C. Cartographic Atlas Folios (`.atlas-folio-card`)
- Double copper-plate border with corner quadrant fleurons and astrolabe degree marks.
- Warm cream parchment background with aged edge vignetting.

### D. Copper Plate Kundli & Astronomical Dasha Timeline
- Procedural North Indian Kundli rendered in crisp burnished copper on cream vellum with serif italic planetary designations.
- Vimshottari Mahadasha timeline formatted as an antique brass astrolabe coordinate ruler.

### E. Karl Popper Epistemic Comparator (Sector 04B)
- Dual antique cartographic parchment folios comparing Ground Truth (Baseline Epoch 1917, Verified 98% Confluence) vs Perturbed Input Shift (+3 Yrs, Collapsed 24% Confluence).

---

# ZEN PAPER MINIMAL // UI THEME SPECIFICATION & PROMPT ARTIFACT

> **System Aesthetic:** Japanese Washi Rice-Paper / Sumi-e Calligraphy / Minimalist Zen Archive  
> **Classification:** High-signal contemplative minimalism, off-white rice-paper, hairline sumi black ink, single vermilion seal stamp, generous negative space, gentle fade-in transitions

---

## 1. Master Generation Prompt

```text
Zen Paper Minimal
"Build calm minimalist website, off-white rice-paper background, thin black ink-brush lines, generous negative space, single accent stamp/seal graphic, gentle fade-in animations, no clutter."
```

### Extended System Architecture Prompt
```text
Build a serene, deeply minimalist Zen paper web application:
- Palette: Off-white Rice-Paper Vellum (#fcfbf8 / #f8f6f0 / #f2efe6), Sumi Ink Black (#121212 / #1e1e1e / #2a2a2a), Charcoal Wash (#595959 / #787878), and exactly ONE accent: Japanese Cinnabar Vermilion Hanko Seal Stamp (#b92b27 / #c23b22).
- Surface & Texture: Natural handmade washi rice-paper texture with subtle fibrous grain, zero heavy dropshadows, zero gradients, generous negative space (60-80px whitespace intervals between logical sectors).
- Linework: Ultra-thin 1px sumi black ink hairline borders, subtle hand-drawn calligraphy brush touches, and a single Ensō / circular calligraphy seal watermark.
- Single Accent Graphic: An authentic Japanese Hanko/Inkan vermilion red seal stamp (square or circular cartouche with classical seal script character) positioned as the focal mark.
- Animations: Gentle fade-in keyframe animations (0.7s cubic-bezier(0.16, 1, 0.3, 1)) that softly reveal cards as if ink is gently drying on fresh paper.
- Typography: Shippori Mincho / Noto Serif JP for serene Japanese/Latin editorial prose, paired with whisper-quiet JetBrains Mono for razor-sharp numerical coordinates and ephemeris tables.
```

---

## 2. Design System Tokens & CSS Variables

```css
:root {
  /* Washi Rice-Paper Palette */
  --zen-bg: #fcfbf8;
  --zen-paper: #f8f6f0;
  --zen-paper-subtle: #f2efe6;
  --zen-paper-darker: #e8e4d8;
  --zen-card: rgba(255, 255, 255, 0.76);
  
  /* Sumi Black Ink Lines */
  --ink-black: #121212;
  --ink-charcoal: #262626;
  --ink-deep: #383838;
  --ink-muted: #6b6b6b;
  --ink-faint: #9c9c9c;
  --ink-hairline: rgba(18, 18, 18, 0.12);
  --ink-border: 1px solid rgba(18, 18, 18, 0.16);
  --ink-stroke: 1.2px solid #1a1a1a;
  
  /* Single Accent: Vermilion Inkan / Hanko Seal Stamp */
  --seal-vermilion: #b92b27;
  --seal-vermilion-glow: rgba(185, 43, 39, 0.18);
  --seal-vermilion-soft: rgba(185, 43, 39, 0.08);

  /* Typography */
  --font-mincho: 'Shippori Mincho', 'Zen Old Mincho', 'Noto Serif JP', Georgia, serif;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}

/* Dark Mode Option: Kuro-Washi / Sumi Ink Wash */
[data-theme="dark"] {
  --zen-bg: #101114;
  --zen-paper: #15161a;
  --zen-paper-subtle: #1b1c22;
  --zen-paper-darker: #22242c;
  --zen-card: #16171c;
  
  /* Bone White / Pale Sumi Ink Lines */
  --ink-black: #f4f1ea;
  --ink-charcoal: #e2ddd3;
  --ink-deep: #c8c3b8;
  --ink-muted: #948e83;
  --ink-faint: #65615a;
  --ink-hairline: rgba(244, 241, 234, 0.10);
  --ink-border: 1px solid rgba(244, 241, 234, 0.14);
  --ink-stroke: 1.2px solid rgba(244, 241, 234, 0.35);
  
  /* Luminous Cinnabar Vermilion Hanko Stamp */
  --seal-vermilion: #e0382b;
  --seal-vermilion-glow: rgba(224, 56, 43, 0.22);
  --seal-vermilion-soft: rgba(224, 56, 43, 0.14);
}
```

---

## 3. Core Visual Components

### A. Hanko Seal Graphic & Ensō Watermark
- Authentic cinnabar vermilion red Hanko seal stamp (`.hanko-seal`) anchoring headers and key telemetry focal points.
- Delicate Ensō brush circle watermark floating softly in the background canvas.

### B. Generous Negative Space Layout
- Calm, wide margin viewports (max-width: 1180px) with generous whitespace intervals (60-80px between sectors).
- Zero visual clutter, zero decorative frames, purely disciplined hairline ink rules.

### C. Gentle Fade-In Motion
- Staggered CSS `@keyframes zenFadeIn` transitions delivering gentle, tranquil opacity reveals on page load and tab change.

### D. Sumi Ink Diamond Kundli & Vimshottari Timeline
- Procedural North Indian Kundli rendered in delicate 1px sumi black ink on off-white rice paper, centered with a miniature vermilion Hanko seal.

---

# CYBER-SACRED HYBRID // UI THEME SPECIFICATION & PROMPT ARTIFACT

> **System Aesthetic:** Cyberpunk HUD + Sacred Iconography / Quantum Yantra Interface  
> **Classification:** High-signal sci-fi HUD, near-black obsidian, gold circuit mandala traces, glitch-in text reveal, rotating chakra/yantra background

---

## 1. Master Generation Prompt

```text
10. Cyber-Sacred Hybrid
"Build website merging cyberpunk HUD with sacred iconography, near-black background, thin gold circuit-line patterns forming mandala shapes, glitch-in text reveal, low-opacity rotating chakra/yantra background animation."
```

### Extended System Architecture Prompt
```text
Build a cyberpunk HUD merging high-tech telemetry with sacred geometric iconography:
- Palette: Near-black obsidian (#04060a / #070a0f / #0c1018), radiant circuit gold (#d4af37 / #fbbf24 / #7a5c18), electric telemetry cyan (#00f0ff / #00a8b5), cyber alert crimson (#ff003c / #990024), and crisp data silver (#e2e8f0 / #94a3b8).
- Background: Interactive full-screen canvas rendering a slow-rotating 9-interlocking Sri Yantra vector with concentric 8-petal / 16-petal lotus chakra geometry at 0.06 opacity, coupled with subtle upward digital data motes.
- Circuit Mandalas & PCB Traces: Thin gold circuit-line patterns (stroke: 1px / 1.5px #d4af37) framing sector modules, featuring 45-degree chamfered PCB corners, gold solder via pads, and concentric mandala center bosses.
- Glitch-in Text Reveal: CSS keyframe animations (@keyframes cyberGlitch) featuring cyan/magenta RGB chromatic aberration splits, clip-path slice offsets, and high-frequency reveal flickers on headers and numerical counters.
- Typography: Orbitron (Futuristic HUD headers, sector badges, and telemetry indices), Rajdhani (Technical subheaders and metrics, weights 600/700), Space Grotesk / Inter (Crisp interface reading), and JetBrains Mono (Ephemeris data, timestamps, coordinates).
- Component Aesthetics: HUD diagnostic sectors with chamfered corners (clip-path: polygon), pulsing gold status nodes, live WebSocket streaming transit monitors, and side-by-side Karl Popper falsifiability split comparators.
```

---

## 2. Design System Tokens & CSS Variables

```css
:root {
  /* Near-Black Obsidian Canvas */
  --cyber-bg: #04060a;
  --cyber-surface: #070a0f;
  --cyber-card: rgba(10, 14, 23, 0.82);
  --cyber-card-solid: #0c111c;
  --cyber-card-lift: #121927;

  /* Thin Gold Circuit Traces & Sacred Gold */
  --gold-primary: #d4af37;
  --gold-bright: #fbbf24;
  --gold-trace: rgba(212, 175, 55, 0.28);
  --gold-subtle: rgba(212, 175, 55, 0.12);
  --gold-glow: 0 0 8px rgba(212, 175, 55, 0.4), 0 0 16px rgba(212, 175, 55, 0.15);
  
  /* Electric Telemetry Cyan */
  --cyan-telemetry: #00f0ff;
  --cyan-dim: #0099a8;
  --cyan-subtle: rgba(0, 240, 255, 0.1);
  --cyan-glow: 0 0 8px rgba(0, 240, 255, 0.45);

  /* Cyber Alert Crimson */
  --crimson-alert: #ff003c;
  --crimson-glow: 0 0 8px rgba(255, 0, 60, 0.5);
  --crimson-subtle: rgba(255, 0, 60, 0.12);

  /* Typography & Readout */
  --text-pure: #ffffff;
  --text-silver: #e2e8f0;
  --text-muted: #8492a6;
  --text-dim: #475569;

  /* Borders & Circuit Geometry */
  --circuit-border: 1px solid rgba(212, 175, 55, 0.35);
  --circuit-border-bright: 1px solid #d4af37;
  --circuit-via: #fbbf24;

  /* Fonts */
  --font-hud: 'Orbitron', -apple-system, sans-serif;
  --font-tech: 'Rajdhani', -apple-system, sans-serif;
  --font-body: 'Inter', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

---

## 3. Core Visual Components

### A. Rotating Chakra / Sri Yantra Canvas Background
- Fullscreen background canvas running at 60fps.
- Concentric geometry: Central bindu, 9 interlocking Sri Yantra triangles, 8-petal and 16-petal lotus rings, outer Bhupura (earth citadel) square gates.
- Constant slow rotation (period: 120s per cycle) rendered in gold (#d4af37) and cyan (#00f0ff) at 0.06 opacity.
- Subtle upward-drifting digital quantum prana particles.

### B. Gold Circuit Mandala Panels (`.cyber-card`)
- Chamfered 45° corner geometry via `clip-path: polygon(14px 0, calc(100% - 14px) 0, 100% 14px, 100% calc(100% - 14px), calc(100% - 14px) 100%, 14px 100%, 0 calc(100% - 14px), 0 14px)`.
- Thin gold circuit-line border traces with golden circular via pads at corners and junction intersections.
- Backdrop blur (`backdrop-filter: blur(14px)`).

### C. Glitch-in Text Reveal
- Text reveal with dual RGB pseudo-elements (`::before` cyan offset -2px, `::after` magenta offset +2px).
- `@keyframes glitchAnim` applying vertical clip-path slices and rapid horizontal displacement on initialization and target acquisition.

### D. Procedural Cyber-Sacred Kundli & Mahadasha Timeline
- Obsidian substrate `#070a0f` with gold circuit traces (`#d4af37`), PCB via pads, sacred Sri Yantra center boss with bindu, cyan planetary nodes (`#00f0ff`), and glowing reticle age cursor.






