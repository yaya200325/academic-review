# Stage 7: Figure/Table Generation Guide

## Goal
Analyze the completed text draft (`output/draft_text.md`) and insert figures/tables only where they improve comprehension. Visuals must support the argument, not decorate the page.

---

## ⚠️ Critical Path Convention

**full_document.md location**: `output/full_document.md`  
**Image paths in Markdown**: MUST use relative path `figures/fig_X.png`  
**DO NOT use**: `output/figures/fig_X.png` (absolute from skill root)

This is a hard constraint enforced by the docx exporter.

---

## ⚠️ Capability Detection Protocol

### Core Principle: Active Testing, Not Passive Assumption

Image generation capability MUST be detected by **actual generation attempt**, not by checking tool names or making assumptions.

### Detection Workflow

**Step 1: Analyze triggers first**
- Check content triggers (process/architecture/timeline)
- Check explicit requests (`VISUAL_PLACEHOLDER`, `如图X所示`)
- Check structural indicators (comparison tables)

**Step 2: If NO triggers match**
- Skip capability detection
- Proceed to table-only generation if needed
- Document in audit log: `No figure triggers detected`

**Step 3: If triggers match**
- Evaluate whether the planned figure would genuinely improve comprehension
- If NOT valuable -> document false positive, no capability test needed
- If valuable -> proceed to Step 4

**Step 4: Test capability (first figure only in this Stage 7 run)**
- Generate a minimal test image:
  - Prompt: `A simple horizontal flowchart with 3 boxes labeled 'Input', 'Process', 'Output', connected by arrows. White background, black text, minimal styling.`
  - Save to: `output/figures/_capability_test.png`
- Record result:
  - **Success** -> Set `CAN_GENERATE_IMAGES = AVAILABLE`, cache for this run, proceed with real figures
  - **Failure** -> Record failure type (see below), set `CAN_GENERATE_IMAGES = NOT_AVAILABLE`

**Step 5: For subsequent figures in the same run**
- Reuse cached `CAN_GENERATE_IMAGES` value
- Do NOT re-test capability

### Failure Type Classification

If capability test fails, record the specific failure type in audit log:

| Failure Type | Description | Audit Log Entry |
|--------------|-------------|-----------------|
| `tool_unavailable` | No image generation tool found in environment | `Image generation capability: NOT_AVAILABLE (tool_unavailable)` |
| `permission_failure` | Tool exists but execution blocked by permissions/hooks | `Image generation capability: NOT_AVAILABLE (permission_failure: [error message])` |
| `generation_failure` | Tool executed but returned error | `Image generation capability: NOT_AVAILABLE (generation_failure: [error message])` |
| `file_not_created` | Tool reported success but no PNG file created | `Image generation capability: NOT_AVAILABLE (file_not_created)` |
| `file_write_failed` | PNG created but cannot write to `output/figures/` | `Image generation capability: NOT_AVAILABLE (file_write_failed: [error])` |

### Test File Handling

- Test image path: `output/figures/_capability_test.png`
- Prefix `_` indicates temporary file
- MUST NOT be referenced in `draft_full.md` or `full_document.md`
- Can be deleted after test or kept for debugging (Stage 9 export ignores files with `_` prefix)

### Anti-Patterns to Avoid

- ❌ **DO NOT**: Check capability before analyzing triggers
- ❌ **DO NOT**: Assume "tool not obvious" means "capability unavailable"
- ❌ **DO NOT**: Test capability for every single figure candidate
- ❌ **DO NOT**: Write test images to formal figure paths and then delete them
- ❌ **DO NOT**: Cache capability result across different Stage 7 runs

- ✅ **DO**: Trigger -> Value judgment -> Test once -> Cache -> Use for all figures this run
- ✅ **DO**: Record specific failure types for diagnostics
- ✅ **DO**: Use isolated test file path (`_capability_test.png`)

---

