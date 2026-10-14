# Export verification report

Checked: 2026-10-14

The curated directory and archive were checked for payload-hash consistency,
relative Markdown links, unsafe archive members, and sensitive patterns. The
check covered local paths, emails, session/thread UUIDs, usage-limit URLs,
transaction identifiers, hostnames, private-key markers, and common cloud-key
forms. No matches or broken relative links were found.

The scan is pattern-based and cannot establish that arbitrary prose contains
no sensitive information. Source commits and source inventories remain pinned;
source accounts are not new runtime tests.
