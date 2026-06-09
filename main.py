from pathlib import Path

from src.extract_facts import process_files
from src.extract_text import extract_text_from_pdf
from src.export_final_pdf import export_final_draft_pdf
from src.generate_draft import generate_review_draft
from src.generate_final_draft import generate_final_review_draft
from src.nepqa_checklist import (
    build_review_mapping,
    load_extracted_facts,
    save_json as save_nepqa_json,
    save_markdown as save_nepqa_markdown,
)
from src.reconcile import (
    build_conflict_matrix,
    save_json as save_conflict_json,
    save_markdown as save_conflict_markdown,
)


def main() -> None:
    project_root = Path(__file__).resolve().parent
    output_dir = project_root / "outputs"
    review_drafts_dir = output_dir / "review_drafts"
    output_dir.mkdir(parents=True, exist_ok=True)

    input_pdfs = [
        project_root / "data" / "input" / "188_1115.pdf",
        project_root / "data" / "input" / "DSS_GZES230100125901_combined-1.pdf",
    ]

    extracted_text_paths = []

    print("1. Extracting text from PDFs...")
    for pdf_path in input_pdfs:
        text_path = extract_text_from_pdf(pdf_path)
        extracted_text_paths.append(text_path)

    extracted_facts_path = output_dir / "extracted_facts.json"

    print("2. Extracting facts...")
    process_files(
        input_paths=extracted_text_paths,
        output_json_path=extracted_facts_path,
    )

    print("3. Building NEPQA mapping...")
    facts = load_extracted_facts(str(extracted_facts_path))
    nepqa_mapping = build_review_mapping(facts)

    save_nepqa_json(
        nepqa_mapping,
        str(output_dir / "nepqa_mapping.json"),
    )
    save_nepqa_markdown(
        nepqa_mapping,
        str(output_dir / "nepqa_mapping.md"),
    )

    print("4. Building conflict matrix...")
    conflict_matrix = build_conflict_matrix(facts)

    save_conflict_json(
        conflict_matrix,
        str(output_dir / "conflict_matrix.json"),
    )
    save_conflict_markdown(
        conflict_matrix,
        str(output_dir / "conflict_matrix.md"),
    )

    print("5. Generating review draft...")
    generate_review_draft(
        facts_path=str(output_dir / "extracted_facts.json"),
        mapping_path=str(output_dir / "nepqa_mapping.json"),
        conflict_path=str(output_dir / "conflict_matrix.json"),
        output_path=str(review_drafts_dir / "nepal_import_review_draft.md"),
    )

    print("6. Generating client-facing final draft...")
    generate_final_review_draft(
        facts_path=str(output_dir / "extracted_facts.json"),
        mapping_path=str(output_dir / "nepqa_mapping.json"),
        conflict_path=str(output_dir / "conflict_matrix.json"),
        output_path=str(review_drafts_dir / "nepal_import_review_final_draft.md"),
    )

    print("7. Exporting client-facing final draft as PDF...")
    export_final_draft_pdf()

    print("Pipeline complete.")


if __name__ == "__main__":
    main()
