---
name: academic-review
description: End-to-end literature review skill for undergraduate course papers and thesis reviews. Runs a full pipeline: search Semantic Scholar, screen relevance, extract knowledge from abstracts, plan the outline with user confirmation, synthesize per-section notes, draft review prose, generate figures and tables on demand, polish the draft, validate references, and export a Word document. Trigger on literature review, review paper, undergraduate thesis review, academic review writing, and similar requests.
version: 2.1.2
author: academic-review skill
---

# Academic Review Skill

> [!NOTE]
> ## Final Deliverable
>
> **What the user expects**: A complete Word document (`output/review.docx`) containing:
> - Structured review text (introduction, body sections, conclusion)
> - Embedded generated figures and comparison tables
> - Polished prose with consistent terminology
> - Properly formatted citations and reference list
> - Academic formatting (Chinese body font / Times New Roman, first-line indent, three-line tables)
>
> **Your mission**: Execute **all 9 stages** to produce this deliverable.  
> **Stage 6 is not the end**. It is only the text draft. You must continue through Stage 7 (figures/tables), Stage 8 (polish), Stage 8.5 (reference validation), and Stage 9 (export docx).

> [!NOTE]
> ## Your Role: Orchestrator, Not Implementer
>
> You are the **workflow orchestrator**. Your job is to:
> - Execute each stage's logic directly
> - Call existing tools when they exist
> - Avoid reimplementing production-ready components
>
> **Tools available**:
> - `scripts/docx_export.py` - Production-ready Markdown-to-Word converter that handles formatting, fonts, local figure embedding, and table styling
> - Built-in capabilities such as search, fetch, read, write, and shell execution
>
> **Visual generation strategy**: This skill uses direct image generation for figures. Mermaid is not the primary figure path.
>
> **What you implement**: Stages 1 to 8.5  
> **What you call**: Stage 9 converter script

> [!CAUTION]
> ## Global Execution Discipline (Mandatory)
>
> **This workflow is a strict 9-stage pipeline. The following rules have highest priority. Violating any one is an execution failure.**
>
> 1. **Serial execution**. Stages must run in order: Search -> Screen -> Extract -> Outline [user confirms] -> Synthesize -> Draft -> Diagram/Table -> Polish -> Reference Validation -> Export
> 2. **Review lock per section**. Before writing each section in Stage 6, you must read `output/review_lock.md`. Writing rules, terminology, and constraints come from that file, not memory.
> 3. **No skipping stages**. Each stage writes its output file before the next stage begins. The workflow is not complete until Stage 9 produces `output/review.docx`.
> 4. **Blocking means hard stop**. Stage 4 is blocking. Present the outline and wait for explicit user confirmation before Stage 5.
> 5. **No invented content**. All claims must be traceable to papers in `output/knowledge.json`. Do not fabricate results, authors, journals, years, or DOIs.
> 6. **Checkpoint output required**. After Stages 2, 3, 4, 5, 6, 7, 8, and 8.5, write the required checkpoint files. On restart, inspect file existence and freshness before rerunning a stage.
> 7. **Diagram and table generation is deferred**. Stage 6 writes text only. Stage 7 analyzes the complete draft globally and inserts visuals afterward.
> 8. **Use existing tools**. All writing stages output Markdown. Stage 9 must call `scripts/docx_export.py`. Do not write custom docx export code.

> [!CAUTION]
> ## Content Integrity Red Lines
>
> These rules override the goal of "making the prose sound good." Violating them is hallucination.
>
> 1. **No mechanism fabrication**. If a mechanism detail such as attention calculation, layer count, or algorithm steps does not appear in the paper abstract recorded in `knowledge.json`, do not write it as fact. Either downgrade the wording or remove it.
> 2. **No ornamental citations**. Every `[PAPERID]` citation must support a specific claim. If removing the citation does not weaken the sentence, the citation is decorative and must be fixed or removed.
> 3. **Evidence quality enforcement**. All papers are treated as `evidence_quality: "abstract_only"` unless the workflow explicitly gathered more evidence. Do not present common-sense inference as the paper's finding.
> 4. **Acknowledge limits**. When abstracts lack detail, state that directly: "The specific mechanism of X is not available from the abstracts reviewed here."
>
> These rules apply in Stage 6 (drafting) and Stage 8 (polishing). See `static/stages/style-guardrails.md`.

