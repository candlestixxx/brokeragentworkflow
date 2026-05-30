<template>
  <div class="flex items-center justify-center space-x-4 mb-8">
    <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-100 transition-colors">One-Minute Manager Dashboard</h2>
    <div class="flex space-x-1" v-if="user.badges && user.badges.length > 0">
       <span v-for="badge in user.badges" :key="badge" class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-bold rounded-full border border-yellow-300" :title="badge">🏆 {{badge}}</span>
    </div>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
    <!-- Daily Goals Column -->
    <div class="flex flex-col h-full">
      <section class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8 flex-1 transition-colors">
        <TabGroup>
          <div class="flex flex-col gap-3 lg:flex-row lg:justify-between border-b border-gray-100 dark:border-gray-700 pb-3 mb-4">
            <h2 class="text-2xl font-semibold text-gray-800 dark:text-gray-100 transition-colors">Daily One-Minute Goals</h2>
            <TabList class="flex gap-2">
              <Tab as="template" v-slot="{ selected }">
                <button :class="[selected ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200', 'px-3 py-1 rounded font-medium text-sm transition outline-none']">Active</button>
              </Tab>
              <Tab as="template" v-slot="{ selected }">
                <button :class="[selected ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200', 'px-3 py-1 rounded font-medium text-sm transition outline-none']">History</button>
              </Tab>
              <Tab as="template" v-slot="{ selected }">
                <button :class="[selected ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200', 'px-3 py-1 rounded font-medium text-sm transition outline-none']">Calendar</button>
              </Tab>
              <Tab as="template" v-slot="{ selected }">
                <button :class="[selected ? 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200', 'px-3 py-1 rounded font-medium text-sm transition outline-none']">Habits</button>
              </Tab>
            </TabList>
          </div>

          <TabPanels>
            <TabPanel><ActiveGoals /></TabPanel>
            <TabPanel><CompletedGoals /></TabPanel>
            <TabPanel><CalendarGoals /></TabPanel>
            <TabPanel><HabitsTracker /></TabPanel>
          </TabPanels>
        </TabGroup>
      </section>
    </div>

    <!-- Quarterly Initiatives Column -->
    <div class="flex flex-col h-full">
      <QuarterlyInitiatives />
    </div>
  </div>
</template>

<script setup lang="ts">
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue'
import ActiveGoals from '../components/ActiveGoals.vue'
import CompletedGoals from '../components/CompletedGoals.vue'
import CalendarGoals from '../components/CalendarGoals.vue'
import QuarterlyInitiatives from '../components/QuarterlyInitiatives.vue'
import HabitsTracker from '../components/HabitsTracker.vue'
import { user } from '../store'
</script>
