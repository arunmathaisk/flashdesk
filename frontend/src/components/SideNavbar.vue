<template>
  <div
    class="flex flex-col justify-between bg-white h-screen md:w-1/6 shadow-lg rounded-lg overflow-y-auto"
  >
    <div class="p-6 w-full bg-gray-100">
      <h1 class="text-blue-500 text-4xl md:text-5xl font-semibold mb-6">
        FlashDesk
      </h1>
      <ul class="space-y-3">
        <li v-for="item in menuItems" :key="item.id">
          <router-link
            :to="item.path"
            class="text-gray-800 text-xl md:text-2xl hover:text-blue-500"
            >{{ item.title }}</router-link
          >
        </li>
      </ul>
    </div>
    <footer class="p-6 w-full bg-gray-100 text-center">
      <p class="text-gray-600 text-lg">
        Welcome, <span class="font-semibold">{{ currentUser }}</span
        > 😊
      </p>
      <router-link
        to="/logout"
        class="text-blue-500 mt-4 inline-block px-4 py-2 bg-blue-100 rounded-full hover:bg-blue-200 transition-colors"
      >
        Logout
      </router-link>
    </footer>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/user.js'

export default {
  name: 'SideNavbar',
  computed: {
    currentUser() {
      const userStore = useUserStore()
      const user = userStore.getUser // Assuming getUser is a getter in your store module
      return user.full_name // Update the property as per your store structure
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
