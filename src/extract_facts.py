import json
import os
import re

from schemas import Evidence, ExtractedFacts, ProductFact


REGEX_FIELDS = {
    "standard",
    "ip_rating",
    "model_name",
}

LLM_FIELDS = {
    "manufacturer",
    "factory",
    "applicant",
    "certificate_holder",
}


def extract_standards(text: str) -> list[str]:
    pattern = r"\bIEC\s{1,2}\d+(?:-\d+)*(?:[:\s]\d{4})?"
    return sorted(set(re.findall(pattern, text)))


def extract_ip_ratings(text: str) -> list[str]:
    pattern = r"\bIP\s?[0-9X][0-9]\b"
    return sorted(set(re.findall(pattern, text)))


def extract_models(text: str) -> list[str]:
    pattern = r"\b(?:CE|SUN)-\d+[A-Z0-9-]*[A-Z0-9]\b"
    models = sorted(set(re.findall(pattern, text)), key=len, reverse=True)

    final_models: list[str] = []

    for model in models:
        if not any(existing.startswith(model) for existing in final_models):
            final_models.append(model)

    return sorted(final_models)


def llm_extract_candidate_facts(
    text: str,
    source_file: str,
    page: str,
) -> list[ProductFact]:
    return []


def deduplicate_facts(facts: list[ProductFact]) -> list[ProductFact]:
    seen = set()
    unique_facts = []

    for fact in facts:
        key = (
            fact.field_name,
            fact.normalized_value or fact.raw_value,
            fact.evidence.source_file,
            fact.evidence.page,
        )

        if key not in seen:
            seen.add(key)
            unique_facts.append(fact)

    return unique_facts


def process_file(input_path: str, output_json_path: str) -> None:
    filename = os.path.basename(input_path)

    with open(input_path, "r", encoding="utf-8") as file:
        content = file.read()

    pages = re.split(r"--- PAGE (\d+) ---", content)

    facts_list: list[ProductFact] = []

    for i in range(1, len(pages), 2):
        page_num = pages[i]
        page_text = pages[i + 1]

        standards = extract_standards(page_text)
        ip_ratings = extract_ip_ratings(page_text)
        models = extract_models(page_text)

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

        for rating in ip_ratings:
            facts_list.append(
                ProductFact(
                    field_name="ip_rating",
                    raw_value=rating,
                    normalized_value=rating.replace(" ", "").upper(),
                    evidence=Evidence(
                        source_file=filename,
                        page=page_num,
                        quote_or_summary=f"Found IP rating {rating}",
                        confidence="high",
                    ),
                )
            )

        for model in models:
            facts_list.append(
                ProductFact(
                    field_name="model_name",
                    raw_value=model,
                    normalized_value=model,
                    evidence=Evidence(
                        source_file=filename,
                        page=page_num,
                        quote_or_summary=f"Found model {model}",
                        confidence="high",
                    ),
                )
            )

        llm_facts = llm_extract_candidate_facts(
            text=page_text,
            source_file=filename,
            page=page_num,
        )

        facts_list.extend(llm_facts)

    extracted_facts = ExtractedFacts(facts=deduplicate_facts(facts_list))

    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(
            extracted_facts.model_dump(),
            json_file,
            indent=2,
            ensure_ascii=False,
        )


if __name__ == "__main__":
    # target_file = "outputs/extracted_text/188_1115.txt"
    target_file = "outputs/extracted_text/DSS_GZES230100125901_combined-1.txt"

    output_file = "outputs/extracted_facts.json"

    process_file(target_file, output_file)
