<template>
  <div class="flex flex-col items-center bg-gray-50">
    <!-- Flex container for alignment -->
    <Avatar
      :shape="'square'"
      image="../../public/logo.png"
      size="3xl"
      class="m-3 mt-5"
    />
    <span class="text-md font-medium">Flashdesk</span>
    <!-- Label next to the avatar -->

    <div class="flex flex-col items-center m-2">
      <ul>
        <li v-for="item in menuItems" :key="item.id">
          <div class="m-2">
            <!-- Using router-link as a wrapper for Button to navigate -->
            <router-link :to="item.path" tag="div" class="block">
              <Button
                class="sm:w-32 md:w-48"
                theme="white"
                :variant="'subtle'"
                size="md"
                :loading="false"
                :loadingText="null"
                :disabled="false"
                :link="null"
                style="text-align: left; justify-content: flex-start"
              >
                {{ item.title }}
              </Button>
            </router-link>
          </div>
        </li>
      </ul>
    </div>

    <div class="text-center mt-5 m-3">
      <p class="text-black-600 text-md whitespace-nowrap">
        Welcome <span class="font-semibold">{{ currentUser }} 😊</span>
      </p>

      <router-link to="/logout" class="block" tag="div">
        <Button
          class="sm:w-32 md:w-48 m-5"
          :variant="'solid'"
          theme="gray"
          size="md"
          :loading="false"
          :loadingText="null"
          :disabled="false"
          :link="null"
        >
          Logout
        </Button>
      </router-link>
    </div>
  </div>
</template>

<script>
import { TextInput, Avatar, Button } from 'frappe-ui'
import { useUserStore } from '@/stores/user.js'
import { FeatherIcon } from 'vue-feather-icons'

export default {
  name: 'SideNavbar',
  computed: {
    currentUser() {
      const userStore = useUserStore()
      const user = userStore.getUser
      return user.full_name
    },
  },
  components: {
    TextInput,
    Avatar,
    Button,
  },
  data() {
    return {
      menuItems: [
        { id: 1, title: 'Home', path: '/' },
        { id: 2, title: 'Create Pod Image', path: '/CreatePodImages' },
        { id: 3, title: 'Pod Images', path: '/PodImages' },
        { id: 4, title: 'Active Pod Images', path: '/ActivePodImages' },
        { id: 5, title: 'Running Pods ', path: '/RunningPods' },
        { id: 6, title: 'Docker Hub Search', path: '/DockerHubSearch' },
        { id: 7, title: 'Remote Queue Jobs', path: '/Events' },
        { id: 8, title: 'Event Logs', path: '/Logs' },
        { id: 9, title: 'PDFs', path: '/UploadPDFS' },
        { id: 10, title: 'Saved Images', path: '/SavedImages' },
      ],
    }
  },
}
</script>
