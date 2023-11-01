<template>
  <div class="flex flex-col">
    <div class="card" style="background-color: #ffffff; border: 2px solid #1E40AF; border-radius: 10px; box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1); padding: 20px; margin: 20px; flex-basis: 50%;">
      <h1 style="color: #1E40AF; font-size: 24px; font-weight: 600; text-align: center; margin-bottom: 20px;">
        Hi ! {{ userDetails.full_name }} 👋
      </h1>
      <div v-if="loading" style="color: #666666; margin-bottom: 20px; text-align: center;">Loading...</div>
      <div v-else>
        <div style="margin-bottom: 20px;">
          <p style="color: #333333;">
            <strong>Full Name:</strong> {{ userDetails.full_name }}
          </p>
          <p style="color: #333333;">
            <strong>Email:</strong> {{ userDetails.email }}
          </p>  
          <p style="color: #333333;">
            <strong>Username:</strong> {{ userDetails.username }}
          </p>
        </div>
      </div>
    </div>
    <div class="card" style="background-color: #ffffff; border: 2px solid #5cb85c; border-radius: 10px; box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1); padding: 20px; margin: 20px; flex-basis: 25%;">
      <div v-if="loading" style="color: #666666; margin-bottom: 20px; text-align: center;">Loading...</div>
      <div v-else>
        <h3 style="color: #28a745; font-size: 24px; font-weight: 600; text-align: center; margin-bottom: 20px;">
          Last Login 📗
        </h3>
        <span style="color: #666666; font-size: 18px; display: block; text-align: center;">
          {{ new Date(last_login).toLocaleString() }}
        </span>
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
