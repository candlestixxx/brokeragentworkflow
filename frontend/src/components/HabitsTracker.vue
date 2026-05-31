<template>
  <div class="space-y-6">
    <div class="relative">
      <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
        <ArrowPathIcon class="h-5 w-5 text-brand-calm" />
      </div>
      <input 
        v-model="newHabit" 
        @keyup.enter="addHabit" 
        placeholder="Add a new daily habit..." 
        class="block w-full pl-11 pr-32 py-4 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-2xl focus:ring-2 focus:ring-brand-calm outline-none transition-all dark:text-white text-lg font-medium shadow-inner"
      >
      <button 
        @click="addHabit" 
        class="absolute right-2 top-2 bottom-2 bg-brand-calm hover:bg-brand-calm/90 text-white px-6 rounded-xl font-bold shadow-lg shadow-brand-calm/20 transition-all active:scale-95 text-sm uppercase tracking-wide"
      >
        Track Habit
      </button>
    </div>

    <div v-if="habits.length === 0" class="py-12 text-center bg-slate-50 dark:bg-slate-900/50 rounded-3xl border-2 border-dashed border-slate-200 dark:border-slate-800">
      <BoltIcon class="h-12 w-12 text-brand-calm/30 mx-auto mb-4" />
      <h4 class="text-xl font-bold text-slate-400 dark:text-slate-500">No habits tracked yet.</h4>
      <p class="text-slate-400 dark:text-slate-600 mt-1 italic">Consistency is the superpower of high achievers.</p>
    </div>

    <div class="grid grid-cols-1 gap-4">
      <div v-for="habit in habits" :key="habit.id" class="group bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 p-5 rounded-2xl shadow-sm hover:shadow-md transition-all duration-300">
        <div class="flex items-center justify-between gap-4">
          <div class="flex items-center gap-4 flex-1">
            <button 
              @click="completeHabit(habit.id)" 
              :disabled="habit.last_completed_date === today"
              :class="[
                habit.last_completed_date === today ? 'bg-brand-calm text-white border-brand-calm' : 'border-slate-300 dark:border-slate-600 hover:border-brand-calm',
                'w-10 h-10 rounded-xl border-2 flex items-center justify-center transition-all shrink-0'
              ]"
            >
              <CheckIcon class="h-6 w-6" />
            </button>
            <div class="min-w-0">
              <h5 class="text-lg font-bold text-slate-800 dark:text-slate-200 truncate">{{ habit.description }}</h5>
              <div class="flex items-center gap-3 mt-1">
                <div class="flex items-center gap-1.5 text-xs font-bold text-orange-500 bg-orange-50 dark:bg-orange-900/20 px-2 py-0.5 rounded-full uppercase tracking-tight">
                  <FireIcon class="h-3.5 w-3.5" />
                  {{ habit.current_streak }} Day Streak
                </div>
                <div class="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest">
                  Best: {{ habit.highest_streak }}
                </div>
              </div>
            </div>
          </div>
          
          <button @click="deleteHabit(habit.id)" class="p-2 text-slate-300 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg opacity-0 group-hover:opacity-100 transition-all">
            <TrashIcon class="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { 
  ArrowPathIcon, 
  CheckIcon, 
  FireIcon, 
  TrashIcon,
  BoltIcon
} from '@heroicons/vue/24/outline'
import { habits, showToast } from '../store'

const newHabit = ref('')
const today = new Date().toISOString().split('T')[0]

const addHabit = async () => {
  if (!newHabit.value.trim()) return
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

const completeHabit = async (id: number) => {
  const res = await fetch(`/api/habits/${id}/complete`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ completed_date: today })
  })
  if (res.ok) {
    showToast("Habit completed for today!")
  }
}

const deleteHabit = async (id: number) => {
  if (!confirm("Are you sure?")) return
  const res = await fetch(`/api/habits/${id}`, { method: 'DELETE' })
  if (res.ok) {
    showToast("Habit deleted.")
  }
}
</script>
