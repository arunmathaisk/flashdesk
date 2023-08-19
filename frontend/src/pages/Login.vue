<template>
  <LoginBox
    title="Log in to FlashDesk"
    :class="{ 'pointer-events-none': loading }"
  >
    <form class="flex flex-col" @submit.prevent="">
      <Input
        v-model="email"
        class="mb-4"
        label="Email"
        placeholder="johndoe@mail.com"
        name="email"
        autocomplete="email"
        :type="email !== 'Administrator' ? 'email' : 'text'"
        required
      />

      <Input
        v-model="password"
        label="Password"
        type="password"
        placeholder="••••••••"
        name="password"
        autocomplete="current-password"
        required
      />
      <ErrorMessage :message="errorMessage" class="mt-4" />
      <Button
        class="mt-4 focus:ring-0 focus:ring-offset-0"
        :loading="loading"
        appearance="primary"
        @click="login"
      >
        Submit
      </Button>
    </form>
  </LoginBox>
</template>

<script>
import { Input, ErrorMessage } from 'frappe-ui'
import LoginBox from '@/components/LoginBox.vue'
import { useAuthStore } from '@/stores/auth.js'
import { useUserStore } from '@/stores/user.js'

export default {
  name: 'Login',
  components: {
    LoginBox,
    Input,
    ErrorMessage,
  },
  data() {
    return {
      email: null,
      password: null,
      errorMessage: null,
    }
  },
  methods: {
    async login() {
      const data = {
        usr: this.email,
        pwd: this.password,
      }

      fetch('/api/method/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((responseData) => {
          if (responseData.message === 'Logged In') {
            const authStore = useAuthStore()
            const userStore = useUserStore()
            let getCookies = () => {
              return Object.fromEntries(
                document.cookie
                  .split('; ')
                  .map((cookie) => cookie.split('='))
                  .map((entry) => [entry[0], decodeURIComponent(entry[1])])
              )
            }
            userStore.$patch((state) => {
              ;(state.user.user_id = getCookies().user_id),
                (state.user.full_name = getCookies().full_name)
            })
            authStore.login()
            this.$router.push('/')
          } else {
            this.errorMessage = 'Invalid credentials'
          }
        })
    },
  },
}
</script>

<style></style>
