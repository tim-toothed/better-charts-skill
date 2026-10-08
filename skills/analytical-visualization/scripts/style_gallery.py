"""Render nine previews using explicitly synthetic data."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from chart_styles import STYLES, apply_style, add_procvetaev_background, procvetaev_font


def render(output):
    output.mkdir(parents=True, exist_ok=True)
    paths = []
    for idx, slug in enumerate(STYLES, 1):
        t = apply_style(slug)
        fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
        if slug == 'procvetaev':
            add_procvetaev_background(fig)
        fig.subplots_adjust(left=.14, right=.96, top=.73, bottom=.16)
        fig.text(.06, .93, f'{idx}. {t.label}', size=20, weight='bold', color=t.accent if slug == 'procvetaev' else t.text,
                 fontproperties=procvetaev_font('heading') if slug == 'procvetaev' else None)
        fig.text(.06, .865, 'Synthetic comparison · invented data', size=13, color=t.text)
        for j, (label, color) in enumerate(zip(['Series A', 'Series B', 'Series C'], t.series)):
            ys = [i + (j - 1) * .23 for i in range(3)]
            nums = [[72, 54, 18], [38, 96, 26], [24, 61, 12]]
            values = [row[j] for row in nums]
            ax.barh(ys, values, height=.20, color=color, label=label,
                    hatch=['///', '...', 'xx'][j] if slug == 'monochrome' else None,
                    edgecolor=t.text if slug in ('monochrome', 'high-contrast') else 'none')
            for y, value in zip(ys, values):
                ax.text(value + 1.8, y, str(value), va='center', size=10, color=t.text)
        ax.set_yticks(range(3), ['Group A', 'Group B', 'Group C'])
        ax.invert_yaxis()
        ax.set_xlim(0, 125)
        ax.set_xlabel('Count, units')
        ax.legend(loc='lower left', bbox_to_anchor=(-.03, 1.04), ncol=3, fontsize=10)
        fig.text(.06, .04, 'All data invented. Colors have no corporate assignment.', size=10, color=t.muted)
        path = output / f'{idx:02d}-{slug}.png'
        fig.savefig(path)
        plt.close(fig)
        paths.append(path)
    gallery = Image.new('RGB', (2250, 1350), '#D9DFE5')
    for i, path in enumerate(paths):
        with Image.open(path) as im:
            tile = im.convert('RGB')
            tile.thumbnail((750, 450))
            gallery.paste(tile, ((i % 3) * 750, (i // 3) * 450))
    gallery.save(output / 'gallery.png')
    print(f'Rendered {len(paths)} styles; all data synthetic')
    print(output / 'gallery.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    render(parser.parse_args().output)
