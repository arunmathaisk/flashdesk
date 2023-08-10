import { defineStore } from 'pinia';
import { useStorage } from '@vueuse/core';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: useStorage('isAuthenticated',false)
  }),
  getters: {
    isUserAuthenticated: (state) => state.isAuthenticated,
  },
  actions: {
    login() {
      this.isAuthenticated = true;
    },
    logout() {
      this.isAuthenticated = false;
    },
  },
});
