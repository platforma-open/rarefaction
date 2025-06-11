<script setup lang="ts">
import type { PlAgDataTableSettings } from '@platforma-sdk/ui-vue';
import {
  PlBlockPage,
  PlBtnGhost, PlDropdownRef,
  PlMaskIcon24,
  PlSlideModal,
  PlLogView,
  PlTextField, PlAgDataTableV2,
} from '@platforma-sdk/ui-vue';
import { useApp } from '../app';
import { ref, computed } from 'vue'; // Added computed

const app = useApp();
const settingsOpen = ref(false);

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

    <!-- Settings -->
    <template #append>
      <PlBtnGhost @click.stop="() => settingsOpen = true">
        Settings
        <template #append>
          <PlMaskIcon24 name="settings" />
        </template>
      </PlBtnGhost>
    </template>
    <PlSlideModal v-model="settingsOpen">
      <template #title>Settings</template>

      <PlDropdownRef
        v-model="app.model.args.datasetRef"
        label="Select dataset"
        :options="app.model.outputs.datasetOptions"
      />
      <PlTextField
        v-model="app.model.args.num"
        label="Input points number"
      /><!--todo: how to show validation error?-->
    </PlSlideModal>
    <!-- /Settings -->
  </PlBlockPage>
</template>
