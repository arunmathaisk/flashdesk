<template>
  <div
    v-if="modal_close"
    class="flex items-center justify-center fixed inset-0 bg-gray-900 bg-opacity-50 z-50"
  >
    <div
      class="bg-white shadow-lg rounded-lg overflow-hidden w-auto max-w-md mx-auto my-8"
    >
      <div class="p-6">
        <h1 class="text-xl font-semibold text-gray-900 mb-4">
          Save Running Pod As Image
        </h1>
        <div class="space-y-4">
          <div class="flex flex-col">
            <label for="image_name" class="text-gray-700 font-medium"
              >Image Name</label
            >
            <input
              type="text"
              v-model="container_params.image_name"
              @input="
                container_params.image_name = $event.target.value.toLowerCase()
              "
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-500 focus:ring-opacity-50"
              placeholder="Enter image name"
            />
          </div>
          <div class="flex flex-col">
            <label for="tag" class="text-gray-700 font-medium">Tag</label>
            <input
              type="text"
              v-model="container_params.tag"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-500 focus:ring-opacity-50"
              placeholder="Enter tag"
            />
          </div>
          <div class="flex flex-col">
            <label for="message" class="text-gray-700 font-medium"
              >Message</label
            >
            <input
              type="text"
              v-model="container_params.message"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-500 focus:ring-opacity-50"
              placeholder="Enter message"
            />
          </div>
          <div class="flex items-center mt-4">
            <input
              id="checked-checkbox"
              type="checkbox"
              v-model="container_params.pause"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
            />
            <label for="checked-checkbox" class="ml-2 text-gray-900"
              >Pause Container</label
            >
          </div>
          <button
            @click="commit_pod()"
            class="w-full bg-blue-500 text-white font-medium rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-700 py-2 mt-4"
          >
            Commit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Modal',
  props: ['modal_close', 'selected_pod'],
  data() {
    return {
      container_params: {
        image_name: '',
        tag: '',
        message: '',
        pause: true,
      },
    }
  },
  methods: {
    async commit_pod() {
      try {
        const response = await fetch(
          '/api/method/flashdesk.api.pods.running_pods.commit_pod',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              container_id: this.selected_pod.container_id,
              container_params: this.container_params,
            }),
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
            text: 'Pod  Commited Sucessfully',
            showCancelButton: 'true',
          })
          this.$emit('close_modal', false)
          this.fetchRunningPods()
        } else {
          this.$swal({
            toast: true,
            position: 'bottom-right',
            showConfirmButton: false,
            timer: 3000,
            icon: 'error',
            title: 'Error',
            text: 'Something Went Wrong with POD COMMITING :(',
            showCancelButton: 'true',
          })
          console.error('Error terminating pod:', response.statusText)
        }
      } catch (error) {
        console.error('Error fetching images:', error)
      }
    },
  },
  emits: ['close_modal'],
}
</script>
