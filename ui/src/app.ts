import { platforma } from '@platforma-open/milaboratories.rarefaction.model';
import { defineAppV3 } from '@platforma-sdk/ui-vue';
import GraphPage from './pages/GraphPage.vue';
import TablePage from './pages/TablePage.vue';

export const sdkPlugin = defineAppV3(platforma, () => {
  return {
    routes: {
      '/': () => GraphPage,
      '/table': () => TablePage,
    },
  };
});

export const useApp = sdkPlugin.useApp;
