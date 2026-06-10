<template>
  <div class="space-y-16 animate-fade-in">
    
    <!-- Hero Header -->
    <div class="text-center max-w-3xl mx-auto space-y-6">
      <div class="inline-flex items-center gap-2 px-4 py-2 bg-brand-accent/10 rounded-full text-brand-calm dark:text-brand-accent font-black text-xs uppercase tracking-[0.2em]">
        <ChartBarIcon class="h-4 w-4" />
        Performance Analytics
      </div>
      <h2 class="text-5xl md:text-7xl font-black text-slate-900 dark:text-white tracking-tighter leading-none">
        Victory <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-calm to-brand-accent">Insights</span>
      </h2>
      <p class="text-xl text-slate-500 dark:text-slate-400 font-medium leading-relaxed">
        Your progress, quantified. We track the micro-wins that lead to macro transformations.
      </p>
    </div>

    <!-- Stats Grid -->
    <div v-if="loading" class="flex justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-brand-calm border-t-transparent opacity-20"></div>
    </div>
    
    <div v-else-if="error" class="text-center py-20 text-red-500 font-bold uppercase tracking-widest">
      {{ error }}
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
      <div v-for="stat in statsCards" :key="stat.label" class="group bg-white dark:bg-slate-800 p-8 rounded-[2.5rem] border border-slate-100 dark:border-slate-700 shadow-sm hover:shadow-2xl transition-all duration-500 relative overflow-hidden">
        <div :class="['absolute -right-4 -bottom-4 h-24 w-24 opacity-5 group-hover:opacity-10 transition-opacity', stat.colorClass]">
          <component :is="stat.icon" class="h-full w-full" />
        </div>
        <p class="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-4">{{ stat.label }}</p>
        <div class="flex items-baseline gap-2">
          <h4 class="text-5xl font-black text-slate-900 dark:text-white tracking-tighter">{{ stat.value }}</h4>
          <span v-if="stat.suffix" class="text-sm font-black text-slate-400 uppercase tracking-widest">{{ stat.suffix }}</span>
        </div>
      </div>
    </div>

    <!-- Trophy Case -->
    <section class="space-y-10">
      <div class="flex items-center gap-4">
        <div class="w-3 h-8 bg-brand-accent rounded-full"></div>
        <h3 class="text-3xl font-black text-slate-900 dark:text-white uppercase tracking-tighter">Trophy Case</h3>
      </div>

      <div v-if="user.badges.length === 0" class="py-20 text-center bg-slate-50/50 dark:bg-slate-900/30 rounded-[3rem] border-2 border-dashed border-slate-100 dark:border-slate-800">
        <TrophyIcon class="h-20 w-20 text-slate-200 dark:text-slate-700 mx-auto mb-6" />
        <h4 class="text-2xl font-black text-slate-400 uppercase tracking-tighter">No Badges Earned</h4>
        <p class="text-slate-400 mt-2 font-medium italic">Complete goals and maintain streaks to unlock rewards.</p>
      </div>

      <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
        <div v-for="badge in user.badges" :key="badge.id" class="group bg-white dark:bg-slate-800 p-8 rounded-[2.5rem] border border-slate-100 dark:border-slate-700 shadow-sm hover:shadow-2xl transition-all duration-500 text-center">
          <div class="w-20 h-20 bg-brand-calm/10 rounded-[2rem] flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-500 group-hover:rotate-6">
            <component :is="iconMap[badge.icon]" class="h-10 w-10 text-brand-calm" />
          </div>
          <h5 class="text-lg font-black text-slate-900 dark:text-white uppercase tracking-tight">{{ badge.name }}</h5>
          <p class="text-xs font-medium text-slate-400 mt-2 leading-relaxed">{{ badge.description }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { 
  ChartBarIcon, 
  ClipboardDocumentListIcon, 
  CheckCircleIcon, 
  ChartPieIcon, 
  FireIcon, 
  StarIcon, 
  TrophyIcon, 
  CheckBadgeIcon,
  RocketLaunchIcon,
  BoltIcon
} from '@heroicons/vue/24/outline'
import { user } from '../store'

const iconMap: Record<string, any> = {
  'StarIcon': StarIcon,
  'FireIcon': FireIcon,
  'TrophyIcon': TrophyIcon,
  'CheckBadgeIcon': CheckBadgeIcon
}

interface AnalyticsStats {
  total_goals: number
  completed_goals: number
  pending_goals: number
  completion_percentage: number
  streak: number
}

const stats = ref<AnalyticsStats | null>(null)
const loading = ref(true)
const error = ref('')

const statsCards = computed(() => [
  { label: 'Completed Goals', value: stats.value?.completed_goals || 0, icon: CheckCircleIcon, colorClass: 'text-green-500' },
  { label: 'Total Tracked', value: stats.value?.total_goals || 0, icon: ClipboardDocumentListIcon, colorClass: 'text-brand-calm' },
  { label: 'Completion Rate', value: stats.value?.completion_percentage || 0, icon: ChartPieIcon, colorClass: 'text-purple-500', suffix: '%' },
  { label: 'Daily Streak', value: stats.value?.streak || 0, icon: FireIcon, colorClass: 'text-orange-600', suffix: 'Days' }
])

onMounted(async () => {
  try {
    const res = await fetch('/api/analytics')
    if (res.ok) {
      stats.value = await res.json()
    } else {
      error.value = 'Failed to load analytics data.'
    }
  } catch (e) {
    error.value = 'An error occurred while fetching analytics.'
  } finally {
    loading.value = false
  }
})
</script>
