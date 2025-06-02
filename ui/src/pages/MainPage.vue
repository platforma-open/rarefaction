<script setup lang="ts">
import {
  PlAlert,
  PlBlockPage,
  PlBtnGhost, PlDropdownRef, PlDropdown,
  PlMaskIcon24,
  PlSlideModal,
  PlTextField
} from '@platforma-sdk/ui-vue';
import { useApp } from '../app';
import { ref, computed } from 'vue'; // Added computed

const app = useApp();
const settingsOpen = ref(false);

</script>

<template>
  <PlBlockPage>
    <PlTextField v-model="app.model.args.name" label="Enter your name" :clearable="() => undefined" />

    <PlAlert v-if="app.model.outputs.rarefactionPframe" type="success"> {{ app.model.outputs.rarefactionPframe }} </PlAlert>

    <template #title>Rere??? Block</template>

    <PlDropdownRef
      label="Select dataset"
      :options="app.model.outputs.datasetOptions"
      v-model="app.model.args.datasetRef"
    />
    <PlTextField
      label="Input points number"
      v-model="app.model.args.num"
    /><!--todo: how to show validation error?-->

    <!-- Settings -->
    <template #append>
      <PlBtnGhost @click.stop="() => settingsOpen = true">Settings
        <template #append>
          <PlMaskIcon24 name="settings"/>
        </template>
      </PlBtnGhost>
    </template>
    <PlSlideModal v-model="settingsOpen">
      <template #title>Settings</template>
    </PlSlideModal>
    <!-- /Settings -->
  </PlBlockPage>
</template>