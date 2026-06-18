# Agents Log

This file is the working ledger for agent-created material in `experimental/`.
Use it to record every new note, script, scan, formalization stub, or audit before
the material is promoted into `tex/` or `scripts/`.

The log is not a proof-status authority. It is a coordination record: what was
added, why it might matter, and what a human or later agent should check next.
Keep entries concise and link to the relevant files.

## Entry Format

```markdown
### YYYY-MM-DD - Short title

- **Agent/model:** Name the agent or model, for example `GPT-5.5 Pro`,
  `Claude Fable 5`, or `Codex`.
- **Files added or changed:** List paths under `experimental/`, `tex/`,
  or `scripts/`.
- **Status:** PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT /
  COUNTEREXAMPLE.
- **What is being added:** State the claim, note, scan, script, or certificate
  in one or two sentences.
- **How it is useful:** Say which paper, theorem, problem, ledger, or toy case
  the material supports.
- **What to do next:** Give the next verification, cleanup, proof step,
  experiment, or promotion decision.
```

## Entries

### 2026-06-18 - Research roadmap blocker analysis

- **Agent/model:** Codex.
- **Files added or changed:** Added
  `experimental/research_roadmap_blocker_analysis.md`.
- **Status:** AUDIT.
- **What is being added:** A consolidated classification of the remaining
  mathematical, audit, tooling, protocol, extension-field, and alternative
  domain blockers standing between the current repository state and a
  successful resolution.
- **How it is useful:** Converts the distributed backlog into a dependency
  roadmap with difficulty, impact, solution paths, and recommended work order.
- **What to do next:** Use it to assign agents to bounded PRs first
  (`A0`, quotient-profile tooling, extension-line scanner, certificate emitter)
  while keeping `L1`, `M1`, and repaired `F1` as the major theorem lanes.

### 2026-06-18 - Verification smoke runner

- **Agent/model:** Codex.
- **Files added or changed:** Added
  `experimental/run_verification_smoke.py`.
- **Status:** PROVED for the local smoke suite when run on this checkout.
- **What is being added:** A standard-library runner with `smoke`, `paperA`,
  and `all` suites, text/JSON output, and per-check timeout handling.
- **How it is useful:** Gives reviewers and future CI one bounded entry point
  for the repository's finite verifiers without requiring a test framework or
  GitHub Actions wiring in this PR.
- **What to do next:** Promote the runner into CI once maintainers decide
  which suites should be mandatory on every pull request.

### 2026-06-18 - F1 extension-line counterexample ledger

- **Agent/model:** Codex.
- **Files added or changed:** Added
  `experimental/f1_extension_line_counterexample_ledger.md`.
- **Status:** COUNTEREXAMPLE / AUDIT.
- **What is being added:** A compact ledger for the verified extension-line
  MCA counterexamples, linking the finite verifier outputs to Paper C's
  `ass:extension-mca-lift` and the blueprint F1 problem.
- **How it is useful:** Makes the protocol consequence explicit: extension
  challenge fields cannot be credited in the MCA denominator without a theorem
  for genuinely extension-valued line data or a replacement line-decoding /
  interleaved-base formulation.
- **What to do next:** Search residue-line denominators in `F[X] \ B[X]` at
  corrected-reserve radii; do not spend cycles on `B`-rational lines, which are
  already covered by subfield confinement.

### 2026-06-18 - A0 CS25 import interface crosswalk

- **Agent/model:** Codex.
- **Files added or changed:** Added
  `experimental/a0_cs25_interface_crosswalk.md`.
- **Status:** AUDIT.
- **What is being added:** A compact interface matrix comparing Paper D's local
  Crites--Stewart import with the public theorem-shaped CS25 summary available
  during audit, separating constant algebra already discharged from source
  checks that remain open.
- **How it is useful:** Turns the broad A0 warning into reviewable action
  items: field generality, slope-field sampling, radius rounding, normalization,
  and strictness.
- **What to do next:** Fetch the primary CS25 theorem and ABF26 restatement,
  then mark each interface row as matched, narrowed, or corrected.

### 2026-06-18 - Paper A finite-verification bundle

- **Agent/model:** Codex.
- **Files added or changed:** Added `experimental/verify_paperA_finite.py`
  and `experimental/verify_paperA_finite.report.json`.
- **Status:** PROVED for the finite computations rerun by the bundle; AUDIT for
  their role as support material for Paper A.
- **What is being added:** A single-command wrapper that runs the existing
  Paper A finite-verification scripts covering Appendix A V1-V5, deployed-field
  DSH arithmetic, and extension-density arithmetic, then emits one JSON report.
- **How it is useful:** Completes the integration gap identified by
  `experimental/a1_paperA_finite_verification_crosswalk.md`: reviewers can now
  reproduce the finite audit with one command instead of a hand-copied command
  list.
- **What to do next:** Keep this wrapper in `experimental/` until maintainers
  decide whether Paper A finite certificates should be promoted into a stable
  script or CI workflow.

### 2026-06-18 - Paper A finite-verification crosswalk

- **Agent/model:** Codex.
- **Files added or changed:** Added
  `experimental/a1_paperA_finite_verification_crosswalk.md`.
- **Status:** AUDIT / PROVED for the finite computations cited in the
  crosswalk.
- **What is being added:** A review map from Paper A Appendix A finite claims
  V1-V5 to the repository scripts that reproduce them, with notes on the
  Claude Opus 4.8 export package and its missing/stale verifier handles.
- **How it is useful:** Supports A1 by making the finite verification route
  explicit, avoiding the `Q=<2>` versus full-group confusion in V1, and keeping
  Paper B verifier material out of the Paper A audit lane until separately
  reviewed.
- **What to do next:** If the Claude standalone verifier scripts are recovered,
  review them as optional convenience wrappers against this crosswalk before
  adding them to `experimental/`.

### 2026-06-17 - Open PR triage integration

- **Agent/model:** Codex.
- **Files added or changed:** Integrated experimental material from PRs #1,
  #2, #3, and #46 through #66; added
  `experimental/pr-triage-2026-06-17.md`; renamed PR #55's dither scanner to
  `experimental/quotient_profile_dither.py` with matching `.md` note.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** One-by-one triage of the open PR queue and local
  integration of accepted experimental notes, scanners, certificates, and
  audit bundles.
- **How it is useful:** Preserves useful agent contributions while enforcing
  the repository rule that new material starts in `experimental/` and Papers
  A-D remain unchanged.
- **What to do next:** Run verifiers and audits on the integrated material,
  review mathematical notes before promotion, and close the original PRs as
  manually integrated once the integration commit is pushed.
