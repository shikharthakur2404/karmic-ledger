"""
karmic-ledger: Zen Paper Minimal Visual & Kundli Rendering Engine
Renders vector SVG Diamond Kundlis and Lifespan Progress Bars in calm Zen Paper Minimal aesthetic:
Adapts seamlessly to both Light (Washi Rice-Paper) and Dark (Kuro-Washi / Sumi Ink Wash) modes
via CSS variables: hairline ink strokes, serene mincho/mono typography, and vermilion seal reticles.
"""

from typing import Any


def generate_diamond_kundli_svg(
    lagna_sign_index: int, planets_by_house: dict[int, list[str]]
) -> str:
    """
    Renders a traditional North Indian Diamond Kundli in Zen Paper Minimal aesthetic:
    Clean sumi ink strokes, subtle house coordinates, and a central vermilion seal focal point.
    Fully theme-responsive across Light Rice-Paper and Dark Kuro-Washi.
    """
    house_positions = {
        1: {"num_x": 200, "num_y": 126, "p_x": 200, "p_y": 80},
        2: {"num_x": 296, "num_y": 48, "p_x": 302, "p_y": 78},
        3: {"num_x": 362, "num_y": 110, "p_x": 348, "p_y": 142},
        4: {"num_x": 296, "num_y": 205, "p_x": 276, "p_y": 205},
        5: {"num_x": 362, "num_y": 298, "p_x": 348, "p_y": 268},
        6: {"num_x": 296, "num_y": 362, "p_x": 302, "p_y": 332},
        7: {"num_x": 200, "num_y": 286, "p_x": 200, "p_y": 330},
        8: {"num_x": 104, "num_y": 362, "p_x": 98, "p_y": 332},
        9: {"num_x": 38, "num_y": 298, "p_x": 52, "p_y": 268},
        10: {"num_x": 104, "num_y": 205, "p_x": 124, "p_y": 205},
        11: {"num_x": 38, "num_y": 110, "p_x": 52, "p_y": 142},
        12: {"num_x": 104, "num_y": 48, "p_x": 98, "p_y": 78},
    }

    svg_elements = []

    for h in range(1, 13):
        sign_val = ((lagna_sign_index + h - 1) % 12) + 1
        coords = house_positions[h]

        # Subtle house & sign index
        svg_elements.append(
            f'<text x="{coords["num_x"]}" y="{coords["num_y"]}" class="zen-svg-muted" font-family="\'Shippori Mincho\', \'JetBrains Mono\', serif" font-size="10" font-weight="500" fill="var(--ink-muted, #707070)" text-anchor="middle">H{h}:{sign_val}</text>'
        )

        # Planetary glyphs
        pls = planets_by_house.get(h, [])
        if pls:
            pls_str = " ".join(pls)
            svg_elements.append(
                f'<text x="{coords["p_x"]}" y="{coords["p_y"]}" class="zen-svg-planet" font-family="\'Shippori Mincho\', \'Noto Serif JP\', serif" font-size="14" font-weight="700" fill="var(--ink-black, #141414)" text-anchor="middle">{pls_str}</text>'
            )

    body_content = "\n  ".join(svg_elements)

    svg = f"""<svg viewBox="0 0 400 400" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" class="kundli-svg-canvas">
  <!-- Washi Paper Base Canvas -->
  <rect x="0" y="0" width="400" height="400" fill="var(--zen-card, #ffffff)" class="zen-svg-card-bg" />

  <!-- Outer Boundary Frame -->
  <rect x="25" y="25" width="350" height="350" fill="none" stroke="var(--ink-black, #141414)" stroke-width="1.2" class="zen-svg-frame" />

  <!-- Diagonal Sumi Ink Crosses -->
  <line x1="25" y1="25" x2="375" y2="375" stroke="var(--ink-black, #141414)" stroke-width="1" class="zen-svg-frame" />
  <line x1="375" y1="25" x2="25" y2="375" stroke="var(--ink-black, #141414)" stroke-width="1" class="zen-svg-frame" />

  <!-- Diamond Rhombus Lines -->
  <polygon points="200,25 375,200 200,375 25,200" fill="none" stroke="var(--ink-black, #141414)" stroke-width="1.2" class="zen-svg-frame" />

  <!-- Center Vermilion Hanko Seal Mark -->
  <rect x="191" y="191" width="18" height="18" fill="none" stroke="var(--seal-red, #b92b27)" stroke-width="1.5" transform="rotate(-3 200 200)" />
  <circle cx="200" cy="200" r="2.5" fill="var(--seal-red, #b92b27)" />

  <!-- Planetary Nodes & Bhavas -->
  {body_content}
</svg>"""
    return svg


