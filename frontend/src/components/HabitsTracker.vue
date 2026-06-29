<template>
  <div class="space-y-10">
    <!-- Input Section -->
    <div class="relative group">
      <div class="absolute -inset-0.5 bg-gradient-to-r from-orange-500 to-brand-accent rounded-3xl blur opacity-20 group-focus-within:opacity-40 transition duration-500"></div>
      <div class="relative bg-white dark:bg-slate-900 rounded-3xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden flex items-center">
        <div class="pl-6 pointer-events-none">
          <FireIcon class="h-6 w-6 text-orange-500" />
        </div>
        <input 
          v-model="newHabit" 
          @keyup.enter="addHabit" 
          placeholder="Build a new identity trait..." 
          class="flex-1 pl-4 pr-32 py-6 bg-transparent outline-none dark:text-white text-lg font-medium placeholder:text-slate-400"
        >
        <div class="pr-2">
          <button 
            @click="addHabit" 
            class="bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 rounded-2xl font-black text-xs uppercase tracking-widest shadow-xl shadow-orange-500/20 transition-all active:scale-95"
          >
            Track Habit
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="habits.length === 0" class="py-20 text-center bg-orange-50/30 dark:bg-orange-900/10 rounded-[3rem] border-2 border-dashed border-orange-100 dark:border-orange-900/30">
      <BoltIcon class="h-20 w-20 text-orange-200 dark:text-orange-900/50 mx-auto mb-6" />
      <h4 class="text-2xl font-black text-orange-400 dark:text-orange-500 uppercase tracking-tighter">Consistency Engine Offline</h4>
      <p class="text-orange-400/70 mt-2 font-medium italic">Small daily wins lead to massive results.</p>
    </div>

    <!-- Habits List -->
    <div class="grid grid-cols-1 gap-6">
      <div v-for="habit in habits" :key="habit.id" class="group bg-white dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700 p-8 rounded-[2.5rem] shadow-sm hover:shadow-xl hover:border-orange-500/30 transition-all duration-500 relative overflow-hidden">
        
        <div class="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
          <FireIcon class="h-24 w-24 text-orange-500 -rotate-12" />
        </div>

        <div class="flex flex-col md:flex-row md:items-center justify-between gap-8 relative z-10">
          <div class="flex items-center gap-6 flex-1 min-w-0">
            <button 
              @click="completeHabit(habit.id)" 
              :disabled="habit.last_completed_date === today"
              :class="[
                habit.last_completed_date === today 
                  ? 'bg-orange-500 text-white border-orange-500 shadow-lg shadow-orange-500/20' 
                  : 'border-slate-200 dark:border-slate-700 hover:border-orange-500 hover:bg-orange-50 dark:hover:bg-orange-900/20',
                'w-16 h-16 rounded-[1.5rem] border-2 flex items-center justify-center transition-all shrink-0'
              ]"
            >
              <CheckIcon class="h-8 w-8" />
            </button>
            <div class="min-w-0">
              <h5 class="text-2xl font-black text-slate-800 dark:text-white truncate tracking-tight group-hover:text-orange-500 transition-colors">{{ habit.description }}</h5>
              <div class="flex items-center gap-4 mt-2">
                <div class="flex items-center gap-1.5 text-xs font-black text-orange-500 bg-orange-50 dark:bg-orange-900/20 px-3 py-1 rounded-full uppercase tracking-widest">
                  <FireIcon class="h-3.5 w-3.5" />
                  {{ habit.current_streak }} Day Streak
                </div>
                <div class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">
                  Personal Best: {{ habit.highest_streak }}
                </div>
              </div>
            </div>
          </div>


          <div class="flex items-center gap-4 pl-4 md:border-l border-slate-100 dark:border-slate-700/50">
            <button @click="askCoach(habit)" class="p-3 text-slate-300 hover:text-brand-calm hover:bg-brand-calm/10 rounded-xl transition-colors" title="Ask AI Coach for Insights">
              <ChatBubbleLeftEllipsisIcon class="h-6 w-6" />
            </button>
            <button @click="deleteHabit(habit.id)" class="p-3 text-slate-300 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-xl opacity-0 group-hover:opacity-100 transition-all transform translate-x-2 group-hover:translate-x-0" title="Delete Habit">

              <TrashIcon class="h-6 w-6" />
            </button>
          </div>
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
  BoltIcon,
  ChatBubbleLeftEllipsisIcon
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

const askCoach = async (habit: any) => {
  showToast("Analyzing streak patterns...")
  const res = await fetch('/api/coach/insights', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      habit_description: habit.description,
      current_streak: habit.current_streak
    })
  })
  if (res.ok) {
    const data = await res.json()
    alert("AI Coach Insight:\n\n" + data.insight) // Quick and dirty UI for the insight
  } else {
    showToast("Coach is currently unavailable.")
  }
}
</script>
