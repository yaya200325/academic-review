# Stage 9 - Export to Word

## Overview

Compile the final review into a `.docx` Word document with embedded figures, tables, and a numbered reference list.

## Script Usage

```bash
python scripts/docx_export.py output/full_document.md output/review.docx
```

## Building the Abstract

If no abstract was drafted during Stage 6, generate it now:
- `zh`: 150 to 250 words or the local institutional equivalent for a short abstract
- `en`: 150 to 250 words covering background, scope, main findings, and conclusion

## Building the Keywords

`polished.md` typically has no keywords section, so Stage 9 must insert one. Derive 5-8 keywords from grounded sources, do not fabricate them:

- the terminology ledger in `review_lock.md` (canonical concepts, e.g. 纸基湿度传感器, 纤维素, 相对湿度)
- `knowledge.json` `domain_tags` and `method_keywords` (the most frequent, topic-defining ones)
- the confirmed outline section themes

Format:
- `zh`: `## 关键词` followed by a single line of terms separated by `；` or `、`, e.g. `纸基湿度传感器；纤维素；碳纳米管；柔性传感；呼吸监测`
- `en`: `## Keywords` followed by comma-separated terms

Write the keywords line as UTF-8 along with the rest of the file (see Hard Rules). A `?` run in this line means the write went through the wrong codec.

## Heading Language (zh vs en)

The four frame headings depend on `review_lock.md` `language`. Body section headings stay in whatever language Stage 6/8 wrote them.

| Heading | zh | en |
|---|---|---|
| Abstract | 摘要 | Abstract |
| Keywords | 关键词 | Keywords |
| References | 参考文献 | References |

Do not mix: a zh review must not carry `## Abstract` while its body uses `## 引言`. If Stage 6/8 already wrote Chinese body headings, keep them and only localize the four frame headings above.

## Building the Reference List

### Step 1: Extract all `paper_id` citations with a generic pattern

Use a generic pattern that catches bracketed citation placeholders while ignoring Markdown links and numeric citations.

### Step 2: Replace all instances globally

Replace each paper ID placeholder with its assigned numeric citation based on first appearance.

### Step 3: Verify no residual paper-ID citations remain

This is critical. If any unresolved paper IDs remain after conversion, export must stop.

### Step 4: Build the reference list from citation order

Reference order must follow citation order in the text, not the order in `knowledge.json`.

For each cited paper, pull fields from `knowledge.json`:
- `authors` (full list) — format `等` (zh) or `et al.` (en) only when there are more than three authors
- `title`
- `year`
- `doi` — append as `DOI: <doi>` only when non-empty

### Step 5: Merge consecutive citations

Examples:
- `[1][2][3] -> [1-3]`
- `[5][6][7][8] -> [5-8]`
- `[1][3][4] -> [1][3-4]`

### Step 6: DOI formatting

- Read `doi` from `knowledge.json` for each cited paper.
- If `doi` is non-empty, append `DOI: <doi>` (zh) or `DOI: <doi>` (en) to the entry.
- If `doi` is empty or missing, **omit the `DOI:` segment entirely**. Never emit a bare `DOI: ` tail.
- Do not reconstruct a DOI from `paper_id`. The `paper_id` replaces both `.` and `/` with `_`, which is lossy and cannot be reversed.

## Hard Rules

- Do not assign numbers from `knowledge.json` order
- Do not assign numbers from paper ID order, DOI order, or title order
- Citation numbers must follow first appearance in reading order
- Final citation blocks must never appear in descending or mixed order
- GB/T document-type markers such as `[J]`, `[M]`, `[D]`, `[CP]`, `[EB/OL]`, `[D/OL]` are not paper IDs and must be ignored during residual-citation checks
- Remove HTML audit comments before export if they do not belong in the final document body
- Replace internal Markdown links with plain text labels before export
- Write `output/full_document.md` as UTF-8. On Windows, a default-locale file handle (cp1252/gbk) silently replaces unencodable CJK characters with `?`, which then appears as literal `?` in the docx. Always use `open(path, "w", encoding="utf-8")` or an equivalent UTF-8 writer. After writing, re-read the file as UTF-8 and confirm the title and keywords lines are intact (no `?` runs); redo the write if they are not.

## Reference Formats

- `zh`: simplified numeric GB/T-style format
- `en`: IEEE-style numeric format

If a non-empty DOI is available, append it in a consistent format.

## Writing `output/full_document.md`

Assemble the final Markdown with the frame headings in the target language (see "Heading Language" above), the body sections, and the reference list. Write it as UTF-8 per the hard rules, then run the pre-export validation in `SKILL.md` Stage 9 before calling the converter.

## Figure and Table Embedding

The exporter embeds local figures from standard Markdown image syntax:

```markdown
![Figure 1 Caption](figures/fig_1.png)
```

Rules:
- image paths must be relative to `output/full_document.md`
- alt text becomes the caption
- Markdown tables are converted to Word tables
- citation superscripts inside table cells must render correctly

## Output

Report the output path clearly:

`Review exported to output/review.docx.`

The `.docx` file is the final deliverable.
