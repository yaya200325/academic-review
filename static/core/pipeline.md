# Pipeline Overview

This skill runs a linear nine-stage pipeline with an additional Stage 8.5 quality gate. Load the corresponding stage fragment before beginning each stage.

## Stage 1 - Search
Retrieve papers from Semantic Scholar or equivalent sources. Target retrieval is about 1.5 times the user's requested reference count.  
Load `static/stages/search.md`.

## Stage 2 - Screen
Score each paper for relevance on a 0 to 1 scale. Keep papers with score >= 0.6. If the kept set is below target, run one more search and merge.  
Load `static/stages/screening.md`.

## Stage 3 - Extract
Extract structured knowledge from abstracts only. This is sufficient for undergraduate-level synthesis unless the workflow explicitly collects stronger evidence.  
Load `static/stages/extraction.md`.

## Stage 4 - Outline [USER CHECKPOINT]
Plan the review structure from thematic clusters and wait for explicit user confirmation before Stage 5.  
Load `static/stages/outline.md`.

## Stage 5 - Synthesize
Generate structured notes for each confirmed section: claims, method groups, consensus, controversy, gaps, and representative references.  
Load `static/stages/synthesis.md`.

## Stage 6 - Draft
Write the review section by section from the synthesis notes. Text only. Figures and tables are deferred.  
Load `static/stages/drafting.md`.

## Stage 7 - Diagram/Table
Analyze the complete draft globally and insert figures or tables where they improve comprehension.  
Load `static/stages/diagram_table.md`.

## Stage 8 - Polish
Polish the complete draft for terminology, clarity, and structural fit. Maximum 2 iterations with sentence-level fixes only.  
Load `static/stages/polishing.md`.

## Stage 8.5 - Reference Validation
Verify reference authenticity and citation-format consistency before export. Critical issues block Stage 9 until resolved or explicitly waived.  
Load `static/stages/reference_validation.md`.

## Stage 9 - Export
Compile the final review into a Word document with embedded figures, tables, and a numbered reference list.  
Load `static/stages/export.md`.

## Interaction Checkpoints

- Before Stage 1: confirm topic, reference count, word count, language, and paper type
- After Stage 4: confirm the outline before writing begins
- After Stage 8.5 if critical issues exist: show the validation report and wait for confirmation before export
