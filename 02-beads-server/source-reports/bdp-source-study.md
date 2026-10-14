# BDP source study — verified worker finalization

Date checked: 2026-10-12 UTC

This report finalizes the supplied BDP source account for the bounded
`bdp-source-study` work order. Source acquisition and source-code inspection
were performed by the manager and Sol in a clean, isolated clone. This
worker verifies and finalizes the supplied research account. It does
not claim an independent full source-code review, a new clone, live PR checks,
runtime experiments, or execution of upstream tests.

## Reproducible source pin

Repository: <https://github.com/gastownhall/bdp>

Pinned commit: `caf5ca75a4e9b9c7865e61e97f849ab736c21e64`

Pinned tree:
<https://github.com/gastownhall/bdp/tree/caf5ca75a4e9b9c7865e61e97f849ab736c21e64>

The supplied [checkout manifest](bdp-source-checkout.json) records:

- commit date `2026-10-11T23:54:22-07:00`;
- an empty working-tree field;
- 552 tracked paths; and
- [bdp-tracked-paths.txt](bdp-tracked-paths.txt) with SHA-256
  `11965f2da0cbd92d8ea8a77f6ee541e5c3bf317623e1ce9f6b23364d09fbcdeb`.

The worker independently checked the supplied manifest and inventory in the
task snapshot. `wc -l` reports 552 lines and `sha256sum` reports the exact
manifest hash above. The inventory is newline-terminated and has no duplicate
path in the checked set. Its first entries are `.github/workflows/ci.yml`,
`.gitignore`, `.node-version`, `.npmrc`, and `.nvmrc`; its last entries are
`tsconfig.json`, `vitest.config.ts`, and `vitest.evidence.config.ts`. The
manifest says the source came from an isolated manager-side clone and that
worker egress was unavailable.

The supplied input artifacts were present in task input commit `39961958` and
were read for this finalization. Their hashes are:

| Input | SHA-256 |
| --- | --- |
| `bdp-source-study-manager.md` | `f09aad05603d0dc0f17c3e5db51ef43c4dcf5826eb0a24aeddd0c80b50631f73` |
| `bdp-source-checkout.json` | `daabbbdf8320dba5f6165a24de2812f5ae09fc05eb85ad98f9003104b6f5ef03d` |
| `bdp-tracked-paths.txt` | `11965f2da0cbd92d8ea8a77f6ee541e5c3bf317623e1ce9f6b23364d09fbcdeb` |
| `upstream-pr-snapshot-20261012.json` | `2e5e80f89d94bd54772cb7bb4b830e1565a82d6b93f86fe217b9b313250dfbc7` |
| `provenance-and-noise-research.md` | `28e95e035f04a19dc3b6a32ebb1c257e3ae3706bcedbfc9d88a49afeca061b73` |

This account is limited to the recorded source inventory and evidence; no BDP
clone, fetch, or network request was performed by this worker.

## Repository organization and instructions

The pinned root [`README.md`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/README.md)
describes BDP as a draft HTTP/JSON protocol for generic Bead and Link
operations. It identifies the draft specification, canonical schema,
Node/TypeScript reference clients and servers, black-box conformance suite,
and Read-profile evidence. The README says the specification is a draft and
is not a conformance target until adopted.

The tracked tree is organized around `apps/`, `packages/`, `docs/specs/`,
`docs/design/`, `docs/research/`, `fixtures/`, `schemas/`, and `scripts/`.
The pinned root has neither `AGENTS.md` nor `CONTRIBUTING.md`.
`CONTEXT.md` is a BDP glossary and wording guide, not a contributor contract.
The [design README](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/design/README.md)
states that design documents are non-normative and that the draft
specification governs conflicts. It organizes decisions by stable identifiers
and links requirements, architecture, packets, and evidence.

Root `package.json` records pnpm/Node version pins and build, boundary,
format, lint, test, typecheck, smoke, and evidence scripts. `STATUS.md` is the
maintainer's implementation/evidence status ledger. The complete path
inventory is the accompanying `bdp-tracked-paths.txt` file.

## Proposal, implementation, and evidence boundaries

The normative candidate text is
[`docs/specs/bdp.md`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/specs/bdp.md).
It describes HTTP resources for Beads and Links, typed properties, opaque
revision tokens, compare-and-swap mutation guards, capability discovery,
versioned reads, and optional history. Profiles are distinct: a schema member
does not by itself advertise a runtime capability.

The pinned [`STATUS.md`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/STATUS.md)
reports a Read profile with 89 observed passing rows and nine justified N/A
slots across two targets, with eight explicit qualifications. Read+Update has
client and component work but no complete served write-profile claim.
Transactional server capability is not claimed. Optional History has a Read
client and walkthrough, but no History server/adapter realization or
conformance evidence. These are separate classes of evidence:
specification, implementation, demonstration, and conformance result.

The source account classifies the supplied tree as follows:

