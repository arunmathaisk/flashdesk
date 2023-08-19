<template>
  <nav
    class="h-full w-1/5 bg-red flex-none shadow-lg rounded-r-lg overflow-y-auto"
  >
    <div class="p-6">
      <h1 class="text-4xl font-semibold text-blue-600 mb-8">FlashDesk</h1>
      <ul class="space-y-4">
        <li v-for="item in menuItems" :key="item.id">
          <router-link
            :to="item.path"
            class="block py-3 px-4 text-gray-800 hover:text-blue-600 transition-colors border-l-4 border-transparent hover:border-blue-500 {{ activeMenuItem(item.path) }}"
          >
            {{ item.title }}
          </router-link>
          <div class="h-px bg-sky-500"></div>
          <!-- Line of distinction -->
        </li>
      </ul>
    </div>
    <footer class="p-6 text-center">
      <p class="text-gray-600 text-lg">
        Welcome, <span class="font-semibold">{{ currentUser }} 😊</span>
      </p>
      <router-link
        to="/logout"
        class="block mt-6 px-6 py-3 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors"
      >
        Logout
      </router-link>
    </footer>
  </nav>
</template>

<script>
import { useUserStore } from '@/stores/user.js'
import { FeatherIcon } from 'vue-feather-icons'

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
        { id: 1, title: 'Home', path: '/' },
        { id: 2, title: 'Pod Images', path: '/PodImages' },
        { id: 1, title: 'Create Pod', path: '/about' },
        { id: 2, title: 'Running Pods ', path: '/contact' },
      ],
    }
  },
}
</script>
