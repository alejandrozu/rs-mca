# CAP25 v13 Q-fin BCH-syndrome reduction

Status: AUDIT / REDUCTION / ROUTE_CUT.

Data:
`experimental/data/certificates/frontier-adjacent/kb_mca_qfin_bch_syndrome_reduction_v1.json`.
Verifier:
`experimental/scripts/verify_cap25_v13_qfin_bch_syndrome_reduction.py`.

This note records a sharper formulation of the live KoalaBear MCA Q-fin wall

```text
CAP25-V13-QFIN-PRIMITIVE-MAX-ORBIT-FLATNESS-KB-MCA-1116048.
```

It does not prove `conj:Q`, does not prove `U(1116048) <= B*`, and does not
move the frontier edge.  Its purpose is to isolate the exact algebraic object
left after the rung audit and to rule out several tempting soft routes whose
constants cannot possibly fit the deployed row.

## 1. Deployed constants

For the live KoalaBear MCA safe candidate,

```text
p = 2^31 - 2^24 + 1 = 2130706433,
n = 2^21,
k = 2^20,
m = 1116048,
w = 67471,
B* = floor(p^6 / 2^128).
```

The existing rung audit charges the nonprimitive divisor-lattice part
conservatively:

```text
K_raw = 4807520,
nonprimitive charge = 35624,
K_rem = 4771896.
```

Thus the primitive residual must satisfy

```text
max primitive fiber <= K_rem * binom(n,m) / p^w.
```

The bit budget is about `log2(K_rem) = 22.1861` after the nonprimitive charge.

## 2. BCH/GRS syndrome formulation

Write an `m`-subset `M subset D` as its indicator vector `1_M in {0,1}^n`.
For `D = alpha * mu_n`, the power-prefix map is

```text
Phi_w(M) = (sum_{x in M} x^i)_{1 <= i <= w}.
```

Equivalently,

```text
Phi_w(M) = H 1_M,
H_{i,x} = x^i,  1 <= i <= w.
```

Since `w < n < p` and the points of `D` are distinct, every `w` columns of
`H` form a nonsingular Vandermonde matrix.  The ambient linear code cut out by
`H` is therefore a generalized Reed-Solomon/BCH code with parameters
`[n,n-w,w+1]` over `F_p`.

The Q-fin problem is not the ordinary `p`-ary coset weight distribution of this
MDS code.  It is the much sharper binary constant-weight slice:

```text
{ v in {0,1}^n : |v| = m, H v = z }.
```

After the quotient-rung audit, the remaining targets are the primitive
syndromes, meaning

```text
gcd(n, { i : z_i != 0 }) = 1.
```

This is the exact object that a proof or counterpacket must address.

## 3. Collision rigidity

If two distinct supports in the same fiber have locators `Lambda_M` and
`Lambda_M'`, equality of the first `w` prefixes gives

```text
deg(Lambda_M - Lambda_M') <= m - w - 1 = k.
```

Writing the exchange size as `e = |M \ M'| = |M' \ M|`, this forces

```text
e >= w + 1 = 67472.
```

Equivalently, every one-fiber support family has pairwise intersections at most

```text
m - (w+1) = k = 1048576.
```

This is a useful rigidity fact, but by itself it is nowhere near the deployed
finite bound.

## 4. Soft routes that fail quantitatively

The verifier recomputes the following route cuts.

### Johnson packing from the minimum distance

Using only the exchange lower bound `e >= w+1`, the Johnson packing/sphere
argument gives a max-fiber ratio bound worse than the average by about

```text
1660773.98 bits.
```

The row needs about

```text
22.19 bits.
```

So minimum-distance packing misses by about `1.66e6` bits.

### Singleton/MDS-support relaxation

A generous "fix `w` coordinates" or support-level MDS relaxation gives a ratio
bound worse than average by about

```text
2028016.17 bits.
```

This is even farther from the deployed row than Johnson packing.  The MDS
syndrome formulation is the right language, but the raw q-ary or support-only
relaxations are not the theorem.

### Fixed or low moments

A moment conversion of the schematic form

```text
max fiber <= avg * p^(w/r)
```

would need

```text
r >= 94241
```

even for the already charged primitive budget `K_rem`.  Therefore exact
`r = 2,3,4` ledgers are useful calibration and falsification tools, but cannot
close this finite adjacent row by themselves.

## 5. What remains valid

The remaining closing routes are now narrower.

1. Prove primitive binary BCH-syndrome max-fiber flatness directly.
2. Prove exchange-compression: any heavy primitive fiber must compress into a
   paid quotient, planted, tangent, extension, or residual branch.
3. Prove a high-moment or tail hierarchy with `r` comparable to `w` and with
   explicit constants.
4. Produce a primitive syndrome whose binary weight-`m` fiber exceeds
   `K_rem` times the average, thereby refuting the adjacent safe conjecture.

This is the practical meaning of the Q-fin wall after the current v13 rung
audit: the problem is not a generic constant-weight code packing question and
not an ordinary MDS coset weight-distribution question.  It is a primitive
binary constant-weight BCH syndrome extremality problem at extremely dense
mean fiber size.
