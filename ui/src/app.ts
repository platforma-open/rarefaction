import { model } from '@platforma-open/milaboratories.rarefaction.model';
import { defineApp } from '@platforma-sdk/ui-vue';
import { watch } from 'vue';
import GraphPage from './pages/GraphPage.vue';
import TablePage from './pages/TablePage.vue';

export const sdkPlugin = defineApp(model, () => {
  return {
    routes: {
      '/': () => GraphPage,
      '/table': () => TablePage,
    },
  };
});

export const useApp = sdkPlugin.useApp;

// Make sure labels are initialized
const unwatch = watch(sdkPlugin, ({ loaded }) => {
  if (!loaded) return;
  const app = useApp();
  app.model.args.customBlockLabel ??= '';
  app.model.args.defaultBlockLabel ??= 'Select dataset';
  unwatch();
});
