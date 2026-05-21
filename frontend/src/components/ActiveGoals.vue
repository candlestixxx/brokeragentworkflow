<template>
  <div>
    <ul class="divide-y divide-gray-100 dark:divide-gray-700 transition-colors">
      <li v-for="goal in goals" :key="goal.id" class="py-4 flex flex-col group">
        <div class="flex justify-between items-center w-full">
          <span class="text-gray-700 dark:text-gray-300 transition-colors">
            <span class="text-gray-400 dark:text-gray-500 font-mono text-sm mr-2 transition-colors">[{{ goal.id }}]</span>
            {{ goal.description }}
          </span>
          <div>
            <button @click="addSubGoalForm(goal.id)" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-gray-200 text-gray-700 px-3 py-1 rounded shadow transition font-medium mr-2 text-sm">
              + Sub-goal
            </button>
            <button @click="completeGoal(goal.id)" class="bg-green-500 hover:bg-green-600 dark:bg-green-600 dark:hover:bg-green-700 text-white px-4 py-1 rounded shadow transition font-medium text-sm">
              Complete
            </button>
          </div>
        </div>

        <!-- Subgoals List -->
        <ul v-if="goal.subgoals && goal.subgoals.length > 0" class="mt-2 ml-6 border-l-2 border-gray-200 dark:border-gray-600 pl-4 transition-colors">
          <li v-for="sub in goal.subgoals" :key="sub.id" class="py-2 flex justify-between items-center">
            <span class="text-gray-600 dark:text-gray-400 text-sm transition-colors">
              <span class="text-gray-400 dark:text-gray-500 font-mono text-xs mr-2 transition-colors">[{{ sub.id }}]</span>
              {{ sub.description }}
            </span>
            <button @click="completeGoal(sub.id)" class="bg-green-400 hover:bg-green-500 dark:bg-green-500 dark:hover:bg-green-600 text-white px-3 py-1 rounded shadow transition font-medium text-xs">
              Complete
            </button>
          </li>
        </ul>

        <!-- Add Subgoal Form -->
        <form v-if="activeSubGoalParent === goal.id" @submit.prevent="submitSubGoal(goal.id)" class="mt-3 ml-6 flex gap-2">
          <input v-model="newSubGoalDescription" type="text" placeholder="Sub-goal description..." required autofocus class="flex-1 px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded focus:outline-none focus:ring-1 focus:ring-blue-500 transition-colors">
          <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-1 rounded shadow font-medium text-sm transition-colors">Save</button>
          <button type="button" @click="activeSubGoalParent = null" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 px-2 text-sm transition-colors">Cancel</button>
        </form>
      </li>
      <li v-if="goals.length === 0" class="py-4 text-gray-500 dark:text-gray-400 italic text-center transition-colors">No pending goals. Great job!</li>
    </ul>

    <form @submit.prevent="submitGoal" class="mt-6 flex gap-3">
      <input v-model="newGoal" type="text" placeholder="New daily goal..." required class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
      <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded shadow font-medium transition-colors">Add Goal</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { goals, showToast } from '../store'

const newGoal = ref<string>('')
const activeSubGoalParent = ref<number | null>(null)
const newSubGoalDescription = ref<string>('')

const completeGoal = async (id: number) => {
  const res = await fetch(`/api/goals/${id}/complete`, { method: 'POST' })
  if (res.ok) {
    showToast("Goal completed! Excellent work.")
  }
}

const submitGoal = async () => {
  const res = await fetch('/api/goals', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description: newGoal.value })
  })
  if (res.ok) {
    newGoal.value = ''
    showToast("Goal added.")
  }
}

const addSubGoalForm = (parentId: number) => {
  activeSubGoalParent.value = parentId
  newSubGoalDescription.value = ''
}

const submitSubGoal = async (parentId: number) => {
  const res = await fetch('/api/goals', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description: newSubGoalDescription.value, parent_id: parentId })
  })
  if (res.ok) {
    activeSubGoalParent.value = null
    newSubGoalDescription.value = ''
    showToast("Sub-goal added.")
  }
}
</script>
