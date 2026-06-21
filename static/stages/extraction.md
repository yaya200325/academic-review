# Stage 3 - Knowledge Extraction

## Source: abstracts only
Extract all knowledge from the `abstract` field. Do not attempt to retrieve or infer full-text content. Abstract-level extraction is sufficient for undergraduate-level literature reviews.

## Extraction fields per paper
For each paper in the screened corpus, extract:

```json
{
  "paper_id": "string",
  "title": "string",
  "year": "integer",
  "authors": ["string (all authors from retrieved_papers.json, in order)"],
  "doi": "string (the DOI exactly as in retrieved_papers.json; empty string if none)",
  "core_contribution": "string (1-2 sentences describing the main contribution from the abstract)",
  "method_keywords": ["string (key methods, techniques, or models mentioned)"],
  "result_summary": "string (main finding or outcome, <= 50 words)",
  "domain_tags": ["string (topic tags for grouping in Stage 4)"],
  "evidence_quality": "abstract_only"
}
```

Always set `evidence_quality` to `"abstract_only"`. This prevents downstream stages from overstating claims.

## Mandatory passthrough fields

### DOI
Copy the `doi` field verbatim from `retrieved_papers.json` into each `knowledge.json` entry.

- The `paper_id` is **not** a DOI: it replaces both `.` and `/` with `_`, a lossy transform that cannot be reversed to recover the real DOI.
- Stage 9 builds the reference list from `knowledge.json` and needs the real DOI. If it is missing, the reference entry renders an empty `DOI: ` tail.
- If `retrieved_papers.json` has no `doi` for a paper, write `"doi": ""` and continue. Never derive a fake DOI from `paper_id`.

### Authors
Copy the **full** author list from `retrieved_papers.json`, in order. Do not truncate to the first three.

- Stage 9 formats the reference list with `等` (zh) or `et al.` (en) when there are more than three authors, but it can only do that if the full list is present.
- Truncating here permanently loses the tail authors and produces incomplete reference entries.

## Extraction method
Extract the fields directly from the paper title and abstract. The LLM executes this stage directly. Do not call any deleted extraction script.

## Filtering after extraction
- Exclude papers where `core_contribution` is empty because the abstract is too short or uninformative
- Report the count in plain language, for example: `Extracted knowledge from 26 papers.`

## After extraction
- Write the results to `output/knowledge.json`
- Build a paper lookup dictionary for later stages when useful
- Pass the knowledge list to Stage 4
