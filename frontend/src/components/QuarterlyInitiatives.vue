<template>
  <div class="space-y-6">
    <section class="bg-white dark:bg-slate-800 rounded-3xl shadow-xl shadow-slate-200/50 dark:shadow-none border border-slate-100 dark:border-slate-700 overflow-hidden transition-colors duration-300">
      <div class="bg-slate-50/50 dark:bg-slate-900/50 px-6 py-4 border-b border-slate-100 dark:border-slate-700 flex items-center gap-3">
        <div class="bg-brand-accent/20 p-1.5 rounded-lg">
          <PresentationChartLineIcon class="h-5 w-5 text-brand-calm dark:text-brand-accent" />
        </div>
        <h3 class="text-lg font-bold text-slate-900 dark:text-white uppercase tracking-tight">Quarterly Initiatives</h3>
      </div>

      <div class="p-6 space-y-6">
        <form @submit.prevent="addInitiative" class="space-y-3">
          <div class="grid grid-cols-3 gap-2">
            <select v-model="newInitQuarter" class="col-span-1 px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white font-bold">
              <option>Q1</option>
              <option>Q2</option>
              <option>Q3</option>
              <option>Q4</option>
            </select>
            <input 
              v-model="newInitDescription" 
              placeholder="Primary objective..." 
              class="col-span-2 px-3 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white font-medium"
            >
          </div>
          <button type="submit" class="w-full bg-slate-900 dark:bg-slate-700 hover:bg-black dark:hover:bg-slate-600 text-white py-2.5 rounded-xl font-bold text-xs uppercase tracking-widest shadow-lg transition-all active:scale-95 flex items-center justify-center gap-2">
            <PlusIcon class="h-4 w-4" />
            Launch Initiative
          </button>
        </form>

        <div v-if="initiatives.length === 0" class="py-8 text-center bg-slate-50/50 dark:bg-slate-900/30 rounded-2xl border-2 border-dashed border-slate-100 dark:border-slate-800">
          <p class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest leading-loose">Think big.<br>Set your trajectory.</p>
        </div>

        <div v-else class="space-y-3">
          <div v-for="[id, quarter, description] in initiatives" :key="id" class="group bg-slate-50/50 dark:bg-slate-900/30 p-4 rounded-2xl border border-slate-100 dark:border-slate-700/50 hover:border-brand-calm/30 transition-all">
            <div class="flex items-start justify-between gap-3">
              <div class="flex-1 min-w-0">
                <span class="inline-block px-2 py-0.5 bg-brand-calm text-white text-[10px] font-black rounded-md mb-2">{{ quarter }}</span>
                <p class="text-sm font-bold text-slate-800 dark:text-slate-200 leading-relaxed">{{ description }}</p>
              </div>
              <button @click="completeInitiative(id)" class="p-1.5 text-slate-400 hover:text-green-500 hover:bg-green-50 dark:hover:bg-green-900/20 rounded-lg transition-all" title="Complete">
                <CheckCircleIcon class="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Progress Card -->
    <div class="bg-gradient-to-br from-brand-calm to-brand-accent p-6 rounded-3xl shadow-xl shadow-brand-calm/20 text-white overflow-hidden relative group">
      <SparklesIcon class="absolute -right-4 -bottom-4 h-32 w-32 text-white/10 group-hover:rotate-12 transition-transform duration-700" />
      <h4 class="text-lg font-black uppercase tracking-tighter">Current Momentum</h4>
      <div class="mt-4 flex items-end gap-2">
        <span class="text-4xl font-black">{{ initiatives.length }}</span>
        <span class="text-sm font-bold text-white/80 mb-1.5 uppercase tracking-widest">Active Initiatives</span>
      </div>
      <div class="mt-6 h-1.5 w-full bg-white/20 rounded-full overflow-hidden">
        <div class="h-full bg-white rounded-full transition-all duration-1000" :style="{ width: initiatives.length > 0 ? '65%' : '0%' }"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { 
  PresentationChartLineIcon, 
  PlusIcon, 
  CheckCircleIcon,
  SparklesIcon
} from '@heroicons/vue/24/outline'
import { initiatives, showToast } from '../store'

const newInitQuarter = ref('Q1')
const newInitDescription = ref('')

const addInitiative = async () => {
  if (!newInitDescription.value.trim()) return
  const res = await fetch('/api/initiatives', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ quarter: newInitQuarter.value, description: newInitDescription.value })
  })
  if (res.ok) {
    newInitDescription.value = ''
    showToast("Initiative launched!")
  }
}

const completeInitiative = async (id: number) => {
  const res = await fetch(`/api/initiatives/${id}/complete`, { method: 'POST' })
  if (res.ok) {
    showToast("Initiative completed. Great work!")
  }
}
</script>
