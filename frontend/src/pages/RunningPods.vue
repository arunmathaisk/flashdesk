<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <div id="test" class="flex-grow p-8 bg-white-200 overflow-auto">
      <h1 class="text-xl font-semibold mb-6 text-gray-800">
        Currently Running Pods
      </h1>
      <hr class="border-t-2 border-black my-6" />
      <Modal
        :modal_close="modal_visible"
        :selected_pod="selected_pod"
        @close_modal="close_modal"
      />
      <div class="grid grid-cols-2">
        <div
          v-for="(pod, index) in runningPods"
          :key="index"
          class="border-2 border-black bg-white shadow-lg p-3 m-3 rounded"
        >
          <div class="flex items-center justify-between">
            <h4 class="text-md text-gray-800">
              <span class="font-bold"> Container Name: </span>
              {{ pod.container_name }}
            </h4>
            <div class="flex gap-4">
              <Button
                @click="open_modal(pod)"
                size="md"
                variant="solid"
                theme="gray"
              >
                Commit
              </Button>
              <Button
                @click="openNewTab(pod)"
                size="md"
                variant="solid"
                theme="gray"
              >
                View
              </Button>
              <Button
                @click="terminatePod(pod.container_id)"
                size="md"
                variant="solid"
                theme="gray"
              >
                Terminate
              </Button>
            </div>
          </div>
          <hr class="border-t-2 border-black my-3 rounded" />
          <div class="mt-4 grid grid-cols-2 gap-4 text-sm">
            <div class="pb-2 rounded">
              <p class="text-gray-700">
                <span class="font-bold">Short ID:</span>
                {{ pod.container_shortid }}
              </p>
            </div>
            <div class="rounded">
              <p class="text-gray-700">
                <span class="font-bold">Status:</span> &nbsp
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
                <span class="font-bold">Tags:</span>
                {{ pod.container_image_tags }}
              </p>
            </div>
            <div class="rounded">
              <p class="text-gray-700">
                <span class="font-bold">VNC Port:</span>
                {{ pod.container_vnc_port }}
              </p>
            </div>
            <div class="pb-2 rounded">
              <p class="text-gray-700">
                <span class="font-bold">Available Ports:</span>
                {{ pod.container_available_ports }}
              </p>
            </div>
            <div class="pb-2 rounded">
              <p class="text-gray-700">
                <span class="font-bold">Port Bindings:</span>
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
import { Button } from 'frappe-ui'

export default {
  name: 'RunningPods',
  data() {
    return {
      runningPods: [],
      modal_visible: false,
      selected_pod: '',
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
    },
    close_modal() {
      this.modal_visible = false
    },
  },
  components: { SideNavbar, Modal },
}
</script>
