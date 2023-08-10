<template>
  <div class="flex h-screen bg-gray-100">
    <nav class="w-1/6 bg-white shadow-lg rounded-r-lg overflow-y-auto">
      <div class="p-6">
        <h1 class="text-3xl font-semibold text-blue-500 mb-6">FlashDesk</h1>
        <ul class="space-y-3">
          <li v-for="item in menuItems" :key="item.id">
            <router-link
              :to="item.path"
              class="block text-gray-800 hover:text-blue-500"
            >
              {{ item.title }}
            </router-link>
          </li>
        </ul>
      </div>
      <footer class="p-6 text-center">
        <p class="text-gray-600 text-lg">
          Welcome, <span class="font-semibold">{{ currentUser }}</span> 😊
        </p>
        <router-link
          to="/logout"
          class="block mt-4 px-4 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors"
        >
          Logout
        </router-link>
      </footer>
    </nav>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/user.js'

export default {
  name: 'SideNavbar',
  computed: {
    currentUser() {
      const userStore = useUserStore()
      const user = userStore.getUser
      return user.full_name 
    },
  },
  data() {
    return {
      menuItems: [
        { id: 1, title: '', path: '/' },
        { id: 2, title: 'About', path: '/about' },
        { id: 3, title: 'Contact', path: '/contact' },
        { id: 3, title: 'Say hello', path: '/hello' },
      ],
    }
  },
}
</script>
