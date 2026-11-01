---
name: analytics-visual
description: Create data visualization.
version: 0.4.0
author: tim-toothed
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [visualization, matplotlib, png, charts, telegram]
---

# Analytics Visual Skill

## When to use

Use at the presentation stage for verified results: when asked for a chart, or when comparisons, trends, ranges, or a dense summary become clearer visually. Choose a chart, visual/plain table, or text to suit the question. Numbers alone do not require an image; a precise table may be easier to search and copy. Fulfill an explicit chart request even for a small example.

This skill does not collect data or choose calculation methodology. Obtain and verify the results with domain tools first; do not change methodology to make a convenient chart. Show substantive results, not decorative KPIs or data coverage alone.

## Style and execution

Selected style: **not selected** (не выбран). On a new installation show the synthetic gallery and ask for a preference. Persist a choice only with the user's permission; do not alter an existing preference. Until selected, use `neutral-light` as a temporary neutral fallback, not an implicit saved choice.

Read and import `scripts/chart_styles.py`; do not reconstruct its palette manually. Nine presets: neutral-light, minimal, dark, high-contrast, monochrome, muted, procvetaev, business-blue, warm. Colors are not assigned to marketplace or corporate identities.

```python
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
sys.path.insert(0, str(Path('<skill-dir>') / 'scripts'))
from chart_styles import apply_style, delta_color, style_context
import matplotlib.pyplot as plt

t = apply_style('neutral-light')  # before creating figures; resets rcParams
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(['A', 'B', 'C'], [12, 8, 10], color=t.accent)
ax.set_ylim(0, 15)
ax.set_ylabel('Count, units')
ax.set_title('Synthetic example')
fig.savefig('<scratch-dir>/example.png')
plt.close(fig)
```

Replace placeholders with actual paths. Immutable tokens contain background, panel, text, muted, accent, series, positive, negative, neutral. Apply tokens explicitly to annotations, series and deltas; existing artists are not recolored. `with style_context('dark') as t:` temporarily applies a preset and restores previous rcParams. Eight presets use DejaVu Sans. The procvetaev graphical template uses #C40123, #C2C2C2, #111111, #FFFFFF, panel #1C1C1C/grid #343434, and semantic delta green #39A96B/red #E2553D. Use uppercase headings with `procvetaev_font('heading')`, uppercase subheadings with `procvetaev_font('subheading')`, and `procvetaev_font('body')` for body text. Set figure-heading color to `t.accent` explicitly. `add_procvetaev_background(fig)` adds the supplied motif and localized red gradient below data axes; pattern_opacity=.05 or .10, or pattern=False. Missing motif skips that layer; missing fonts warn and fall back to DejaVu Sans. Read `references/asset-provenance.md` for asset terms. Bundled support: `assets/cyberpunk.mplstyle`, `assets/procvetaev-pattern.png`, `assets/fonts/TikTokSans18-heading.ttf`, `assets/fonts/TikTokSans18-subheading.ttf`, `assets/fonts/TikTokSans18-body.ttf`, `assets/fonts/OFL-TikTokSans.txt`.

## Meaning and layout

- Priority: truthfulness, readability and semantics, then style. A story can connect verified results but is not obligatory. A single bar chart may answer a comparison. Never invent causes, previous values or comparisons; preserve caveats.
- Choose chart type, layout and image count for the question. Do not force a two-image template or bury the main result in tiny text. Whitespace and typography serve the data.
- Different units require separate labeled fields, columns or panels: one cell, one metric. Place a value and its delta together, on the same row/alignment. Do not concatenate money, percentages and counts with slashes. Label absolute deltas with units; distinguish percent from percentage points.
- Comparable bars/panels require a shared scale, visible axis and zero baseline. A narrowed line/point scale must be explicit. Distinguish forecasts from facts. State the known period, comparison base, limitations and qualifiers. Missing values are not zero; do not hide gaps.
- `delta_color(value, t)` uses green for positive, red for negative, neutral for zero/None/NaN/infinity. This indicates direction, not good/bad: rising expenses are not improvement. Always retain signs and values. Do not compute a percentage against a zero baseline without a defined method.
- Use the preset palette/font; adjust label placement and grid locally. If small colored text lacks contrast, pair a readable semantic marker with a high-contrast number. Color never replaces labels. Use hatching or markers where useful.

## Procedure and verification

1. Check numbers, units, period, base and limitations. If analysis is unfinished, return to it. Rendering checks do not validate domain calculations.
2. Choose a format preserving all material metrics and identifiers. Optionally read `references/chart-guidelines.md` for additional forms/scales; the core rules above are self-contained.
3. Create a short Python script in managed scratch using direct Matplotlib, backend `Agg`, and Unicode-capable fonts. No Seaborn, browser, ImageGen or server. If Matplotlib is unavailable, use `uv run --no-project --with matplotlib python "<script>"`. Do not store customer data permanently in the skill.
4. Save PNG and script together; close figures. Split dense results only to preserve readability and content.
5. Check numbers/completeness with code and inspect the actual final PNG with `vision_analyze`: color meaning, conclusions, units, separated fields, labels/Unicode, scales, readability, contrast, margins, completeness and cropping. A clipping-only check is insufficient. Fix before delivery.
6. Send `MEDIA:<absolute-path>` with a brief explanation of notation. Do not repeat the entire report; supply the source table/code on request.

Synthetic gallery: `uv run --no-project --with matplotlib --with pillow python "<skill-dir>/scripts/style_gallery.py" --output "<scratch-dir>/style-gallery"`.

Synthetic example (not a mandatory template): `uv run --no-project --with matplotlib python "<skill-dir>/scripts/example.py" --output "<scratch-dir>/example.png"`.


