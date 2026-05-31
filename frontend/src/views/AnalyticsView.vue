<template>
  <div class="space-y-8 animate-fade-in">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <h2 class="text-3xl font-black text-slate-900 dark:text-white tracking-tight uppercase">Performance Analytics</h2>
      <div class="flex items-center gap-2 text-sm font-bold text-slate-500 uppercase tracking-widest bg-white dark:bg-slate-800 px-4 py-2 rounded-xl border border-slate-100 dark:border-slate-700 shadow-sm">
        <ChartBarSquareIcon class="h-5 w-5 text-brand-calm" />
        Live Metrics
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Metric Card -->
      <div class="bg-white dark:bg-slate-800 p-6 rounded-3xl shadow-xl shadow-slate-200/50 dark:shadow-none border border-slate-100 dark:border-slate-700 relative overflow-hidden group transition-all hover:-translate-y-1">
        <div class="absolute -right-2 -top-2 opacity-10 group-hover:scale-110 transition-transform duration-500">
          <CheckCircleIcon class="h-24 w-24 text-brand-calm" />
        </div>
        <h3 class="text-xs font-black text-slate-400 dark:text-slate-500 uppercase tracking-[0.2em] mb-1">Goals Completed</h3>
        <p class="text-4xl font-black text-slate-900 dark:text-white">{{ analytics.completed_goals }}</p>
        <div class="mt-4 flex items-center gap-1.5 text-[10px] font-bold text-green-500 bg-green-50 dark:bg-green-900/20 px-2 py-0.5 rounded-full w-max uppercase tracking-tighter">
          All Time
        </div>
      </div>

      <div class="bg-white dark:bg-slate-800 p-6 rounded-3xl shadow-xl shadow-slate-200/50 dark:shadow-none border border-slate-100 dark:border-slate-700 relative overflow-hidden group transition-all hover:-translate-y-1">
        <div class="absolute -right-2 -top-2 opacity-10 group-hover:scale-110 transition-transform duration-500">
          <FireIcon class="h-24 w-24 text-orange-500" />
        </div>
        <h3 class="text-xs font-black text-slate-400 dark:text-slate-500 uppercase tracking-[0.2em] mb-1">Longest Streak</h3>
        <p class="text-4xl font-black text-slate-900 dark:text-white">{{ analytics.longest_streak }} <span class="text-lg font-bold text-slate-400">days</span></p>
        <div class="mt-4 flex items-center gap-1.5 text-[10px] font-bold text-orange-500 bg-orange-50 dark:bg-orange-900/20 px-2 py-0.5 rounded-full w-max uppercase tracking-tighter">
          Peak Momentum
        </div>
      </div>

      <div class="bg-white dark:bg-slate-800 p-6 rounded-3xl shadow-xl shadow-slate-200/50 dark:shadow-none border border-slate-100 dark:border-slate-700 relative overflow-hidden group transition-all hover:-translate-y-1">
        <div class="absolute -right-2 -top-2 opacity-10 group-hover:scale-110 transition-transform duration-500">
          <ArrowPathIcon class="h-24 w-24 text-brand-accent" />
        </div>
        <h3 class="text-xs font-black text-slate-400 dark:text-slate-500 uppercase tracking-[0.2em] mb-1">Daily Habits</h3>
        <p class="text-4xl font-black text-slate-900 dark:text-white">{{ analytics.total_habits }}</p>
        <div class="mt-4 flex items-center gap-1.5 text-[10px] font-bold text-brand-accent bg-brand-accent/10 px-2 py-0.5 rounded-full w-max uppercase tracking-tighter">
          Active Systems
        </div>
      </div>

      <div class="bg-white dark:bg-slate-800 p-6 rounded-3xl shadow-xl shadow-slate-200/50 dark:shadow-none border border-slate-100 dark:border-slate-700 relative overflow-hidden group transition-all hover:-translate-y-1">
        <div class="absolute -right-2 -top-2 opacity-10 group-hover:scale-110 transition-transform duration-500">
          <PresentationChartLineIcon class="h-24 w-24 text-indigo-500" />
        </div>
        <h3 class="text-xs font-black text-slate-400 dark:text-slate-500 uppercase tracking-[0.2em] mb-1">Initiatives</h3>
        <p class="text-4xl font-black text-slate-900 dark:text-white">{{ analytics.active_initiatives }}</p>
        <div class="mt-4 flex items-center gap-1.5 text-[10px] font-bold text-indigo-500 bg-indigo-50 dark:bg-indigo-900/20 px-2 py-0.5 rounded-full w-max uppercase tracking-tighter">
          Big Objectives
        </div>
      </div>
    </div>

    <!-- Charts Placeholder / Visual Breakdown -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-12">
      <section class="bg-slate-900 rounded-[2rem] p-10 text-white relative overflow-hidden shadow-2xl">
        <div class="relative z-10">
          <h4 class="text-2xl font-black uppercase tracking-tighter mb-2">Weekly Velocity</h4>
          <p class="text-slate-400 font-medium mb-8">Visualization of your goal completion throughput.</p>
          <div class="flex items-end gap-3 h-48">
            <div v-for="i in 7" :key="i" class="flex-1 bg-white/10 rounded-t-xl hover:bg-brand-accent/50 transition-all cursor-pointer relative group" :style="{ height: `${[40, 65, 30, 85, 55, 95, 70][i-1]}%` }">
              <div class="absolute -top-8 left-1/2 -translate-x-1/2 bg-white text-slate-900 px-2 py-1 rounded-md text-[10px] font-black opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                {{ [4, 6, 3, 8, 5, 9, 7][i-1] }} Goals
              </div>
            </div>
          </div>
          <div class="flex justify-between mt-4 text-[10px] font-black text-slate-500 uppercase tracking-widest">
            <span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span>
          </div>
        </div>
        <div class="absolute top-0 right-0 w-64 h-64 bg-brand-calm opacity-20 blur-[100px] -mr-32 -mt-32 rounded-full"></div>
      </section>

      <section class="bg-white dark:bg-slate-800 rounded-[2rem] p-10 border border-slate-100 dark:border-slate-700 shadow-xl shadow-slate-200/50 dark:shadow-none">
        <h4 class="text-2xl font-black text-slate-900 dark:text-white uppercase tracking-tighter mb-8">Focus Distribution</h4>
        <div class="space-y-6">
          <div v-for="category in ['Real Estate', 'Operations', 'Networking', 'Learning']" :key="category" class="space-y-2">
            <div class="flex justify-between text-xs font-black uppercase tracking-widest">
              <span class="text-slate-600 dark:text-slate-400">{{ category }}</span>
              <span class="text-brand-calm dark:text-brand-accent">{{ Math.floor(Math.random() * 50) + 10 }}%</span>
            </div>
            <div class="h-2 w-full bg-slate-100 dark:bg-slate-900 rounded-full overflow-hidden">
              <div class="h-full bg-brand-calm dark:bg-brand-accent transition-all duration-1000" :style="{ width: `${Math.floor(Math.random() * 50) + 30}%` }"></div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { 
  ChartBarSquareIcon, 
  CheckCircleIcon, 
  FireIcon, 
  ArrowPathIcon, 
  PresentationChartLineIcon 
} from '@heroicons/vue/24/outline'
import { analytics } from '../store'
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
