import json
import os
import re

from schemas import Evidence, ExtractedFacts, ProductFact


def extract_standards(text: str) -> list[str]:
    pattern = r"\bIEC\s{1,2}\d+(?:-\d+)*(?:[:\s]\d{4})?"
    return sorted(set(re.findall(pattern, text)))


def process_file(input_path: str, output_json_path: str):
    filename = os.path.basename(input_path)

    with open(input_path, "r", encoding="utf-8") as file:
        content = file.read()

    pages = re.split(r"--- PAGE (\d+) ---", content)

    facts_list = []

    for i in range(1, len(pages), 2):
        page_num = pages[i]
        page_text = pages[i + 1]

        standards = extract_standards(page_text)

        for standard in standards:
            facts_list.append(
                ProductFact(
                    field_name="standard",
                    raw_value=standard,
                    normalized_value=standard,
                    evidence=Evidence(
                        source_file=filename,
                        page=page_num,
                        quote_or_summary=f"Found standard {standard}",
                        confidence="high",
                    ),
                )
            )

    extracted_facts = ExtractedFacts(facts=facts_list)

    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(extracted_facts.model_dump(), json_file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # target_file = "outputs/extracted_text/188_1115.txt"
    target_file = "outputs/extracted_text/DSS_GZES230100125901_combined-1.txt"
    output_file = "outputs/extracted_facts.json"
    process_file(target_file, output_file)
