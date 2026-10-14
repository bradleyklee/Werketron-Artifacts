# TLS migration and standards governance

Source check: 2026-10-12. This supplement supports the TLS/Noise comparison
in [Beads on the Server](Beads-on-the-Server.md). It records criticism,
standards facts, and architectural implications as separate evidence classes.

## Collection and reading boundary

The requested [Bernstein blog index](https://blog.cr.yp.to/index.html)
listed nine entries in the NSA and IETF series. The index and all nine
articles were retrieved directly with HTTP 200. The
[acquisition manifest](source-reports/bernstein-series-acquisition.json)
records URLs, times, sizes, headings, and HTML/text hashes. Original snapshots
are isolated research inputs; they are not republished in the review archive.
Reading focused on the technical and governance arguments. Every quoted
mailing-list message, historical allegation, and claimed count has not been
independently audited.

| Entry | Contribution to this research |
| --- | --- |
| [Part 1, 2025-10-04](https://blog.cr.yp.to/20251004-weakened.html) | Argues that retaining classical ECC alongside PQ key agreement hedges against failures, and questions standardization incentives. |
| [Part 2, 2025-11-23](https://blog.cr.yp.to/20251123-corruption.html) | Alleges improper influence on the standalone-PQ process; classify this as the author's claim. |
| [Part 3, 2025-11-23](https://blog.cr.yp.to/20251123-dodging.html) | Challenges responses to technical and procedural objections. |
| [Part 4, 2025-11-23](https://blog.cr.yp.to/20251123-scope.html) | Alleges suppressed dissent and disputes charter scope. |
| [Part 5, 2026-02-19](https://blog.cr.yp.to/20260219-obaa.html) | Criticizes repeated last calls and the burden on dissenters. |
| [Part 6, 2026-02-21](https://blog.cr.yp.to/20260221-structure.html) | Organizes claims, responses, and counterarguments as an argument graph. |
| [Part 7, 2026-04-05](https://blog.cr.yp.to/20260405-votes.html) | Gives the author's position counts and challenges the chairs' characterization. |
| [Part 8, 2026-07-06](https://blog.cr.yp.to/20260706-fairness.html) | Connects algorithm risk with participation costs and asymmetric decision rules. |
| [Part 9, 2026-08-14](https://blog.cr.yp.to/20260814-update.html) | Reports subsequent opposition and escalation, giving a dated procedural update. |

The series supplies a warning about standards governance and removal of a
cryptographic hedge. It does not establish that ML-KEM has been broken, that
TLS deployments are generally compromised, or that Noise avoids comparable
algorithm and implementation risks.

## Bounded standards web check

On 2026-10-12, the worker used the separate web-reading capability for a
bounded read of the following primary pages; no shell networking or clone was
used:

| Page | Observed result |
| --- | --- |
| [RFC 10024 §3](https://www.rfc-editor.org/rfc/rfc10024.html#section-3) and [§6](https://www.rfc-editor.org/rfc/rfc10024.html#section-6) | Web open returned page content. The RFC identifies itself as Standards Track, defines the hybrid security hedge, and qualifies the TLS-transcript, side-channel, and RNG assumptions. |
| [draft-ietf-tls-mlkem-11](https://www.ietf.org/archive/id/draft-ietf-tls-mlkem-11.html) | Web open returned page content. The page is dated 2026-09-17, states Intended Status: Informational, and contains the standalone security and IANA sections. |
| [ML-KEM draft tracker](https://datatracker.ietf.org/doc/draft-ietf-tls-mlkem/) | Web open returned page content on the 2026-10-12 check. It reports Submitted to IESG for Publication, IESG state RFC Ed Queue, RFC Editor status Awaiting First editor, and IANA state RFC-Ed-Ack. |
| [RFC 7282](https://www.rfc-editor.org/rfc/rfc7282.html) | Web open returned page content. The introduction and consensus sections describe technical consideration of objections and distinguish rough consensus from voting. |

The web operation confirms the dated status used by this supplement; it does
not refresh the nine Bernstein article acquisitions or independently audit
their allegations. Tracker and draft status can change, and the local
acquisition manifest remains the identity record for the previously acquired
series.

## Compare the criticism with the standards

The technical distinction is real. [RFC 10024 §3](https://www.rfc-editor.org/rfc/rfc10024.html#section-3)
defines hybrid key agreement with the goal of retaining security if at least
one component remains secure. Its [security section](https://www.rfc-editor.org/rfc/rfc10024.html#section-6)
qualifies this with TLS transcript binding, side-channel resistance, and RNG
requirements: shared insecure randomness can affect both components. A
hybrid is not a blanket remedy for implementation bugs.

As checked on 2026-10-12, RFC 10024 was a published Standards Track document.
Standalone ML-KEM was [draft-ietf-tls-mlkem-11](https://www.ietf.org/archive/id/draft-ietf-tls-mlkem-11.html),
intended as Informational, with its [tracker](https://datatracker.ietf.org/doc/draft-ietf-tls-mlkem/)
showing RFC Editor queue status. Its §5 discusses formal analyses,
implementation constraints, side channels, and RNG concerns; §6 requests
`Recommended: N` entries. That value means no IETF suitability statement,
not a declaration that the mechanism is necessarily flawed. Publication,
registration, recommendation, and deployment policy are different facts.

For the procedural dispute, [RFC 7282](https://www.rfc-editor.org/rfc/rfc7282.html)
describes rough consensus through consideration of technical objections,
rather than simple majority voting. Bernstein's counts and allegations need
their underlying messages and decisions checked before being treated as
findings of misconduct. The dates in his series are historical snapshots,
not evidence of today's draft state.

## Implications for a future BDP deployment

Our architectural inference is that a transport record saying only “TLS” or
“HTTPS” is insufficient for long-lived knowledge and provenance exchange.
Future review should identify the TLS implementation and version, negotiated
key-agreement group, allowed fallback behavior, authentication policy, and
relevant implementation evidence. It should also retain disputed security
arguments and their disposition, instead of treating standardization as the
end of review. These are research questions, not a new BDP requirement.

Noise does not remove that responsibility. Its standard
[DH functions](https://noiseprotocol.org/noise.html#section-12)
are classical X25519/X448; static keys address peer continuity rather than
post-quantum confidentiality. RFC 10024 warns that its TLS-specific hybrid
analysis cannot simply be transferred to another protocol.

Part 6 also supplies a useful ASSEMBLER precedent: a source claim can have
supporting evidence, counterarguments, and unresolved responses. Preserve
those typed relationships and provenance; extracting an argument into a
knowledge graph must not turn it into a verified fact.
