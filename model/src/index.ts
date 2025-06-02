import {
  deriveLabels,
  InferOutputsType,
  isPColumnSpecResult, parseResourceMap,
  PlRef,
  readOutput,
  RenderCtx
} from '@platforma-sdk/model';
import { BlockModel } from '@platforma-sdk/model';


// rules


export type BlockArgs = {
  num?: string;
  name?: string;
  datasetRef?: PlRef;
  numRules?: ((num: string) => boolean | string)[];
};
export type DatasetOption = {
  ref: PlRef;
  label: string;
  assemblingFeature: string;
};

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


// @ts-ignore
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
  .argsValid((ctx) => (ctx.args.datasetRef !== undefined && numRule(ctx.args.num)))

  /*************************
   *        OUTPUTS        *
   *************************/
  .output('rarefactionPframe', (ctx) => ctx.outputs?.resolve('rarefactionPframe')?.getDataAsJson())
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
          { "name": "pl7.app/vdj/scClonotypeKey" }
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
