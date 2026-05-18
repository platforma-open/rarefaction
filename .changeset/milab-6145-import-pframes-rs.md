---
"@platforma-open/milaboratories.rarefaction.workflow": minor
---

MILAB-6145: import `@platforma-sdk/workflow-tengo:pframes-rs` from the workflow.

This pulls the upstream `@milaboratories/pframes-rs-wasip2` wasm bytes into
the compiled `main.plj.gz` via the SDK's opt-in `:pframes-rs` lib. Functional
use of the wasm component is a follow-up — for now the import opts the block
into the wasm bundling pipeline so the build flow can be exercised
end-to-end.
