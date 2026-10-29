"""
Sandboxed Code Execution Engine Service
Integrates with Judge0 CE / RapidAPI Judge0 API with complete support for
compilation, runtime execution, standard I/O, output normalization,
and competitive programming testcase judging.
"""
import time
import re
import httpx
from typing import Dict, List, Any, Optional
from ..config import get_settings

settings = get_settings()

# Language ID mapping for Judge0
LANGUAGE_MAP = {
    "python": 71,       # Python (3.8.1)
    "py": 71,
    "cpp": 54,          # C++ (GCC 9.2.0)
    "c++": 54,
    "java": 62,         # Java (OpenJDK 13.0.1)
}


def normalize_output(text: Optional[str]) -> str:
    """
    Normalizes program output for robust judging:
    - Normalizes Windows CRLF to LF.
    - Strips trailing whitespace on each line.
    - Strips leading and trailing blank lines.
    """
    if text is None:
        return ""
    # Normalize line breaks
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Strip trailing whitespace on each line
    lines = [line.rstrip() for line in text.split("\n")]
    # Strip empty lines from head and tail
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines).strip()


def outputs_match(actual: str, expected: str) -> bool:
    """
    Compares actual and expected outputs according to normalized policy.
    Supports exact match, normalized space-separated tokens, and boolean synonyms.
    """
    norm_actual = normalize_output(actual)
    norm_expected = normalize_output(expected)

    if norm_actual == norm_expected:
        return True

    # Case-insensitive comparison for boolean results
    if norm_actual.lower() == norm_expected.lower() and norm_expected.lower() in ("true", "false", "yes", "no"):
        return True

    # Check token-by-token comparison (handles multiple whitespace differences between numbers)
    actual_tokens = norm_actual.split()
    expected_tokens = norm_expected.split()
    if actual_tokens == expected_tokens:
        return True

    return False


def get_judge0_headers() -> Dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    api_key = getattr(settings, "judge0_api_key", "").strip()
    api_host = getattr(settings, "judge0_api_host", "").strip()

    if api_key:
        headers["X-RapidAPI-Key"] = api_key
        if api_host:
            headers["X-RapidAPI-Host"] = api_host
    return headers


def get_judge0_base_url() -> str:
    base = getattr(settings, "judge0_api_url", "https://ce.judge0.com").rstrip("/")
    return base


def run_single_execution(
    source_code: str,
    language: str,
    stdin: str = "",
    cpu_time_limit: float = 3.0,
    memory_limit_kb: int = 128000
) -> Dict[str, Any]:
    """
    Submits code to Judge0 sandbox and synchronously polls for execution result.
    Enforces time and memory limits, captures stdout, stderr, and compilation errors.
    """
    lang_key = language.lower().strip()
    lang_id = LANGUAGE_MAP.get(lang_key)
    if not lang_id:
        return {
            "success": False,
            "status": "Compilation Error",
            "compile_output": f"Unsupported language: '{language}'. Supported: python, cpp, java.",
            "stdout": None,
            "stderr": None,
            "time": 0,
            "memory": 0,
        }

    base_url = get_judge0_base_url()
    headers = get_judge0_headers()

    payload = {
        "source_code": source_code,
        "language_id": lang_id,
        "stdin": stdin,
        "cpu_time_limit": cpu_time_limit,
        "memory_limit": memory_limit_kb,
    }

    try:
        with httpx.Client(timeout=15.0) as client:
            # 1. Create submission
            submit_resp = client.post(
                f"{base_url}/submissions?base64_encoded=false",
                json=payload,
                headers=headers
            )

            if submit_resp.status_code not in (200, 201):
                return {
                    "success": False,
                    "status": "Execution Service Error",
                    "stderr": f"Judge0 submission failed (HTTP {submit_resp.status_code}): {submit_resp.text}",
                    "compile_output": None,
                    "stdout": None,
                    "time": 0,
                    "memory": 0,
                }

            token = submit_resp.json().get("token")
            if not token:
                return {
                    "success": False,
                    "status": "Execution Service Error",
                    "stderr": "No execution token returned by sandbox service.",
                    "compile_output": None,
                    "stdout": None,
                    "time": 0,
                    "memory": 0,
                }

            # 2. Poll for completion
            # Status IDs in Judge0: 1: In Queue, 2: Processing, 3: Accepted, 4: Wrong Answer,
            # 5: Time Limit Exceeded, 6: Compilation Error, 7-12: Runtime Error
            max_attempts = 15
            for attempt in range(max_attempts):
                time.sleep(0.6 if attempt < 3 else 1.0)
                get_resp = client.get(
                    f"{base_url}/submissions/{token}?base64_encoded=false",
                    headers=headers
                )
                if get_resp.status_code == 200:
                    data = get_resp.json()
                    status_info = data.get("status", {})
                    status_id = status_info.get("id", 1)

                    if status_id not in (1, 2):  # Finished!
                        stdout = data.get("stdout") or ""
                        stderr = data.get("stderr") or ""
                        compile_output = data.get("compile_output") or ""
                        time_spent = float(data.get("time") or 0)
                        memory_spent = int(data.get("memory") or 0)
                        status_desc = status_info.get("description", "Unknown")

                        # Categorize result
                        if status_id == 6:
                            verdict = "Compilation Error"
                        elif status_id == 5:
                            verdict = "Time Limit Exceeded"
                        elif status_id in (7, 8, 9, 10, 11, 12):
                            verdict = "Runtime Error"
                        elif status_id == 13 or status_id == 14:
                            verdict = "Internal Error"
                        else:
                            verdict = "Success"

                        return {
                            "success": (status_id == 3 or verdict == "Success"),
                            "status": verdict,
                            "status_description": status_desc,
                            "stdout": stdout,
                            "stderr": stderr,
                            "compile_output": compile_output,
                            "time": time_spent,
                            "memory": memory_spent,
                        }

            return {
                "success": False,
                "status": "Time Limit Exceeded",
                "stderr": "Execution timed out while waiting for sandbox response.",
                "compile_output": None,
                "stdout": None,
                "time": cpu_time_limit,
                "memory": 0,
            }

    except httpx.RequestError as exc:
        return {
            "success": False,
            "status": "Network Error",
            "stderr": f"Could not reach code execution sandbox: {str(exc)}",
            "compile_output": None,
            "stdout": None,
            "time": 0,
            "memory": 0,
        }


