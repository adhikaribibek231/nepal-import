import json
from pathlib import Path

from src.schemas import Conflict, ConflictMatrix, ExtractedFacts


SOURCE_A = "DSS_GZES230100125901_combined-1.txt"
SOURCE_B = "188_1115.txt"

FIELDS_TO_COMPARE = [
    "manufacturer",
    "product_type",
    "standard",
    "model_name",
    "ip_rating",
]


def load_extracted_facts(path: str) -> ExtractedFacts:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return ExtractedFacts(**data)


def values_for_source(
    facts: ExtractedFacts,
    source_file: str,
    field_name: str,
) -> set[str]:
    values = set()

    for fact in facts.facts:
        if fact.field_name != field_name:
            continue

        if fact.evidence.source_file != source_file:
            continue

        value = fact.normalized_value or fact.raw_value
        values.add(value)

    return values


def compare_values(
    field_name: str,
    source_a_values: set[str],
    source_b_values: set[str],
) -> Conflict:
    source_a_text = ", ".join(sorted(source_a_values)) or "Not found"
    source_b_text = ", ".join(sorted(source_b_values)) or "Not found"

    if not source_a_values and not source_b_values:
        status = "needs_confirmation"
        issue = f"No extracted values found for {field_name} in either source."

    elif source_a_values and not source_b_values:
        status = "missing_in_one_source"
        issue = f"{field_name} was found in Source A but not in Source B."

    elif source_b_values and not source_a_values:
        status = "missing_in_one_source"
        issue = f"{field_name} was found in Source B but not in Source A."

    elif source_a_values == source_b_values:
        status = "consistent"
        issue = f"{field_name} appears consistent across both sources."

    else:
        status = "conflict"
        issue = f"{field_name} differs between Source A and Source B."

    return Conflict(
        field_name=field_name,
        source_a=source_a_text,
        source_b=source_b_text,
        status=status,
        issue=issue,
        decision="Needs confirmation if this affects the imported product identity.",
    )


def build_conflict_matrix(facts: ExtractedFacts) -> ConflictMatrix:
    conflicts = []

    for field_name in FIELDS_TO_COMPARE:
        source_a_values = values_for_source(facts, SOURCE_A, field_name)
        source_b_values = values_for_source(facts, SOURCE_B, field_name)

        conflict = compare_values(field_name, source_a_values, source_b_values)
        conflicts.append(conflict)

    return ConflictMatrix(conflicts=conflicts)


def save_json(matrix: ConflictMatrix, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(matrix.model_dump(), file, indent=2, ensure_ascii=False)


def save_markdown(matrix: ConflictMatrix, output_path: str) -> None:
    lines = ["# Conflict Matrix", ""]

    for conflict in matrix.conflicts:
        lines.append(f"## {conflict.field_name}")
        lines.append("")
        lines.append(f"Status: `{conflict.status}`")
        lines.append("")
        lines.append(f"Source A: {conflict.source_a}")
        lines.append("")
        lines.append(f"Source B: {conflict.source_b}")
        lines.append("")
        lines.append(f"Issue: {conflict.issue}")
        lines.append("")

        if conflict.decision:
            lines.append(f"Decision: {conflict.decision}")
            lines.append("")

        lines.append("---")
        lines.append("")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    facts = load_extracted_facts("outputs/extracted_facts.json")
    matrix = build_conflict_matrix(facts)

    save_json(matrix, "outputs/conflict_matrix.json")
    save_markdown(matrix, "outputs/conflict_matrix.md")
