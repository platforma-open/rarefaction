import type { PlRef } from "@platforma-sdk/model";

/**
 * This block's init-params contract — the shape a block of this kind receives
 * at creation, and exactly what a project template serializes for it: which
 * dataset the curves are drawn from, the knobs that decide what gets computed,
 * and the naming shown on the block.
 *
 * Every field is optional. A block with no dataset picked is an ordinary state
 * the UI reaches, so export has to be able to write it and apply has to be able
 * to take it back; a contract that demanded `datasetRef` would make export and
 * apply stop being inverses. Whether a configuration is runnable is settled by
 * the model's `args` lambda, not here.
 *
 * `tableState` and `graphState` are absent: they are view state, which the
 * projection never hands out.
 */
export type BlockParams = {
  // Input wiring — a PlRef a template engine fills from an earlier entry's output.
  datasetRef?: PlRef;

  // Analysis configuration — the recipe a template exists to reproduce.
  numPoints?: string;
  numIterations?: string;
  extrapolation?: boolean;

  // Per-process resource limits — a deliberate user choice, set in the block's
  // advanced settings, and part of the recipe a template reproduces. A block
  // created without a template takes the model's defaults instead.
  mem?: number;
  cpu?: number;

  // Display naming.
  datasetLabel?: string;
  customBlockLabel?: string;
};
