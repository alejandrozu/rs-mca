# A0 CS25 Import Interface Crosswalk

**Status:** AUDIT.

This note sharpens the existing A0 import audit by separating the part of
`tex/cs25_cap_v4.tex` that is locally checked from the part that still depends
on the exact Crites--Stewart / ABF theorem interface.

It should not be read as a source certification.  The official CS25 ePrint
entry is `https://eprint.iacr.org/2025/2046`, but the exact theorem text was
not available during this audit pass.  The only accessible theorem-shaped
statement was a public, non-authoritative CS25 summary; it is useful for
interface triage, not for upgrading the import to `PROVED`.

## Local Import

Paper D imports the conversion as:

```text
C = RS[F,D,k], C+ = RS[F,D,k+1],
delta in (0,dmin(C)), eta in [0,1).

If eca(C,delta) <= eta * (1/k - n/(k|F|)),
then Lst(C+,delta) <= ceil(|F| * eca(C,delta) / (1 - eta)).
```

This is the exact interface used by the universal cap in
`tex/cs25_cap_v4.tex`.

## Public Summary Interface

The accessible CS25 summary states the conversion in the following shape:

```text
For RS(Z_q,D,k), if correlated agreement over lines holds at f errors with
f < n-k-1 and error epsilon < (q-n)/(kq), then RS(Z_q,D,k+1) is
(f/n,L)-list decodable with

L = ceil(epsilon * q * (q-n) / (q-n-k*epsilon*q)).

If epsilon < (q-n)/(2kq), then L <= 2*epsilon*q.
```

This matches the local constant manipulation, but it does not by itself certify
the broader field, radius, or normalization interface used in Paper D.

## Interface Matrix

| Interface item | Paper D needs | Public summary shows | Audit status |
| --- | --- | --- | --- |
| Code rung | `C+=RS[F,D,k+1]` | `RS(Z_q,D,k+1)` | Compatible in shape; field generality still open. |
| Field scope | arbitrary finite `F`, including extensions `B subset F` | `Z_q` notation | Needs primary CS25 or ABF text. |
| Slope field | `gamma` uniform in the same ambient `F` used by the RS code | "over lines" in `Z_q` | Needs source confirmation for extension-field sampling. |
| Radius | real `delta in (0,dmin(C))` | integer `f < n-k-1`, radius `f/n` | High-risk mismatch; needs rounding or theorem narrowing. |
| Error normalization | `eca` is a probability over slopes | error parameter `epsilon` | Algebraically compatible; definition still needs source match. |
| List bound | relaxed `ceil(q epsilon/(1-eta))` | rational `ceil(epsilon q(q-n)/(q-n-k epsilon q))` | Derived correctly if `epsilon <= eta(q-n)/(kq)`. |
| `eta=1/2` constant | gives `Lst(C+,delta) <= ceil(2q eca)` | summary gives `L <= 2 epsilon q` | Matches. |
| Strictness | local hypothesis uses `<=`; theorem summary uses `<` | possible endpoint mismatch | Harmless for open thresholds, but should be stated precisely. |

## What Is Locally Discharged

Assume the source theorem has the rational form over the same line field `F`:

```text
epsilon < (q-n)/(kq)
implies
Lst(C+,delta) <= ceil(epsilon*q*(q-n)/(q-n-k*epsilon*q)).
```

Then the local relaxed import follows: if

```text
epsilon <= eta * (q-n)/(kq)
```

with `eta in [0,1)`, then

```text
q-n-k*epsilon*q >= (1-eta)(q-n)
```

and therefore

```text
Lst(C+,delta) <= ceil(q*epsilon/(1-eta)).
```

For `eta=1/2`, a list lower bound

```text
Lst(C+,delta) >= q/k + 1
```

forces

```text
eca(C,delta) > (1/(2k)) * (1 - n/q).
```

The constant algebra is therefore not the remaining blocker.

## Remaining Blockers

1. **Field generality.**  Paper D's strongest claims use extension fields:
   `D subset B^* subset F^*`, codewords over `F`, and slopes sampled from
   `F`.  If CS25/ABF is only stated over prime fields, the deployed sextic and
   "every field below 2^256" corollaries are not source-certified.

2. **Radius range.**  Paper D states the imported theorem for
   `delta in (0,dmin(C))`, while the public summary advertises an integer
   condition `f < n-k-1`.  If that is the real source condition, Paper D should
   either add a rounding lemma or narrow the direct `eca(C,delta)` claim to
   source-admissible radii.

3. **Normalization.**  The source must use the same probability-normalized CA
   error over the line field.  A count-normalized or differently sampled
   theorem would change the constants.

4. **Endpoint strictness.**  The local theorem uses `<=` in the small-error
   hypothesis.  If the source uses only strict `<`, the final statements should
   avoid relying on equality at the threshold.

5. **BCHKS fallback separation.**  The fallback theorem in Paper D is a
   two-radius/slacked CA route.  It should remain a separate robustness check,
   not a substitute for the no-loss CS25 import.

## Recommended Manuscript Edits

- Put "conditional on the CS25/ABF import" in the abstract theorem prose, not
  only in the late verification caveat.
- Add a one-sentence field ledger next to `thm:A`: `q=|F|` is the line-slope
  field, while `B` is only the field of definition for locator coefficients.
- If the source theorem is integer-radius, replace the direct interval
  `delta in [1-rho-2/N, dmin(C))` by the verified source-admissible interval,
  and use monotonicity only where it is explicitly proved.
- Keep `experimental/a0_cs25_rational_constant_derivation.md` as the constant
  check; use this file as the source-interface checklist.

## Verdict

The local cap composition is coherent conditional on the imported theorem, and
the `eta=1/2` constants are correct.  The import does **not** yet match exactly
from the evidence available here: field generality, radius convention,
normalization, and endpoint strictness remain source checks.
