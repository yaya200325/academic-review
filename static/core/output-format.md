# Output Format

## Final deliverable
A Word document (`.docx`) produced by `scripts/docx_export.py`.

## Document structure
1. **Title** - concise review title
2. **Abstract** - 150-250 words summarizing background, scope, main findings, and conclusion
3. **Keywords** - 5-8 terms (`关键词` / `Keywords`, matching the target language)
4. **Main body** - sections from the confirmed outline
5. **Conclusion** - summarizes main lines, open questions, and future directions
6. **References** - numbered list in citation order

The three frame headings (Abstract / Keywords / References) follow `review_lock.md` `language`:

| Section | zh | en |
|---|---|---|
| Abstract | 摘要 | Abstract |
| Keywords | 关键词 | Keywords |
| References | 参考文献 | References |

Body section headings stay in whatever language Stage 6/8 wrote them; do not mix an English frame heading with Chinese body headings in a zh review.

## Figures
- Format: PNG, embedded inline from local Markdown image paths
- Source: direct image generation during Stage 7
- Caption placement: below the figure
- zh caption: a Chinese-language figure caption in the local academic style
- en caption: `Figure X. [Caption]`

## Tables
- Format: Markdown tables in the review Markdown, rendered as Word tables by `scripts/docx_export.py`
- Caption placement: above the table
- zh caption: a Chinese-language table caption in the local academic style
- en caption: `Table X. [Caption]`
- Supported use: comparison tables grounded in `draft_text.md` or `knowledge.json`

## Citation style
- **zh mode**: GB/T 7714-2015 numeric format
- **en mode**: IEEE numeric format by default
- Reference list numbering follows first appearance in the text
- Author lists come from `knowledge.json` (full list); format `等` (zh) or `et al.` (en) only when there are more than three authors
- DOI is appended from `knowledge.json` `doi` only when non-empty; never emit a bare `DOI: ` tail

## Word document style
- Font: Times New Roman for English text and the configured Chinese body font for Chinese text
- Body: 12 pt, 1.5 line spacing
- Headings: bold, 14 pt (H1), 12 pt (H2)
- Page margins: 2.5 cm on all sides
- Rendering is handled by `python-docx` via `scripts/docx_export.py`

## File encoding
`output/full_document.md` must be written as UTF-8. On Windows a default-locale file handle silently replaces unencodable CJK characters with `?`, which then appears as literal `?` in the docx. Always use an explicit UTF-8 writer.
