# Research Roadmap and Blocker Analysis

**Status:** AUDIT.

This note classifies the advances that stand between the repository's current
state and a successful resolution of the smooth-domain Reed--Solomon MCA /
proximity-prize program.  It is a roadmap, not a theorem.  It prioritizes
work by impact, tractability, and dependency order.

## Executive Picture

There are two different meanings of "success" in this project:

1. **Theorem-backed protocol success.**  Produce a reserve-certified proximity
   layer whose list, MCA or line-decoding, field, and query ledgers are paid by
   proved theorems.
2. **Conjectural smooth-RS success.**  Keep smooth multiplicative RS domains
   near capacity, but prove the missing corrected local-limit and transfer
   statements that Paper C currently records as assumptions.

The first route may be achievable through audits, certificate tooling,
dimension hygiene, and theorem-backed alternatives.  The second route is a
deep research program.  Its core blockers are L1, M1, F1, L2, and P1.

## Difficulty Scale

| Rating | Meaning |
| --- | --- |
| Low | Mostly engineering, parsing, exact arithmetic, or citation hygiene. |
| Medium | Bounded mathematics or scripts; likely useful PR in days. |
| High | New theorem, counterexample search, or nontrivial finite classification. |
| Very high | Central research problem; may require new ideas. |
| Wild | Could reshape the program; high uncertainty and high payoff. |

## A. Source, Audit, and Proof-Status Blockers

These are not the deepest mathematics, but they control whether existing
claims can be cited safely.

| Item | Type | Impact | Difficulty | What would solve it |
| --- | --- | --- | --- | --- |
| A0 CS25/ABF import audit | Source audit | Critical for Paper D's universal cap becoming unconditional. | High but bounded | Obtain primary CS25 Theorem 2 and ABF Theorem 5.3; compare field scope, radius, `C+`, CA normalization, slope field, strictness, and constants row by row. |
| BCHKS fallback strictness | Source audit | Medium-high; affects independent slacked robustness route. | Medium-high | Derive Paper D's `thm:B` directly from BCHKS or cite ABF's exact restatement, including strict `>q` versus `>=q` list thresholds. |
| Universal-cap conditionality | Status hygiene | High; prevents overclaiming. | Low-medium | Audit every citation of Paper D so it says conditional on CS25/ABF until A0 is discharged, and never call the cap error-one. |
| Theorem-label map and cross-citations | Status hygiene | Medium; reduces review friction. | Medium | Keep `experimental/theorem_label_map.md` synchronized with actual paper labels and replace vague "companion proves" references. |
| Field-ledger audit | Status hygiene | High for protocol claims. | Medium | Grep all uses of `q`, `q_gen`, `q_line`, `q_chal`, `B`, and `F`; flag denominator substitutions without a theorem. |

**Best near-term play:** A0 is the most important audit.  If it passes, Paper D
becomes much stronger.  If it fails, the exact correction tells the team which
cap statements survive.

## B. List-Side Theorem Blockers

These decide whether smooth RS can have polynomial list size above the
corrected reserve.

| Item | Type | Impact | Difficulty | What would solve it |
| --- | --- | --- | --- | --- |
| L1 repaired arbitrary locator local limit | Core theorem | Critical for positive list certificates. | Very high | Replace raw `Fib_U` by a list-faithful object that avoids contained-support overcount, prove polynomial bounds above entropy plus quotient reserves, and preserve the list bridge. |
| L1 monomial-prefix local limit | Core theorem, narrower | High; likely first provable positive lane. | Very high | Prove finite-field aperiodic prefix fibers are polynomial after quotient-periodic components are removed and entropy margin clears. |
| Arbitrary-word repair choice | Definition repair | Critical prerequisite to L1. | High | Decide between exact-agreement supports, maximal supports, codeword-indexed canonical supports, or another object; prove it upper-bounds list size without the `U=0` overcount. |
| Characteristic-zero to finite-field transfer below norm threshold | Analytic/algebraic theorem | High | Very high | Extend Galois/norm methods or use density-over-primes theorems to control finite-field collisions in polynomial fields. |
| L3 quotient-profile constants and dithering | Finite theorem/tooling | High for real parameters. | Medium | Implement scanner over actual `(n,k,sigma)` and prove maximal-remainder/dither lemmas beyond `k=rho n-1`. |
| Entropy reserve constants | Certificate arithmetic | Medium-high | Low | Produce exact `entropy_margin.py` tables for `tau*`, `entres`, and deployed field choices. |

