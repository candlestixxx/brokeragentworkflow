import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

import { checkAuth } from './store'

const initApp = async () => {
  await checkAuth()

  const app = createApp(App)
  app.use(router)
  app.mount('#app')
}

initApp()
