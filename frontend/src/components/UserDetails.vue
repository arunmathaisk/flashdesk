<template>
      <div class="flex flex-row">
    <div class="border-2 border-sky-400 bg-white max-w-md shadow-lg p-6 m-6 basis-1/2">
    <h1 class="text-2xl text-blue-600 font-semibold mb-4 text-center">
      Hi ! {{ userDetails.full_name }} 👋
    </h1>
    <hr class="border-t-2 border-sky-400 my-6" />
    <div v-if="loading" class="text-gray-600 mb-4 text-center">Loading...</div>
    <div v-else>
      <div class="mb-4">
          <p class="text-gray-600">
            <strong>Full Name:</strong> {{ userDetails.full_name }}
          </p>
          <p class="text-gray-600">
            <strong>Email:</strong> {{ userDetails.email }}
          </p>
          <p class="text-gray-600">
            <strong>Username:</strong> {{ userDetails.username }}
          </p>
    </div>
      <!-- <div class="mb-4">
          <p class="text-gray-600"><strong>Roles:</strong></p>
          <ul class="list-disc list-inside">
            <li v-for="role in userDetails.roles" :key="role">{{ role }}</li>
          </ul>
        </div> -->
    </div>
  </div>
  <div class="border-2 border-green-400 bg-white max-width-max shadow-lg p-6 m-6 basis-1/2">
    <div v-if="loading" class="text-gray-600 mb-4 text-center">Loading...</div>
    <div v-else>
      <h3 class="text-2xl text-green-600 font-semibold mb-4 text-center">
        Last Login 🗒️
        <hr class="border-t-2 border-green-400 my-6" />
        <span class="text-gray-600 text-xl">
          {{ new Date(last_login).toLocaleString() }}</span
        >
      </h3>
    </div>
  </div>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/user.js'
export default {
  name: 'UserDetails',
  computed: {
    currentUser() {
      const userStore = useUserStore()
      const user = userStore.getUser
      return user.full_name
    },
  },
  data() {
    return {
      userDetails: {},
      last_login: null,
    }
  },
  async created() {
    try {
      const response = await fetch(
        '/api/method/flashdesk.api.users.user.get_logged_in_user_details'
      )
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      this.userDetails = data.message
    } catch (error) {
      console.error('Error fetching user details:', error)
    }
    try {
      const response = await fetch(
        '/api/method/flashdesk.api.users.user.get_last_login'
      )
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      this.last_login = data.message
    } catch (error) {
      console.error('Error fetching user details:', error)
    }
  },
}
</script>
