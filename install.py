"""Install the complete skill package; no runtime dependencies are installed."""
import argparse
from pathlib import Path
import shutil


ROOTS = {
    'openclaw': '.openclaw/skills',
    'claude-code': '.claude/skills',
    'codex': '.agents/skills',
}
NAME = 'analytics-visual'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=ROOTS, required=True)
    parser.add_argument('--dest', type=Path,
                        help='Override skills root (package is copied into ROOT/analytics-visual)')
    parser.add_argument('--force', action='store_true',
                        help='Replace an existing analytics-visual package, discarding local changes')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent / 'skills' / NAME
    root = (args.dest or Path.home() / ROOTS[args.target]).expanduser().resolve()
    destination = root / NAME
    # Never allow a forced install to delete the source tree or recurse into it.
    resolved = destination.resolve()
    if resolved == source or source in resolved.parents or resolved in source.parents:
        parser.error('Destination must not overlap the source package')
    if not (source / 'SKILL.md').is_file():
        parser.error(f'Source package not found: {source}')
    if destination.is_symlink():
        parser.error(f'Refusing a symlink destination: {destination}')
    if destination.exists():
        if not args.force:
            parser.error(f'Already exists: {destination}; use --force to replace it')
        if not destination.is_dir():
            parser.error(f'Destination is not a directory: {destination}')
        shutil.rmtree(destination)
    shutil.copytree(source, destination,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo'))
    print(f'Installed for {args.target}: {destination}')
    print('No dependencies installed. Start a new agent session to load the skill.')


if __name__ == '__main__':
    main()
