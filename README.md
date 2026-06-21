# academic-review

[简体中文](README.zh-CN.md)

**academic-review** is a Codex skill for end-to-end literature review writing. It helps an AI coding agent search papers, screen relevance, extract abstract-level knowledge, plan an outline, draft a review, add figures and tables, polish the prose, validate references, and export a formatted Word document.

## What It Does

- Runs a 9-stage literature review workflow from topic to `.docx`
- Supports Chinese and English review writing
- Targets undergraduate thesis reviews and course-paper literature reviews
- Uses checkpoint files so long writing tasks can be resumed
- Keeps claims grounded in collected paper metadata and abstracts
- Separates drafting from figure/table placement for better structure
- Exports academic Word documents through `scripts/docx_export.py`

## Workflow

```text
Stage 1   Search                -> output/retrieved_papers.json
Stage 2   Screen                -> output/screened_papers.json
Stage 3   Extract               -> output/knowledge.json
Stage 4   Outline               -> output/outline.json + output/review_lock.md
Stage 5   Synthesize            -> output/synthesis_notes.json
Stage 6   Draft                 -> output/draft_text.md
Stage 7   Diagram/Table         -> output/draft_full.md
Stage 8   Polish                -> output/polished.md + output/polish_audit.md
Stage 8.5 Reference Validation  -> output/reference_validation.md
Stage 9   Export                -> output/full_document.md + output/review.docx
```

Stage 4 is intentionally blocking: the agent should present the outline and wait for user confirmation before drafting.

## Typical Prompt

```text
Use academic-review to write a Chinese literature review on "Graph Neural Networks in Recommender Systems".
Target: 30 references, 7000 Chinese characters, undergraduate thesis review.
```

## Required Inputs

| Parameter | Description | Example |
| --- | --- | --- |
| `topic` | Review topic | `Graph neural networks in recommender systems` |
| `ref_count` | Target number of references | `30` |
| `word_count` | Target length | `7000` |
| `language` | Output language | `zh` / `en` |
| `paper_type` | Paper scenario | `course_paper` / `undergraduate_thesis` |

If some fields are missing, the skill instructs the agent to ask only for the necessary missing information.

## Output

The final deliverable is:

```text
output/review.docx
```

The generated Word document includes:

- title, abstract, and keywords
- structured body sections
- renumbered in-text citations
- comparison tables when useful
- embedded local figures when image generation is available
- numbered references with DOI information when available
- academic formatting handled by the exporter

## Installation

Clone or copy this folder into your Codex skills directory:

```text
~/.codex/skills/academic-review
```

Install Python dependencies for the export script:

```bash
pip install -r requirements.txt
```

Then invoke it naturally in Codex with a literature-review writing request.

## Dependencies

The skill itself is instruction-driven. The only production script is the Word exporter:

| Script | Purpose |
| --- | --- |
| `scripts/docx_export.py` | Convert the final Markdown document into a formatted Word document |

Python dependencies are listed in `requirements.txt`:

- `httpx`
- `python-docx`
- `pillow`
- `requests`

## Repository Structure

```text
academic-review/
├── SKILL.md
├── manifest.yaml
├── README.md
├── README.zh-CN.md
├── CHANGELOG.md
├── LICENSE
├── requirements.txt
├── schemas/
├── scripts/
│   ├── docx_export.py
│   ├── fix_encoding.py
│   └── utils.py
├── static/
│   ├── core/
│   ├── fragments/
│   └── stages/
└── workflows/
    └── resume-review.md
```

## Design Principles

- **Agent-orchestrated, not script-orchestrated**: Codex executes the writing workflow stage by stage.
- **Evidence bounded**: claims should be grounded in retrieved paper metadata and abstracts.
- **Checkpointed**: each major stage writes output files before the next stage begins.
- **Outline-locked**: drafting should follow the confirmed outline and `review_lock.md`.
- **Export-focused**: Markdown is the intermediate format; `.docx` is the final user-facing artifact.

## Limitations

- The workflow is designed for abstract-level literature review writing unless the agent explicitly retrieves and reads full papers.
- Reference validation depends on available DOI, arXiv, or metadata records.
- Figure generation depends on the image-generation capability available to the running agent.
- The generated review still requires human academic judgment before formal submission.

## Before Publishing to GitHub

Recommended additions:

- `examples/`: add a sample prompt, representative checkpoint outputs, and final document screenshots.
- `agents/openai.yaml`: add Codex UI metadata such as display name, short description, and default prompt.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
