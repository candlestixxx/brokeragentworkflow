<template>
  <div>
    <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-100 border-b border-gray-100 dark:border-gray-700 pb-3 mb-4 transition-colors">Daily Habits</h3>

    <ul class="divide-y divide-gray-100 dark:divide-gray-700 transition-colors">
      <li v-for="habit in habits" :key="habit.id" class="py-4 flex flex-col group">
        <div class="flex justify-between items-center w-full">
          <span class="text-gray-700 dark:text-gray-300 transition-colors">
            <span class="text-gray-400 dark:text-gray-500 font-mono text-sm mr-2 transition-colors">[{{ habit.id }}]</span>
            {{ habit.description }}
          </span>
          <div>
            <button @click="completeHabit(habit.id)" class="bg-green-500 hover:bg-green-600 dark:bg-green-600 dark:hover:bg-green-700 text-white px-4 py-1 rounded shadow transition font-medium text-sm mr-2">
              Complete
            </button>
            <button @click="deleteHabit(habit.id)" class="bg-red-500 hover:bg-red-600 dark:bg-red-600 dark:hover:bg-red-700 text-white px-4 py-1 rounded shadow transition font-medium text-sm">
              Delete
            </button>
          </div>
        </div>

        <div class="mt-2 text-sm text-gray-500 dark:text-gray-400 transition-colors">
          <span class="font-semibold text-orange-500 mr-4">🔥 Current Streak: {{ habit.current_streak }}</span>
          <span class="mr-4">🏆 Highest: {{ habit.highest_streak }}</span>
          <span v-if="habit.last_completed_date" class="text-xs italic">Last done: {{ habit.last_completed_date }}</span>
          <span v-else class="text-xs italic">Not completed yet</span>
        </div>
      </li>
      <li v-if="habits.length === 0" class="py-4 text-gray-500 dark:text-gray-400 italic text-center transition-colors">No habits tracked. Start one today!</li>
    </ul>

    <form @submit.prevent="submitHabit" class="mt-6 flex gap-3">
      <input v-model="newHabit" type="text" placeholder="New daily habit..." required class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
      <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded shadow font-medium transition-colors">Add Habit</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { habits, showToast } from '../store'

const newHabit = ref<string>('')

const completeHabit = async (id: number) => {
  const res = await fetch(`/api/habits/${id}/complete`, { method: 'POST' })
  const data = await res.json()
  if (res.ok) {
    showToast("Habit completed! Streak updated.")
  } else {
    showToast(data.error || "Failed to complete habit.", true)
  }
}

const deleteHabit = async (id: number) => {
  const res = await fetch(`/api/habits/${id}`, { method: 'DELETE' })
  if (res.ok) {
    showToast("Habit deleted.")
  }
}

const submitHabit = async () => {
  const res = await fetch('/api/habits', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description: newHabit.value })
  })
  if (res.ok) {
    newHabit.value = ''
    showToast("Habit added.")
  }
}
</script>
