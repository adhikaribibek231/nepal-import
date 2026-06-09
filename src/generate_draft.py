import json
from pathlib import Path

from src.schemas import ConflictMatrix, ExtractedFacts, ReviewMapping


def load_extracted_facts(path: str) -> ExtractedFacts:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return ExtractedFacts(**data)


def load_review_mapping(path: str) -> ReviewMapping:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return ReviewMapping(**data)


def load_conflict_matrix(path: str) -> ConflictMatrix:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return ConflictMatrix(**data)


def values_for_field(facts: ExtractedFacts, field_name: str) -> list[str]:
    values = {
        fact.normalized_value or fact.raw_value
        for fact in facts.facts
        if fact.field_name == field_name
    }

    return sorted(values)


def documents_reviewed(facts: ExtractedFacts) -> list[str]:
    documents = {fact.evidence.source_file for fact in facts.facts}
    return sorted(documents)


def status_counts(mapping: ReviewMapping) -> dict[str, int]:
    counts: dict[str, int] = {}

    for item in mapping.mappings:
        counts[item.status] = counts.get(item.status, 0) + 1

    return counts


def add_value_section(lines: list[str], label: str, values: list[str]) -> None:
    lines.append(f"**{label}:**")

    if not values:
        lines.append("- Not found in extracted facts.")
    else:
        for value in values:
            lines.append(f"- {value}")

    lines.append("")


def add_mapping_list(lines: list[str], mapping: ReviewMapping, status: str) -> None:
    items = [item for item in mapping.mappings if item.status == status]

    if not items:
        lines.append("- None.")
        lines.append("")
        return

    for item in items:
        lines.append(f"- {item.requirement}")
        if item.notes:
            lines.append(f"  Notes: {item.notes}")

    lines.append("")


def generate_review_draft(
    facts_path: str,
    mapping_path: str,
    conflict_path: str,
    output_path: str,
) -> None:
    facts = load_extracted_facts(facts_path)
    mapping = load_review_mapping(mapping_path)
    conflict_matrix = load_conflict_matrix(conflict_path)

    counts = status_counts(mapping)

    lines = [
        "# Nepal Import Review Draft",
        "",
        "## 1. Cover Note",
        "",
        "This draft summarizes the extracted PDF text, extracted facts, NEPQA mapping, and detected source conflicts. It is not a final approval decision.",
        "",
        "## 2. Documents Reviewed",
        "",
    ]

    for document in documents_reviewed(facts):
        lines.append(f"- {document}")

    lines.extend(["", "## 3. Product Summary", ""])
    add_value_section(lines, "Product type", values_for_field(facts, "product_type"))
    add_value_section(lines, "Model names", values_for_field(facts, "model_name"))
    add_value_section(lines, "IP ratings", values_for_field(facts, "ip_rating"))

    lines.extend(["## 4. Manufacturer and Factory Information", ""])
    add_value_section(lines, "Manufacturer", values_for_field(facts, "manufacturer"))
    add_value_section(lines, "Factory", values_for_field(facts, "factory"))
    add_value_section(
        lines,
        "Certificate holder",
        values_for_field(facts, "certificate_holder"),
    )
    add_value_section(lines, "Applicant", values_for_field(facts, "applicant"))

    lines.extend(["## 5. Standards and Test Evidence", ""])
    add_value_section(lines, "Standards found", values_for_field(facts, "standard"))
    add_value_section(
        lines,
        "Certificate numbers",
        values_for_field(facts, "certificate_number"),
    )
    add_value_section(lines, "Report numbers", values_for_field(facts, "report_number"))

    lines.extend(["## 6. NEPQA Mapping Summary", ""])
    for status, count in sorted(counts.items()):
        lines.append(f"- `{status}`: {count}")

    lines.extend(["", "**Evidence found:**"])
    add_mapping_list(lines, mapping, "evidence_found")

    lines.extend(["## 7. Conflict Summary", ""])
    if not conflict_matrix.conflicts:
        lines.append("- No conflicts generated.")
        lines.append("")
    else:
        for conflict in conflict_matrix.conflicts:
            lines.append(f"### {conflict.field_name}")
            lines.append("")
            lines.append(f"- Status: `{conflict.status}`")
            lines.append(f"- Source A: {conflict.source_a}")
            lines.append(f"- Source B: {conflict.source_b}")
            lines.append(f"- Issue: {conflict.issue}")
            if conflict.decision:
                lines.append(f"- Decision: {conflict.decision}")
            lines.append("")

    lines.extend(["## 8. Missing Information", ""])
    add_mapping_list(lines, mapping, "missing")

    missing_conflicts = [
        conflict
        for conflict in conflict_matrix.conflicts
        if conflict.status == "missing_in_one_source"
    ]

    if missing_conflicts:
        lines.append("**Missing in one source:**")
        for conflict in missing_conflicts:
            lines.append(f"- {conflict.field_name}: {conflict.issue}")
        lines.append("")

    lines.extend(["## 9. Items Needing Confirmation", ""])
    add_mapping_list(lines, mapping, "not_assessed")

    confirmation_conflicts = [
        conflict
        for conflict in conflict_matrix.conflicts
        if conflict.status in {"conflict", "partial_match", "needs_confirmation"}
    ]

    if confirmation_conflicts:
        lines.append("**Source conflicts needing confirmation:**")
        for conflict in confirmation_conflicts:
            lines.append(f"- {conflict.field_name}: {conflict.issue}")
        lines.append("")

    lines.extend(
        [
            "## 10. Limitations",
            "",
            "- This draft only summarizes existing extracted facts, NEPQA mappings, and conflict results.",
            "- It does not verify certification body listing or scope on IECEE/IECRE websites.",
            "- It does not decide whether the product is approved for import.",
            "- Missing values may mean the information is absent, not extracted yet, or present in a format not currently handled.",
            "- Conflicts should be confirmed with the importer, manufacturer, or original document issuer.",
            "",
        ]
    )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    generate_review_draft(
        facts_path="outputs/extracted_facts.json",
        mapping_path="outputs/nepqa_mapping.json",
        conflict_path="outputs/conflict_matrix.json",
        output_path="outputs/nepal_import_review_draft.md",
    )
