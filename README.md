# Analytics Visual Skill

![Analytics Visual Skill](docs/banner.png)

Agent skill for designing data visualization with clear visual narrative.

Guides agents through choosing charts, arranging layouts, and connecting findings into visual reports. Produces ready-to-view PNG or JPEG images to attach in chat or use as local files, rather than only code or a separate SVG/HTML viewer.

## Install

### Hermes

```bash
hermes skills install tim-toothed/analytics-visual-skill/skills/analytics-visual --category data-science --yes
```

### OpenClaw, Claude Code and Codex

Requires Git and Python 3. Clone once, then run **one** installer command for your agent (`python3` may be needed instead of `python`):

```bash
git clone https://github.com/tim-toothed/analytics-visual-skill.git
cd analytics-visual-skill
python install.py --target openclaw
python install.py --target claude-code
python install.py --target codex
```

| Target | User-level package location |
| --- | --- |
| OpenClaw | `~/.openclaw/skills/analytics-visual` |
| Claude Code | `~/.claude/skills/analytics-visual` |
| Codex | `~/.agents/skills/analytics-visual` |

`~` is your user home on Windows, macOS or Linux. The stdlib-only installer copies the complete skill package, including scripts, references, fonts and assets; it does not install dependencies. Existing installs are refused unless you explicitly pass `--force` (replaces the package and discards local edits). `--dest "<skills-root>"` overrides the parent skills directory for a custom profile, project or isolated check; it still appends `analytics-visual`.

OpenClaw also documents native local installation: `openclaw skills install ./skills/analytics-visual --as analytics-visual --global`. For non-default OpenClaw profiles, use its profile-aware native installer or an explicit `--dest` instead of assuming the default home directory.

Start a new agent session, then ask it to use **Analytics Visual Skill** to render the bundled synthetic example and inspect the resulting image before delivery. Chat attachments depend on the host; local files remain usable without messenger integration.

Installation sources: [OpenClaw](https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md), [Claude Code](https://code.claude.com/docs/en/skills), [Codex](https://developers.openai.com/codex/skills).

Support level: the three Python installer targets have been verified in isolated directories on Windows, including complete file copies and no-overwrite behavior. The bundled example was rendered from an installed copy and visually inspected. Real-agent end-to-end discovery/delivery and Linux/macOS execution have not been run; installation support is not a claim of identical tool or attachment capabilities.

## Highlights

- **Visual storytelling.** Organize findings into a visual narrative the reader can follow.
- **Chart selection.** Choose charts for trends, comparisons, distributions, relationships, and composition.
- **Layout.** Arrange charts and annotations into dashboards and visual reports.
- **Nine styles.** Matplotlib presets with light, dark, muted, and high-contrast options.
- **Ready-to-share images.** Deliver PNG or JPEG files for chat attachments, documents or local viewing; Telegram is just one possible destination.

## Examples

Nine chart types in nine styles. All examples use synthetic data.

![Nine chart types in nine styles](docs/gallery.png)

Available styles: `neutral-light`, `minimal`, `dark`, `high-contrast`, `monochrome`, `muted`, `procvetaev`, `business-blue`, and `warm`.

Choose a style with your agent. Until you choose one, the skill uses `neutral-light`.

## How it works

The skill provides visualization guidelines and Python styling helpers. The agent writes and runs Matplotlib code for your task, then inspects the exported PNG or JPEG before delivering it.

Requires Python and Matplotlib. The skill includes instructions for running with `uv` when Matplotlib is not installed.

The [skill instructions](skills/analytics-visual/SKILL.md) map execution, image inspection and delivery to the host's available tools without changing the chart methodology.

## License

[MIT](LICENSE). Third-party asset and font terms are listed in [asset provenance](skills/analytics-visual/references/asset-provenance.md).
