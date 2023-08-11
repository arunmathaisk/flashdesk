import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue'),
  },
  {
    path: '/logout',
    name: 'Logout',
    beforeEnter: (to, from, next) => {
      const authStore = useAuthStore()
      authStore.logout()
      var Cookies = document.cookie.split(';')
      // set past expiry to all cookies
      for (var i = 0; i < Cookies.length; i++) {
        document.cookie = Cookies[i] + '=; expires=' + new Date(0).toUTCString()
      }
      localStorage.clear()
      next('/login')
    },
  },
  {
    path: '/PodImages',
    name: 'Pod Images',
    component: () => import('@/pages/PodImages.vue'),
    meta: { requiresAuth: true },
  },
]

let router = createRouter({
  history: createWebHistory('/frontend'),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
