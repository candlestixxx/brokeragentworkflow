<template>
  <div class="space-y-8">
    <div v-if="Object.keys(calendarGoals).length === 0" class="py-12 text-center bg-slate-50 dark:bg-slate-900/50 rounded-3xl border-2 border-dashed border-slate-200 dark:border-slate-800">
      <CalendarDaysIcon class="h-12 w-12 text-slate-300 mx-auto mb-4" />
      <h4 class="text-xl font-bold text-slate-400 dark:text-slate-500">History is empty.</h4>
    </div>

    <div v-else class="space-y-10">
      <div v-for="(goals, date) in calendarGoals" :key="date" class="relative pl-8 border-l-2 border-slate-100 dark:border-slate-700">
        <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-brand-calm shadow-lg shadow-brand-calm/30 ring-4 ring-white dark:ring-slate-800"></div>
        
        <h4 class="text-sm font-bold text-brand-calm dark:text-brand-accent uppercase tracking-widest mb-4">{{ formatDate(date) }}</h4>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div v-for="goal in goals" :key="goal.id" :class="[
            goal.status === 'completed' ? 'bg-green-50/50 dark:bg-green-900/10 border-green-100 dark:border-green-900/30' : 'bg-white dark:bg-slate-800 border-slate-100 dark:border-slate-700',
            'p-3 rounded-xl border shadow-sm flex items-center gap-3 transition-all'
          ]">
            <CheckCircleIcon v-if="goal.status === 'completed'" class="h-5 w-5 text-green-500 shrink-0" />
            <div v-else class="w-5 h-5 rounded-full border-2 border-slate-200 dark:border-slate-700 shrink-0"></div>
            <span :class="[
              goal.status === 'completed' ? 'text-slate-500 dark:text-slate-500 line-through' : 'text-slate-700 dark:text-slate-200',
              'text-sm font-medium truncate'
            ]">{{ goal.description }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CalendarDaysIcon, CheckCircleIcon } from '@heroicons/vue/24/outline'
import { calendarGoals } from '../store'

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}
</script>
