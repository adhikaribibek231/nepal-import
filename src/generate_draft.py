import json
import re
from pathlib import Path

from src.schemas import ConflictMatrix, ExtractedFacts, ReviewMapping


SOURCE_A = "DSS_GZES230100125901_combined-1.txt"
SOURCE_B = "188_1115.txt"

NEPQA_RELEVANT_STANDARDS = {
    "IEC 61727",
    "IEC 62116",
    "IEC 62891",
    "IEC 62109-1",
    "IEC 62109-2",
}


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


def values_for_source(
    facts: ExtractedFacts,
    source_file: str,
    field_name: str,
) -> list[str]:
    values = {
        fact.normalized_value or fact.raw_value
        for fact in facts.facts
        if fact.field_name == field_name
        and fact.evidence.source_file == source_file
    }

    return sorted(values)


def normalize_model_name(model: str) -> str:
    return model.replace(" -", "-").replace("- ", "-").strip()


def remove_partial_model_names(models: list[str]) -> list[str]:
    cleaned = []

    for model in sorted(set(models), key=len, reverse=True):
        if not any(
            existing.startswith(model) and existing != f"{model}-P1"
            for existing in cleaned
        ):
            cleaned.append(model)

    return sorted(cleaned)


def add_implied_sun_am2_models(models: list[str]) -> list[str]:
    expanded = set(models)

    for model in models:
        if model.endswith("-AM2-P1"):
            expanded.add(model.removesuffix("-P1"))

    return sorted(expanded)


def display_models_for_source(facts: ExtractedFacts, source_file: str) -> list[str]:
    models = [
        normalize_model_name(model)
        for model in values_for_source(facts, source_file, "model_name")
    ]

    if source_file == SOURCE_B:
        models = add_implied_sun_am2_models(models)

    return remove_partial_model_names(models)


def model_sort_key(model: str) -> tuple[int, int, str]:
    ce_match = re.search(r"\bCE-1P(?P<power>\d+)G", model)
    if ce_match:
        return 0, int(ce_match.group("power")), model

    sun_match = re.search(r"\bSUN-(?P<power>\d+)K", model)
    if sun_match:
        return 1, int(sun_match.group("power")), model

    return 2, 0, model


def model_family(models: list[str]) -> str:
    if any(model.startswith("CE-1P") for model in models):
        return "CE-1P series"

    if any(model.startswith("SUN-") and "G06P3" in model for model in models):
        return "SUN G06P3 series"

    return ", ".join(models) or "Not found in extracted facts."


def format_inline_values(values: list[str]) -> str:
    return ", ".join(values) or "Not found in extracted facts."


def add_model_list(lines: list[str], models: list[str]) -> None:
    if not models:
        lines.append("- Not found in extracted facts.")
        return

    for model in sorted(models, key=model_sort_key):
        lines.append(f"- {model}")


def add_sun_model_groups(lines: list[str], models: list[str]) -> None:
    am2_models = [model for model in models if model.endswith("-AM2")]
    p1_models = [model for model in models if model.endswith("-AM2-P1")]

    if am2_models:
        lines.append("  AM2 models:")
        for model in sorted(am2_models, key=model_sort_key):
            lines.append(f"  - {model}")

    if p1_models:
        lines.append("  AM2-P1 models:")
        for model in sorted(p1_models, key=model_sort_key):
            lines.append(f"  - {model}")


def add_model_list_for_source(
    lines: list[str],
    source_file: str,
    models: list[str],
) -> None:
    if not models:
        lines.append("- Models found: Not found in extracted facts.")
        return

    lines.append("- Models found:")

    if source_file == SOURCE_B:
        add_sun_model_groups(lines, models)
    else:
        for model in sorted(models, key=model_sort_key):
            lines.append(f"  - {model}")


