<template>
  <div class="flex flex-col items-center min-h-screen bg-gray-100">
    <h2 class="text-2xl font-bold mb-4">{{ title }}</h2>
    <img src="../../public/logo.png" alt="App Logo" class="mx-auto mb-4 w-32 h-32" />
    <form class="w-80 flex flex-col bg-white p-6 rounded-lg shadow-md" @submit.prevent="login">
      <div class="mb-4">
        <label for="email" class="text-lg">Email</label>
        <input v-model="email" class="input input-bordered mt-1 p-2 rounded-md" type="text" placeholder="johndoe@mail.com" required />
      </div>
      <div class="mb-4">
        <label for="password" class="text-lg">Password</label>
        <input v-model="password" type="password" class="input input-bordered mt-1 p-2 rounded-md" placeholder="••••••••" required />
      </div>
      <p v-if="errorMessage" class="text-red-500 mb-4">{{ errorMessage }}</p>
      <button class="btn btn-primary mt-4" :class="{ 'opacity-50 cursor-not-allowed': loading }" type="submit">
        <span v-if="!loading">Login</span>
        <span v-else>Loading...</span>
      </button>
    </form>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth.js'
import { useUserStore } from '@/stores/user.js'

export default {
  name: 'Login',
  data() {
    return {
      email: null,
      password: null,
      errorMessage: null,
      title: 'Welcome to Our App'
    };
  },
  methods: {
    async login() {
      const data = {
        usr: this.email,
        pwd: this.password,
      };

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
            const authStore = useAuthStore();
            const userStore = useUserStore();
            let getCookies = () => {
              return Object.fromEntries(
                document.cookie
                  .split('; ')
                  .map((cookie) => cookie.split('='))
                  .map((entry) => [entry[0], decodeURIComponent(entry[1])])
              );
            };
            userStore.$patch((state) => {
              state.user.user_id = getCookies().user_id;
              state.user.full_name = getCookies().full_name;
            });
            authStore.login();
            this.$router.push('/');
          } else {
            this.errorMessage = 'Invalid credentials';
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    },
  },
};
</script>



<style>
/* Add any required styles here */
.input {
  border: 1px solid #d2d6dc;
}
.input-bordered {
  border: 1px solid #d2d6dc;
}
.btn {
  background-color: #4f46e5;
  color: #ffffff;
}
.btn:hover {
  background-color: #4338ca;
}
</style>