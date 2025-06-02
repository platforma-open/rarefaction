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

const result = computed(() => {
  // Adjust the path if clnsCounts is located elsewhere in your app.model
  const data = app.model.outputs.result;
  return Array.isArray(data) ? data : [];
});
</script>

<template>
  <PlBlockPage>
    <PlTextField v-model="app.model.args.name" label="Enter your name" :clearable="() => undefined" />

    <PlAlert v-if="app.model.outputs.debugStdout" type="success"> {{ app.model.outputs.debugStdout }} </PlAlert>

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

    <!-- Table for clnsCounts -->
    <div style="margin-top: 20px;">
      <table v-if="result.length > 0" border="1" style="width: 100%; border-collapse: collapse;">
        <thead>
        <tr>
          <!-- Adjust these headers based on the properties of objects in result -->
          <th>ID</th>
          <th>Name</th>
          <!-- Add more <th> elements if your objects have more properties -->
        </tr>
        </thead>
        <tbody>
        <tr v-for="(item, index) in result" :key="index">
          <td v-for="(value, colIndex) in item" :key="colIndex">
            {{ value }}
          </td>
        </tr>
        </tbody>
      </table>
      <p v-else>
        No counts data to display.
      </p>
    </div>
    <!-- /Table for clnsCounts -->


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