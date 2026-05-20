<template>
  <ul class="divide-y divide-gray-100">
    <li v-for="goal in completedGoals" :key="goal.id" class="py-4 flex justify-between items-center opacity-60">
      <span class="text-gray-700 line-through">
        <span class="text-gray-400 font-mono text-sm mr-2 line-through">[{{ goal.id }}]</span>
        {{ goal.description }}
      </span>
      <span class="text-green-600 font-bold text-lg">✓</span>
    </li>
    <li v-if="completedGoals.length === 0" class="py-4 text-gray-500 italic text-center">No completed goals yet.</li>
  </ul>
</template>

<script setup>
import { completedGoals } from '../store.js'
</script>
