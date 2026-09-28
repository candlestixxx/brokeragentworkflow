<template>
  <div class="space-y-16 animate-fade-in">

    <!-- Hero Header -->
    <div class="text-center max-w-3xl mx-auto space-y-6">
      <div class="inline-flex items-center gap-2 px-4 py-2 bg-brand-calm/10 rounded-full text-brand-calm font-black text-xs uppercase tracking-[0.2em]">
        Micro-To-Macro Planner
      </div>
      <h2 class="text-4xl sm:text-5xl md:text-7xl font-black text-slate-900 dark:text-white tracking-tighter leading-none">
        Vision <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-calm to-brand-accent">Mapping</span>
      </h2>
      <p class="text-xl text-slate-500 dark:text-slate-400 font-medium leading-relaxed">
        Break down your 3-Month Look-Ahead buffer into actionable granular steps.
      </p>
    </div>

    <!-- Planner Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">

      <!-- Yearly Plan -->
      <section class="bg-white dark:bg-slate-800 rounded-3xl shadow-sm border border-slate-100 dark:border-slate-700 p-8 flex flex-col gap-6">
        <h3 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight uppercase">Yearly Plan</h3>
        <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">High-level production volume, GCI goals, and major community events.</p>

        <form @submit.prevent="addPlan('yearly')" class="space-y-4">
          <div class="flex flex-col gap-3">
            <input v-model="newPlanForm.yearly.period_name" placeholder="e.g. 2024" class="px-5 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white font-medium" required>
            <input v-model="newPlanForm.yearly.description" placeholder="Objective..." class="px-5 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white font-medium" required>
            <button type="submit" class="bg-brand-calm text-white py-3 rounded-xl font-black text-xs uppercase tracking-widest hover:bg-brand-calm/90 transition-all">Add Yearly Plan</button>
          </div>
        </form>

        <ul class="space-y-3 mt-4">
          <li v-for="plan in yearlyPlans" :key="plan.id" class="flex justify-between items-start bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl">
             <div>
                <span class="text-[10px] font-black uppercase text-brand-calm bg-brand-calm/10 px-2 py-1 rounded mb-2 inline-block">{{ plan.period_name }}</span>
                <p class="text-sm font-bold text-slate-700 dark:text-slate-300">{{ plan.description }}</p>
             </div>
             <button v-if="plan.status === 'pending'" @click="completePlan(plan.id)" class="text-slate-400 hover:text-green-500 transition-colors p-1" title="Mark Complete">
               <CheckCircleIcon class="w-6 h-6" />
             </button>
             <span v-else class="text-green-500"><CheckCircleIcon class="w-6 h-6 solid" /></span>
          </li>
        </ul>
      </section>

      <!-- Quarterly Plan -->
      <section class="bg-white dark:bg-slate-800 rounded-3xl shadow-sm border border-slate-100 dark:border-slate-700 p-8 flex flex-col gap-6">
        <h3 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight uppercase">Quarterly Plan</h3>
        <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">The 3-Month Look-Ahead buffer (setting up next quarter's marketing today).</p>

        <form @submit.prevent="addPlan('quarterly')" class="space-y-4">
          <div class="flex flex-col gap-3">
            <input v-model="newPlanForm.quarterly.period_name" placeholder="e.g. Q4" class="px-5 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white font-medium" required>
            <input v-model="newPlanForm.quarterly.description" placeholder="Objective..." class="px-5 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white font-medium" required>
            <button type="submit" class="bg-brand-calm text-white py-3 rounded-xl font-black text-xs uppercase tracking-widest hover:bg-brand-calm/90 transition-all">Add Quarterly Plan</button>
          </div>
        </form>

        <ul class="space-y-3 mt-4">
          <li v-for="plan in quarterlyPlans" :key="plan.id" class="flex justify-between items-start bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl">
             <div>
                <span class="text-[10px] font-black uppercase text-brand-calm bg-brand-calm/10 px-2 py-1 rounded mb-2 inline-block">{{ plan.period_name }}</span>
                <p class="text-sm font-bold text-slate-700 dark:text-slate-300">{{ plan.description }}</p>
             </div>
             <button v-if="plan.status === 'pending'" @click="completePlan(plan.id)" class="text-slate-400 hover:text-green-500 transition-colors p-1" title="Mark Complete">
               <CheckCircleIcon class="w-6 h-6" />
             </button>
             <span v-else class="text-green-500"><CheckCircleIcon class="w-6 h-6 solid" /></span>
          </li>
        </ul>
      </section>

      <!-- Monthly Plan -->
      <section class="bg-white dark:bg-slate-800 rounded-3xl shadow-sm border border-slate-100 dark:border-slate-700 p-8 flex flex-col gap-6">
        <h3 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight uppercase">Monthly Plan</h3>
        <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">Theme-based lead generation (e.g., Expireds, Geographic Farming, SOI).</p>

        <form @submit.prevent="addPlan('monthly')" class="space-y-4">
          <div class="flex flex-col gap-3">
            <input v-model="newPlanForm.monthly.period_name" placeholder="e.g. October" class="px-5 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white font-medium" required>
            <input v-model="newPlanForm.monthly.description" placeholder="Objective..." class="px-5 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white font-medium" required>
            <button type="submit" class="bg-brand-calm text-white py-3 rounded-xl font-black text-xs uppercase tracking-widest hover:bg-brand-calm/90 transition-all">Add Monthly Plan</button>
          </div>
        </form>

        <ul class="space-y-3 mt-4">
          <li v-for="plan in monthlyPlans" :key="plan.id" class="flex justify-between items-start bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl">
             <div>
                <span class="text-[10px] font-black uppercase text-brand-calm bg-brand-calm/10 px-2 py-1 rounded mb-2 inline-block">{{ plan.period_name }}</span>
                <p class="text-sm font-bold text-slate-700 dark:text-slate-300">{{ plan.description }}</p>
             </div>
             <button v-if="plan.status === 'pending'" @click="completePlan(plan.id)" class="text-slate-400 hover:text-green-500 transition-colors p-1" title="Mark Complete">
               <CheckCircleIcon class="w-6 h-6" />
             </button>
             <span v-else class="text-green-500"><CheckCircleIcon class="w-6 h-6 solid" /></span>
          </li>
        </ul>
      </section>

      <!-- Weekly Plan -->
      <section class="bg-white dark:bg-slate-800 rounded-3xl shadow-sm border border-slate-100 dark:border-slate-700 p-8 flex flex-col gap-6">
        <h3 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight uppercase">Weekly Plan</h3>
        <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">Tracking active escrows, open house prep, and pipeline health.</p>

        <form @submit.prevent="addPlan('weekly')" class="space-y-4">
          <div class="flex flex-col gap-3">
            <input v-model="newPlanForm.weekly.period_name" placeholder="e.g. Week 42" class="px-5 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white font-medium" required>
            <input v-model="newPlanForm.weekly.description" placeholder="Objective..." class="px-5 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-calm outline-none text-sm dark:text-white font-medium" required>
            <button type="submit" class="bg-brand-calm text-white py-3 rounded-xl font-black text-xs uppercase tracking-widest hover:bg-brand-calm/90 transition-all">Add Weekly Plan</button>
          </div>
        </form>

        <ul class="space-y-3 mt-4">
          <li v-for="plan in weeklyPlans" :key="plan.id" class="flex justify-between items-start bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl">
             <div>
                <span class="text-[10px] font-black uppercase text-brand-calm bg-brand-calm/10 px-2 py-1 rounded mb-2 inline-block">{{ plan.period_name }}</span>
                <p class="text-sm font-bold text-slate-700 dark:text-slate-300">{{ plan.description }}</p>
             </div>
             <button v-if="plan.status === 'pending'" @click="completePlan(plan.id)" class="text-slate-400 hover:text-green-500 transition-colors p-1" title="Mark Complete">
               <CheckCircleIcon class="w-6 h-6" />
             </button>
             <span v-else class="text-green-500"><CheckCircleIcon class="w-6 h-6 solid" /></span>
          </li>
        </ul>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { CheckCircleIcon } from '@heroicons/vue/24/outline'
