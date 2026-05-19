# @platforma-open/milaboratories.rarefaction

## 2.1.0

### Minor Changes

- 85a7c32: Migrate block to BlockModelV3. Unified `BlockData` (UI-shaped persistence); `.args` lambda derives the workflow-visible shape and validates by throw. Persisted V1 state preserved via `DataModelBuilder.upgradeLegacy`. UI bindings move to `app.model.data`; `defineApp` → `defineAppV3`.

  `defaultBlockLabel` is no longer stored: the UI snapshots `datasetLabel` into `data` on the dataset-picker gesture, and `.subtitle` composes the label from data. Existing projects keep `customBlockLabel`; the dataset-name fragment of the default label is reseeded on the next interaction with the dataset dropdown. The unused `numRules` field (an array of validator functions that never serialized) is dropped from the model.

### Patch Changes

- Updated dependencies [85a7c32]
  - @platforma-open/milaboratories.rarefaction.model@2.1.0
  - @platforma-open/milaboratories.rarefaction.ui@2.1.0

## 2.0.1

### Patch Changes

- 60ead39: Remove telegram
- Updated dependencies [60ead39]
  - @platforma-open/milaboratories.rarefaction.model@2.0.1
  - @platforma-open/milaboratories.rarefaction.ui@2.0.1
  - @platforma-open/milaboratories.rarefaction.workflow@2.0.1

## 2.0.0

### Major Changes

- 654a905: Support peptides

### Patch Changes

- Updated dependencies [654a905]
  - @platforma-open/milaboratories.rarefaction.workflow@2.0.0
  - @platforma-open/milaboratories.rarefaction.model@2.0.0
  - @platforma-open/milaboratories.rarefaction.ui@2.0.0

## 1.0.19

### Patch Changes

- 1573d0e: Update SDK dependencies to latest versions
- Updated dependencies [64ccb8d]
- Updated dependencies [0075c7e]
- Updated dependencies [1573d0e]
  - @platforma-open/milaboratories.rarefaction.model@1.3.4
  - @platforma-open/milaboratories.rarefaction.ui@1.3.4
  - @platforma-open/milaboratories.rarefaction.workflow@1.1.9

## 1.0.18

### Patch Changes

- Updated dependencies [770f778]
  - @platforma-open/milaboratories.rarefaction.workflow@1.1.8
  - @platforma-open/milaboratories.rarefaction.model@1.3.3
  - @platforma-open/milaboratories.rarefaction.ui@1.3.3

## 1.0.17

### Patch Changes

- ab9a4ca: Optimized rarefaction computation performance and added periodic execution logs that propagate to the UI GraphMaker component.
- Updated dependencies [ab9a4ca]
  - @platforma-open/milaboratories.rarefaction.model@1.3.2
  - @platforma-open/milaboratories.rarefaction.ui@1.3.2
  - @platforma-open/milaboratories.rarefaction.workflow@1.1.7

## 1.0.16

### Patch Changes

- 251ffa6: SDK Update

## 1.0.15

### Patch Changes

- c66bfe6: Update SDK

## 1.0.14

### Patch Changes

- Updated dependencies [778acaf]
  - @platforma-open/milaboratories.rarefaction.workflow@1.1.6
  - @platforma-open/milaboratories.rarefaction.model@1.3.1
  - @platforma-open/milaboratories.rarefaction.ui@1.3.1

## 1.0.13

### Patch Changes

- Updated dependencies [f1908f9]
  - @platforma-open/milaboratories.rarefaction.model@1.3.0
  - @platforma-open/milaboratories.rarefaction.ui@1.3.0

## 1.0.12

### Patch Changes

- 8e56508: Show running state for tables and graphs
- Updated dependencies [8e56508]
  - @platforma-open/milaboratories.rarefaction.workflow@1.1.5
  - @platforma-open/milaboratories.rarefaction.model@1.2.3
  - @platforma-open/milaboratories.rarefaction.ui@1.2.5

## 1.0.11

### Patch Changes

- c3d0cdb: Block metadata updated.

## 1.0.10

### Patch Changes

- Updated dependencies [602e87e]
  - @platforma-open/milaboratories.rarefaction.workflow@1.1.4

## 1.0.9

### Patch Changes

- a247a45: Update SDK

## 1.0.8

### Patch Changes

- Updated dependencies [4750a61]
  - @platforma-open/milaboratories.rarefaction.ui@1.2.4

## 1.0.7

### Patch Changes

- Updated dependencies [f1cf90d]
  - @platforma-open/milaboratories.rarefaction.workflow@1.1.3

## 1.0.6

### Patch Changes

- Updated dependencies [695b238]
  - @platforma-open/milaboratories.rarefaction.ui@1.2.3

## 1.0.5

### Patch Changes

- a262b52: technical release
- 391913b: technical release
- 811e16f: technical release
- eb49134: technical release
- Updated dependencies [a262b52]
- Updated dependencies [391913b]
- Updated dependencies [811e16f]
- Updated dependencies [eb49134]
  - @platforma-open/milaboratories.rarefaction.model@1.2.2
  - @platforma-open/milaboratories.rarefaction.ui@1.2.2
  - @platforma-open/milaboratories.rarefaction.workflow@1.1.2

## 1.0.4

### Patch Changes

- Updated dependencies [8c2a02a]
  - @platforma-open/milaboratories.rarefaction.model@1.2.1
  - @platforma-open/milaboratories.rarefaction.ui@1.2.1
  - @platforma-open/milaboratories.rarefaction.workflow@1.1.1

## 1.0.3

### Patch Changes

- Updated dependencies [56727cb]
  - @platforma-open/milaboratories.rarefaction.workflow@1.1.0
  - @platforma-open/milaboratories.rarefaction.model@1.2.0
  - @platforma-open/milaboratories.rarefaction.ui@1.2.0

## 1.0.2

### Patch Changes

- Updated dependencies [ee66f9a]
  - @platforma-open/milaboratories.rarefaction.model@1.1.0
  - @platforma-open/milaboratories.rarefaction.ui@1.1.0
  - @platforma-open/milaboratories.rarefaction.workflow@1.0.2

## 1.0.1

### Patch Changes

- 211c5f4: Release
- Updated dependencies [211c5f4]
  - @platforma-open/milaboratories.rarefaction.workflow@1.0.1
  - @platforma-open/milaboratories.rarefaction.model@1.0.1
  - @platforma-open/milaboratories.rarefaction.ui@1.0.1
