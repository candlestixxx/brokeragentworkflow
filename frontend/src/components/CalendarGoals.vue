<template>
  <div v-for="(dayGoals, date) in calendarGoals" :key="date" class="mb-6">
    <h3 class="font-bold text-gray-700 bg-gray-50 px-3 py-2 rounded-t border border-gray-100 border-b-0">{{ date }}</h3>
    <ul class="border border-gray-100 rounded-b divide-y divide-gray-50">
      <li v-for="goal in dayGoals" :key="goal.id" :class="{'opacity-60 bg-gray-50': goal.status === 'completed'}" class="py-3 px-4 flex justify-between items-center">
        <span class="text-gray-700" :class="{'line-through': goal.status === 'completed'}">
          {{ goal.description }}
        </span>
        <span v-if="goal.status === 'completed'" class="text-green-600 font-bold text-sm">✓</span>
        <span v-else class="text-yellow-600 text-xs font-semibold px-2 py-1 bg-yellow-100 rounded">Pending</span>
      </li>
    </ul>
  </div>
  <div v-if="Object.keys(calendarGoals).length === 0" class="py-4 text-gray-500 italic text-center">No goals recorded yet.</div>
</template>

<script setup lang="ts">
import { calendarGoals } from '../store'
</script>