---

## Pipeline Overview

```text
Stage 1   Search                -> output/retrieved_papers.json
Stage 2   Screen                -> output/screened_papers.json
Stage 3   Extract               -> output/knowledge.json
Stage 4   Outline               -> output/outline.json + output/review_lock.md   [USER CONFIRMS]
Stage 5   Synthesize            -> output/synthesis_notes.json
Stage 6   Draft                 -> output/draft_text.md                          (text only)
Stage 7   Diagram/Table         -> output/draft_full.md
Stage 8   Polish                -> output/polished.md + output/polish_audit.md
Stage 8.5 Reference Validation  -> output/reference_validation.md                [BLOCKS ON CRITICAL ISSUES]
Stage 9   Export                -> output/full_document.md + output/review.docx
```

**Phase A / Phase B split (optional)**: For large reviews (50+ references, 10k+ words), you can pause after Stage 4 and resume in a fresh conversation. See `workflows/resume-review.md`.

**Architecture principle**: Stages 6 and 7 separate text writing from visual generation. This lets the model inspect the complete draft before deciding where visuals genuinely help.

---

## How to Use

When the user requests a literature review, collect these parameters:

| Parameter | Example | Required |
|-----------|---------|----------|
| topic | "Applications of graph neural networks in recommender systems" | Yes |
| ref_count | 30 | Yes |
| word_count | 7000 | Yes |
| language | zh / en | Yes (default: zh) |
| paper_type | course_paper / undergraduate_thesis | No (default: course_paper) |

Then proceed through the full workflow through Stage 9.

---

## Stage 1: Search

**Goal**: Collect research papers on the topic.

**Method**:
- Use available search capabilities to find papers
- Search with the user's topic directly and expand with precise topic terms when needed
- Retrieve metadata: title, authors, year, abstract, DOI, URL
- Target `ceil(ref_count * 1.5)` papers

**Output**: Write to `output/retrieved_papers.json`

**Format**:
```json
[
  {
    "paper_id": "<unique_id>",
    "title": "...",
    "abstract": "...",
    "year": 2023,
    "authors": ["Alice", "Bob"],
    "doi": "10.1234/example",
    "url": "https://..."
  }
]
```

**Skip check**: If `output/retrieved_papers.json` exists, skip this stage.

---

## Stage 2: Screen

**Goal**: Score each paper for relevance on a 0-1 scale and keep papers with score >= 0.6.

**Process**:
1. Read `output/retrieved_papers.json`
2. For each paper, inspect title and abstract
3. Score using this rubric:
   - `0.9-1.0`: directly addresses the topic
   - `0.7-0.8`: strongly relevant
   - `0.6-0.7`: relevant
   - `0.4-0.5`: marginal
   - `0.0-0.3`: not relevant
4. Keep papers with score >= 0.6

**Target**: Aim for `ref_count`, but **accept any count >= ref_count**.

**Retry logic**:
- If kept count < `ref_count`:
  - Compute `gap = ref_count - kept_count`
  - Run Stage 1 one more time with about `gap * 2` additional papers
  - Merge and deduplicate by paper ID, DOI, or normalized title
- If kept count >= `ref_count`:
  - Keep them all
  - Do not truncate arbitrarily

**Rationale**: Relevance is the real filter. More relevant papers improve the review.

**Output**: Write to `output/screened_papers.json`

**Format**:
```json
[
  {
    "paperId": "...",
    "title": "...",
    "abstract": "...",
    "year": 2023,
    "authors": ["..."],
    "relevance_score": 0.85,
    "relevance_reason": "Directly addresses the topic"
  }
]
```

**Skip check**: If `output/screened_papers.json` exists, skip.

---

## Stage 3: Extract

**Goal**: Extract structured knowledge from abstracts.

