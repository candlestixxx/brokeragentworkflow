<template>
  <header class="bg-white dark:bg-slate-800 shadow-lg border-b border-brand-calm/10 sticky top-0 z-40 transition-colors duration-300">
    <nav class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 justify-between items-center">
        <div class="flex items-center gap-2">
          <div class="bg-brand-calm p-1.5 rounded-lg shadow-inner">
            <RocketLaunchIcon class="h-6 w-6 text-white" />
          </div>
          <h1 class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-brand-calm to-brand-accent tracking-tight transition-colors">
            One-Minute Manager
          </h1>
        </div>

        <div class="flex items-center gap-4">
          <!-- Desktop Nav -->
          <div v-if="user.authenticated" class="hidden md:flex items-center gap-1 bg-slate-100 dark:bg-slate-700 p-1 rounded-xl">
            <router-link to="/" class="px-4 py-1.5 rounded-lg transition-all duration-200 font-medium text-sm" active-class="bg-white dark:bg-slate-600 text-brand-calm dark:text-brand-accent shadow-sm">Dashboard</router-link>
            <router-link to="/community" class="px-4 py-1.5 rounded-lg transition-all duration-200 font-medium text-sm" active-class="bg-white dark:bg-slate-600 text-brand-calm dark:text-brand-accent shadow-sm">Community</router-link>
            <router-link to="/analytics" class="px-4 py-1.5 rounded-lg transition-all duration-200 font-medium text-sm" active-class="bg-white dark:bg-slate-600 text-brand-calm dark:text-brand-accent shadow-sm">Analytics</router-link>
            <router-link to="/settings" class="px-4 py-1.5 rounded-lg transition-all duration-200 font-medium text-sm" active-class="bg-white dark:bg-slate-600 text-brand-calm dark:text-brand-accent shadow-sm">Settings</router-link>
          </div>

          <div class="flex items-center gap-3 border-l border-slate-200 dark:border-slate-700 pl-4">
            <button @click="toggleTheme" class="p-2 text-slate-500 hover:text-brand-calm dark:text-slate-400 dark:hover:text-brand-accent transition-all rounded-full hover:bg-slate-100 dark:hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-brand-calm" :aria-label="isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
              <SunIcon v-if="isDarkMode" class="w-5 h-5" />
              <MoonIcon v-else class="w-5 h-5" />
            </button>

            <template v-if="user.authenticated">
              <Menu as="div" class="relative">
                <MenuButton class="flex items-center gap-2 group focus:outline-none">
                  <img :src="user.avatar_url || `https://ui-avatars.com/api/?name=${user.username}&background=0ea5e9&color=fff`" alt="Avatar" class="w-9 h-9 rounded-full shadow-sm object-cover border-2 border-transparent group-hover:border-brand-accent transition-all">
                  <span class="hidden sm:inline text-sm font-semibold text-slate-700 dark:text-slate-200 group-hover:text-brand-calm transition-colors">{{ user.username }}</span>
                  <ChevronDownIcon class="w-4 h-4 text-slate-400 group-hover:text-brand-calm" />
                </MenuButton>

                <transition enter-active-class="transition duration-100 ease-out" enter-from-class="transform scale-95 opacity-0" enter-to-class="transform scale-100 opacity-100" leave-active-class="transition duration-75 ease-in" leave-from-class="transform scale-100 opacity-100" leave-to-class="transform scale-95 opacity-0">
                  <MenuItems class="absolute right-0 mt-2 w-48 origin-top-right divide-y divide-slate-100 dark:divide-slate-700 rounded-lg bg-white dark:bg-slate-800 shadow-xl ring-1 ring-black ring-opacity-5 focus:outline-none">
                    <div class="px-1 py-1">
                      <MenuItem v-slot="{ active }">
                        <button @click="showAvatarModal = true" :class="[active ? 'bg-brand-calm text-white' : 'text-slate-700 dark:text-slate-200', 'group flex w-full items-center rounded-md px-2 py-2 text-sm font-medium transition-colors']">
                          <UserCircleIcon class="mr-2 h-5 w-5" aria-hidden="true" />
                          Update Avatar
                        </button>
                      </MenuItem>
                    </div>
                    <div class="px-1 py-1">
                      <MenuItem v-slot="{ active }">
                        <button @click="logout" :class="[active ? 'bg-red-500 text-white' : 'text-red-600 dark:text-red-400', 'group flex w-full items-center rounded-md px-2 py-2 text-sm font-bold transition-colors']">
                          <ArrowRightOnRectangleIcon class="mr-2 h-5 w-5" aria-hidden="true" />
                          Logout
                        </button>
                      </MenuItem>
                    </div>
                  </MenuItems>
                </transition>
              </Menu>
            </template>
            <template v-else>
              <router-link to="/login" class="text-sm font-bold text-slate-600 hover:text-brand-calm dark:text-slate-300 dark:hover:text-brand-accent transition-colors">Login</router-link>
              <router-link to="/register" class="bg-brand-calm hover:bg-brand-calm/90 text-white px-4 py-2 rounded-lg shadow-md text-sm font-bold transition-all transform hover:scale-105 active:scale-95">Sign Up</router-link>
            </template>
          </div>
        </div>
      </div>
    </nav>
  </header>

  <!-- Avatar Modal -->
  <Dialog :open="showAvatarModal" @close="showAvatarModal = false" class="relative z-50">
    <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm" aria-hidden="true" />

    <div class="fixed inset-0 flex items-center justify-center p-4">
      <DialogPanel class="w-full max-w-sm rounded-2xl bg-white dark:bg-slate-800 p-6 shadow-2xl border border-slate-100 dark:border-slate-700 transform transition-all">
        <div class="flex items-center gap-3 mb-6">
          <div class="bg-brand-calm/10 p-2 rounded-full">
            <PhotoIcon class="h-6 w-6 text-brand-calm" />
          </div>
          <DialogTitle class="text-xl font-bold text-slate-900 dark:text-white">Update Avatar</DialogTitle>
        </div>

        <form @submit.prevent="updateAvatar" class="space-y-4">
          <div>
            <label class="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-1">Image URL</label>
            <input v-model="newAvatarUrl" type="url" placeholder="https://example.com/photo.jpg" class="block w-full px-4 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-calm outline-none transition-all dark:text-white">
          </div>
          <div class="flex justify-end gap-3 mt-8">
            <button type="button" @click="showAvatarModal = false" class="px-4 py-2 text-sm font-bold text-slate-600 hover:text-slate-800 dark:text-slate-400 transition">Cancel</button>
            <button type="submit" class="bg-brand-calm text-white px-6 py-2 rounded-xl font-bold shadow-lg shadow-brand-calm/20 hover:bg-brand-calm/90 transition-all active:scale-95">Save Changes</button>
          </div>
        </form>
      </DialogPanel>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Dialog, DialogPanel, DialogTitle, Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import { 
  UserCircleIcon, 
  SunIcon, 
  MoonIcon, 
  RocketLaunchIcon, 
  ChevronDownIcon, 
  ArrowRightOnRectangleIcon,
  PhotoIcon
} from '@heroicons/vue/24/outline'
import { user, logout as storeLogout, showToast, toggleTheme, isDarkMode } from '../store'

const router = useRouter()
const showAvatarModal = ref(false)
const newAvatarUrl = ref('')

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
    newAvatarUrl.value = ''
  } else {
    showToast("Failed to update avatar.", true)
  }
}
</script>