## Stage 7 Audit Log (Mandatory)

Before finalizing `output/draft_full.md`, write the audit log as the first line:

- **Image generation capability**: Result of capability detection (`AVAILABLE` / `NOT_AVAILABLE`)
- **Planned figures**: Count of figure candidates identified during analysis
- **Generated figures**: Count of figures actually inserted with `![...](...)`
- **Omitted figures**: Count and reasons for each omission

If omitted figures > 0, list each with:
- Description of what the figure would show
- Specific reason for omission (essential vs non-essential, generation failure, etc.)

This log makes Stage 7 decisions auditable and prevents "silent figure deletion".

## Mandatory Figure Planning Triggers

Stage 7 MUST attempt to plan at least one figure when ANY of these conditions are met:

1. **Content triggers**:
   - Text describes a process with 4+ steps
   - Text describes architecture / module relationships
   - Text describes method evolution timeline
   - Text describes mechanism chains or feedback loops

2. **Explicit requests**:
   - `<!-- VISUAL_PLACEHOLDER: ... -->` comment exists in `draft_text.md`
   - Text contains forward reference like `如图X所示` or `见图X`

3. **Structural indicators**:
   - Section contains comparison of 3+ methods with 3+ dimensions (table OR figure)

**If triggers are met but no figure is added**: Document in audit log why planning did not result in generation.

**"Must attempt"** execution sequence:

1. **Evaluate figure value**: Would this figure genuinely improve comprehension?
   - If NO -> document as false positive, skip to next trigger
   - If YES -> proceed to step 2

2. **Test capability** (only if not tested yet in this run):
   - Generate test image to `output/figures/_capability_test.png`
   - Record result and cache for this run
   - If test succeeds -> set `CAN_GENERATE_IMAGES = AVAILABLE`
   - If test fails -> set `CAN_GENERATE_IMAGES = NOT_AVAILABLE` + record failure type

3. **Decision branch**:
   - **If AVAILABLE**: Generate the planned figure to `output/figures/fig_X.png`
   - **If NOT_AVAILABLE**:
     - Judge if figure is essential (see definitions in "Image Generation Guidance" section)
     - Essential -> Report blocker to user with specific figure description
     - Non-essential -> Document omission in audit log with failure type

4. **For subsequent figures in this run**:
   - Reuse cached capability result
   - Skip step 2 (no re-testing)

⚠️ **Critical ordering**:
- Trigger analysis -> Value judgment -> Capability test -> Generate/Omit
- NOT: Capability test -> Trigger analysis (wrong)
- NOT: Test every figure separately (wasteful)

This prevents Stage 7 from silently skipping figure consideration.

---

## When to Add Visuals

### Add a figure when

- A process or workflow has 4 or more steps and is spread across multiple paragraphs
- A structure or architecture is abstract and difficult to understand from text alone
- A method evolution spans multiple years or phases
- A taxonomy or hierarchy has 3 or more levels
- Relationships between concepts form a nontrivial network

### Add a table when

- Comparing 3 or more methods across 3 or more dimensions
- The text lists multiple items with parallel attributes
- A dense comparison would be slower to read in prose than in rows and columns

### Do not add visuals when

- The text is already clear and concise
- Only 2 items are being compared
- The visual would repeat what a single sentence already states
- The visual is being added only to increase apparent richness or page count

---

## Quantity Constraint

Density guideline: 1 to 3 visuals per 2000 words

- 3000-word review: usually 2 to 4 visuals
- 5000-word review: usually 3 to 6 visuals
- 7000-word review: usually 4 to 7 visuals

Over-illustration weakens academic prose. Use only visuals that improve understanding.

⚠️ **If actual count is significantly below guideline** (e.g., 5000-word review with 0 visuals):
- Re-check mandatory triggers (process/architecture/placeholders)
- If no triggers match, document in audit log: `Low visual density is appropriate for this content type`
- If triggers match but figures omitted, ensure omission reasons are documented

