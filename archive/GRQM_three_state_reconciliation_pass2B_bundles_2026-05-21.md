# GRQM Three-State Reconciliation — Pass 2B Bundle Families (2026-05-21)

## Scope
This pass classifies three heavy families at bundle level rather than individual-file level:
- notebook families
- output bundles
- archive note families

States:
- **L** = local `repos/GRQM` working tree
- **G** = public `origin/main`
- **M** = `Molt\workspace\Physics`
- **T** = proposed target canonical placement

## Mechanical bundle findings
- Current L notebook top-level is effectively collapsed to `notebooks/outputs/` only.
- L root `outputs/` contains at least two newer bundles:
  - `shoulder_causality_20260323T215813Z`
  - `shoulder_causality_20260323T222400Z`
- Earlier pass also identified a newer live root bundle:
  - `bohmian_adaptation_20260319_191614`
- G↔L diff concentration shows most reduction pressure landed on notebook-run families and archive notes, not just root docs.
- `archive/session-notes/2026-03/` still contains **39** files in L, so archive was reduced but not removed.

## Notebook family classification

| Family | L | G | M | Reading | Proposed T |
|---|---|---|---|---|---|
| `grqm_*` batch / cycle notebooks | mostly absent as runnable notebooks in L | heavily present | heavily present | large historical execution layer from richer repo state | **Do not restore wholesale; keep only if needed to regenerate canonical evidence bundles** |
| `edge*` notebooks | absent as live notebooks in L | present | present | exploratory diagnostics / mitigation lane | **Archive or retain only one canonical reproducer path** |
| `wdw_*` notebooks | absent in L | present | present | identity-sensitive, tied to whether WDW remains canonical | **Archive unless WDW remains active scientific identity** |
| `boo*` notebooks | absent in L | present | present | branch/eval lane from older exploratory phase | **Archive** |
| `a001` / `a002` notebooks | absent in L | present | present | dated minitest / ablation families | **Archive, not canonical active surface** |
| `cgrqm002*` notebooks | absent in L | present | present | specific cycle/protocol family | **Archive** |
| `lqc*` notebooks | absent in L | present | present | identity-sensitive exploratory lane | **Archive unless explicitly retained in canonical scientific scope** |
| `sn*` notebooks | absent in L as notebook lane | implicit older repo lane | present | may correspond to Schrödinger-Newton toy work now represented elsewhere | **Prefer code/docs representation over notebook restoration** |
| `notebooks/outputs/` as residual artifact container | present | present | present | indicates notebook-era provenance still exists even after notebook reduction | **Retain only selected provenance bundles or migrate chosen bundles to clearer archive/output conventions** |

## Output bundle classification

### Newer L-root canonical-looking bundles
| Bundle | L | G | M | Reading | Proposed T |
|---|---|---|---|---|---|
| `outputs/bohmian_adaptation_20260319_191614/` | present | appears as newer local addition beyond old public shape | likely present or derivable in M lineage | strong candidate canonical evidence bundle for current Bohmian lane | **Keep in T** |
| `outputs/shoulder_causality_20260323T215813Z/` | present | newer local addition | likely present or derivable in M lineage | strong candidate canonical evidence bundle | **Keep in T** |
| `outputs/shoulder_causality_20260323T222400Z/` | present | newer local addition | likely present or derivable in M lineage | strong candidate canonical evidence bundle / rerun | **Keep in T, maybe collapse if redundant with prior bundle** |

