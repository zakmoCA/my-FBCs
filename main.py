import re
from collections import defaultdict


def parse_results(file_path):
    with open(file_path, "r") as f:
        content = f.read().lower()

    sections = {
        "vitamin_d": "cumulative serum vitamin d",
        "cholesterol": "cumulative lipid risk report",
        "b12": "cumulative vitamin b12 and folate assays",
        "iron": "cumulative iron studies",
        "serum_biochemistry": "cumulative serum biochemistry",
        "thyroid": "cumulative serum thyroid function tests",
        "fbc": "cumulative full blood examination",
    }

    results = defaultdict(str)

    for key, header in sections.items():
        start = content.find(header)
        if start != -1:
            end = content.find("cumulative", start + len(header))
            end = end if end != -1 else len(content)
            section = content[start:end].strip()
            results[key] = extract_relevant_data(section)
        else:
            results[key] = "section not found."

    return results


def extract_relevant_data(section):
    lines = section.split("\n")
    relevant_data = []

    for line in lines:
        match = re.match(r"([\w\s/]+)\s+([\d.-]+.*\w+/?.*)", line)
        if match:
            test_name, value_unit = match.groups()
            relevant_data.append(f"{test_name.strip():30} | {value_unit.strip()}")

    return "\n".join(relevant_data)


def display_results(results):
    for section, data in results.items():
        print(f"\n--- {section.upper()} ---")
        if data == "section not found.":
            print("no data available for this section.")
        else:
            print(data)
        print("-" * 80)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process a medical report .txt file.")
    parser.add_argument("--file", "-f", type=str, required=True, help="path to the results txt file")
    args = parser.parse_args()

    parsed_results = parse_results(args.file)
    display_results(parsed_results)
