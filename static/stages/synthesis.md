# Stage 5 — Per-Section Synthesis

## Overview
For each confirmed section, generate structured synthesis notes before writing any prose. This intermediate step ensures the writing stage has a clear analytical foundation.

## Output method
Generate the synthesis notes directly in Markdown/JSON-compatible structure. Do not call any legacy helper script for this stage.

## Synthesis note schema (see schemas/synthesis.json)
```json
{
  "section_title": "string",
  "core_claims": ["3–5 key claims supported by papers in this section"],
  "method_groups": [
    {"name": "group name", "papers": ["paper_id1", "paper_id2"]}
  ],
  "consensus_points": ["points where papers broadly agree"],
  "controversies": ["disagreements or debates in the literature"],
  "evidence_gaps": ["what is unknown, understudied, or not covered by available abstracts"],
  "representative_refs": ["paper_id list — the most important 5–10 papers to cite in this section"],
  "word_count_target": 800
}
```

## Visual decision policy
Do not decide figure or table placement in Stage 5. Stage 7 reads the complete draft and decides visual placement globally after the prose exists.

## Process all sections
Generate synthesis notes for every section in the confirmed outline before moving to Stage 6. This gives a complete analytical picture before prose writing begins.

## Citation Coverage Audit (Post-synthesis check)

After generating synthesis notes for all sections, audit how many papers from `knowledge.json` were assigned:

```python
total_papers = len(knowledge)
assigned_papers = set()

for section in synthesis_notes.values():
    assigned_papers.update(section.get("representative_refs", []))

coverage = len(assigned_papers) / total_papers if total_papers > 0 else 0
unused_papers = set(knowledge.keys()) - assigned_papers

print("Citation Coverage Audit:")
print(f"  Total papers in knowledge.json: {total_papers}")
print(f"  Papers assigned to sections: {len(assigned_papers)} ({coverage:.1%})")
print(f"  Unused papers: {len(unused_papers)}")

if coverage < 0.50:
    print("  ⚠️ Coverage is low (< 50%)")
    print("     Consider reviewing unused papers and integrating valuable ones")
    print()
    print("  Unused papers:")
    for paper_id in list(unused_papers)[:10]:
        paper = knowledge[paper_id]
        print(f"    - [{paper_id}] {paper['title'][:60]}...")
    if len(unused_papers) > 10:
        print(f"    ... and {len(unused_papers) - 10} more")
elif coverage >= 0.60:
    print("  ✅ Coverage is adequate (>= 60%)")
else:
    print("  ℹ️ Coverage is acceptable (50-60%)")
```

Interpretation:
- `< 50%`: Low coverage. Review unused papers; some may contain valuable findings.
- `50-60%`: Acceptable. Some papers may be tangential or lower quality.
- `>= 60%`: Good coverage. Most valuable papers are being used.

Note: This is an audit metric, not a blocking gate. Use professional judgment.