**Best near-term play:** L3 and entropy tooling are tractable and immediately
useful.  L1 itself is central but probably not a single-agent quick win unless
restricted to monomial-prefix toy cases.

## C. MCA, CA, and Line-Decoding Blockers

These decide whether list-side progress actually gives protocol-facing
agreement guarantees.

| Item | Type | Impact | Difficulty | What would solve it |
| --- | --- | --- | --- | --- |
| M1 corrected residue-line local limit | Core theorem | Critical for positive MCA certificates. | Very high | Bound noncontained residue-line packing by `n^{1+o(1)}` plus tangent and quotient terms above corrected reserve. |
| Low-degree residue-line classification | Finite/inverse problem | High; likely first M1 attack. | High | Classify degree-1 and degree-2 denominators after quotient-periodic components are removed; either prove packing bounds or find new floors. |
| M2 line-decoding formulation | Translation theorem | High for protocols. | Medium-high | Convert support-wise MCA/residue-line packing into explicit `(delta,a_LD,n+1)` line-decoding parameters and prove implications/separations. |
| X1 list-to-CA/MCA equivalence without square-root loss | Bridge theorem | Potentially critical; could collapse L1 and M1. | Wild | Show corrected-reserve list bounds imply CA/MCA/line-decoding at the same radius, or find smooth sparse-field counterexamples. |
| X2 attack up to MCA rather than CA | Protocol interpretation | Medium-high | High | Turn MCA-bad same-support witnesses into an actual attack strategy for a constrained-code protocol, or prove CA is the right attack object. |
| Error-one in the `2^150..2^256` band | Negative theorem/open frontier | Medium-high | Very high | Decide whether `emca(C,1-rho-1/64)=1-o(1)` for all primes in the remaining band, beyond Paper D's lower-error cap. |

**Best near-term play:** M2 is probably the most tractable high-impact
mathematical writeup.  It may expose whether the protocol really needs MCA or
can consume line-decoding.

## D. Extension-Field Blockers

These are crucial because practical systems often use extension challenges.

| Item | Type | Impact | Difficulty | What would solve it |
| --- | --- | --- | --- | --- |
| F1 unrestricted extension-line lift | Counterexample already found | Critical field-accounting warning. | Done for unrestricted form | Keep the counterexample ledger visible; do not let protocol certificates divide MCA by `q_chal` through this dead interface. |
| F1 arbitrary-anchor balanced-denominator gap | Core repaired theorem/counterexample | Critical for any extension-line positive theorem. | Very high | Decide whether arbitrary anchors `w:D->F` reduce to the `hat E` base-field readout, or exhibit richer extension slopes. |
| Extension-line scanner | Experimental/tooling | High for F1. | Medium-high | Generalize current verifiers into a scanner over `p`, extension degree, denominator degree, slack, anchors, and support size. |
| Explicit deployed `F`-valued certifying lines | Constructive witness problem | High for understanding Paper D. | High | Find explicit pairs over KoalaBear sextic with CA-bad density `>2^-22` at gap `2^-7`, or smaller analogues revealing the template. |
| F2 generated-field entropy under extensions | Ledger theorem | High but mostly already conceptually clear. | Medium | State and prove when locator entropy is governed by `B` rather than ambient `F`, and exactly what data must be extension-defined to change codimension. |

**Best near-term play:** build `extension_line_scan.py` from the existing
verifiers.  The unrestricted lift is dead; the valuable question is the
corrected-reserve/arbitrary-anchor boundary.

