#!/usr/bin/env python3
"""Verify the L2 common-subset upper bound for interleaved RS lists.

For an RS code of dimension k and agreement threshold a >= k, every listed
mu-row interleaved codeword has at least a common agreement columns. Choosing a
canonical a-subset of those common columns injects the direct interleaved list
into the set of a-subsets of the domain. Hence

    |Lambda(Int(C, mu), 1-a/n, U)| <= binom(n, a)

for every received mu-row word U, independently of mu.

This script is a certificate-facing calculator for that proved bound. It is a
coarse upper bound; the sharper L2 support-bridge and codegree notes explain
when smaller common-intersection certificates are available.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from typing import Any

LN2 = math.log(2.0)


def positive_int(raw: str) -> int:
    value = int(raw, 0)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def h2(value: float) -> float:
    if value <= 0.0 or value >= 1.0:
        return 0.0
    return -value * math.log2(value) - (1.0 - value) * math.log2(1.0 - value)


def log2_int(value: int) -> float:
    if value <= 0:
        return float("-inf")
    bits = value.bit_length()
    if bits <= 53:
        return math.log2(value)
    shift = bits - 53
    mantissa = value >> shift
    return math.log2(mantissa) + shift


def log2_binom_estimate(n_value: int, k_value: int, exact_threshold: int) -> tuple[float, bool]:
    if k_value < 0 or k_value > n_value:
        raise ValueError("binomial bottom must satisfy 0 <= k <= n")
    k_value = min(k_value, n_value - k_value)
    if k_value == 0:
        return 0.0, True
    if n_value <= exact_threshold:
        return log2_int(math.comb(n_value, k_value)), True
    return (
        math.lgamma(n_value + 1.0)
        - math.lgamma(k_value + 1.0)
        - math.lgamma(n_value - k_value + 1.0)
    ) / LN2, False


def log2_binom_entropy_bounds(n_value: int, k_value: int) -> tuple[float, float]:
    if k_value < 0 or k_value > n_value:
        raise ValueError("binomial bottom must satisfy 0 <= k <= n")
    if k_value == 0 or k_value == n_value:
        return 0.0, 0.0
    upper = n_value * h2(k_value / n_value)
    lower = max(0.0, upper - math.log2(n_value + 1))
    return lower, upper


def compute_bound(
    n_value: int,
    k_value: int,
    agreement: int,
    mu: int,
    exact_threshold: int,
) -> dict[str, Any]:
    if not (1 <= k_value <= n_value):
        raise ValueError("require 1 <= k <= n")
    if not (k_value <= agreement <= n_value):
        raise ValueError("common-subset injection requires k <= agreement <= n")

    estimate_bits, exact = log2_binom_estimate(n_value, agreement, exact_threshold)
    lower_bits, upper_bits = log2_binom_entropy_bounds(n_value, agreement)
    exact_bound = math.comb(n_value, agreement) if exact else None
    sigma = agreement - k_value

    return {
        "status": "PROVED",
        "object": "L2 common-subset interleaved list bound",
        "theorem_source": "experimental/notes/l2/l2_interleaved_support_bridge.md",
        "parameters": {
            "n": n_value,
            "k": k_value,
            "agreement": agreement,
            "sigma": sigma,
            "rho": str(Fraction(k_value, n_value)),
            "eta": str(Fraction(sigma, n_value)),
            "mu": mu,
        },
        "result": {
            "direct_interleaved_upper_bound": exact_bound,
            "direct_interleaved_upper_bound_exact": exact,
            "log2_upper_bound_estimate": estimate_bits,
            "log2_upper_bound_lower_entropy": lower_bits,
            "log2_upper_bound_upper_entropy": upper_bits,
            "independent_of_mu": True,
        },
        "proof_certificate": {
            "method": "canonical common agreement subset injection",
            "claim": "|Lambda(Int(C,mu),1-a/n,U)| <= binom(n,a) for a >= k",
            "reason": (
                "A listed interleaved tuple has at least a common agreement "
                "columns. A fixed a-subset determines each row codeword "
                "uniquely because a >= k."
            ),
            "scope": (
                "Coarse direct interleaved upper bound. Sharper support-fiber "
                "or codegree certificates may be smaller."
            ),
        },
    }


def built_in_checks(exact_threshold: int) -> dict[str, Any]:
    cases = [
        {
            "id": "boundary_n5_k3_a3",
            "n": 5,
            "k": 3,
            "a": 3,
            "mu": 2,
            "expected_exact": 10,
        },
        {
            "id": "positive_reserve_n6_k3_a4",
            "n": 6,
            "k": 3,
            "a": 4,
            "mu": 2,
            "expected_exact": 15,
        },
        {
            "id": "toy_certificate_n16_k8_a9",
            "n": 16,
            "k": 8,
            "a": 9,
            "mu": 2,
            "expected_exact": 11440,
        },
        {
            "id": "deployed_scale_half_rate_sigma1",
            "n": 1 << 20,
            "k": 1 << 19,
            "a": (1 << 19) + 1,
            "mu": 2,
            "expected_exact": None,
        },
    ]
    rows = []
    all_ok = True
    for case in cases:
        report = compute_bound(
            case["n"],
            case["k"],
            case["a"],
            case["mu"],
            exact_threshold,
        )
        exact_value = report["result"]["direct_interleaved_upper_bound"]
        if case["expected_exact"] is None:
            ok = exact_value is None and not report["result"]["direct_interleaved_upper_bound_exact"]
        else:
            ok = exact_value == case["expected_exact"]
        all_ok = all_ok and ok
        rows.append(
            {
                "id": case["id"],
                "ok": ok,
                "parameters": report["parameters"],
                "result": report["result"],
            }
        )
    return {
        "status": "PASS" if all_ok else "FAIL",
        "object": "L2 common-subset bound built-in checks",
        "checks": rows,
    }


def print_human(report: dict[str, Any]) -> None:
    if "checks" in report:
        print("L2 common-subset bound built-in checks")
        print(f"status: {report['status']}")
        for row in report["checks"]:
            result = row["result"]
            print(
                "{id}: {ok}; n={n} k={k} a={agreement} mu={mu}; "
                "log2_bound={bits:.12g}; exact={exact}".format(
                    id=row["id"],
                    ok="PASS" if row["ok"] else "FAIL",
                    n=row["parameters"]["n"],
                    k=row["parameters"]["k"],
                    agreement=row["parameters"]["agreement"],
                    mu=row["parameters"]["mu"],
                    bits=result["log2_upper_bound_estimate"],
                    exact=result["direct_interleaved_upper_bound_exact"],
                )
            )
        return

    params = report["parameters"]
    result = report["result"]
    print("L2 common-subset interleaved list bound")
    print(
        "n={n} k={k} agreement={agreement} sigma={sigma} mu={mu}".format(
            **params
        )
    )
    print(f"exact bound: {result['direct_interleaved_upper_bound']}")
    print(f"exact used: {result['direct_interleaved_upper_bound_exact']}")
    print(f"log2 estimate: {result['log2_upper_bound_estimate']:.12g}")
    print(f"entropy lower: {result['log2_upper_bound_lower_entropy']:.12g}")
    print(f"entropy upper: {result['log2_upper_bound_upper_entropy']:.12g}")
    print("independent of mu: yes")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=positive_int)
    dim = parser.add_mutually_exclusive_group()
    dim.add_argument("--k", type=positive_int)
    dim.add_argument("--rho-den", type=positive_int)
    agreement = parser.add_mutually_exclusive_group()
    agreement.add_argument("--agreement", type=positive_int)
    agreement.add_argument("--sigma", type=positive_int)
    parser.add_argument("--mu", type=positive_int, default=2)
    parser.add_argument("--exact-threshold", type=positive_int, default=5000)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.n is None:
        report = built_in_checks(args.exact_threshold)
    else:
        if args.k is None and args.rho_den is None:
            raise SystemExit("provide --k or --rho-den with --n")
        k_value = args.k if args.k is not None else args.n // args.rho_den
        if args.agreement is None and args.sigma is None:
            raise SystemExit("provide --agreement or --sigma with --n")
        agreement = args.agreement if args.agreement is not None else k_value + args.sigma
        try:
            report = compute_bound(
                args.n,
                k_value,
                agreement,
                args.mu,
                args.exact_threshold,
            )
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report["status"] in {"PASS", "PROVED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
