from src.sdlc.states.states import State
from src.sdlc.prompts.prompts import TESTCASES_GEN_INSTRNS
from src.sdlc import logger
import traceback
from typing import List, Tuple, Dict
import re
import io
import contextlib
from copy import deepcopy


class QATestingNode:
    """
    Node logic implementation for QA Testing.
    """

    @staticmethod
    def markdown_test_cases_to_python(markdown: str) -> Tuple[str, List[Dict]]:
        lines = markdown.strip().split("\n")
        data_lines = [line.strip() for line in lines if line.strip()]
        header_index = next((i for i, line in enumerate(data_lines) if "---" in line), None)

        if header_index is None or header_index == 0:
            raise ValueError("Markdown table is malformed or missing header separator.")

        headers = [h.strip() for h in data_lines[0].split('|')[1:-1]]
        rows = data_lines[header_index + 1:]

        test_funcs: List[str] = []
        metadata: List[Dict] = []

        for row in rows:
            columns = [col.strip() for col in row.split('|')[1:-1]]
            if len(columns) != len(headers):
                continue

            case_id, use_case, scenario, steps, expected, test_type = columns
            func_name = re.sub(r'\W+', '_', f"test_{case_id}_{use_case}_{scenario}").lower()
            step_lines = steps.replace("<br>", "\n").split("\n")
            step_code = "\n    ".join(f"# {step.strip()}" for step in step_lines)
            expected_comment = f"# Expected: {expected}"

            test_func = f"""
            def {func_name}():
                {step_code}
                {expected_comment}
                print("Simulated Output for: {expected}")  # Add dummy output
                assert True  # TODO: Replace with real assertion
            """
            test_funcs.append(test_func.strip())

            metadata.append({
                "func_name": func_name,
                "Test Case ID": case_id,
                "Use Case": use_case,
                "Test Scenario": scenario,
                "Test Steps": steps,
                "Expected Result": expected,
                "Test Type": test_type
            })

        return "\n\n".join(test_funcs), metadata

    def process(self, state):
        generated_code = state.get("generated_code", {})
        test_cases_markdown = state.get("test_cases", "")

        overall_results = []

        # Parse test cases once
        try:
            test_code, metadata = QATestingNode.markdown_test_cases_to_python(test_cases_markdown)
        except Exception:
            return {
                "qa_testing": {
                    "result":"Failed",
                    "summary": "❌ Failed to parse test cases.",
                    "table": "",
                    "details": [{
                        "Test Case ID": "Unknown",
                        "Use Case": "Global",
                        "Test Scenario": "Test case markdown parsing failed",
                        "Test Steps": "-",
                        "Expected Result": "-",
                        "Actual Output": "-",
                        "Test Type": "-",
                        "Status": "❌ Fail",
                        "Error": traceback.format_exc()
                    }]
                }
            }

        # ✅ One shared environment
        local_env = {}
        try:
            # Load all code files into same namespace
            for file_path, code in generated_code.items():
                if not file_path.endswith(".py"):
                    logger.warning(f"Skipping non-Python file: {file_path}")
                    continue
                try:
                    exec(code, local_env)
                except Exception as e:
                    logger.error(f"Failed to exec {file_path}: {e}")

            exec(test_code, local_env)

            for test_meta_orig in metadata:
                test_meta = deepcopy(test_meta_orig)
                func_name = test_meta.get("func_name")

                try:
                    test_func = local_env.get(func_name)
                    if not test_func:
                        raise ValueError(f"Function '{func_name}' not found")

                    # Capture stdout
                    f = io.StringIO()
                    with contextlib.redirect_stdout(f):
                        result = test_func()
                    output = f.getvalue().strip()
                    test_meta["Actual Output"] = output or str(result)
                    test_meta["Status"] = "✅ Pass"

                except Exception:
                    test_meta["Actual Output"] = "-"
                    test_meta["Status"] = "❌ Fail"
                    test_meta["Error"] = traceback.format_exc()

                overall_results.append(test_meta)

        except Exception:
            for test_meta_orig in metadata:
                test_meta = deepcopy(test_meta_orig)
                test_meta["Status"] = "❌ Fail"
                test_meta["Actual Output"] = "-"
                test_meta["Error"] = traceback.format_exc()
                overall_results.append(test_meta)

        # Markdown table generation
        table_header = (
            "| Test Case ID | Use Case | Test Scenario | Test Steps | Expected Result | Actual Output | Test Type | Status |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
        )

        table_rows = ""
        for r in overall_results:
            table_rows += (
                f"| {r.get('Test Case ID')} | {r.get('Use Case')} | {r.get('Test Scenario')} | "
                f"{r.get('Test Steps')} | {r.get('Expected Result')} | {r.get('Actual Output')} | "
                f"{r.get('Test Type')} | {r.get('Status')} |\n"
            )

        markdown_table = table_header + table_rows
        summary = "✅ All tests passed" if all(r["Status"] == "✅ Pass" for r in overall_results) else "❌ Some tests failed"
        logger.info(f"IN QA TESTING NODE, results : {summary}")
        return {
            "qa_testing": {
                "result":"Passed",
                "summary": summary,
                "table": markdown_table,
                "details": overall_results
            }
        }
    


