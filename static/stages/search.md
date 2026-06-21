# Stage 1 - Literature Search

## Overview
Retrieve papers from Semantic Scholar using the available web/search capabilities. The LLM executes this stage directly. Do not rely on any deleted local search script.

## Target retrieval count
```text
search_count = ceil(user_requested_refs * 1.5)
```

Example: if the user wants 25 references, search for about 38 papers.

## Retrieval method
- Use the user's topic keywords directly as the main query
- For `zh` mode, try both Chinese and English keyword variants, then merge and deduplicate
- For technical topics, add precise domain terms when needed to improve recall
- Prefer specific topic phrases over broad generic queries

## Required fields
For each paper, collect when available:
- `paper_id` or equivalent stable identifier
- `title`
- `abstract`
- `year`
- `authors`
- `doi`
- `url`

Abstracts only. Do not attempt to retrieve or infer full text in this stage.

## Handling missing abstracts
- If `abstract` is missing or empty, keep the record only if the metadata still looks relevant
- Expect Stage 2 to score such papers very low or filter them out
- Do not fabricate abstract content

## After retrieval
- Write the results to `output/retrieved_papers.json`
- Pass the full retrieved list to Stage 2
- Log the count in plain language, for example: `Retrieved 38 papers from Semantic Scholar.`
