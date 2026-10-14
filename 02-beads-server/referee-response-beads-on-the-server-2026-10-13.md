# Referee response: Beads on the Server

Date: 2026-10-13

The referee report is preserved verbatim at
`FromClaude/referee-report-beads-on-the-server-2026-10-13.md`. This response
uses the referee's C1–C19 and M1–M6 identifiers; the chapter's coverage IDs
are a separate numbering scheme.

| Referee ID | Existing coverage ID or revision block | Disposition |
| --- | --- | --- |
| C1 | C10 | Retained; Radicle disclosure remains qualified. |
| C2 | C14 | Retained; TLS security limits remain explicit. |
| C3 | C14 | Corrected to adoption of RFC 9954's definition. |
| C4 | C15 | Corrected with draft-header versus tracker dates. |
| C5 | C13 | Retained as attributed, selective reading. |
| C6 | C4 | Retained; Beads embedded/server boundary linked. |
| C7 | C11 | Corrected with `dolt.md`/implementation port qualification. |
| C8 | C2/C8 | Retained; Dolt data refs and federation are distinct. |
| C9 | C5 | Retained; selected CAS is not whole-state conformance. |
| C10 | C5 | Added R16-c and skipped-hook caveat. |
| C11 | C5/C7 | Retained; projected read revision is not a BDP write. |
| C12 | C7 | Qualified with claim eligibility and self-certification limits. |
| C13 | C6/C9 | Retained; carried attribution is not attestation. |
| C14 | C6/C7 | Dated PR snapshot retained as historical evidence. |
| C15 | C9 | Retained; merged narrower provenance envelope. |
| C16 | C9 | Retained; Beads #7510 remains a proposal. |
| C17 | C11 | Corrected; unsupported shared-server default removed. |
| C18 | HTTP comparison block (new) | Corrected; #7513 merged and #7518 open. |
| C19 | BDP naming block (new) | Corrected; “Bead Protocol” plus PR #61 proposal. |

The two “new” blocks have no pre-existing chapter coverage ID; they are the
bounded additions required by this revision and are covered in the revised
coverage record and hash receipt.

## Disposition

Accepted changes:

- M1/M2: add a native Beads HTTP comparison and a provisional recommendation.
- M4: join selected `row_lock` CAS, label/parent guard scope, R16-c, and the
  BDP adapter's projected read revision without inventing an adapter motive.
- M5: add reported SQL latency and adapter-cap evidence with explicit limits.
- C3/C4/C7/C12/C17/C18/C19: apply the RFC 9954, ML-KEM date, port/source,
  Read-evidence, PR-status, and protocol-name corrections.
- M6: retain the companion files locally and check artifact-relative links.
  Public URL availability remains a later publication check.

Qualified changes:

- C1/C2/C5/C6/C8/C9/C10/C11/C13/C14/C15/C16: retain the source-grounded
  claims and their classifications, while preserving the referee's limits on
  fetched pages, dated status, and selective reading.
- C12: Read evidence is reported as `claimEligible: false` by construction,
  with 11 self-certified case definitions and two BDP-authored targets.
- C18: #7513 is a merged 2026-10-12 update; #7518 remains open and its
  workaround is running `bd` beside the database over SSH, with same-region
  hosting as an alternative.
- M5: 10.2–10.8 seconds versus 0.17 seconds are SQL server-mode measurements;
  HTTP latency is unmeasured. The 4,000,000-byte limit is a byte cap, not a
  measured failure at a record count.

Declined or not adopted:

- M3's recommendation to remove TLS, Noise, Radicle, and governance material
  is declined because the governing revision spec requires security research
  to remain. The sections are retained as shortened protocol context and say
  explicitly that they create no immediate BDP requirement.
- The report's suggested verdict is not adopted verbatim. The chapter's
  independent recommendation is that BDP is not yet justified as a Beads HTTP
  replacement, with a revisit gate for independent Read+Update, whole-resource
  conditional revisions, measured HTTP behavior, and demonstrated client need.
- No runtime experiment is claimed for the port clash, adapter size, Beads
  HTTP behavior, or upstream tests.

## Evidence and remaining action

The revised chapter and coverage record link the pinned source studies, the
dated PR pages, and the report's correction points. `chapter-verification.md`
records the focused checks and limits. The original report remains byte
preserved. Final packaging should include this response, the report, chapter,
coverage, verification, and the hash receipt; no upstream publication is
authorized by this response.