### Older notebook-era output families from G/M
| Family | L | G | M | Reading | Proposed T |
|---|---|---|---|---|---|
| `grqm_batch_*` | absent from live root outputs | present under `notebooks/outputs/` | present | broad early parameter sweeps | **Archive, not canonical public output surface** |
| `grqm_batch_tiered_*` | absent from live root outputs | present | present | historical batch runs | **Archive** |
| `grqm_q2_*` debug/outlier bundles | absent | present | present | diagnostic/autopsy bundles, useful provenance but not public-first | **Archive** |
| `grqm_delta_autopsy_*` | absent | present | present | autopsy/debug family | **Archive** |
| `grqm_cycle*` output bundles | absent | present | present | cycle-specific historical outputs | **Archive unless directly cited by current claims** |
| `golden_run_20260302` | absent | present | present | looks like a benchmark/reference bundle | **Maybe retain in archive as benchmark anchor** |
| `grqm_a001*` / `grqm_a002*` bundles | absent | present | present | dated closure / ablation / nuisance-sweep outputs | **Archive** |
| `grqm_boo*` bundles | absent | present | present | branch/eval outputs from older lane | **Archive** |
| `grqm_edge*` bundles | absent | present | present | edge diagnostics and mitigation bundles | **Archive, unless needed as canonical failure-boundary evidence** |
| `grqm_lqc*` / `grqm_nonlinear*` bundles | absent | present | present | exploratory side lanes | **Archive unless restored by identity decision** |

## Archive note family classification

| Family | Approx. count in G↔L diff | Reading | Proposed T |
|---|---:|---|---|
| `EDGE` | 6 | mitigation / boundary / package notes for edge lane | **Archive** |
| `CGRQM002` | 3 | specific protocol/cycle package notes | **Archive** |
| `LEDGER` | 2 | governance mitigation ledger notes | **Archive** |
| `NONLINEAR` | 2 | exploratory side-lane notes | **Archive** |
| `LQC` | 2 | exploratory side-lane notes | **Archive unless identity restores LQC relevance** |
| `NEXT` | 2 | process / continuation planning | **Archive** |
| `KPI` | 2 | governance snapshot notes | **Archive** |
| `PROMOTION` | 2 | governance process notes | **Archive** |
| `SN` | 2 | Schrödinger-Newton-related note family | **Archive, maybe cross-link from canonical docs if still scientifically relevant** |
| `BOO` | 2 | branch/eval notes | **Archive** |
| singleton families (`ASTROPY`, `CLIFF`, `CWDW001`, `SYMBOLIC`, `PROCESS`, `SESSION`, `QUICK`, `CRITIQUE`, `EXTERNAL`, `HARDENING`, `A001`, `A002`, `CYCLE`, `CONTINUATION`) | 1 each | provenance-bearing historical notes | **Archive** |
| `README` | 1 | archive orientation surface | **Keep as archive orientation surface** |

## Pass 2B reading
The local reduction appears to have done three things at once:
1. removed most runnable historical notebooks
2. retained a reduced archive note layer
3. promoted a newer root `outputs/` surface for later Bohmian / shoulder-causality evidence bundles

That implies a real scientific/posture shift:
- away from a sprawling notebook-first exploratory workspace
- toward a narrower canonical repo with selected evidence bundles and supporting code/docs

## Provisional target-bundle stance
### Keep as likely canonical in T
- `src/`
- `tests/`
- root/docs orientation surfaces from Pass 2A
- `outputs/bohmian_adaptation_20260319_191614/`
- `outputs/shoulder_causality_20260323T215813Z/`
- `outputs/shoulder_causality_20260323T222400Z/` (pending redundancy check)
- `archive/session-notes/README.md`

### Keep archived in T
- most `archive/session-notes/2026-03/*`
- most `notebooks/outputs/*` historical bundles
- most historical notebook families if preserved at all

### Probably exclude from T public canonical surface
- broad notebook-era sweep clutter
- duplicate/debug/autopsy bundles unless directly claim-relevant
- exploratory side-lane bundles not part of active scientific identity

## Main unresolved questions before concrete cleanup
1. Is `bohmian_adaptation_20260319_191614` the primary canonical evidence anchor, with shoulder-causality as follow-on?
2. Are both shoulder-causality bundles needed, or is one a superseding rerun?
3. Should any notebook family survive as runnable exemplars, or should T be code-first plus archived receipts?
4. Which archive note families deserve cross-links from curated docs because they still support active claims?

## Recommended next move
Convert these bundle-level calls into a concrete cleanup sequence:
1. define canonical root/docs set
2. restore minimal reproducibility files
3. decide canonical output bundles
4. move surviving governance/scientific status docs into curated `docs/`
5. demote the rest to archive or leave them only in cold archive M
