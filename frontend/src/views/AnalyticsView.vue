<template>
  <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-8 text-center transition-colors">Analytics Dashboard</h2>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
    <!-- Stat Card 1 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 flex flex-col items-center justify-center transition-colors">
      <span class="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">{{ analytics.completed_goals }}</span>
      <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide text-center">Total Goals Completed</h3>
    </div>

    <!-- Stat Card 2 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 flex flex-col items-center justify-center transition-colors">
      <span class="text-4xl font-bold text-indigo-600 dark:text-indigo-400 mb-2">{{ analytics.total_habits }}</span>
      <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide text-center">Habits Tracked</h3>
    </div>

    <!-- Stat Card 3 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 flex flex-col items-center justify-center transition-colors">
      <span class="text-4xl font-bold text-orange-500 dark:text-orange-400 mb-2">{{ analytics.longest_streak }}</span>
      <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide text-center">Longest Streak</h3>
    </div>

    <!-- Stat Card 4 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 flex flex-col items-center justify-center transition-colors">
      <span class="text-4xl font-bold text-green-600 dark:text-green-400 mb-2">{{ analytics.active_initiatives }}</span>
      <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide text-center">Active Initiatives</h3>
    </div>
  </div>
</template>

<script setup lang="ts">
import { analytics } from '../store'
</script>
