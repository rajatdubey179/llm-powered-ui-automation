"""
LLM to Test Converter — Converts Ollama-generated test cases (txt) into
executable Playwright pytest files inside the tests/ folder.

Usage:
    python llm_to_test.py                                  # uses reports/generated_test_cases.txt
    python llm_to_test.py --file reports/my_cases.txt      # custom file
"""

import re
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def parse_test_cases(content: str) -> list[dict]:
    """
    Parse test cases from Ollama output.
    Handles the format:
        N. Test Case Title: <title>
           - Preconditions: <text>
           - Test Steps (numbered): ...
           - Expected Result: <text>
           - Priority: <text>
    """
    cases = []

    # Split on numbered entries like: 1. Test Case Title: ...
    blocks = re.split(r"\n(?=\d+\.\s+Test Case Title)", content, flags=re.IGNORECASE)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Title
        title_match = re.search(r"\d+\.\s+Test Case Title:\s*(.+)", block, re.IGNORECASE)
        if not title_match:
            continue
        title = title_match.group(1).strip()

        # Preconditions
        pre_match = re.search(r"Preconditions?:\s*(.+?)(?=\n\s*-?\s*Test Steps?|\Z)", block, re.DOTALL | re.IGNORECASE)
        preconditions = pre_match.group(1).strip() if pre_match else ""

        # Steps
        steps_match = re.search(r"Test Steps?.*?:\s*(.+?)(?=\n\s*-?\s*Expected|\Z)", block, re.DOTALL | re.IGNORECASE)
        steps = steps_match.group(1).strip() if steps_match else ""

        # Expected result
        expected_match = re.search(r"Expected Results?:\s*(.+?)(?=\n\s*-?\s*Priority|\Z)", block, re.DOTALL | re.IGNORECASE)
        expected = expected_match.group(1).strip() if expected_match else ""

        # Priority
        priority_match = re.search(r"Priority:\s*(\w+)", block, re.IGNORECASE)
        priority = priority_match.group(1).strip() if priority_match else "Medium"

        cases.append({
            "title": title,
            "preconditions": preconditions,
            "steps": steps,
            "expected": expected,
            "priority": priority,
        })

    return cases


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "generated_test"


def extract_steps(text: str) -> list[str]:
    return [
        re.sub(r"^\d+\.\s*", "", line.strip())
        for line in text.splitlines()
        if re.match(r"^\d+\.", line.strip())
    ]


def detect_page_object(title: str, steps: str) -> str:
    combined = (title + " " + steps).lower()
    if "login" in combined or "sign in" in combined or "password" in combined:
        return "login"
    if "hotel" in combined or "stay" in combined or "check-in" in combined:
        return "hotel"
    if "flight" in combined or "departure" in combined or "arrival" in combined:
        return "flight"
    return "login"