This is a guideline, not a hard requirement. The audit log makes exceptions transparent.

---

## Figure Type Selection

Use the following decision tree, not free intuition.

### Step 1: Identify the paragraph content type from textual cues

| Cue in the paragraph | Figure type | Typical trigger |
|---|---|---|
| Year sequence such as `2016`, `2017`, `2018` and an evolution narrative | `timeline figure` | "A was proposed in 2016, then B improved it in 2017" |
| Phrases like `分为…类` / `包括…种` / `可划分为…` | `taxonomy figure` | Taxonomy or hierarchy |
| Phrases like `基于X发展出Y` / `A改进为B` / `由X扩展到Y` | `relationship figure` | Method relationship or improvement path |
| State changes such as `初始化→前向传播→反向传播→更新` | `process figure` | State transition or workflow |
| Sequential phrases such as `首先` / `然后` / `最后` / `依次` | `process figure` | Process or workflow |

### Step 2: Default behavior

- If one cue pattern clearly matches, use the corresponding type
- If multiple patterns match, choose the type that preserves the main argumentative structure
- If none matches clearly, default to `conceptual process figure`

### Step 3: Build the image-generation prompt

Build the prompt from fixed components, not free-form intuition.

Include all of the following:

**A. Purpose and context**
- State what paragraph or section the figure supports
- State what confusion or density in the text this figure resolves
- State the single key takeaway the reader should get from the image

**B. Figure type**
- Choose one primary type: process / timeline / taxonomy / relationship / architecture / conceptual illustration
- If the figure mixes types, name the dominant one and keep the layout simple

**C. Required elements**
- List the components, stages, concepts, or categories that must appear
- Keep only elements that are explicitly supported by `draft_text.md` or `knowledge.json`

**D. Required relationships**
- Specify arrows, grouping, hierarchy, sequence, comparison, before-after, or feedback loop
- State directionality clearly when order matters

**E. Language and labeling**
- Chinese labels only
- Short labels preferred
- No full English paper titles in the image

**F. Visual style**

### F.0 Design principles

**Academic journal illustration standards** - not presentation slides.

Core principles:
- **Information-first**: Every visual element carries meaning, no decoration
- **Minimalist restraint**: Simple shapes, restrained colors, generous whitespace
- **Professional precision**: Grid-aligned, consistent hierarchy, sharp rendering
- **Publication-ready**: Could appear in Nature, Science, IEEE journals without visual editing

Visual discipline:
- White or very light background (`#FFFFFF` or `#F8F8F8` maximum)
- Restrained color palette: deep blues/grays, avoid bright/saturated colors
- Clear visual hierarchy through size, weight, and spacing (not through decoration)
- Simple geometric shapes with minimal corner radius (`2-3px` maximum)
- No shadows, gradients, textures, 3D effects, glossy surfaces
- No icon library clipart, emoji-style graphics, or decorative embellishments

**Anti-pattern (PPT style to avoid)**:
- Bright accent colors (yellow, bright green, hot pink)
- Large corner radius (>3px makes shapes look cartoonish)
- Drop shadows and 3D effects
- Decorative icons from clipart libraries
- Gradient fills and glossy buttons
- Cluttered layouts with <20% whitespace

### F.1 Color scheme

Choose one restrained scheme for the entire figure.

- **Scheme A (Nature/Science style - 推荐用于流程图、关系图)**
  - Primary: `#1F4E79` (深海蓝)
  - Secondary: `#5B9BD5` (标准蓝)
  - Accent: `#C55A11` (深橙，仅用于关键对比)
  - Neutral: `#7F7F7F` (灰色，用于次要元素)
  - Background: `#FFFFFF`

