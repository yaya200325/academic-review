# Changelog

## [2.1.2] - 2026-06-20

### Changed - Figure generation visual standards

Overhauled SVG/image generation prompts to eliminate "PowerPoint-style" visual artifacts and align with academic journal illustration standards (Nature, Science, IEEE).

**Problem**: Generated figures had presentation-slide aesthetics:
- Bright accent colors (yellow `#E8A838`)
- Large corner radius (`4-6px`) creating cartoonish appearance
- Oversized typography (`16pt` in-figure titles)
- Insufficient anti-PPT constraints in prompts

**Changes**:

- **Color schemes (F.1)**: Replaced bright palettes with three journal-standard schemes:
  - Scheme A (Nature/Science): deep navy `#1F4E79` primary, eliminated yellow accent
  - Scheme B (IEEE/Elsevier): blue-gray `#2C3E50` primary, deep red accent for contrast only
  - Scheme C (Monochrome academic): grayscale hierarchy for mechanism diagrams
  - Added saturation limit: HSB < 60% to avoid bright colors
  - Accent colors now "sparingly" constrained to max 5% of visual elements

- **Typography (F.2)**: Removed in-figure titles (belongs in caption), reduced hierarchy to `11pt/9pt/8pt`, added WCAG AA contrast requirement (`4.5:1`)

- **Shape language (F.3)**: Reduced corner radius from `4-6px` to `2-3px` maximum, refined arrow hierarchy (`1.5px` primary / `1px` secondary with specific head sizes), added precise connection requirement

- **Layout (F.4)**: Added grid alignment rule (`8px` grid), whitespace discipline (max `70%` content density), explicit anti-scattering constraints

- **Generation parameters (F.5)**: Expanded from 6 bullet points to comprehensive specification with explicit exclusion list (no shadows, gradients, textures, 3D effects, icon library elements, glossy surfaces)

- **Design principles (F.0)**: Added "anti-pattern" section explicitly listing PPT-style elements to avoid (bright accent colors, large radius, drop shadows, clipart, gradient fills)

- **Prompt templates (H)**: Completely rewritten with:
  - Inline hex color specifications
  - "Nature/Science journal figure style" reference anchor
  - Strict exclusions section in every template
  - Content verification checklist for mechanism schematics
  - SVG preferred over PNG for vector quality

- **Image Generation Guidance**: Added "Reference style" requirement, expanded exclusions, defined quality targets ("could appear in Nature/Science/IEEE without visual editing")

### Modified Files

- `static/stages/diagram_table.md` (sections F.0, F.1, F.2, F.3, F.4, F.5, H, Image Generation Guidance)

### No Breaking Changes

- Stage 7 execution flow unchanged
- Output file paths and Markdown embedding unchanged
- Quality verification protocol unchanged

## [2.1.1] - 2026-06-20

### Fixed - Export integrity (zh mode)

Three defects surfaced in a zh course-paper export (`output/full_document.md` / `review.docx`):

1. **Frame headings not localized.** Stage 9 wrote `## Abstract`, `## Keywords`, `## References` even when `review_lock.md` had `language: zh`, so an otherwise Chinese document carried English section headings mid-stream.
2. **Title and keywords rendered as `?`.** `full_document.md` was written through a Windows default-locale (cp1252/gbk) file handle, which silently replaced unencodable CJK characters in the agent-assembled title and keywords lines with `?`. Those `?` then became literal in the docx. The body paragraphs survived only because they were copied verbatim from the UTF-8 `polished.md`.
3. **Reference DOI tail empty.** `knowledge.json` had no `doi` field (Stage 3 schema omitted it), so Stage 9 emitted `DOI: ` with nothing after it for all 12 entries, even though `retrieved_papers.json` carried the DOIs and Stage 8.5 verified them.

### Changed

- **Stage 3 schema (`SKILL.md`, `static/stages/extraction.md`)**: added a mandatory `doi` passthrough from `retrieved_papers.json`. `paper_id` is explicitly called out as a lossy transform of the DOI (both `.` and `/` -> `_`) that cannot be reversed, so the real DOI must be carried separately. `authors` is now the full list (was "first 3 only") so Stage 9 can apply `等` / `et al.` correctly.
- **Stage 9 (`SKILL.md`, `static/stages/export.md`, `static/core/output-format.md`)**: frame headings (Abstract / Keywords / References) now follow `review_lock.md` `language` (`摘要` / `关键词` / `参考文献` for zh). Body headings are left in the language Stage 6/8 wrote them. Reference list reads `doi` from `knowledge.json` and appends `DOI: <doi>` only when non-empty; a bare `DOI: ` tail is forbidden. Added a hard rule and a write-and-verify step that `full_document.md` must be written as UTF-8, with a post-write re-read confirming the title and keywords lines contain no `?`.
- **Pre-export validation (`SKILL.md`)**: added checks for `?` runs in the title/keywords, language-matched reference heading, and no bare `DOI: ` tails.

