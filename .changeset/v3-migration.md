---
"@platforma-open/milaboratories.rarefaction.model": minor
"@platforma-open/milaboratories.rarefaction.ui": minor
"@platforma-open/milaboratories.rarefaction": minor
---

Migrate block to BlockModelV3. Unified `BlockData` (UI-shaped persistence); `.args` lambda derives the workflow-visible shape and validates by throw. Persisted V1 state preserved via `DataModelBuilder.upgradeLegacy`. UI bindings move to `app.model.data`; `defineApp` → `defineAppV3`.

`defaultBlockLabel` is no longer stored: the UI snapshots `datasetLabel` into `data` on the dataset-picker gesture, and `.subtitle` composes the label from data. Existing projects keep `customBlockLabel`; the dataset-name fragment of the default label is reseeded on the next interaction with the dataset dropdown. The unused `numRules` field (an array of validator functions that never serialized) is dropped from the model.
