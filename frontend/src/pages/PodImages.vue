<template>
  <div class="bg-gray-100 min-h-screen flex">
    <SideNavbar />
    <div class="flex-grow p-8">
      <h1 class="text-3xl font-semibold mb-6 text-gray-800">Pod Images</h1>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="(image, index) in podImages"
          :key="index"
          class="bg-white rounded-lg shadow-md p-6 border border-gray-300"
        >
          <h3 class="text-xl text-gray-800">{{ image.image_name }}</h3>
          <div class="mt-4">
            <div class="border-b pb-2">
              <p class="text-gray-700">
                <strong>Image ID:</strong> {{ image.image_id }}
              </p>
            </div>
            <div class="border-b pb-2 mt-2">
              <p class="text-gray-700">
                <strong>Created On:</strong> {{ image.created_on }}
              </p>
            </div>
            <div class="mt-2">
              <p class="text-gray-700">
                <strong>Description:</strong> {{ image.image_description }}
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
import SideNavbar from '../components/SideNavbar.vue'
export default {
  data() {
    return {
      podImages: [],
    }
  },
  mounted() {
    this.fetchPodImages()
  },
  methods: {
    async fetchPodImages() {
      try {
        const response = await fetch(
          '/api/method/flashdesk.api.pod_image.get_all_published_pod_images'
        )
        const data = await response.json()
        this.podImages = data.message
      } catch (error) {
        console.error('Error fetching images:', error)
      }
    },
  },
  components: { SideNavbar },
}
</script>
