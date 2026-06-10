<template>
  <header class="bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-b border-slate-100 dark:border-slate-800 sticky top-0 z-[60] transition-all duration-300">
    <nav class="max-w-7xl mx-auto px-6 h-20 flex justify-between items-center">
      
      <router-link to="/" class="flex items-center gap-3 group">
        <div class="p-2.5 bg-brand-calm rounded-2xl group-hover:rotate-12 transition-transform duration-500 shadow-lg shadow-brand-calm/20">
          <RocketLaunchIcon class="w-6 h-6 text-white" />
        </div>
        <h1 class="text-2xl font-black text-slate-900 dark:text-white tracking-tighter uppercase transition-colors">
          Focus<span class="text-brand-calm">OS</span>
        </h1>
      </router-link>

      <div class="hidden md:flex items-center gap-8">
        <div v-if="user.authenticated" class="flex items-center gap-1 bg-slate-100/50 dark:bg-slate-800/50 p-1.5 rounded-2xl border border-slate-100 dark:border-slate-700">
          <router-link 
            v-for="link in navLinks" 
            :key="link.path"
            :to="link.path" 
            class="px-5 py-2.5 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all"
            active-class="bg-white dark:bg-slate-700 text-brand-calm dark:text-brand-accent shadow-sm"
            inactive-class="text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white"
          >
            {{ link.name }}
          </router-link>
        </div>

        <div class="flex items-center gap-4 pl-4 border-l border-slate-200 dark:border-slate-700">
          <button @click="toggleTheme" class="p-2.5 text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white transition-all rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 focus:outline-none" aria-label="Toggle Dark Mode">
            <SunIcon v-if="isDarkMode" class="w-5 h-5" />
            <MoonIcon v-else class="w-5 h-5" />
          </button>

          <template v-if="user.authenticated">
            <div class="relative group">
              <button @click="showAvatarModal = true" class="flex items-center gap-3 p-1 pr-4 bg-slate-50 dark:bg-slate-900 rounded-2xl border border-slate-100 dark:border-slate-800 hover:border-brand-calm transition-all group/user">
                <img :src="user.avatar_url || `https://ui-avatars.com/api/?name=${user.username}&background=2563eb&color=fff`" alt="Avatar" class="w-10 h-10 rounded-xl shadow-sm object-cover transition-transform group-hover/user:scale-105">
                <div class="text-left">
                  <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-none">High Performer</p>
                  <p class="text-sm font-bold text-slate-700 dark:text-slate-200 mt-0.5">{{ user.username }}</p>
                </div>
              </button>
            </div>
            
            <button @click="logout" class="p-2.5 text-red-500 hover:text-red-600 transition-all rounded-xl hover:bg-red-50 dark:hover:bg-red-900/20" title="Logout">
              <ArrowLeftOnRectangleIcon class="w-5 h-5" />
            </button>
          </template>

          <template v-else>
            <router-link to="/login" class="text-sm font-black text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white uppercase tracking-widest">Login</router-link>
            <router-link to="/register" class="px-6 py-3 bg-brand-calm text-white text-sm font-black uppercase tracking-widest rounded-2xl hover:bg-brand-calm/90 transition-all active:scale-95 shadow-lg shadow-brand-calm/20">Get Started</router-link>
          </template>
        </div>
      </div>
    </nav>
  </header>

  <!-- Avatar Modal via Headless UI -->
  <TransitionRoot appear :show="showAvatarModal" as="template">
    <Dialog as="div" @close="showAvatarModal = false" class="relative z-[100]">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-sm transform overflow-hidden rounded-[2.5rem] bg-white dark:bg-slate-800 p-10 text-left align-middle shadow-2xl transition-all border border-slate-100 dark:border-slate-700">
              <div class="flex flex-col items-center">
                <div class="p-4 bg-brand-calm/10 rounded-[2rem] mb-6">
                  <UserCircleIcon class="h-12 w-12 text-brand-calm" />
                </div>
                <DialogTitle as="h3" class="text-2xl font-black text-slate-900 dark:text-white tracking-tighter uppercase mb-2">
                  Update Identity
                </DialogTitle>
                <p class="text-sm font-medium text-slate-500 text-center mb-8">Choose an image URL to represent your focus OS profile.</p>

                <form @submit.prevent="updateAvatar" class="w-full space-y-6">
                  <div>
                    <label class="block text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-2 pl-1">Image URL</label>
                    <input 
                      v-model="newAvatarUrl" 
                      type="url" 
                      placeholder="https://images.unsplash.com/..." 
                      class="w-full px-5 py-4 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-700 rounded-2xl focus:ring-2 focus:ring-brand-calm outline-none transition-all dark:text-white text-sm"
                    >
                  </div>
                  <div class="flex gap-3">
                    <button type="button" @click="showAvatarModal = false" class="flex-1 px-6 py-4 text-slate-500 hover:text-slate-900 dark:hover:text-white font-black text-xs uppercase tracking-widest transition-all">Cancel</button>
                    <button type="submit" class="flex-1 bg-brand-calm text-white py-4 rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-brand-calm/90 transition-all active:scale-95 shadow-xl shadow-brand-calm/20">Save</button>
                  </div>
                </form>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { 
  TransitionRoot, 
  TransitionChild, 
  Dialog, 
  DialogPanel, 
  DialogTitle 
} from '@headlessui/vue'
import { 
  UserCircleIcon, 
  SunIcon, 
  MoonIcon, 
  RocketLaunchIcon, 
  ArrowLeftOnRectangleIcon 
} from '@heroicons/vue/24/outline'
import { user, logout as storeLogout, showToast, toggleTheme, isDarkMode } from '../store'

const router = useRouter()
const showAvatarModal = ref(false)
const newAvatarUrl = ref('')

const navLinks = [
  { name: 'Dashboard', path: '/' },
  { name: 'Analytics', path: '/analytics' },
  { name: 'Community', path: '/community' },
  { name: 'Settings', path: '/settings' }
]

const logout = async () => {
  await storeLogout()
  router.push({ name: 'login' })
}

const updateAvatar = async () => {
  if (!newAvatarUrl.value) return
  const res = await fetch('/api/me/avatar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ avatar_url: newAvatarUrl.value })
  })
  if (res.ok) {
    user.avatar_url = newAvatarUrl.value
    showAvatarModal.value = false
    showToast("Avatar updated successfully.")
  } else {
    showToast("Failed to update avatar.", true)
  }
}
</script>
