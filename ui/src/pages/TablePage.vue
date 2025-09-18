<script setup lang="ts">
import { PlAgDataTableV2, PlBlockPage, usePlDataTableSettingsV2 } from '@platforma-sdk/ui-vue';
import { useApp } from '../app';

const app = useApp();

const tableSettings = usePlDataTableSettingsV2({
  sourceId: () => app.model.args.datasetRef,
  model: () => app.model.outputs.table,
});

</script>

<template>
  <PlBlockPage>
    <template #title>Rarefaction</template>

    <PlAgDataTableV2
      v-model="app.model.ui.tableState"
      :settings="tableSettings"
    />
  </PlBlockPage>
</template>
