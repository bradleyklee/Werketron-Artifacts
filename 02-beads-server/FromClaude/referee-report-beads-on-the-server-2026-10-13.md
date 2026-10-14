# Referee Report: Beads on the Server

As of 2026-10-13. Chapter reviewed: research snapshot 2026-10-12.

## Verdict

**Keep the chapter, but trim and extend it before it goes to the Beads project.** Its Beads-facing material is accurate and partly useful, about a quarter of the text is off-topic (my estimate by paragraph), and the comparison that would show whether BDP is worth Beads' time is missing.

- **Helps:** the layer-and-listener map, the calibrated limits on what BDP has shown so far, and a few facts upstream could use directly.
- **Wastes time:** the TLS, Noise and NSA/IETF governance material. The chapter itself says it creates no BDP requirement.
- **Missing:** a comparison of BDP with Beads' own HTTP backend, which maintainers are merging now, and a stated recommendation.
- **Accuracy is good:** of 19 claims checked against primary sources, 12 hold as written, 4 need a small correction, 2 are only partly verified, and 1 is wrong (BDP's name).

Confidence: high on accuracy, since I read the primary sources. Medium on the value judgment, which depends on what the chapter is meant to do.

## Scope and method

I reviewed the chapter as it stood on main on 2026-10-12, then read the primary sources it cites and the live pull request and issue pages.

- **Assumption:** I read "Beads project" as upstream gastownhall/beads and its BDP work. If a different project was intended, the value judgment changes, not the accuracy findings.
- **Method:** read-only. I fetched sources myself and ran no code, including none of the author's. The chapter has no numeric or algebraic claims, so there was nothing to certify algebraically.
- **Requirement IDs:** no R/S/TC list was supplied, so claims are numbered C1 to C19 in chapter order and findings M1 to M6. Map them to another scheme if one applies.
- **Pins:** the chapter pins Beads at b630f96 and BDP at caf5ca7. Both resolved. Beads main has since merged #7513, so some details are already behind.
- **Fetch limits:** GitHub's folder listing refused automated access, one Dolt blog URL looped on redirects, and the companion files returned 404 (see M6).

## Value to Beads: keep, cut, add

The parts that help are the ones that sort out which layer a statement belongs to, and they are worth keeping.

| Part of the chapter | Call | Why |
| --- | --- | --- |
| Layer table and listener map (Git, Dolt, Beads, BDP, network) | Keep | Verified (C6 to C8, C17). Clears up SQL access versus remote sync versus application API. Most reusable piece. |
| Limits on what BDP has shown (Read-only, no write or History server) | Keep | Verified (C12). Add the caveats in M4 and the minor corrections. |
| Port notes, including the ephemeral-port caveat | Keep | Verified (C7). Add that setting BEADS_DOLT_SERVER_PORT marks a server as externally managed, per Beads' dolt.md. |
| Provenance: claims versus attestation | Keep, shorten | Verified (C13, C16). Overlaps #7510, which upstream is already debating. |
| TLS migration, Noise versus TLS, Radicle, NSA/IETF governance | Cut to a separate note | Accurate (C1 to C5) but nothing in Beads or BDP depends on it (M3). |
| Source map and companion-file apparatus | Fix or cut | Linked files return 404 (M6). |
| BDP versus Beads' own HTTP backend | Add | The comparison that decides the question (M1). |
| A stated recommendation | Add | The chapter ends on conditions only (M2). |
| Server-mode latency evidence | Add | The headline fact for "Beads on the Server" (M5). |

## Major findings

The chapter is accurate where I checked it. Its weaknesses are what it leaves out.

**M1. The closest competitor to BDP is missing from the comparison.** The chapter asks what BDP adds beyond Git, Dolt, DoltHub and Beads. It never compares BDP with Beads' own HTTP backend (`bd serve` and `bd connect`), which is on main and under active work. [PR #7513](https://github.com/gastownhall/beads/pull/7513) merged on 2026-10-12 and describes a `/v0/beads/...` API with capability tokens and a conformance corpus. The designs pull in opposite directions. BDP's spec says a Type Descriptor "cannot add an operation". The Beads API already has domain operations such as `:advanceMolecule`. That tension decides whether BDP earns its keep, and the chapter gives it one sentence. Confidence: high on the omission, medium on the characterization, since I read the PR text and not the API source.

**M2. There is no recommendation.** The chapter ends on conditions ("BDP may be justified if") and an open question about a Git-specific agent protocol. A reader has to infer the author's view. State one, even a provisional one, such as "not yet justified for Beads; revisit when Read+Update has an independent implementation." That wording is a suggestion, not a finding.

**M3. About a quarter of the text does not bear on Beads.** The TLS migration, Noise-versus-TLS, Radicle and NSA/IETF sections end with the chapter's own statement that they are "review implications, not a new BDP requirement." Beads federation rides Dolt remotes over SSH, HTTPS and Git, so no Noise-or-TLS decision is pending. Move these to a separate note. The share is my estimate by paragraph, not an exact count.

**M4. The chapter holds three pieces of a key design finding and never joins them.** BDP's revision covers whole state: properties, metadata and owned Links. Beads' `row_lock` does not. Label and parent edits sit outside the `--if-revision` guard (`update_input.go`). The conformance file calls this a "documented partial-coverage gap" and says case R16-c is expected to fail once a real backend wires compare-and-swap. So BDP's `expectedRevision` cannot be served from `row_lock` today. That is why the bd adapter hashes the projected record and is read-only. This synthesis is mine, drawn from three verified sources (C9, C10, C11). It is the most useful sentence the chapter could add for Beads.

**M5. Two server-side facts are missing.**

- Latency. [PR #7518](https://github.com/gastownhall/beads/pull/7518) measured `bd show` at 10.2 to 10.8 s over a 0.24 s round trip, against 0.17 s on the database host, with 24 to 48 SQL statements per command. These are SQL server-mode numbers. The PR says WAN latency of the HTTP backend is unmeasured, so "a coarse API fixes this" is a hypothesis, not a result.
- Adapter limits. The bd adapter builds each snapshot from one `bd list --all --limit 0` call, caches it for 1 s, caps output at 4,000,000 bytes and the call at 10 s, and answers 503 beyond that. One contributor's data in #7510 shows 13,635 identities in the Beads tracker itself, so a real workspace may exceed the cap. I did not run it. Medium confidence that it fails at that size.

**M6. The audit trail cannot be inspected.** Seven of seven companion files I tried returned 404 at their linked paths on main: both source studies, the syllogism, source-link coverage, the Noise and provenance research, the TLS verification and the wiki context. Broken links were set aside for this review, so this is a pre-publication blocker, not a flaw in the argument. The chapter says a coverage record audits it, and a reader cannot check that until the links resolve.

## Claim verification

Twelve of 19 claims hold as written, four need a correction, two are partly verified and one is wrong. IDs follow chapter order.

| ID | Chapter claim | Source checked | Result | Confidence |
| --- | --- | --- | --- | --- |
| C1 | Radicle's 2026-09-23 disclosure: node traffic unencrypted, peer authentication broken, custom Noise protocol being replaced by iroh | [Radicle disclosure](https://radicle.dev/2026/09/23/disclosure-of-vulnerability-in-network-protocol) | Verified. It also places the flaws in the transport layer, matching the chapter's caution about Noise. | High |
| C2 | RFC 10024 specifies ML-KEM plus ECDHE hybrid groups for TLS 1.3; its analysis relies on the TLS transcript; ML-KEM randomness matters for an insecure shared RNG | [RFC 10024](https://www.rfc-editor.org/rfc/rfc10024.html) sections 2, 4, 6 | Verified. | High |
| C3 | RFC 10024 section 3 defines a hybrid key exchange | RFC 10024 section 3 | Correction: it adopts RFC 9954's definition ("same meaning") and does not originate it. | High |
| C4 | ML-KEM draft 11 published 2026-09-17, Informational, in the RFC Editor queue, IANA Recommended N | [IETF datatracker](https://datatracker.ietf.org/doc/draft-ietf-tls-mlkem/) and draft text | Verified except the date: the draft header says 17 Sep 2026, the tracker lists a revision date of 2026-09-16. | High |
| C5 | Bernstein's NSA and IETF series has nine dated articles | [Bernstein's blog index](https://blog.cr.yp.to/index.html) | Count verified (parts 1 to 9, 2025-10-04 to 2026-08-14). I read titles only, not the articles. | Medium |
| C6 | Beads defaults to embedded Dolt; server mode uses dolt sql-server | Beads [architecture/index.md](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/architecture/index.md) and [dolt.md](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/architecture/dolt.md) | Verified. | High |
| C7 | 3307 is a common server port, 3308 for a shared server, and a managed server may use an OS-assigned port | [configfile.go](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/configfile/configfile.go) and dolt.md | Verified. The ports are in dolt.md, not the page the chapter cites. | High |
| C8 | Issue history lives under refs/dolt/data, apart from code branches; bd dolt push and pull sync it | [sync-concepts.md](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/core-concepts/sync-concepts.md) | Verified. | High |
| C9 | Beads has row-version compare-and-swap on selected writes; label and parent edits are outside the guard | [version.go](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/issueops/version.go), [issues.go](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/issues.go), [update_input.go](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/cmd/bd/update_input.go) | Verified for the Dolt store: the check shares the write's transaction. I did not read the embedded-Dolt store. | High |
| C10 | R16/R17 expected-revision conformance scaffolding has nil hooks and skipped cases | [expected_revision_contract.go](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/backend/conformance/expected_revision_contract.go) | Verified. The file adds that R16-c is expected to fail once real CAS is wired. The chapter omits this (M4). | High |
| C11 | The bd adapter hashes the canonical projected Resource for revisions and exposes no write path | [adapter-bd source](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/adapter-bd/src/index.ts) | Verified: SHA-256 of canonical JSON; the port is described as read-only. | High |
| C12 | BDP evidence is Read-profile only; Read+Update, Transactional and History servers are incomplete | [STATUS.md](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/STATUS.md) | Verified, with a calibration gap: runs are claimEligible false by construction and come from two BDP-authored targets. The chapter's "measured Read evidence" omits that. | High |
| C13 | BDP is a draft; carried attribution is data, not evidence | [BDP spec](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/specs/bdp.md) and [PR #65](https://github.com/gastownhall/bdp/pull/65) | Verified. | High |
| C14 | Five BDP PRs open on 2026-10-12; #60 is a draft Type design | [BDP PR list](https://github.com/gastownhall/bdp/pulls) and [PR #60](https://github.com/gastownhall/bdp/pull/60) | Verified: #85, #61, #60, #58, #57. #60 is marked Draft. | High |
| C15 | PR #65 merged the revisionProvenance envelope | PR #65 | Verified. Merged 2026-10-12 by its author; the page records no reviews. | High |
| C16 | Beads #7510 "Provenance V2" is a proposal, not adopted | [Beads issue #7510](https://github.com/gastownhall/beads/issues/7510) | Verified. Open; an auto-triage bot labelled it priority p3. | High |
| C17 | Federation Remotes API defaults to 8080 and BDP's reference server also defaults to 8080 | configfile.go, [BDP config source](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/config/src/index.ts), [federation.md](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/multi-agent/federation.md) | Both defaults verified. A real clash needs both to bind one address; I did not test it. I found no source for the claim that shared-server mode disables the Remotes listener by default. | High on defaults, medium on the clash |
| C18 | #7513 routes molecule behavior through HTTP-facing issueops roles; #7518 documents remote-SQL latency and a same-region workaround | [#7513](https://github.com/gastownhall/beads/pull/7513) and [#7518](https://github.com/gastownhall/beads/pull/7518) | Correction: #7513 is merged. #7518's headline workaround is running bd next to the database over SSH; a same-region server is one listed alternative. #7518 is open with changes requested. | High |
| C19 | "The Beads Data Protocol (BDP)" | BDP spec and [PR #61](https://github.com/gastownhall/bdp/pull/61) | Wrong: the spec is titled "Bead Protocol (BDP)", and open PR #61 proposes "Beads Protocol". | High |

## Minor corrections

Seven small edits fix every wording or date issue I found.

1. Replace "Beads Data Protocol" with "Bead Protocol (BDP)" and note that open PR #61 proposes "Beads Protocol" (C19).
2. Say RFC 10024 section 3 adopts RFC 9954's definition of a hybrid, not that it defines one (C3).
3. Give the ML-KEM draft 11 date as 17 Sep 2026 per the draft header, and note the tracker's 16 Sep revision date, or pick one and say which (C4).
4. Describe #7518's workaround as running bd next to the database over SSH, with a same-region server as an alternative. Note that #7513 is merged and #7518 is open (C18).
5. Qualify "measured Read evidence": runs are claimEligible false by construction, 11 case definitions are self-certified, and both targets are BDP-authored (C12).
6. Cite docs/architecture/dolt.md for the 3307 and 3308 ports (C7).
7. Give a source for the claim that shared-server mode disables the Remotes listener by default, or drop it (C17).

## Not verified

These claims were not checked against a source I opened, so treat them as unreviewed.

- **Background knowledge only, not re-fetched:** the Pro Git protocol pages, GitHub REST API docs, the Noise specification, RFC 7282, RFC 7250, RFC 8446, the IANA port and protocol registries, and the three Dolt blog posts. One Dolt URL looped on redirects.
- **Beads source claims:** the federation tests and their comments, the embedded-Dolt `UpdateIssueChecked` path, and the shared-server Remotes listener default.
- **BDP source claims:** the private transaction-store tests, the development runtime being non-attesting and loopback-only, and the content of PR #85.
- **Bernstein articles:** I read titles and tags only, so the chapter's attributed characterization is consistent with them but not confirmed.
- **Companion files:** all seven I tried returned 404 (M6).
- **Execution:** I ran no code, so the port clash (C17) and the adapter size cap (M5) are untested.

## Next steps

Five edits turn the chapter from a survey into something the Beads project can use, in this order.

1. Add a table comparing BDP with Beads' HTTP backend, and one paragraph of recommendation (M1, M2).
2. Add the `row_lock` paragraph (M4) and the latency and adapter facts (M5), marking what was measured and what is hypothesis.
3. Move the TLS, Noise, Radicle and governance material to its own note (M3).
4. Apply the seven minor corrections.
5. Restore or remove the 404 links (M6).

Three items are ready for upstream once the author approves them. None has been filed.

- Beads' federation.md draws the SQL port as 3306, while the code default and dolt.md say 3307.
- Beads' Remotes API and BDP's reference server both default to port 8080 (C17).
- Ask how BDP's `expectedRevision` is meant to be served given the `row_lock` gap (M4).

Independent checks I would write fresh and run next. I have run none of them yet.

- Start a Dolt server with its Remotes API on 8080 and the BDP reference server on defaults, and see whether the second bind fails.
- Generate a synthetic bd workspace of 15,000 or more beads and compare the `bd list --all` output size with the adapter's 4,000,000-byte cap.
- Count the exact share of the chapter taken by the TLS, Noise and governance sections, replacing my paragraph-level estimate.
- Read the embedded-Dolt `UpdateIssueChecked` path to close the one gap in C9.

## Sources

Pages opened for this review, as of 2026-10-13.

- [Chapter under review: Beads on the Server](https://github.com/bradleyklee/Werketron-Artifacts/blob/main/02-beads-server/Beads-on-the-Server.md)
- BDP at commit caf5ca7: [STATUS.md](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/STATUS.md), [spec](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/specs/bdp.md), [architecture](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/design/architecture.md), [adapter-bd](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/adapter-bd/src/index.ts), [config](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/config/src/index.ts)
- BDP pull requests: [list](https://github.com/gastownhall/bdp/pulls), [#60](https://github.com/gastownhall/bdp/pull/60), [#65](https://github.com/gastownhall/bdp/pull/65)
- Beads at commit b630f96: [architecture/index.md](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/architecture/index.md), [dolt.md](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/architecture/dolt.md), [sync-concepts.md](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/core-concepts/sync-concepts.md), [federation.md](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/multi-agent/federation.md), [configfile.go](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/configfile/configfile.go), [version.go](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/issueops/version.go), [issues.go](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/issues.go), [update_input.go](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/cmd/bd/update_input.go), [expected_revision_contract.go](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/backend/conformance/expected_revision_contract.go)
- Beads issue and pull requests: [#7510](https://github.com/gastownhall/beads/issues/7510), [#7513](https://github.com/gastownhall/beads/pull/7513), [#7518](https://github.com/gastownhall/beads/pull/7518)
- [Radicle disclosure, 2026-09-23](https://radicle.dev/2026/09/23/disclosure-of-vulnerability-in-network-protocol)
- [RFC 10024](https://www.rfc-editor.org/rfc/rfc10024.html)
- [IETF datatracker: draft-ietf-tls-mlkem](https://datatracker.ietf.org/doc/draft-ietf-tls-mlkem/)
- [D. J. Bernstein's blog index](https://blog.cr.yp.to/index.html)
