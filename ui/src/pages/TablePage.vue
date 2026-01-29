<script setup lang="ts">
import { PlAgDataTableV2, PlBlockPage, usePlDataTableSettingsV2 } from '@platforma-sdk/ui-vue';
import strings from '@milaboratories/strings';
import { useApp } from '../app';

const app = useApp();

const tableSettings = usePlDataTableSettingsV2({
  model: () => app.model.outputs.table,
});

</script>

<template>
  <PlBlockPage
    title="Rarefaction"
  >
    <PlAgDataTableV2
      v-model="app.model.ui.tableState"
      :settings="tableSettings"
      :not-ready-text="strings.callToActions.configureSettingsAndRun"
      :no-rows-text="strings.states.noDataAvailable"
    />
  </PlBlockPage>
</template>
