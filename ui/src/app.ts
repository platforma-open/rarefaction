import { model } from '@platforma-open/platforma-open.rarefaction.model';
import { defineApp } from '@platforma-sdk/ui-vue';
import TablePage from './pages/TablePage.vue';
import GraphPage from './pages/GraphPage.vue';

export const sdkPlugin = defineApp(model, () => {
  return {
    routes: {
      '/': () => GraphPage,
      '/table': () => TablePage,
    },
  };
});

export const useApp = sdkPlugin.useApp;
