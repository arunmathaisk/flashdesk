<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-100">
    <div class="bg-white shadow-md p-6 rounded-lg w-full md:max-w-md">
      <h1 class="text-2xl font-semibold mb-4 text-center">
        Welcome, {{ currentUser }}
      </h1>
      <div v-if="loading" class="text-gray-600 mb-4 text-center">
        Loading...
      </div>
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
      console.log(this.userDetails)
    } catch (error) {
      console.error('Error fetching user details:', error)
    }
  },
}
</script>
