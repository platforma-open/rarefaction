---
"@platforma-open/milaboratories.rarefaction": patch
---

Release graph-maker default palette fix. The prior release (074f69d) was lost to a CI race during a force-push on main: sub-package versions advanced but the block's dependency cascade bump never landed, leaving the block stranded at 2.1.0. This forces a clean block release picking up the already-bumped ui.
