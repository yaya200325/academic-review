# Stage 8 - Polishing

## Overview

Audit the complete draft for structural, logical, and stylistic issues, then apply **targeted sentence-level fixes only**. Maximum 2 iterations.

**Constraint**: This stage does **not** rewrite paragraphs or restructure sections. It identifies problems, outputs a diagnostic report, and applies conservative sentence-level fixes.

---

## Workflow: Diagnose -> Report -> Fix

### Step 1: Diagnose the Main Failure Mode

Before editing, identify the **primary failure mode** using the priority hierarchy from `style-guardrails.md`:

```text
outline fit -> section job -> paragraph logic -> claim/evidence/boundary -> terminology -> sentence style
```

Do not sentence-polish a draft whose section job is wrong. Surface structural problems first, then fix sentence-level issues.

Read these files before diagnosing:
1. `output/draft_full.md` (or `polished.md` if re-iterating)
2. `output/review_lock.md`
3. `static/stages/style-guardrails.md`

### Step 2: Output Diagnostic Report to `output/polish_audit.md`

The report must be structured. Include:

- detected primary failure mode
- quantitative metrics
- issues by category
- recommended fixes
- issues intentionally left unresolved

Suggested metrics:
- total paragraph count
- percentage of dialectical openings
- count of forced synthesis endings
- count of empty meta-statements
- suspected evidence-free mechanism claims

### Step 3: Apply Targeted Fixes

Allowed fixes:
- replace overloaded dialectical openings with direct statements
- delete forced synthesis endings when overused
- replace empty meta-statements with specific claims
- delete or downgrade mechanism claims lacking abstract support
- unify terminology
- fix grammar and register issues

Not allowed:
- reordering sentences inside a paragraph
- changing the paragraph's main claim wholesale
- adding or removing paragraphs
- restructuring section flow

Fix each problem paragraph once, then move on.

### Step 4: Re-Audit (Iteration 2, Optional)

After the first pass, re-run the diagnostic. If meaningful issues remain, perform one more pass. Maximum 2 iterations total.

---

## Priority Checklist Per Audit Pass

| Priority | Issue type | What to check |
|---|---|---|
| P0 | outline fit | all planned sections present, no major drift |
| P1 | section job | introduction, body, and conclusion do their correct jobs |
| P2 | paragraph logic | clear paragraph claims, no sequential summary drift |
| P3 | claim/evidence | claims cited, citations support claims, no invented mechanisms |
| P4 | terminology | canonical terms used consistently |
| P5 | sentence style | repetitive openings, repetitive endings, empty meta-statements |

---

## Output

Write the polished draft to `output/polished.md`.

**Skip check**: If `output/polished.md` exists, skip.

**Do not stop here.** Continue to Stage 8.5 and Stage 9.
