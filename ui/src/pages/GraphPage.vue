<script setup lang="ts">
import type { PredefinedGraphOption } from "@milaboratories/graph-maker";
import { GraphMaker } from "@milaboratories/graph-maker";
import strings from "@milaboratories/strings";
import type { DatasetSelection, PColumnSpec } from "@platforma-sdk/model";
import { createDatasetSelection, createPrimaryRef, plRefsEqual } from "@platforma-sdk/model";
import {
  PlAccordionSection,
  PlAlert,
  PlBlockPage,
  PlBtnGhost,
  PlCheckbox,
  PlDatasetSelector,
  PlLogView,
  PlMaskIcon24,
  PlNumberField,
  PlSlideModal,
} from "@platforma-sdk/ui-vue";
import { computed, ref, watch } from "vue";
import { useApp } from "../app";

const app = useApp();

const logOpen = ref(false);

// Auto-close settings panel when block starts running
watch(
  () => app.model.outputs.isRunning,
  (isRunning, wasRunning) => {
    if (isRunning && !wasRunning) {
      app.model.data.graphState.currentTab = null;
    }
  },
);

const datasetSelection = computed<DatasetSelection | undefined>({
  get: () => {
    const { datasetRef, filterRef } = app.model.data;
    if (datasetRef === undefined) return undefined;
    return createDatasetSelection(createPrimaryRef(datasetRef, filterRef));
  },
  set: (selection) => {
    const datasetRef = selection?.primary.column;
    const filterRef = selection?.primary.filter;
    app.model.data.datasetRef = datasetRef;
    app.model.data.filterRef = filterRef;
    // Snapshot the chosen dataset's (or subset's) human label into `data` so `.subtitle`
    // can derive the default block label without re-querying the result pool.
    const option = datasetRef
      ? app.model.outputs.datasetOptions?.find((o) => plRefsEqual(o.primary.ref, datasetRef, true))
      : undefined;
    const filter = filterRef
      ? option?.filters?.find((f) => plRefsEqual(f.ref, filterRef, true))
      : undefined;
    app.model.data.datasetLabel = (filter ?? option?.primary)?.label;
  },
});

// Bridge string-typed data fields (kept as string to satisfy the workflow's
// "string" subtemplate validation and the string-typed domain values in
// column specs) to PlNumberField's numeric v-model.
const numPointsModel = computed({
  get: () => {
    const n = Number(app.model.data.numPoints);
    return Number.isFinite(n) ? n : undefined;
  },
  set: (v) => {
    app.model.data.numPoints = v === undefined ? "" : String(v);
  },
});

const numIterationsModel = computed({
  get: () => {
    const n = Number(app.model.data.numIterations);
    return Number.isFinite(n) ? n : undefined;
  },
  set: (v) => {
    app.model.data.numIterations = v === undefined ? "" : String(v);
  },
});

function validateIntCount(value: number | undefined): string | undefined {
  if (value === undefined) return "Required";
  if (!Number.isInteger(value)) return "Must be an integer";
  if (value < 1) return "Must be at least 1";
  if (value >= 10000) return "Must be less than 10000";
  return undefined;
}

const defaultOptions = computed((): PredefinedGraphOption<"scatterplot">[] | null => {
  const pCols = app.model.outputs.rarefactionPFrameCols;
  if (!pCols) return null;

  function getColumnSpec(name: string, cols: PColumnSpec[]) {
    return cols.find((p) => p.name === name);
  }

  const yCol = getColumnSpec("pl7.app/rarefaction/meanUniqueSequences", pCols);
  const shapeCol = getColumnSpec("pl7.app/rarefaction/type", pCols);

  if (!yCol || !shapeCol) return null;

  return [
    { inputName: "x", selectedSource: yCol.axesSpec[1] },
    { inputName: "y", selectedSource: yCol },
    { inputName: "grouping", selectedSource: yCol.axesSpec[0] },
    { inputName: "shape", selectedSource: shapeCol },
  ];
});
</script>

<template>
  <PlBlockPage no-body-gutters>
    <PlAlert v-if="app.model.outputs.noData" type="warn" icon style="margin: 12px 12px 0">
      No sequences found in the selected dataset. Please check your input data.
    </PlAlert>
    <GraphMaker
      v-model="app.model.data.graphState"
      chart-type="scatterplot"
      :p-frame="app.model.outputs.graphPFrame"
      :default-options="defaultOptions"
      default-palette="bright"
      :status-text="{ noPframe: { title: strings.callToActions.configureSettingsAndRun } }"
    >
      <template #titleLineSlot>
        <PlBtnGhost @click.stop="() => (logOpen = true)">
          {{ strings.titles.logs }}
          <template #append>
            <PlMaskIcon24 name="file-logs" />
          </template>
        </PlBtnGhost>
      </template>
      <template #settingsSlot>
        <PlDatasetSelector
          v-model="datasetSelection"
          label="Select dataset"
          :options="app.model.outputs.datasetOptions"
          clearable
          :disabled="app.model.outputs.isRunning"
        >
          <template #tooltip>
            Select the dataset to be used for the rarefaction analysis.
          </template>
        </PlDatasetSelector>
        <PlNumberField
          v-model="numPointsModel"
          label="Input points number"
          :min="1"
          :max="9999"
          :step="1"
          required
          :validate="validateIntCount"
          :disabled="app.model.outputs.isRunning"
        >
          <template #tooltip>
            The number of subsampling depths to be used for the rarefaction analysis.
          </template>
        </PlNumberField>
        <PlNumberField
          v-model="numIterationsModel"
          label="Number of iterations per depth"
          :min="1"
          :max="9999"
          :step="1"
          required
          :validate="validateIntCount"
          :disabled="app.model.outputs.isRunning"
        >
          <template #tooltip>
            The number of times the subsampling will be repeated at each depth.
          </template>
        </PlNumberField>
        <PlCheckbox
          v-model="app.model.data.extrapolation"
          label="Extrapolation"
          :disabled="app.model.outputs.isRunning"
        >
          Extrapolate to largest sample
          <template #tooltip>
            Extrapolate the number of unique sequences for depths greater than the total number of
            sequences.
          </template>
        </PlCheckbox>
        <PlAccordionSection :label="strings.titles.advancedSettings">
          <PlNumberField
            v-model="app.model.data.mem"
            label="Memory (GiB)"
            :disabled="app.model.outputs.isRunning"
            :min-value="1"
          >
            <template #tooltip> The amount of memory to allocate to the job. </template>
          </PlNumberField>
          <PlNumberField
            v-model="app.model.data.cpu"
            label="CPU (cores)"
            :disabled="app.model.outputs.isRunning"
            :min-value="1"
          >
            <template #tooltip> The number of CPU cores to allocate to the job. </template>
          </PlNumberField>
        </PlAccordionSection>
      </template>
    </GraphMaker>
    <PlSlideModal v-model="logOpen" width="80%">
      <template #title>Rarefaction Log</template>
      <PlLogView :log-handle="app.model.outputs.rarefactionLogs" />
    </PlSlideModal>
  </PlBlockPage>
</template>