- **Scheme B (IEEE/Elsevier style - 推荐用于技术架构图)**
  - Primary: `#2C3E50` (深蓝灰)
  - Secondary: `#3498DB` (湖蓝)
  - Accent: `#E74C3C` (深红，仅用于警示/对比)
  - Neutral: `#95A5A6` (冷灰)
  - Background: `#FFFFFF`

- **Scheme C (单色学术 - 推荐用于机制示意图)**
  - Primary: `#2C3E50` (深灰蓝)
  - Secondary: `#7F8C8D` (中灰)
  - Accent: `#34495E` (深灰，用于强调)
  - Neutral: `#BDC3C7` (浅灰，用于辅助线)
  - Background: `#FFFFFF`

Color usage rules:
- Use primary for main modules, core paths, and key labels
- Use secondary for supporting modules and secondary structure
- Use accent **sparingly** - only for critical emphasis or key contrast points (max 5% of visual elements)
- Use neutral for grouping boundaries, secondary annotations, background elements
- Prefer flat fills with no gradients; use solid colors or very light tints (opacity ≤ 0.1)
- Avoid bright saturated colors (HSB saturation < 60%)
- Do not rely on red/green contrast alone to encode meaning

### F.2 Typography hierarchy

- Module labels (primary): `11pt` medium sans-serif
- Relationship labels / annotations: `9pt` regular sans-serif
- Minimum font size: `8pt` (不低于此值以保证可读性)

Typography rules:
- Academic figures do not need in-figure titles (标题在caption中，图内无需16pt大标题)
- Keep one sans-serif family per figure (推荐 Arial 或 Helvetica)
- Text-background contrast ratio ≥ `4.5:1` (WCAG AA标准)
- Prefer short labels (≤ 8 Chinese characters or ≤ 12 English words)
- If a label is long, wrap to two lines instead of shrinking below `8pt`
- Avoid all-caps text unless for standard acronyms

### F.3 Shape language

- **Primary modules/components**: rounded rectangles, corner radius `2-3px` (不超过3px以避免卡通化)
- **Secondary containers**: sharp rectangles (0px radius) or minimal `1px` radius
- **Emphasis nodes**: use `1.5px` stroke instead of heavy fills
- **Arrow specifications**:
  - Primary flow arrows: `1.5px` line width, simple triangular head (6-8px edge length)
  - Secondary/feedback arrows: `1px` line width, smaller head (5px edge length)
  - Dashed feedback loops: `1px` dashed line, dash pattern `[4, 3]`
  - Arrow heads must precisely connect to shape boundaries
- **Grouping boundaries**: `0.5px` stroke, neutral color, dashed pattern `[2, 2]`
- **Avoid**: thick arrows (>2px), 3D arrows, gradient arrows, decorative arrow styles, bubble shapes, star shapes

### F.4 Layout and spacing

- Canvas margin: at least `10%` on all sides (上下左右留白充足)
- Inter-element gap: at least `20%` relative to module width (元素间距不拥挤)
- Grid alignment: all elements snap to invisible `8px` grid (精确对齐)
- Whitespace discipline: content occupies max `70%` of canvas area (留白占比至少30%)
- Flow direction: 
  - Process flows: left-to-right (L→R)
  - Hierarchies: top-to-bottom (T→B)
  - Only deviate when content strongly suggests otherwise
- Avoid: freestyle scattered placement, cluttered layouts, edge-to-edge content

### F.5 Generation parameters

When using image generation, specify:
- **Background**: Pure white `#FFFFFF`, no texture or patterns
- **Design style**: Flat design, minimalist academic illustration
- **Color palette**: Explicitly specify hex codes from chosen scheme, avoid bright/saturated colors
- **Typography**: Sans-serif labels (Arial or Helvetica), 3-level hierarchy (11pt/9pt/8pt), no in-figure title
- **Layout**: Clean spacing, grid-aligned, uncluttered, 30% minimum whitespace
- **Line quality**: Sharp, anti-aliased, consistent width hierarchy
- **Output format**: SVG preferred (vector, scalable); PNG fallback at minimum `1200x800px` resolution
- **Rendering quality**: High-quality anti-aliasing, crisp text rendering

