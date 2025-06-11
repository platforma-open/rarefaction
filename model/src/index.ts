import type { GraphMakerState } from '@milaboratories/graph-maker';
import type { InferOutputsType, PlDataTableState, PlRef } from '@platforma-sdk/model';
import { BlockModel, createPFrameForGraphs, createPlDataTableV2 } from '@platforma-sdk/model';

// validation rules
function numRule(num: string | undefined): boolean {
  const numValue = Number(num);
  return numValue > 0 && numValue < 100;
}

function numRuleError(num: string | undefined): boolean | string {
  if (numRule(num)) {
    return 'Input a number between 1 and 100';
  }
  return true;
}

export type BlockArgs = {
  num: string;
  name?: string; // todo cleanup code
  datasetRef?: PlRef;
  numRules?: ((num: string) => boolean | string)[]; // todo cleanup
};

export type UiState = {
  title?: string;
  tableState: PlDataTableState;
  graphState: GraphMakerState;
};

/*************************
 *         MODEL         *
 *************************/
export const model = BlockModel.create()

  /*************************
   *          ARGS         *
   *************************/
  .withArgs<BlockArgs>({
    numRules: [numRuleError],
    num: '20',
  })

  /*************************
   *        UI STATE       *
   *************************/
  .withUiState<UiState>({
    tableState: {
      gridState: {},
    },
    graphState: {
      title: 'Rarefaction',
      template: 'line_binnedDots',
      // layersSettings: {
      //   dots: {
      //     dotFill: '#5d32c6',
      //   },
      // },
    },
  },
  )
  .argsValid((ctx) => (ctx.args.datasetRef !== undefined && numRule(ctx.args.num)))

  /*************************
   *        OUTPUTS        *
   *************************/
  .output('rarefactionGraphPframe', (ctx) => {
    return createPFrameForGraphs(ctx, ctx.outputs?.resolve('rarefactionPframe')?.getPColumns());
  })
  .output('table', (ctx) => {
    const cols = ctx.outputs?.resolve('rarefactionPframe')?.getPColumns();
    if (cols === undefined) {
      return undefined;
    }

    return createPlDataTableV2(
      ctx,
      cols,
      // if there are links, we need to pick one of the links to show all axes in the table
      (spec) => {
        return spec.name === "pl7.app/mean_unique_clonotypes";
      },
      ctx.uiState.tableState,
      undefined,
    );
  })

  // Get MiXCR outputs from the result pool
  .output('datasetOptions', (ctx) =>
    ctx.resultPool.getOptions([{
      axes: [
        { name: 'pl7.app/sampleId' },
        { name: 'pl7.app/vdj/clonotypeKey' },
      ],
      annotations: { 'pl7.app/isAnchor': 'true' },
    }, {
      axes: [
        { name: 'pl7.app/sampleId' },
        { name: 'pl7.app/vdj/scClonotypeKey' },
      ],
      annotations: { 'pl7.app/isAnchor': 'true' },
    }]),
  )
  .output('debugStdout', (ctx) =>
    ctx.outputs?.resolve('debugStdout')?.getFileContentAsString(),
  )
  .output('debugStdoutStream', (ctx) =>
    ctx.outputs?.resolve('debugStdoutStream')?.getLogHandle(),
  )

  /*************************
   *        SECTIONS       *
   *************************/
  .sections((_ctx) => [
    { type: 'link', href: '/', label: 'Graph' },
    { type: 'link', href: '/table', label: 'Table' }
  ])
  .done();

export type BlockOutputs = InferOutputsType<typeof model>;
