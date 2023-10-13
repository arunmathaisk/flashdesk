  <template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <div id="test" class="flex-grow p-8 bg-white-200 overflow-auto">
      <h1 class="text-3xl font-semibold mb-6 text-gray-800">
        Active Runnable Pod Images
      </h1>
      <hr class="border-t-2 border-green-400 my-6" />
      <div class="grid grid-cols-1">
        <div
          v-for="(image, index) in activeImages"
          :key="index"
          class="border-2 border-green-400 bg-white shadow-lg p-6 m-6"
        >
          <h3
            class="text-xl font-bold text-gray-800"
            style="display: grid; grid-template-columns: 1fr auto auto"
          >
            Image Tags : {{ image.tags }}
            <button
              @click="runPod(image.image_id)"
              class="bg-green-400 text-white p-2 pl-4 pr-4 hover:bg-green-600 focus:outline focus:ring focus:border-green-400"
            >
              Run
            </button>
            <button
              @click="deleteImage(image.image_id)"
              class="bg-red-400 text-white p-2 pl-4 pr-4 ml-4 hover:bg-red-600 focus:outline focus:ring focus:border-red-400"
            >
              Remove
            </button>
          </h3>
          <hr class="border-t-2 border-green-400 my-6" />
          <div class="mt-4">
            <div class="pb-2 border-green-400">
              <p class="text-gray-700">
                <strong>ID:</strong> {{ image.image_id }}
              </p>
            </div>
            <div class="pb-2 mt-2 border-green-400">
              <p class="text-gray-700">
                <strong>Created On:</strong>
                {{ new Date(image.created).toDateString() }}
              </p>
            </div>
            <div class="pb-2 border-green-400">
              <p class="text-gray-700">
                <strong>Short ID:</strong> {{ image.short_id }}
              </p>
            </div>
            <div class="pb-2 mt-2 border-green-400">
              <p class="text-gray-700">
                <strong>Architecture:</strong> {{ image.architecture }}
              </p>
            </div>
            <div class="pb-2 mt-2 border-green-400">
              <p class="text-gray-700"><strong>OS:</strong> {{ image.os }}</p>
            </div>
            <div class="mt-2">
              <p class="text-gray-700">
                <strong>Size</strong> {{ image.size }}
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
    async runPod(image_id) {
      try {
        const response = await fetch(
          '/api/method/flashdesk.api.pods.running_pods.run_pod',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image_id: image_id }),
          }
        )
        if (response.ok) {
          const data = await response.json()
          this.$swal({
            toast: true,
            position: 'bottom-right',
            showConfirmButton: false,
            timer: 3000,
            icon: 'success',
            title: 'Sucess',
            text: 'Pod Run Sucessfully',
            showCancelButton: 'true',
          })
          const currentOrigin = window.location.origin;
          const currentProtocol = window.location.protocol;
          const currentHostname = window.location.hostname;
          const newTab = window.open(`${currentProtocol}//${currentHostname}:${data.message.vnc_port}`,'_blank');
          this.fetchActiveImages()
        } else {
          this.$swal({
            toast: true,
            position: 'bottom-right',
            showConfirmButton: false,
            timer: 3000,
            icon: 'error',
            title: 'Error',
            text: 'Something Went Wrong :(',
            showCancelButton: 'true',
          })
        }
      } catch (error) {
      }
    },
    async deleteImage(image_id) {
      try {
        const response = await fetch(
          '/api/method/flashdesk.api.pod_image.delete_image_using_id',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image_id: image_id }),
          }
        )
        if (response.ok) {
          const data = await response.json()
          this.$swal({
            toast: true,
            position: 'bottom-right',
            showConfirmButton: false,
            timer: 3000,
            icon: 'success',
            title: 'Sucess',
            text: 'Pod Image Sucessfully Deleted',
            showCancelButton: 'true',
          })
          this.fetchActiveImages()
        } else {
          this.$swal({
            toast: true,
            position: 'bottom-right',
            showConfirmButton: false,
            timer: 3000,
            icon: 'error',
            title: 'Error',
            text: 'Something Went Wrong While Deleting Pod Image :(',
            showCancelButton: 'true',
          })
          console.error('Error terminating pod image:', response.statusText)
        }
      } catch (error) {
        console.error('Error terminating pod image :', error)
      }
    },
  },
  components: { SideNavbar },
}
</script>
