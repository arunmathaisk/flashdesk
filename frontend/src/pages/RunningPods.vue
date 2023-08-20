<template>
    <div class="h-screen flex overflow-hidden">
      <SideNavbar />
      <div id="test" class="flex-grow p-8 bg-white-200 overflow-auto">
        <h1 class="text-3xl font-semibold mb-6 text-gray-800">Currently Running Pods</h1>
        <hr class="border-t-2 border-teal-400 my-6" />
        <div class="grid grid-cols-1">
          <div
            v-for="(pod, index) in runningPods"
            :key="index"
            class="border-2 border-teal-500 bg-white shadow-lg p-6 m-6"
          >
          <h3
            class="text-xl font-bold text-gray-800"
            style="display: grid; grid-template-columns: 1fr auto"
          >
            Container Name : {{ pod.container_name }}
            <button
              class="bg-teal-500 text-white p-2 pl-4 pr-4 hover:bg-teal-600 focus:outline focus:ring focus:border-teal-700"
            >
              Terminate
            </button>
          </h3>
            <hr class="border-t-2 border-teal-400 my-6" />
            <div class="mt-4">
              <div class="pb-2 mt-2 ">
                <p class="text-gray-700">
                  <strong>Short ID : </strong> {{pod.container_shortid }}
                </p>
              </div>
              <div class="pb-2 mt-2">
                <p class="text-gray-700">
                  <strong>Tags : </strong> {{ pod.container_image_tags}}
                </p>
              </div>
              <div class="mt-2">
                <p class="text-gray-700"><strong>Status : </strong> {{ pod.container_status }}</p>
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
      }
    },
    mounted() {
      this.fetchRunningPods()
    },
    methods: {
      async fetchRunningPods() {
        try {
          const response = await fetch(
            '/api/method/flashdesk.api.pods.running_pods.get_all_actively_running_pod_images'
          )
          const data = await response.json()
          this.runningPods= data.message
        } catch (error) {
          console.error('Error fetching images:', error)
        }
      },
    },
    components: { SideNavbar },
  }
  </script>
  