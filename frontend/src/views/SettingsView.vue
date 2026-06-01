<template>
  <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-8 text-center transition-colors">Settings</h2>

  <div class="max-w-xl mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 transition-colors">
    <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-100 border-b border-gray-100 dark:border-gray-700 pb-3 mb-6 transition-colors">Notifications</h3>

    <div class="flex items-center justify-between">
      <div>
        <h4 class="text-md font-medium text-gray-900 dark:text-gray-200 transition-colors">Email & SMS Alerts</h4>
        <p class="text-sm text-gray-500 dark:text-gray-400 transition-colors">Receive morning prompts and weekly initiative reminders.</p>
      </div>
      <Switch
        v-model="user.notifications_enabled"
        @update:modelValue="saveSettings"
        :class="user.notifications_enabled ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'"
        class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        <span class="sr-only">Enable notifications</span>
        <span
          :class="user.notifications_enabled ? 'translate-x-6' : 'translate-x-1'"
          class="inline-block h-4 w-4 transform rounded-full bg-white transition"
        />
      </Switch>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Switch } from '@headlessui/vue'
import { user, showToast } from '../store'

const saveSettings = async (newValue: boolean) => {
  const res = await fetch('/api/me/settings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ notifications_enabled: newValue })
  })

  if (res.ok) {
    showToast("Settings updated successfully.")
  } else {
    showToast("Failed to update settings.", true)
    // Revert visually on error
    user.notifications_enabled = !newValue
  }
}
</script>