## E. Interleaving and Protocol-Consumed List Blockers

These determine whether mathematical bounds map to actual FRI/WHIR-like
reductions.

| Item | Type | Impact | Difficulty | What would solve it |
| --- | --- | --- | --- | --- |
| L2 sharp interleaved-list constants | Protocol theorem | Critical for concrete parameters. | High | Bound `Lambda(Int(C,mu),delta)` directly rather than paying `L_1^mu`; test whether quotient-core families multiply or share supports. |
| Direct tiny interleaved enumeration | Experimental | Medium-high | Medium | Exhaust `mu=2` toy cases and compare direct counts to product/GGR-style bounds. |
| Extension-code list identity integration | Protocol ledger | High | Medium | Ensure Paper C certificates distinguish base, interleaved, and extension-code list objects. |
| List-over-field budget | Certificate arithmetic | High | Medium | Compute `B_L/q_line` for actual consumed list arity and field, with status tags for theorem/conjecture/audit. |

**Best near-term play:** direct `mu=2` enumeration is a good bounded task.  It
could quickly show whether product overcharging is severe.

## F. Protocol, Certificate, and Arithmetization Blockers

These are the bridge from research claims to usable parameter choices.

| Item | Type | Impact | Difficulty | What would solve it |
| --- | --- | --- | --- | --- |
| P1 FRI/WHIR ledger rewrite | Protocol proof audit | Critical for real systems. | High | Rewrite one full reduction in Paper C's ledger form, naming exact list/MCA/line-decoding/curve/query/fold terms and fields. |
| P2 reserve certificate emitter | Tooling/certificate | High | Medium | Implement domain descriptor, entropy, quotient profile, list budget, MCA budget, failure ladder, field status, and proof-mode labels. |
| P3 quotient-hygienic arithmetization | Design/theorem | High for smooth-RS practicality. | High | Show dimension dithering such as `k=rho n-r` is compatible with AIR/R1CS/Plonkish degree bounds without losing efficiency. |
| Security statement modes | Documentation/protocol hygiene | Medium-high | Low-medium | Clearly separate theorem-backed, conjectural aggressive, obstruction-audit, and hybrid parameter modes. |
| Query/folding budget integration | Protocol arithmetic | Medium-high | Medium | Combine coding ledgers with query branch, folding, batching, Fiat-Shamir, Merkle, recursion, and masking terms. |

**Best near-term play:** P2 is most buildable.  P1 is more important, but needs
deep reading of a concrete protocol reduction.

## G. Domain Alternatives and Escape Routes

These matter if smooth multiplicative RS remains obstructed.

| Item | Type | Impact | Difficulty | What would solve it |
| --- | --- | --- | --- | --- |
| X3 domain shattering | Alternative-domain theorem | Wild but important | Very high | Prove random puncturing, unions of cosets, or mild shattering destroy quotient-core/MCA floors while preserving enough FFT structure. |
| Circle/Chebyshev cap transfer | Alternative-domain theorem | High for Circle-STARK-like domains. | High | Replace `X^a-b` locator fibers by Chebyshev/circle locators and redo the Paper D fiber-plus-conversion composition. |
| Mixed-radix domains | Structural theorem | Medium-high | High | Turn `{2,3}` relation modules and set decompositions into quotient-profile and MCA floor formulas. |
| Folded/subspace-design alternatives | Theorem-backed fallback | High if smooth RS positive path fails. | High | Improve concrete parameters or prove overhead lower barriers for folded RS, multiplicity, and subspace-design codes. |

**Best near-term play:** Circle/Chebyshev transfer is more concrete than broad
domain shattering and has existing locator analogues in the repo.

## H. Tooling, CI, and Formalization

These do not solve the problem alone, but they prevent regression and make
finite claims reviewable.

