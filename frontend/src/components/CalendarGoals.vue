<template>
  <div v-for="(dayGoals, date) in calendarGoals" :key="date" class="mb-6">
    <h3 class="font-bold text-gray-700 dark:text-gray-200 bg-gray-50 dark:bg-gray-700 px-3 py-2 rounded-t border border-gray-100 dark:border-gray-600 border-b-0 transition-colors">{{ date }}</h3>
    <ul class="border border-gray-100 dark:border-gray-600 rounded-b divide-y divide-gray-50 dark:divide-gray-700 transition-colors">
      <li v-for="goal in dayGoals" :key="goal.id" :class="{'opacity-60 bg-gray-50 dark:bg-gray-800': goal.status === 'completed'}" class="py-3 px-4 flex justify-between items-center transition-colors">
        <span class="text-gray-700 dark:text-gray-300 transition-colors" :class="{'line-through': goal.status === 'completed'}">
          {{ goal.description }}
        </span>
        <span v-if="goal.status === 'completed'" class="text-green-600 dark:text-green-500 font-bold text-sm">✓</span>
        <span v-else class="text-yellow-600 dark:text-yellow-500 text-xs font-semibold px-2 py-1 bg-yellow-100 dark:bg-yellow-900/50 rounded transition-colors">Pending</span>
      </li>
    </ul>
  </div>
  <div v-if="Object.keys(calendarGoals).length === 0" class="py-4 text-gray-500 dark:text-gray-400 italic text-center transition-colors">No goals recorded yet.</div>
</template>

<script setup lang="ts">
import { calendarGoals } from '../store'
</script>