- **Normative/proposed:** `docs/specs/bdp.md`, `schemas/bdp-v0.schema.json`,
  and the draft vocabulary around Beads, Links, profiles, revisions, and
  capabilities. The README and spec's draft status remain authoritative for
  the proposal boundary.
- **Implemented reference code:** `packages/server/`,
  `packages/adapter-bd/`, `packages/adapter-in-memory/`, `packages/client/`,
  `packages/config/`, `packages/conformance/`, and the `apps/` entries in the
  inventory. These are source evidence, not proof that every profile is
  served or interoperable.
- **Fixtures and tests:** package `*.test.ts` files, `fixtures/`, conformance
  matrices, sealed cohort evidence, and `scripts/*test*`. They establish the
  behavior their tests and bounded fixtures cover; they do not establish
  untested profiles or hosted-provider behavior.
- **Demonstrations:** `docs/history-client-demo.md` and related demo scripts
  show client/fixture behavior. A History walkthrough is not evidence of a
  Beads-backed History server.
- **Unmerged designs and editorial work:** `docs/design/`, `docs/research/`,
  and `docs/blog/` contain non-normative design, research, tracking, and blog
  material unless the pinned spec or status ledger says otherwise. Open PR
  content is not merged behavior.

## Focused mechanism-to-test map

This is a targeted crosswalk from the supplied source inspection, not a claim
that every tracked path or operation received line-by-line review.

| Mechanism or claim | Source evidence | Bounded conclusion |
| --- | --- | --- |
| Read HTTP server validates and dispatches requests | [`packages/server/src/index.ts`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/server/src/index.ts), [`index.test.ts`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/server/src/index.test.ts) | Tests cover validation-before-dispatch, identity policy, lifecycle, and the port seam. |
| `bd` adapter projects Beads resources | [`packages/adapter-bd/src/index.ts`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/adapter-bd/src/index.ts), [`index.test.ts`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/adapter-bd/src/index.test.ts) | Tests cover projection, dependency links, IDs, process boundaries, and revisions. |
| In-memory storage is a deterministic test implementation | [`packages/adapter-in-memory/src/index.ts`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/adapter-in-memory/src/index.ts), its tests | Repeatable protocol tests exist; this is not evidence of a second production storage system. |
| Read conformance is a bounded cohort artifact | [`STATUS.md`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/STATUS.md), [Read matrix](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/conformance/matrices/read-v1.json), [sealed evidence](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/design/evidence/read-cohort/read-v1.json) | The recorded cohort is bounded to named targets, rows, and qualifications; it was not rerun or resealed here. |
| History client checks controlled values | [`packages/client/src/history.test.ts`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/client/src/history.test.ts), [History walkthrough](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/docs/history-client-demo.md) | Client and fixture behavior do not demonstrate a Beads-backed History server. |
| Reference listener port is configurable | [`packages/config/src/index.ts`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/config/src/index.ts) | Source defines default 8080 and reads `BDP_SERVER_PORT`; this is deployment configuration, not protocol identity. |

