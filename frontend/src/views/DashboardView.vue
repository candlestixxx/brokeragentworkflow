<template>
  <div class="space-y-12 animate-fade-in">
    
    <!-- High-Impact Hero Section -->
    <header class="relative group">
      <div class="absolute -inset-1 bg-gradient-to-r from-brand-calm to-brand-accent rounded-[3rem] blur opacity-25 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
      <div class="relative bg-white dark:bg-slate-800 rounded-[2.5rem] p-10 md:p-14 shadow-2xl border border-slate-100 dark:border-slate-700 flex flex-col md:flex-row items-center justify-between gap-10 overflow-hidden">
        
        <div class="flex-1 space-y-6 text-center md:text-left relative z-10">
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-brand-calm/10 rounded-full text-brand-calm font-black text-xs uppercase tracking-widest">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-calm opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-brand-calm"></span>
            </span>
            System Online
          </div>
          
          <h2 class="text-5xl md:text-6xl font-black text-slate-900 dark:text-white tracking-tighter leading-none">
            Welcome back, <br/>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-calm to-brand-accent">{{ user.username }}</span>
          </h2>
          
          <p class="text-xl text-slate-500 dark:text-slate-400 font-medium max-w-lg leading-relaxed">
            You've completed <span class="text-slate-900 dark:text-white font-bold">{{ analytics.completed_goals }} goals</span> so far. Ready to win the next minute?
          </p>

          <div class="flex flex-wrap items-center gap-4 justify-center md:justify-start">
            <div class="px-6 py-3 bg-slate-50 dark:bg-slate-900/50 rounded-2xl border border-slate-100 dark:border-slate-700 flex items-center gap-3 shadow-sm">
              <CalendarIcon class="h-6 w-6 text-brand-calm" />
              <span class="text-sm font-bold text-slate-700 dark:text-slate-200 uppercase tracking-wide">{{ todayDate }}</span>
            </div>
          </div>
        </div>

        <div class="flex-shrink-0 relative hidden lg:block">
          <div class="w-64 h-64 bg-brand-calm/5 rounded-full flex items-center justify-center animate-pulse">
            <div class="w-48 h-48 bg-brand-calm/10 rounded-full flex items-center justify-center">
              <RocketLaunchIcon class="h-24 w-24 text-brand-calm -rotate-12" />
            </div>
          </div>
          <!-- Floating mini-stats -->
          <div class="absolute -top-4 -right-4 bg-white dark:bg-slate-700 p-4 rounded-2xl shadow-xl border border-slate-100 dark:border-slate-600 animate-bounce" style="animation-duration: 3s;">
            <FireIcon class="h-6 w-6 text-orange-500 mx-auto" />
            <p class="text-xs font-black text-center mt-1">{{ analytics.longest_streak }}D Streak</p>
          </div>
        </div>

      </div>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
      
      <!-- Primary Action Area -->
      <div class="lg:col-span-8 space-y-10">
        
        <section class="bg-white dark:bg-slate-800 rounded-[2.5rem] shadow-xl shadow-slate-200/50 dark:shadow-none border border-slate-100 dark:border-slate-700 overflow-hidden transition-all duration-300">
          <TabGroup>
            <div class="bg-slate-50/50 dark:bg-slate-900/50 px-8 py-6 border-b border-slate-100 dark:border-slate-700 flex flex-col sm:flex-row sm:items-center justify-between gap-6">
              <div class="flex items-center gap-4">
                <div class="w-3 h-8 bg-brand-calm rounded-full"></div>
                <h3 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight uppercase">Daily Focus</h3>
              </div>
              
              <TabList class="flex p-1.5 space-x-1.5 bg-slate-200/50 dark:bg-slate-800 rounded-2xl">
                <Tab as="template" v-slot="{ selected }">
                  <button :class="[selected ? 'bg-white dark:bg-slate-700 text-brand-calm dark:text-brand-accent shadow-sm scale-105' : 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200', 'px-6 py-2.5 rounded-xl font-black text-xs uppercase tracking-widest transition-all outline-none']">
                    Active
                  </button>
                </Tab>
                <Tab as="template" v-slot="{ selected }">
                  <button :class="[selected ? 'bg-white dark:bg-slate-700 text-brand-calm dark:text-brand-accent shadow-sm scale-105' : 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200', 'px-6 py-2.5 rounded-xl font-black text-xs uppercase tracking-widest transition-all outline-none']">
                    History
                  </button>
                </Tab>
                <Tab as="template" v-slot="{ selected }">
                  <button :class="[selected ? 'bg-white dark:bg-slate-700 text-brand-calm dark:text-brand-accent shadow-sm scale-105' : 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200', 'px-6 py-2.5 rounded-xl font-black text-xs uppercase tracking-widest transition-all outline-none']">
                    Calendar
                  </button>
                </Tab>
                <Tab as="template" v-slot="{ selected }">
                  <button :class="[selected ? 'bg-white dark:bg-slate-700 text-brand-calm dark:text-brand-accent shadow-sm scale-105' : 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200', 'px-6 py-2.5 rounded-xl font-black text-xs uppercase tracking-widest transition-all outline-none']">
                    Habits
                  </button>
                </Tab>
              </TabList>
            </div>

            <TabPanels class="p-8">
              <TabPanel class="outline-none focus:outline-none focus-visible:ring-0">
                <ActiveGoals />
              </TabPanel>
              <TabPanel class="outline-none focus:outline-none focus-visible:ring-0">
                <CompletedGoals />
              </TabPanel>
              <TabPanel class="outline-none focus:outline-none focus-visible:ring-0">
                <CalendarGoals />
              </TabPanel>
              <TabPanel class="outline-none focus:outline-none focus-visible:ring-0">
                <HabitsTracker />
              </TabPanel>
            </TabPanels>
          </TabGroup>
        </section>

      </div>

      <!-- Sidebar / Insights Area -->
      <aside class="lg:col-span-4 space-y-10">
        <QuarterlyInitiatives />
        
        <!-- Helpful Guide Card -->
        <div class="bg-gradient-to-br from-slate-800 to-slate-900 dark:from-slate-900 dark:to-black p-8 rounded-[2.5rem] shadow-2xl text-white relative overflow-hidden group">
          <div class="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
            <LightBulbIcon class="h-24 w-24 text-yellow-400" />
          </div>
          <h4 class="text-xl font-black uppercase tracking-tighter mb-4 relative z-10">Need a refresh?</h4>
          <p class="text-slate-400 font-medium text-sm leading-relaxed mb-8 relative z-10">
            Re-run the interactive onboarding guide to learn more about micro-wins and AI power-ups.
          </p>
          <button 
            @click="user.has_completed_onboarding = false"
            class="w-full bg-white text-slate-900 py-4 rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-brand-accent hover:text-white transition-all active:scale-95 relative z-10 shadow-xl"
          >
            Launch Guide
          </button>
        </div>
      </aside>

    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue'
import { 
  CalendarIcon, 
  RocketLaunchIcon, 
  FireIcon,
  LightBulbIcon
} from '@heroicons/vue/24/outline'
import { user, analytics } from '../store'
import ActiveGoals from '../components/ActiveGoals.vue'
import CompletedGoals from '../components/CompletedGoals.vue'
import CalendarGoals from '../components/CalendarGoals.vue'
import QuarterlyInitiatives from '../components/QuarterlyInitiatives.vue'
import HabitsTracker from '../components/HabitsTracker.vue'

const todayDate = computed(() => {
  return new Date().toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
})
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
