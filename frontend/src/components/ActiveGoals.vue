<template>
  <div>
    <ul class="divide-y divide-gray-100">
      <li v-for="goal in goals" :key="goal.id" class="py-4 flex flex-col group">
        <div class="flex justify-between items-center w-full">
          <span class="text-gray-700">
            <span class="text-gray-400 font-mono text-sm mr-2">[{{ goal.id }}]</span>
            {{ goal.description }}
          </span>
          <div>
            <button @click="addSubGoalForm(goal.id)" class="bg-gray-200 hover:bg-gray-300 text-gray-700 px-3 py-1 rounded shadow transition duration-150 font-medium mr-2 text-sm">
              + Sub-goal
            </button>
            <button @click="completeGoal(goal.id)" class="bg-green-500 hover:bg-green-600 text-white px-4 py-1 rounded shadow transition duration-150 font-medium text-sm">
              Complete
            </button>
          </div>
        </div>

        <!-- Subgoals List -->
        <ul v-if="goal.subgoals && goal.subgoals.length > 0" class="mt-2 ml-6 border-l-2 border-gray-200 pl-4">
          <li v-for="sub in goal.subgoals" :key="sub.id" class="py-2 flex justify-between items-center">
            <span class="text-gray-600 text-sm">
              <span class="text-gray-400 font-mono text-xs mr-2">[{{ sub.id }}]</span>
              {{ sub.description }}
            </span>
            <button @click="completeGoal(sub.id)" class="bg-green-400 hover:bg-green-500 text-white px-3 py-1 rounded shadow transition duration-150 font-medium text-xs">
              Complete
            </button>
          </li>
        </ul>

        <!-- Add Subgoal Form -->
        <form v-if="activeSubGoalParent === goal.id" @submit.prevent="submitSubGoal(goal.id)" class="mt-3 ml-6 flex gap-2">
          <input v-model="newSubGoalDescription" type="text" placeholder="Sub-goal description..." required autofocus class="flex-1 px-3 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500">
          <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-1 rounded shadow font-medium text-sm">Save</button>
          <button type="button" @click="activeSubGoalParent = null" class="text-gray-500 hover:text-gray-700 px-2 text-sm">Cancel</button>
        </form>
      </li>
      <li v-if="goals.length === 0" class="py-4 text-gray-500 italic text-center">No pending goals. Great job!</li>
    </ul>

    <form @submit.prevent="submitGoal" class="mt-6 flex gap-3">
      <input v-model="newGoal" type="text" placeholder="New daily goal..." required class="flex-1 px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
      <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded shadow font-medium">Add Goal</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { goals, showToast } from '../store.js'

const newGoal = ref('')
const activeSubGoalParent = ref(null)
const newSubGoalDescription = ref('')

const completeGoal = async (id) => {
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

const addSubGoalForm = (parentId) => {
  activeSubGoalParent.value = parentId
  newSubGoalDescription.value = ''
}

const submitSubGoal = async (parentId) => {
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