def build_test_body(case: dict) -> list[str]:
    """Generate actual executable Playwright lines based on the test case content."""
    title = case["title"].lower()
    steps = case["steps"].lower()
    expected = case["expected"].lower()
    page_type = detect_page_object(case["title"], case["steps"])
    lines = []

    if page_type == "login":
        lines.append("    from pages.login_page import LoginPage")
        lines.append("    login = LoginPage(page)")
        lines.append("    login.navigate()")

        if "invalid username" in title or "invalid username" in steps:
            lines.append('    login.login("invalid_user@fake.com", "secret_sauce")')
            lines.append("    assert login.has_error_message(), 'Expected error for invalid username'")

        elif "invalid password" in title or "invalid password" in steps:
            lines.append('    login.login("user@phptravels.com", "wrongpassword")')
            lines.append("    assert login.has_error_message(), 'Expected error for invalid password'")

        elif "empty" in title or "empty" in steps:
            lines.append('    login.login("", "")')
            lines.append("    assert login.has_error_message() or 'login' in page.url, 'Expected to stay on login page'")

        elif "locked" in title or "locked" in steps:
            lines.append('    login.login("locked_out_user", "secret_sauce")')
            lines.append("    assert login.has_error_message(), 'Expected error for locked user'")

        else:
            lines.append('    login.login("user@phptravels.com", "demouser")')
            lines.append("    assert login.is_logged_in(), 'Expected successful login'")

    elif page_type == "hotel":
        lines.append("    from pages.hotels_page import HotelsPage")
        lines.append("    hotels = HotelsPage(page)")
        lines.append("    hotels.open()")

        if "empty" in title or "empty" in steps:
            lines.append("    hotels.search_button.click()")
            lines.append("    error = page.locator('.error, .alert, [class*=\"error\"]').first")
            lines.append("    assert error.is_visible() or not hotels.has_results(), 'Expected validation error'")

        elif "invalid" in title or "past" in title:
            lines.append('    hotels.destination_input.fill("Dubai")')
            lines.append('    hotels.checkin_input.fill("2020-01-01")')
            lines.append('    hotels.checkout_input.fill("2020-01-02")')
            lines.append("    hotels.search_button.click()")
            lines.append("    page.wait_for_load_state('networkidle')")
            lines.append("    error = page.locator('.error, .alert, [class*=\"error\"]').first")
            lines.append("    assert error.is_visible() or not hotels.has_results(), 'Expected error for invalid date'")

        else:
            lines.append('    hotels.search("Dubai", "2025-10-01", "2025-10-05")')
            lines.append("    assert hotels.has_results(), 'Expected hotel results'")

    elif page_type == "flight":
        lines.append("    from pages.flights_page import FlightsPage")
        lines.append("    flights = FlightsPage(page)")
        lines.append("    flights.open()")
        lines.append("    flights.select_one_way()")
        lines.append('    flights.search("Dubai", "London", "2025-10-01")')
        lines.append("    assert flights.has_results(), 'Expected flight results'")

    return lines


def to_pytest_file(feature: str, cases: list[dict]) -> str:
    """Build a complete pytest file string from parsed test cases."""
    lines = []
    lines.append(f'"""Tests for: {feature}"""')
    lines.append("")
    lines.append("import pytest")
    lines.append("")
    lines.append("")

    for i, case in enumerate(cases, 1):
        fn_name = f"test_{slugify(case['title'])}"
        priority = case["priority"]

        lines.append(f"# TC-{i} | Priority: {priority}")
        lines.append(f"def {fn_name}(page):")
        lines.append(f'    """{case["title"]}"""')

        body = build_test_body(case)
        lines.extend(body)
        lines.append("")
        lines.append("")

    return "\n".join(lines)


def derive_filename(feature: str) -> str:
    name = slugify(re.sub(r"[^a-zA-Z0-9 ]", "", feature))
    return f"test_{name[:60]}.py"


def main():
    if "--file" in sys.argv:
        idx = sys.argv.index("--file")
        input_file = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
    else:
        input_file = "reports/generated_test_cases.txt"

    if not input_file or not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}")
        print("Run first: python llm_runner.py generate \"<feature>\"")
        sys.exit(1)

    with open(input_file, encoding="utf-8") as f:
        content = f.read()

    feature = content.splitlines()[0].replace("Feature:", "").strip()
    print(f"\nFeature : {feature}")

    cases = parse_test_cases(content)
    if not cases:
        print("ERROR: No test cases found. Paste the txt content if the format is unexpected.")
        sys.exit(1)

    print(f"Found   : {len(cases)} test case(s)")
    for i, c in enumerate(cases, 1):
        print(f"  TC-{i}: {c['title']} [{c['priority']}]")

    filename = derive_filename(feature)
    output_path = Path("tests") / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(to_pytest_file(feature, cases), encoding="utf-8")

    print(f"\n✓ Test file saved: {output_path}")
    print(f"\nRun with:")
    print(f"    pytest {output_path} -v")


if __name__ == "__main__":
    main()
