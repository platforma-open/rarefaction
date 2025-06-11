<script setup lang="ts">
import '@milaboratories/graph-maker/styles';
import { PlBlockPage } from '@platforma-sdk/ui-vue';
import { useApp } from '../app';

import type { GraphMakerProps } from '@milaboratories/graph-maker';
import { GraphMaker } from '@milaboratories/graph-maker';
// import type { PlSelectionModel } from '@platforma-sdk/model';
import { ref } from 'vue';

const app = useApp();

const defaultOptions: GraphMakerProps['defaultOptions'] = [
  {
    inputName: 'x',
    selectedSource: {
      kind: 'PColumn',
      name: 'pl7.app/vdj/umap1',   //todo: fix spec
      valueType: 'Double',
      axesSpec: [
        {
          name: 'pl7.app/clonotypeKey',
          type: 'String'
        }
      ]
    }
  },
  {
    inputName: 'y',
    selectedSource: {
      kind: 'PColumn',
      name: 'pl7.app/vdj/umap2',
      valueType: 'Double',
      axesSpec: [
        {
          name: 'pl7.app/clonotypeKey',
          type: 'String'
        }
      ]
    }
  },
  {
    inputName: 'highlight',
    selectedSource: {
      kind: 'PColumn',
      name: 'pl7.app/vdj/sampling-column',
      valueType: 'Int',
      axesSpec: [
        {
          name: 'pl7.app/clonotypeKey',
          type: 'String'
        }
      ]
    }
  }
];

// const selection = ref<PlSelectionModel>({
//   axesSpec: [],
//   selectedKeys: [],
// });

</script>

<template>
  <PlBlockPage>
    <GraphMaker
      v-model="app.model.ui.graphState"
      chartType="discrete"
      :data-state-key="app.model.outputs.rarefactionGraphPframe"
      :p-frame="app.model.outputs.rarefactionGraphPframe"
      :default-options="defaultOptions"
    >
      <template #titleLineSlot>
        Rarefaction
      </template>
    </GraphMaker>
  </PlBlockPage>
</template>
