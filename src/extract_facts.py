import re


def extract_standards(text: str) -> list[str]:
    pattern = r"IEC\s+\d+(?:-\d+)*(?:[:\s]\d{4})?"
    return sorted(set(re.findall(pattern, text)))


def process_file(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        standards = extract_standards(content)

        if standards:
            print(f"--- Found {len(standards)} IEC Standards ---")
            for standard in standards:
                print(f" - {standard}")
        else:
            print("No IEC standards were found in the file.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' could not be found.")


if __name__ == "__main__":
    target_file = "outputs/extracted_text/DSS_GZES230100125901_combined-1.txt"
    # target_file = "outputs/extracted_text/188_1115.txt"
    process_file(target_file)
