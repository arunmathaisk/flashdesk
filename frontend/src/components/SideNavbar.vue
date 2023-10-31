<template>
  <nav
    class="h-full w-1/5 bg-red flex-none shadow-lg rounded-r-lg overflow-y-auto"
  >
    <div class="p-6">
      <div class="flex">
        <img
          src="../../public/logo.png"
          alt="Logo"
          class="mb-4 max-w-[50px] max-h-[50px] w-auto h-auto"
        />
        <h1 class="text-4xl font-semibold text-blue-600 justify-center pl-2">FlashDesk</h1>
      </div>
      <div class="h-full border-l-2 border-blue-500"></div> <!-- Vertical line -->
      <ul class="space-y-4">
        <li v-for="item in menuItems" :key="item.id">
          <router-link
            :to="item.path"
            class="block py-3 px-4 text-gray-800 hover:text-blue-600 transition-colors border-l-4 border-transparent hover:border-blue-500 {{ activeMenuItem(item.path) }}"
          >
            {{ item.title }}
          </router-link>
          <div class="h-px bg-sky-500"></div> <!-- Horizontal line -->
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
        { id: 2, title: 'Create Pod Image', path: '/CreatePodImages' },
        { id: 3, title: 'Pod Images', path: '/PodImages' },
        { id: 4, title: 'Active Pod Images', path: '/ActivePodImages' },
        { id: 5, title: 'Running Pods ', path: '/RunningPods' },
        { id: 6, title: 'Docker Hub Search', path: '/DockerHubSearch' },
        { id: 7, title: 'Events', path: '/Events' }
      ],
    }
  },
}
</script>