### Added - Abbreviation discipline (zh mode)

Review prose defined abbreviations like `碳纳米管 (CNT)` but then reverted to the Chinese long form in later sections, defeating the abbreviation.

- **`static/fragments/language/zh.md`**: new "English abbreviation discipline" rule. First mention writes `中文全称 (ABBR)`; every later mention uses `ABBR` only. Mapping is recorded in the terminology ledger. Exceptions documented (single-use terms, already-short forms, dense table/caption sites).
- **`static/stages/drafting.md`**: Stage 6 enforces the rule and points at the ledger.
- **`static/stages/style-guardrails.md`**: new section 6.1 gives Stage 8 a concrete diagnostic scan (for each defined `(ABBR)`, check the Chinese long form does not reappear after the definition site) with fix examples.
- **`static/stages/outline.md`**: Stage 4 now pre-seeds the terminology ledger from `knowledge.json` `method_keywords` / `domain_tags` so abbreviations are decided before drafting begins.

### Modified Files

- `SKILL.md` (version bump, Stage 3 schema, Stage 9 structure + validation + UTF-8 write rule)
- `manifest.yaml` (version bump)
- `static/stages/extraction.md` (doi + full authors passthrough)
- `static/stages/export.md` (heading language table, DOI step, UTF-8 hard rule, writing section)
- `static/stages/outline.md` (terminology ledger seed)
- `static/stages/drafting.md` (abbreviation discipline)
- `static/stages/style-guardrails.md` (section 6.1 abbreviation consistency)
- `static/fragments/language/zh.md` (abbreviation discipline)
- `static/core/output-format.md` (heading language table, DOI note, file encoding note)

### No Breaking Changes

- `output/*.json` shapes gain optional/expected fields (`doi`, full `authors`); older knowledge files still load, they just yield empty-DOI reference entries until Stage 3 is rerun.
- `docx_export.py` is unchanged; it already reads UTF-8 and already keys reference-heading detection on both `参考文献` and `References`.

## [2.1.0] - 2026-06-18

### Changed - Architecture Upgrade

**Pipeline stages: 8 -> 9**

```text
v2.0:
Stage 6: Draft (writing and figures/tables generated together)
Stage 7: Polish
Stage 8: Export

v2.1:
Stage 6: Draft (text only)
Stage 7: Diagram/Table (global post-draft visual insertion)
Stage 8: Polish
Stage 9: Export
```

### Rationale

In v2.0, Stage 5 decided `needs_diagram` and `needs_table` before the review had
been fully written. That design had three practical weaknesses:

1. figure planning was inaccurate before the whole article existed
2. writing quality suffered because prose and visual placement competed for attention
3. visual density became uneven across sections

The v2.1 improvement is to separate prose drafting from visual generation:

- **Stage 6** focuses on writing strong prose and may leave placeholders
- **Stage 7** reads the complete draft and decides visual placement globally

Benefits:
1. better global optimization
2. smoother writing flow
3. more controllable visual density

### Modified Files

- `SKILL.md`
  - updated pipeline overview from 8 to 9 stages
  - removed `needs_diagram` and `needs_table` from Stage 5
  - made Stage 6 text-only
  - added Stage 7 as a dedicated visual integration stage
  - shifted later stage numbering accordingly
  - updated global execution discipline
  - updated static resource references

- `README.md`
  - updated workflow description
  - clarified the role of Stage 7

- `static/stages/diagram_table.md`
  - added the full decision framework for figures and tables
  - added density guidance
  - added figure type guidance
  - added integration and quality checklist guidance

### No Breaking Changes

- Existing `output/*.json` file shapes remain usable
- `docx_export.py` remains the only export script
- Stages 1 to 5 remain logically consistent
- User input parameters are unchanged

## [2.0.0] - 2026-06-17

### Added

- Initial pure-skill architecture
- Eight-stage pipeline: Search -> Screen -> Extract -> Outline -> Synthesize -> Draft -> Polish -> Export
- Direct execution from `SKILL.md`
- One production script: `docx_export.py`

### Design Decisions

- Search source: Semantic Scholar
- Knowledge extraction: abstracts only
- Visuals: direct image generation plus Markdown tables
- Output: `.docx` with Chinese and English font handling
