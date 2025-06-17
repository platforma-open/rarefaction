<script setup lang="ts">
import '@milaboratories/graph-maker/styles';
import { PlBlockPage, PlDropdownRef, PlTextField } from '@platforma-sdk/ui-vue';
import { useApp } from '../app';

import type { GraphMakerProps } from '@milaboratories/graph-maker';
import { GraphMaker } from '@milaboratories/graph-maker';
import type { PlSelectionModel } from '@platforma-sdk/model';
import { ref, watch } from 'vue';

const app = useApp();

const defaultOptions: GraphMakerProps['defaultOptions'] = [
  {
    inputName: 'y',
    selectedSource: {
      kind: 'PColumn',
      name: 'pl7.app/mean_unique_clonotypes',   //todo: fix spec
      valueType: 'Float',
      axesSpec: []
    }
  },
  {
    inputName: 'x',
    selectedSource: {
      name: 'pl7.app/subsampling_depth',
      type: 'Int',
    }
  },
  {
    inputName: 'grouping',
    selectedSource: {
      name: 'pl7.app/sampleId',
      type: 'String',
    }
  }
];

const selection = ref<PlSelectionModel>({
  axesSpec: [],
  selectedKeys: []
});

// todo: add as debug feature to readme
watch(() => app.model.outputs.graphPFrame, async (handle) => {
  const list = await platforma?.pFrameDriver.listColumns(handle!);
  console.log(list, 'list');
}, { immediate: true });
</script>

<template>
  <PlBlockPage>
    <GraphMaker
      v-model="app.model.ui.graphState"
      chartType="scatterplot"
      :p-frame="app.model.outputs.graphPFrame"
      :default-options="defaultOptions"

    >
      <template #settingsSlot>
        <PlDropdownRef
          v-model="app.model.args.datasetRef"
          label="Select dataset"
          :options="app.model.outputs.datasetOptions"
        />
        <PlTextField
          v-model="app.model.args.numPoints"
          label="Input points number"
        /><!--todo: how to show validation error?-->
        <PlTextField
          v-model="app.model.args.numIterations"
          label="Number of iterations per depth"
        /><!--todo: how to show validation error?-->
      </template>
    </GraphMaker>
  </PlBlockPage>
</template>
