<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <div class="flex-grow p-8 bg-white-200 overflow-auto">
      <h1 class="text-3xl font-semibold mb-6 text-gray-800">
        Search Docker Hub
      </h1>
      <hr class="border-t-2 border-violet-400 my-6" />
      <div class="p-4 flex items-center">
        <input
          type="text"
          placeholder="Search..."
          class="p-2 border border-violet-500 focus:ring-violet-300 flex-grow"
          v-model="searchInput"
          @input="fetchDockerHubImages"
        />
        <div class="pl-4">
          <button
            class="bg-violet-500 text-white p-2 hover:bg-violet-600 focus:outline focus:ring focus:border-violet-700"
          >
            Search
          </button>
        </div>
      </div>
      <div class="grid grid-cols-1">
        <div
          v-for="(image, index) in dockerImages"
          :key="index"
          class="border-2 border-violet-400 bg-white shadow-lg p-6 m-6"
        >
          <h3
            class="text-xl font-bold text-gray-800"
            style="display: grid; grid-template-columns: 1fr auto"
          >
            Image Name : {{ image.name }}
            <button
              class="bg-violet-500 text-white p-2 pl-4 pr-4 hover:bg-violet-600 focus:outline focus:ring focus:border-violet-700"
            >
              Pull
            </button>
          </h3>
          <hr class="border-t-2 border-violet-400 my-6" />
          <div class="mt-4">
            <div class="pb-2 mt-2">
              <p class="text-gray-700">
                <strong>Official :</strong> {{ image.is_official }}
              </p>
            </div>
            <div class="pb-2 mt-2">
              <p class="text-gray-700">
                <strong>Automated :</strong> {{ image.is_automated }}
              </p>
            </div>
            <div class="pb-2 mt-2">
              <p class="text-gray-700">
                <strong>Star Count:</strong> {{ image.star_count }}
              </p>
            </div>

            <div class="mt-2">
              <p class="text-gray-700">
                <strong>Description :</strong> {{ image.description }}
              </p>
            </div>
            <!-- Add more fields here if needed -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SideNavbar from '@/components/SideNavbar.vue'
import UserDetails from '@/components/UserDetails.vue'
import UserDisclaimer from '@/components/UserDisclaimer.vue'

export default {
  name: 'DockerHubSearch',
  data() {
    return {
      searchInput: '',
      dockerImages: [],
    }
  },
  methods: {
    async fetchDockerHubImages() {
      try {
        const response = await fetch(
          `/api/method/flashdesk.api.pod_image.docker_hub_search?search_query=${this.searchInput}`
        )
        const data = await response.json()
        this.dockerImages = data.message
      } catch (error) {
        console.error('Error fetching images:', error)
      }
    },
  },
  components: {
    SideNavbar,
    UserDetails,
    UserDisclaimer,
  },
}
</script>
