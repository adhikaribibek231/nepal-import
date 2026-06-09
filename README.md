# Nepal Import Review Draft Generator

## Problem

SunBridge Trading, a fictional importer, needs a clear document draft that they can share with a Nepal import agent for review. The manufacturer sent two PDFs, but the content is not fully consistent. The goal of this project is to read those documents, extract useful information, compare it with common Nepal import review expectations, and generate a careful draft that points out what is found, what is missing, and what does not match.

This project does not certify compliance. It only prepares a review draft from the available documents.

---

## What This Project Does

The project takes two manufacturer PDF documents and creates a review package for Nepal import discussion.

It focuses on:

* product and model information
* manufacturer, applicant, factory, and certificate holder information
* test reports and certificate evidence
* NEPQA-style review items for grid-connected PV inverters
* mismatches between the two source documents
* missing information that should be confirmed before import review

The final output is a Markdown draft that SunBridge Trading could share with a local agent for an initial review.

---

## Main Finding

The two manufacturer PDFs appear to describe different inverter model families.

* `DSS_GZES230100125901_combined-1.pdf` appears to describe CHISAGE `CE-1P` single-phase inverter models.
* `188_1115.pdf` appears to describe Deye `SUN-G06P3` grid-connected inverter models.

Because of this, the exact inverter model being imported into Nepal needs to be confirmed before relying on the review draft.

---

## Inputs

Source PDFs are stored in:

```text
data/input/
```

Input files:

```text
188_1115.pdf
DSS_GZES230100125901_combined-1.pdf
```

Supporting notes are stored in:

```text
notes/
```

Important notes:

```text
notes/review_notes.md
notes/source_observations.md
approach_note.md
```

`review_notes.md` contains the initial understanding of the task and NEPQA relevance.

`source_observations.md` contains manual observations from the two manufacturer PDFs before and during coding.

`approach_note.md` briefly explains the working approach in simple non-technical words.

---

## Pipeline in Simple Words

The pipeline works like this:

```text
PDF documents
↓
Text extraction
↓
Fact extraction
↓
NEPQA-style checklist mapping
↓
Conflict detection
↓
Review draft generation
```

In simple terms:

1. The PDFs are converted into page-level text.
2. Important facts are extracted from the text.
3. Each fact keeps a source reference.
4. The facts are compared with Nepal import review expectations.
5. The two source documents are compared against each other.
6. A review draft is generated from the structured results.
7. The client-facing final draft is exported as PDF.

The goal is to avoid loose summaries and keep the draft tied to evidence from the source documents.

---

## Current Pipeline

The current full pipeline does the following:

1. Extracts text from the source PDFs.
2. Extracts evidence-backed facts using regex and labeled-field extraction.
3. Maps extracted facts against NEPQA-style inverter review items.
4. Detects missing, unclear, or conflicting information.
5. Generates a mechanical review draft.
6. Generates a cleaner client-facing final draft.
7. Exports the client-facing final draft as PDF.

---

## How to Run

Run the full pipeline:

```bash
uv run python main.py
```

This will generate all main outputs.

You can also run text extraction separately:

```bash
uv run python src/extract_text.py
```

For normal use, run:

```bash
uv run python main.py
```

because it processes both source documents together.

---

## Outputs

Generated files are stored in:

```text
outputs/
```

Main outputs:

```text
outputs/extracted_text/
outputs/extracted_facts.json
outputs/nepqa_mapping.json
outputs/nepqa_mapping.md
outputs/conflict_matrix.json
outputs/conflict_matrix.md
outputs/review_drafts/nepal_import_review_draft.md
outputs/review_drafts/nepal_import_review_final_draft.md
outputs/review_drafts/nepal_import_review_final_draft.pdf
```

What they mean:

* `outputs/extracted_text/` contains text extracted from each PDF.
* `outputs/extracted_facts.json` contains structured facts with evidence references.
* `outputs/nepqa_mapping.md` shows which NEPQA-style review items have evidence, are missing, or need manual review.
* `outputs/conflict_matrix.md` shows mismatches between the two source documents.
* `outputs/review_drafts/nepal_import_review_draft.md` is the mechanical draft generated from the structured outputs.
* `outputs/review_drafts/nepal_import_review_final_draft.md` is the cleaner draft intended for SunBridge Trading.
* `outputs/review_drafts/nepal_import_review_final_draft.pdf` is the PDF version of the client-facing final draft.

---

## Repository Structure

```text
nepal-import/
├── data/
│   └── input/
│       ├── 188_1115.pdf
│       └── DSS_GZES230100125901_combined-1.pdf
├── notes/
│   ├── review_notes.md
│   └── source_observations.md
├── outputs/
│   ├── extracted_text/
│   ├── extracted_facts.json
│   ├── nepqa_mapping.json
│   ├── nepqa_mapping.md
│   ├── conflict_matrix.json
│   ├── conflict_matrix.md
│   └── review_drafts/
│       ├── nepal_import_review_draft.md
│       ├── nepal_import_review_final_draft.md
│       ├── nepal_import_review_final_draft.pdf
│       └── past_drafts
│           ├── nepal_import_review_draft_v1.md
│           ├── nepal_import_review_draft_v2.md
│           ├── nepal_import_review_draft_v3.md
│           └── nepal_import_review_draft_v4.md
├── src/
│   ├── extract_text.py
│   ├── extract_facts.py
│   ├── nepqa_checklist.py
│   ├── reconcile.py
│   ├── generate_draft.py
│   ├── generate_final_draft.py
│   ├── export_final_pdf.py
│   └── schemas.py
├── main.py
├── approach_note.md
├── README.md
└── pyproject.toml
```

