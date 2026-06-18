#!/usr/bin/env python3
"""Run the Paper A finite-verification bundle.

This is a convenience wrapper for the existing repository-native certificate
scripts that cover `tex/RS_disproof_v3.tex` Appendix A, items V1--V5, plus the
nearby deployed-field and extension arithmetic certificates.

The wrapper does not reimplement the mathematics.  It executes the underlying
exact scripts, validates the expected finite outputs, and emits one JSON report
that is easy to archive or compare.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(sys.executable)


@dataclass(frozen=True)
class CommandCheck:
    check_id: str
    paper_item: str
    description: str
    command: list[str]
    validate: Callable[[dict[str, Any]], tuple[bool, dict[str, Any]]]


def rel(path: str) -> str:
    return Path(path).as_posix()


def run_command(command: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


def json_command(script: str, *args: str) -> list[str]:
    return [str(PYTHON), rel(script), *args, "--format", "json"]


def validate_path(data: dict[str, Any], path: list[str], expected: Any) -> tuple[bool, dict[str, Any]]:
    value: Any = data
    for key in path:
        value = value[key]
    return value == expected, {"path": ".".join(path), "expected": expected, "actual": value}


def validate_deployed(data: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    ok = bool(data["result"]["all_qualify"])
    return ok, {"all_qualify": ok, "row_count": len(data["result"]["rows"])}


def validate_restricted(expected_size: int, missing_zero: bool) -> Callable[[dict[str, Any]], tuple[bool, dict[str, Any]]]:
    def inner(data: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
        size = int(data["restricted_sum_size"])
        missing = data["missing_values_sample"]
        ok = size == expected_size and ((missing == [0]) if missing_zero else bool(data["full_coverage"]))
        return ok, {
            "restricted_sum_size": size,
            "expected_size": expected_size,
            "full_coverage": bool(data["full_coverage"]),
            "missing_values_sample": missing,
            "missing_zero_expected": missing_zero,
        }

    return inner


def validate_p257(data: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    result = data["result"]
    summary = {
        "subsets_checked": result["subsets_checked"],
        "expected_subsets": result["expected_subsets"],
        "all_subsets_ok": result["all_subsets_ok"],
        "support_size_range": [result["min_support_size"], result["max_support_size"]],
        "unique_slope_count": result["unique_slope_count"],
    }
    ok = (
        result["subsets_checked"] == 11440
        and result["expected_subsets"] == 11440
        and result["all_subsets_ok"]
        and result["min_support_size"] == 144
        and result["max_support_size"] == 144
        and result["unique_slope_count"] == 256
    )
    return ok, summary


def validate_sieve(data: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    result = data["result"]
    summary = {
        "formal_formula_count": result["formal_formula_count"],
        "formal_enumeration_count": result["formal_enumeration_count"],
        "formal_count_ok": result["formal_count_ok"],
        "all_prime_rows_ok": result["all_prime_rows_ok"],
        "row_count": len(result["rows"]),
    }
    ok = bool(result["formal_count_ok"] and result["all_prime_rows_ok"])
    return ok, summary


def validate_extension(data: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    result = data["result"]
    ok = bool(result["all_bases_ok"] and result["all_rates_ok"])
    return ok, {
        "all_bases_ok": result["all_bases_ok"],
        "all_rates_ok": result["all_rates_ok"],
        "base_row_count": len(result["base_rows"]),
        "rate_row_count": len(result["rate_rows"]),
    }


def validate_goldilocks(data: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    result = data["result"]
    ok = bool(result["all_rows_ok"] and result["claimed_goldilocks_bounds_ok"])
    return ok, {
        "all_rows_ok": result["all_rows_ok"],
        "claimed_goldilocks_bounds_ok": result["claimed_goldilocks_bounds_ok"],
        "row_count": len(result["rows"]),
    }


def q17_command() -> list[str]:
    return [
        str(PYTHON),
        rel("experimental/q17_locator_mca/verify_q17_locator_mca.py"),
        "--check",
        rel("experimental/q17_locator_mca/q17_locator_mca_certificate.json"),
    ]


def run_q17_check() -> dict[str, Any]:
    command = q17_command()
    returncode, stdout, stderr = run_command(command)
    certificate_path = REPO_ROOT / "experimental/q17_locator_mca/q17_locator_mca_certificate.json"
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    target_case = None
    for rate in certificate["rates"]:
        if rate["rho"] != "1/2":
            continue
        for case in rate["cases"]:
            if case["N"] == 16 and case["slack_t"] == 1:
                target_case = case
                break
    if target_case is None:
        raise RuntimeError("missing q=17 rho=1/2, N=16, slack-one case")
    histogram = target_case["locator_slope_count_histogram"]
    ok = (
        returncode == 0
        and certificate["status"] == "PROVED"
        and histogram == {"672": 1, "673": 16}
        and target_case["locator_subset_count"] == 11440
        and target_case["locator_slopes_equal_exhaustive_list"]
        and target_case["locator_slopes_equal_exhaustive_mca"]
    )
    return {
        "id": "V3-q17-pigeonhole",
        "paper_item": "V3",
        "description": "q=17, n=16, k=8 distribution 672/673 for 9-subset sums",
        "command": command_for_report(command),
        "exit_code": returncode,
        "ok": ok,
        "summary": {
            "histogram": histogram,
            "locator_subset_count": target_case["locator_subset_count"],
            "list_slopes_equal": target_case["locator_slopes_equal_exhaustive_list"],
            "mca_slopes_equal": target_case["locator_slopes_equal_exhaustive_mca"],
        },
        "stdout_excerpt": excerpt_lines(stdout),
        "stderr_excerpt": excerpt_lines(stderr),
    }


def command_for_report(command: list[str]) -> list[str]:
    result = []
    for part in command:
        try:
            path = Path(part)
            if path.is_absolute() and path == PYTHON:
                result.append("python")
            elif path.is_absolute() and REPO_ROOT in path.parents:
                result.append(path.relative_to(REPO_ROOT).as_posix())
            else:
                result.append(Path(part).as_posix() if "\\" in part else part)
        except ValueError:
            result.append(part)
    return result


def excerpt_lines(text: str) -> list[str]:
    return [line.replace("\\", "/") for line in text.strip().splitlines()[:4]]


def command_checks() -> list[CommandCheck]:
    restricted = "experimental/restricted_sum_dp.py"
    return [
        CommandCheck(
            "A1-deployed-dsh",
            "main(a)",
            "deployed-field DSH divisor arithmetic",
            json_command("experimental/deployed_dsh_certificate.py"),
            validate_deployed,
        ),
        CommandCheck(
            "V1-p17-r5",
            "V1",
            "Fermat quotient coverage p=17, r=M+1=5",
            json_command(restricted, "--p", "17", "--subgroup-order", "8", "--r", "5", "--expect-size", "16"),
            validate_restricted(16, True),
        ),
        CommandCheck(
            "V1-p17-r3",
            "V1",
            "Fermat quotient coverage p=17, r=M/2+1=3",
            json_command(restricted, "--p", "17", "--subgroup-order", "8", "--r", "3", "--expect-size", "16"),
            validate_restricted(16, True),
        ),
        CommandCheck(
            "V1-p257-r9",
            "V1",
            "Fermat quotient coverage p=257, r=M+1=9",
            json_command(restricted, "--p", "257", "--subgroup-order", "16", "--r", "9", "--expect-size", "256"),
            validate_restricted(256, True),
        ),
        CommandCheck(
            "V1-p257-r5",
            "V1",
            "Fermat quotient coverage p=257, r=M/2+1=5",
            json_command(restricted, "--p", "257", "--subgroup-order", "16", "--r", "5", "--expect-size", "256"),
            validate_restricted(256, True),
        ),
        CommandCheck(
            "V1-p65537-r17",
            "V1",
            "Fermat quotient coverage p=65537, r=M+1=17",
            json_command(restricted, "--p", "65537", "--subgroup-order", "32", "--r", "17", "--expect-size", "65536"),
            validate_restricted(65536, True),
        ),
        CommandCheck(
            "V1-p65537-r9",
            "V1",
            "Fermat quotient coverage p=65537, r=M/2+1=9",
            json_command(restricted, "--p", "65537", "--subgroup-order", "32", "--r", "9", "--expect-size", "65536"),
            validate_restricted(65536, True),
        ),
        CommandCheck(
            "V2-p257-locator",
            "V2",
            "p=257 locator expansion and pointwise agreement",
            json_command("experimental/p257_locator_certificate.py"),
            validate_p257,
        ),
        CommandCheck(
            "V4-p12289-ladder",
            "V4",
            "p=12289, N=256 ladder rung full coverage",
            json_command(restricted, "--p", "12289", "--subgroup-order", "256", "--r", "129", "--expect-full"),
            validate_restricted(12289, False),
        ),
        CommandCheck(
            "V5-sieve",
            "V5",
            "N=16, r=9 sieve-mechanism finite reductions",
            json_command("experimental/sieve_mechanism_certificate.py"),
            validate_sieve,
        ),
        CommandCheck(
            "A1-extension-full-density",
            "extension/tower",
            "Fermat/Proth extension full-density arithmetic",
            json_command("experimental/extension_full_density_certificate.py"),
            validate_extension,
        ),
        CommandCheck(
            "A1-goldilocks-density",
            "extension/tower",
            "Goldilocks extension-density arithmetic",
            json_command("experimental/goldilocks_density_certificate.py"),
            validate_goldilocks,
        ),
    ]


def run_json_check(check: CommandCheck) -> dict[str, Any]:
    returncode, stdout, stderr = run_command(check.command)
    parsed: dict[str, Any] | None = None
    ok = False
    summary: dict[str, Any] = {}
    if returncode == 0:
        try:
            parsed = json.loads(stdout)
            ok, summary = check.validate(parsed)
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            summary = {"parse_error": str(exc)}
    return {
        "id": check.check_id,
        "paper_item": check.paper_item,
        "description": check.description,
        "command": command_for_report(check.command),
        "exit_code": returncode,
        "ok": ok,
        "summary": summary,
        "stderr_excerpt": excerpt_lines(stderr),
    }


def build_report() -> dict[str, Any]:
    checks = [run_json_check(check) for check in command_checks()]
    checks.append(run_q17_check())
    checks.sort(key=lambda item: item["id"])
    all_ok = all(bool(item["ok"]) for item in checks)
    return {
        "status": "PROVED" if all_ok else "AUDIT_FAILED",
        "object": "Paper A finite verification bundle",
        "theorem_problem_id": "tex/RS_disproof_v3.tex:app:verify / AGENTS A1",
        "generated_by": "experimental/verify_paperA_finite.py",
        "determinism": "deterministic finite arithmetic; no random seed",
        "scope": (
            "Appendix A V1-V5 plus adjacent deployed-field and extension "
            "arithmetic certificates. No asymptotic theorem is verified here."
        ),
        "result": {
            "all_ok": all_ok,
            "check_count": len(checks),
            "passed_count": sum(1 for item in checks if item["ok"]),
        },
        "checks": checks,
    }


def print_text(report: dict[str, Any]) -> None:
    result = report["result"]
    print("Paper A finite-verification bundle")
    print(f"status: {report['status']}")
    print(f"checks: {result['passed_count']}/{result['check_count']} passed")
    print()
    for item in report["checks"]:
        mark = "PASS" if item["ok"] else "FAIL"
        print(f"{mark} {item['id']} ({item['paper_item']}): {item['description']}")
    print()
    print("scope: " + report["scope"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="print a text summary or the full JSON report",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        help="write the full JSON report to this path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.write_text(rendered, encoding="utf-8")
    if args.format == "json":
        print(rendered, end="")
    else:
        print_text(report)
    return 0 if report["result"]["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
