<script setup lang="ts">
import {
  PlAlert,
  PlBlockPage,
  PlBtnGhost, PlDropdownRef, PlDropdown,
  PlMaskIcon24,
  PlSlideModal,
  PlTextField, PlAgDataTableV2, PlAgDataTableSettings
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
    <PlTextField v-model="app.model.args.name" label="Enter your name" :clearable="() => undefined" />

    <template #title>Rere??? Block</template>

    <PlAlert type="success" v-if="app.model.outputs.rarefactionPframe">{{app.model.outputs.table}}</PlAlert>

    <PlDropdownRef
      label="Select dataset"
      :options="app.model.outputs.datasetOptions"
      v-model="app.model.args.datasetRef"
    />
    <PlTextField
      label="Input points number"
      v-model="app.model.args.num"
    /><!--todo: how to show validation error?-->

    <PlAgDataTableV2
      v-model="app.model.ui.tableState"
      :settings="tableSettings"
    />


    <!-- Settings -->
    <template #append>
      <PlBtnGhost @click.stop="() => settingsOpen = true">Settings
        <template #append>
          <PlMaskIcon24 name="settings" />
        </template>
      </PlBtnGhost>
    </template>
    <PlSlideModal v-model="settingsOpen">
      <template #title>Settings</template>
    </PlSlideModal>
    <!-- /Settings -->
  </PlBlockPage>
</template>