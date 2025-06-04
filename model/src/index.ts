import { BlockModel, createPlDataTableV2, InferOutputsType, PlDataTableState, PlRef } from '@platforma-sdk/model';


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
  num?: string;
  name?: string;
  datasetRef?: PlRef;
  numRules?: ((num: string) => boolean | string)[];
};

export type UiState = {
  title?: string;
  tableState: PlDataTableState;
}


/*************************
 *         MODEL         *
 *************************/
export const model = BlockModel.create()

  /*************************
   *          ARGS         *
   *************************/
  .withArgs<BlockArgs>({
    numRules: [numRuleError]
  })

  /*************************
   *        UI STATE       *
   *************************/
  .withUiState<UiState>({
    tableState: {
      gridState: {}
    }
  })
  .argsValid((ctx) => (ctx.args.datasetRef !== undefined && numRule(ctx.args.num)))

  /*************************
   *        OUTPUTS        *
   *************************/
  .output('rarefactionPframe', (ctx) => {
    return ctx.outputs?.resolve('rarefactionPframe');
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
      undefined
    );
  })
  .output('table_debug', (ctx) => {
    const cols = ctx.outputs?.resolve('rarefactionPframe')?.getPColumns();
    if (cols === undefined) {
      return undefined;
    }

    return cols.map((c) => ({
      id: c.id,
      spec: c.spec
    }));
  })




  // Get MiXCR outputs from the result pool
  .output('datasetOptions', (ctx) =>
    ctx.resultPool.getOptions([{
      axes: [
        { name: 'pl7.app/sampleId' },
        { name: 'pl7.app/vdj/clonotypeKey' }
      ],
      annotations: { 'pl7.app/isAnchor': 'true' }
    }, {
      axes: [
        { name: 'pl7.app/sampleId' },
        { 'name': 'pl7.app/vdj/scClonotypeKey' }
      ],
      annotations: { 'pl7.app/isAnchor': 'true' }
    }])
  )
  .output('debugStdout', (ctx) =>
    ctx.outputs?.resolve('debugStdout')?.getDataAsString()
  )


  /*************************
   *        SECTIONS       *
   *************************/
  .sections((_ctx) => [{ type: 'link', href: '/', label: 'Main' }])
  .done();

export type BlockOutputs = InferOutputsType<typeof model>;
