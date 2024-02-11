<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <div id="test" class="flex-grow p-8 bg-white-200 overflow-auto">
      <h1 class="text-3xl font-semibold mb-6 text-gray-800">
        Currently Running Pods
      </h1>
      <hr class="border-t-2 border-teal-400 my-6" />
      <Modal :modal_close="modal_visible" :selected_pod="selected_pod" @close_modal="close_modal"/>
      <div class="grid grid-cols-1">
        <div
          v-for="(pod, index) in runningPods"
          :key="index"
          class="border-2 border-teal-500 bg-white shadow-lg p-6 m-6 rounded"
        >
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-bold text-gray-800">
              Container Name: {{ pod.container_name }}
            </h3>
            <div class="flex gap-4">
              <button
                @click="open_modal(pod)"
                class="bg-blue-500 text-white ml-2 mr-2 p-2 pl-4 pr-4 rounded-md hover:bg-blue-600 focus:outline focus:ring focus:border-blue-700"
              >
                Commit
              </button>
              <button
                @click="openNewTab(pod)"
                class="bg-teal-500 text-white ml-2 mr-2 p-2 pl-4 pr-4 rounded-md hover:bg-teal-600 focus:outline focus:ring focus:border-teal-700"
              >
                View
              </button>
              <button
                @click="terminatePod(pod.container_id)"
                class="bg-red-500 text-white ml-2 mr-2 p-2 pl-4 pr-4 rounded-md hover:bg-red-600 focus:outline focus:ring focus:border-red-700 ml-4"
              >
                Terminate
              </button>
            </div>
          </div>
          <hr class="border-t-2 border-teal-400 my-6 rounded" />
          <div class="mt-4 grid grid-cols-2 gap-4">
            <div class="pb-2 rounded">
              <p class="text-gray-700">
                <strong>Short ID: </strong> {{ pod.container_shortid }}
              </p>
            </div>
            <div class="rounded">
              <p class="text-gray-700">
                <strong>Status: &nbsp</strong>
                <span
                  class="h-3 w-3 rounded-full inline-block mr-2"
                  :class="{
                    'bg-green-500': pod.container_status === 'running',
                    'bg-red-500': pod.container_status !== 'running',
                  }"
                ></span>
                {{ pod.container_status }}
              </p>
            </div>
            <div class="pb-2 rounded">
              <p class="text-gray-700">
                <strong>Tags: </strong> {{ pod.container_image_tags }}
              </p>
            </div>
            <div class="rounded">
              <p class="text-gray-700">
                <strong>VNC Port: </strong> {{ pod.container_vnc_port }}
              </p>
            </div>
            <div class="pb-2 rounded">
              <p class="text-gray-700">
                <strong>Available Ports: </strong>
                {{ pod.container_available_ports }}
              </p>
            </div>
            <div class="rounded">
              <p class="text-gray-700">
                <strong>Port Bindings: </strong>
                {{ pod.container_port_bindings }}
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
import Modal from '../components/Modal.vue'

export default {
  name: 'RunningPods',
  data() {
    return {
      runningPods: [],
      modal_visible:false,
      selected_pod:""
    }
  },
  mounted() {
    this.fetchRunningPods()
  },
  methods: {
    openNewTab(pod) {
      const currentProtocol = window.location.protocol
      const currentHostname = window.location.hostname
      window.open(
        `${currentProtocol}//${currentHostname}:${pod.container_vnc_port}/vnc.html`,
        '_blank'
      )
    },
    async fetchRunningPods() {
      try {
        const response = await fetch(
          '/api/method/flashdesk.api.pods.running_pods.get_all_actively_running_pod_images'
        )
        const data = await response.json()
        this.runningPods = data.message
      } catch (error) {
        console.error('Error fetching images:', error)
      }
    },
    async terminatePod(containerId) {
      try {
        const response = await fetch(
          '/api/method/flashdesk.api.pods.running_pods.terminate_pod',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ container_id: containerId }),
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
            text: 'Pod Terminated Sucessfully',
            showCancelButton: 'true',
          })
          this.fetchRunningPods()
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
          console.error('Error terminating pod:', response.statusText)
        }
      } catch (error) {
        console.error('Error terminating pod:', error)
      }
    },
    open_modal(pod) {
      this.selected_pod = pod
      this.modal_visible = true
    },close_modal() {
      this.modal_visible= false
    }
  },
  components: { SideNavbar, Modal },
}
</script>
