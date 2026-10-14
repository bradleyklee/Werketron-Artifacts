# Beads on the Server: Stage 1 Syllogism

Status: provisional research frame; not a statement of implemented behavior.
Date: 2026-10-11 (UTC)
This provisional frame was developed as part of the `LLM-0kc` research work
and is grounded in the pinned source studies included with this chapter.

## The starting analogy

The working hypothesis is:

    filesystem : Git :: database : Dolt

This is a rhetorical starting point, not a syllogism whose premises have been
established. It suggests that Git and Dolt can each version a different kind
of durable state, but it does not imply that they have the same object model,
history semantics, merge behavior, server boundary, or wire protocol. The
two source studies must test those differences before the analogy is used in
the chapter.

The notation below uses these labels:

- **H** — provisional hypothesis or candidate mapping.
- **Q** — question that remains open.
- **V** — claim that requires primary-source verification.
- **I** — interpretation to be tested, not an implementation conclusion.

Every mapping in the layer checklist below is provisional.

### Storage

- **H (provisional mapping):** Filesystem state corresponds to database
  state; Git and Dolt operate on their respective state domains.
- **V:** What is the actual unit of storage and identity in each system? Does
  either system version only a projection rather than the whole store?

### Versioning

- **H (provisional mapping):** Git history and Dolt history provide analogous
  revisions for their state domains.
- **V:** Are commits, branches, merges, ancestry, conflicts, and revision
  guards equivalent enough for this comparison? Which behaviors are documented
  and which are implemented?

### Synchronization

- **H (provisional mapping):** Git fetch/push and Dolt pull/push may both
  synchronize revisions between locations.
- **V:** Do they exchange the same kind of object, use the same negotiation
  model, or have the same remote and conflict semantics? Do not equate
  synchronization with query access.

### SQL/database access

- **H (provisional mapping):** A Dolt database may be accessed through
  embedded APIs or a SQL server, whereas ordinary Git access is not
  database-query access.
- **V:** Which access modes actually exist in the pinned Beads/Dolt study, and
  how are SQL queries separated from Dolt revision synchronization?

### Beads application semantics

- **H (provisional mapping):** Beads adds domain entities and relationships
  above a versioned database.
- **V:** Which entities, constraints, revisions, transactions, and graph
  operations are implemented by Beads rather than inherited from Dolt?

### BDP transport/interface semantics

- **H (provisional mapping):** BDP may define a portable interface for
  Bead/Link operations over a transport.
- **Q:** Is BDP normative protocol text, an implemented service, a
  demonstration, or a mixture? Which operations, identities, errors,
  transactions, and transports are actually specified or tested?

### Semantic graph traversal

- **H (provisional mapping):** Beads links and traversal concern meaning in an
  application graph.
- **V:** What traversal operations exist, and what evidence shows their
  semantics? They must not be described as network routing merely because
  both use words such as link or path.

### Network routing

- **H (provisional mapping):** Network paths carry requests between clients
  and services.
- **V:** Which protocol and endpoint boundaries are real? What is
  configurable, what is a default, and what evidence distinguishes a service
  port from an IP protocol number?

## What the hypothesis does and does not say

The analogy may help a Git-familiar reader ask how durable relational state is
stored, revised, and exchanged. It does not establish any of the following:

- that a database is a filesystem, or that Dolt's model is Git's model;
- that a Dolt SQL query is a Dolt pull or push;
- that Beads' application graph is the same thing as a revision graph or a
  network graph;
- that BDP is required for Beads, is implemented everywhere, or replaces an
  existing interface; or
- that a useful Git analogy automatically creates a need for a new protocol.

These are negative constraints on the later chapter, not verified findings.

## Questions about what BDP may add

Treat each item as an open question until the BDP source study supplies exact
source, schema, test, or fixture evidence.

1. Does BDP add a transport-neutral interface for generic Bead and Link
   operations, or mainly document an existing application's API?
2. Does it define identity, revisions, history, optimistic concurrency,
   transactions, errors, or federation beyond what Beads and Dolt already
   expose? If so, which parts are normative, implemented, tested, or merely
   proposed?
3. Does its generality enable clients or servers that are not Beads/Dolt, and
   what interoperability evidence demonstrates that benefit?
4. What problem is solved by putting an interface boundary above application
   semantics: independent clients, remote services, federation, automation,
   or something else? What complexity or loss of native semantics does it
   introduce?
5. Does BDP use HTTP/JSON or another transport as an implementation choice,
   a protocol requirement, or only an example? Are network routing and
   semantic links explicitly kept separate?

The answer to “what BDP adds” must therefore be a source-classified result,
not an inference from the name or from the analogy.

## Is a Git-specific agent protocol justified?

This frame leaves a future Git-specific agent protocol undecided. The source
studies and later synthesis should ask:

- What agent operations are missing after ordinary Git object, ref, and
  transport interfaces are considered?
- Would an agent protocol expose repository intent, work items, review state,
  provenance, or semantic links that Git intentionally does not model?
- Would that be a Git-specific application layer, a general protocol that can
  use Git as one backend, or merely a client convention?
- Is the additional protocol justified by observed interoperability needs and
  tests, or only by an attractive analogy with BDP?
- Can the proposed boundary preserve Git's existing history and transport
  semantics without claiming that semantic graph traversal is routing?

No protocol proposal should be promoted from these questions without a
demonstrated use case, a precise boundary, and primary-source evidence.

## Verification checklist for the dependent studies

### BDP source study

- Pin the exact commit and inventory every tracked path.
- Read repository instructions and documentation conventions.
- Classify normative specification, design/research notes, implemented
  packages/apps, schemas, fixtures, tests, demos, and unmerged work
  separately.
- For each BDP operation, record whether it is specified, implemented,
  demonstrated, tested, or unresolved; include exact path/section/commit
  evidence.
- Resolve the questions above about identity, links, revisions, history,
  transactions, federation, transport, and network boundaries.

### Beads source study

- Pin the exact commit and inventory every tracked path separately from BDP.
- Read repository instructions and documentation conventions.
- Trace the actual data model, Dolt integration, refs/data behavior, sync
  mechanisms, CLI/server/embedded modes, links, federation, revisions, and
  history through source and tests.
- Distinguish implemented behavior from documentation claims, demonstrations,
  proposals, and active unmerged work.
- Test the boundaries: Dolt history versus source branches; synchronization
  versus SQL; Beads graph semantics versus transport; and federation/history
  versus ordinary revision behavior.

### Primary-source checks for the later chapter

The following are exact claims to verify, not claims made by this artifact:

- Git's object, ref, history, and transport behavior, including any default
  ports or alternative remotes, against the Git documentation and source.
- Dolt's storage, versioning, pull/push, SQL-server, embedded, and DoltHub
  behavior against official Dolt/DoltHub documentation and source.
- MySQL wire-protocol claims against the protocol documentation, including
  whether a cited port is a convention rather than a protocol identity.
- IANA service-port and IP-protocol claims against the relevant registries;
  do not infer registration from a product's default port.
- GitHub hosting/API claims against GitHub's official documentation, keeping
  them distinct from Git transport and from DoltHub.
- Any BDP and Beads statement against the pinned repositories' exact source,
  tests, fixtures, and dated active-work evidence.

## Stop boundary

This artifact completes only the Stage 1 framing task. It intentionally does
not inspect upstream repositories, assert their current behavior, write the
research chapter, export findings into Beads, create memory, or propose a
protocol design. The next two workers should use this checklist to produce
independent, commit-pinned source accounts before any synthesis.
