# Provenance, identity, and Noise: research note

Research captured 2026-10-12 for integration into “Beads on the Server.”
This note supplements the staged source studies; it does not change the pinned
SPEC or claim a BDP design decision.

## Finding

Noise is relevant to persistent peer identity only through application policy.
Its static-key handshake patterns can prove that a live peer possesses the
private key matching a presented static public key. Noise does not decide what
real-world or application identity that key represents, whether the key should
remain stable across sessions, or how a resource's authorship is durably
proven. The framework explicitly leaves peer-key acceptance to the application
and lists certificates, configured key lists, and remembered-key continuity as
possible approaches
([Noise §14](https://noiseprotocol.org/noise.html#section-14)).

Thus “a slow key that persists” is a useful intuition for some deployments,
but not a Noise guarantee. “Static” describes a key's role in a handshake
pattern; storage lifetime, identity mapping, continuity, rotation, revocation,
and recovery remain application responsibilities. Noise's `Rekey()` updates a
transport cipher state; it does not establish a durable identity or sign a
resource record
([Noise §11.3](https://noiseprotocol.org/noise.html#section-11.3)).

A Noise pattern with peer authentication can authenticate a session; the
`NN` pattern is unauthenticated ([Noise §7.2](https://noiseprotocol.org/noise.html#section-7.2)).
Neither establishes the truth of a provenance claim. Its handshake hash can be used for channel binding: an application may
sign it to bind an authentication token to that particular session. That is
not a signature over an arbitrary Bead, Link, Git commit, or source list
([Noise §11.2](https://noiseprotocol.org/noise.html#section-11.2)). The
framework also warns that a Noise static key pair should not be reused outside Noise
([Noise §14](https://noiseprotocol.org/noise.html#section-14)). A design needing
durable signed statements should therefore define a separate signing identity
or credential and an explicit binding from that signer to an application
principal.

## Where Noise can have an advantage over TLS

Noise's clearest advantage is design flexibility for a purpose-built secure
channel. Its handshake patterns make choices such as whether static keys are
known beforehand or sent during the handshake explicit. A protocol designer
can select a concrete pattern and primitive suite instead of adopting the
broader TLS handshake and extension model
([Noise handshake patterns](https://noiseprotocol.org/noise.html#section-7.5),
[Noise protocol names](https://noiseprotocol.org/noise.html#section-8)). This
can fit a peer-to-peer application with a defined peer-discovery and key
distribution mechanism, a narrow set of supported peers, and no need for web
PKI or general-purpose TLS interoperability.

That is a trade, not a general security or performance win. TLS 1.3 can use
PSKs, and TLS raw-public-key mode can use application-provisioned or pinned
keys, so “no central CA” is not unique to Noise. Noise also leaves framing,
protocol negotiation, trust/bootstrap, session termination, and other
application decisions to its users. The framework warns about rollback risks
in compound negotiation and asks applications to handle stream truncation
([Noise application responsibilities](https://noiseprotocol.org/noise.html#section-13)).
TLS has a standardized, widely deployed handshake and a larger general-purpose
interoperability surface; Noise's flexibility means the application must
select and integrate the pieces correctly.

The sources reviewed establish no blanket Noise advantage in throughput,
latency, code size, or security over a correctly configured TLS 1.3
implementation. Those claims need workload-specific benchmarks and
implementation review. A reasonable selection rule is: consider Noise when a
custom peer protocol benefits from explicit handshake-pattern control and can
own the associated trust, negotiation, and lifecycle rules; prefer TLS when
standard interoperability, conventional service certificates, and broad
implementation support are primary. Neither choice establishes that an
endpoint's software is honest or creates durable provenance for its data.

## TLS and Noise are not inherently opposing trust models

The “customer” versus “neighborhood” contrast is useful as a description of
two deployment choices, but it should not be assigned to TLS and Noise as an
intrinsic property of either protocol.

The familiar TLS web deployment uses CA-issued certificates to bind a service
name to a public key. TLS 1.3 also supports PSK-based authentication, and it
can carry raw public keys instead of X.509 certificates
([TLS 1.3, authentication](https://www.rfc-editor.org/rfc/rfc8446.html#section-4.4),
[RFC 7250](https://www.rfc-editor.org/rfc/rfc7250.html)). With raw keys, the
application must supply an out-of-band binding between the key and the entity.
That can be a preconfigured or pinned key, so TLS can support direct peer
continuity without relying on a public CA. Certificate expiration limits the
certificate's validity; it does not inherently prevent a stable identity or
key from continuing across renewed certificates.

Noise makes static-key handshake patterns available, but does not require
long-lived key storage or a central-authority-free trust model. Its own
guidance says applications may accept keys through certificates, configured
key lists, or remembered-key continuity. The application still has to bootstrap
trust, bind keys to principals, and decide what rotation or revocation means
([Noise §14](https://noiseprotocol.org/noise.html#section-14)). A deployment
can therefore use Noise with centrally certified keys, just as it can use TLS
with directly pinned keys.

Neither a Noise handshake nor TLS proves that a peer's software is honest or
that a remote server executed a particular program faithfully. They establish
cryptographic properties of a communication session and its authenticated
keys. Remote code or platform attestation is a separate mechanism. Likewise,
session authentication is not durable authorship evidence: an attestation
about a Bead or Link version needs an explicitly defined signed claim, a
verifiable signer-to-principal binding, and rules for version binding,
freshness, revocation, and validation. Noise's optional channel binding binds
an application token to one handshake; it is not such a durable resource
attestation.

A more accurate report formulation is: “A common TLS deployment trusts a CA
to bind a service name to a key and protects traffic to that service. A
peer-to-peer application may instead use Noise with remembered static keys to
authenticate peers directly, without a public CA. Either protocol can support
other trust arrangements; neither by itself proves honest server execution or
the durable provenance of stored content.”

## Git precedent: Radicle, with a current security qualification

For the Git–Dolt–Beads–BDP syllogism, Radicle is an in-the-wild comparison
for layering and transport boundaries: it carries Git repository data through
a peer network. It is not evidence that Radicle implements Dolt, Beads, or
BDP, nor that those systems need the same transport.

Radicle is a concrete in-the-wild comparison for Git, application semantics,
and peer transport. Its protocol guide says Radicle incorporates Git's object
model and transfer protocol into a peer-to-peer network, and identifies peers
by Ed25519 Node IDs. The guide describes Noise XK with the Node ID as the
static key, with peers learning IDs through gossip before connecting
([Radicle protocol guide](https://radicle.dev/guides/protocol)).

That design description must be read alongside Radicle's security disclosure.
On 2026-09-23, Radicle reported that released node traffic was not encrypted
and peer authentication was broken, despite the guide's description of a
Noise-secured handshake. This is evidence of a gap between documented
protocol intent and deployed behavior; it does not establish that Noise itself
was responsible or that the deployed handshake correctly implemented Noise
XK. The report should preserve both claims and their different evidence
classes rather than summarizing Radicle as a successful example of secure
Noise transport. Radicle remains useful here because Git replication,
application-level social objects, peer discovery, signed repository data, and
the network transport are explicit, separable layers.

It is not a clean endorsement of the transport. On 2026-09-23 Radicle disclosed
confidentiality and peer-authentication flaws in its network transport, stated
that the issues did not let attackers forge Git objects or identities because
those are verified at the storage layer, and said it was replacing its custom
Noise-based networking protocol with iroh. The current guide removes its
transport-security section pending a resolution
([Radicle disclosure](https://radicle.dev/2026/09/23/disclosure-of-vulnerability-in-network-protocol)).
The available announcement says replacement is in progress; this note does not
claim that migration is complete. The example supports studying layer boundaries
and implementation-specific review, not attributing the disclosed flaws to the
Noise framework itself.

This answers “is Noise used with Git?” with a qualified yes: Radicle has used
Noise for its peer network while carrying Git repository data. It is not one of
Git's built-in remote transports, which are local, HTTP(S), SSH, and `git://`;
Git can also delegate other schemes to remote helpers
([Git transport protocols](https://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols),
[Git URL documentation](https://git-scm.com/docs/git-pull#_git_urls)). Git's
transfer protocol and a secure network channel are separable components; the
Radicle Git remote helper exposes the peer network to Git as a distinct
`rad://` transport
([Radicle quick start](https://radicle.dev/guides/quick-start)).

## Beads provenance proposal and implementation boundary

[Beads issue #7510](https://github.com/gastownhall/beads/issues/7510) publishes
the “Provenance V2” proposal and recommends two different records:

- **Revision provenance** describes a particular Bead or Link version: its
  attributed actor, commit time, optional agent/message, and proposed sources.
- **Activity provenance** records an event around a resource independently,
  such as a reported commit, handoff, or use. An Activity record has its own
  revision provenance, distinct from the actor said to have performed the
  activity.

The issue is explicitly broader than an adopted implementation. Its
2026-10-12 follow-up reports that BDP PR65 merged the common
`revisionProvenance` envelope, including `actor: {id, basis}` and the existing
time/context fields. It also states that source lists, completeness, Activity
records, terminal deletion versions, and CLI/query changes remain proposals.
The merged PR explicitly says grouping an actor with other fields does not
authenticate that actor
([BDP PR65](https://github.com/gastownhall/bdp/pull/65), [versioned proposal](https://github.com/gastownhall/bdp/blob/50e6b89620aeafea1f25836844ebd370b63ccccb/docs/design/provenance-on-resource-versions-proposal.md)).
The BDP default branch was at `caf5ca75a4e9b9c7865e61e97f849ab736c21e64`
when checked on 2026-10-12, after PR65 and PR83 were merged
([BDP commit](https://github.com/gastownhall/bdp/commit/caf5ca75a4e9b9c7865e61e97f849ab736c21e64)).

That distinction maps directly to the Noise question. A Noise-authenticated
connection could help a server establish which key controlled a session. It
would not, by itself, authenticate a writer-supplied `revisionProvenance.actor`,
prove that the actor authored the revision, verify cited sources, or establish
source-list completeness. Those require separate application-level identity
binding and evidence rules. Conversely, durable provenance does not require
Noise: a system may record attributable claims without authenticated transport,
provided it labels them honestly.

## Implications for the chapter and open questions

Place this comparison where the chapter discusses Beads provenance and then
revisit it in the network-boundary section. Preserve these distinctions:

1. **Peer authentication:** which public key controlled this connection?
2. **Principal binding:** why should that key be treated as a named person,
   service, or agent, and how are rotation and revocation handled?
3. **Revision provenance:** what actor, time, and source claims are stored with
   this exact version?
4. **Attestation:** which issuer cryptographically stands behind which exact
   claim, under what verification rules?

The chapter should ask whether BDP needs authenticated provenance, ordinary
writer-supplied provenance, or both for distinct use cases. It should not imply
that adding Noise solves authorship, provenance storage, or trust policy. It
should also note the concrete Radicle precedent and its current transport
security/migration status rather than presenting it as an unqualified model.

Suggested source-map edges:

```text
Noise framework --supports peer key possession--> secure channel
Noise framework --leaves trust mapping to--> application policy
Radicle --uses Git with Noise peer transport--> layered P2P case study
Radicle disclosure --qualifies--> current transport suitability
Beads issue #7510 --proposes--> revision + activity provenance
BDP PR65 --implements subset of--> revisionProvenance envelope
revisionProvenance actor --does not imply--> authenticated identity
authenticated session --does not imply--> durable content attestation
```

All issue/PR states and Radicle security status above are time-sensitive and
were checked on 2026-10-12. Recheck them when the complete source inventories
and chapter are assembled.
