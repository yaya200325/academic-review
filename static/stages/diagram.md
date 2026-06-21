# Diagram Generation

> [!WARNING]
> Deprecated guidance. This file is retained only as a legacy placeholder.
> The current workflow does not use Mermaid, `needs_diagram`, or any legacy diagram helper script.
> Use `static/stages/diagram_table.md` and the Stage 7 instructions in `SKILL.md` instead.

## Current status
- Figure planning and insertion happen only in Stage 7
- Figures are inserted as Markdown images such as `![图 X 标题](figures/fig_X.png)`
- `scripts/docx_export.py` embeds those local PNG figures into the final Word document
- Only include content grounded in `draft_text.md` or `knowledge.json`
