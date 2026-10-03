# Process record

The frozen specification and plan were committed at `2f1f63d`. STARCHART
created sibling implementation Beads `LLM-ksk.1` (Luna) and `LLM-ksk.2` (Sol),
followed by comparison Bead `LLM-ksk.3`.

Luna ran in transaction `factory-c30ea6bef562601f1d92a456aa4aede3`.
Sol ran in transaction `factory-8a2929aec03d3072fa2ec88957bd58e5`.
Both returns were collected, reviewed, accepted, and materialized.

The comparison worker ran in transaction
`factory-3015c1a86f9da8ab5ce78887aa8bb5cb`. Its deterministic checks passed both
candidates, but it correctly returned BLOCKED because raw transaction records,
accounting, Quality authority, and manager acceptance live on Aloeus rather
than in its Amoyensis workspace.

This bundle was therefore collated on Aloeus. Candidate contents are copied
into symmetric paths, while transaction directories are copied unchanged.
The Sol worker could see the already-materialized Luna directory by name, so
the comparison demonstrates procedural non-inspection rather than strong
filesystem blindness. No canonical winner is claimed here.

Measured worker accounting is available in each transaction's `state.json`
and `worker-evidence/metrics.json`. Monetary conversion is intentionally absent.

