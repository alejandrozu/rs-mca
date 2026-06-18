#!/usr/bin/env python3
"""Run a bounded repository verification smoke suite.

This script is intentionally small and standard-library only.  It gives
reviewers one command for the finite verifier layer without committing the
repository to a particular CI provider or test framework.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(sys.executable)


@dataclass(frozen=True)
class Check:
    check_id: str
    suite: str
    description: str
    command: list[str]
    timeout_seconds: int = 120


def rel(path: str) -> str:
    return Path(path).as_posix()


def py(script: str, *args: str) -> list[str]:
    return [str(PYTHON), rel(script), *args]


CHECKS: tuple[Check, ...] = (
    Check(
        "f1-extension-counterexample",
        "smoke",
        "Verified finite counterexamples to unrestricted extension-line MCA lift",
        py("experimental/2026-06-17-codex-f1-l1-audit/verifiers/verify_f1_extension_counterexample.py"),
    ),
    Check(
        "f1-fixed-rate-slice",
        "smoke",
        "Fixed-rate extension-line slice counts",
        py("experimental/2026-06-17-codex-f1-l1-audit/verifiers/verify_f1_fixed_rate_slice.py"),
    ),
    Check(
        "f1-sigma2-degree1",
        "smoke",
        "Degree-one sigma=2 finite extension-line check",
        py("experimental/2026-06-17-codex-f1-l1-audit/verifiers/verify_f1_sigma2_degree1.py"),
    ),
    Check(
        "l1-arbitrary-fiber-overcount",
        "smoke",
        "Locator arbitrary-fiber overcount counterexample",
        py("experimental/2026-06-17-codex-f1-l1-audit/verifiers/verify_l1_arbitrary_fiber_overcount.py"),
    ),
    Check(
        "f1-canonical-extension-witness",
        "smoke",
        "Canonical degree-1 residue-line extension witness",
        py("experimental/f1-extension-witness/verify_ext_witness.py"),
        timeout_seconds=180,
    ),
    Check(
        "paperA-finite-bundle",
        "paperA",
        "Paper A finite-verification bundle",
        py("experimental/verify_paperA_finite.py"),
        timeout_seconds=180,
    ),
)


def command_for_report(command: list[str]) -> list[str]:
    rendered: list[str] = []
    for part in command:
        path = Path(part)
        if path.is_absolute() and path == PYTHON:
            rendered.append("python")
        elif path.is_absolute() and REPO_ROOT in path.parents:
            rendered.append(path.relative_to(REPO_ROOT).as_posix())
        else:
            rendered.append(Path(part).as_posix() if "\\" in part else part)
    return rendered


def excerpt(text: str | bytes | None) -> list[str]:
    if text is None:
        return []
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    return [line.replace("\\", "/") for line in text.strip().splitlines()[:8]]


def selected_checks(suite: str) -> list[Check]:
    if suite == "all":
        return list(CHECKS)
    return [check for check in CHECKS if check.suite == suite]


def run_check(check: Check) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            check.command,
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=check.timeout_seconds,
            check=False,
        )
        duration = time.perf_counter() - started
        return {
            "id": check.check_id,
            "suite": check.suite,
            "description": check.description,
            "command": command_for_report(check.command),
            "exit_code": completed.returncode,
            "ok": completed.returncode == 0,
            "duration_seconds": round(duration, 3),
            "stdout_excerpt": excerpt(completed.stdout),
            "stderr_excerpt": excerpt(completed.stderr),
        }
    except subprocess.TimeoutExpired as exc:
        duration = time.perf_counter() - started
        return {
            "id": check.check_id,
            "suite": check.suite,
            "description": check.description,
            "command": command_for_report(check.command),
            "exit_code": None,
            "ok": False,
            "duration_seconds": round(duration, 3),
            "stdout_excerpt": excerpt(exc.stdout),
            "stderr_excerpt": excerpt(exc.stderr),
            "timeout_seconds": check.timeout_seconds,
            "error": "timeout",
        }


def build_report(suite: str) -> dict[str, Any]:
    checks = [run_check(check) for check in selected_checks(suite)]
    all_ok = all(check["ok"] for check in checks)
    return {
        "status": "PASS" if all_ok else "FAIL",
        "object": "repository verification smoke suite",
        "suite": suite,
        "generated_by": "experimental/run_verification_smoke.py",
        "result": {
            "all_ok": all_ok,
            "check_count": len(checks),
            "passed_count": sum(1 for check in checks if check["ok"]),
        },
        "checks": checks,
    }


def print_text(report: dict[str, Any]) -> None:
    result = report["result"]
    print("Repository verification smoke suite")
    print(f"status: {report['status']}")
    print(f"suite: {report['suite']}")
    print(f"checks: {result['passed_count']}/{result['check_count']} passed")
    print()
    for check in report["checks"]:
        mark = "PASS" if check["ok"] else "FAIL"
        print(f"{mark} {check['id']} ({check['duration_seconds']}s): {check['description']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--suite",
        choices=("smoke", "paperA", "all"),
        default="smoke",
        help="which bounded verifier suite to run",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="print a text summary or the full JSON report",
    )
    parser.add_argument("--json-out", type=Path, help="write the full JSON report")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(args.suite)
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
