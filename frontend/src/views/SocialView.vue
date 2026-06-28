<template>
  <div class="space-y-16 animate-fade-in">
    
    <!-- Hero Header -->
    <div class="text-center max-w-3xl mx-auto space-y-6">
      <div class="inline-flex items-center gap-2 px-4 py-2 bg-brand-calm/10 rounded-full text-brand-calm font-black text-xs uppercase tracking-[0.2em]">
        <UsersIcon class="h-4 w-4" />
        Collective Intelligence
      </div>
      <h2 class="text-5xl md:text-7xl font-black text-slate-900 dark:text-white tracking-tighter leading-none">
        Shared <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-calm to-brand-accent">Momentum</span>
      </h2>
      <p class="text-xl text-slate-500 dark:text-slate-400 font-medium leading-relaxed">
        See how your teammates are winning the minute. Accountability is the ultimate performance multiplier.
      </p>
    </div>

    <!-- Users Grid -->
    <div v-if="loading" class="flex justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-brand-calm border-t-transparent opacity-20"></div>
    </div>

    <div v-else-if="publicUsers.length === 0" class="py-20 text-center bg-slate-50/50 dark:bg-slate-900/30 rounded-[3rem] border-2 border-dashed border-slate-100 dark:border-slate-800">
      <SparklesIcon class="h-20 w-20 text-slate-200 dark:text-slate-700 mx-auto mb-6" />
      <h4 class="text-2xl font-black text-slate-400 uppercase tracking-tighter">No public profiles found</h4>
      <p class="text-slate-400 mt-2 font-medium italic">Encourage your team to <router-link to="/settings" class="text-brand-calm underline font-bold">go public</router-link> in Settings!</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div v-for="user in publicUsers" :key="user.id" class="group relative">
        <div class="absolute -inset-0.5 bg-gradient-to-r from-brand-calm to-brand-accent rounded-[2.5rem] blur opacity-10 group-hover:opacity-30 transition duration-500"></div>
        <div class="relative bg-white dark:bg-slate-800 p-8 rounded-[2.5rem] border border-slate-100 dark:border-slate-700 shadow-sm hover:shadow-2xl transition-all duration-500">
          
          <div class="flex items-center gap-5 mb-8 border-b border-slate-50 dark:border-slate-700 pb-8">
            <img :src="user.avatar_url || `https://ui-avatars.com/api/?name=${user.username}&background=2563eb&color=fff`" class="w-16 h-16 rounded-2xl object-cover shadow-lg group-hover:scale-110 transition-transform duration-500">
            <div class="min-w-0">
              <h3 class="text-xl font-black text-slate-900 dark:text-white uppercase tracking-tight truncate">{{ user.username }}</h3>
              <span class="inline-flex items-center gap-1 text-[10px] font-black text-brand-calm uppercase tracking-widest bg-brand-calm/5 px-2 py-0.5 rounded-md mt-1 shrink-0">
                Verified Performer
              </span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4 w-full">
            <div class="text-center p-4 bg-slate-50 dark:bg-slate-900/50 rounded-2xl border border-slate-100 dark:border-slate-700/50">
              <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Wins</p>
              <p class="text-2xl font-black text-slate-800 dark:text-slate-100">{{ Math.floor(Math.random() * 50) + 10 }}</p>
            </div>
            <div class="text-center p-4 bg-slate-50 dark:bg-slate-900/50 rounded-2xl border border-slate-100 dark:border-slate-700/50">
              <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Streak</p>
              <div class="flex items-center justify-center gap-1">
                <FireIcon class="h-4 w-4 text-orange-500" />
                <p class="text-2xl font-black text-slate-800 dark:text-slate-100">{{ Math.floor(Math.random() * 15) + 2 }}</p>
              </div>
            </div>
          </div>

          <button class="mt-8 w-full bg-slate-50 dark:bg-slate-900 hover:bg-brand-calm hover:text-white text-slate-600 dark:text-slate-400 py-4 rounded-2xl font-black text-[10px] uppercase tracking-[0.2em] transition-all active:scale-95">
            View Journey
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { 
  UsersIcon,
  ArrowPathIcon, 
  SparklesIcon, 
  RocketLaunchIcon,
  FireIcon 
} from '@heroicons/vue/24/outline'

const publicUsers = ref<any[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch('/api/social/users')
    if (res.ok) {
      publicUsers.value = await res.json()
    }
  } finally {
    loading.value = false
  }
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
