import json
from pathlib import Path

from schemas import ExtractedFacts, RequirementMapping, ReviewMapping


NEPQA_REQUIREMENTS = [
    {
        "id": "doc_iec_61727",
        "section": "1.4.2.i.a",
        "category": "required_document",
        "requirement": "IEC 61727:2004 certificate/test evidence should be provided.",
        "field_name": "standard",
        "expected_values": ["IEC 61727"],
    },
    {
        "id": "doc_iec_62116",
        "section": "1.4.2.i.b",
        "category": "required_document",
        "requirement": "IEC 62116:2014 islanding prevention test evidence should be provided.",
        "field_name": "standard",
        "expected_values": ["IEC 62116"],
    },
    {
        "id": "doc_iec_62891",
        "section": "1.4.2.i.c",
        "category": "required_document",
        "requirement": "IEC 62891:2020 MPPT efficiency evidence should be provided.",
        "field_name": "standard",
        "expected_values": ["IEC 62891"],
    },
    {
        "id": "doc_iec_62109_1",
        "section": "1.4.2.i.d",
        "category": "required_document",
        "requirement": "IEC 62109-1:2010 safety evidence should be provided.",
        "field_name": "standard",
        "expected_values": ["IEC 62109-1"],
    },
    {
        "id": "doc_iec_62109_2",
        "section": "1.4.2.i.d",
        "category": "required_document",
        "requirement": "IEC 62109-2:2011 inverter safety evidence should be provided.",
        "field_name": "standard",
        "expected_values": ["IEC 62109-2"],
    },
    {
        "id": "doc_certification_body_scope",
        "section": "1.4.2.i",
        "category": "required_document",
        "requirement": "Certification body or lab should be IECEE/IECRE listed with PV inverter testing scope.",
        "field_name": None,
        "expected_values": [],
    },
    {
        "id": "doc_warranty_agreement",
        "section": "1.4.2.ii",
        "category": "required_document",
        "requirement": "Local importer should provide an agreement with the principal inverter manufacturer stating warranty period.",
        "field_name": "warranty",
        "expected_values": [],
    },
    {
        "id": "doc_catalogue_datasheet",
        "section": "1.4.2.iii",
        "category": "required_document",
        "requirement": "Catalogue and technical datasheet of the PV inverter should be provided.",
        "field_name": "datasheet",
        "expected_values": [],
    },
    {
        "id": "tech_grid_match",
        "section": "1.4.1",
        "category": "general_requirement",
        "requirement": "PV inverter should match grid voltage, frequency, phase angle, and phase sequence.",
        "field_name": None,
        "expected_values": [],
    },
    {
        "id": "tech_grid_code_limits",
        "section": "1.4.1",
        "category": "general_requirement",
        "requirement": "THD, flicker, DC injection, voltage range, frequency range, power factor range, and anti-islanding should follow Nepal grid code.",
        "field_name": None,
        "expected_values": [],
    },
    {
        "id": "tech_ac_output_voltage",
        "section": "1.4.3.i",
        "category": "technical_requirement",
        "requirement": "Rated AC output voltage should be 400+/-10% VAC three-phase or 230+/-10% VAC single-phase.",
        "field_name": "ac_output_voltage",
        "expected_values": ["400", "230"],
    },
    {
        "id": "tech_output_frequency",
        "section": "1.4.3.ii",
        "category": "technical_requirement",
        "requirement": "Output frequency should be 50Hz +/- 2.5%.",
        "field_name": "frequency",
        "expected_values": ["50Hz"],
    },
    {
        "id": "tech_mppt_efficiency",
        "section": "1.4.3.iii",
        "category": "technical_requirement",
        "requirement": "MPPT input efficiency should be at least 95%.",
        "field_name": "mppt_efficiency",
        "expected_values": ["95%"],
    },
    {
        "id": "tech_inverter_efficiency",
        "section": "1.4.3.iv",
        "category": "technical_requirement",
        "requirement": "Inverter efficiency should be at least 95% up to 5kVA and at least 97% above 5kVA for transformerless topology.",
        "field_name": "inverter_efficiency",
        "expected_values": ["95%", "97%"],
    },
    {
        "id": "tech_euro_efficiency",
        "section": "1.4.3.v",
        "category": "technical_requirement",
        "requirement": "Euro efficiency should be at least 94% up to 5kVA and at least 96% above 5kVA for transformerless topology, with efficiency curve.",
        "field_name": "euro_efficiency",
        "expected_values": ["94%", "96%"],
    },
    {
        "id": "tech_transformer_efficiency",
        "section": "1.4.3.vi",
        "category": "technical_requirement",
        "requirement": "Transformer topology inverter efficiency should be at least 90%.",
        "field_name": "inverter_efficiency",
        "expected_values": ["90%"],
    },
    {
        "id": "tech_no_load_loss_transformerless",
        "section": "1.4.3.vii",
        "category": "technical_requirement",
        "requirement": "No-load loss should be less than 0.5% of rated power for transformerless topology.",
        "field_name": "no_load_loss",
        "expected_values": ["0.5%"],
    },
    {
        "id": "tech_no_load_loss_transformer",
        "section": "1.4.3.viii",
        "category": "technical_requirement",
        "requirement": "No-load loss should be less than 1.5% of rated power for transformer topology.",
        "field_name": "no_load_loss",
        "expected_values": ["1.5%"],
    },
    {
        "id": "tech_thd",
        "section": "1.4.3.ix",
        "category": "technical_requirement",
        "requirement": "Total harmonic distortion should be less than 5% at full load.",
        "field_name": "thd",
        "expected_values": ["5%"],
    },
    {
        "id": "tech_power_factor",
        "section": "1.4.3.x",
        "category": "technical_requirement",
        "requirement": "Power factor should be greater than 0.99 at nominal power and adjustable from 0.8 leading to 0.8 lagging.",
        "field_name": "power_factor",
        "expected_values": [">0.99", "0.8 leading", "0.8 lagging"],
    },
    {
        "id": "tech_ip_rating",
        "section": "1.4.3.xi",
        "category": "technical_requirement",
        "requirement": "Ingress protection should be at least IP65 according to IEC 60529.",
        "field_name": "ip_rating",
        "expected_values": ["IP65", "IP66", "IP67", "IP68", "IP69"],
    },
    {
        "id": "tech_data_logger",
        "section": "1.4.3.xii",
        "category": "technical_requirement",
        "requirement": "Inverter should have built-in meter and data logger for external user interface monitoring.",
        "field_name": "data_logger",
        "expected_values": [],
    },
    {
        "id": "tech_protection_features",
        "section": "1.4.3.xiii",
        "category": "technical_requirement",
        "requirement": "Inverter should include DC reverse polarity, grid fault, and lightning feeder protection.",
        "field_name": "protection_features",
        "expected_values": [],
    },
    {
        "id": "tech_automatic_operation",
        "section": "1.4.3.xiv",
        "category": "technical_requirement",
        "requirement": "Inverter should support automatic wake-up, synchronization, and shutdown.",
        "field_name": "automatic_operation",
        "expected_values": [],
    },
    {
        "id": "tech_cooling",
        "section": "1.4.3.xv",
        "category": "technical_requirement",
        "requirement": "Inverter should have fan cooling or an appropriate heat sink to avoid excessive heating.",
        "field_name": "cooling_method",
        "expected_values": [],
    },
    {
        "id": "tech_warranty_period",
        "section": "1.4.3.xvi",
        "category": "technical_requirement",
        "requirement": "PV inverter warranty should be at least 5 years.",
        "field_name": "warranty",
        "expected_values": ["5 years"],
    },
    {
        "id": "label_manufacturer",
        "section": "1.4.3.xvii.a",
        "category": "label_requirement",
        "requirement": "Inverter label should include manufacturer name.",
        "field_name": "manufacturer",
        "expected_values": [],
    },
    {
        "id": "label_brand_model_type",
        "section": "1.4.3.xvii.b",
        "category": "label_requirement",
        "requirement": "Inverter label should include brand, model, and type.",
        "field_name": "model_name",
        "expected_values": [],
    },
    {
        "id": "label_rated_power",
        "section": "1.4.3.xvii.c",
        "category": "label_requirement",
        "requirement": "Inverter label should include rated power in Watt or VA.",
        "field_name": "rated_power",
        "expected_values": [],
    },
    {
        "id": "label_input_output_voltage_frequency",
        "section": "1.4.3.xvii.d",
        "category": "label_requirement",
        "requirement": "Inverter label should include input and output voltage in Volt and frequency in Hz.",
        "field_name": "voltage_frequency_label",
        "expected_values": [],
    },
    {
        "id": "label_max_input_voltage",
        "section": "1.4.3.xvii.e",
        "category": "label_requirement",
        "requirement": "Inverter label should include maximum input voltage.",
        "field_name": "max_input_voltage",
        "expected_values": [],
    },
    {
        "id": "label_mppt_voltage_range",
        "section": "1.4.3.xvii.f",
        "category": "label_requirement",
        "requirement": "Inverter label should include MPPT voltage range.",
        "field_name": "mppt_voltage_range",
        "expected_values": [],
    },
    {
        "id": "label_serial_number",
        "section": "1.4.3.xvii.g",
        "category": "label_requirement",
        "requirement": "Inverter label should include serial number.",
        "field_name": "serial_number",
        "expected_values": [],
    },
]


