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
