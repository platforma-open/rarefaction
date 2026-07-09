import type { GraphMakerState } from "@milaboratories/graph-maker";
import type { PlDataTableStateV2, PlRef } from "@platforma-sdk/model";

/** Unified V3 data: persisted state shaped on the UI's terms. */
export type BlockData = {
  customBlockLabel: string;
  datasetRef?: PlRef;
  /**
   * Human-readable label of the chosen dataset, snapshotted by the UI in the
   * same gesture that picks `datasetRef`. Consumed by `.subtitle` so the
   * default label can be derived without re-querying the result pool there.
   */
  datasetLabel?: string;
  numPoints: string;
  numIterations: string;
  extrapolation: boolean;
  mem: number;
  cpu: number;
  tableState: PlDataTableStateV2;
  graphState: GraphMakerState;
};

/** Projected args consumed by the workflow. */
export type BlockArgs = {
  datasetRef: PlRef;
  numPoints: string;
  numIterations: string;
  extrapolation: boolean;
  mem: number;
  cpu: number;
};

/** Pre-V3 args shape, frozen snapshot for `upgradeLegacy`. */
export type LegacyBlockArgs = {
  defaultBlockLabel: string;
  customBlockLabel: string;
  numPoints: string;
  numIterations: string;
  extrapolation: boolean;
  mem?: number;
  cpu?: number;
  datasetRef?: PlRef;
  // V1 also carried a `numRules: ((num: string) => boolean | string)[]` field
  // whose value (an array of functions) could not be persisted; nothing in the
  // UI ever read it, so it is intentionally absent here.
};

/** Pre-V3 UI state shape, frozen snapshot for `upgradeLegacy`. */
export type LegacyBlockUiState = {
  tableState: PlDataTableStateV2;
  graphState: GraphMakerState;
};
