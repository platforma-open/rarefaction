<script setup lang="ts">
import '@milaboratories/graph-maker/styles';
import { PlBlockPage, PlDropdownRef, PlTextField } from '@platforma-sdk/ui-vue';
import { useApp } from '../app';

import type { PredefinedGraphOption } from '@milaboratories/graph-maker';
import { GraphMaker } from '@milaboratories/graph-maker';

const app = useApp();

const defaultOptions: PredefinedGraphOption<'scatterplot'>[] = [
  {
    inputName: 'y',
    selectedSource: {
      kind: 'PColumn',
      name: 'pl7.app/vdj/rarefaction/meanUniqueClonotypes',
      valueType: 'Float',
      axesSpec: [],
    },
  },
  {
    inputName: 'x',
    selectedSource: {
      name: 'pl7.app/vdj/rarefaction/samplingDepth',
      type: 'Int',
    },
  },
  {
    inputName: 'grouping',
    selectedSource: {
      name: 'pl7.app/sampleId',
      type: 'String',
    },
  },
];

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
        />
        <PlTextField
          v-model="app.model.args.numIterations"
          label="Number of iterations per depth"
        />
      </template>
    </GraphMaker>
  </PlBlockPage>
</template>
