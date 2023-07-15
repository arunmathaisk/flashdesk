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

export default {
  name: 'LoginPage',
  components: {
    LoginBox,
    Input,
    ErrorMessage,
  },
  data() {
    return {
      email: '',
      password: '',
    }
  },
  methods: {
    login() {
      
    },
  },
}
</script>

<style>
</style>
