<template>
  <div class="space-y-6">
    <div v-if="completedGoals.length === 0" class="py-12 text-center bg-slate-50 dark:bg-slate-900/50 rounded-3xl border-2 border-dashed border-slate-200 dark:border-slate-800">
      <ArchiveBoxIcon class="h-12 w-12 text-slate-300 mx-auto mb-4" />
      <h4 class="text-xl font-bold text-slate-400 dark:text-slate-500">No completed goals yet.</h4>
      <p class="text-slate-400 dark:text-slate-600 mt-1 italic">The journey of a thousand miles begins with a single step.</p>
    </div>

    <div v-else class="space-y-4">
      <div v-for="goal in completedGoals" :key="goal.id" class="flex items-center gap-4 bg-slate-50/50 dark:bg-slate-900/30 p-4 rounded-2xl border border-slate-100 dark:border-slate-700/50 group">
        <div class="bg-green-100 dark:bg-green-900/30 p-2 rounded-full">
          <CheckIcon class="h-5 w-5 text-green-600 dark:text-green-400" />
        </div>
        <span class="text-slate-600 dark:text-slate-400 font-medium line-through decoration-slate-300 dark:decoration-slate-600">{{ goal.description }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArchiveBoxIcon, CheckIcon } from '@heroicons/vue/24/outline'
import { completedGoals } from '../store'
</script>
