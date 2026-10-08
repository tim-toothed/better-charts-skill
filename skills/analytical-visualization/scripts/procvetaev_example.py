"""Approved synthetic example; illustrative layout, not a required template."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from chart_styles import apply_style, delta_color, procvetaev_font, add_procvetaev_background


def render(output):
    T = apply_style('procvetaev')
    names = ['Магазин А', 'Магазин Б', 'Магазин В', 'Магазин Г', 'Магазин Д', 'Магазин Е']
    current = [148, 126, 104, 88, 73, 57]
    previous = [132, 138, 100, 96, 73, 60]
    deltas = [100 * (a / b - 1) for a, b in zip(current, previous)]
    assert len(names) == len(current) == len(previous) == len(deltas) == 6
    fig = plt.figure(figsize=(11, 6.3))
    add_procvetaev_background(fig)
    heading = procvetaev_font('heading')
    subheading = procvetaev_font('subheading')
    # A single comparison, common zero-based scale, independent aligned delta column.
    ax = fig.add_axes([.17, .24, .61, .49])
    ax.barh(range(6), current, height=.56, color=T.accent)
    ax.set_yticks(range(6), names)
    ax.invert_yaxis()
    ax.set_xlim(0, 175)
    ax.set_xticks([0, 40, 80, 120, 160])
    ax.set_xlabel('Выручка, тыс. ₽', labelpad=15)
    for i, value in enumerate(current):
        ax.text(value + 3, i, str(value), va='center', color=T.text, fontsize=14)
        ax.text(1.13, i, f'{deltas[i]:+.1f}%'.replace('.', ',').replace('-', '−'),
                transform=ax.get_yaxis_transform(), va='center', ha='center',
                fontsize=14, color=delta_color(deltas[i], T))
    fig.text(.055, .92, 'PROCVETAEV / ВЫРУЧКА МАГАЗИНОВ', fontsize=25, fontproperties=heading, color=T.accent)
    fig.text(.055, .865, 'Синтетический пример · шесть магазинов · единая шкала', color=T.muted, fontsize=13)
    fig.text(.86, .775, 'К ПРОШЛОМУ\nПЕРИОДУ', ha='center', fontsize=12, fontproperties=subheading, color=T.accent, linespacing=1.35)
    fig.text(.055, .10, 'ВЫРУЧКА', color=T.accent, fontsize=13, fontproperties=subheading)
    fig.text(.285, .10, '+  Рост', color=T.positive, fontsize=13)
    fig.text(.455, .10, '−  Снижение', color=T.negative, fontsize=13)
    fig.text(.69, .10, '0  Без изменений', color=T.neutral, fontsize=13)
    fig.text(.055, .065, 'База: предыдущий период · данные вымышлены · TikTok Sans', color=T.muted, fontsize=11)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output)
    plt.close(fig)
    print(f'Rendered: {output}; synthetic only; negative={T.negative}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    render(parser.parse_args().output)
