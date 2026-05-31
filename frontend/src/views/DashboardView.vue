<template>
  <div class="space-y-8 animate-fade-in">
    <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
      <div>
        <h2 class="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          Welcome back, <span class="text-brand-calm dark:text-brand-accent">{{ user.username }}</span>
        </h2>
        <p class="text-slate-500 dark:text-slate-400 mt-1 font-medium">
          Here's what's happening with your goals today.
        </p>
      </div>
      <div class="flex items-center gap-3">
        <div class="px-4 py-2 bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 flex items-center gap-2">
          <CalendarIcon class="h-5 w-5 text-brand-calm" />
          <span class="text-sm font-bold text-slate-700 dark:text-slate-200">{{ todayDate }}</span>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
      <!-- Main Content Column -->
      <div class="lg:col-span-2 space-y-8">
        <section class="bg-white dark:bg-slate-800 rounded-3xl shadow-xl shadow-slate-200/50 dark:shadow-none border border-slate-100 dark:border-slate-700 overflow-hidden transition-colors duration-300">
          <TabGroup>
            <div class="bg-slate-50/50 dark:bg-slate-900/50 px-6 py-4 border-b border-slate-100 dark:border-slate-700 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div class="flex items-center gap-2">
                <div class="w-2 h-6 bg-brand-calm rounded-full"></div>
                <h3 class="text-lg font-bold text-slate-900 dark:text-white">Daily Focus</h3>
              </div>
              <TabList class="flex p-1 space-x-1 bg-slate-200/50 dark:bg-slate-800 rounded-xl">
                <Tab as="template" v-slot="{ selected }">
                  <button :class="[selected ? 'bg-white dark:bg-slate-700 text-brand-calm dark:text-brand-accent shadow-sm' : 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200', 'px-4 py-1.5 rounded-lg font-bold text-xs uppercase tracking-wider transition-all outline-none']">
                    Active
                  </button>
                </Tab>
                <Tab as="template" v-slot="{ selected }">
                  <button :class="[selected ? 'bg-white dark:bg-slate-700 text-brand-calm dark:text-brand-accent shadow-sm' : 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200', 'px-4 py-1.5 rounded-lg font-bold text-xs uppercase tracking-wider transition-all outline-none']">
                    History
                  </button>
                </Tab>
                <Tab as="template" v-slot="{ selected }">
                  <button :class="[selected ? 'bg-white dark:bg-slate-700 text-brand-calm dark:text-brand-accent shadow-sm' : 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200', 'px-4 py-1.5 rounded-lg font-bold text-xs uppercase tracking-wider transition-all outline-none']">
                    Calendar
                  </button>
                </Tab>
                <Tab as="template" v-slot="{ selected }">
                  <button :class="[selected ? 'bg-white dark:bg-slate-700 text-brand-calm dark:text-brand-accent shadow-sm' : 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200', 'px-4 py-1.5 rounded-lg font-bold text-xs uppercase tracking-wider transition-all outline-none']">
                    Habits
                  </button>
                </Tab>
              </TabList>
            </div>

            <TabPanels class="p-6">
              <TabPanel class="outline-none focus:outline-none"><ActiveGoals /></TabPanel>
              <TabPanel class="outline-none focus:outline-none"><CompletedGoals /></TabPanel>
              <TabPanel class="outline-none focus:outline-none"><CalendarGoals /></TabPanel>
              <TabPanel class="outline-none focus:outline-none"><HabitsTracker /></TabPanel>
            </TabPanels>
          </TabGroup>
        </section>
      </div>

      <!-- Sidebar Column -->
      <div class="space-y-8">
        <QuarterlyInitiatives />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue'
import { CalendarIcon } from '@heroicons/vue/24/outline'
import { user } from '../store'
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
