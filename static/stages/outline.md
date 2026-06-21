# Stage 4 - Outline Planning

## Overview
Analyze extracted knowledge, identify thematic clusters, and plan the review structure. Then present the outline to the user and wait for confirmation.

## Output method
Build the outline directly from `knowledge.json` and the user's constraints. The LLM executes this stage directly. Do not call any legacy outline-planning script for this stage.

## Outline schema (see `schemas/outline.json`)
```json
{
  "title": "string (concise review title)",
  "sections": [
    {
      "index": 1,
      "title": "Introduction",
      "description": "Background, motivation, review scope, and organization",
      "estimated_words": 500,
      "estimated_refs": 5,
      "assigned_paper_ids": ["paperId1", "paperId2"]
    }
  ]
}
```

## Structural guidelines

### Course paper outline shape
1. Introduction
2. Theme A
3. Theme B
4. Theme C (optional)
5. Current challenges and open problems
6. Conclusion

### Undergraduate thesis outline shape
1. Introduction
2. Background and fundamentals
3. Theme A
4. Theme B
5. Theme C-D as needed
6. Comparative analysis
7. Challenges and future directions
8. Conclusion

## Thematic clustering
Group papers by `domain_tags` and `method_keywords`. Do not group sections by year or author.

## User checkpoint
Present the outline in this format:

```text
Draft outline:
1. Introduction (~500 words, ~5 references)
   Background, motivation, and review scope.
2. [Section title] (~800 words, ~8 references)
   [One-sentence description]
...

Please confirm or modify this outline before I begin writing.
```

Do not proceed to Stage 5 until the user explicitly confirms the outline. If the user modifies the outline, update the outline object before continuing.

## Terminology ledger seed (zh mode)

While planning the outline, pre-seed the terminology ledger that `review_lock.md` will carry. Scan `knowledge.json` `method_keywords` and `domain_tags` for recurring technical terms that have a standard English abbreviation (e.g. 碳纳米管 -> CNT, 相对湿度 -> RH, 纤维素纳米纤维 -> CNF, 多壁碳纳米管 -> MWCNT).

Record each as `中文全称 -> ABBBR`. This ledger is the single source of truth for abbreviation use in Stage 6 and the Stage 8 consistency check: first mention writes `中文全称 (ABBR)`, every later mention uses `ABBR` only. See `static/fragments/language/zh.md`.