def judge_problem_submission(
    source_code: str,
    language: str,
    test_cases: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Evaluates a solution against a suite of test cases (both public and hidden).
    Returns detailed summary without leaking hidden test case inputs or expected outputs.
    """
    if not test_cases:
        return {
            "verdict": "Accepted",
            "passed_count": 0,
            "total_count": 0,
            "runtime_ms": 0,
            "memory_kb": 0,
            "test_results": [],
            "score": 100.0,
            "feedback": "No test cases configured.",
        }

    total_count = len(test_cases)
    passed_count = 0
    max_runtime_sec = 0.0
    max_memory_kb = 0
    results_summary = []
    overall_verdict = "Accepted"
    first_failure_reason = None

    for idx, tc in enumerate(test_cases):
        test_input = tc.get("input", "")
        expected_output = tc.get("expected_output", "")
        is_hidden = tc.get("is_hidden", False)

        exec_res = run_single_execution(source_code, language, stdin=test_input)

        runtime = exec_res.get("time", 0.0)
        memory = exec_res.get("memory", 0)
        if runtime > max_runtime_sec:
            max_runtime_sec = runtime
        if memory > max_memory_kb:
            max_memory_kb = memory

        status = exec_res.get("status")

        # If compilation failed, stop immediately — all tests fail with Compilation Error
        if status == "Compilation Error":
            return {
                "verdict": "Compilation Error",
                "passed_count": 0,
                "total_count": total_count,
                "runtime_ms": 0,
                "memory_kb": 0,
                "score": 0.0,
                "compile_output": exec_res.get("compile_output"),
                "feedback": exec_res.get("compile_output") or "Compilation failed. Check your syntax and types.",
                "test_results": [
                    {
                        "test_number": 1,
                        "status": "Compilation Error",
                        "error": exec_res.get("compile_output"),
                        "is_hidden": False,
                    }
                ],
            }

        # Check execution status
        if status in ("Runtime Error", "Time Limit Exceeded", "Internal Error"):
            test_passed = False
            case_verdict = status
            if overall_verdict == "Accepted":
                overall_verdict = status
                first_failure_reason = f"Test Case {idx + 1} encountered {status}: {exec_res.get('stderr') or ''}"
        else:
            # Check correctness against expected output
            actual_stdout = exec_res.get("stdout", "")
            if outputs_match(actual_stdout, expected_output):
                test_passed = True
                case_verdict = "Passed"
                passed_count += 1
            else:
                test_passed = False
                case_verdict = "Wrong Answer"
                if overall_verdict == "Accepted":
                    overall_verdict = "Wrong Answer"
                    first_failure_reason = f"Test Case {idx + 1} produced incorrect output."

        # Record testcase summary (mask hidden test cases to prevent cheating)
        res_entry = {
            "test_number": idx + 1,
            "status": case_verdict,
            "passed": test_passed,
            "runtime_ms": int(runtime * 1000),
            "memory_kb": memory,
            "is_hidden": is_hidden,
        }

        if not is_hidden:
            res_entry["input"] = test_input
            res_entry["expected_output"] = expected_output
            res_entry["actual_output"] = exec_res.get("stdout", "")
            if exec_res.get("stderr"):
                res_entry["error"] = exec_res.get("stderr")
        else:
            # Hidden test case: do not reveal input or expected output
            res_entry["message"] = "Hidden test case"

        results_summary.append(res_entry)

    score = round((passed_count / total_count) * 100.0, 2) if total_count > 0 else 0.0

    return {
        "verdict": overall_verdict,
        "passed_count": passed_count,
        "total_count": total_count,
        "runtime_ms": int(max_runtime_sec * 1000),
        "memory_kb": max_memory_kb,
        "score": score,
        "feedback": first_failure_reason if overall_verdict != "Accepted" else f"All {total_count} test cases passed successfully!",
        "test_results": results_summary,
    }
