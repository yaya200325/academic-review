# Chinese Writing Mode (zh)

## Language Register

- Use formal academic written Chinese
- Open each paragraph with a clear thesis sentence
- Avoid repetitive empty lead-ins such as "studies show" or "in summary" when they add no information
- Make transitions logical rather than decorative

## Terminology Consistency

- Give both the Chinese and English term at first mention when useful
- After that, keep a stable canonical term for each concept
- Maintain a terminology ledger if the review involves many specialized variants
- Do not rotate synonyms merely for stylistic variation

### English abbreviation discipline (mandatory)

Once an English abbreviation has been introduced, use **only the abbreviation** thereafter. The whole point of defining an abbreviation is to stop repeating the long form.

- First mention: `中文全称 (ABBR)` — for example `碳纳米管 (CNT)` or `相对湿度 (RH)`
- Every subsequent mention: `ABBR` only — `CNT`, `RH`. Do **not** revert to `碳纳米管` or `相对湿度` later in the same document.
- This applies across all sections, the abstract, tables, and figure captions. The first-mention site is the abstract if the term appears there; otherwise the body section where it first occurs.
- Record each `中文全称 -> ABBR` mapping in the terminology ledger in `review_lock.md` so later sections stay consistent.
- Exceptions (keep the long form, do not abbreviate):
  - the term appears only once in the whole document — no abbreviation needed
  - the long form is itself short and unambiguous, e.g. `LED`, `MgCl2` — introduce once, then keep as-is
  - the first mention is inside a table cell or caption that already reads densely — still define it in prose at the earliest opportunity
- Do not introduce a new abbreviation in the final sections that was never defined earlier. If a term first appears late, either define it there or use the full Chinese form throughout.

Anti-pattern to avoid: writing `碳纳米管 (CNT)` in section 2 and then `碳纳米管` again in sections 3, 4, and 5. That defeats the abbreviation and signals the terminology ledger was not used.

## Citation Format

- Use numeric GB/T-style citations
- In-text citations may appear as bracketed numeric references
- Order the reference list by first appearance in the text
- Keep author names in their original language form in the reference list

## Paragraph Structure

- Typical paragraph length is 150 to 300 Chinese characters or the locally appropriate equivalent
- Use a structure such as: thesis sentence -> development or comparison -> citation support -> transition or local conclusion
- Avoid chaining many contrast markers in the same paragraph
- Prefer horizontal comparison where possible

## Figures and Tables

- Figure captions appear below figures
- Table captions appear above tables
- In running text, refer explicitly to figures and tables in a natural way