| Item | Type | Impact | Difficulty | What would solve it |
| --- | --- | --- | --- | --- |
| Verification runner / CI | Tooling | Medium-high | Low | Promote `experimental/run_verification_smoke.py` into CI once maintainers choose mandatory suites. |
| Paper A finite certificates | Tooling/audit | Mostly discharged | Low-medium | Keep `verify_paperA_finite.py` and JSON reports synchronized with Appendix A changes. |
| `quotient_profile.py` | Tooling/theorem support | High | Low-medium | Enumerate active divisor scales and dither effects with exact logs and JSON. |
| `extension_line_scan.py` | Tooling/counterexample search | High | Medium-high | Parameterized scanner for extension-only bad lines and arbitrary anchors. |
| `interleaved_budget.py` | Tooling/protocol support | Medium-high | Medium | Product, GGR-style, and direct enumeration comparisons. |
| Lean/Coq finite skeleton | Formalization | Medium now, high long-term | Medium-high | Formalize RS code, distance, locator identities, quotient profile predicates, and finite certificate statements. |

**Best near-term play:** quotient-profile and certificate-emitter tooling have
the best impact-to-effort ratio.

## Dependency Graph

```text
Paper A finite verification
  -> stable no-slack obstruction and failure ladders

A0 CS25 import audit
  -> Paper D cap becomes proved or precisely corrected
  -> Paper C failure-ladder status improves

L3 + entropy tooling
  -> exact reserve certificates
  -> input to L1/P2/P3

L1 repaired list theorem
  -> base/interleaved list certificates
  -> P2 can certify list side

M1 or M2 or X1
  -> MCA/line-decoding certificates
  -> P2 can certify agreement side

F1 repaired extension theorem
  -> extension challenge fields can be used safely
  -> otherwise certificates need base fields or explicit extension terms

L2 interleaved constants + P1 protocol rewrite
  -> real FRI/WHIR parameter claims

X3/X4 alternatives
  -> escape route if smooth multiplicative RS remains blocked
```

## Most Promising Near-Term Contributions

1. **Finish A0 from primary sources.**  High impact; bounded if sources are
   accessible.
2. **Implement quotient-profile scanner.**  Medium effort; immediately useful
   for every certificate and dithered dimension.
3. **Build `extension_line_scan.py`.**  Turns the F1 counterexample into a
   systematic search and may settle the arbitrary-anchor boundary in small
   cases.
4. **Draft M2 line-decoding formulation.**  Could unlock protocol use even if
   support-wise MCA remains awkward.
5. **Direct `mu=2` interleaved-list enumeration.**  Bounded experiment with
   high protocol relevance.
6. **Reserve certificate emitter.**  Converts the theory into the actual
   deliverable Paper C wants.
7. **Circle/Chebyshev Paper D transfer note.**  Concrete alternative-domain
   lane with clear mathematical object.

## Hardest Central Problems

- **L1 repaired arbitrary locator local limit.**  This is the main list-side
  theorem and the raw object is already known to be wrong.
- **M1 residue-line local limit.**  This is the main MCA-side theorem.
- **F1 arbitrary-anchor extension theorem.**  This is the key extension-field
  repair after the same-numerator lift failed.
- **X1 list-to-agreement equivalence without square-root loss.**  If true, it
  could simplify the whole positive theory; if false, it explains why L1 and
  M1 must remain separate.
- **P1 full protocol rewrite.**  Without this, even correct coding theorems do
  not become a drop-in SNARK security statement.

## Recommended Work Order

For maximal practical progress:

1. A0 import audit.
2. Quotient-profile and entropy tooling.
3. P2 reserve certificate schema/emitter.
4. F1 scanner and arbitrary-anchor experiments.
5. L2 tiny interleaved-list enumeration.
6. M2 line-decoding formulation.
7. L1/M1 theorem attacks using data from the scanners.
8. P1 WHIR or FRI ledger rewrite.
9. X3/X4 alternatives if smooth RS remains blocked.

This order balances quick PRs, theorem risk, and protocol usefulness.  It also
keeps the central rule intact: do not spend extension-field denominators,
interleaved-list savings, or MCA/list conversions before the exact theorem that
earns them is in hand.
