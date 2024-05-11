<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <div class="flex-grow p-8 overflow-auto">
      <h1 class="text-xl font-semibold mb-6 text-black">Search Docker Hub</h1>
      <hr class="border-t-2 border-black my-6" />
      <div class="p-4 flex items-center mb-3">
        <TextInput
          :type="'text'"
          placeholder="Search..."
          v-model="searchInput"
          @input="fetchDockerHubImages"
          class="flex-grow border-2 border-black rounded-md"
          size="md"
        />
        <div class="pl-4">
          <Button
            size="md"
            :variant="'solid'"
            theme="gray"
            @click="fetchDockerHubImages"
          >
            Search
          </Button>
        </div>
      </div>
      <div class="grid grid-cols-3 gap-3">
        <div
          v-for="(image, index) in dockerImages"
          :key="index"
          class="border-2 border-black bg-white shadow-lg p-6 rounded-md"
        >
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-md font-bold text-black">
              Image Name: {{ image.name }}
            </h3>
            <Button
              size="sm"
              :variant="'solid'"
              theme="gray"
              @click="docker_pull(image.name)"
            >
              Pull
            </Button>
          </div>
          <hr class="border-t border-black my-4" />
          <div>
            <p class="text-gray-700">Official: {{ image.is_official }}</p>
            <p class="text-gray-700">Automated: {{ image.is_automated }}</p>
            <p class="text-gray-700">Star Count: {{ image.star_count }}</p>
            <p class="text-gray-700">Description: {{ image.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { TextInput, Button } from 'frappe-ui'
import SideNavbar from '@/components/SideNavbar.vue'

const searchInput = ref('')
const dockerImages = ref([])

const fetchDockerHubImages = async () => {
  try {
    const response = await fetch(
      `/api/method/flashdesk.api.pod_image.docker_hub_search?search_query=${searchInput.value}`
    )
    const data = await response.json()
    dockerImages.value = data.message
  } catch (error) {
    console.error('Error fetching images:', error)
  }
}

const docker_pull = async (imageName) => {
  try {
    const response = await fetch(
      `/api/method/flashdesk.api.pod_image.docker_pull`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image_name: imageName }),
      }
    )
    if (response.ok) {
      Swal.fire({
        toast: true,
        position: 'bottom-right',
        showConfirmButton: false,
        timer: 3000,
        icon: 'success',
        title: 'Success',
        text: 'Image pull has started in the background. Check events for more information.',
      })
    } else {
      const data = await response.json()
      Swal.fire({
        toast: true,
        position: 'bottom-right',
        showConfirmButton: false,
        timer: 3000,
        icon: 'error',
        title: 'Error',
        text: data.messages,
      })
    }
  } catch (error) {
    console.error('Error pulling images:', error)
  }
}
</script>
