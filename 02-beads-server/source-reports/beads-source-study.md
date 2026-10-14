# Beads source study — verified worker finalization

Date checked: 2026-10-12 UTC

This report finalizes the supplied Beads source account for the bounded
`beads-source-study` work order. Source acquisition and source-code inspection
were performed by the manager and Sol in a separate isolated clone.
This worker verifies and finalizes the supplied research account; it
does not claim an independent full source-code review, a new clone, live PR
checks, runtime experiments, or upstream test execution.

## Reproducible source pin

Repository: <https://github.com/gastownhall/beads>

Pinned commit: `b630f96f5bd231ff7aea78af0d47b6038f228d00`

Pinned tree: <https://github.com/gastownhall/beads/tree/b630f96f5bd231ff7aea78af0d47b6038f228d00>

The supplied [checkout manifest](beads-source-checkout.json) records:

- commit date `2026-10-12T09:02:22Z`;
- an empty working-tree field;
- 4,791 tracked paths; and
- inventory file [beads-tracked-paths.txt](beads-tracked-paths.txt) with
  SHA-256 `e6ca45b5b28c39da59c56d4459fe5108c0f0961ddefaa9e62b918453d152af5a`.

The worker independently checked the supplied manifest and inventory in the
task snapshot. `wc -l` reports 4,791 lines, and `sha256sum` reports the exact
manifest hash above. The inventory is newline-terminated, has no duplicate
path visible in the checked set, and its first and last entries are preserved
by the committed file. The manifest says the source came from an isolated
manager-side clone and that the earlier worker source study stopped before
inspection.

The supplied input artifacts themselves were present at task input commit
`39961958` and were read in full for this finalization:

Input `beads-source-study-manager.md` hash:
`58c0b7f68ac6dc897268fe14d4bbd4a1bb641bb844953fd04cb82b660e4efa67`

Input `beads-source-checkout.json` hash:
`a3780f45786ba92a3918f73cb3436d0090a1a00948a63497a7d4d9e1d8abee83`

Input `beads-tracked-paths.txt` hash:
`e6ca45b5b28c39da59c56d4459fe5108c0f0961ddefaa9e62b918453d152af5a`

Input `upstream-pr-snapshot-20261012.json` hash:
`2e5e80f89d94bd54772cb7bb4b830e1565a82d6b93f86fe217b9b313250dfbc7`

Input `provenance-and-noise-research.md` hash:
`28e95e035f04a19dc3b6a32ebb1c257e3ae3706bcedbfc9d88a49afeca061b73`

## Instructions and documentation organization

The supplied source account reports that the pinned repository's contributor
[`AGENTS.md`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/AGENTS.md)
identifies GitHub Issues as the public tracker, treats the internal `bd`
ledger as optional for contributors, routes storage through Dolt's storage
driver boundary, and identifies Bazel lanes (`make test`, `make check`, and
related targets) as the canonical build/test gate. It also requires behavior
changes to have corresponding user documentation. `AGENT_INSTRUCTIONS.md`
routes `bd` users to user documentation.

The reported documentation map separates architecture, core concepts, getting
started, multi-agent/federation, reference, and operations. Relevant paths
include:

- `docs/architecture/index.md` and `docs/architecture/dolt.md`;
- `docs/core-concepts/sync-concepts.md` and
  `docs/core-concepts/graph-links.md`;
- `docs/getting-started/sync-setup.md`; and
- `docs/multi-agent/federation.md`.

The supplied instruction review also covers
[`CONTRIBUTING.md`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/CONTRIBUTING.md),
`cmd/bd/AGENTS.md`, and `engdocs/AGENTS.md`.
These distinguish contributor
documentation from user documentation, define CLI/storage boundaries, require
JSON corpus and generated-reference checks where applicable, and require
exact relative links in engineering documentation.

## Storage, access, and history

The source account's documentation and implementation trace establish the
following bounded claims.

1. Dolt is Beads' storage backend. Embedded mode is the default deployment
   path; server mode connects to a Dolt SQL server. Mode resolution and
   lifecycle code are in `internal/doltserver/servermode.go` and
   `internal/doltserver/`.
2. `configfile.DefaultDoltServerPort` is 3307 in
   `internal/configfile/configfile.go`. This is a Beads/Dolt configuration
   default, not an IANA assignment and not MySQL's conventional 3306.
   The mode and port-source tests distinguish OS-assigned project ports from
   configured and external defaults.
