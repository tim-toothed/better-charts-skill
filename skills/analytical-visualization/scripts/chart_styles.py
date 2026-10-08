"""Reusable Matplotlib presets; no chart type, layout, or market assignments.

Call apply_style before creating figures. Use returned tokens explicitly for
figure headings, annotations, semantic deltas and any locally overridden colors.
"""
from contextlib import contextmanager
from dataclasses import dataclass
from math import isfinite
from pathlib import Path
from types import MappingProxyType
import matplotlib.style as mplstyle

import matplotlib as mpl
from cycler import cycler


@dataclass(frozen=True)
class StyleTokens:
    name: str
    label: str
    background: str
    panel: str
    text: str
    muted: str
    accent: str
    series: tuple[str, ...]
    positive: str
    negative: str
    neutral: str
    grid: bool = True


# Explicit colors: switching themes must never inherit another theme's cycle.
STYLES = MappingProxyType({
    'neutral-light': StyleTokens('neutral-light', 'Нейтральный', '#F7F9FC', '#F7F9FC', '#192D45', '#596B80', '#8068B3', ('#8068B3', '#478FBD', '#C79827'), '#16853D', '#B20D2D', '#596B80'),
    'minimal': StyleTokens('minimal', 'Минимализм', '#FFFFFF', '#FFFFFF', '#202124', '#62696D', '#34495E', ('#34495E', '#95A5A6', '#D4DADD'), '#16853D', '#B20D2D', '#62696D', False),
    'dark': StyleTokens('dark', 'Тёмный', '#152033', '#152033', '#E7EDF6', '#A4B2C7', '#BD9FEA', ('#BD9FEA', '#69B8EC', '#F0CA6D'), '#51C78A', '#FF6B78', '#A4B2C7'),
    'high-contrast': StyleTokens('high-contrast', 'Контрастный', '#FFFFFF', '#FFFFFF', '#000000', '#4D4D4D', '#1748C9', ('#1748C9', '#DF6200', '#16853D'), '#12652D', '#A30929', '#4D4D4D'),
    'monochrome': StyleTokens('monochrome', 'Монохромный', '#FFFFFF', '#FFFFFF', '#222222', '#656565', '#303030', ('#303030', '#848484', '#C5C5C5'), '#16853D', '#B20D2D', '#656565'),
    'muted': StyleTokens('muted', 'Приглушённый', '#F2F3EF', '#E8E8E8', '#35463D', '#606D65', '#647F74', ('#647F74', '#9A8298', '#BA9B69'), '#23734A', '#A52A40', '#606D65'),
    'procvetaev': StyleTokens('procvetaev', 'PROCVETAEV', '#111111', '#1C1C1C', '#FFFFFF', '#C2C2C2', '#C40123', ('#C40123', '#C2C2C2', '#FFFFFF'), '#39A96B', '#E2553D', '#C2C2C2'),
    'business-blue': StyleTokens('business-blue', 'Деловой синий', '#F0F5FA', '#F0F5FA', '#12365B', '#546F89', '#154D82', ('#154D82', '#4E8FB9', '#94C4DF'), '#16853D', '#B20D2D', '#546F89'),
    'warm': StyleTokens('warm', 'Тёплый', '#FAF4E9', '#FAF4E9', '#49382B', '#776553', '#B96C49', ('#B96C49', '#D2A35C', '#858864'), '#33734A', '#B20D2D', '#776553'),
})


def procvetaev_font(role='body'):
    """OFL TikTok Sans static instances; no dependency on system installation.

    18pt means optical size, not a fixed chart point size. Use heading for
    uppercase titles, subheading for uppercase section labels, body otherwise.
    Missing bundled files have an explicit DejaVu Sans fallback, never fake TikTok.
    """
    import warnings
    from matplotlib.font_manager import FontProperties, fontManager
    if role not in ('body', 'subheading', 'heading'):
        raise ValueError(f'Unknown font role: {role}')
    path = Path(__file__).resolve().parents[1] / 'assets' / 'fonts' / f'TikTokSans18-{role}.ttf'
    if path.is_file():
        fontManager.addfont(str(path))
        return FontProperties(fname=str(path))
    warnings.warn(f'TikTok Sans asset missing: {path}; using DejaVu Sans', stacklevel=2)
    return FontProperties(family='DejaVu Sans', weight='semibold' if role == 'heading' else 'normal')