**Process**:
1. Read `output/screened_papers.json`
2. For each paper, extract:
   - `core_contribution` (1-2 sentences)
   - `method_keywords` (key methods or techniques)
   - `result_summary` (main finding, <= 50 words)
   - `domain_tags` (tags for thematic grouping)
3. Pass through these fields verbatim from `retrieved_papers.json` (do not modify or truncate):
   - `doi` - the real DOI; never derive from `paper_id` (it is lossy)
   - `authors` - the full author list, in order
4. Always set `evidence_quality: "abstract_only"`

**Output**: Write to `output/knowledge.json`

**Format**:
```json
[
  {
    "paper_id": "abc123",
    "title": "...",
    "year": 2023,
    "authors": ["Alice", "Bob", "Charlie"],
    "doi": "10.1234/example",
    "core_contribution": "...",
    "method_keywords": ["GNN", "collaborative filtering"],
    "result_summary": "...",
    "domain_tags": ["recommender-systems", "graph-learning"],
    "evidence_quality": "abstract_only"
  }
]
```

**Skip check**: If `output/knowledge.json` exists, skip.

---

## Stage 4: Outline

**Goal**: Plan the review structure. **This stage is blocking.**

**Process**:
1. Read `output/knowledge.json`
2. Identify thematic clusters from `domain_tags` and `method_keywords`
3. Plan sections by theme, not by year or author
4. Include abstract as `sections[0]` when appropriate (estimated 200-300 words)
5. Estimate word count and reference count per section

**Output**: Write to `output/outline.json`

**Format**:
```json
{
  "title": "A Review of Graph Neural Networks in Recommender Systems",
  "sections": [
    {
      "index": 0,
      "title": "Abstract",
      "description": "Summarizes topic, major findings, and significance without meta-comments about the review document itself.",
      "estimated_words": 250,
      "estimated_refs": 0,
      "assigned_paper_ids": []
    },
    {
      "index": 1,
      "title": "Introduction",
      "description": "Research background, motivation, and scope of the review.",
      "estimated_words": 600,
      "estimated_refs": 5,
      "assigned_paper_ids": ["abc123", "def456"]
    }
  ]
}
```

**Present the outline to the user**:

```text
Draft outline:
0. Abstract (~250 words, no references)
   Summarizes the topic, major findings, and significance.
1. Introduction (~600 words, ~5 references)
   Research background, motivation, and scope.
2. ...

BLOCKING: Please confirm or modify this outline.
Type 'yes' to proceed, or provide modifications.
```

**After confirmation**, generate `output/review_lock.md`:

```markdown
# Review Execution Lock
<!-- Do not edit manually after confirmation. Re-read before every Stage 6 section. -->

## Contract
- topic: Graph neural networks in recommender systems
- language: zh
- paper_type: undergraduate_thesis
- total_words: 7000
- ref_count: 30

## Confirmed Outline
P01 Introduction (~600w, ~5 refs)
P02 Background and Fundamentals (~800w, ~6 refs)
...

## Writing Rules (must follow per section)
- Open each paragraph with a real thesis sentence, not "In this section..."
- Prefer horizontal comparison over paper-by-paper listing
- Important claims should be supported by multiple citations when the evidence allows
- Make consensus, controversy, and evidence gaps explicit

## Terminology Ledger
(To be accumulated and normalized during later stages)
```

**Skip check**: If both `output/outline.json` and `output/review_lock.md` exist, skip.

---

## Stage 5: Synthesize

**Goal**: Generate structured synthesis notes for each section, not prose yet.

**Process**:
1. Read `output/outline.json` and `output/knowledge.json`
2. For each section:
   - Collect assigned papers
   - Identify core claims, method groups, consensus, controversies, and evidence gaps
   - Select 5-10 representative papers to cite

**Output**: Write to `output/synthesis_notes.json`

**Format**:
```json
{
  "Introduction": {
    "section_title": "Introduction",
    "core_claims": ["...", "...", "..."],
    "method_groups": [{"name": "Graph-based methods", "papers": ["abc123", "def456"]}],
    "consensus_points": ["..."],
    "controversies": ["..."],
    "evidence_gaps": ["..."],
    "representative_refs": ["abc123", "def456", "ghi789"],
    "word_count_target": 600
  }
}
```

