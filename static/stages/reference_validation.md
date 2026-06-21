# Stage 8.5 - Reference Validation

## Overview

Verify that all papers in `knowledge.json` are real and that their metadata is accurate enough for final export. Also check citation-format consistency before exporting to docx.

**This is a quality gate**: critical issues such as fabricated papers or major metadata errors block Stage 9 and require user confirmation.

---

## Goal

1. **Metadata authenticity** - verify that DOI or arXiv identifiers resolve to the correct paper
2. **Citation-format consistency** - verify that the final reference list follows the target standard

---

## Process

### Step 1: Load Data

1. Read `output/knowledge.json`
2. Read `output/polished.md`
3. Read `output/review_lock.md`

### Step 2: Verify Metadata Authenticity

For each paper in `knowledge.json`:

#### A. Papers with DOI

Call the Crossref API:

```bash
curl "https://api.crossref.org/works/{doi}"
```

Check:
- DOI resolves
- title matches strongly enough
- year matches within tolerance
- at least one expected author appears in the returned metadata

**Critical issues**:
- DOI returns 404
- year mismatch greater than 2 years
- title clearly refers to a different paper

**Warnings**:
- year mismatch within 1 year
- title partially different
- incomplete author mismatch

#### B. Papers with arXiv ID but No DOI

Call the arXiv API:

```bash
curl "http://export.arxiv.org/api/query?id_list={arxiv_id}"
```

Check title and year.

#### C. Papers with Neither DOI nor arXiv ID

Mark them as **cannot verify**. This is a limitation, not automatically an error.

### Step 3: Check Citation Format Consistency

Build the reference list from `knowledge.json` and check the target format.

#### For `language: zh`

Expected simplified numeric GB/T-style pattern:

```text
[n] Author. Title[J]. Year. DOI: xxx
```

Check:
- consistent author separation
- consistent punctuation
- valid 4-digit year
- consistent DOI formatting

#### For `language: en`

Expected IEEE-style pattern:

```text
[n] Author1, Author2, and Author3, "Title," Year. DOI: xxx
```

Check:
- title in quotes
- consistent author joining
- year placed before DOI
- DOI formatting consistent

---

## Output: `output/reference_validation.md`

Generate a structured report containing:

- summary counts
- valid papers
- warnings
- critical issues
- cannot-verify items
- citation-format findings
- export recommendation

Suggested summary fields:
- total papers in `knowledge.json`
- papers actually cited
- verified via DOI
- verified via arXiv
- cannot verify
- critical issue count
- warning count

---

## Decision Logic

### Block Export

Block export if any critical issue exists:
- DOI does not resolve
- year mismatch > 2 years
- title is clearly for another paper

Action:
- output the report
- display the critical issues
- ask the user whether to proceed anyway

### Allow Export with Warnings

If only warnings exist:
- output the report
- proceed automatically to Stage 9
- recommend a final metadata review before submission

---

## Implementation Notes

### API Limits

- Crossref: generous public limit, but still avoid wasteful repeated calls
- arXiv: use respectfully and avoid unnecessary bursts

### Error Handling

- network error -> mark as cannot verify (API error)
- API timeout -> mark as cannot verify
- invalid DOI format -> report warning and try a cleaned DOI if possible

### Optional Caching

If the same review is validated repeatedly, caching responses is acceptable.

---

## Skip Check

If `output/reference_validation.md` exists:
- skip if it is newer than `output/polished.md`
- rerun if `output/polished.md` was updated after validation

---

## Output Files

- `output/reference_validation.md` - human-readable report
- optional machine-readable status file for pipeline control

---

## Summary

Stage 8.5 is the final quality gate before export:
1. verify papers are real
2. verify metadata is credible
3. verify citation formatting is consistent
4. block export on critical issues
5. allow export on warnings only
