# Quarantined Lanes

This directory holds code paths intentionally removed from the live canonical execution surface.

## `runner_phase2.py`
- Former location: `src/grqm/bohmian_probe/runner_phase2.py`
- Quarantined on: 2026-05-21
- Reason: imports `grqm.core`, which is not present in the reduced public repository
- Policy: do not recreate missing modules with compatibility shims just to keep an old interface nominally alive

## Restoration rule
A quarantined lane should return to the live source tree only when:
1. its dependency surface is restored intentionally,
2. its execution path matches the current canonical scientific identity of GRQM,
3. tests/docs are updated alongside the restoration.
