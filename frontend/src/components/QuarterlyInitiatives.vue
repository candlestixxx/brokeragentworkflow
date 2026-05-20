<template>
  <section class="bg-white rounded-lg shadow-md p-6 mb-8 flex-1">
    <h2 class="text-2xl font-semibold text-gray-800 border-b border-gray-100 pb-3 mb-4">Quarterly Initiatives</h2>
    <ul class="divide-y divide-gray-100">
      <li v-for="initiative in initiatives" :key="initiative.id" class="py-4 flex justify-between items-center group">
        <span class="text-gray-700">
          <span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded font-semibold mr-2">{{ initiative.quarter }}</span>
          {{ initiative.description }}
        </span>
        <button @click="completeInitiative(initiative.id)" class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded shadow transition duration-150 font-medium">
          Complete
        </button>
      </li>
      <li v-if="initiatives.length === 0" class="py-4 text-gray-500 italic text-center">No pending initiatives. Time to plan!</li>
    </ul>

    <form @submit.prevent="addInitiative" class="mt-6 flex flex-col gap-3">
      <div class="flex gap-3">
        <select v-model="newInitiative.quarter" required class="w-1/3 px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white">
          <option value="" disabled>Quarter</option>
          <option value="Q1">Q1</option>
          <option value="Q2">Q2</option>
          <option value="Q3">Q3</option>
          <option value="Q4">Q4</option>
        </select>
        <input v-model="newInitiative.description" type="text" placeholder="Initiative description..." required class="flex-1 px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
      </div>
      <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded shadow font-medium">Add Initiative</button>
    </form>
  </section>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { initiatives, showToast } from '../store'

const newInitiative = reactive({ quarter: '', description: '' })

const addInitiative = async () => {
  const res = await fetch('/api/initiatives', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newInitiative)
  })
  if (res.ok) {
    newInitiative.quarter = ''
    newInitiative.description = ''
    showToast("Initiative added.")
  }
}

const completeInitiative = async (id: number) => {
  const res = await fetch(`/api/initiatives/${id}/complete`, { method: 'POST' })
  if (res.ok) {
    showToast("Initiative completed!")
  }
}
</script>
