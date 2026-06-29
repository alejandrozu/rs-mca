# L2 Common-Subset Bound Calculator

**Status:** PROVED calculator / certificate-facing audit.

This note records a small script-level addition to the existing L2 support
bridge.  The bridge note already proves that an interleaved listed codeword
injects into the simultaneous feasible-support fiber when `a >= k`.  The
calculator added here exposes the coarsest certificate consequence:

```text
|Lambda(Int(C,mu), 1-a/n, U)| <= binom(n,a).
```

The proof is the canonical common-subset injection.  A listed `mu`-row
interleaved codeword has at least `a` common agreement columns.  Choose a
canonical `a`-subset of those columns.  On that subset, each row codeword is
unique because `a >= k`, so two different interleaved codewords cannot map to
the same subset.

## Script

`experimental/scripts/verify_l2_common_subset_bound.py` emits this bound in a
JSON shape suitable for certificate experiments.  It uses exact integer
binomials for small `n` and logarithmic estimates plus entropy bounds for
large `n`.

Examples:

```bash
python experimental/scripts/verify_l2_common_subset_bound.py

python experimental/scripts/verify_l2_common_subset_bound.py \
  --n 16 --k 8 --sigma 1 --mu 2 --json

python experimental/scripts/verify_l2_common_subset_bound.py \
  --n 1048576 --rho-den 2 --sigma 1 --mu 2 --json
```

For `n=16,k=8,a=9`, the exact bound is `binom(16,9)=11440`.  For
`n=2^20,k=2^19,a=k+1`, the logarithmic estimate is about
`1,048,565.674249` bits.

## Novelty Check

This does not replace the stronger L2 bridge, codegree, or sharp-target notes.
It is a small certificate-facing wrapper around the already-current theorem:
useful when a row needs a conservative direct interleaved numerator without
reintroducing the Cartesian product `L_1(a)^mu`.

The bound is intentionally coarse.  It removes the interleaving-product factor,
but at tiny reserve it is still exponential.  Polynomial/protocol-affordable
list bounds still require the L1/local-limit or sharper L2 codegree lanes.
