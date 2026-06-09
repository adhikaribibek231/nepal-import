from pathlib import Path

from src.generate_draft import (
    SOURCE_A,
    SOURCE_B,
    display_models_for_source,
    format_inline_values,
    load_conflict_matrix,
    load_extracted_facts,
    load_review_mapping,
    model_family,
    model_sort_key,
    split_standards,
    values_for_field,
    values_for_source,
)


TEST_REPORT = SOURCE_A
CERTIFICATE = SOURCE_B

DOCUMENT_LABELS = {
    TEST_REPORT: "SGS IEC/EN 62109-1 Test Report",
    CERTIFICATE: "SGS Certificate of Conformity",
}


def add_bullets(lines: list[str], values: list[str]) -> None:
    if not values:
        lines.append("- Not identified in the supplied documents.")
        return

    for value in values:
        lines.append(f"- {value}")


def add_model_list(lines: list[str], models: list[str]) -> None:
    if not models:
        lines.append("- Not identified in the supplied documents.")
        return

    lines.append("Models listed:")
    for model in sorted(models, key=model_sort_key):
        lines.append(f"- {model}")


def add_sun_model_groups(lines: list[str], models: list[str]) -> None:
    am2_models = [model for model in models if model.endswith("-AM2")]
    p1_models = [model for model in models if model.endswith("-AM2-P1")]

    if am2_models:
        lines.append("AM2 models:")
        for model in sorted(am2_models, key=model_sort_key):
            lines.append(f"- {model}")
        lines.append("")

    if p1_models:
        lines.append("AM2-P1 models:")
        for model in sorted(p1_models, key=model_sort_key):
            lines.append(f"- {model}")


def add_document_model_review(
    lines: list[str],
    facts,
    source_file: str,
    family_description: str,
) -> None:
    models = display_models_for_source(facts, source_file)

    lines.append(f"**{DOCUMENT_LABELS[source_file]} - {family_description}**")
    lines.append(
        f"- Product type: {format_inline_values(values_for_source(facts, source_file, 'product_type'))}"
    )
    lines.append(
        f"- IP rating: {format_inline_values(values_for_source(facts, source_file, 'ip_rating'))}"
    )
    lines.append("")

    if source_file == CERTIFICATE:
        add_sun_model_groups(lines, models)
    else:
        add_model_list(lines, models)

    lines.append("")


def document_values_line(facts, source_file: str, field_name: str) -> str:
    return format_inline_values(values_for_source(facts, source_file, field_name))


def sentence_value(value: str) -> str:
    return value.rstrip(".")


def found_requirements(mapping) -> list[str]:
    return [
        item.requirement
        for item in mapping.mappings
        if item.status == "evidence_found"
    ]


def add_nepal_reference_items(lines: list[str], mapping) -> None:
    evidence_items = found_requirements(mapping)

    lines.append("The following review reference items had evidence in the supplied documents:")
    lines.append("")
    add_bullets(lines, evidence_items)
    lines.append("")


def add_consistent_information(lines: list[str]) -> None:
    lines.extend(
        [
            "The following information appears broadly consistent:",
            "",
            "- Both documents relate to grid-connected photovoltaic inverters.",
            "- Both documents originate from SGS certification or testing processes.",
            "- Both documents reference IEC-based standards.",
            "- Both documents relate to products associated with NingBo Deye Inverter Technology Co., Ltd.",
            "",
        ]
    )


def add_mismatch_summary(lines: list[str], facts) -> None:
    test_family = model_family(display_models_for_source(facts, TEST_REPORT))
    certificate_family = model_family(display_models_for_source(facts, CERTIFICATE))

    lines.extend(
        [
            "- Model family mismatch: the test report appears to cover "
            f"{test_family}, while the certificate appears to cover {certificate_family}.",
            "- Product type mismatch: the test report identifies "
            f"{document_values_line(facts, TEST_REPORT, 'product_type')}, while the certificate identifies "
            f"{document_values_line(facts, CERTIFICATE, 'product_type')}.",
            "- IP rating mismatch: the test report identifies "
            f"{document_values_line(facts, TEST_REPORT, 'ip_rating')}, while the certificate identifies "
            f"{document_values_line(facts, CERTIFICATE, 'ip_rating')}.",
            "- Manufacturer and certificate identity should be confirmed: the test report names "
            f"{sentence_value(document_values_line(facts, TEST_REPORT, 'manufacturer'))} as manufacturer, while the certificate holder is "
            f"{sentence_value(document_values_line(facts, CERTIFICATE, 'certificate_holder'))}.",
            "- Standards evidence is split across the document set. The certificate supports IEC 61727 and IEC 62116 evidence; the test report supports IEC 62109-1 evidence.",
            "- The exact inverter model intended for Nepal import could not be confirmed from the supplied documents.",
            "",
        ]
    )


