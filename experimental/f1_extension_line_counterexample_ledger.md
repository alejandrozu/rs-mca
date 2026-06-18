# F1 Extension-Line Counterexample Ledger

**Status:** COUNTEREXAMPLE / AUDIT.

This ledger condenses the extension-line MCA material into a review-facing
claim: the unrestricted same-numerator lift from base-field MCA to
extension-field MCA is false as stated.  The remaining useful target is a
restricted extension theorem above the corrected reserve, or an extension
certificate that accounts for genuinely extension-valued residue-line data.

## Refuted Interface

The refuted interface is the numerator-preserving lift isolated at:

- `tex/snarks_v4.tex` `ass:extension-mca-lift`
- `tex/proximity_blueprint_v3.tex` `prob:F1`

In words:

```text
If C_B over B has MCA numerator N over q_B,
then the extension code C_F over F should have essentially the same numerator
N over q_F for all F-valued affine lines f+zg.
```

The verified counterexamples show that new bad slopes can be created by
genuinely `F`-valued line data.  They are not explained by base-rational bad
slopes deflating from `B` into `F`.

## Verified Finite Evidence

Run:

```text
python experimental/2026-06-17-codex-f1-l1-audit/verifiers/verify_f1_extension_counterexample.py
```

Observed result:

```text
F1 verifier passed
p=7: extension bad slopes = 15/49; base numerator = 7
p=17: extension bad slopes = 288/289; base numerator = 17
```

The `p=17` case is already decisive for the finite same-numerator interface:
a base numerator of `17` would predict a numerator of roughly `17` over
`F_17^2`, but the extension-valued construction produces `288` bad slopes out
of `289`.

Run also:

```text
python experimental/f1-extension-witness/verify_ext_witness.py
```

Observed result:

```text
OK canonical witness
OK F\B bad-slope recount: 51
```

This smaller fixture records a degree-1 residue-line same-set MCA witness over
`F_17^2` with `51` bad slopes outside the base field.

## Mechanism

The broad verifier uses a degree-1 extension denominator:

```text
E(X) = X - alpha, alpha in F \ B.
```

For the `p=17` instance:

```text
B = F_17
F = F_17[alpha] / (alpha^2 - 3)
H = B^*
n = 16
k = 8
agreement size = 9
f(x) = x^9 / (x - alpha)
g(x) = -1 / (x - alpha)
```

For each 9-subset `S`, the construction builds a slope
`z_S = Q_S(alpha)` and a degree-`<8` polynomial `P_S` so that
`f + z_S g` agrees with `P_S` on `S`.  The same support does not explain
`(f,g)` by degree-`<8` base-codewords, so the slope is MCA-bad.

The key point is that `E` is not in `B[X]`.  This is why the construction
evades subfield confinement, which only says that `B`-valued line data has all
bad slopes in `B`.

## Ledger Consequences

- Extension challenge fields cannot be credited in the MCA denominator by
  simply replacing `q_gen` with `q_chal`.
- A certificate using `q_line > q_gen` needs a theorem for the actual
  `F`-line family, a line-decoding replacement, or an explicit
  affine-subspace/interleaved-base formulation.
- Base-rational witness searches are provably the wrong search space for this
  problem; the search target is residue-line denominators in `F[X] \ B[X]`.
- Paper D's `cor:Fvalued` and explicit-lines problem are consistent with this:
  base-rational lines deflate, but genuinely `F`-valued bad lines can exist.

## What This Does Not Prove

- It does not refute every corrected-reserve extension-line theorem.
- It does not give a deployed-parameter explicit line at KoalaBear sextic
  scale.
- It does not replace the extension-code list identity; the failure is on the
  MCA/line side.

## Replacement Target

The natural corrected statement is not scalar base-MCA preservation.  An
`F`-line over an extension `F/B` should be treated as a structured
`B`-affine-subspace or multiplication-slice problem for the interleaved base
code.  Any future extension certificate should state which of these objects it
controls and whether degree-1 residue denominators `E in F[X] \ B[X]` are
included.
