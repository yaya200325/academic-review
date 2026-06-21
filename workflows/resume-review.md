---
description: Phase B entry - resume review writing in a fresh chat after Phase A (Stage 1-4) completed in a previous session. Reads project state from disk and runs Stage 5-9 with no Phase-A context carry-over.
---

# Resume Review Workflow

> Standalone Phase-B entry. Run when Phase A (Stage 1-4) completed in a previous session and the user wants to continue with synthesis, writing, and export. Loads project state from disk and runs Stage 5-9 in a clean session.

This workflow is independent: it owns Phase B starting from a fresh chat with no upstream conversation context required.

## When to Run

Run this workflow when the user opens a new chat and asks to continue a previously prepared review.

## Step 1: Sanity check

Verify these Phase-A artifacts before doing anything else:

| File / Directory | Required | Reason |
|---|---|---|
| `output/review_lock.md` | Always | Writing contract; re-read before each section |
| `output/outline.json` | Always | Section structure |
| `output/knowledge.json` | Always | Paper corpus |
| `output/checkpoints/stage_3_extract.json` | Always | Confirms extraction completed |

If any required artifact is missing, report which one is missing and stop.

## Step 2: Load `SKILL.md`, proceed from Stage 5

Read:

```text
~/.codex/skills/academic-review/SKILL.md
```

Then continue the workflow directly from disk state:

- Read `output/review_lock.md`, `output/outline.json`, and `output/knowledge.json`
- Follow `SKILL.md` from Stage 5 onward
- Re-read `review_lock.md` before each section write (Stage 6)
- Run Stage 5 (Synthesize) -> Stage 6 (Draft) -> Stage 7 (Diagram/Table) -> Stage 8 (Polish) -> Stage 8.5 (Reference Validation) -> Stage 9 (Export)

## Step 3: Hand-back

When Stage 9 completes and `output/review.docx` is produced, the workflow ends. Report the export path to the user.