def add_additional_documents(lines: list[str]) -> None:
    lines.extend(
        [
            "- IEC 62891 MPPT efficiency evidence.",
            "- IEC 62109-2 inverter safety evidence.",
            "- Warranty agreement with the principal inverter manufacturer.",
            "- Technical catalogue and datasheet for the exact imported model.",
            "- Voltage, frequency, phase sequence, THD, flicker, DC injection, and power factor specifications for Nepal grid-code review.",
            "- Efficiency information, including MPPT efficiency, inverter efficiency, Euro efficiency, and no-load loss.",
            "- Data logging and external user-interface information.",
            "- Protection-function documentation for DC reverse polarity, grid fault, lightning feeder protection, automatic wake-up, synchronization, and shutdown.",
            "- Final product label or nameplate showing rated power, input/output voltage and frequency, maximum input voltage, MPPT range, and serial number.",
            "",
        ]
    )


def generate_final_review_draft(
    facts_path: str,
    mapping_path: str,
    conflict_path: str,
    output_path: str,
) -> None:
    facts = load_extracted_facts(facts_path)
    mapping = load_review_mapping(mapping_path)
    load_conflict_matrix(conflict_path)

    nepqa_standards, other_standards = split_standards(
        values_for_field(facts, "standard")
    )

    lines = [
        "# Nepal Import Review Draft for SunBridge Trading",
        "",
        "## 1. Executive Summary",
        "",
        "The supplied documents provide evidence of PV inverter testing and certification activities, but they do not appear to describe the same inverter model family.",
        "",
        "The test report appears to cover CHISAGE CE-1P single-phase inverter models.",
        "",
        "The certificate appears to cover Deye SUN G06P3 inverter models.",
        "",
        "Several NEPQA-relevant standards were identified, including IEC 61727, IEC 62116, and IEC 62109-1.",
        "",
        "However, the exact inverter model intended for import could not be confirmed from the provided documents.",
        "",
        "Additional documentation may be required before a Nepal import review can be completed.",
        "",
        "## 2. Documents Reviewed",
        "",
    ]

    for source_file in (TEST_REPORT, CERTIFICATE):
        lines.append(f"- {DOCUMENT_LABELS[source_file]}")

    lines.extend(["", "## 3. Product and Variant Review", ""])
    lines.append(
        "The reviewed documents appear to describe different grid-connected photovoltaic inverter families."
    )
    lines.append("")
    add_document_model_review(
        lines,
        facts,
        TEST_REPORT,
        "CHISAGE CE-1P single-phase inverter models",
    )
    add_document_model_review(
        lines,
        facts,
        CERTIFICATE,
        "Deye SUN G06P3 inverter models",
    )

    lines.extend(["## 4. Manufacturer and Certificate Information", ""])
    lines.append(
        f"- Manufacturer named in the test report: {document_values_line(facts, TEST_REPORT, 'manufacturer')}"
    )
    lines.append(
        f"- Applicant named in the test report: {document_values_line(facts, TEST_REPORT, 'applicant')}"
    )
    lines.append(
        f"- Factory named in the test report: {document_values_line(facts, TEST_REPORT, 'factory')}"
    )
    lines.append(
        f"- Certificate holder named in the certificate: {document_values_line(facts, CERTIFICATE, 'certificate_holder')}"
    )
    lines.append(
        f"- Certificate number: {document_values_line(facts, CERTIFICATE, 'certificate_number')}"
    )
    lines.append(
        f"- Test report number: {document_values_line(facts, TEST_REPORT, 'report_number')}"
    )
    lines.append("")

    lines.extend(["## 5. Test and Standards Evidence", ""])
    lines.append("**NEPQA-relevant standards identified:**")
    add_bullets(lines, nepqa_standards)
    lines.append("")
    lines.append("**Other referenced standards identified:**")
    add_bullets(lines, other_standards)
    lines.append("")
    lines.append("**Standards by reviewed document:**")
    lines.append(
        f"- {DOCUMENT_LABELS[TEST_REPORT]}: {document_values_line(facts, TEST_REPORT, 'standard')}"
    )
    lines.append(
        f"- {DOCUMENT_LABELS[CERTIFICATE]}: {document_values_line(facts, CERTIFICATE, 'standard')}"
    )
    lines.append("")

    lines.extend(["## 6. Nepal Import Review Reference Items", ""])
    add_nepal_reference_items(lines, mapping)

    lines.extend(["## 7. Consistent Information Across Documents", ""])
    add_consistent_information(lines)

    lines.extend(["## 8. Mismatches and Items Requiring Confirmation", ""])
    add_mismatch_summary(lines, facts)

    lines.extend(["## 9. Additional Documents Recommended", ""])
    add_additional_documents(lines)

    lines.extend(
        [
            "## 10. Limitations",
            "",
            "- This draft is based only on the supplied documents and identified facts available at the time of review.",
            "- It does not certify compliance or make an import approval decision.",
            "- Certification-body listing, testing scope, and current certificate status were not independently verified.",
            "- The exact inverter model intended for import should be confirmed before relying on this review package.",
            "",
        ]
    )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    generate_final_review_draft(
        facts_path="outputs/extracted_facts.json",
        mapping_path="outputs/nepqa_mapping.json",
        conflict_path="outputs/conflict_matrix.json",
        output_path="outputs/nepal_import_review_final_draft.md",
    )