def add_procvetaev_background(fig, *, pattern=True, pattern_opacity=.05):
    """Optional graphical template layer, below all data axes; not an rcParams setting.

    Dark base with localized red illumination and optional supplied motif.
    The layer remains below data axes. Pattern opacity is 5% or 10%.
    """
    import numpy as np
    from matplotlib.colors import to_rgb
    from matplotlib import image as mpimg
    if pattern_opacity not in (.05, .10):
        raise ValueError('Template pattern opacity must be 0.05 or 0.10')
    if getattr(fig, '_procvetaev_background', None) is not None:
        return fig._procvetaev_background
    t = STYLES['procvetaev']
    ax = fig.add_axes([0, 0, 1, 1], zorder=-100, label='procvetaev-template-background')
    ax.set_axis_off()
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_facecolor(t.background)
    # Opaque neutral base, actual motif underneath a translucent red illumination.
    ax.imshow(np.array([[to_rgb(t.background)]]), extent=(0, 1, 0, 1), aspect='auto', zorder=0)
    if pattern:
        path = Path(__file__).resolve().parents[1] / 'assets' / 'procvetaev-pattern.png'
        if path.is_file():
            rgba = np.rot90(mpimg.imread(path)).copy()
            rgba[..., 3] *= pattern_opacity
            ax.imshow(rgba, extent=(.86, 1.025, -.10, 1.10), origin='upper', aspect='auto', zorder=1)
    y, x = np.mgrid[0:1:400j, 0:1:700j]
    alpha = (.38*np.exp(-((x-.99)/.23)**2-((y-.99)/.38)**2)
             + .18*np.exp(-((x+.06)/.22)**2-((y+.03)/.36)**2))
    gradient = np.empty((*alpha.shape, 4))
    gradient[..., :3] = to_rgb(t.accent); gradient[..., 3] = alpha
    ax.imshow(gradient, extent=(0, 1, 0, 1), origin='lower', aspect='auto', zorder=2)
    ax.set_in_layout(False)
    fig._procvetaev_background = ax
    return ax


def apply_style(name='neutral-light') -> StyleTokens:
    """Reset rc defaults, apply a full preset, and return immutable tokens.

    Existing artists are not recolored. Call before plt.subplots(); graph type,
    scales, data and layout remain the caller's responsibility.
    """
    try:
        t = STYLES[name]
    except KeyError:
        raise ValueError(f'Unknown style {name!r}; choose from {", ".join(STYLES)}') from None
    mpl.rcdefaults()
    if name == 'procvetaev':
        # Load the real upstream geometry; only approved palette/font/export overrides.
        mplstyle.use(str(Path(__file__).resolve().parents[1] / 'assets' / 'cyberpunk.mplstyle'))
        mpl.rcParams.update({
            'figure.facecolor': t.background, 'figure.edgecolor': t.background,
            'axes.facecolor': t.panel, 'axes.edgecolor': t.muted,
            'savefig.facecolor': t.background, 'savefig.edgecolor': t.background,
            'text.color': t.text, 'axes.labelcolor': t.text, 'axes.titlecolor': t.accent,
            'xtick.color': t.muted, 'ytick.color': t.text, 'grid.color': '#343434',
            'axes.prop_cycle': cycler(color=t.series), 'lines.color': t.accent,
            'patch.facecolor': t.accent, 'legend.labelcolor': t.text,
            'image.cmap': 'Greys',
            'font.family': 'sans-serif', 'font.sans-serif': [procvetaev_font('body').get_name(), 'DejaVu Sans'],
            'font.size': 13, 'axes.titlesize': 16, 'axes.labelsize': 12,
            'xtick.labelsize': 12, 'ytick.labelsize': 14,
            'figure.dpi': 160, 'savefig.dpi': 160, 'savefig.transparent': False,
            'pdf.fonttype': 42, 'svg.fonttype': 'none',
        })
        return t
    mpl.rcParams.update({
        'font.family': 'DejaVu Sans', 'font.size': 11, 'text.usetex': False,
        'text.color': t.text, 'figure.facecolor': t.background,
        'figure.edgecolor': t.background, 'axes.facecolor': t.panel,
        'axes.edgecolor': t.muted, 'axes.labelcolor': t.text,
        'axes.titlecolor': t.text, 'axes.titlesize': 15,
        'axes.titleweight': 'bold', 'axes.labelsize': 11,
        'axes.prop_cycle': cycler(color=t.series), 'axes.axisbelow': True,
        'axes.grid': t.grid, 'axes.grid.axis': 'x',
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.spines.bottom': False, 'axes.spines.left': False,
        'xtick.color': t.text, 'ytick.color': t.text,
        'xtick.labelsize': 10, 'ytick.labelsize': 11,
        'xtick.major.size': 0, 'ytick.major.size': 0,
        'xtick.minor.size': 0, 'ytick.minor.size': 0,
        'grid.color': t.muted, 'grid.alpha': .18,
        'grid.linewidth': .7, 'grid.linestyle': '-',
        'legend.facecolor': t.panel, 'legend.edgecolor': t.muted,
        'legend.labelcolor': t.text, 'legend.frameon': False,
        'legend.fontsize': 10, 'savefig.facecolor': t.background,
        'savefig.edgecolor': t.background, 'savefig.transparent': False,
        'figure.dpi': 150, 'savefig.dpi': 150,
        'lines.color': t.accent, 'patch.facecolor': t.accent,
    })
    return t


def delta_color(value, tokens: StyleTokens) -> str:
    """Positive/negative direction, not good/bad; zero/missing use neutral.

    None, NaN and infinities are treated as unavailable. Keep signs and values
    in the chart: color alone is insufficient.
    """
    if value is None or not isfinite(value):
        return tokens.neutral
    return tokens.positive if value > 0 else tokens.negative if value < 0 else tokens.neutral


@contextmanager
def style_context(name='neutral-light'):
    """Temporarily apply a preset and restore the previous rcParams on exit."""
    with mpl.rc_context():
        yield apply_style(name)