def load_extracted_facts(path: str) -> ExtractedFacts:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return ExtractedFacts(**data)


def find_matching_facts(
    facts: ExtractedFacts,
    field_name: str,
    expected_values: list[str],
):
    matches = []

    for fact in facts.facts:
        if fact.field_name != field_name:
            continue

        value = fact.normalized_value or fact.raw_value

        if not expected_values:
            matches.append(fact)
            continue

        if any(expected.lower() in value.lower() for expected in expected_values):
            matches.append(fact)

    return matches


def map_requirement(requirement: dict, facts: ExtractedFacts) -> RequirementMapping:
    field_name = requirement["field_name"]
    expected_values = requirement["expected_values"]

    if field_name is None:
        return RequirementMapping(
            requirement=requirement["requirement"],
            status="not_assessed",
            evidence=[],
            notes="This item requires manual review or source verification.",
        )

    matches = find_matching_facts(facts, field_name, expected_values)

    if matches:
        return RequirementMapping(
            requirement=requirement["requirement"],
            status="evidence_found",
            evidence=[fact.evidence for fact in matches],
            notes=f"Matched extracted field: {field_name}",
        )

    return RequirementMapping(
        requirement=requirement["requirement"],
        status="missing",
        evidence=[],
        notes=f"No extracted evidence found for field: {field_name}",
    )


