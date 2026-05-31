import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

import { checkAuth, initTheme } from './store'

const initApp = async () => {
  initTheme()
  await checkAuth()

  const app = createApp(App)
  app.use(router)
  app.mount('#app')
}

initApp()
