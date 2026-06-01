<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-100 dark:border-gray-700 transition-colors">
      <h2 class="text-2xl font-semibold text-gray-800 dark:text-gray-100 mb-6 flex items-center gap-2">
        <ChartBarIcon class="w-6 h-6 text-blue-500" />
        Analytics Dashboard
      </h2>

      <div v-if="loading" class="text-center py-10 text-gray-500 dark:text-gray-400">
        Loading analytics...
      </div>

      <div v-else-if="error" class="text-center py-10 text-red-500">
        {{ error }}
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

        <!-- Total Goals -->
        <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-100 dark:border-blue-800 flex flex-col items-center justify-center text-center transition-colors">
          <span class="text-blue-500 dark:text-blue-400 mb-1">
            <ClipboardDocumentListIcon class="w-8 h-8 mx-auto" />
          </span>
          <span class="text-3xl font-bold text-gray-800 dark:text-gray-100">{{ stats?.total_goals || 0 }}</span>
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mt-1">Total Goals</span>
        </div>

        <!-- Completed Goals -->
        <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-100 dark:border-green-800 flex flex-col items-center justify-center text-center transition-colors">
          <span class="text-green-500 dark:text-green-400 mb-1">
            <CheckCircleIcon class="w-8 h-8 mx-auto" />
          </span>
          <span class="text-3xl font-bold text-gray-800 dark:text-gray-100">{{ stats?.completed_goals || 0 }}</span>
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mt-1">Completed</span>
        </div>

        <!-- Completion Rate -->
        <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg border border-purple-100 dark:border-purple-800 flex flex-col items-center justify-center text-center transition-colors">
          <span class="text-purple-500 dark:text-purple-400 mb-1">
            <ChartPieIcon class="w-8 h-8 mx-auto" />
          </span>
          <span class="text-3xl font-bold text-gray-800 dark:text-gray-100">{{ stats?.completion_percentage || 0 }}%</span>
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mt-1">Completion Rate</span>
        </div>

        <!-- Daily Streak -->
        <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg border border-orange-100 dark:border-orange-800 flex flex-col items-center justify-center text-center transition-colors">
          <span class="text-orange-500 dark:text-orange-400 mb-1">
            <FireIcon class="w-8 h-8 mx-auto" />
          </span>
          <span class="text-3xl font-bold text-gray-800 dark:text-gray-100">{{ stats?.streak || 0 }}</span>
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide mt-1">Day Streak</span>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ChartBarIcon, ClipboardDocumentListIcon, CheckCircleIcon, ChartPieIcon, FireIcon } from '@heroicons/vue/24/outline'

interface AnalyticsStats {
  total_goals: number
  completed_goals: number
  pending_goals: number
  completion_percentage: number
  streak: number
}

const stats = ref<AnalyticsStats | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const res = await fetch('/api/analytics')
    if (res.ok) {
      stats.value = await res.json()
    } else {
      error.value = 'Failed to load analytics data.'
    }
  } catch (e) {
    error.value = 'An error occurred while fetching analytics.'
  } finally {
    loading.value = false
  }
})
</script>
