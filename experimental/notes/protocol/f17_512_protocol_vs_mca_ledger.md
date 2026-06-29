# F17 512 Protocol-vs-MCA Ledger Readout

- **Status:** AUDIT / SCANNER-READOUT
- **Agent/model:** Codex
- **Date:** 2026-06-30
- **Scope:** `F_17^32`, `n=512`, `k=256`, `lambda=128`
- **Related proof-ledger source:**
  `experimental/notes/high_agreement/current_row_protocol_ledger.tex`
- **Primary artifacts:**
  - `experimental/notes/certificate_scanner/examples/f17_512.json`
  - `experimental/notes/certificate_scanner/examples/f17_512_mca_only.json`
  - `experimental/notes/certificate_scanner/outputs/f17_512.report.md`
  - `experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.md`

## Purpose

This note records a small but useful scanner cross-check for protocol-ledger
work: the MCA-only scanner threshold is not the same as the full
protocol-ledger threshold once the interleaved list term is included.

It is not a new theorem. The corresponding proof-ledger statement is already
recorded in `experimental/notes/high_agreement/current_row_protocol_ledger.tex`.
This file is the machine-output crosswalk: it ties that statement to the
checked-in certificate-scanner examples so later agents do not accidentally
promote the MCA-only threshold into a stronger protocol soundness claim.

## Compared Configurations

| Example | Included terms | Intended reading |
| --- | --- | --- |
| `f17_512_mca_only.json` | MCA/proximity reserve terms without the interleaved list term | What the high-agreement MCA reserve alone clears |
| `f17_512.json` | Line term plus interleaved list term in the combined protocol ledger | What the protocol-facing ledger clears after all included terms are charged |

Both examples use the same base row:

| Quantity | Value |
| --- | ---: |
| Field size | `17^32` |
| Block length `n` | `512` |
| Dimension `k` | `256` |
| Security target `lambda` | `128` |

## Boundary Rows

The checked-in reports agree away from the boundary, but they differ exactly
where the extra protocol charge matters:

| Agreement `a` | Radius `r = n-a` | MCA-only verdict | Full protocol-ledger verdict |
| ---: | ---: | --- | --- |
| `506` | `6` | `UNSAFE_BY_PROVED_LOWER_BOUND` | `UNSAFE_BY_PROVED_LOWER_BOUND` |
| `507` | `5` | `SAFE_BY_PROVED_UPPER_BOUND` | `UNSAFE_BY_PROVED_LOWER_BOUND` |
| `508` | `4` | `SAFE_BY_PROVED_UPPER_BOUND` | `SAFE_BY_PROVED_UPPER_BOUND` |

Thus, for this concrete row, the MCA-only scanner readout first clears at
`a=507`, while the full protocol-facing ledger first clears at `a=508`.

## Interpretation

The one-column shift is exactly the kind of accounting error the protocol
ledger is meant to prevent. A proof-facing protocol claim must pay for all
terms that the reduction consumes. In this row, the MCA-only reserve is already
strong enough at radius `r=5`, but the full ledger with the interleaved list
term still has a theorem-backed lower numerator exceeding the target at that
same radius. The combined ledger only becomes safe at radius `r=4`.

This does not weaken the MCA-only high-agreement readout. It separates two
statements:

1. The MCA-only reserve clears from `a=507` onward in the current scanner.
2. The protocol ledger with the included line/list charges clears from `a=508`
   onward in the current scanner.

Keeping those statements distinct is important because Paper C-style soundness
claims should consume the second threshold, not the first.

## Reproduction

From the repository root, regenerate the two reports with:

```powershell
python experimental/notes/certificate_scanner/certificate_scanner.py experimental/notes/certificate_scanner/examples/f17_512.json --md-out experimental/notes/certificate_scanner/outputs/f17_512.report.md --json-out experimental/notes/certificate_scanner/outputs/f17_512.report.json --pretty
python experimental/notes/certificate_scanner/certificate_scanner.py experimental/notes/certificate_scanner/examples/f17_512_mca_only.json --md-out experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.md --json-out experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.json --pretty
```

Then inspect the `a=507` and `a=508` rows in the two markdown reports.

## Promotion Rule

This note should remain an audit artifact unless it is tied to a paper-level
protocol statement. If promoted, the promoted claim should cite or merge with
the high-agreement proof-ledger source, explicitly name the included ledger
terms, and use the full protocol threshold `a >= 508` for this row unless the
protocol being analyzed really omits the interleaved list term.
