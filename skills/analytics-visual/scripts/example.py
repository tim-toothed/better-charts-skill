"""Render a small example using invented data only."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from chart_styles import apply_style


def render(output, style='neutral-light'):
    t = apply_style(style)
    fig, ax = plt.subplots(figsize=(10, 6), layout='constrained')
    labels, values = ['Group A', 'Group B', 'Group C'], [12, 8, 10]
    ax.barh(labels, values, color=t.accent)
    ax.set_xlim(0, 15)
    ax.set_xlabel('Count, units')
    ax.set_title('Synthetic comparison')
    ax.invert_yaxis()
    for index, value in enumerate(values):
        ax.text(value + .2, index, str(value), va='center', color=t.text)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output)
    plt.close(fig)
    print(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--style', default='neutral-light')
    args = parser.parse_args()
    render(args.output, args.style)
