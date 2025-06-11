<script setup lang="ts">
import type { PlAgDataTableSettings } from '@platforma-sdk/ui-vue';
import { PlAgDataTableV2, PlBlockPage, PlLogView } from '@platforma-sdk/ui-vue';
import { useApp } from '../app';
import { computed } from 'vue'; // Added computed

const app = useApp();

const tableSettings = computed<PlAgDataTableSettings>(() => (
  app.model.outputs.table
    ? { sourceType: 'ptable', model: app.model.outputs.table }
    : undefined
));
</script>

<template>
  <PlBlockPage>
    <template #title>Rarefaction</template>

    <PlAgDataTableV2
      v-model="app.model.ui.tableState"
      :settings="tableSettings"
      notReadyText="Please select dataset in Settings panel"
      loadingText="Processing data..."
      noRowsText="Empty result. Check that sample contains data. Use Clonotype Browser block."
    />

    <PlLogView
      :log-handle="app.model.outputs.debugStdoutStream"
    />
  </PlBlockPage>
</template>
