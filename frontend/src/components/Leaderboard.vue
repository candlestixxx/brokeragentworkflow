<template>
  <div class="relative bg-white dark:bg-slate-800 p-8 rounded-[2.5rem] border border-slate-100 dark:border-slate-700 shadow-sm overflow-hidden">
    <!-- Header -->
    <div class="flex items-center gap-3 mb-8">
      <div class="p-3 bg-brand-calm/10 rounded-2xl">
        <TrophyIcon class="h-6 w-6 text-brand-calm" />
      </div>
      <div>
        <h3 class="text-xl font-black text-slate-900 dark:text-white uppercase tracking-tight leading-none">Global Leaderboard</h3>
        <p class="text-xs text-slate-400 font-medium mt-1">Top performers across the network</p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-2 border-brand-calm border-t-transparent opacity-20"></div>
    </div>

    <!-- Empty State -->
    <div v-else-if="leaders.length === 0" class="py-12 text-center text-slate-400 font-medium italic">
      No data available yet.
    </div>

    <!-- Leader List -->
    <div v-else class="space-y-4">
      <div v-for="(leader, index) in leaders" :key="leader.id"
           class="flex items-center justify-between p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-700/50 hover:border-brand-calm/30 transition-colors">

        <div class="flex items-center gap-4">
          <!-- Rank Badge -->
          <div :class="[
            'flex items-center justify-center w-8 h-8 rounded-xl font-black text-sm',
            index === 0 ? 'bg-yellow-400/20 text-yellow-600 dark:text-yellow-400' :
            index === 1 ? 'bg-slate-300/20 text-slate-600 dark:text-slate-300' :
            index === 2 ? 'bg-orange-400/20 text-orange-600 dark:text-orange-400' :
            'bg-transparent text-slate-400'
          ]">
            #{{ index + 1 }}
          </div>

          <!-- Avatar & Name -->
          <img :src="leader.avatar_url || `https://ui-avatars.com/api/?name=${leader.username}&background=2563eb&color=fff`"
               class="w-10 h-10 rounded-xl object-cover">
          <div class="font-bold text-slate-700 dark:text-slate-200">
            {{ leader.username }}
          </div>
        </div>

        <!-- Score -->
        <div class="text-right">
          <div class="text-lg font-black text-slate-900 dark:text-white leading-none">{{ leader.completed_count }}</div>
          <div class="text-[9px] font-black text-slate-400 uppercase tracking-widest mt-1">Wins</div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { TrophyIcon } from '@heroicons/vue/24/outline'

const leaders = ref<any[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch('/api/social/leaderboard')
    if (res.ok) {
      leaders.value = await res.json()
    }
  } finally {
    loading.value = false
  }
})
</script>