**Note**: Figure and table placement decisions are deferred to Stage 7.

**Skip check**: If `output/synthesis_notes.json` exists, skip.

---

## Stage 6: Draft

**Goal**: Write review prose section by section in Markdown. **Text only**.

**Critical rule**: Before writing **each** section, re-read `output/review_lock.md`.

**Process**:
1. Read `output/synthesis_notes.json`
2. Read `output/knowledge.json`
3. For each section:
   - Re-read `output/review_lock.md`
   - Read `static/stages/drafting.md`
   - Write prose in Markdown:
     - Use `[PAPERID]` citations
     - Compare horizontally, do not summarize sequentially
     - Open paragraphs with thesis sentences
     - Do not insert figures or tables yet
     - If a visual would help later, leave a placeholder comment such as:
       ```markdown
       <!-- VISUAL_PLACEHOLDER: flowchart showing GNN message passing -->
       ```
       or
       ```markdown
       <!-- VISUAL_PLACEHOLDER: comparison table of major GNN architectures -->
       ```
   - Validate word count; if below 75% of target, expand the section

4. Concatenate all sections into a full draft

**Output**: Write to `output/draft_text.md`

**Skip check**: If `output/draft_text.md` exists, skip.

**Do not stop here.** Stage 6 only produces the text draft.

---

## Stage 7: Diagram/Table

**Progress**: 6/9 complete. After this comes Stage 8.

**Goal**: Analyze the completed text draft and insert figures or tables where they improve comprehension.

**Process**:
1. Read `output/draft_text.md`
2. Read `output/knowledge.json`
3. Perform global analysis:
   - Identify abstract or dense sections that would benefit from visual support
   - Identify method comparisons suitable for tables
   - Identify processes, architectures, or concept relationships suitable for figures
   - Check `VISUAL_PLACEHOLDER` comments
   - Aim for 1 to 3 visuals per 2000 words

4. **Mandatory Stage 7 audit log**. Write this as an HTML comment at the top of `output/draft_full.md`:

```markdown
<!-- STAGE7_AUDIT
Image generation capability: [AVAILABLE | NOT_AVAILABLE]
Planned figures: N
Generated figures: M
Omitted figures: K

[If K > 0, list each:]
- Figure candidate: [description]
  Omit reason: [non-essential | generation failure | text already clear | capability unavailable]
  [If capability unavailable, include failure type:]
  Capability failure type: [tool_unavailable | permission_failure | generation_failure | file_not_created | file_write_failed]
  Failure detail: [specific error message]
-->
```

This audit block is mandatory. Missing it means Stage 7 is incomplete.

5. For each selected location, generate and insert:

**For figures**:
- Use direct image generation if available
- Do not use Mermaid as fallback
- Generate a PNG grounded only in claims supported by `draft_text.md` and `knowledge.json`
- Save to `output/figures/fig_X.png`
- Use relative Markdown paths such as `![Figure X caption](figures/fig_X.png)`
- Update surrounding prose so it explicitly refers to the figure
- Prompt constraints:
  - academic scientific illustration style
  - white background
  - restrained colors
  - clear hierarchy
  - no fabricated data, metrics, mechanisms, or labels

**For tables**:
- Build Markdown comparison tables from `knowledge.json`
- Add a caption line above the table
- Update surrounding prose so the table is discussed, not just inserted

6. **Numbering**: Assign sequential figure and table numbers.

7. **No Mermaid fallback**:
- If image generation is unavailable, do not replace figures with Mermaid
- Keep tables when useful
- For non-essential figures, remove the placeholder and continue
- For essential figures that are required for comprehension, stop and report the blocker

8. **Remove placeholders**: Delete all `VISUAL_PLACEHOLDER` comments.

**Output**: Write to `output/draft_full.md`

**Skip check**:
- If `output/draft_full.md` does not exist, run Stage 7
- If it exists, verify:
  - no `VISUAL_PLACEHOLDER` comments remain
  - no `IMAGE_GENERATION_PROMPT` comments remain
  - the Stage 7 audit comment is present
  - forward references to figures are matched by actual figure embeds
  - if there are zero figures, a clear explanatory note is present

