"""
LLM Runner — Generate test cases or analyze test failures using a local Ollama model.

Usage:
    python llm_runner.py generate "Tours search with invalid destination"
    python llm_runner.py analyze "TimeoutError: button not found after 30000ms"
    python llm_runner.py analyze --file reports/last_failure.txt
"""

import sys
import os
from utils.llm_helper import LLMHelper


def generate(feature_description: str):
    print("\n" + "=" * 60)
    print(f"Generating test cases for: {feature_description}")
    print("=" * 60 + "\n")

    llm = LLMHelper()
    result = llm.generate_test_cases(feature_description)
    print(result)

    output_path = "reports/generated_test_cases.txt"
    os.makedirs("reports", exist_ok=True)
    with open(output_path, "w") as f:
        f.write(f"Feature: {feature_description}\n\n")
        f.write(result)
    print(f"\n✓ Saved to {output_path}")


def analyze(error_log: str):
    print("\n" + "=" * 60)
    print("Analyzing failure with AI...")
    print("=" * 60 + "\n")

    llm = LLMHelper()
    result = llm.analyze_failure(error_log)
    print(result)

    output_path = "reports/failure_analysis.txt"
    os.makedirs("reports", exist_ok=True)
    with open(output_path, "w") as f:
        f.write(result)
    print(f"\n✓ Saved to {output_path}")


def print_help():
    print("""
LLM Runner — supports two commands:

1. GENERATE TEST CASES:
   python llm_runner.py generate "<feature description>"

   Examples:
   python llm_runner.py generate "Hotel search with invalid check-in date"
   python llm_runner.py generate "Flight booking for 10 passengers"
   python llm_runner.py generate "Login with special characters in password"

2. ANALYZE A FAILURE (paste error directly):
   python llm_runner.py analyze "<error message>"

   Example:
   python llm_runner.py analyze "TimeoutError: Locator.click exceeded 30000ms waiting for button"

3. ANALYZE A FAILURE (from saved log file):
   python llm_runner.py analyze --file reports/last_failure.txt
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    command = sys.argv[1]

    if command == "generate":
        if len(sys.argv) < 3:
            print("ERROR: Provide a feature description.\nExample: python llm_runner.py generate \"Login page test\"")
            sys.exit(1)
        generate(sys.argv[2])

    elif command == "analyze":
        if len(sys.argv) < 3:
            print("ERROR: Provide an error log.\nExample: python llm_runner.py analyze \"TimeoutError...\"")
            sys.exit(1)

        if sys.argv[2] == "--file":
            if len(sys.argv) < 4:
                print("ERROR: Provide a file path.\nExample: python llm_runner.py analyze --file reports/last_failure.txt")
                sys.exit(1)
            with open(sys.argv[3]) as f:
                error_log = f.read()
            analyze(error_log)
        else:
            analyze(sys.argv[2])

    else:
        print(f"ERROR: Unknown command '{command}'")
        print_help()
        sys.exit(1)
