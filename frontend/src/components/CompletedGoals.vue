<template>
  <ul class="divide-y divide-gray-100 dark:divide-gray-700 transition-colors">
    <li v-for="goal in completedGoals" :key="goal.id" class="py-4 flex justify-between items-center opacity-60 hover:opacity-100 transition-opacity">
      <span class="text-gray-700 dark:text-gray-300 line-through transition-colors">
        <span class="text-gray-400 dark:text-gray-500 font-mono text-sm mr-2 line-through transition-colors">[{{ goal.id }}]</span>
        {{ goal.description }}
      </span>
      <div class="flex items-center gap-4">
        <span class="text-green-600 dark:text-green-500 font-bold text-lg">✓</span>
        <button @click="deleteGoal(goal.id)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded shadow transition font-medium text-xs">
          Delete
        </button>
      </div>
    </li>
    <li v-if="completedGoals.length === 0" class="py-4 text-gray-500 dark:text-gray-400 italic text-center transition-colors">No completed goals yet.</li>
  </ul>
</template>

<script setup lang="ts">
import { completedGoals, showToast } from '../store'

const deleteGoal = async (id: number) => {
  const res = await fetch(`/api/goals/${id}`, { method: 'DELETE' })
  if (res.ok) {
    showToast("Goal deleted.")
  }
}
</script>