If any check fails, re-run Stage 7.

**Do not stop here.** Continue to Stage 8 and Stage 9.

---

## Stage 8: Polish

**Progress**: 7/9 complete. After this comes Stage 8.5 and then Stage 9.

**Goal**: Diagnose structural and stylistic issues, then apply **sentence-level fixes only**. Maximum 2 iterations.

**Constraint**: This stage does **not** rewrite paragraph structure or reorganize sections. See `static/stages/polishing.md`.

**Process**:
1. Read `output/draft_full.md` (or `polished.md` when re-iterating)
2. Read `output/review_lock.md` and `static/stages/style-guardrails.md`
3. Diagnose the primary failure mode using this priority:
   ```text
   outline fit -> section job -> paragraph logic -> claim/evidence/boundary -> terminology -> sentence style
   ```
4. Output a diagnostic report to `output/polish_audit.md`:
   - quantitative metrics
   - issues by category
   - recommended fixes
5. Apply targeted sentence-level fixes:
   - reduce overloaded dialectical openings
   - delete forced synthesis endings when overused
   - replace empty meta-statements with concrete claims
   - delete or downgrade unsupported mechanism claims
   - unify terminology
   - do not reorder sentences or change paragraph structure
6. Optionally repeat once more, for a maximum of two iterations

**Outputs**:
- `output/polish_audit.md`
- `output/polished.md`

**Skip check**: If `output/polished.md` exists, skip.

**Do not stop here.** Continue to Stage 8.5 and Stage 9.

---

## Stage 8.5: Reference Validation

**Progress**: 8/9 complete. After this comes Stage 9.

**Goal**: Verify reference authenticity and citation format before export. This is a **quality gate**. Critical issues block Stage 9.

**Read full protocol**: `static/stages/reference_validation.md`

**Process**:
1. Read `output/knowledge.json`
2. Read `output/polished.md`
3. Read `output/review_lock.md`
4. Verify metadata authenticity:
   - papers with DOI -> CrossRef API
   - papers with arXiv ID -> arXiv API
   - papers with neither -> mark as "cannot verify"
5. Check citation-format consistency:
   - `zh`: GB/T 7714-style numeric references
   - `en`: IEEE-style numeric references
6. Write `output/reference_validation.md` with:
   - summary
   - detailed issues
   - recommendation

**Critical issues**:
- DOI returns 404
- year mismatch > 2 years
- title clearly refers to a different paper

**Warnings**:
- year mismatch within 1 year
- partial title mismatch
- incomplete author list
- cannot verify

**Decision**:
- If critical issues exist, show the report and ask before export
- If only warnings exist, proceed automatically

**Skip check**: If `output/reference_validation.md` exists and is newer than `output/polished.md`, skip.

**Do not stop here.** Continue to Stage 9.

---

## Stage 9: Export

**Progress**: Final stage.

**Goal**: Prepare the final Markdown document and call the Word converter.

**Critical rule**: Do **not** write custom conversion code. Use `scripts/docx_export.py`.

**Process**:
1. Read `output/polished.md`
2. Read `output/knowledge.json`
3. Extract the abstract from the first section (`## Abstract` / `## 摘要` or equivalent)
4. Renumber citations in order of first appearance:
   - initialize `citation_map = {}`
   - scan from top to bottom
   - assign numbers on first appearance
   - replace all `[PAPERID]` with numeric citations
5. Normalize and merge consecutive citation blocks:
   - sort numeric blocks in ascending order
   - merge true consecutive runs such as `[1][2][3] -> [1-3]`
6. Build the reference list:
   - `zh`: numeric GB/T-style simplified format, `等` after more than three authors
   - `en`: numeric IEEE-style simplified format, `et al.` after more than three authors
   - Append `DOI: <doi>` only when `knowledge.json` has a non-empty `doi` for that paper. Never emit a bare `DOI: ` tail.
7. Build `output/full_document.md`

