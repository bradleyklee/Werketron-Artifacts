# Source-link coverage

Coverage audit for [Beads on the Server](Beads-on-the-Server.md), checked
2026-10-13. Repository links below are pinned to the inspected commits unless
otherwise marked. “Direct” means the linked source documents or implements the
claim; “interpretation” identifies a conclusion drawn by comparing sources.

**Referee correction map.** The referee's C1–C19 numbering is separate from
this record's chapter coverage IDs. C1–C5 concern the retained TLS supplement
and are qualified below; C6–C18 are corrected or retained in the sections on
Beads, BDP, federation, and network boundaries; C19 changes “Beads Data
Protocol” to the pinned draft's “Bead Protocol,” while recording open PR #61's
proposed “Beads Protocol” wording. Referee findings M1–M5 are addressed by
the native HTTP comparison, recommendation, row-lock/R16-c synthesis, dated
latency and adapter-limit qualifications, and corrections below. M6 is
resolved for the local artifact by retaining and checking the companion paths;
public URL availability remains outside this worker's authority.

**Native HTTP comparison.** Beads' [pinned HTTP backend documentation](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/README.md#http-backend-experimental)
supports the `bd serve`/`bd connect` description and deliberate divergence
from local mode: some operations are refused and some response shapes degrade
with documented behavior differences. The surface is domain-oriented and does
not cover every local operation. Merged [Beads PR #7513](https://github.com/gastownhall/beads/pull/7513)
is the dated 2026-10-12 update: its issueops molecule routes, capability
tokens, and served tests are Beads implementation evidence, not BDP
conformance; this is PR-described merged work, not inspection of a repinned
post-merge source tree. Open [PR #7518](https://github.com/gastownhall/beads/pull/7518)
supplies reported SQL server-mode latency (10.2–10.8 seconds remotely versus
0.17 seconds beside the database, over 0.24 seconds round trip) and recommends
running `bd` near the database; HTTP latency is unmeasured. These PR facts are
post-baseline updates and do not repin the source studies.

The BDP adapter limit is supported by its pinned adapter source and manager
study: one `bd list --all --limit 0` snapshot, one-second cache, 10-second
call limit, 4,000,000-byte cap, and 503 beyond the cap. The 13,635-identity
figure is contributor-reported in Beads #7510, not a worker measurement; no
record-count failure is claimed. The BDP Read evidence is also qualified:
`claimEligible: false` by construction, 11 self-certified case definitions,
and two BDP-authored targets. No BDP public Read+Update, Transactional, or
History serving claim is inferred.

**Revision coverage.** Beads' selected `row_lock` CAS checks are distinct
from the broader R16/R17 expected-revision contract, whose nil hooks and
skipped cases include the R16-c caveat. The BDP `bd` adapter hashes the
projected resource for a read revision and does not expose a conditional
write. This supports the chapter's interpretation that a whole-resource BDP
revision cannot currently be mapped to `row_lock` alone; it does not explain
the adapter author's design choice beyond the observed read-only boundary.

**Git objects and transports.** The chapter's description of repository
objects and local, HTTP(S), SSH, and native protocol access is documented in
[Pro Git server protocols](https://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols)
and [transfer protocols](https://git-scm.com/book/en/v2/Git-Internals-Transfer-Protocols).
[Protocol v2](https://git-scm.com/docs/protocol-v2) documents request/response
negotiation. The distinction between Git transfer and the
[GitHub REST API](https://docs.github.com/en/rest) follows from their
separate documented operation scopes (interpretation).

**Dolt data, SQL, and remotes.** The chapter's description of versioned
relational data and remote history movement is supported by the
[Dolt docs](https://docs.dolthub.com/), [remote internals](https://www.dolthub.com/blog/2026-10-08-how-dolt-remotes-work/),
and [SQL remotes explanation](https://www.dolthub.com/blog/2021-09-22-sql-remotes/)
(documentation). Multiple remote forms are shown by the
[SSH remote announcement](https://www.dolthub.com/blog/2026-03-17-announcing-ssh-remotes/)
and [Git remote support](https://www.dolthub.com/blog/2026-02-19-supporting-git-remotes-as-dolt-remotes/)
(implementation announcements); their mechanics are not treated as
equivalent. The service boundary between DoltHub, the engine, and SQL server
is a synthesis of [DoltHub](https://www.dolthub.com/) and the Dolt docs.

**MySQL and Beads storage.** MySQL classic protocol and port reference:
[protocol](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_PROTOCOL.html)
and [port table](https://dev.mysql.com/doc/mysql-port-reference/en/mysql-port-reference-tables.html)
(protocol/product documentation). Beads embedded/server modes and its
configured/common 3307, shared 3308, and possible ephemeral managed port are
supported by pinned [architecture](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/architecture/index.md),
[`doltserver.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/doltserver/doltserver.go),
and [`configfile.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/configfile/configfile.go)
(docs and implementation). The distinction between Dolt data refs and SQL
access is supported by pinned [sync concepts](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/core-concepts/sync-concepts.md)
and [`bootstrap.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/bootstrap.go)
(docs and implementation).

**Beads federation transport.** The pinned
[federation guide](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/multi-agent/federation.md)
describes MySQL on 3306 for multi-writer SQL and Dolt Remotes API on 8080 for
peer-to-peer push/pull (documentation). The configured default and mode-aware
resolution are in [`configfile.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/configfile/configfile.go)
and [`doltserver.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/doltserver/doltserver.go)
(implementation). The chapter distinguishes this synchronization service
from BDP's separately configured 8080 resource API; the possible bind-port
conflict when colocated is an operational inference.

**Beads graph semantics.** The claim that links express application
relationships is documented in pinned [graph links](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/core-concepts/graph-links.md)
and [architecture](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/architecture/index.md).
The distinction from network routing is an architectural interpretation.
Federation's use of Dolt history is documented in the pinned
[federation guide](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/multi-agent/federation.md);
its separation from SQL and BDP access is synthesis. The same commit's
[`federation_test.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/federation_test.go)
states that remote configuration is tested without a live remote and its
push/pull cases use a nonexistent peer. These tests establish local setup,
cleanup, and failure behavior, not a successful peer-to-peer transfer. The
separate [`route_logging_test.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/route_logging_test.go)
does successfully push/pull a local `file://` remote via SQL, while
[`route_logging_integration_test.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/route_logging_integration_test.go)
only checks that a nonexistent `git+file://` target chooses the CLI route and
fails. This is evidence of local-file transfer and route selection, not
successful live network/provider transfer across the documented remote forms.

The pinned tree also contains an integration-tagged
[`doltremoteapi://` pull test](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/pull_branch_tracking_integration_test.go)
that starts a local SQL server and Remotes API listener, then checks the
branch-tracking fallback and pulled data. It establishes that this positive
loopback integration path is represented in source; it was not run here, and
it does not establish hosted or cloud-provider behavior.

**Revision-guard distinctions.** Selected Beads write paths implement
row-version guards: [`CheckVersionInTx`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/issueops/version.go)
checks `row_lock` in the mutation transaction, with checked paths in the
[Dolt](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/issues.go)
and [embedded-Dolt](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/embeddeddolt/issues.go)
stores. The CLI exposes selected `--if-revision` guards
([`update.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/cmd/bd/update.go)); its update input
explicitly excludes label and parent edits from that guard
([`update_input.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/cmd/bd/update_input.go)).
The shared
[`expected_revision_contract.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/backend/conformance/expected_revision_contract.go)
and the pinned [`Dolt`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/expected_revision_contract_test.go)
and [`embedded-Dolt`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/embeddeddolt/expected_revision_contract_test.go)
test wiring leave hooks nil and skip the broader R16/R17 opaque-address,
whole-state contract cases. That is an unverified cross-backend contract, not
evidence that the selected `row_lock` guards do not exist. Listed code and
tests were inspected but not run here. The pinned BDP `bd` adapter derives a
read revision by hashing the canonical projected Resource
([adapter](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/adapter-bd/src/index.ts));
the shared public Read-profile handler accepts only GET and HEAD
([server](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/server/src/index.ts)).
BDP also has a separate [non-attesting, loopback-only development runtime](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/server/src/development-runtime.ts)
with limited POST mutation routes; this does not establish a public transactional profile.
BDP's pinned [private transaction-store tests](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/server/src/transaction-store.test.ts)
cover that separate implementation, while its pinned [status](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/STATUS.md)
still marks public Transactional serving incomplete. The existing Beads
guards therefore do not establish end-to-end conditional writes through the
BDP `bd` adapter.

**BDP proposal and evidence.** The draft's protocol claims link to the pinned
[specification](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/specs/bdp.md).
The differences among proposal, implementation, demo, and conformance evidence
are documented in pinned [status](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/STATUS.md),
[architecture](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/design/architecture.md),
[Read demo](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/read-demo.md),
and [History demo](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/history-client-demo.md).
The default 8080 port and `BDP_SERVER_PORT` setting come from pinned
[configuration source](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/config/src/index.ts)
and [startup design](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/design/startup-configuration.md);
the claim that these are deployment settings rather than protocol semantics
is an interpretation. The draft's [actor attribution](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/specs/bdp.md#actor-attribution)
and [carried attribution](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/specs/bdp.md#carried-attribution)
sections state that the authenticated principal is authorization input, not
Resource protocol data, and that `revisionProvenance` is carried data, not an
authority attestation (proposed protocol behavior). The chapter's boundary
between authentication configuration and actor attestation is an
interpretation of those sections. BDP's potential value as a uniform
independent-client contract is a synthesis and remains an open evaluation
question.

**BDP Read operation trace.** The manager source report traces Scope discovery,
collection retrieval, Bead/Link/Type resources, property views, and incident
Link reads from [`read-request.ts`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/server/src/read-request.ts)
through the shared [`server/index.ts`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/server/src/index.ts)
and [`adapter-bd/src/index.ts`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/adapter-bd/src/index.ts).
The associated [`HTTP handler tests`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/server/src/http-handler.test.ts)
and [`adapter tests`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/adapter-bd/src/index.test.ts)
are code evidence only; they were not run in this work order. The trace
supports the chapter's implemented Read boundary and does not establish a
served write, History, or Transactional profile.

The 2026-10-12 open-PR snapshot is linked inline in the chapter: BDP [#60](https://github.com/gastownhall/bdp/pull/60)
and [#85](https://github.com/gastownhall/bdp/pull/85) are Type design/tracking
documents; Beads [#7513](https://github.com/gastownhall/beads/pull/7513) was
recorded in the snapshot as open but is now a dated merged update adding
HTTP-facing application operations, while [#7518](https://github.com/gastownhall/beads/pull/7518)
remains open and documents remote SQL latency. The snapshot is historical;
the linked PR pages supply the update. Exact search scope, PR metadata, and
changed paths are preserved in the [upstream PR snapshot](source-reports/upstream-pr-snapshot-20261012.json).

**Provenance and Radicle.** Beads issue [#7510](https://github.com/gastownhall/beads/issues/7510)
was an open proposal at the 2026-10-12 check. Merged BDP [PR #65](https://github.com/gastownhall/bdp/pull/65)
implements a narrower revision-provenance envelope; the pinned
[status](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/STATUS.md)
was checked on that date. Radicle's [protocol guide](https://radicle.dev/guides/protocol)
documents Git replication, gossip, peer identity, and Noise XK. Its
[2026-09-23 disclosure](https://radicle.dev/2026/09/23/disclosure-of-vulnerability-in-network-protocol)
reports deployed authentication/encryption failures and planned iroh
migration. No causal claim is made against Noise itself. The bounded Noise/TLS
comparison links the [Noise handshake patterns](https://noiseprotocol.org/noise.html#section-7.5),
[TLS 1.3 authentication](https://www.rfc-editor.org/rfc/rfc8446.html#section-4.4),
and [TLS raw public keys](https://www.rfc-editor.org/rfc/rfc7250.html).
Its practical advantage/limitations and identity qualifications are also
analyzed in [provenance-and-noise-research.md](provenance-and-noise-research.md).
This is not a claim about BDP's current authentication or transport
implementation.

**Network registries.** TCP service-port entries are checked against the
[IANA service registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml);
IP protocol numbers are checked separately in the
[IANA protocol registry](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml).
The 9418/TCP, 22/TCP, 443/TCP, and 3306/TCP registrations are registry
evidence. BDP's 8080 and Beads' Remotes API 8080 are project defaults
documented above, not IANA registrations.

**TLS migration and governance.** Bernstein's nine-entry NSA and IETF series
is an author's criticism and allegation set, not an independently established
finding. The [series index](https://blog.cr.yp.to/index.html), local
[governance research](tls-standards-governance-research.md), and its
[acquisition manifest](source-reports/bernstein-series-acquisition.json)
provide the dated source identity, selective-reading boundary, and explicit
limits. The chapter therefore attributes the criticism and does not introduce
a claim that TLS or ML-KEM is currently compromised.

[RFC 10024 section 3](https://www.rfc-editor.org/rfc/rfc10024.html#section-3)
and its [security section](https://www.rfc-editor.org/rfc/rfc10024.html#section-6)
support the protocol facts that published TLS 1.3 PQ/T groups combine ECDHE
with ML-KEM and that hybrid security depends on the TLS transcript and careful
implementation, including side-channel and RNG qualifications. The
[standalone ML-KEM draft 11](https://www.ietf.org/archive/id/draft-ietf-tls-mlkem-11.html)
and [IETF tracker](https://datatracker.ietf.org/doc/draft-ietf-tls-mlkem/),
checked on 2026-10-12, support the dated facts that the draft is Informational,
has `Recommended: N` entries, and was in the RFC Editor queue awaiting a first
editor. Those status facts are not a deployment verdict. [RFC
7282](https://www.rfc-editor.org/rfc/rfc7282.html) supports the governance
fact that rough consensus addresses technical objections and is not a simple
majority vote. The chapter's recommendation to record negotiated transport
details and provenance evidence, and its separation of key agreement, peer
authentication, and durable provenance, are explicitly marked architectural
inference. The [Noise specification](https://noiseprotocol.org/noise.html#section-12)
and RFC 10024's TLS-specific analysis support the limitation that selecting
Noise does not supply PQ security or transfer TLS's hybrid analysis.

The chapter's linked source map is a navigation aid authored for this report.
It is not output from Beads, BDP, an extractor, or a graph-inference operation.
The Noise/TLS comparison is exploratory research and should be read with the
linked provenance note; it is not a finding about BDP's current authentication
or transport implementation.

## Claim-level index

This compact index makes the material claim-to-source mapping auditable without
turning the chapter into a detached bibliography. Classifications are
`implementation`, `documentation`, `proposal`, `demonstration/test`, or
`interpretation`.

| ID | Material claim | Exact supporting source(s) | Class |
| --- | --- | --- | --- |
| C1 | Git transports move repository objects; GitHub REST is a separate API. | [Pro Git protocols](https://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols); [GitHub REST](https://docs.github.com/en/rest) | documentation; interpretation |
| C2 | Dolt SQL access is distinct from Dolt push/pull and remote history. | [Dolt remotes](https://www.dolthub.com/blog/2026-10-08-how-dolt-remotes-work/); [SQL remotes](https://www.dolthub.com/blog/2021-09-22-sql-remotes/) | documentation |
| C3 | DoltHub and other remote forms are synchronization endpoints, not automatically SQL listeners. | [DoltHub](https://www.dolthub.com/); [SSH remotes](https://www.dolthub.com/blog/2026-03-17-announcing-ssh-remotes/); [Git remotes](https://www.dolthub.com/blog/2026-02-19-supporting-git-remotes-as-dolt-remotes/) | documentation; interpretation |
| C4 | Beads adds application entities and graph relationships over Dolt. | [Beads architecture](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/architecture/index.md); [graph links](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/core-concepts/graph-links.md) | documentation |
| C5 | Beads has selected row-version guards, while the broader BDP/public revision contract remains bounded. | [Beads version check](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/issueops/version.go); [BDP status](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/STATUS.md) | implementation; proposal/status |
| C6 | BDP proposes generic Bead/Link HTTP/JSON resources and configurable service startup. | [BDP draft](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/specs/bdp.md); [BDP config](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/config/src/index.ts) | proposal; implementation |
| C7 | BDP Read evidence, demos, private tests, and unmerged PRs do not prove complete public write/history/transaction serving. | [BDP status](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/STATUS.md); [Read demo](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/read-demo.md); [History demo](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/history-client-demo.md) | demonstration/test; interpretation |
| C8 | Federation exchanges Dolt history through configured remotes and is distinct from SQL and BDP access. | [federation guide](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/multi-agent/federation.md); [federation implementation](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/federation.go) | documentation; implementation; interpretation |
| C9 | Revision history, activity events, provenance envelopes, and durable attestation are different claims. | [Beads #7510](https://github.com/gastownhall/beads/issues/7510); [BDP PR65](https://github.com/gastownhall/bdp/pull/65); [provenance note](provenance-and-noise-research.md) | proposal; implementation; interpretation |
| C10 | Radicle demonstrates layered Git/peer transport, but its 2026-09-23 disclosure qualifies deployed Noise claims. | [Radicle protocol](https://radicle.dev/guides/protocol); [disclosure](https://radicle.dev/2026/09/23/disclosure-of-vulnerability-in-network-protocol) | documentation; security disclosure |
| C11 | Service ports are distinct from IP protocol numbers; 8080/3307 are project defaults, not dedicated IANA assignments. | [IANA service registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml); [IANA protocol registry](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml); pinned Beads/BDP configuration sources above | registry evidence; implementation; interpretation |
| C12 | The analogy is useful across versioned state and synchronization but breaks at storage, SQL, application graph, protocol, and routing boundaries. | [syllogism](syllogism.md); [Beads study](source-reports/beads-source-study.md); [BDP study](source-reports/bdp-source-study.md) | interpretation |
| C13 | Bernstein's NSA/IETF series supplies attributed criticism about standalone PQ, hybrid hedges, and governance; it does not establish current compromise or misconduct. | [series index](https://blog.cr.yp.to/index.html); [acquisition manifest](source-reports/bernstein-series-acquisition.json); [governance research](tls-standards-governance-research.md) | attributed criticism; source-limit |
| C14 | RFC 10024 defines TLS 1.3 PQ/T hybrids and qualifies their security with transcript binding, side-channel resistance, and RNG requirements. | [RFC 10024 §3](https://www.rfc-editor.org/rfc/rfc10024.html#section-3); [RFC 10024 §6](https://www.rfc-editor.org/rfc/rfc10024.html#section-6) | protocol fact; implementation qualification |
| C15 | Dated standalone ML-KEM draft 11 is Informational, has `Recommended: N` entries, and was in the RFC Editor queue on the 2026-10-12 tracker check; these facts are not a deployment verdict. | [draft 11](https://www.ietf.org/archive/id/draft-ietf-tls-mlkem-11.html); [IETF tracker](https://datatracker.ietf.org/doc/draft-ietf-tls-mlkem/) | protocol/status fact; interpretation |
| C16 | RFC 7282 describes rough consensus as consideration of technical objections, not majority vote counting. | [RFC 7282](https://www.rfc-editor.org/rfc/rfc7282.html) | governance fact |
| C17 | Future knowledge exchange should distinguish key agreement, peer authentication, and durable provenance; Noise's classical DH choices do not provide PQ security or import RFC 10024's TLS analysis. | [Noise §12](https://noiseprotocol.org/noise.html#section-12); [RFC 10024 §6](https://www.rfc-editor.org/rfc/rfc10024.html#section-6); [provenance note](provenance-and-noise-research.md) | architectural inference; limitation |

The source studies and [upstream PR snapshot](source-reports/upstream-pr-snapshot-20261012.json)
preserve exact commit pins, tracked-path inventories, and dated open-work
status. This index does not claim fresh upstream state beyond the stated
2026-10-12 evidence date.
