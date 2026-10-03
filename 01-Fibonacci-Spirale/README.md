# Italian Fibonacci review bundle

This directory is a self-contained, prepublication export of the controlled
Luna/Sol Italian Fibonacci exercise. Start with `SPEC.md`, then inspect
`process/PROCESS.md` and `MANIFEST.json`.

- `candidates/luna/` and `candidates/sol/` contain normalized candidate trees.
- `beads/` contains fresh raw JSON exports from Aloeus.
- `transactions/` contains unchanged Aloeus transaction records, including
  dispatcher accounting, worker returns, traces, manager reviews, and verdicts
  where available.
- `verification/verify.py` runs the same public modes against both candidates.

Both implementation Beads received independent acceptance. The comparison
transaction stopped before canonical selection because its Amoyensis worker
could not access Aloeus-owned transaction records. This Aloeus bundle supplies
those records but does not conceal that procedural limitation or claim a final
canonical winner.

