<template>
  <div class="bg-white dark:bg-slate-800 rounded-[2.5rem] p-8 shadow-sm border border-slate-100 dark:border-slate-700/50 overflow-hidden relative group">
    <div class="flex items-center gap-3 mb-6">
      <div class="p-3 bg-brand-calm/10 rounded-2xl">
        <ChartBarIcon class="h-6 w-6 text-brand-calm" />
      </div>
      <div>
        <h3 class="text-xl font-black text-slate-900 dark:text-white uppercase tracking-tight leading-none">Activity Heatmap</h3>
        <p class="text-xs text-slate-400 font-medium mt-1">Last 365 Days</p>
      </div>
    </div>

    <!-- Scrollable container for mobile -->
    <div class="w-full overflow-x-auto pb-4 custom-scrollbar">
      <!-- 53 weeks (columns) x 7 days (rows) -->
      <div class="flex gap-1.5 min-w-max">
        <div v-for="(week, wIdx) in grid" :key="wIdx" class="flex flex-col gap-1.5">
          <div v-for="(day, dIdx) in week" :key="dIdx"
               :title="day.date ? `${day.date}: ${day.count} goals` : ''"
               :class="[
                 'w-3.5 h-3.5 rounded-sm transition-all duration-300',
                 !day.date ? 'bg-transparent' :
                 day.count === 0 ? 'bg-slate-100 dark:bg-slate-700/50' :
                 day.count < 3 ? 'bg-indigo-300 dark:bg-indigo-900/60' :
                 day.count < 6 ? 'bg-indigo-400 dark:bg-indigo-700' :
                 'bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.5)]'
               ]">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ChartBarIcon } from '@heroicons/vue/24/outline'

const heatmapData = ref<{date: string, count: number}[]>([])
const grid = ref<any[][]>([])

onMounted(async () => {
  try {
    const res = await fetch('/api/me/heatmap')
    if (res.ok) {
      heatmapData.value = await res.json()
      buildGrid()
    }
  } catch(e) {
    console.error(e)
  }
})

function buildGrid() {
  // Map data by date for O(1) lookup
  const dataMap: Record<string, number> = {}
  heatmapData.value.forEach(d => dataMap[d.date] = d.count)

  const endDate = new Date()
  const startDate = new Date()
  startDate.setDate(endDate.getDate() - 364) // exactly 52 weeks

  const weeks: any[][] = []
  let currentWeek: any[] = []

  // Pad the first week if startDate isn't Sunday (0)
  const startDay = startDate.getDay()
  for(let i=0; i<startDay; i++) {
    currentWeek.push({ date: null, count: 0 })
  }

  let curr = new Date(startDate)
  while(curr <= endDate) {
    const dStr = curr.toISOString().split('T')[0]
    currentWeek.push({
      date: dStr,
      count: dataMap[dStr] || 0
    })

    if(currentWeek.length === 7) {
      weeks.push(currentWeek)
      currentWeek = []
    }
    curr.setDate(curr.getDate() + 1)
  }

  // Push the final incomplete week
  if(currentWeek.length > 0) {
    while(currentWeek.length < 7) {
      currentWeek.push({ date: null, count: 0 })
    }
    weeks.push(currentWeek)
  }

  grid.value = weeks
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 10px;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #334155;
}
</style>
