# Beads on the Server

*A source-grounded comparison of Git, Dolt, Beads, and BDP*
Research snapshot: 2026-10-13 referee revision; baseline source studies checked
at 2026-10-12

Git users already know the shape of distributed work: a repository has a
history, branches name lines of change, and remotes exchange repository data.
The proposal examined here starts with a parallel:

```text
filesystem : Git  :: database : Dolt
```

It is a useful question, not an identity. Git versions file-system trees and
exchanges Git objects. Dolt gives relational data SQL access together with
commits, branches, merges, and remotes. Beads stores work items and typed
relationships on Dolt. The Bead Protocol (BDP) proposes an HTTP/JSON
interface over generic Beads and Links. Each layer answers a different
question: what is stored, how it is versioned, how versions move, what the
records mean, and how a client addresses a service.

The naming is dated evidence: the pinned BDP specification calls this the
“Bead Protocol,” while open PR [#61](https://github.com/gastownhall/bdp/pull/61)
proposes “Beads Protocol.” This chapter uses BDP without treating either
unmerged naming proposal as settled.

## Git: repository objects and transport

Git's repository model stores objects such as blobs, trees, and commits; refs
name commits and other objects. Its transport protocols move repository data.
The familiar [Pro Git protocol chapter](https://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols)
groups access as local, HTTP(S), SSH, and the native `git://` protocol. Local
access needs no network listener. Smart HTTP uses HTTP requests to negotiate
and transfer Git data; SSH runs Git's upload/receive programs through an
authenticated shell; the native Git daemon normally listens on TCP 9418 and
does not authenticate peers. Git can also delegate schemes to remote helpers.
The [Git transfer-protocol description](https://git-scm.com/book/en/v2/Git-Internals-Transfer-Protocols)
explains that transport is the path used to exchange repository objects, not
the repository's meaning. [Protocol v2](https://git-scm.com/docs/protocol-v2)
defines request/response negotiation over supported transports.

GitHub is one host and collaboration service for Git repositories. Its
[GitHub REST API](https://docs.github.com/en/rest) exposes application operations
such as repository, issue, and pull-request management. That API is not the
Git object-transfer protocol. A repository may be cloned or pushed through
Git transports while a separate HTTP API manages hosting features.

## Dolt: relational data with revision operations

Dolt combines SQL access with version-control operations over database state.
Its tables and indexes are represented by Dolt's content-addressed storage
structures; commits identify database versions, and branches and merges
operate on those versions. The [Dolt documentation](https://docs.dolthub.com/)
and its account of [how Dolt remotes move data](https://www.dolthub.com/blog/2026-10-08-how-dolt-remotes-work/)
describe two interfaces that are easy to conflate:

- SQL reads or changes rows through a database connection.
- Dolt `fetch`, `pull`, and `push` exchange committed database history with a
  remote, then update or merge refs and working state.

Those are different operations. A running Dolt SQL server can accept SQL over
the MySQL client/server protocol; a Dolt remote is a synchronization endpoint.
Some Dolt versions also expose remote procedures through SQL, but calling
`DOLT_PUSH()` from SQL does not make a SQL query identical to the remote
transfer: the SQL statement invokes a synchronization operation. The Dolt
team's [SQL remotes explanation](https://www.dolthub.com/blog/2021-09-22-sql-remotes/)
describes that distinction directly.

Dolt supports multiple remote forms. Depending on Dolt version and
configuration, these include DoltHub, SQL-server remotes, Git remotes, local
paths, cloud storage, and SSH. The [SSH remote announcement](https://www.dolthub.com/blog/2026-03-17-announcing-ssh-remotes/)
and [Git-remote implementation account](https://www.dolthub.com/blog/2026-02-19-supporting-git-remotes-as-dolt-remotes/)
are examples of distinct transports carrying Dolt database history. A remote
is not necessarily a queryable SQL server: ordinary storage and hosted remotes
are accessed with Dolt's remote operations, while a SQL server exposes a live
database interface.

## DoltHub: hosted remote synchronization

DoltHub is a hosted service for Dolt databases: it stores and presents
database history and supports remote collaboration. A local Dolt client can
clone a database, commit changes, and push or pull them. That service is
separate from the Dolt engine and separate from a MySQL-compatible SQL
listener. A hosted database product may offer a SQL endpoint too, but that
does not collapse SQL queries and remote history synchronization into one
interface. The [DoltHub site](https://www.dolthub.com/) and Dolt's
[remote documentation](https://docs.dolthub.com/)
describe the hosted service and client workflow.

## Embedded Dolt and the SQL server

Dolt may run embedded inside an application, or as a separate `dolt
sql-server` process. Embedded mode can serve SQL calls inside the process
without opening a TCP listener. A standalone Dolt SQL server commonly uses
TCP 3306, the default for the classic MySQL protocol; both server ports and
bind addresses are configurable. MySQL's [client/server protocol reference](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_PROTOCOL.html)
describes the wire protocol, and its [port reference](https://dev.mysql.com/doc/mysql-port-reference/en/mysql-port-reference-tables.html)
identifies 3306/TCP as the classic protocol default.

Beads currently uses Dolt as its storage backend. Its
[architecture documentation](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/architecture/index.md)
says embedded mode is the default and server mode connects to a Dolt SQL
server. The Beads documentation describes 3307 as its common per-project
server port, with 3308 used for a shared server. Source qualification matters:
the pinned implementation can allocate an OS-selected ephemeral port for a
managed per-project server when no port is configured; a configured or remote
server can use 3307. See
[`internal/doltserver/doltserver.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/doltserver/doltserver.go)
and [`internal/configfile/configfile.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/configfile/configfile.go).
Treat 3307 as a documented/common default, not a guarantee about every live
listener.

Beads also separates Dolt history from source-code branches. Its sync guide
says issue history is published in `refs/dolt/data`, while ordinary Git
branches such as `refs/heads/main` carry source files. `bd dolt push` and
`bd dolt pull` synchronize that database history; they are not equivalent to
querying the SQL listener. See the pinned
[Beads sync concepts](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/core-concepts/sync-concepts.md)
and the implementation's
[`internal/storage/dolt/bootstrap.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/bootstrap.go).

## Beads: application data and relationships

Beads adds an application model to Dolt: issues or tasks, typed dependencies,
labels, comments, events, and related workflow data. Beads commands decide
what a task means, which work is ready, and what a relationship such as
`blocks`, `parent-child`, or `related` means. Those semantics belong to
Beads; Dolt supplies the database and versioned storage beneath them. The
pinned [architecture overview](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/architecture/index.md)
and [graph-link guide](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/core-concepts/graph-links.md)
describe that boundary.

The graph is an application graph: its vertices and edges express work and
other domain relations. It is not the network graph through which packets
travel. A Beads `Link` or dependency may constrain task order; it does not
name a TCP connection, IP route, or Dolt remote.

Beads already has row-version compare-and-swap on selected write paths. The
[`bd` update command](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/cmd/bd/update.go)
passes `--if-revision` into guarded issue operations;
[`CheckVersionInTx`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/issueops/version.go)
checks `row_lock` in the same transaction as the write, and the Dolt and
embedded-Dolt stores use that check in their `UpdateIssueChecked` paths
([Dolt](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/issues.go),
[embedded Dolt](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/embeddeddolt/issues.go)).
The CLI intentionally limits which edits `--if-revision` guards; for example,
label and parent edits are outside that guarded update path
([`update_input.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/cmd/bd/update_input.go)).
Separate R16/R17 conformance scaffolding for a broader opaque-address,
whole-state expected-revision contract still has nil fixture hooks and skipped
cases ([contract](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/backend/conformance/expected_revision_contract.go),
[`Dolt test wiring`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/expected_revision_contract_test.go)).
That gap does not mean Beads lacks row-version CAS; it means the broader
cross-backend contract is not established by those skipped tests. The linked
implementation and tests were inspected but not run here. The important
synthesis is that BDP's whole-resource `expectedRevision` cannot be served by
exposing `row_lock` alone: labels and parents are outside the guarded CLI
update path, and R16-c is explicitly expected to fail once a real backend
wires compare-and-swap. The BDP `bd` adapter therefore hashes a projected
read resource and does not provide a conditional write. This is a coverage
gap, not evidence that Beads' selected row-version guards are absent.
The current BDP `bd` adapter instead derives its opaque read revision by
hashing the canonical projected Resource; the shared public Read-profile
handler accepts only GET and HEAD. That adapter therefore does not expose
Beads' `row_lock` as a revision or prove an end-to-end conditional BDP write
([revision projection](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/adapter-bd/src/index.ts),
[server method boundary](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/server/src/index.ts)).
BDP's pinned source has a separate private transaction store whose tests
exercise revision-guarded updates in that store
([transaction-store tests](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/server/src/transaction-store.test.ts)).
That private test implementation does not turn Beads' skipped hooks into a
working backend contract, nor does it establish that BDP's public transactional
server profile is complete; the pinned [status](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/STATUS.md)
still marks that serving work incomplete. A separate development runtime has
limited POST mutation routes, but its source labels it non-attesting and
loopback-only; it is not the public Read profile or evidence of a completed
public transactional implementation
([development runtime](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/server/src/development-runtime.ts)).

The distinctions can be stated compactly:

| Layer | Main question | Example |
| --- | --- | --- |
| Storage | Where are records represented? | Git objects; Dolt tables/chunks |
| Version control | Which durable state follows which? | Git/Dolt commits and refs |
| Synchronization | How are committed states exchanged? | `git fetch`; `dolt pull` |
| Database access | How are rows queried or changed now? | SQL over a Dolt server |
| Application semantics | What do records and relations mean? | Beads issues and dependencies |
| Protocol interface | How does a client address generic resources? | BDP HTTP/JSON |
| Network routing | How do packets reach a host and listener? | IP routing and TCP ports |

### Beads' native HTTP backend

The closest existing competitor to BDP is Beads' own experimental HTTP
backend, exposed through `bd serve` and selected by `bd connect`. The backend
is Beads-specific: its OpenAPI surface carries issue, dependency, query,
claim, close, batch, and other domain operations, with capability discovery
and typed `problem+json` errors. The [Beads HTTP backend
documentation](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/README.md#http-backend-experimental)
describes the client setup and its deliberate divergence from local mode:
some operations are deliberately refused, and some response shapes degrade
with documented behavior differences.
That is a different boundary from BDP's generic Bead/Link resources: a BDP
Type Descriptor cannot add an operation, while Beads' API can expose domain
operations such as `issues.advanceMolecule`.

This comparison preserves the source-date boundary. The original Beads study
is pinned at `b630f96`; the dated upstream snapshot recorded PR #7513 before
it merged. The [merged PR #7513](https://github.com/gastownhall/beads/pull/7513)
landed on 2026-10-12 and routes molecule reads, auto-close, parent creation,
and `close --continue` through shared `issueops` roles. It adds capability
tokens and a served conformance path, but it remains Beads behavior, not BDP
conformance. The chapter does not rewrite the historical source account as if
it had inspected the post-merge tree.

The server boundary also has an operational cost. PR
[#7518](https://github.com/gastownhall/beads/pull/7518) reports `bd show` at
10.2–10.8 seconds over a 0.24-second round trip versus 0.17 seconds beside
the database, with 24–48 SQL statements per command. These are reported SQL
server-mode measurements, not HTTP measurements; the PR says HTTP latency is
unmeasured. Running `bd` beside the database over SSH is the headline
workaround, with a same-region server as an alternative. The figures support
an operational question, not a claim that another API fixes latency.

The BDP adapter has a separate scale boundary: it builds a snapshot from one
`bd list --all --limit 0` call, caches it for one second, caps the output at
4,000,000 bytes, and returns 503 beyond that limit. A contributor-reported
13,635 identities in the Beads tracker suggests a possible real workspace
pressure point, but neither that size nor failure threshold was run here.
This is adapter evidence and a hypothesis about scale, not an observed
record-count failure.

The comparison yields a provisional recommendation: BDP is not yet justified
as a replacement for Beads' native HTTP backend. Beads already has a
domain-oriented, capability-discovering HTTP path with active conformance
work. It is not a byte-for-byte local-mode mirror: deliberate refusals and
documented degradation remain part of its contract. BDP's independent
interoperability value is still mostly
prospective and its public Read+Update, Transactional, and History serving
remains incomplete at the pinned status. Revisit BDP when Read+Update and
conditional whole-resource revisions are served by an independent
implementation, with measured HTTP behavior and a demonstrated client need
that Beads' domain API cannot meet. This recommendation is interpretation,
not a claim that BDP has no eventual value.

## BDP: a generic Bead/Link interface

BDP (the pinned draft's “Bead Protocol”) is a proposed HTTP/JSON protocol for
reading and mutating generic Beads and Links. Its draft specification defines
common resource operations,
nominal types and JSON-valued properties, capability discovery, conditional
updates using opaque revision values, and optional history and higher-level
profiles. The [normative draft at the pinned source commit](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/specs/bdp.md)
is still marked draft; schema presence does not establish that an endpoint
implements or advertises a capability.

The [reference architecture](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/design/architecture.md)
separates protocol values, client, HTTP server, adapters, and black-box
conformance. It includes a deterministic test adapter and a `bd`-backed
adapter. The adapter seam is important: BDP aims to describe resources at an
application boundary rather than expose Dolt tables or assume every store is
relational.

The reference server defaults to port 8080, configurable through
`BDP_SERVER_PORT`; this is a deployment setting rather than part of the wire
protocol. See the pinned [configuration source](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/config/src/index.ts)
and [startup configuration design](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/design/startup-configuration.md).

BDP also separates authentication from carried attribution. In its draft,
the authenticated principal is an input to authorization, not protocol data;
BDP v0 does not expose an authority-attested actor in Resource records.
`revisionProvenance` may carry writer-supplied attribution, but it is data,
not evidence that an authority verified the actor. See the draft's
[actor-attribution](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/specs/bdp.md#actor-attribution)
and [carried-attribution](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/specs/bdp.md#carried-attribution)
sections. Transport authentication and identity are deployment concerns in
this draft: the authority receives a principal for authorization, but the
resource contract does not carry that principal or standardize its identity
and delegation semantics. Actor attestation remains outside the v0 contract.

The evidence is profile-specific. At the pinned commit,
[`STATUS.md`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/STATUS.md)
reports Read-profile observations, but those runs are `claimEligible: false`
by construction, use 11 self-certified case definitions, and target two
BDP-authored implementations. Read+Update server work and
Transactional serving remain incomplete; History has client-side behavior
and a controlled walkthrough but no complete History server/conformance
claim. The [Read demo](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/read-demo.md)
uses the actual client against two servers. The
[History demo](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/history-client-demo.md)
uses the actual SDK with controlled HTTP fixture responses; it explicitly
does not show Beads serving retained History. These are useful implementation
and evidence boundaries, not interchangeable proof.

The 2026-10-12 upstream snapshot also had five open BDP PRs. The most
substantive was [draft PR #60](https://github.com/gastownhall/bdp/pull/60), a
documentation-only Type design with unresolved wire and product choices;
[#85](https://github.com/gastownhall/bdp/pull/85) tracks those seams without
accepting them. The remaining open changes covered protocol naming and blog
drafts. None should be read as merged protocol behavior.

What does BDP add beyond Git, Dolt, DoltHub, and Beads? Its strongest
potential contribution is a uniform resource-level contract: independent
clients can use shared Bead/Link representations, conditional revisions,
discovery, and standardized HTTP errors without implementing a Dolt remote
client or depending on a particular Beads CLI. That is distinct from moving
database commits. The available evidence does not yet show that all profiles
are deployed across independent implementations, or that a second protocol is
needed for every existing Beads use case. The design should be judged by
interoperability actually gained and by the extra profile, identity, and
conformance obligations it creates.

## Federation, revisions, provenance, and history

Beads describes federation as separately stored workspaces exchanging Dolt
history through configured peers. Its
[federation guide](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/multi-agent/federation.md)
lists hosted, cloud, local, HTTPS, SSH, and Git-style remote forms. This
combines Beads records with Dolt synchronization; it is not SQL query access
and it is not BDP's HTTP resource API. In the pinned source, federation tests
cover configuration, local history/state, cleanup, and graceful failures for
missing peers. The push/pull tests do not exercise a live remote, as their
comments explicitly note
([federation tests](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/federation_test.go)).
The implementation routes operations through Dolt SQL procedures or a Dolt
CLI subprocess, depending on remote type and environment
([`federation.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/federation.go)).
A route test successfully pushes and pulls a local `file://` remote through
SQL ([`route_logging_test.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/route_logging_test.go));
the CLI route test deliberately targets a nonexistent `git+file://` remote and
only verifies route selection and failure handling
([`route_logging_integration_test.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/route_logging_integration_test.go)).
Thus local file-remote transfer has test evidence, while successful live
Git-over-SSH, HTTPS, DoltHub, and cloud-provider transfer remains unverified
in this source study. The tree also has an integration-tagged test that starts
a local Dolt SQL server with its Remotes API, configures a `doltremoteapi://`
peer, and checks that a fallback pull brings a row from the peer into the
local store ([integration test](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/storage/dolt/pull_branch_tracking_integration_test.go)).
That is source evidence for a loopback Remotes API test path, not a test result
from this study or evidence of a live hosted/cloud provider transfer.
Two same-day Beads PRs illustrate adjacent active work. Merged [#7513](https://github.com/gastownhall/beads/pull/7513)
routes additional molecule behavior through HTTP-facing issueops roles, while
[#7518](https://github.com/gastownhall/beads/pull/7518) remains an open,
docs-only change about remote SQL latency and running `bd` near the database.
Neither makes Beads' HTTP interface BDP or proves remote federation.

“History” has more than one meaning here. Dolt history is a database commit
graph. Beads events are application audit records. BDP resource revisions are
opaque tokens for versions of a particular Bead or Link, and BDP's optional
History surface describes retrieval of retained resource versions. They can
refer to related changes, but they are not the same identifier or history
store.

Provenance needs similar care. Beads issue
[#7510, “Provenance V2”](https://github.com/gastownhall/beads/issues/7510)
remains a proposal in the 2026-10-12 check. It recommends separating claims
about a resource revision from activity records about events around that
resource. BDP PR #65 merged a narrower `revisionProvenance` envelope for
Beads and Links; that field records supplied attribution/context and does not
authenticate the named actor. See the
[merged PR](https://github.com/gastownhall/bdp/pull/65) and the
[pinned BDP status](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/STATUS.md).

Radicle offers an in-the-wild comparison for layering. Its protocol guide
describes Git repository replication alongside gossip and a Noise XK peer
handshake. Its 2026-09-23 security disclosure says released node traffic was
not encrypted and peer authentication was broken, and announces replacement
of its custom Noise-based networking with iroh. The [guide](https://radicle.dev/guides/protocol)
and [disclosure](https://radicle.dev/2026/09/23/disclosure-of-vulnerability-in-network-protocol)
therefore preserve a gap between documented intent and deployed behavior;
they do not show that the Noise framework itself caused the flaws. Radicle
helps illustrate separate Git storage, application objects, identity, peer
discovery, and transport layers. It does not prove that Dolt, Beads, or BDP
needs the same design.

Noise can be useful when a purpose-built peer protocol benefits from explicit
control over handshake patterns and static-key presentation. That is a design
flexibility advantage, not a general security or performance win. TLS can also
use pre-shared keys or application-provisioned raw public keys, so direct key
pinning is not unique to Noise ([Noise patterns](https://noiseprotocol.org/noise.html#section-7.5),
[TLS 1.3 authentication](https://www.rfc-editor.org/rfc/rfc8446.html#section-4.4),
[TLS raw public keys](https://www.rfc-editor.org/rfc/rfc7250.html)). Neither
protocol makes a key a durable application identity by itself: the application
must define key-to-principal binding, continuity, rotation, and revocation.
Noise also leaves framing, negotiation, and trust bootstrap to the application;
TLS offers a broader standardized interoperability surface. The available
sources establish no blanket throughput, latency, security, or code-size
advantage for Noise over a correctly configured TLS implementation. Radicle's
disclosure is a useful warning that deployed behavior must be assessed
separately from intended handshake design.

## TLS migration and standards governance

TLS's future deserves continuing scrutiny of both algorithm choices and
standardization governance. In the [NSA and IETF
series](https://blog.cr.yp.to/index.html), D. J. Bernstein argues that
standalone post-quantum key agreement removes the classical hedge retained by
hybrid designs and alleges improper influence and suppressed technical
dissent. Those are the author's allegations and criticism, not findings
independently established here. The [series research
record](tls-standards-governance-research.md) preserves the nine dated
articles, acquisition identities, and reading limits.

The technical hedge is concrete. [RFC 10024 section
3](https://www.rfc-editor.org/rfc/rfc10024.html#section-3) adopts RFC 9954's
definition of a hybrid key exchange: combining algorithms so that security
can remain if at least one component remains secure. The RFC specifies TLS
1.3 groups combining
ML-KEM with ECDHE. Its [security
section](https://www.rfc-editor.org/rfc/rfc10024.html#section-6) is not a
blanket implementation guarantee: the analysis relies on the TLS 1.3
transcript, while implementations still need side-channel resistance and
cryptographically secure randomness. In particular, disclosure of ML-KEM
encapsulation randomness can affect an insecure shared RNG, so a hybrid does
not erase implementation or RNG risk.

Standalone [ML-KEM draft
11](https://www.ietf.org/archive/id/draft-ietf-tls-mlkem-11.html#section-5)
has a draft-header publication date of 2026-09-17 and intended status
Informational; the tracker records a 2026-09-16 revision date. The
[IETF tracker](https://datatracker.ietf.org/doc/draft-ietf-tls-mlkem/),
checked on 2026-10-12, records it as submitted to the IESG, in the IESG RFC
Editor queue, and awaiting a first RFC Editor. Its [IANA
section](https://www.ietf.org/archive/id/draft-ietf-tls-mlkem-11.html#section-6)
requests `Recommended: N` for the standalone groups. That dated registry
state is not evidence that ML-KEM is broken, and publication, registry
registration, general recommendation, and a deployment policy are separate
facts.

The governance criticism also needs a precise comparator. [RFC
7282](https://www.rfc-editor.org/rfc/rfc7282.html) describes rough consensus
as technical objections being considered and answered, or judged insufficient
to block progress; it rejects treating a majority count as the decision rule.
That governance description does not validate or refute Bernstein's
allegations. It explains why counts and procedural claims need their underlying
messages, responses, and decisions checked separately.

For future knowledge and provenance exchange, our architectural inference is
to record the implemented TLS version, negotiated key-agreement group,
fallback policy, endpoint-authentication policy, and relevant implementation
evidence rather than treating an “HTTPS” label as complete assurance. Key
agreement is distinct from peer authentication, and both are distinct from a
durable application record attributing a particular knowledge revision. The
[Noise specification's DH
choices](https://noiseprotocol.org/noise.html#section-12) are classical;
choosing Noise therefore provides no post-quantum guarantee, and RFC 10024's
TLS-specific hybrid analysis cannot simply be imported into a Noise handshake
or a provenance protocol. These are review implications, not a new BDP
requirement.

## Network paths and protocol boundaries

The diagram shows application protocols above TCP/IP and the network. Port
numbers identify service listeners at the transport layer; they are not IP
protocol numbers. IANA lists TCP as IP protocol number 6 and records service
ports separately. It registers `git` on TCP 9418, `ssh` on TCP 22, and
`mysql` on TCP 3306. BDP's reference configuration defaults to TCP 8080 but
allows a configured port; that project default is not an IANA registration.
The Beads use of 3307 is a documented default, not a dedicated IANA
registration. The pinned [federation guide](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/docs/multi-agent/federation.md)
and [`configfile.go`](https://github.com/gastownhall/beads/blob/b630f96f5bd231ff7aea78af0d47b6038f228d00/internal/configfile/configfile.go)
show that Beads federation can use a separate Dolt Remotes API listener.
Non-shared federation configuration can use port 8080, distinct from the
MySQL listener used for multi-writer access. The source checked here does not
establish a shared-server default that disables the Remotes listener, so that
claim is not made. Deployment mode and configuration determine whether and
where it listens. This is a Dolt synchronization
surface, not BDP's resource API; the defaults can conflict if both listeners
bind the same address on one host.
See the [IANA service-name/port registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
and [IP protocol-number registry](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml).

```text
 Application or synchronization entry point
   Git native protocol (git://)        TCP 9418  --\
   Git over SSH (ssh://)               TCP 22     --+--\
   Git over HTTPS                      TCP 443    --+   \
   Dolt SQL (MySQL wire)             commonly TCP 3306 --+    \
   Beads-managed Dolt SQL            commonly TCP 3307 --+     +--> TCP --> IP
   Dolt Remotes API (Beads federation)  often 8080 --+    /         |
   BDP HTTP/JSON resource API       configurable; default 8080 --+ /  v
   DoltHub hosted remote synchronization          --/   underlying
                                                         network path

   Embedded Dolt: in-process database calls; no TCP listener required.
   Beads-managed SQL can use an OS-assigned port when unconfigured.
   Beads federation's Remotes API port depends on mode and configuration.
   Dolt remotes may use SQL, Git, SSH, HTTPS, cloud storage, or local paths;
   DoltHub is hosted synchronization, not a local SQL listener.
```

Git's HTTPS endpoint and GitHub's REST API may share the HTTPS origin while
serving different protocols and operations. Likewise, a Dolt SQL listener
accepts database-protocol sessions, while DoltHub or another Dolt remote
receives commit synchronization. BDP is an HTTP application API with a
configurable listener; the protocol draft does not assign it a universal
port. Beads' Dolt Remotes API is a separate federation synchronization
surface with its own documented 8080 default. These defaults are independent
and may require separate bind addresses or port configuration when co-located.
No semantic Beads edge routes packets through this diagram.

## What the analogy establishes—and what it does not

The analogy helps a Git-literate reader transfer a few useful expectations:
both Git and Dolt version durable data, expose branches/merges, and synchronize
committed state with remotes. It stops being a literal equivalence at the
object model and query interface. Git's file trees are not SQL tables; Dolt
queries are not remote pulls; Beads' domain graph is not a network topology;
and BDP's HTTP/JSON resource operations are not Dolt's commit-transfer
protocol.

BDP is not yet justified as a replacement for Beads' native HTTP backend.
Beads now has a domain-oriented `bd serve`/`bd connect` path with capability
discovery and active served conformance, while BDP's independent
interoperability value remains prospective and its public Read+Update,
Transactional, and History serving is incomplete at the pinned status. A
reasonable revisit gate is an independently implemented Read+Update profile,
conditional whole-resource revisions that cover Beads' relevant mutations,
measured HTTP behavior, and a client need not met by Beads' domain API. This
is a provisional interpretation, not a claim that BDP has no eventual value.

A Git-specific agent protocol remains an open question: identify a real
missing operation after Git's object, ref, and transport interfaces are
considered, then compare the cost of a Git-only application protocol with a
generic resource interface such as BDP.

## Source map

The following map makes the relationships explicit. Arrows describe authored
evidence relationships; they are not output from an inference engine.

```text
Pro Git ---> analogy checklist <--- Dolt documentation
                    |
                    v
Beads source ---> this chapter <--- BDP source
                    ^
                    |
Noise framework ---> provenance analysis <--- Radicle guide + disclosure
                           ^
                           |
Beads proposal --partial realization--> BDP merged subset

Bernstein series --attributed criticism--> TLS warning
RFC 10024 --defines and qualifies--> TLS hybrid key agreement
ML-KEM draft 11 + tracker --dated status--> standalone ML-KEM review
RFC 7282 --distinguishes--> rough consensus from vote counting
TLS/Noise evidence --informs inference--> future knowledge/provenance exchange
key agreement --separate from--> peer authentication --separate from-->
durable provenance

this chapter --audited by--> claim coverage record
```

The proposal-to-subset relationship describes PR65's documented scope; the
Radicle comparison supplies a precedent and a limitation, not a dependency
of BDP. The links below identify each node and its source role:

- [Pro Git's server protocols](https://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols)
  grounds the familiar Git transports and object exchange.
- [Dolt's remote and SQL documentation](https://docs.dolthub.com/),
  [DoltHub](https://www.dolthub.com/), and the local
  [syllogism](syllogism.md) establish and test the database analogy.
- The accepted [Beads source study](source-reports/beads-source-study.md)
  links Dolt storage and synchronization to Beads application semantics.
- The accepted [BDP source study](source-reports/bdp-source-study.md)
  links those semantics to the proposed generic Bead/Link interface and its
  implementation evidence.
- [Beads issue #7510](https://github.com/gastownhall/beads/issues/7510)
  proposes provenance requirements; [BDP PR #65](https://github.com/gastownhall/bdp/pull/65)
  implements a narrower `revisionProvenance` envelope.
- [Radicle's protocol guide](https://radicle.dev/guides/protocol) is an
  in-the-wild layering precedent, qualified by its
  [security disclosure](https://radicle.dev/2026/09/23/disclosure-of-vulnerability-in-network-protocol).
- The [Bernstein series](https://blog.cr.yp.to/index.html) supplies
  attributed criticism; the local [TLS governance research](tls-standards-governance-research.md)
  records its nine acquired article identities and limits.
- [RFC 10024](https://www.rfc-editor.org/rfc/rfc10024.html) supplies the
  published TLS hybrid definition and security qualifications. The
  [standalone ML-KEM draft 11](https://www.ietf.org/archive/id/draft-ietf-tls-mlkem-11.html)
  and its [IETF tracker](https://datatracker.ietf.org/doc/draft-ietf-tls-mlkem/)
  supply dated publication and registry-status facts, while [RFC
  7282](https://www.rfc-editor.org/rfc/rfc7282.html) supplies the rough-
  consensus distinction.
- This [chapter](Beads-on-the-Server.md), its
  [Noise and provenance analysis](provenance-and-noise-research.md), and
  [TLS standards research](tls-standards-governance-research.md), plus
  [source-link coverage](source-link-coverage.md) record the comparison and
  unresolved questions. The map is authored navigation, not software
  inference.

The [knowledge-creation summary](knowledge-creation-summary.md) records which
findings were represented in Beads and the limits of those operations. This
chapter is research evidence rather than a normative protocol document.