**Critical exclusions** (explicitly state in every prompt):
- No shadows, drop shadows, or inner shadows
- No gradients (linear or radial) on fills or strokes
- No textures, patterns, or decorative backgrounds
- No 3D effects, perspective, or depth simulation
- No glossy/shiny surfaces or reflection effects
- No icon library elements, clipart, or emoji-style graphics
- No decorative embellishments that don't carry information

### F.6 Mechanism schematic rules

When `figure type` is `mechanism schematic` (mechanism diagram, principle diagram, conceptual model), apply these additional content constraints.

### Core principle: evidence-grounded visualization

Only show content explicitly supported by `draft_text.md` or `knowledge.json`. If evidence is insufficient, use black-box representation instead of inventing internal steps.

### Four content constraints

1. **Object constraint**
   - Only include entities explicitly mentioned in the draft text.
   - Allowed entity types: input/output, module/component, state/representation, feedback/regulation.
   - Forbidden:
     - Inventing intermediate layers for symmetry
     - Expanding one module into sub-components without text evidence
     - Adding "typical" mechanisms based on domain knowledge but not stated in the text

2. **Relationship constraint**
   - Use at most 2 relationship semantics per figure.
   - All arrows use the same visual style: solid line, simple triangle head.
   - Distinguish semantics by text labels, not by extra arrow styles.
   - Prefer labels such as `影响`, `产生`, `增强`, `抑制`, `反馈`, `调节`.

3. **Abstraction level constraint**
   - One figure, one abstraction level.
   - Allowed levels:
     - `conceptual`: high-level causal links
     - `modular`: components and their connections
   - `implementation` level is not allowed in `academic-review` because evidence quality is abstract-only.

4. **Evidence boundary constraint**
   - If mechanism details are unclear from the text, use black-box representation.
   - Black-box module:
     - Single rounded rectangle
     - Module name only, optionally with `(机制)` or `(过程)`
     - No internal sub-divisions or implied sub-steps

### Four canonical templates

Choose exactly one template for each mechanism figure:

1. **Layered mechanism**
   - Use when: clear input -> mechanism -> output stages
   - Structure: `[Input] -> [Mechanism] -> [Output]`

2. **Causal chain**
   - Use when: linear cause-effect sequence
   - Structure: `[Factor A] -> [Mechanism B] -> [Result C]`

3. **Module interaction**
   - Use when: multiple components interact
   - Structure: 3-5 modules with minimal cross-connections

4. **Side-by-side comparison**
   - Use when: comparing traditional vs improved mechanism
   - Structure: aligned parallel paths with one key difference highlighted

### Three hard rules

Before finalizing any mechanism figure, verify:

1. **Text grounding**
   - Every module and relationship appears explicitly in `draft_text.md`
   - If not, remove it or convert it to a black-box

2. **Black-box discipline**
   - If internal mechanism is unclear, keep it as a black-box
   - Do not invent sub-steps to complete the story

3. **Simplicity limits**
   - Maximum 5 major modules
   - Maximum 2 relationship semantics
   - One figure, one core mechanism storyline

**Label length guidance**
- Prefer labels within 8 Chinese characters
- If longer, wrap to two lines instead of shrinking the font too far
- Do not sacrifice terminology accuracy for brevity

Mechanism figures must also satisfy Section F (appearance). Section F controls how the figure looks; Section F.6 controls what it is allowed to contain.

**G. Exclusions**
- No fabricated metrics
- No unsupported mechanisms
- No extra modules or experimental details not in source text
- No English paper titles
- No decorative filler that does not strengthen the argument

**H. Prompt assembly template**

