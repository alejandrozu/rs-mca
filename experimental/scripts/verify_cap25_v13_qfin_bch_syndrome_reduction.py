#!/usr/bin/env python3
"""Verify the CAP25 v13 Q-fin BCH-syndrome reduction packet.

This verifier is intentionally arithmetic-only.  It checks the deployed
KoalaBear MCA constants, the BCH/MDS syndrome reformulation, and the numerical
failure of several soft upper-bound routes.  It does not prove the primitive
max-fiber bound.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


OUT = Path(
    "experimental/data/certificates/frontier-adjacent/"
    "kb_mca_qfin_bch_syndrome_reduction_v1.json"
)


def log2_choose(n: int, k: int) -> float:
    return (
        math.lgamma(n + 1)
        - math.lgamma(k + 1)
        - math.lgamma(n - k + 1)
    ) / math.log(2)


def payload_hash(payload: dict[str, Any]) -> str:
    clone = {key: value for key, value in payload.items() if key != "payload_sha256"}
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def write_lf(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def build_payload() -> dict[str, Any]:
    p = 2**31 - 2**24 + 1
    n = 2**21
    k = 2**20
    m = 1_116_048
    w = 67_471
    b_star = p**6 // 2**128
    k_raw = 4_807_520
    nonprimitive_charge = 35_624
    k_rem = k_raw - nonprimitive_charge

    assert p == 2_130_706_433
    assert p - 1 == 1016 * n
    assert m == k + 1 + w
    assert k_rem == 4_771_896
    assert w < n < p

    log2_binom = log2_choose(n, m)
    log2_avg = log2_binom - w * math.log2(p)
    log2_b_star = math.log2(b_star)
    log2_k_raw = math.log2(k_raw)
    log2_k_rem = math.log2(k_rem)

    # Same prefix for two distinct supports forces exchange size e >= w+1.
    min_exchange = w + 1
    max_intersection = m - min_exchange
    assert max_intersection == k

    # Johnson packing from this minimum distance alone.
    packing_radius = w // 2
    log2_ball_last = (
        log2_choose(m, packing_radius)
        + log2_choose(n - m, packing_radius)
    )
    log2_ball_upper = log2_ball_last + math.log2(packing_radius + 1)
    log2_packing_fiber_upper = log2_binom - log2_ball_upper
    packing_ratio_bits = log2_packing_fiber_upper - log2_avg

    # A very generous "fix w coordinates" / MDS-support-style relaxation.
    log2_singleton_relax = log2_choose(n - w, m - w)
    singleton_ratio_bits = log2_singleton_relax - log2_avg

    # Moment conversion barrier: p^(w/r) <= K_rem.
    moment_order_for_krem = math.ceil(w * math.log2(p) / log2_k_rem)
    moment_order_for_kraw = math.ceil(w * math.log2(p) / log2_k_raw)

    return {
        "schema_version": "cap25-v13-qfin-bch-syndrome-reduction-v1",
        "wall_id": "CAP25-V13-QFIN-PRIMITIVE-MAX-ORBIT-FLATNESS-KB-MCA-1116048",
        "status": "AUDIT / REDUCTION / ROUTE_CUT",
        "claim": (
            "The primitive Q-fin wall is exactly a binary constant-weight "
            "BCH/GRS syndrome max-fiber problem; soft packing, singleton-style "
            "MDS support relaxation, and low/fixed moments miss the deployed "
            "finite constant by enormous margins."
        ),
        "non_claims": [
            "does not prove primitive max-orbit flatness",
            "does not prove U(1116048) <= B*",
            "does not change the frontier edge",
            "does not certify any finite safe row",
        ],
        "row": {
            "p": p,
            "p_minus_1_over_n": (p - 1) // n,
            "n": n,
            "k": k,
            "m_safe": m,
            "w_safe": w,
            "B_star": b_star,
            "K_raw": k_raw,
            "nonprimitive_charge_from_rung_audit": nonprimitive_charge,
            "K_rem_primitive_after_charge": k_rem,
            "log2_average_fiber": round(log2_avg, 12),
            "log2_B_star": round(log2_b_star, 12),
            "log2_K_raw": round(log2_k_raw, 12),
            "log2_K_rem": round(log2_k_rem, 12),
        },
        "bch_syndrome_reduction": {
            "domain": "D = alpha * mu_n, n | p-1",
            "indicator_form": (
                "For M subset D, the power-prefix vector is the BCH syndrome "
                "H 1_M, where H_{i,x}=x^i for 1<=i<=w."
            ),
            "mds_check": (
                "Because w < n < p and the x in D are distinct, every w columns "
                "of H form a nonsingular Vandermonde matrix. The ambient linear "
                "code is an [n,n-w,w+1] generalized Reed-Solomon code over F_p."
            ),
            "binary_slice": (
                "Q-fin is not the q-ary coset weight distribution; it is the "
                "binary constant-weight slice {0,1}^n with weight m."
            ),
            "primitive_target": (
                "After quotient-rung charges, the remaining targets have "
                "gcd(n,{i:z_i != 0})=1."
            ),
        },
        "collision_rigidity": {
            "same_prefix_implies_locator_difference_degree_at_most": m - w - 1,
            "min_exchange_size_for_distinct_same_fiber_supports": min_exchange,
            "max_pairwise_intersection_in_one_fiber": max_intersection,
            "max_pairwise_intersection_equals_k": max_intersection == k,
            "interpretation": (
                "Every fiber is a constant-weight family with pairwise "
                "intersection at most k, but this packing fact alone is far "
                "too weak."
            ),
        },
        "soft_route_failures": {
            "johnson_packing_from_min_distance": {
                "packing_radius": packing_radius,
                "log2_ball_upper_bound_used": round(log2_ball_upper, 6),
                "log2_fiber_upper_bound": round(log2_packing_fiber_upper, 6),
                "ratio_to_average_bits": round(packing_ratio_bits, 6),
                "required_ratio_bits": round(log2_k_rem, 6),
                "misses_by_bits": round(packing_ratio_bits - log2_k_rem, 6),
            },
            "singleton_or_fix_w_coordinate_relaxation": {
                "log2_relaxed_fiber_bound": round(log2_singleton_relax, 6),
                "ratio_to_average_bits": round(singleton_ratio_bits, 6),
                "required_ratio_bits": round(log2_k_rem, 6),
                "misses_by_bits": round(singleton_ratio_bits - log2_k_rem, 6),
            },
            "fixed_or_low_moment_conversion": {
                "moment_order_needed_for_K_raw": moment_order_for_kraw,
                "moment_order_needed_for_K_rem": moment_order_for_krem,
                "interpretation": (
                    "Any route of the schematic form max <= avg*p^(w/r) "
                    "needs r around 9.4e4, so r=2,3,4 tail ledgers cannot "
                    "close the finite adjacent row by themselves."
                ),
            },
        },
        "next_valid_closing_routes": [
            "prove primitive binary BCH-syndrome max-fiber flatness directly",
            "prove exchange-compression forcing every heavy primitive fiber into a paid quotient/planted/tangent branch",
            "prove a high-moment or tail hierarchy up to r comparable to w with explicit constants",
            "produce a primitive syndrome whose binary weight-m fiber exceeds K_rem times the average",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()

    payload = build_payload()
    payload["payload_sha256"] = payload_hash(payload)

    if args.check:
        recorded = json.loads(args.check.read_text())
        if recorded != payload:
            raise AssertionError("recorded packet does not match recomputed payload")
        print(f"PASS {args.check.as_posix()}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_lf(args.output, json.dumps(payload, indent=2, sort_keys=True) + "\n")
    if args.emit:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"WROTE {args.output.as_posix()}")
        print(f"payload_sha256={payload['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
