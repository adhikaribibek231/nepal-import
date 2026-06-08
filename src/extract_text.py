from pathlib import Path
from typing import Any, Iterable, cast

import fitz


def extract_text_from_pdf(pdf_path: str | Path) -> Path:
    input_path = Path(pdf_path).resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"PDF not found: {input_path}")

    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "outputs" / "extracted_text"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{input_path.stem}.txt"

    try:
        with (
            fitz.open(input_path) as doc,
            open(output_path, "w", encoding="utf-8") as file,
        ):
            iterable_doc = cast(Iterable[Any], doc)  # just to silence typechecker
            for page_number, page in enumerate(iterable_doc, start=1):
                text = page.get_text("text", sort=True).strip()

                file.write(f"--- PAGE {page_number} ---\n")
                file.write(text or "[Empty Page]")
                file.write("\n\n")

        return output_path

    except Exception as error:
        if output_path.exists():
            output_path.unlink()

        raise RuntimeError(
            f"Failed to extract text from {input_path.name}: {error}"
        ) from error


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    test_pdf = project_root / "data" / "input" / "DSS_GZES230100125901_combined-1.pdf"
    # test_pdf = project_root / "data" / "input" / "188_1115.pdf"

    try:
        saved_path = extract_text_from_pdf(test_pdf)
        print(f"Text saved to: {saved_path}")
    except Exception as error:
        print(f"Extraction failed: {error}")
