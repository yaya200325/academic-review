# Style Guardrails

> Use this checklist after drafting each paragraph in Stage 6 and when diagnosing the draft in Stage 8.
> These are mechanical expression-level checks. They are meant for careful sentence refinement, **not** for rewriting whole paragraphs or restructuring sections.
>
> One of the most common failure modes in this skill is that the entire document sounds like one person repeating the same sentence pattern. This checklist exists to break that homogeneity.

---

## 0. Diagnostic Order

Before editing sentences, identify the **primary failure mode** and fix in this order:

```text
outline fit -> section job -> paragraph logic -> claim/evidence/boundary -> terminology -> sentence style
```

Do not polish sentence texture on a structurally wrong draft. Surface structural problems first in `polish_audit.md`.

---

## 1. Sentence Homogeneity

The typical pathology is overuse of **dialectical openings** or **forced synthesis endings**. Count them before editing.

### 1.1 Overloaded Dialectical Openings

The following opening styles should appear **at most once per section**, and never in adjacent paragraphs:

| Problematic opening | Better replacement |
|---|---|
| `... is not X but Y` | Use a direct definition, evidence statement, or example |
| `The reason is not only ... but also ...` | Remove the setup and state the conclusion with evidence |
| `... is essentially ...` | Replace with a concrete action or result statement |
| `The essential difference lies not in ... but in ...` | State the difference directly |

**Soft threshold**: if more than 30% of paragraphs use openings like `not`, `essential`, `key`, or `the reason`, reduce the density.

### 1.2 Forced Synthesis Endings

The following closing styles should appear **at most once per section**:

| Problematic ending | Better replacement |
|---|---|
| `This shows that ...` | Remove it or replace it with the actual finding |
| `This means that ...` | Replace with a concrete implication |
| `Therefore, the issue is not ... but ...` | Usually redundant if the paragraph already made the point |

If a paragraph uses both a dialectical opening and a forced synthesis ending, revise at least one of them.

---

## 2. Sentence-Role Toolbox

Do not make every paragraph follow the same rhetorical template. Alternate among these roles:

| Role | Function | When to use it |
|---|---|---|
| Definition sentence | Establish a concept boundary | When introducing a new term |
| Evidence sentence | State a concrete paper finding | When the abstract supports a specific claim |
| Comparison sentence | Contrast two methods or groups | When tradeoffs or disagreements exist |
| Example sentence | Ground an abstract claim | When the prose risks becoming vague |
| Concession sentence | Acknowledge a limit before advancing | When evidence boundaries matter |
| Closing sentence | Summarize the paragraph conclusion | Use sparingly |

Adjacent paragraphs should not open with the same role.

---

## 3. Empty Meta-Statements

Replace vague generalizations with concrete evidence-bearing claims.

| Empty expression | Better replacement |
|---|---|
| `Related studies show ...` | `X et al. [cite] report that ...` |
| `Existing reviews point out ...` | `A prior review [cite] argues that ...` |
| `It is widely believed ...` | Delete it or specify who holds the view and why |
| `The literature shows ...` | Tie the claim to specific papers and a specific conclusion |

Diagnostic rule: if a sentence still works after removing the citation because it is merely common knowledge, the citation may be decorative rather than evidentiary.

---

## 4. Evidence Boundaries

All entries in `knowledge.json` are `abstract_only`. Therefore:

- do not infer missing implementation details as fact
- do not describe mechanism details that are absent from the abstract
- if support is insufficient, downgrade or delete

This is not about writing less. It is about writing only what the evidence supports.

---

## 5. Citation Support Check

Every `[PAPERID]` citation should answer this question:

> What specific claim does this citation support?

Common problems:

| Problem | Fix |
|---|---|
| Broad claim followed by 3 unrelated citations | Narrow the claim to the overlap those papers actually support |
| Citation does not map to a specific claim | Remove the citation or rewrite the sentence |
| Same claim gets repeated with redundant citations | Deduplicate |

---

## 6. Academic Register and Mechanical Checks

- Avoid conversational filler and inflated praise
- Expand abbreviations on first use
- Keep terminology consistent across the full document
- Prefer one main proposition per sentence
- Do **not** alter citation markers, figure captions, or reference entries casually

### 6.1 Abbreviation Consistency (zh mode)

After an abbreviation is introduced with `中文全称 (ABBR)`, every later mention must use the abbreviation only. Reverting to the Chinese long form after definition (e.g. writing `碳纳米管` again after `碳纳米管 (CNT)` was already given) is an inconsistency that must be fixed.

Diagnostic rule: for each `(ABBR)` defined in the document, scan the rest of the text. If the corresponding Chinese long form appears again after the definition site, replace it with the abbreviation (unless it is the one allowed re-use at the definition site itself, or an exception listed in `static/fragments/language/zh.md`).

Common fixes:
- `碳纳米管` after `碳纳米管 (CNT)` was defined -> `CNT`
- `相对湿度` after `相对湿度 (RH)` was defined -> `RH`
- a term defined once in the abstract and then re-expanded in the body -> keep the abbreviation in the body

---

## 7. AI Boundary

The model may control language, but it must not invent content.

| Allowed | Not allowed |
|---|---|
| grammar cleanup, clarity, sentence reshaping | fabricated citations or datasets |
| downgraded wording, hedging when needed | invented mechanisms stated as paper facts |
| terminology unification | exaggerated novelty or generality |

Hard rule: if a mechanism detail cannot be traced back to the corresponding paper in `knowledge.json`, delete it or downgrade it.

### Citation Style Rule for Chinese Reviews

In Chinese-body reviews, do not place full English paper titles inside running prose. Reserve titles for the reference list only.