def add_source_product_summary(
    lines: list[str],
    facts: ExtractedFacts,
    source_label: str,
    source_file: str,
) -> None:
    models = display_models_for_source(facts, source_file)

    lines.append(f"**{source_label} \u2014 {model_family(models)}**")
    product_type = format_inline_values(
        values_for_source(facts, source_file, "product_type")
    )
    ip_rating = format_inline_values(
        values_for_source(facts, source_file, "ip_rating")
    )

    lines.append(f"- Source file: {source_file}")
    lines.append(f"- Product type: {product_type}")
    lines.append(f"- IP rating: {ip_rating}")
    add_model_list_for_source(lines, source_file, models)
    lines.append("")


def split_standards(standards: list[str]) -> tuple[list[str], list[str]]:
    primary = []
    other = []

    for standard in standards:
        if any(key in standard for key in NEPQA_RELEVANT_STANDARDS):
            primary.append(standard)
        else:
            other.append(standard)

    return sorted(set(primary)), sorted(set(other))


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


def add_model_conflict_summary(lines: list[str]) -> None:
    lines.append("- Source A: CE-1P series models listed in Product Summary")
    lines.append(
        "- Source B: SUN G06P3 AM2 / AM2-P1 models listed in Product Summary"
    )


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
        "## 2. Key Review Finding",
        "The provided documents appear to cover different inverter model families. The imported model must be confirmed before this draft can be treated as a reliable import review package.",
        "",
        "## 3. Documents Reviewed",
        "",
    ]

    for document in documents_reviewed(facts):
        lines.append(f"- {document}")

    lines.extend(["", "## 4. Product Summary", ""])
    lines.append(
        "The documents appear to describe grid-connected PV inverters, but not the same model family."
    )
    lines.append("")
    add_source_product_summary(lines, facts, "Source A", SOURCE_A)
    add_source_product_summary(lines, facts, "Source B", SOURCE_B)
    lines.append(
        "**Review note:** These appear to be different inverter families. The exact model being imported should be confirmed."
    )
    lines.append("")
    lines.append(
        "Full extracted model list is available in `outputs/extracted_facts.json`."
    )
    lines.append("")

    lines.extend(["## 5. Manufacturer and Factory Information", ""])
    add_value_section(lines, "Manufacturer", values_for_field(facts, "manufacturer"))
    add_value_section(lines, "Factory", values_for_field(facts, "factory"))
    add_value_section(
        lines,
        "Certificate holder",
        values_for_field(facts, "certificate_holder"),
    )
    add_value_section(lines, "Applicant", values_for_field(facts, "applicant"))

    lines.extend(["## 6. Standards and Test Evidence", ""])
    nepqa_standards, other_standards = split_standards(
        values_for_field(facts, "standard")
    )
    add_value_section(lines, "NEPQA-relevant standards found", nepqa_standards)
    add_value_section(lines, "Other referenced standards found", other_standards)
    add_value_section(
        lines,
        "Certificate numbers",
        values_for_field(facts, "certificate_number"),
    )
    add_value_section(lines, "Report numbers", values_for_field(facts, "report_number"))

    lines.extend(["## 7. NEPQA Mapping Summary", ""])
    for status, count in sorted(counts.items()):
        lines.append(f"- `{status}`: {count}")

    lines.extend(["", "**Evidence found:**"])
    add_mapping_list(lines, mapping, "evidence_found")

    lines.extend(["## 8. Conflict Summary", ""])
    if not conflict_matrix.conflicts:
        lines.append("- No conflicts generated.")
        lines.append("")
    else:
        for conflict in conflict_matrix.conflicts:
            lines.append(f"### {conflict.field_name}")
            lines.append("")
            lines.append(f"- Status: `{conflict.status}`")
            if conflict.field_name == "model_name":
                add_model_conflict_summary(lines)
            else:
                lines.append(f"- Source A: {conflict.source_a}")
                lines.append(f"- Source B: {conflict.source_b}")
            lines.append(f"- Issue: {conflict.issue}")
            if conflict.decision:
                lines.append(f"- Decision: {conflict.decision}")
            lines.append("")

    lines.extend(["## 9. Missing Information", ""])
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

    lines.extend(["## 10. Items Needing Confirmation", ""])
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
            "## 11. Limitations",
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
        output_path="outputs/review_drafts/nepal_import_review_draft.md",
    )
