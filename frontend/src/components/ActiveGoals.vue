<template>
  <div class="space-y-6">
    <div class="relative">
      <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
        <PlusIcon class="h-5 w-5 text-brand-calm" />
      </div>
      <input 
        v-model="newGoalDescription" 
        @keyup.enter="addGoal" 
        placeholder="What's your primary focus right now?" 
        class="block w-full pl-11 pr-32 py-4 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-2xl focus:ring-2 focus:ring-brand-calm outline-none transition-all dark:text-white text-lg font-medium shadow-inner"
      >
      <button 
        @click="addGoal" 
        class="absolute right-2 top-2 bottom-2 bg-brand-calm hover:bg-brand-calm/90 text-white px-6 rounded-xl font-bold shadow-lg shadow-brand-calm/20 transition-all active:scale-95 text-sm uppercase tracking-wide"
      >
        Add Goal
      </button>
    </div>

    <div v-if="goals.length === 0" class="py-12 text-center">
      <div class="bg-slate-50 dark:bg-slate-900/50 rounded-3xl p-8 border-2 border-dashed border-slate-200 dark:border-slate-800">
        <SparklesIcon class="h-12 w-12 text-brand-calm/30 mx-auto mb-4" />
        <h4 class="text-xl font-bold text-slate-400 dark:text-slate-500">No active goals yet.</h4>
        <p class="text-slate-400 dark:text-slate-600 mt-1 italic">Ready to win the minute?</p>
      </div>
    </div>

    <ul class="space-y-4">
      <li v-for="goal in goals" :key="goal.id" class="group bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 p-5 rounded-2xl shadow-sm hover:shadow-md transition-all duration-300">
        <div class="flex items-center justify-between gap-4">
          <div class="flex items-center gap-4 flex-1 min-w-0">
            <button 
              @click="completeGoal(goal.id)" 
              class="w-7 h-7 rounded-full border-2 border-slate-300 dark:border-slate-600 flex items-center justify-center hover:border-brand-calm dark:hover:border-brand-accent transition-colors group/check shrink-0"
              aria-label="Complete goal"
            >
              <CheckIcon class="h-4 w-4 text-brand-calm opacity-0 group-hover/check:opacity-100 transition-opacity" />
            </button>
            <span class="text-lg font-semibold text-slate-800 dark:text-slate-200 truncate">{{ goal.description }}</span>
          </div>
          
          <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <button @click="breakdownGoal(goal.id, goal.description)" class="p-2 text-slate-400 hover:text-brand-calm hover:bg-brand-calm/10 rounded-lg transition-all" title="AI Breakdown">
              <BoltIcon class="h-5 w-5" />
            </button>
            <button @click="activeSubGoalParent = goal.id" class="p-2 text-slate-400 hover:text-brand-calm hover:bg-brand-calm/10 rounded-lg transition-all" title="Add Sub-goal">
              <PlusCircleIcon class="h-5 w-5" />
            </button>
            <button @click="deleteGoal(goal.id)" class="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-all" title="Delete">
              <TrashIcon class="h-5 w-5" />
            </button>
          </div>
        </div>

        <!-- Subgoals List -->
        <ul v-if="goal.subgoals && goal.subgoals.length > 0" class="mt-4 ml-11 space-y-3 border-l-2 border-slate-100 dark:border-slate-700 pl-4">
          <li v-for="sub in goal.subgoals" :key="sub.id" class="flex items-center justify-between group/sub">
            <div class="flex items-center gap-3">
              <button @click="completeGoal(sub.id)" class="w-5 h-5 rounded-md border-2 border-slate-300 dark:border-slate-600 flex items-center justify-center hover:border-brand-calm transition-colors shrink-0">
                <CheckIcon class="h-3 w-3 text-brand-calm opacity-0 group-hover/sub:opacity-100 transition-opacity" />
              </button>
              <span class="text-sm font-medium text-slate-600 dark:text-slate-400">{{ sub.description }}</span>
            </div>
            <button @click="deleteGoal(sub.id)" class="p-1.5 text-slate-300 hover:text-red-500 opacity-0 group-hover/sub:opacity-100 transition-all">
              <XMarkIcon class="h-4 w-4" />
            </button>
          </li>
        </ul>

        <!-- Add Subgoal Input -->
        <div v-if="activeSubGoalParent === goal.id" class="mt-4 ml-11 flex gap-2">
          <input 
            v-model="newSubGoalDescription" 
            @keyup.enter="addSubGoal(goal.id)" 
            placeholder="Add sub-task..." 
            class="flex-1 px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white"
            auto-focus
          >
          <button @click="addSubGoal(goal.id)" class="bg-brand-calm text-white px-4 py-2 rounded-xl text-xs font-bold hover:bg-brand-calm/90 transition-all">Add</button>
          <button @click="activeSubGoalParent = null" class="text-slate-400 hover:text-slate-600 px-2 transition-all font-bold text-xs">Cancel</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { 
  PlusIcon, 
  CheckIcon, 
  TrashIcon, 
  PlusCircleIcon, 
  BoltIcon, 
  XMarkIcon,
  SparklesIcon
} from '@heroicons/vue/24/outline'
import { goals, showToast } from '../store'

const newGoalDescription = ref('')
const activeSubGoalParent = ref<number | null>(null)
const newSubGoalDescription = ref('')

const addGoal = async () => {
  if (!newGoalDescription.value.trim()) return
  const res = await fetch('/api/goals', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description: newGoalDescription.value })
  })
  if (res.ok) {
    newGoalDescription.value = ''
    showToast("Goal added.")
  }
}

const completeGoal = async (id: number) => {
  const res = await fetch(`/api/goals/${id}/complete`, { method: 'POST' })
  if (res.ok) {
    showToast("Goal completed!")
  }
}

const deleteGoal = async (id: number) => {
  if (!confirm("Are you sure?")) return
  const res = await fetch(`/api/goals/${id}`, { method: 'DELETE' })
  if (res.ok) {
    showToast("Goal deleted.")
  }
}

const breakdownGoal = async (id: number, description: string) => {
  showToast("AI breaking down goal...")
  const res = await fetch(`/api/goals/${id}/breakdown`, { method: 'POST' })
  if (res.ok) {
    showToast("Goal broken down successfully.")
  } else {
    showToast("Failed to breakdown goal.", true)
  }
}

const addSubGoal = async (parentId: number) => {
  if (!newSubGoalDescription.value.trim()) return
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
