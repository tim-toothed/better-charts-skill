"""Render README artwork using the unchanged bundled chart-style API.

Run from the repository root with matplotlib and pillow installed.
Banner font: --font path/to/VT323.ttf (SIL OFL).
"""
from pathlib import Path
import argparse
import math
import random
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'skills/analytics-visual/scripts'))
from chart_styles import apply_style, procvetaev_font, add_procvetaev_background


def render_charts():
    output = ROOT / 'docs'
    specs = [
        ('line', 'dark', 'Momentum', 'Weekly orders'),
        ('bar', 'business-blue', 'Category comparison', 'Orders by category'),
        ('scatter', 'warm', 'Relationship', 'Spend and orders'),
        ('stacked', 'muted', 'Composition', 'Orders by channel'),
        ('range', 'high-contrast', 'Uncertainty', 'Median and 10th–90th percentile'),
        ('horizontal', 'procvetaev', 'RANKING', 'COMPLETED ORDERS BY REGION'),
        ('box', 'monochrome', 'Distribution', 'Delivery time by service'),
        ('heatmap', 'minimal', 'Pattern matrix', 'Hourly demand by weekday'),
        ('area', 'neutral-light', 'Volume over time', 'Cumulative monthly activity'),
    ]
    paths = []
    for kind, style, title, subtitle in specs:
        t = apply_style(style)
        fig, ax = plt.subplots(figsize=(7.2, 4.8), dpi=150)
        fig.subplots_adjust(left=.14, right=.95, bottom=.20, top=.72)
        if style == 'procvetaev':
            add_procvetaev_background(fig)
            heading = {'fontproperties': procvetaev_font('heading')}
        else:
            heading = {'fontweight': 'bold'}
        fig.text(.08, .90, title, fontsize=18, color=t.accent if style == 'procvetaev' else t.text, **heading)
        fig.text(.08, .82, subtitle, fontsize=10, color=t.muted)
        fig.text(.08, .055, f'{style}  ·  synthetic data', fontsize=8.5, color=t.muted)
        ax.grid(False)
        if kind == 'line':
            x = list(range(1, 9))
            ax.plot(x, [110, 124, 119, 143, 151, 146, 171, 185], '-o', label='Online', color=t.series[0], linewidth=2.2, markersize=4)
            ax.plot(x, [74, 82, 79, 91, 95, 103, 99, 115], '--s', label='Retail', color=t.series[1], linewidth=2.2, markersize=4)
            ax.set(xlabel='Week', ylabel='Orders', ylim=(0, 210), xticks=x)
            ax.legend(loc='upper left', ncol=2, fontsize=8)
        elif kind == 'bar':
            values = [420, 350, 285, 210]
            bars = ax.bar(['Home', 'Outdoor', 'Office', 'Travel'], values, color=t.accent, width=.58)
            ax.bar_label(bars, padding=4, color=t.text, fontsize=9)
            ax.set(ylabel='Orders', ylim=(0, 500))
        elif kind == 'scatter':
            x = [1.1, 1.8, 2.2, 2.7, 3.2, 3.8, 4.1, 4.9, 5.2, 5.8, 6.3, 6.9]
            y = [30, 48, 37, 67, 55, 92, 72, 105, 86, 115, 99, 132]
            sizes = [45, 58, 40, 74, 52, 91, 68, 108, 75, 120, 88, 132]
            ax.scatter(x, y, s=sizes, color=t.accent, alpha=.82, edgecolors=t.text, linewidths=.5)
            ax.set(xlabel='Spend, USD thousands', ylabel='Orders', xlim=(0, 8), ylim=(0, 150))
        elif kind == 'stacked':
            channels = [('Direct', [180, 220, 250, 280]), ('Search', [140, 160, 190, 210]), ('Partners', [80, 100, 110, 130])]
            bottom = [0] * 4
            for (label, values), color in zip(channels, t.series):
                ax.bar(['Q1', 'Q2', 'Q3', 'Q4'], values, bottom=bottom, label=label, color=color, width=.55)
                bottom = [a + b for a, b in zip(bottom, values)]
            ax.set(ylabel='Orders', ylim=(0, 750))
            ax.legend(loc='upper left', ncol=3, fontsize=8)
        elif kind == 'range':
            median, lower, upper = [2.5, 3.5, 4.5, 3], [1.5, 2, 3, 2], [4, 5.5, 7, 4.5]
            ax.errorbar(median, ['North', 'South', 'East', 'West'], xerr=[[a-b for a,b in zip(median, lower)], [a-b for a,b in zip(upper, median)]], fmt='o', markersize=7, capsize=6, linewidth=2, color=t.accent)
            ax.invert_yaxis()
            ax.set(xlabel='Delivery time, days', xlim=(0, 8), ylim=(3.6, -.6))
        elif kind == 'horizontal':
            bars = ax.barh(['North', 'West', 'South', 'East'], [620, 510, 435, 350], color=[t.accent, t.series[1], t.series[1], t.series[1]], height=.58)
            ax.bar_label(bars, padding=6, color=t.text, fontsize=9)
            ax.invert_yaxis()
            ax.set(xlabel='Completed orders', xlim=(0, 740))
        elif kind == 'box':
            data = [[1.8, 2.1, 2.2, 2.5, 2.7, 3.0, 3.6], [2.4, 2.8, 3.1, 3.3, 3.8, 4.2, 5.0], [1.2, 1.7, 1.9, 2.0, 2.3, 2.7, 3.1]]
            bp = ax.boxplot(data, tick_labels=['Express', 'Standard', 'Pickup'], patch_artist=True, widths=.55)
            for patch, color in zip(bp['boxes'], t.series):
                patch.set_facecolor(color)
                patch.set_alpha(.72)
            for item in bp['medians']:
                item.set_color(t.text)
                item.set_linewidth(2)
            ax.set(ylabel='Days', ylim=(0, 5.8))
        elif kind == 'heatmap':
            matrix = [[12, 18, 26, 31, 28, 20], [16, 25, 34, 38, 36, 24], [14, 22, 30, 42, 39, 27], [18, 29, 41, 48, 44, 32], [20, 33, 46, 55, 50, 37]]
            cmap = matplotlib.colors.LinearSegmentedColormap.from_list('skill_heat', [t.panel, t.series[1], t.accent])
            image = ax.imshow(matrix, cmap=cmap, aspect='auto')
            ax.set_xticks(range(6), ['08', '10', '12', '14', '16', '18'])
            ax.set_yticks(range(5), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'])
            ax.set(xlabel='Hour')
            fig.colorbar(image, ax=ax, fraction=.035, pad=.03)
        else:
            x = list(range(1, 13))
            a = [18, 24, 31, 39, 48, 60, 72, 86, 98, 113, 129, 148]
            b = [10, 14, 19, 25, 33, 40, 49, 59, 70, 82, 95, 109]
            ax.fill_between(x, a, color=t.series[0], alpha=.72, label='Product A')
            ax.fill_between(x, b, color=t.series[1], alpha=.70, label='Product B')
            ax.plot(x, a, color=t.series[0], linewidth=1.5)
            ax.plot(x, b, color=t.series[1], linewidth=1.5)
            ax.set(xlabel='Month', ylabel='Activity', xlim=(1, 12), ylim=(0, 165), xticks=[1, 3, 5, 7, 9, 11])
            ax.legend(loc='upper left', fontsize=8)
        ax.grid(True, axis='x' if kind in ('range', 'horizontal', 'scatter') else 'y', alpha=.18)
        ax.set_axisbelow(True)
        path = output / f'showcase-{kind}.png'
        fig.savefig(path, dpi=150)
        plt.close(fig)
        paths.append(path)
        print(path)

    cards = [Image.open(path).convert('RGB') for path in paths]
    card_w, card_h = cards[0].size
    gap = 18
    canvas = Image.new('RGB', (card_w * 3 + gap * 4, card_h * 3 + gap * 4), (18, 18, 20))
    for index, card in enumerate(cards):
        row, col = divmod(index, 3)
        canvas.paste(card, (gap + col * (card_w + gap), gap + row * (card_h + gap)))
    gallery = output / 'gallery.png'
    canvas.save(gallery, quality=95)
    print(gallery)


def render_banner(font):
    # Adapted from github-branding/round3.py: warm-white VT323 on red waves.
    width, height = 1600, 400
    image = Image.new('RGB', (width, height), (12, 11, 14))
    draw = ImageDraw.Draw(image)
    rng = random.Random(446)
    for y in range(-80, 480, 7):
        points = [(x, y + int(27 * math.sin(x * .008 + y * .018))) for x in range(0, width, 4)]
        draw.line(points, fill=rng.choice([(48, 15, 24), (89, 20, 32), (143, 28, 42)]), width=1)
    face = ImageFont.truetype(str(font), 120)
    text = 'Analytics Visual Skill'
    box = draw.textbbox((0, 0), text, font=face)
    x = (width - (box[2] - box[0])) // 2
    y = (height - (box[3] - box[1])) // 2 - box[1]
    draw.text((x, y), text, font=face, fill=(235, 232, 224), stroke_width=6, stroke_fill=(12, 11, 14))
    path = ROOT / 'docs/banner.png'
    image.save(path)
    print(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', type=Path, help='Optional VT323 TTF; omit to render charts only')
    args = parser.parse_args()
    render_charts()
    if args.font:
        render_banner(args.font)