The pinned Read request path can be followed from URL parsing to storage and
back. `GET` at the Scope and `bdp.json` routes through `createHttpHandler` and
the `read-request.ts` parser; handler tests cover discovery and service
description. Collection routes for `beads/`, `links/`, and `types/` apply
structural filters, ordering, identity, selectors, and continuation controls
where admitted by the profile. Resource routes support canonical identities
and property views. `GET beads/{id}?view=links` binds continuation state to
the request projection and identity. The relevant source is
[`packages/server/src/read-request.ts`](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/server/src/read-request.ts),
its [HTTP handler tests](https://github.com/gastownhall/bdp/blob/caf5ca75a4e9b9c7865e61e97f849ab736c21e64/packages/server/src/http-handler.test.ts),
and the adapter paths above.

The shared public Read-profile handler admits only GET and HEAD. A separate
development runtime contains limited POST mutation routes, but its source
labels it non-attesting and loopback-only; it is not the public Read profile.
Read+Update has client-side mutation and sequence code, while `STATUS.md` does
not claim a complete served write profile. Transactional serving and History
serving remain unclaimed. The trace above covers representative operation
families, not every conformance row.

## Dated upstream work

The supplied [upstream PR snapshot](upstream-pr-snapshot-20261012.json) records
a read-only GitHub API search checked on 2026-10-12. Its BDP `is:open` query
returned five PRs and preserves exact base/head commits and every changed path.
It is not a maintainer-worktree inventory and must be refreshed before
publication.

- [PR #85](https://github.com/gastownhall/bdp/pull/85) is open and adds two
  `docs/design/` tracking files for Type/CLI seams at PR60. It is a
  release-coordination record, not release acceptance.
- [PR #61](https://github.com/gastownhall/bdp/pull/61) is open and changes
  README, context, design-index, and spec naming. It is naming clarification,
  not protocol behavior evidence.
- [PR #60](https://github.com/gastownhall/bdp/pull/60) is open draft and
  changes 16 documentation/design files. Its type decisions and provenance
  material remain proposals; it does not establish merged runtime behavior.
- [PR #58](https://github.com/gastownhall/bdp/pull/58) is open and changes one
  blog file. It is an editorial supplement, not implementation evidence.
- [PR #57](https://github.com/gastownhall/bdp/pull/57) is open and changes one
  blog file. Its own description leaves HTTP writes and HTTP History ahead of
  the walkthrough, so it is not served-profile evidence.

The manager/Sol account also records that BDP PR #65 (revision provenance) and
PR #83 (Read-profile evidence reseal) were merged before the pinned commit,
while Beads issue #7510 remained open. The merged PR #65 subset must not be
expanded into the broader Provenance V2 proposal. The exact PR/issue state is
time-sensitive and is preserved in the supplied manager report and research
note; it was not rechecked live by this worker.

## Findings against the Stage 1 checklist

The supplied evidence supports this bounded account of the provisional
`filesystem : Git :: database : Dolt` comparison:

- BDP is an application-facing HTTP/JSON interface proposal above storage. It
  defines generic Bead and Link resources, capabilities, revisions, and
  profile boundaries; it does not turn an application graph into network
  routing.
- Its potential addition is a portable resource vocabulary and interface
  across adapters. The status ledger does not justify claiming that all
  profiles or operations are implemented or interoperable.
- BDP's resource revisions are distinct from storage-engine history and from
  Dolt commit synchronization. The storage engine remains an adapter concern
  in this source account.
- Capability negotiation is material: a schema member or documented profile
  does not prove that a deployed server advertises or serves it.
- Bead and Link relationships are application semantics. They are not packet
  routes, IP paths, or evidence of a network-routing algorithm.
- Read client behavior, in-memory tests, and a History walkthrough do not
  establish a complete write, transaction, or History server.

The first three bullets are synthesis interpretations from the pinned draft,
README, and status record, not additional normative BDP requirements. The
report does not answer whether a future Git-specific agent protocol is needed;
that remains an open interoperability question requiring an observed use case,
precise boundary, and primary-source evidence.

## Provenance, identity, and transport limits

The supplied [provenance and Noise research note](../provenance-and-noise-research.md)
is an integration input, not a change to the pinned BDP source account. It
records these distinctions for the later chapter:

- Noise can authenticate possession of a static key in a selected handshake,
  while application policy must bind that key to a principal and define
  continuity, rotation, revocation, and recovery.
- TLS can use certificates, PSKs, or raw/pinned public keys; Noise can use
  configured keys, certificates, or continuity pins. “Customer” and
  “neighborhood” are deployment archetypes, not inherent properties of either
  protocol.
- Neither TLS nor Noise proves honest code execution or durable authorship of a
  Bead or Link. A durable provenance claim needs separate signer identity,
  binding, version, freshness, and verification rules.
- Radicle is a layered Git/peer-transport comparison, not evidence that Beads,
  Dolt, or BDP requires Noise. Its 2026-09-23 transport disclosure belongs
  alongside its protocol-guide description and is not an unqualified security
  endorsement.

For Beads issue [#7510](https://github.com/gastownhall/beads/issues/7510), the
2026-10-12 account classifies revision-provenance and activity-provenance
records as an open proposal. BDP PR #65 supplies a merged subset around a
shared `revisionProvenance` envelope for Beads and Links. The subset does not
make source completeness, Activity records, terminal deletion versions, or
CLI/query changes an already-deployed Beads provenance system. An `actor`
field does not authenticate its actor merely by being present.

## Verification record and limitations

Worker checks completed:

1. Read the complete supplied manager report, checkout manifest, tracked-path
   inventory, dated upstream snapshot, and provenance/Noise note.
2. Confirmed the five input artifacts and all governing local inputs exist in
   the task snapshot; confirmed the input artifacts' SHA-256 values above.
3. Confirmed the checkout manifest's repository, pinned commit, commit date,
   empty working-tree field, path count, inventory path, and inventory hash.
4. Confirmed `wc -l` and `sha256sum` agree with the declared 552-path
   inventory, which is newline-terminated and duplicate-free.
5. Parsed the supplied JSON manifests and confirmed the BDP snapshot contains
   exactly five open PR records with the listed states and changed-file sets.
6. Checked the BDP account against the Stage 1 syllogism and the local
   `SPEC.md`/`PLAN.json` boundaries; no BDP source was cloned or fetched.

No upstream repository, branch, pull request, Beads database, canonical
memory, or network state was changed. No BDP build, conformance suite,
runtime experiment, or upstream test was run by this worker. The manager-side
account states that its source inspection did not run the BDP build or tests
because `node` and `pnpm` were unavailable there; its linked tests remain
source evidence rather than results produced in this work order.

This is a bounded, commit-pinned source account rather than line-by-line review
of all 552 paths. It does not establish hosted-provider success, complete
operation coverage, a complete write/transaction/History profile, maintainer-
local worktree state, current PR status after 2026-10-12, or runtime behavior
not directly recorded in the supplied evidence. Those limits must remain
visible in manager QA and later chapter synthesis.
