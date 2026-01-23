import type { GraphMakerState } from '@milaboratories/graph-maker';
import type { InferOutputsType, PlDataTableStateV2, PlRef } from '@platforma-sdk/model';
import { BlockModel, createPFrameForGraphs, createPlDataTableStateV2, createPlDataTableV2 } from '@platforma-sdk/model';
import { getDefaultBlockLabel } from './label';

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
  defaultBlockLabel: string;
  customBlockLabel: string;
  numPoints: string;
  numIterations: string;
  extrapolation: boolean;
  mem?: number;
  cpu?: number;
  datasetRef?: PlRef;
  numRules?: ((num: string) => boolean | string)[]; // todo find a way to show text field err
};

export type UiState = {
  tableState: PlDataTableStateV2;
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
    defaultBlockLabel: getDefaultBlockLabel({
      numPoints: '20',
      extrapolation: true,
    }),
    customBlockLabel: '',
    numRules: [numRuleError],
    numPoints: '20',
    numIterations: '100',
    extrapolation: true,
    mem: 8,
    cpu: 4,
  })

  /*************************
   *        UI STATE       *
   *************************/
  .withUiState<UiState>({
    tableState: createPlDataTableStateV2(),
    graphState: {
      title: 'Rarefaction Curves',
      template: 'curve_dots',
      currentTab: 'settings',
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
  .outputWithStatus('graphPFrame', (ctx) => {
    const pCols = ctx.outputs?.resolve('rarefactionPFrame')?.getPColumns();
    if (pCols === undefined) {
      return undefined;
    }
    return createPFrameForGraphs(ctx, pCols);
  })
  .output('rarefactionPFrameCols', (ctx) => {
    return ctx.outputs?.resolve('rarefactionPFrame')?.getPColumns()?.map((p) => p.spec);
  })
  .outputWithStatus('table', (ctx) => {
    const cols = ctx.outputs?.resolve('rarefactionPFrame')?.getPColumns();
    if (cols === undefined) {
      return undefined;
    }

    return createPlDataTableV2(
      ctx,
      cols,
      ctx.uiState.tableState,
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
  .title(() => 'Rarefaction')

  .subtitle((ctx) => ctx.args.customBlockLabel || ctx.args.defaultBlockLabel || '')

  .output('isRunning', (ctx) => ctx.outputs?.getIsReadyOrError() === false)

  /*************************
   *        SECTIONS       *
   *************************/
  .sections((_ctx) => [
    { type: 'link', href: '/', label: 'Curves' },
    { type: 'link', href: '/table', label: 'Table' },
  ])
  .done(2);

export type BlockOutputs = InferOutputsType<typeof model>;

export { getDefaultBlockLabel } from './label';
