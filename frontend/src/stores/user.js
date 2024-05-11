import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: useStorage('user', {
      user_id: null,
      full_name: null,
    }),
  }),
  getters: {
    getUser: (state) => state.user,
  },
})
