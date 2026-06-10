<template>
  <div class="space-y-8">
    <section class="bg-white dark:bg-slate-800 rounded-[2.5rem] shadow-xl shadow-slate-200/50 dark:shadow-none border border-slate-100 dark:border-slate-700 overflow-hidden transition-all duration-300">
      <div class="bg-slate-50/50 dark:bg-slate-900/50 px-8 py-6 border-b border-slate-100 dark:border-slate-700 flex items-center gap-4">
        <div class="bg-brand-accent/20 p-2.5 rounded-2xl">
          <PresentationChartLineIcon class="h-6 w-6 text-brand-calm dark:text-brand-accent" />
        </div>
        <h3 class="text-xl font-black text-slate-900 dark:text-white uppercase tracking-tight">Macro Vision</h3>
      </div>
      
      <div class="p-8 space-y-8">
        <form @submit.prevent="addInitiative" class="space-y-4">
          <div class="grid grid-cols-4 gap-3">
            <select v-model="newInitQuarter" class="col-span-1 px-4 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-2xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white font-black uppercase tracking-widest">
              <option>Q1</option>
              <option>Q2</option>
              <option>Q3</option>
              <option>Q4</option>
            </select>
            <input 
              v-model="newInitDescription" 
              placeholder="Primary objective..." 
              class="col-span-3 px-5 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-2xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white font-medium"
            >
          </div>
          <button type="submit" class="w-full bg-slate-900 dark:bg-slate-700 hover:bg-black dark:hover:bg-slate-600 text-white py-4 rounded-2xl font-black text-xs uppercase tracking-widest shadow-xl transition-all active:scale-95 flex items-center justify-center gap-3">
            <PlusIcon class="h-4 w-4" />
            Launch Initiative
          </button>
        </form>

        <div v-if="initiatives.length === 0" class="py-10 text-center bg-slate-50/50 dark:bg-slate-900/30 rounded-3xl border-2 border-dashed border-slate-100 dark:border-slate-800">
          <p class="text-xs font-black text-slate-400 dark:text-slate-500 uppercase tracking-widest leading-loose">
            Think big.<br/>Set your trajectory.
          </p>
        </div>

        <div v-else class="space-y-4">
          <div v-for="{id, quarter, description} in initiatives" :key="id" class="group bg-slate-50/50 dark:bg-slate-900/30 p-5 rounded-2xl border border-slate-100 dark:border-slate-700/50 hover:border-brand-calm/30 transition-all">
            <div class="flex items-start justify-between gap-4">
              <div class="flex-1 min-w-0">
                <span class="inline-block px-3 py-1 bg-brand-calm text-white text-[10px] font-black rounded-lg mb-3 uppercase tracking-widest">{{ quarter }}</span>
                <p class="text-sm font-bold text-slate-800 dark:text-slate-200 leading-relaxed">{{ description }}</p>
              </div>
              <button @click="completeInitiative(id)" class="p-2 text-slate-400 hover:text-green-500 hover:bg-green-50 dark:hover:bg-green-900/20 rounded-xl transition-all" title="Complete">
                <CheckCircleIcon class="h-6 w-6" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Momentum Card -->
    <div class="bg-gradient-to-br from-brand-calm to-brand-accent p-8 rounded-[2.5rem] shadow-2xl text-white overflow-hidden relative group">
      <div class="absolute -right-6 -bottom-6 h-40 w-40 text-white/10 group-hover:rotate-12 transition-transform duration-700">
        <SparklesIcon class="h-full w-full" />
      </div>
      <h4 class="text-lg font-black uppercase tracking-widest mb-6">Current Momentum</h4>
      <div class="flex items-end gap-3 mb-6">
        <span class="text-5xl font-black leading-none">{{ initiatives.length }}</span>
        <span class="text-sm font-black text-white/80 mb-1.5 uppercase tracking-widest">Active Tracks</span>
      </div>
      <div class="h-2 w-full bg-white/20 rounded-full overflow-hidden">
        <div 
          class="h-full bg-white rounded-full transition-all duration-1000" 
          :style="{ width: initiatives.length > 0 ? '65%' : '0%' }"
        />
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