```text
For general figures (process flowcharts, timelines, taxonomies, relationships):

Create an academic figure for a Chinese literature review in the style of Nature/Science journals.

**Purpose**: [what confusion or density this figure resolves]
**Figure type**: [process flowchart | timeline | taxonomy | comparison matrix | relationship diagram]
**Context**: [brief section summary or paragraph topic]

**Required elements**: 
- [element 1]
- [element 2]
- [element 3]
[list only elements explicitly supported by draft text]

**Required relationships**: 
- [describe arrows, grouping, hierarchy, or sequence]
- [specify directionality when order matters]

**Visual specifications**:
- Color scheme: Nature/Science style
  - Primary `#1F4E79`, Secondary `#5B9BD5`, Accent `#C55A11` (use sparingly), Neutral `#7F7F7F`
- Background: Pure white `#FFFFFF`, no texture
- Typography: Arial, module labels `11pt`, annotations `9pt`, no in-figure title
- Shapes: rounded rectangles `2-3px` radius, simple arrows `1.5px` primary / `1px` secondary
- Layout: grid-aligned on `8px` grid, `20%` inter-element spacing, `10%` canvas margin, max `70%` content density
- Line quality: sharp anti-aliased vectors, consistent width hierarchy

**Language**: Chinese labels only, short and precise (≤8 characters preferred)

**Strict exclusions**:
- No shadows, gradients, textures, 3D effects, glossy surfaces
- No icon library clipart, emoji-style graphics, decorative elements
- No fabricated metrics, unsupported mechanisms, English paper titles
- No bright saturated colors (keep HSB saturation <60%)
- No decorative filler that doesn't strengthen the argument

**Output**: SVG vector format preferred, or PNG at minimum `1200x800px` with high-quality anti-aliasing

---

For mechanism schematics (principle diagrams, conceptual models):

Create an academic mechanism schematic for a Chinese literature review in engineering journal style.

**Purpose**: [what mechanism or principle this figure clarifies]
**Figure type**: mechanism schematic

**Mechanism structure**:
- Abstraction level: [conceptual | modular]
- Template: [layered (Input→Mechanism→Output) | causal-chain | module-interaction | side-by-side-comparison]
- Major modules (3-5 max):
  - [Module 1: brief description, grounded in draft text]
  - [Module 2: ...]
  - [Module 3: ...]
- Relationships (max 2 types):
  - Type 1: [e.g., "影响" / "产生"] - represented by solid arrows
  - Type 2: [e.g., "反馈" / "调节"] - represented by dashed arrows

**Evidence grounding**:
- Black-box modules: [list modules whose internals are unclear from text]
- Excluded details: [list omitted sub-steps not evidenced in abstracts]

**Content verification checklist**:
- [ ] Every module traces to draft text
- [ ] Every relationship is explicitly stated in text
- [ ] No invented sub-mechanisms or intermediate steps
- [ ] Black-box discipline applied where evidence is thin

**Visual specifications**:
- Color scheme: Single-color academic style
  - Primary `#2C3E50`, Secondary `#7F8C8D`, Neutral `#BDC3C7`
- Background: Pure white `#FFFFFF`
- Typography: Arial, module labels `11pt`, relationship labels `9pt`
- Shapes: rounded rectangles `2-3px` radius, all arrows use same visual style (solid `1.5px` or dashed `1px [4,3]`)
- Arrow semantics: distinguish by text labels only, not by arrow style variations
- Layout: follow chosen template structure, `20%` spacing, `10%` margin, visible whitespace
- Black-box representation: single rectangle with module name + "(机制)" or "(过程)", no internal subdivisions

**Language**: Chinese labels, terminology consistent with review text

**Strict exclusions**:
- No invented mechanisms, unsupported formulas, fabricated sub-steps
- No shadows, gradients, 3D effects, decorative depth cues
- No icon library elements, clipart representations
- No multiple arrow styles (one solid, one dashed maximum)
- No decorative color coding beyond the 3-color palette

