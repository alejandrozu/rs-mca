#!/usr/bin/env python3
"""Replay the F_17^32 M3 endpoint rank-witness packets.

This verifier keeps the two endpoint stress packets in
``experimental/notes/m1/f17_32_m3_rank_witness_packet.md`` honest.  It checks
that the deterministic input generator, the regular-Hankel extractor, and the
aperiodic eliminant packet checker all agree for A=385 and A=426.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ENDPOINTS = {
    385: {
        "input": ROOT
        / "experimental/data/hankel-regular-minor-inputs/"
        "f17_32_n512_k256_a385_rank_witness_input.json",
        "packet": ROOT
        / "experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/"
        "f17_32_n512_k256_a385_rank_witness_packet.json",
    },
    426: {
        "input": ROOT
        / "experimental/data/hankel-regular-minor-inputs/"
        "f17_32_n512_k256_a426_rank_witness_input.json",
        "packet": ROOT
        / "experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/"
        "f17_32_n512_k256_a426_rank_witness_packet.json",
    },
}


def run(args: list[str]) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def repo_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> None:
    for agreement, paths in ENDPOINTS.items():
        print(f"checking F_17^32 M3 endpoint A={agreement}")
        run(
            [
                sys.executable,
                "experimental/scripts/emit_f17_32_m3_rank_witness_input.py",
                "--agreement",
                str(agreement),
                "--check",
                repo_path(paths["input"]),
            ]
        )
        run(
            [
                sys.executable,
                "experimental/scripts/extract_regular_hankel_minors.py",
                repo_path(paths["input"]),
                "--check",
                repo_path(paths["packet"]),
            ]
        )
        run(
            [
                sys.executable,
                "scripts/check_aperiodic_eliminant_packet.py",
                repo_path(paths["packet"]),
            ]
        )
    print("F_17^32 M3 endpoint rank-witness packets: PASS")


if __name__ == "__main__":
    main()
