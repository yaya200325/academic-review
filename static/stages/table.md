# Table Generation

> [!WARNING]
> Deprecated guidance. This file is retained only as a legacy placeholder.
> The current workflow does not use `needs_table`, `table_generator.py`, or any legacy table-generation script.
> Use `static/stages/diagram_table.md` and the Stage 7 instructions in `SKILL.md` instead.

## Current status
- Table planning and insertion happen only in Stage 7
- Tables are written directly as Markdown tables in `output/draft_full.md` or `output/full_document.md`
- `scripts/docx_export.py` converts those Markdown tables into Word tables
- Only include data supported by `draft_text.md` or `knowledge.json`
