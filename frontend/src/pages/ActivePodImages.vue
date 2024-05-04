<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <div id="test" class="flex-grow p-8 bg-white-200 overflow-auto">
      <h1 class="text-xl font-semibold mb-6 text-gray-800">
        Active Runnable Pod Images
      </h1>
      <hr class="border-t-2 border-black my-3" />
      <div class="grid grid-cols-1">
        <div
          v-for="(image, index) in activeImages"
          :key="index"
          class="border-2 border-black bg-white shadow-lg p-5 m-3 rounded"
        >
          <div class="flex items-center justify-between">
            <h4
              class="text-md font-medium text-gray-800"
              style="display: grid; grid-template-columns: 1fr auto auto"
            >
            <span class="font-bold">Image Tags : &nbsp; </span>{{ image.tags }}
            </h4>
            <div class="flex gap-4">
              <Button
                @click="savePod(image.image_id)"
                size="md"
                :variant="'solid'"
                theme="gray"
              >
                Save
              </Button>
              <Button
                @click="runPod(image.image_id)"
                size="md"
                :variant="'solid'"
                theme="gray"
              >
                Run
              </Button>
              <Button
                @click="deleteImage(image.image_id)"
                size="md"
                :variant="'solid'"
                theme="gray"
              >
                Remove
              </Button>
            </div>
          </div>
          <hr class="border-t-2 border-black my-3" />
          <div class="mt-4">
  <div class="pb-2 border-black">
    <p class="text-gray-700 text-sm">
      <span class="font-bold">ID:</span> {{ image.image_id }}
    </p>
  </div>
  <div class="pb-2 border-black">
    <p class="text-gray-700 text-sm">
      <span class="font-bold">Created On:</span> {{ new Date(image.created).toDateString() }}
    </p>
  </div>
  <div class="pb-2 border-black">
    <p class="text-gray-700 text-sm">
      <span class="font-bold">Short ID:</span> {{ image.short_id }}
    </p>
  </div>
  <div class="pb-2  border-black">
    <p class="text-gray-700 text-sm">
      <span class="font-bold">Architecture:</span> {{ image.architecture }}
    </p>
  </div>
  <div class="pb-2  border-black">
    <p class="text-gray-700 text-sm">
      <span class="font-bold">OS:</span> {{ image.os }}
    </p>
  </div>
  <div class="pb-2">
    <p class="text-gray-700 text-sm">
      <span class="font-bold">Size:</span> {{ image.size }}
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
import { Button} from 'frappe-ui'
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
          const currentOrigin = window.location.origin
          const currentProtocol = window.location.protocol
          const currentHostname = window.location.hostname
          const newTab = window.open(
            `${currentProtocol}//${currentHostname}:${data.message.vnc_port}/vnc.html`,
            '_blank'
          )
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
      } catch (error) {}
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
    async savePod(image_id) {
      try {
        const response = await fetch(
          '/api/method/flashdesk.api.pod_image.create_file_from_image',
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
          this.$toast(
            data.message.status,
            'Saving to tar file',
            data.message.message
          )
          this.fetchActiveImages()
        } else {
          this.$toast(
            data.message.status,
            'Saving to tar file',
            data.message.message
          )
          console.error('Error saving pod image:', response.statusText)
        }
      } catch (error) {
        console.error('Error saving pod image :', error)
      }
    },
  },
  components: { SideNavbar, Button },
}
</script>
