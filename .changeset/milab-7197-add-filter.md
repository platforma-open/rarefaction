---
"@platforma-open/milaboratories.rarefaction": minor
"@platforma-open/milaboratories.rarefaction.kind": minor
"@platforma-open/milaboratories.rarefaction.model": minor
"@platforma-open/milaboratories.rarefaction.ui": minor
"@platforma-open/milaboratories.rarefaction.workflow": minor
---

Update the SDK and accept a subset filter (e.g. a Repertoire Labeling label or Lead Selection picks) with the input dataset. The dataset list is built with buildDatasetOptions (requireEnrichments: false). The subset restricts the clonotypes before the curves are computed, so depths and unique counts describe the subset only. Curves of a subset run carry a trace rooted in the subset, and the default subtitle names it. Unfiltered runs are unchanged.