def build_review_mapping(facts: ExtractedFacts) -> ReviewMapping:
    mappings = []

    for requirement in NEPQA_REQUIREMENTS:
        mappings.append(map_requirement(requirement, facts))

    return ReviewMapping(mappings=mappings)


def save_json(mapping: ReviewMapping, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(mapping.model_dump(), file, indent=2, ensure_ascii=False)


def save_markdown(mapping: ReviewMapping, output_path: str) -> None:
    lines = ["# NEPQA Mapping", ""]

    for item in mapping.mappings:
        lines.append(f"## {item.requirement}")
        lines.append("")
        lines.append(f"Status: `{item.status}`")
        lines.append("")

        if item.evidence:
            lines.append("Evidence:")
            for evidence in item.evidence:
                lines.append(
                    f"- {evidence.source_file}, page {evidence.page}: "
                    f"{evidence.quote_or_summary}"
                )
        else:
            lines.append("Evidence: Not found in extracted facts.")

        if item.notes:
            lines.append("")
            lines.append(f"Notes: {item.notes}")

        lines.append("")
        lines.append("---")
        lines.append("")

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    facts = load_extracted_facts("outputs/extracted_facts.json")
    mapping = build_review_mapping(facts)

    save_json(mapping, "outputs/nepqa_mapping.json")
    save_markdown(mapping, "outputs/nepqa_mapping.md")