**Required final structure**:

Section heading language is decided by `review_lock.md` `language`. Preserve the Chinese section headings that Stage 6/8 already wrote (摘要, 引言, …, 结论). Only the four standardized frame headings below differ by language:

```text
zh:
# {title}
## 摘要
## 关键词
{remaining sections, Chinese headings}
## 参考文献

en:
# {title}
## Abstract
## Keywords
{remaining sections, English headings}
## References
```

**Heading rule**: do not swap an existing Chinese body heading such as `## 引言` for `## Introduction` mid-document. The frame headings (Abstract/Keywords/References) follow `language`; body headings stay in whatever language Stage 6/8 wrote them.

**Pre-export validation**:
- title is not empty
- title and keywords line contain no `?` characters (a `?` run indicates a UTF-8 write failure)
- keywords exist
- abstract was extracted successfully
- reference section header matches the target language (摘要/参考文献 for zh, Abstract/References for en)
- all reference entries have a DOI when `knowledge.json` records one; none end with a bare `DOI: `
- all figure files exist
- figure numbering is sequential
- table numbering is sequential
- no placeholder comments remain
- image paths are relative

If any field is empty, derive it from available structured inputs. Do not leave placeholders.

8. Write `output/full_document.md` **as UTF-8**. This is mandatory on Windows: writing through a default-locale (cp1252/gbk) file handle silently replaces unencodable CJK characters with `?`, which then becomes literal `?` in the exported docx. Use `open(path, "w", encoding="utf-8")` or an equivalent UTF-8 writer; never rely on the OS default encoding. After writing, re-read the file as UTF-8 and confirm the title and keywords lines are intact (no `?`); if they are not, the write went through the wrong codec and must be redone.
9. Call the converter:
   ```bash
   python scripts/docx_export.py output/full_document.md output/review.docx
   ```

**What the converter handles automatically**:
- font application
- local PNG embedding
- Markdown table conversion
- citation superscripting
- first-line indent
- automatic table of contents
- heading styles

**Output**: `output/review.docx`

**Report to the user**: `Review exported to output/review.docx.`

---

## Phase A / Phase B Split (Optional)

For large reviews, you may split execution:

**Phase A** (Stages 1-4):
- run until outline confirmation
- write `output/review_lock.md`, `output/outline.json`, and `output/knowledge.json`
- tell the user how to continue in a fresh chat

**Phase B** (Stages 5-9):
- detect the existing lock, outline, and knowledge files
- resume from Stage 5

See `workflows/resume-review.md`.

---

## Tools (Python Scripts)

**Important**: The converter script is production-ready and feature-complete. Do not attempt to rebuild Markdown-to-docx export in the workflow itself.

| Script | Purpose | Usage |
|--------|---------|-------|
| `docx_export.py` | Markdown-to-Word converter with academic formatting | `python scripts/docx_export.py <input.md> <output.docx>` |

All other tasks are executed directly by the agent.

---

## Static Resources

Load these on demand per stage:

| Resource | When to Load |
|----------|--------------|
| `static/core/stance.md` | Always at start |
| `static/core/pipeline.md` | Always at start |
| `static/fragments/paper_type/<type>.md` | After collecting parameters |
| `static/fragments/language/<lang>.md` | After collecting parameters |
| `static/stages/style-guardrails.md` | Stage 6 and Stage 8 |
| `static/stages/drafting.md` | Stage 6 |
| `static/stages/diagram_table.md` | Stage 7 |
| `static/stages/polishing.md` | Stage 8 |
| `static/stages/reference_validation.md` | Stage 8.5 |
| `static/stages/export.md` | Stage 9 |

`style-guardrails.md` is the shared diagnostic checklist used both during drafting and polishing.

---

## Why This Design

- The workflow is LLM-orchestrated rather than script-orchestrated
- `review_lock.md` prevents specification drift during long drafting runs
- Checkpoint files support restart and continuation
- Markdown is the intermediate format for all content stages
- Phase A / Phase B split allows context reset for very large reviews
- Decoupled visual generation lets the model place figures and tables only after the full argument is visible