def generate_dasha_progress_bar_svg(
    dasha_timeline: list[dict[str, Any]],
    current_age_years: float,
    max_lifespan: float = 95.0,
) -> str:
    """
    Renders a 120-Year Vimshottari Mahadasha timeline in Zen Paper Minimal style:
    Clean monochrome cells on washi paper substrate with a single vermilion age reticle needle.
    """
    total_width = 820
    height = 32

    segments_svg = []
    current_x = 0.0

    for idx, maha in enumerate(dasha_timeline):
        dur = maha["duration_years"]
        seg_width = (dur / max_lifespan) * total_width
        fill_color = (
            "var(--zen-paper-subtle, #f3f0e6)"
            if idx % 2 == 0
            else "var(--zen-card, #ffffff)"
        )

        # Adaptive typography based on segment width
        m_name = maha["mahadasha"]
        if seg_width >= 85:
            label = f"{m_name} ({dur:.0f}y)"
        elif seg_width >= 42:
            label = m_name
        else:
            label = m_name[:3]

        tooltip = f"{m_name} Mahadasha ({dur:.1f} Years: {maha.get('start_date', '')} to {maha.get('end_date', '')})"

        segments_svg.append(
            f'<g class="dasha-group" data-dasha="{m_name}">'
            f"<title>{tooltip}</title>"
            f'<rect class="dasha-rect" x="{current_x:.1f}" y="0" width="{seg_width:.1f}" height="{height}" fill="{fill_color}" stroke="var(--ink-hairline, rgba(20,20,20,0.15))" stroke-width="1"/>'
            f'<text x="{current_x + seg_width / 2.0:.1f}" y="20" font-family="\'Shippori Mincho\', \'JetBrains Mono\', monospace" font-size="10.5" font-weight="600" fill="var(--ink-charcoal, #2a2a2a)" text-anchor="middle">{label}</text>'
            f"</g>"
        )
        current_x += seg_width

    # Current Age Reticle: Vermilion Needle & Triangular Seal Indicator
    marker_x = min((current_age_years / max_lifespan) * total_width, total_width)
    marker_svg = f"""
    <g class="age-reticle" transform="translate(0, 0)">
      <line x1="{marker_x:.1f}" y1="-4" x2="{marker_x:.1f}" y2="{height + 4}" stroke="var(--seal-red, #b92b27)" stroke-width="1.8" />
      <polygon points="{marker_x - 4:.1f},-5 {marker_x + 4:.1f},-5 {marker_x:.1f},0" fill="var(--seal-red, #b92b27)" />
      <circle cx="{marker_x:.1f}" cy="{height / 2}" r="2.5" fill="var(--seal-red, #b92b27)" />
      <text x="{marker_x:.1f}" y="{height + 17}" font-family="\'Shippori Mincho\', monospace" font-size="10" font-weight="600" fill="var(--seal-red, #b92b27)" text-anchor="middle">{current_age_years:.1f}Y</text>
    </g>
    """

    full_svg = f"""<svg viewBox="0 0 {total_width} {height + 24}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" class="dasha-svg-bar">
  <rect x="0" y="0" width="{total_width}" height="{height}" fill="var(--zen-paper, #f8f6f0)" stroke="var(--ink-black, #141414)" stroke-width="1.2" />
  <g>
    {"".join(segments_svg)}
    {marker_svg}
  </g>
</svg>"""
    return full_svg
