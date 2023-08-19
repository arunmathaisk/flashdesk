<template>
  <div class="h-screen flex">
    <SideNavbar />
    <div id="test" class="flex-grow p-8 bg-green-200">
      <h1 class="text-3xl font-semibold mb-6 text-gray-800">Active Runnable Pod Images</h1>
      <hr class="border-t-2 border-green-400 my-6" />
      <div class="grid grid-cols-1">
        <div
          v-for="(image, index) in activeImages"
          :key="index"
          class="border-2 border-green-400 bg-white shadow-lg p-6 m-6"
        >
          <h3 class="text-xl font-bold text-gray-800">
          Image Tags : {{ image.tags }}
          </h3>
          <hr class="border-t-2 border-green-400 my-6" />
          <div class="mt-4">
            <div class="border-b pb-2 border-blue-400">
              <p class="text-gray-700">
                <strong>ID:</strong> {{ image.image_id }}
              </p>
            </div>
            <div class="border-b pb-2 mt-2 border-blue-400">
              <p class="text-gray-700">
                <strong>Created On:</strong>
                {{ new Date(image.created).toDateString() }}
              </p>
            </div>
            <div class="border-b pb-2 border-blue-400">
              <p class="text-gray-700">
                <strong>Short ID:</strong> {{ image.short_id }}
              </p>
            </div>
            <div class="border-b pb-2 mt-2 border-blue-400">
              <p class="text-gray-700">
                <strong>Architecture:</strong> {{ image.architecture }}
              </p>
            </div>
            <div class="mt-2">
              <p class="text-gray-700"><strong>OS:</strong> {{ image.os }}</p>
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
export default {
  name: 'ActivePodImages',
  data() {
    return {
      activeImages: [],
    }
  },
  mounted() {
    this.fetchActiveImages()
  },
  methods: {
    async fetchActiveImages() {
      try {
        const response = await fetch(
          '/api/method/flashdesk.api.pod_image.get_all_available_pod_images'
        )
        const data = await response.json()
        this.activeImages = data.message
      } catch (error) {
        console.error('Error fetching images:', error)
      }
    },
  },
  components: { SideNavbar },
}
</script>
