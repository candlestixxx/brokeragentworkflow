<template>
  <div class="space-y-12 animate-fade-in">
    <div class="text-center max-w-2xl mx-auto space-y-4">
      <div class="inline-flex items-center gap-2 px-4 py-2 bg-brand-calm/10 rounded-full text-brand-calm font-black text-xs uppercase tracking-widest">
        <UsersIcon class="h-4 w-4" />
        Focus Community
      </div>
      <h2 class="text-4xl font-black text-slate-900 dark:text-white tracking-tighter uppercase">Shared Momentum</h2>
      <p class="text-slate-500 dark:text-slate-400 font-medium leading-relaxed">
        Connect with other high-performers. Accountability is the bridge between goals and accomplishment.
      </p>
    </div>

    <div v-if="loading" class="flex justify-center py-20">
      <ArrowPathIcon class="h-12 w-12 text-brand-calm animate-spin opacity-20" />
    </div>

    <div v-else-if="publicUsers.length === 0" class="py-20 text-center bg-white dark:bg-slate-800 rounded-[3rem] border border-slate-100 dark:border-slate-700 shadow-xl">
      <SparklesIcon class="h-16 w-12 text-slate-200 mx-auto mb-4" />
      <h3 class="text-xl font-bold text-slate-400">The community is just starting.</h3>
      <p class="text-slate-400 mt-2">Be the first to <router-link to="/settings" class="text-brand-calm underline font-bold">go public</router-link>.</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div v-for="user in publicUsers" :key="user.id" class="group bg-white dark:bg-slate-800 p-8 rounded-[2.5rem] shadow-xl shadow-slate-200/50 dark:shadow-none border border-slate-100 dark:border-slate-700 hover:border-brand-calm transition-all duration-300 relative overflow-hidden">
        <div class="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
          <RocketLaunchIcon class="h-24 w-24 text-brand-calm -rotate-12" />
        </div>
        
        <div class="flex flex-col items-center text-center relative z-10">
          <div class="relative">
            <img :src="user.avatar_url || `https://ui-avatars.com/api/?name=${user.username}&background=2563eb&color=fff`" alt="Avatar" class="w-24 h-24 rounded-full shadow-2xl border-4 border-white dark:border-slate-700 object-cover group-hover:scale-105 transition-transform duration-500">
            <div class="absolute -bottom-1 -right-1 bg-green-500 w-6 h-6 rounded-full border-4 border-white dark:border-slate-800 shadow-sm"></div>
          </div>
          
          <h3 class="mt-6 text-2xl font-black text-slate-900 dark:text-white tracking-tight">{{ user.username }}</h3>
          <div class="mt-2 flex items-center gap-1.5 text-[10px] font-black text-brand-calm bg-brand-calm/10 px-3 py-1 rounded-full uppercase tracking-widest">
            Elite Performer
          </div>

          <div class="grid grid-cols-2 gap-4 w-full mt-8 pt-8 border-t border-slate-50 dark:border-slate-700/50">
            <div class="text-center">
              <p class="text-xs font-black text-slate-400 uppercase tracking-widest">Wins</p>
              <p class="text-xl font-black text-slate-800 dark:text-slate-100">{{ Math.floor(Math.random() * 50) + 10 }}</p>
            </div>
            <div class="text-center">
              <p class="text-xs font-black text-slate-400 uppercase tracking-widest">Streak</p>
              <div class="flex items-center justify-center gap-1">
                <FireIcon class="h-4 w-4 text-orange-500" />
                <p class="text-xl font-black text-slate-800 dark:text-slate-100">{{ Math.floor(Math.random() * 15) + 2 }}</p>
              </div>
            </div>
          </div>

          <button class="mt-8 w-full bg-slate-50 dark:bg-slate-900 hover:bg-brand-calm hover:text-white text-slate-600 dark:text-slate-400 py-3 rounded-2xl font-black text-xs uppercase tracking-widest transition-all">
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