---

## Important Files

### `src/extract_text.py`

Extracts page-level text from the source PDFs.

The output keeps page markers like:

```text
--- PAGE 1 ---
```

This helps later when facts need source references.

---

### `src/extract_facts.py`

Extracts important facts from the extracted text.

Examples:

* certificate number
* report number
* issue date
* expiry date
* certificate holder
* applicant
* manufacturer
* factory
* product type
* model names
* standards
* IP rating
* protective class
* cooling method

---

### `src/schemas.py`

Defines the small data models used in the project.

The main models are:

* `Evidence`
* `ProductFact`
* `RequirementMapping`
* `Conflict`
* `ExtractedFacts`
* `ReviewMapping`
* `ConflictMatrix`

These models help keep the project structured and traceable.

---

### `src/nepqa_checklist.py`

Maps extracted facts against NEPQA-style review items for PV inverters.

It uses statuses such as:

* `evidence_found`
* `partial`
* `missing`
* `needs_confirmation`
* `not_assessed`

This does not decide compliance. It only shows what the provided documents appear to support.

---

### `src/reconcile.py`

Compares facts across the two source documents.

It checks fields such as:

* manufacturer
* product type
* standards
* model names
* IP rating

The goal is to show what matches, what differs, and what needs confirmation.

---

### `src/generate_draft.py`

Generates a mechanical review draft from the structured outputs.

This draft is useful for checking the pipeline result.

---

### `src/generate_final_draft.py`

Generates a cleaner client-facing draft for SunBridge Trading.

This draft avoids raw filenames where possible and uses clearer document names such as:

* SGS IEC/EN 62109-1 Test Report
* SGS Certificate of Conformity

---

### `src/export_final_pdf.py`

Converts the already-clean client-facing Markdown draft into a PDF.

It reads:

```text
outputs/review_drafts/nepal_import_review_final_draft.md
```

and writes:

```text
outputs/review_drafts/nepal_import_review_final_draft.pdf
```

---

## Data Models

The project uses small data models so the extracted information stays organized.

### Evidence

Shows where a fact came from.

It stores:

* source document
* page number
* short source note
* confidence

### Product Fact

Stores one important fact found in the documents.

Examples:

* model name
* manufacturer
* certificate number
* standard
* IP rating

### Requirement Mapping

Shows whether a Nepal import review item is covered by the available evidence.

Examples:

* evidence found
* missing
* needs confirmation
* not assessed

### Conflict

Stores information that does not clearly match between the two documents.

Examples:

* different model families
* different manufacturer or certificate holder information
* different IP ratings
* missing value in one document

---

## Working Process

I started with manual review before writing the full pipeline.

The rough process was:

1. Read the assessment brief.
2. Skim NEPQA 2025 and focus on the PV inverter / grid-connected inverter section.
3. Manually review the two manufacturer PDFs.
4. Write notes about product details, manufacturer information, test evidence, labeling, and differences.
5. Build text extraction.
6. Build structured fact extraction.
7. Create the NEPQA-style checklist mapping.
8. Build source reconciliation and conflict detection.
9. Generate a review draft.
10. Improve the draft into a cleaner client-facing version.

The plan changed slightly while building. Some cleanup was better handled during draft generation instead of during raw extraction. For example, full model lists were kept as evidence, but the final draft groups them by document and model family to make the output easier to read.

---

## Manual Review Notes

Before relying on the generated outputs, I manually reviewed the main documents and wrote notes.

`notes/review_notes.md` explains the task understanding:

* this is a draft for review
* NEPQA is used as a rough import-side reference
* Section 1.4 is the relevant section for grid-tied inverters
* the work does not need to be a final legal filing

`notes/source_observations.md` records source-level findings:

* Source A appears to be an SGS safety test report.
* Source B appears to be an SGS Certificate of Conformity.
* The two sources appear to describe different inverter families.
* Several items need confirmation, including exact imported model, warranty, data logger, efficiency, MPPT efficiency, and THD information.

---

## Known Text Extraction Issues

Raw text extracted from manufacturer PDFs can contain formatting problems.

Examples:

* multi-column tables may extract in the wrong reading order
* model names may be split across lines
* model suffixes may appear separately from model prefixes
* some words and dates may be merged together

Example:

```text
CE-1P3001G   CE-1P5001G   CE-1P6001G
-230-EU      -230-EU      -230-EU
```

Because of this, the project keeps raw extracted text as evidence but handles some cleanup later when generating the draft.

---

## Challenges and Improvements

Several practical issues came up while turning the two manufacturer PDFs into reviewable outputs.

### Page References

