# @platforma-open/milaboratories.rarefaction.model

## 2.1.1

### Patch Changes

- d1a5f92: Migrate onto the block-tools structurer (tool-managed layout: oxlint/oxfmt,
  ts-builder, regenerated configs) and bump the SDK to latest (model/ui-vue
  1.79.15, workflow-tengo 6.6.3, tengo-builder 4.0.9, block-tools 2.11.1). No block
  behavior change — the model was already on BlockModelV3.

## 2.1.0

### Minor Changes

- 85a7c32: Migrate block to BlockModelV3. Unified `BlockData` (UI-shaped persistence); `.args` lambda derives the workflow-visible shape and validates by throw. Persisted V1 state preserved via `DataModelBuilder.upgradeLegacy`. UI bindings move to `app.model.data`; `defineApp` → `defineAppV3`.

  `defaultBlockLabel` is no longer stored: the UI snapshots `datasetLabel` into `data` on the dataset-picker gesture, and `.subtitle` composes the label from data. Existing projects keep `customBlockLabel`; the dataset-name fragment of the default label is reseeded on the next interaction with the dataset dropdown. The unused `numRules` field (an array of validator functions that never serialized) is dropped from the model.

## 2.0.1

### Patch Changes

- 60ead39: Remove telegram

## 2.0.0

### Major Changes

- 654a905: Support peptides

## 1.3.4

### Patch Changes

- 64ccb8d: Fix build for new SDK: update ts-builder CLI usage, remove removed style imports
- 1573d0e: Update SDK dependencies to latest versions

## 1.3.3

### Patch Changes

- 770f778: Show warning when selected dataset contains no clonotypes

## 1.3.2

### Patch Changes

- ab9a4ca: Optimized rarefaction computation performance and added periodic execution logs that propagate to the UI GraphMaker component.

## 1.3.1

### Patch Changes

- 778acaf: Fix initial block state, remove workflow exports, improve block subtitle generation

## 1.3.0

### Minor Changes

- f1908f9: Support custom block title and running status

## 1.2.3

### Patch Changes

- 8e56508: Show running state for tables and graphs

## 1.2.2

### Patch Changes

- a262b52: technical release
- 391913b: technical release
- 811e16f: technical release
- eb49134: technical release

## 1.2.1

### Patch Changes

- 8c2a02a: Full SDK update

## 1.2.0

### Minor Changes

- 56727cb: Added extrapolation viz

## 1.1.0

### Minor Changes

- ee66f9a: Extrapolation

## 1.0.1

### Patch Changes

- 211c5f4: Release
