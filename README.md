# nepal-import
# Nepal Import Review draft generator

# problem
Sunbridge trading(fictional) needs a proper document draft that they can share with local agents that cover the necessary information about the imports. the manufacturer sent two pdfs with inconsistent content. from those two need to generate a combined helpful reference draft that Nepal import reviews usually want. If two sources do not match then that needs to be pointed out. 

## Planned Pipeline

1. Extract text from the source PDFs.
2. Extract important facts and attach source references(use llm for messy + simple regex extraction for obvious fields).
3. Compare the facts against Nepal import review expectations.
4. Identify missing, unclear, or conflicting information.
5. Generate a final review draft in Markdown (and optionally PDF).

# how to run
## Running the full pipeline
```bash
uv run python main.py
```

This will:

1. Extract text from PDFs in `data/input/`
2. Extract evidence-backed facts
3. Generate NEPQA mapping
4. Generate conflict matrix
5. Generate Nepal import review draft

## running text extraction
``` bash
uv run python src/extract_text.py
```
## Data Models

The project uses small data models so the extracted information stays organized.

### Evidence

Shows where a fact came from.

It stores:

- PDF name
- page number
- short source note
- confidence

### Product Fact

Stores one important fact found in the PDFs.

Examples:

- model name
- manufacturer
- certificate number
- standard
- rating

### Requirement Mapping

Shows whether the available documents cover an expected review item.

Examples:

- found
- partly found
- missing
- needs confirmation

### Conflict

Stores anything that does not clearly match between documents.

Examples:

- different model names
- different company names
- missing value in one PDF

## How These Models Work in the Pipeline

PDF text → Product Facts + Evidence → Requirement Mapping → Conflicts → Final Draft


### Documenting the Extraction Issues

---

### Known Text Extraction Issues

Raw text extracted from manufacturer PDFs contains formatting bugs that distort the data:

* **Split Table Rows:** Multi-column tables often extract line-by-line incorrectly. Model prefixes get grouped together on one line, while their matching suffixes drop down to the next line:
```text
CE-1P3001G   CE-1P5001G   CE-1P6001G
-230-EU      -230-EU      -230-EU

```

* **Column Line-Breaks:** Tight column layouts break long words and model names across lines using a hyphen and a newline character (e.g., `EU-\nAM2`).
* **Merged Text Noise:** Artifacts from extraction occasionally smash distinct words and dates together into a single block of text (e.g., `GRAPHIEC      11/Oct/19`).


### Strategic Deferrals

To prioritize building the core pipeline, the following refinements are consciously deferred:

* **Standards Classification:** Every `IEC` standard is logged, including page headers. Differentiating between a primary certification standard and a referenced standard is postponed.
* **String Variation:** The current regex strictly targets pure `IEC` formats. Handling compound prefixes like `IEC/EN` or mapping them to common base standards is deferred to the normalization phase.
* **Duplicate Mentions:** Identical facts found on different pages are intentionally preserved to maintain a complete log of evidence.


### Manual Script Caveat

Use `uv run python main.py` for normal runs. It extracts facts from both source files before generating NEPQA mapping and conflict outputs.

Running `src/extract_facts.py` manually still writes only its configured single source into `outputs/extracted_facts.json`, so downstream outputs may show the other source as missing.

## Current Outputs

The pipeline generates:

- `outputs/extracted_text/` - raw text extracted from the source PDFs
- `outputs/extracted_facts.json` - structured facts with evidence references
- `outputs/nepqa_mapping.json` - machine-readable NEPQA checklist mapping
- `outputs/nepqa_mapping.md` - readable NEPQA checklist mapping
- `outputs/conflict_matrix.json` - machine-readable source conflict comparison
- `outputs/conflict_matrix.md` - readable conflict summary
- `outputs/nepal_import_review_draft.md` - final review draft for SunBridge Trading


## Current Key Finding

The two manufacturer PDFs appear to describe different inverter model families.

- `DSS_GZES230100125901_combined-1.pdf` appears to describe CHISAGE `CE-1P` single-phase inverter models.
- `188_1115.pdf` appears to describe Deye `SUN-G06P3` grid-connected inverter models.

Because of this, the exact inverter model being imported into Nepal should be confirmed before treating the generated draft as a reliable review package.


## AI / LLM Design Note

The core pipeline currently uses deterministic extraction and rule-based mapping instead of relying on an LLM.

This was intentional because the task needs evidence-backed review, not a black-box summary. Regex and labeled-field extraction are easier to test, explain, and trace back to source pages.

An LLM could be added later as a candidate extraction helper for messy fields, but any LLM output should still be checked against source evidence before being used in the final draft.


## Draft Evolution

The review draft was improved through a few versions to make it clearer and easier to review.

### v1 - Initial Draft

- Facts were listed directly from extraction.
- Model names were shown in one large combined list.
- Standards were also shown in one combined list.
- There was no key finding section.

Problem:

- The main issue, that the two PDFs may describe different inverter families, was not clear enough.

---

### v2 - More Structured Draft

- Added clearer headings.
- Added product, standards, conflict, and missing information sections.

Problem:

- The model list was still too flat.
- Source A and Source B were not separated clearly enough.

---

### v3 - Source-Aware Draft

- Separated Source A and Source B information.
- Made conflicts easier to see.
- Added better manufacturer and product summaries.

Problem:

- Some sections were still too verbose.
- Important findings needed to appear earlier.

---

### v4 - Full Model Listings

- Changed from representative model ranges to complete model lists.
- SUN models are now grouped by variant: AM2 and AM2-P1.
- CE-1P models are listed in full.
- Product summary header now shows model family instead of filename.
- Model conflicts reference the Product Summary section instead of inline ranges.

Main improvements:

- Easier to review all available models at a glance.
- SUN model variants are clearly organized.
- No ambiguity from representative ranges — all models are visible.