import { macroPlans, fetchData, showToast } from '../store'

const newPlanForm = ref({
  yearly: { period_name: '', description: '' },
  quarterly: { period_name: '', description: '' },
  monthly: { period_name: '', description: '' },
  weekly: { period_name: '', description: '' },
})

const yearlyPlans = computed(() => macroPlans.value.filter(p => p.plan_type === 'yearly'))
const quarterlyPlans = computed(() => macroPlans.value.filter(p => p.plan_type === 'quarterly'))
const monthlyPlans = computed(() => macroPlans.value.filter(p => p.plan_type === 'monthly'))
const weeklyPlans = computed(() => macroPlans.value.filter(p => p.plan_type === 'weekly'))

const addPlan = async (type: 'yearly'|'quarterly'|'monthly'|'weekly') => {
  const form = newPlanForm.value[type]
  if (!form.period_name.trim() || !form.description.trim()) return

  const res = await fetch('/api/planner', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      plan_type: type,
      period_name: form.period_name,
      description: form.description
    })
  })

  if (res.ok) {
    showToast(`${type.charAt(0).toUpperCase() + type.slice(1)} plan added.`)
    form.period_name = ''
    form.description = ''
    await fetchData()
  } else {
    showToast("Failed to add plan.", true)
  }
}

const completePlan = async (id: number) => {
  const res = await fetch(`/api/planner/${id}/complete`, { method: 'POST' })
  if (res.ok) {
    showToast("Plan marked complete!")
    await fetchData()
  } else {
    showToast("Failed to complete plan.", true)
  }
}
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