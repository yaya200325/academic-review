# Stage 2 - Relevance Screening

## Overview
Score each retrieved paper for relevance to the review topic. Keep papers with `relevance_score >= 0.6`.

## Scoring scale
| Score | Meaning |
|-------|---------|
| 0.9-1.0 | Directly and centrally addresses the review topic |
| 0.7-0.8 | Strongly relevant, covers key aspects |
| 0.6-0.7 | Relevant, useful to keep |
| 0.4-0.5 | Marginal, only tangentially related |
| 0.0-0.3 | Not relevant or wrong domain |

## Screening method
Evaluate each paper directly from its title and abstract. The LLM executes this stage directly. Do not call any deleted screening script.

## Threshold
Keep papers with `relevance_score >= 0.6`.

## Retry logic
If the kept count is still below the user's requested reference count:
1. Compute the gap
2. Run one additional search for roughly `gap * 2` more papers
3. Screen the new papers the same way
4. Merge and deduplicate the kept set

Execute this retry logic at most once. Do not loop indefinitely.

## Deduplication
Deduplicate by this priority:
1. Stable paper identifier
2. DOI
3. Normalized title + year

## After screening
- Write kept papers to `output/screened_papers.json`
- Report the count in plain language, for example: `Kept 28 papers with relevance >= 0.6 out of 41 retrieved.`
- Pass the kept papers list to Stage 3
