# @platforma-open/milaboratories.rarefaction.kind

## 1.1.0

### Minor Changes

- d33fef1: Add the mandatory block kind and its init-params contract

  The block now declares a `kind/` package carrying its identity and its
  init-params contract — the fields a project template supplies to seed a new
  instance: `datasetRef`, `numPoints`, `numIterations`, `extrapolation`, `mem`,
  `cpu`, `datasetLabel` and `customBlockLabel`. The model consumes them in `init`
  and projects the same set back out via `templateParams`, so export and apply are
  inverses. Every field is optional and keeps a default, since a block may be
  created by hand rather than from a template.

  `tableState` and `graphState` stay out of the contract: they are view state, and
  a template that carried them would restore one user's scroll position onto
  another user's block.

  Also upgrades the SDK catalog to the current published versions.
