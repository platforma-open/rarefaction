import { getDefaultBlockLabel, model } from '@platforma-open/milaboratories.rarefaction.model';
import { plRefsEqual } from '@platforma-sdk/model';
import { defineApp } from '@platforma-sdk/ui-vue';
import { watchEffect } from 'vue';
import GraphPage from './pages/GraphPage.vue';
import TablePage from './pages/TablePage.vue';

export const sdkPlugin = defineApp(model, (app) => {
  app.model.args.customBlockLabel ??= '';

  syncDefaultBlockLabel(app.model);

  return {
    routes: {
      '/': () => GraphPage,
      '/table': () => TablePage,
    },
  };
});

export const useApp = sdkPlugin.useApp;

type AppModel = ReturnType<typeof useApp>['model'];

function syncDefaultBlockLabel(model: AppModel) {
  watchEffect(() => {
    const datasetLabel = model.args.datasetRef
      ? model.outputs.datasetOptions
        ?.find((option) => plRefsEqual(option.ref, model.args.datasetRef!))
        ?.label
      : undefined;

    model.args.defaultBlockLabel = getDefaultBlockLabel({
      datasetLabel,
      numPoints: model.args.numPoints,
      extrapolation: model.args.extrapolation,
    });
  });
}
