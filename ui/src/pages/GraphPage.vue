<script setup lang="ts">
import type { PredefinedGraphOption } from '@milaboratories/graph-maker';
import { GraphMaker } from '@milaboratories/graph-maker';
import '@milaboratories/graph-maker/styles';
import type { PlRef } from '@platforma-sdk/model';
import { plRefsEqual, type PColumnSpec } from '@platforma-sdk/model';
import { PlBlockPage, PlDropdownRef, PlTextField } from '@platforma-sdk/ui-vue';
import { computed } from 'vue';
import { useApp } from '../app';

const app = useApp();

function setDatasetRef(datasetRef?: PlRef) {
  app.model.args.datasetRef = datasetRef;
  let label = '';
  if (datasetRef) {
    label = app.model.outputs.datasetOptions?.find((o) => plRefsEqual(o.ref, datasetRef))?.label ?? '';
  }
  app.model.ui.title = 'Rarefaction – ' + label;
}

const defaultOptions = computed((): PredefinedGraphOption<'scatterplot'>[] | undefined => {
  const pCols = app.model.outputs.rarefactionPFrameCols;
  if (!pCols) {
    return undefined;
  }

  function getColumnSpec(name: string, cols: PColumnSpec[]) {
    return cols.find((p) => p.name === name);
  }

  const yCol = getColumnSpec('pl7.app/vdj/rarefaction/meanUniqueClonotypes', pCols);

  if (!yCol) {
    return undefined;
  }

  return [
    {
      inputName: 'x',
      selectedSource: yCol.axesSpec[1],
    },
    {
      inputName: 'y',
      selectedSource: yCol,
    },
    {
      inputName: 'grouping',
      selectedSource: yCol.axesSpec[0],
    },
  ];
});
</script>

<template>
  <PlBlockPage no-body-gutters>
    <GraphMaker
      v-if="app.model.outputs.graphPFrame"
      v-model="app.model.ui.graphState"
      chart-type="scatterplot"
      :p-frame="app.model.outputs.graphPFrame"
      :default-options="defaultOptions"
      :title="app.model.ui.title"
    >
      <template #settingsSlot>
        <PlDropdownRef
          v-model="app.model.args.datasetRef"
          label="Select dataset"
          :options="app.model.outputs.datasetOptions"
          clearable
          @update:model-value="setDatasetRef"
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
