# Stage 6 - Review Drafting

## Overview

Write the review prose section by section, guided by the synthesis notes from Stage 5. **Text only**: no figures or tables yet. Those belong to Stage 7. After writing each section, re-read `output/review_lock.md` to prevent specification drift.

## Read Before Writing

1. `output/review_lock.md` - contract, outline, terminology
2. `output/synthesis_notes.json` - what this section must say
3. `output/knowledge.json` - paper lookup and evidence source
4. `static/stages/style-guardrails.md` - sentence and expression audit checklist

---

## Writing Principles

### Synthesis Over Summary

Do not summarize papers sequentially. Compare and synthesize.

- **Bad**: "Chen et al. (2021) proposed method A. Wang et al. (2022) proposed method B."
- **Good**: "Methods A and B both address X, but they differ in their treatment of Y: A improves precision through one mechanism, whereas B trades some precision for lower computational cost."

### Citation Placeholder

Use `[PAPERID]` as the citation placeholder. These will be renumbered during export.

### Citation Style in Running Text

**Do not write full English paper titles in the body text.**

Incorrect:
- `"Paper Title Here" shows that ...`
- `The article "Another Paper Title" suggests ...`

Correct:
- `A study reports that [paper_1] ...`
- `Related work shows that [paper_2][paper_3] ...`
- `One dual-network study indicates that [paper_7] ...`

Rules:
- Full paper titles belong in the reference list, not the running prose
- Refer to papers by function, claim, or concise description rather than by title

### English Abbreviation Discipline (zh mode, mandatory)

Once an abbreviation is defined it must be used consistently; do not revert to the long form later.

- First mention: `中文全称 (ABBR)`, e.g. `碳纳米管 (CNT)`, `相对湿度 (RH)`
- Every subsequent mention: the abbreviation alone, e.g. `CNT`, `RH`
- Record each mapping in the terminology ledger (`review_lock.md`) so later sections stay consistent
- Never re-expand the same abbreviation in a later section, and never write the Chinese long form after the abbreviation has been introduced
- See `static/fragments/language/zh.md` for the full rule and exceptions

This is checked again in Stage 8.

---

## Anti-Homogeneity Rules

One of the most common failure modes is that every paragraph uses the same sentence pattern. Enforce the following paragraph by paragraph.

### R1. Use a Sentence-Role Toolbox, Not a Single Formula

Do not make every paragraph follow the exact same pattern such as:

`topic sentence -> comparison -> citation -> wrap-up`

Choose 3 to 4 opening roles from the toolbox in `style-guardrails.md`, and do not let adjacent paragraphs start with the same rhetorical role.

### R2. Limit Dialectical Openings

Openings such as:
- `The key is not X but Y`
- `The reason is not only ... but also ...`
- `The essential difference lies not in ... but in ...`

should appear **at most once per section**, and never in two adjacent paragraphs.

### R3. Limit Forced Synthesis Endings

Closings such as:
- `This shows that ...`
- `This means that ...`
- `Therefore, the real issue is not ... but ...`

should also appear **at most once per section**.

Practical rule: if one paragraph uses a dialectical opening and a synthesis-heavy ending, at least one of them should be revised.

### R4. Eliminate Empty Meta-Statements

Avoid vague formulations such as:
- `Related studies show ...`
- `Existing reviews commonly point out ...`
- `It is widely believed that ...`

Replace them with concrete, attributed claims.

---

## Evidence-Quality Enforcement

All evidence in `knowledge.json` is `abstract_only`. Therefore:

- Do **not** invent mechanism details from general background knowledge
- Do **not** turn likely inference into claimed paper evidence
- If evidence is insufficient, do one of two things:
  - downgrade the statement
  - delete the unsupported detail

### Explicitly Acknowledge Evidence Limits

If the required detail is not available from the abstract, say so explicitly. For example:

> "The specific mechanism of X is not available from the abstracts reviewed here and would require full-text analysis."

This is a strength, not a weakness.

---

## Special Rules for the Abstract

If the current section is `Abstract`:

### What the Abstract Must Contain

1. The topic
2. The scope or organizing principle
3. The main findings or trends
4. The significance

### What the Abstract Must Not Contain

Do not write meta-information such as:
- `This review is based on X papers`
- `This review discusses ...`
- `This paper is organized as follows`

Write directly about the topic itself, not about the review document.

### Format

- 200 to 300 words in Chinese mode, or 150 to 250 words in English mode
- Usually no citations
- No subheadings

---

## Per-Section Writing Loop

For each section:

1. Re-read `output/review_lock.md`
2. Re-read `style-guardrails.md`
3. Write the section prose in Markdown:
   - compare horizontally
   - avoid paper-by-paper listing
   - vary paragraph opening roles
   - support important claims with multiple citations when appropriate
   - do not insert figures or tables here
   - if a visual would help, leave a placeholder comment
4. Validate word count; if below 75% of target, expand
5. Self-check for violations of R1 to R4, evidence overreach, and repetitive rhetoric

### Assemble the Full Draft

After all sections are written, concatenate them and write `output/draft_text.md`.

---

## Post-Drafting Citation Audit

After assembling `output/draft_text.md`, audit which papers were actually cited and how many knowledge entries remain unused. This audit is not a hard gate, but it helps surface underused evidence before polishing.

Guidance on citation density:
- consensus claims: usually 3 to 5 papers
- comparison claims: 2 to 4 representative papers
- single, narrow findings: one citation may be enough

Do not force citations just to hit a quota. Quality matters more than count.

**Skip check**: If `output/draft_text.md` already exists, skip.

**Do not stop here.** Continue to Stage 7, Stage 8, and Stage 9.
