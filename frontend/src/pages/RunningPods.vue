<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <div id="test" class="flex-grow p-8 bg-white-200 overflow-auto">
      <h1 class="text-3xl font-semibold mb-6 text-gray-800">
        Currently Running Pods
      </h1>
      <hr class="border-t-2 border-teal-400 my-6" />
      <div v-if="modal_close" class="flex flex-col items-center p-2 border-2 border-teal-500 bg-white shadow-lg p-6 m-6 rounded w-fit absolute top-4 left-3">
        <h1>New Image Details</h1>
        <div class="flex flex-col">
          <div class="flex items-center">
            <label for="text-gray-900">Name/Tag</label>
            <input type="text" v-model="container_params.tag" class="block w-full font-medium rounded-md border-1 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 m-4">
          </div>
          <div class="flex items-center">
            <label for="text-gray-900">Message</label>
            <input type="text" v-model="container_params.message" class="block w-full font-medium rounded-md border-1 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 m-4">
          </div>
          <div class="flex gap-2 items-center" @click="toggleActive = !toggleActive">
            <label for="text-gray-900">Pause Container</label>
            <div class="w-16 h-10 flex items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out" :class="{ 'bg-green-500': toggleActive}">
              <div class="bg-white w-8 h-8 rounded-full shadow-md transform duration-300 ease-in-out" :class="{ 'translate-x-6': toggleActive,}"></div>
            </div>
        </div>
        <button
                @click="commit_pod()"
                class="bg-blue-500 text-white ml-2 mr-2 p-2 pl-4 pr-4 rounded-md hover:bg-blue-600 focus:outline focus:ring focus:border-blue-700 m-4"
              >
                Commit
        </button>    
        </div>
      </div>
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

export default {
  name: 'RunningPods',
  data() {
    return {
      runningPods: [],
      modal_close:false,
      toggleActive:false,
      selected_pod:"",
      container_params: {
      tag: "",
      message: "",
      pause: this.toggleActive
    }
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
    },open_modal(pod){
      this.selected_pod = pod
      console.log(this.selected_pod.container_id)
      this.modal_close = true
    },close_modal(){
      this.modal_close = false
    },
    async commit_pod() {
      try {

        const response = await fetch(
          '/api/method/flashdesk.api.pods.running_pods.commit_pod',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ container_id: this.selected_pod.container_id,container_params:this.container_params}),
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
          this.close_modal()
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
  components: { SideNavbar },
}
</script>