**Output**: SVG vector format preferred, or PNG at minimum `1200x800px`
```

---

## Image Generation Guidance

Use image generation for all figures in this stage.

**Core principle**: Academic journal quality, not presentation slides.

### Prompt requirements

**Content**:
- Explicit element list (only what's supported by draft text or knowledge.json)
- Clear relationship specification (arrows, grouping, hierarchy)
- Chinese labels only, short and precise
- No fabricated metrics, unsupported mechanisms, or decorative elements

**Visual style** (must include in every prompt):
- **Reference style**: "Nature/Science journal figure style" or "IEEE engineering diagram style"
- Clean academic illustration, minimalist flat design
- White background, no texture or patterns
- Restrained color palette with explicit hex codes
- Sans-serif typography (Arial/Helvetica), clear hierarchy
- Sharp vector lines, grid-aligned elements
- Generous whitespace (30% minimum)

**Explicit exclusions** (critical - state in every prompt):
- No shadows, gradients, textures, 3D effects
- No glossy/shiny surfaces, reflections, lighting effects
- No icon library clipart, emoji-style graphics, cartoon elements
- No decorative embellishments, ornamental borders, background patterns
- No bright saturated colors (HSB saturation must be <60%)

### Quality targets

- **Legibility**: Readable at normal document size, no overlapping text
- **Clarity**: Obvious reading order, clear hierarchy
- **Professionalism**: Could appear in Nature, Science, IEEE journals without visual editing

### Output format

- **Preferred**: SVG (vector, scalable, editable)
- **Fallback**: PNG at minimum `1200x800px` with high-quality anti-aliasing

Save outputs to `output/figures/fig_X.png` or `output/figures/fig_X.svg`.

Insert as standard Markdown images:

```markdown
![图X 标题文字](figures/fig_X.png)
```

Use the alt text as the full caption. Keep captions concise and specific.

### Content Boundaries (Red Lines)

Images MUST ONLY visualize:
- Relationships explicitly stated in the draft text
- Concepts defined in `knowledge.json` abstracts
- Comparisons directly supported by cited papers

Images MUST NOT include:
- Experimental results not in `knowledge.json` (e.g., `accuracy: 95.3%`)
- Mechanism details not mentioned in abstracts (e.g., `layer normalization + dropout`)
- Invented evaluation metrics or benchmarks
- English paper titles from references

**Verification rule**: Every element in the image should trace back to a sentence in `draft_text.md` or a field in `knowledge.json`.

## Figure Quality Verification

Run a lightweight manual quality check after each generated figure.

Check four dimensions:

**1. Legibility**
- Labels are readable at normal document size
- Text is not overlapping, cropped, or too dense
- Arrows and connectors are visually distinguishable

**2. Layout clarity**
- Main reading order is obvious
- Grouping and hierarchy are easy to understand
- The image does not feel cluttered or visually noisy

**3. Language compliance**
- Chinese labels only
- No full English paper titles
- No awkward mixed-language labels unless the technical term must stay in English

**4. Content fidelity**
- Elements match the text and `knowledge.json`
- No invented mechanisms, metrics, benchmarks, or extra claims
- The figure supports the paragraph's actual argument

Quality result must be classified as one of:
- `PASS`: keep the figure
- `MINOR_ISSUES`: keep the figure if the problem does not mislead the reader
- `MAJOR_ISSUES`: regenerate or remove the figure

## Regeneration Protocol

Only regenerate for `MAJOR_ISSUES`.

Rules:
- Maximum 2 regeneration attempts per figure
- Each retry should add only 1 to 2 critical corrections to the prompt
- Do not rewrite the whole prompt unless the first prompt was structurally wrong

Examples of `MAJOR_ISSUES`:
- Labels are unreadable
- Layout is confusing enough to harm comprehension
- English paper titles appear in the figure
- Unsupported content was invented

If a figure still fails after 2 regeneration attempts:
- Essential figure -> report blocker to user with the specific quality failure
- Non-essential figure -> omit the figure and record in audit log: `Figure omitted after failed quality verification`

If zero figures were added, `draft_full.md` MUST contain explanation in audit log.
Valid reasons:
- `Content is comparison-heavy, tables sufficient`
- `No process/architecture/relationship suitable for visualization`
- `Image generation unavailable, all candidates were non-essential`
- `Figure omitted after failed quality verification`
- Invalid: no reason given (execution failure)

If image generation is unavailable:
- **Non-essential figure** (text is clear without it): Delete the placeholder and continue
- **Essential figure** (text is incomplete without it): Report blocker with specific figure description

**"Essential" definition**:
- The text says `如图X所示` but doesn't explain what the figure shows
- The figure is the ONLY way to understand a complex architecture/workflow described
- Removing it would leave a logical gap in the argument

**"Non-essential" definition**:
- The figure illustrates something already clear from text
- The figure is supplementary or decorative
- The text can stand alone without it

Do not keep an `IMAGE_GENERATION_PROMPT` comment in the final markdown.

---

## Table Guidance

Use Markdown tables.

Recommended columns:
- Method
- Year
- Core technique
- Key advantage
- Limitation
- Typical application

Avoid:
- Author names
- Journal names
- Too many performance columns

Prefer 5 to 10 rows. Use representative methods, not every paper.

---

## Integration with Text

Every visual must have three parts:

1. Setup sentence before the visual
2. The visual itself
3. Interpretation sentence after the visual

Checklist for every visual:
- The previous sentence explains why the visual is needed
- The caption is specific
- The following sentence extracts the key insight
- Removing the visual would weaken the paragraph's support

Do not write only `如图X所示` or `如表X所示` without explanation.

---

## Placeholder Handling

If Stage 6 left placeholders such as:

```markdown
<!-- VISUAL_PLACEHOLDER: flowchart showing message passing -->
```

Process every placeholder with this mandatory rule:

1. Read the placeholder description
2. Choose exactly one action:
   - Option A: generate a visual and replace the placeholder
   - Option B: delete the placeholder comment
3. Never leave the placeholder comment in the output

Hard rule:
- `<!-- VISUAL_PLACEHOLDER: ... -->` and `<!-- IMAGE_GENERATION_PROMPT: ... -->` in `output/draft_full.md` are execution failures

Required self-check before finalizing `output/draft_full.md`:
- Search the file for `<!-- VISUAL_PLACEHOLDER`
- Search the file for `<!-- IMAGE_GENERATION_PROMPT`
- If any match remains, fail Stage 7 and remove all remaining placeholders before proceeding

---

## Quality Checklist

Before finalizing Stage 7, verify:

- Total visuals stay within the density guideline
- Every visual has a caption
- Every visual has both setup and interpretation
- Text references visuals naturally
- No placeholder comments remain in `output/draft_full.md`
- A final grep/search check confirms no placeholder comments remain
- Every referenced figure file exists
- Every image path resolves from `output/draft_full.md`
- Image paths are relative (no `output/` prefix)
- Every generated figure passed lightweight quality verification or has a documented omission reason
- Any regenerated figure stayed within the 2-attempt limit
- Table columns are aligned and readable
- Figure and table numbering is sequential

---

## Common Mistakes to Avoid

- Leaving placeholder comments in the final draft
- Leaving an image-generation prompt in the final draft
- Adding a visual without rewriting surrounding text
- Generating a decorative image that does not sharpen the argument
- Putting unsupported mechanisms or metrics into the figure

---

## Summary

Stage 7 is a decision-and-integration stage:

1. Decide whether a visual is genuinely needed
2. Detect whether image generation is available
3. Choose the figure type from textual cues
4. Generate the visual with image generation or table as appropriate
5. Remove all placeholders
6. Run a final grep/search check before writing `output/draft_full.md`
