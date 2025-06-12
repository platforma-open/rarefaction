import type { GraphMakerState } from '@milaboratories/graph-maker';
import type { InferOutputsType, PlDataTableState, PlRef } from '@platforma-sdk/model';
import { BlockModel, createPFrameForGraphs, createPlDataTableV2 } from '@platforma-sdk/model';

// validation rules
function numRule(num: string | undefined): boolean {
  const numValue = Number(num);
  return numValue > 0 && numValue < 10000;
}

function numRuleError(num: string | undefined): boolean | string {
  if (numRule(num)) {
    return 'Input a number between 1 and 100';
  }
  return true;
}

export type BlockArgs = {
  numPoints: string;
  numIterations: string;
  datasetRef?: PlRef;
  numRules?: ((num: string) => boolean | string)[]; // todo find a way to show text field err
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
    numPoints: '20',
    numIterations: '100',
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
  .argsValid((ctx) => (
    ctx.args.datasetRef !== undefined
    && numRule(ctx.args.numPoints)
    && numRule(ctx.args.numIterations)
  ))

  /*************************
   *        OUTPUTS        *
   *************************/
  .output('graphPFrame', (ctx) => {
    return createPFrameForGraphs(ctx, ctx.outputs?.resolve('exportedPFrame')?.getPColumns());
   // return ctx.createPFrame(ctx.outputs?.resolve('exportedPFrame')?.getPColumns()??[])
  })
  .output('table', (ctx) => {
    const cols = ctx.outputs?.resolve('exportedPFrame')?.getPColumns();
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
