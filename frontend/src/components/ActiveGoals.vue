<template>
  <div class="space-y-10">
    <!-- Input Section -->
    <div class="relative group">
      <div class="absolute -inset-0.5 bg-gradient-to-r from-brand-calm to-brand-accent rounded-3xl blur opacity-20 group-focus-within:opacity-40 transition duration-500"></div>
      <div class="relative bg-white dark:bg-slate-900 rounded-3xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden flex items-center">
        <div class="pl-6 pointer-events-none">
          <PlusIcon class="h-6 w-6 text-brand-calm" />
        </div>
        <input 
          v-model="newGoalDescription" 
          @keyup.enter="addGoal" 
          placeholder="What's your primary focus right now?" 
          class="flex-1 pl-4 pr-32 py-6 bg-transparent outline-none dark:text-white text-lg font-medium placeholder:text-slate-400"
        >
        <div class="pr-2">
          <button 
            @click="addGoal" 
            class="bg-slate-900 dark:bg-slate-700 hover:bg-black dark:hover:bg-slate-600 text-white px-8 py-4 rounded-2xl font-black text-xs uppercase tracking-widest shadow-xl transition-all active:scale-95"
          >
            Add Goal
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="goals.length === 0" class="py-20 text-center bg-slate-50/50 dark:bg-slate-900/30 rounded-[3rem] border-2 border-dashed border-slate-100 dark:border-slate-800">
      <SparklesIcon class="h-20 w-20 text-slate-200 dark:text-slate-700 mx-auto mb-6" />
      <h4 class="text-2xl font-black text-slate-400 uppercase tracking-tighter">Mission Control Empty</h4>
      <p class="text-slate-400 mt-2 font-medium italic">Ready to win the minute?</p>
    </div>

    <!-- Goals List -->
    <ul class="space-y-6">
      <li v-for="goal in goals" :key="goal.id" class="group bg-white dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700 p-6 rounded-[2rem] shadow-sm hover:shadow-xl hover:border-brand-calm/30 transition-all duration-500 relative">
        
        <div class="flex items-center justify-between gap-6">
          <div class="flex items-center gap-5 flex-1 min-w-0">
            <button 
              @click="completeGoal(goal.id)" 
              class="w-10 h-10 rounded-2xl border-2 border-slate-200 dark:border-slate-700 flex items-center justify-center hover:border-brand-calm hover:bg-brand-calm/5 transition-all group/check shrink-0"
              aria-label="Complete goal"
            >
              <CheckIcon class="h-6 w-6 text-brand-calm opacity-0 group-hover/check:opacity-100 transition-opacity" />
            </button>
            <span class="text-xl font-bold text-slate-800 dark:text-slate-100 truncate group-hover:text-brand-calm transition-colors">{{ goal.description }}</span>
          </div>
          
          <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all transform translate-x-2 group-hover:translate-x-0">
            <button @click="breakdownGoal(goal.id, goal.description)" class="p-3 text-slate-400 hover:text-brand-calm hover:bg-brand-calm/10 rounded-xl transition-all" title="AI Breakdown">
              <BoltIcon class="h-5 w-5" />
            </button>
            <button @click="activeSubGoalParent = goal.id" class="p-3 text-slate-400 hover:text-brand-calm hover:bg-brand-calm/10 rounded-xl transition-all" title="Add Sub-goal">
              <PlusCircleIcon class="h-5 w-5" />
            </button>
            <button @click="deleteGoal(goal.id)" class="p-3 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-xl transition-all" title="Delete">
              <TrashIcon class="h-5 w-5" />
            </button>
          </div>
        </div>

        <!-- Subgoals List -->
        <ul v-if="goal.subgoals && goal.subgoals.length > 0" class="mt-6 ml-14 space-y-4 border-l-2 border-slate-50 dark:border-slate-700/50 pl-6">
          <li v-for="sub in goal.subgoals" :key="sub.id" class="flex items-center justify-between group/sub">
            <div class="flex items-center gap-4">
              <button @click="completeGoal(sub.id)" class="w-6 h-6 rounded-lg border-2 border-slate-200 dark:border-slate-700 flex items-center justify-center hover:border-brand-calm transition-all shrink-0">
                <CheckIcon class="h-4 w-4 text-brand-calm opacity-0 group-hover/sub:opacity-100 transition-opacity" />
              </button>
              <span class="text-sm font-bold text-slate-500 dark:text-slate-400 group-hover/sub:text-slate-900 dark:group-hover/sub:text-white transition-colors">{{ sub.description }}</span>
            </div>
            <button @click="deleteGoal(sub.id)" class="p-2 text-slate-300 hover:text-red-500 opacity-0 group-hover/sub:opacity-100 transition-all transform translate-x-2 group-hover/sub:translate-x-0">
              <XMarkIcon class="h-4 w-4" />
            </button>
          </li>
        </ul>

        <!-- Add Subgoal Input -->
        <Transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="transform -translate-y-2 opacity-0"
          enter-to-class="transform translate-y-0 opacity-100"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="transform translate-y-0 opacity-100"
          leave-to-class="transform -translate-y-2 opacity-0"
        >
          <div v-if="activeSubGoalParent === goal.id" class="mt-6 ml-14 flex items-center gap-3">
            <div class="flex-1 relative">
              <input 
                v-model="newSubGoalDescription" 
                @keyup.enter="addSubGoal(goal.id)" 
                placeholder="Micro-task description..." 
                class="w-full px-5 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-2xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white font-medium"
                auto-focus
              >
            </div>
            <button @click="addSubGoal(goal.id)" class="bg-brand-calm text-white px-5 py-3 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-brand-calm/90 transition-all shadow-lg shadow-brand-calm/10">Add</button>
            <button @click="activeSubGoalParent = null" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 px-2 font-black text-[10px] uppercase tracking-widest transition-all">Cancel</button>
          </div>
        </Transition>
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
