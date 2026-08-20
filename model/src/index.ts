import type { InferOutputsType } from "@platforma-sdk/model";
import {
  BlockModelV3,
  createPFrameForGraphs,
  createPlDataTableStateV2,
  createPlDataTableV2,
  DataModelBuilder,
} from "@platforma-sdk/model";
import { kind } from "@platforma-open/milaboratories.rarefaction.kind";
import { getDefaultBlockLabel } from "./label";
import type { BlockArgs, BlockData, LegacyBlockArgs, LegacyBlockUiState } from "./types";

export type * from "@milaboratories/helpers";

const defaultGraphState = (): BlockData["graphState"] => ({
  title: "Rarefaction Curves",
  template: "curve_dots",
  currentTab: "settings",
});

const blockDataModel = new DataModelBuilder({ kind })
  .from<BlockData>("V20260518")
  .upgradeLegacy<LegacyBlockArgs, LegacyBlockUiState>(({ args, uiState }) => ({
    customBlockLabel: args?.customBlockLabel ?? "",
    datasetRef: args?.datasetRef,
    // No V1 source for `datasetLabel`: V1 carried only the full
    // `defaultBlockLabel` string. Reseeded on the next dataset-picker gesture.
    datasetLabel: undefined,
    numPoints: args?.numPoints ?? "20",
    numIterations: args?.numIterations ?? "100",
    extrapolation: args?.extrapolation ?? true,
    mem: args?.mem ?? 8,
    cpu: args?.cpu ?? 4,
    tableState: uiState?.tableState ?? createPlDataTableStateV2(),
    graphState: uiState?.graphState ?? defaultGraphState(),
  }))
  // `params` is absent when a block is created by hand rather than from a
  // template, so every field the contract carries keeps its own default.
  .init(({ params }) => ({
    customBlockLabel: params?.customBlockLabel ?? "",
    datasetRef: params?.datasetRef,
    datasetLabel: params?.datasetLabel,
    numPoints: params?.numPoints ?? "20",
    numIterations: params?.numIterations ?? "100",
    extrapolation: params?.extrapolation ?? true,
    mem: params?.mem ?? 8,
    cpu: params?.cpu ?? 4,
    tableState: createPlDataTableStateV2(),
    graphState: defaultGraphState(),
  }));

function isValidNum(num: string | undefined): boolean {
  if (num === undefined) return false;
  const v = Number(num);
  return Number.isInteger(v) && v > 0 && v < 10000;
}

function deriveSubtitle(data: BlockData): string {
  if (data.customBlockLabel) return data.customBlockLabel;
  return (
    getDefaultBlockLabel({
      datasetLabel: data.datasetLabel,
      numPoints: data.numPoints,
      extrapolation: data.extrapolation,
    }) || ""
  );
}

export const platforma = BlockModelV3.create({ dataModel: blockDataModel, kind })

  // Inverse of `init` — the same fields, projected back out for template export,
  // handed back exactly as they sit in live state. `tableState` and `graphState`
  // are view state and never cross the boundary. `datasetRef` carries a block id,
  // which the SDK rewrites on the way out and resolves again on the way in.
  .templateParams((data) => ({
    datasetRef: data.datasetRef,

    numPoints: data.numPoints,
    numIterations: data.numIterations,
    extrapolation: data.extrapolation,

    mem: data.mem,
    cpu: data.cpu,

    datasetLabel: data.datasetLabel,
    customBlockLabel: data.customBlockLabel,
  }))

  .args<BlockArgs>((data) => {
    if (data.datasetRef === undefined) throw new Error("Dataset is required");
    if (!isValidNum(data.numPoints)) throw new Error("Number of points must be between 1 and 9999");
    if (!isValidNum(data.numIterations))
      throw new Error("Number of iterations must be between 1 and 9999");
    if (data.mem === undefined) throw new Error("Memory is required");
    if (data.cpu === undefined) throw new Error("CPU is required");

    return {
      datasetRef: data.datasetRef,
      numPoints: data.numPoints.trim(),
      numIterations: data.numIterations.trim(),
      extrapolation: data.extrapolation,
      mem: data.mem,
      cpu: data.cpu,
    };
  })

  .outputWithStatus("graphPFrame", (ctx) => {
    const pCols = ctx.outputs?.resolve("rarefactionPFrame")?.getPColumns();
    if (pCols === undefined) return undefined;
    return createPFrameForGraphs(ctx, pCols);
  })

  .output("rarefactionPFrameCols", (ctx) =>
    ctx.outputs
      ?.resolve("rarefactionPFrame")
      ?.getPColumns()
      ?.map((p) => p.spec),
  )

  .outputWithStatus("table", (ctx) => {
    const cols = ctx.outputs?.resolve("rarefactionPFrame")?.getPColumns();
    if (cols === undefined) return undefined;
    return createPlDataTableV2(ctx, cols, ctx.data.tableState);
  })

  .output("datasetOptions", (ctx) =>
    ctx.resultPool.getOptions([
      {
        axes: [{ name: "pl7.app/sampleId" }, { name: "pl7.app/vdj/clonotypeKey" }],
        annotations: { "pl7.app/isAnchor": "true" },
      },
      {
        axes: [{ name: "pl7.app/sampleId" }, { name: "pl7.app/vdj/scClonotypeKey" }],
        annotations: { "pl7.app/isAnchor": "true" },
      },
      {
        axes: [{ name: "pl7.app/sampleId" }, { name: "pl7.app/variantKey" }],
        annotations: { "pl7.app/isAnchor": "true" },
      },
    ]),
  )

  .output("isRunning", (ctx) => ctx.outputs?.getIsReadyOrError() === false)

  .output("noData", (ctx) => ctx.outputs?.resolve("noData")?.getDataAsJson<boolean>())

  .output("rarefactionLogs", (ctx) => ctx.outputs?.resolve("rarefactionLogs")?.getLogHandle())

  .title(() => "Rarefaction")

  .subtitle((ctx) => deriveSubtitle(ctx.data))

  .sections((_ctx) => [
    { type: "link" as const, href: "/" as const, label: "Curves" },
    { type: "link" as const, href: "/table" as const, label: "Table" },
  ])

  .done();

export type Platforma = typeof platforma;
export type BlockOutputs = InferOutputsType<typeof platforma>;

export { getDefaultBlockLabel } from "./label";
export * from "./types";
