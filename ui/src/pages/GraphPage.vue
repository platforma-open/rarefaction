<script setup lang="ts">
import type { PredefinedGraphOption } from '@milaboratories/graph-maker';
import { GraphMaker } from '@milaboratories/graph-maker';
import '@milaboratories/graph-maker/styles';
import type { PlRef } from '@platforma-sdk/model';
import { plRefsEqual, type PColumnSpec } from '@platforma-sdk/model';
import { PlAccordionSection, PlBlockPage, PlCheckbox, PlDropdownRef, PlNumberField, PlTextField } from '@platforma-sdk/ui-vue';
import { computed, watchEffect } from 'vue';
import { useApp } from '../app';

const app = useApp();

// updating defaultBlockLabel
watchEffect(() => {
  let label = '';
  // Add dataset name if available
  if (app.model.args.datasetRef) {
    const datasetOption = app.model.outputs.datasetOptions?.find((o) => plRefsEqual(o.ref, app.model.args.datasetRef!));
    if (datasetOption?.label) {
      label = datasetOption.label;
    }
  }

  // Build secondary parts (points and extrapolation)
  const secondaryParts: string[] = [];
  if (app.model.args.numPoints) {
    secondaryParts.push(`${app.model.args.numPoints} points`);
  }
  if (app.model.args.extrapolation) {
    secondaryParts.push('extrapolated');
  }

  // Combine: "Dataset - 10 iter, extrapolated"
  if (label && secondaryParts.length > 0) {
    label = `${label} - ${secondaryParts.join(', ')}`;
  } else if (secondaryParts.length > 0) {
    label = secondaryParts.join(', ');
  }

  app.model.args.defaultBlockLabel = label || 'Select dataset';
});

function setDatasetRef(datasetRef?: PlRef) {
  app.model.args.datasetRef = datasetRef;
}

const defaultOptions = computed((): PredefinedGraphOption<'scatterplot'>[] | null => {
  const pCols = app.model.outputs.rarefactionPFrameCols;
  if (!pCols) {
    return null;
  }

  function getColumnSpec(name: string, cols: PColumnSpec[]) {
    return cols.find((p) => p.name === name);
  }

  const yCol = getColumnSpec('pl7.app/vdj/rarefaction/meanUniqueClonotypes', pCols);
  const shapeCol = getColumnSpec('pl7.app/vdj/rarefaction/type', pCols);

  if (!yCol || !shapeCol) {
    return null;
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
    {
      inputName: 'shape',
      selectedSource: shapeCol,
    },
  ];
});

const key = computed(() => defaultOptions.value ? JSON.stringify(defaultOptions.value) : '');

</script>

<template>
  <PlBlockPage no-body-gutters>
    <GraphMaker
      :key="key"
      v-model="app.model.ui.graphState"
      chart-type="scatterplot"
      :p-frame="app.model.outputs.graphPFrame"
      :default-options="defaultOptions"
    >
      <template #settingsSlot>
        <PlDropdownRef
          v-model="app.model.args.datasetRef"
          label="Select dataset"
          :options="app.model.outputs.datasetOptions"
          clearable
          :disabled="app.model.outputs.isRunning"
          @update:model-value="setDatasetRef"
        >
          <template #tooltip>
            Select the dataset to be used for the rarefaction analysis.
          </template>
        </PlDropdownRef>
        <PlTextField
          v-model="app.model.args.numPoints"
          label="Input points number"
          :disabled="app.model.outputs.isRunning"
        >
          <template #tooltip>
            The number of subsampling depths to be used for the rarefaction analysis.
          </template>
        </PlTextField>
        <PlTextField
          v-model="app.model.args.numIterations"
          label="Number of iterations per depth"
          :disabled="app.model.outputs.isRunning"
        >
          <template #tooltip>
            The number of times the subsampling will be repeated at each depth.
          </template>
        </PlTextField>
        <PlCheckbox
          v-model="app.model.args.extrapolation"
          label="Extrapolation"
          :disabled="app.model.outputs.isRunning"
        >
          Extrapolate to largest sample
          <template #tooltip>
            Extrapolate the number of unique clonotypes for depths greater than the total number of clonotypes.
          </template>
        </PlCheckbox>
        <PlAccordionSection label="Advanced Settings">
          <PlNumberField
            v-model="app.model.args.mem"
            label="Memory (GiB)"
            :disabled="app.model.outputs.isRunning"
            :min-value="1"
          >
            <template #tooltip>
              The amount of memory to allocate to the job.
            </template>
          </PlNumberField>
          <PlNumberField
            v-model="app.model.args.cpu"
            label="CPU (cores)"
            :disabled="app.model.outputs.isRunning"
            :min-value="1"
          >
            <template #tooltip>
              The number of CPU cores to allocate to the job.
            </template>
          </PlNumberField>
        </PlAccordionSection>
      </template>
    </GraphMaker>
  </PlBlockPage>
</template>
