<template>
  <LoginBox
    title="Log in to FlashDesk"
    :class="{ 'pointer-events-none': loading }"
  >
    <img
      src="../../public/logo.png"
      alt="App Logo"
      class="mx-auto block mb-4 w-32 h-32"
    />
    <br />
    <hr class="border-t-2 border-black my-3" />
    <br />
    <form class="flex flex-col" @submit.prevent="">
      <TextInput
        v-model="email"
        class="border-2 border-black rounded-md"
        label="Email"
        placeholder="username"
        name="email"
        autocomplete="email"
        :type="email !== 'Administrator' ? 'email' : 'text'"
      />
      <br />
      <TextInput
        v-model="password"
        label="Password"
        type="password"
        placeholder="••••••••"
        name="password"
        autocomplete="current-password"
        class="border-2 border-black rounded-md"
      />
      <ErrorMessage :message="errorMessage" class="mt-4" />
      <br />
      <br />
      <Button
        :variant="'solid'"
        theme="gray"
        size="sm"
        label="Button"
        :loading="false"
        :loadingText="null"
        :disabled="false"
        :link="null"
        @click="login"
      >
        Login
      </Button>
    </form>
  </LoginBox>
</template>

<script>
import { TextInput, ErrorMessage, Button } from 'frappe-ui'
import LoginBox from '@/components/LoginBox.vue'
import { useAuthStore } from '@/stores/auth.js'
import { useUserStore } from '@/stores/user.js'

export default {
  name: 'Login',
  components: {
    LoginBox,
    TextInput,
    ErrorMessage,
    Button,
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

<style scoped>
.rainbow {
  background: linear-gradient(
    45deg,
    rgba(255, 0, 102, 0.8),
    rgba(68, 204, 0, 0.8),
    rgba(0, 51, 255, 0.8),
    rgba(255, 0, 68, 0.8),
    rgba(0, 204, 68, 0.8)
  );
  background-size: 300% 300%;
  animation: rainbow 5s linear infinite;
}

@keyframes rainbow {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 100% 50%;
  }
}
</style>
