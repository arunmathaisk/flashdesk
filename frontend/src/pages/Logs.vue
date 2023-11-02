<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />

    <div class="bg-white border w-screen">
      <div class="p-6">
        <h1 class="text-3xl font-semibold my-4 text-gray-800">
          Terminated Pods
        </h1>
        <hr class="border-t-2 border-pink-500 my-6" />
      </div>
      <div
        v-for="pod in terminatedPods"
        :key="pod.container_short_id"
        class="border-2 border-pink-500 rounded-lg p-4 m-4"
      >
        <div class="flex justify-between items-center">
          <p class="text-lg font-semibold">
            Container ID: {{ pod.container_short_id }}
          </p>
          <button
            @click="toggleDropdown(pod.container_short_id)"
            class="focus:outline-none"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              class="w-6 h-6 transition-transform transform rotate-0 hover:rotate-180 duration-300 ease-in-out"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 9l-7 7-7-7"
              ></path>
            </svg>
          </button>
        </div>
        <div
          v-if="showDropdown(pod.container_short_id)"
          class="mt-2 bg-white border-2 border-pink-500 border-gray-300 p-4 rounded-lg shadow-lg"
        >
          <div class="mb-2">
            <p class="text-sm text-gray-600">
              <strong>Name:</strong> {{ pod.name }}
            </p>
            <p class="text-sm text-gray-600">
              <strong>Image ID:</strong> {{ pod.image_id }}
            </p>
            <p class="text-sm text-gray-600">
              <strong>Available Ports:</strong> {{ pod.available_ports }}
            </p>
            <p class="text-sm text-gray-600">
              <strong>VNC Port:</strong> {{ pod.vnc_port }}
            </p>
            <p class="text-sm text-gray-600">
              <strong>Port Bindings:</strong> {{ pod.port_bindings }}
            </p>
            <p class="text-sm text-gray-600">
              <strong>Timestamp:</strong> {{ pod.timestamp }}
            </p>
            <p class="text-sm text-gray-600">
              <strong>Container Labels:</strong> {{ pod.container_labels }}
            </p>
            <p class="text-sm text-gray-600">
              <strong>Terminated Timestamp:</strong>
              {{ pod.terminated_timestamp }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SideNavbar from '@/components/SideNavbar.vue'

export default {
  name: 'Events',
  components: {
    SideNavbar,
  },
  data() {
    return {
      terminatedPods: [], // Populate this array with the data from the API response
      expandedDropdowns: [], // Keeps track of the expanded state for each dropdown
    }
  },
  methods: {
    // Fetch data from the API and assign it to the terminatedPods array
    async fetchTerminatedPods() {
      try {
        const response = await fetch(
          '/api/method/flashdesk.api.pods.running_pods.get_all_terminated_pods'
        )
        const data = await response.json()
        this.terminatedPods = data.message
      } catch (error) {
        console.error('Error fetching terminated pods:', error)
      }
    },
    toggleDropdown(containerId) {
      const index = this.expandedDropdowns.indexOf(containerId)
      if (index > -1) {
        this.expandedDropdowns.splice(index, 1)
      } else {
        this.expandedDropdowns.push(containerId)
      }
    },
    showDropdown(containerId) {
      return this.expandedDropdowns.includes(containerId)
    },
  },
  created() {
    // Call the method to fetch terminated pods when the component is created
    this.fetchTerminatedPods()
  },
}
</script>

<style>
.border-pink-500 {
  border-color: #ec4899; /* Use your preferred shade of pink here */
}
.border-violet-500 {
  border-color: #7f00ff; /* Use your preferred shade of violet here */
}
</style>
