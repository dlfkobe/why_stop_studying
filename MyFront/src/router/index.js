import { createRouter, createWebHistory } from 'vue-router'
// import Layout from '../views/Layout/index.vue'
import Chat from '../views/chat.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Chat,
    },
  ]
})

export default router