Early extraction treated each document too much like one block of text, which made source references less useful. The text extractor now writes page markers, and fact extraction reads those markers so extracted facts can keep page numbers.

Remaining limitation:

* Page references still depend on the quality of the PDF text extraction.

### Single-File Testing

Early testing was done one document at a time, which could replace a combined `outputs/extracted_facts.json` with facts from only one source. The normal `main.py` pipeline now processes both source documents together before building the NEPQA mapping, conflict matrix, and drafts.

Remaining limitation:

* Running `src/extract_facts.py` directly is still a manual testing path and can overwrite the combined facts output.

### PDF Layout Noise

The PDFs contain table layouts, split rows, broken model suffixes, and other extraction artifacts. The current extraction handles the common structured fields and preserves raw evidence, while draft generation performs some display cleanup.

Remaining limitation:

* Layout noise is not fully removed from raw extracted text or every intermediate output.

### Model Names

Model extraction can still capture partial names alongside more complete names. The review drafts reduce this by showing cleaner, source-separated model lists.

Remaining limitation:

* `outputs/extracted_facts.json` intentionally keeps partial model matches when they were found in the source text.

### IP Ratings

The observed IP ratings appear in formats such as `IP65`, `IP67`, and `IP 67`. Extraction normalizes the observed spacing differences so these can be compared in later steps.

Remaining limitation:

* Additional IP formats should be tested before treating the extractor as fully general.

### Standards

The final drafts separate NEPQA-relevant standards from other standards referenced in the documents. This keeps the Nepal import review items easier to scan.

Remaining limitation:

* The separation uses a predefined standards list, not a full certificate-scope analysis.

### Conflicts

The conflict matrix compares fields that matter for review, including product description, model names, standards, manufacturer information, and IP rating. This helps show that the two PDFs should not be treated as one confirmed product package.

Remaining limitation:

* Some conflict entries still need manual interpretation because they reflect raw extraction behavior as well as real document differences.

---

## Draft Evolution

The review draft was improved through a few versions to make it clearer and easier to review.

### v1 - Initial Draft

* Facts were listed directly from extraction.
* Model names were shown in one large combined list.
* Standards were also shown in one combined list.
* There was no key finding section.

Problem:

* The main issue, that the two PDFs may describe different inverter families, was not clear enough.

---

### v2 - More Structured Draft

* Added clearer headings.
* Added product, standards, conflict, and missing information sections.

Problem:

* The model list was still too flat.
* The two source documents were not separated clearly enough.

---

### v3 - Source-Aware Draft

* Separated the two source documents.
* Made conflicts easier to see.
* Added better manufacturer and product summaries.

Problem:

* Some sections were still too verbose.
* Important findings needed to appear earlier.

---

### v4 - Full Model Listings

* Changed from representative model ranges to complete model lists.
* Grouped SUN models into AM2 and AM2-P1 variants.
* Listed CE-1P models in full.

Main improvement:

* All available models are visible without hiding the document mismatch.

---

### Current Final Draft

The current final draft is:

```text
outputs/review_drafts/nepal_import_review_final_draft.md
```

It is cleaner than the mechanical draft and is intended to be easier for SunBridge Trading or a local Nepal import agent to read.

---

## Extraction Approach

When I started the project, I expected to use an LLM to help extract information from the manufacturer documents.

After reviewing the PDFs, I decided to first try a deterministic approach using regex patterns and labeled-field extraction.

The main reason was that many important fields already appeared in predictable formats, such as:

- certificate numbers
- report numbers
- manufacturer names
- certificate holder names
- standards
- model names
- IP ratings

For these fields, deterministic extraction was simpler, easier to verify, and easier to trace back to the original document pages.

As the project evolved, the extraction pipeline remained rule-based because it was able to recover most of the information needed for the review draft.

### Where an LLM Could Help

There are still some areas where an LLM could be useful in a future version.

Examples include:

- understanding long technical descriptions
- extracting information from inconsistent table layouts
- identifying manufacturer, applicant, and factory information when labels are written differently
- grouping related information spread across multiple pages
- distinguishing between primary certification standards and standards that are only referenced
- generating cleaner summaries from large amounts of extracted evidence

For this assessment, I chose to keep the core pipeline deterministic and evidence-based because the source documents were structured enough to support that approach.

---

## Current Limitations

This project is still a review aid, not a final compliance package.

Known limitations:

* The exact imported inverter model still needs confirmation.
* The two source documents may not belong to the same shipment.
* Warranty information was not found in the provided PDFs.
* Data logger and external monitoring information was not clearly found.
* Efficiency, MPPT efficiency, Euro efficiency, THD, and no-load loss evidence was not clearly found.
* IECEE / IECRE listing and certification body scope were not independently verified.
* The final draft should still be reviewed by the importer, manufacturer, or Nepal import agent.

---

## Future Improvements

Possible improvements:

* Add more normalization for IEC and IEC/EN standard names.
* Add automated tests for extraction and draft generation.
* Add better model-name cleanup for complex PDF table layouts.
* Add certificate body verification workflow.
* Add extraction from technical datasheets if more documents are provided.
* Make source document names configurable instead of hard-coded.