3. Beads data history is distinct from ordinary Git source history. The
   account identifies `refs/dolt/data` in `internal/storage/dolt/bootstrap.go`
   and the sync documentation. `bd dolt push` and `bd dolt pull` move Dolt
   history to or from a Dolt remote; they are not SQL statements sent to the
   SQL listener. Embedded mode requires no TCP SQL listener.
4. The documentation lists DoltHub, S3, GCS, filesystem paths, HTTPS, SSH,
   and Git-style remotes. That list is not evidence that every provider or
   transport has the same implementation or successful live coverage.
5. `PushTo` and `PullFrom` in `internal/storage/dolt/federation.go` select
   between Dolt SQL procedures and a Dolt CLI subprocess. Git-protocol remotes
   use the CLI route; credentials and server mode also affect route selection.
   A local `file://` route has positive test evidence. The integration route
   test uses a nonexistent `git+file://` target and checks failure plus route
   logging. No live-provider success is claimed for SSH, HTTPS, DoltHub, or
   cloud storage.

The supplied behavior-to-test map identifies these implementation and test
paths:

### Selected mechanism traces

- **Mode and ports:** `internal/doltserver/doltserver.go`,
  `servermode.go`, and `portsources_test.go` separate embedded/server modes
  and port sources.
- **Dolt data refs:** `internal/storage/dolt/bootstrap.go` and
  `docs/core-concepts/sync-concepts.md` distinguish database history from the
  Git source branch.
- **Federation setup/failure:** `internal/storage/dolt/federation.go` and
  `federation_test.go` cover configuration, local state, staging cleanup, and
  failure paths, but not hosted synchronization success.
- **Remotes API fallback:**
  `internal/storage/dolt/pull_branch_tracking_integration_test.go` contains a
  loopback SQL/Remotes API success test; it was not run here.
- **Local route choice:** `route_logging_test.go` and
  `route_logging_integration_test.go` provide local `file://` success and
  failed nonexistent `git+file://` route-selection evidence.

## Application entities and graph semantics

Beads stores issues, dependencies, labels, comments, and events in Dolt.
The user-facing graph documentation and `internal/storage/issueops/` trace
typed dependency/link relationships, including blocking and non-blocking
associations, reachability, and cycle controls. `cycles.go` and `cycles_test.go`
are the selected implementation/test evidence.

These are application relationships. They are not packet routes, IP paths, or
proof of a network-routing algorithm. Federation composes Beads application
semantics with remote Dolt history exchange. The reported federation docs
describe hub-spoke, mesh, and hierarchical deployment patterns; those are
topology choices, not guarantees that Beads implements a particular routing
algorithm.

## Revisions, history, and proposal boundaries

The pinned source account traces issue history and as-of reads through
`internal/storage/dolt/history.go` and `history_test.go`. It separately traces
selected row-version guards through `internal/storage/issueops/version.go`,
`internal/storage/dolt/issues.go`, `internal/storage/embeddeddolt/issues.go`,
and `cmd/bd/if_revision_proxied_integration_test.go`. Those selected paths
compare a current `row_lock`/`ExpectedVersion` token in the write transaction
and reject a stale token, within the stated CLI and operation scope.

The account also identifies a separate
`backend/conformance/expected_revision_contract.go` fixture contract and its
Dolt/embedded wiring. Its nil hooks and skipped cases do not establish the
broader opaque-address or whole-state R16/R17 contract across backends. The
selected row-lock behavior must therefore not be expanded into a general
cross-backend CAS claim.

This distinction matters to BDP: Beads/Dolt history, selected row-version
guards, and BDP's proposed opaque resource revisions are related but are not
the same mechanism. A SQL query, a Dolt history transfer, an application graph
edge, and a protocol revision token have different boundaries.

## Dated upstream activity

The supplied [upstream snapshot](upstream-pr-snapshot-20261012.json) records a
read-only, topic-filtered GitHub API search checked on 2026-10-12. It preserves
the exact base/head commits and all returned changed paths. It is not an
exhaustive survey of open work and must be refreshed before publication.

Relevant Beads PRs in that snapshot are:

- [#7513](https://github.com/gastownhall/beads/pull/7513): open, based
  exactly on `b630f96`; HTTP molecule/issueops work, not BDP conformance.
- [#7518](https://github.com/gastownhall/beads/pull/7518): open docs-only
  change, based exactly on `b630f96`; remote SQL latency guidance, not a new
  protocol implementation.
- [#7511](https://github.com/gastownhall/beads/pull/7511): open, based on the
  older `7477ec1`; bounds an advisory Git remote probe wait, not federation or
  SQL evidence.
- [#6943](https://github.com/gastownhall/beads/pull/6943): open, based on the
  older `4493eb8`; proposes a history participation/write fence and is not
  merged behavior.
- [#7169](https://github.com/gastownhall/beads/pull/7169): open draft, based
  on the older `b1bee12`; guarded JSON batches whose description disclaims BDP
  conformance.
- [#7282](https://github.com/gastownhall/beads/pull/7282): open draft, based
  on the older `e72cd8b`; CLI preflight error classification, not a general
  backend CAS contract.

Only #7513 and #7518 are based on the exact inspected commit. The other
changes are prospective until rebased and reviewed against the pinned source.

## Provenance and identity boundaries

The supplied [provenance and Noise research note](../provenance-and-noise-research.md)
is an integration input, not a change to the pinned source account. It records
the following distinctions for the later chapter:

- Noise can authenticate possession of a static key in a chosen handshake,
  but application policy must bind that key to a principal and decide
  continuity, rotation, revocation, and recovery.
- TLS can use certificates, PSKs, or raw/pinned public keys; Noise can use
  configured keys, certificates, or continuity pins. “Customer” and
  “neighborhood” are deployment archetypes, not inherent properties of either
  protocol.
- Neither TLS nor Noise proves honest code execution or durable authorship of
  a Bead/Link. A durable provenance claim needs separate signer identity,
  binding, version, freshness, and verification rules.
- Radicle is a layered Git/peer-transport comparison, not evidence that
  Beads, Dolt, or BDP require Noise. Its 2026-09-23 transport disclosure must
  remain alongside the protocol-guide description; it is not an unqualified
  security endorsement.

For Beads issue [#7510](https://github.com/gastownhall/beads/issues/7510), the
2026-10-12 account classifies revision-provenance and activity-provenance
records as an open P3 proposal. BDP PR #65 is merged and supplies a subset
around a shared `revisionProvenance` envelope for Beads and Links. The merged
subset does not make the full proposal, source completeness, Activity records,
terminal deletion versions, or CLI/query changes an already-deployed Beads
provenance system. In particular, an `actor` field does not authenticate the
actor merely by being present.

## Findings against the Stage 1 checklist

The supplied evidence supports this bounded account of the working analogy
`filesystem : Git :: database : Dolt`:

- Dolt supplies versioned relational storage and remote history
  synchronization; Beads supplies domain records, workflow semantics, and
  typed relationships.
- SQL access is distinct from Dolt push/pull and from database-history refs.
- Beads dependency links are application graph edges, not network paths.
- Embedded Beads can operate without a SQL TCP listener; SQL server mode is a
  separate deployment choice.
- Federation composes application semantics with remote Dolt synchronization;
  it is not identical to SQL access or a generic HTTP protocol such as BDP.
- Selected row-version guards are evidenced, but the broader opaque expected-
  revision contract remains unresolved across backends and operation roles.
- The BDP/Beads provenance boundary is a proposal-versus-implementation
  distinction, not proof of authenticated durable provenance.

These are source-classified synthesis findings from the supplied manager/Sol
inspection. They are not a protocol redesign, an interoperability proof, or a
claim that all documented transports and all federation cases were reviewed.

## Verification record and limitations

Worker checks completed:

1. Read the complete supplied manager report, checkout manifest, tracked-path
   inventory, dated upstream snapshot, and provenance/noise note.
2. Confirmed all five inputs exist in the task snapshot at commit `39961958`.
3. Confirmed the checkout manifest's commit, date, empty working-tree field,
   path count, inventory path, and inventory SHA-256.
4. Confirmed `wc -l` and `sha256sum` agree with the declared 4,791-path
   inventory and hash.
5. Checked the pinned BDP account and its inventory as a dependent source
   context; no BDP source was cloned or fetched by this worker.

No upstream repository, branch, pull request, Beads database, or canonical
memory was changed. No Go tests or runtime experiments were run in this
worker. The supplied manager report states that the pinned Beads tests were
not run because the available Go version was 1.24.4 while the pinned
`go.mod` requires Go 1.26.5 or newer; `GOTOOLCHAIN=local` prevented a network
toolchain fetch. Therefore all listed implementation tests are source
evidence, not test results from this worker.

The report is a bounded source account rather than line-by-line review of all
4,791 paths. It does not establish hosted-provider success, complete
federation coverage, universal CAS semantics, current PR state after
2026-10-12, or any runtime behavior not directly recorded in the supplied
evidence. These limits are intentional and must remain visible in manager QA
and in any later chapter.
