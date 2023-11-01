<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <div id="test" class="flex-grow p-8 bg-emrald-300 overflow-auto">
      <h1 class="text-3xl font-semibold mb-6 text-gray-800">Pod Images</h1>
      <hr class="border-t-2 border-blue-400 my-6" />
      <div class="grid grid-cols-1">
        <div
          v-for="(image, index) in podImages"
          :key="index"
          class="border-2 border-blue-400 bg-white shadow-lg p-6 m-6 rounded-md"
        >
        <h3
            class="text-xl font-bold text-gray-800 rounded-md"
            style="display: grid; grid-template-columns: 1fr auto"
          >
            {{ image.image_name }}
            <button
             @click="extractFile(image.name)" class="bg-blue-400 text-white p-2 pl-4 pr-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 " 
            >
              Extract
            </button>
          </h3>
          <hr class="border-t-2 border-blue-400 my-6 rounded-md" />
          <div class="mt-4">
            <div class="pb-2 mt-2 rounded-md">
              <p class="text-gray-700">
                <strong>Image ID:</strong> {{ image.image_id }}
              </p>
            </div>
            <div class="pb-2 mt-2 rounded-md">
              <p class="text-gray-700">
                <strong>Created On:</strong>
                {{ new Date(image.created_on).toDateString() }}
              </p>
            </div>
            <div class="pb-2 mt-2 rounded-md">
              <p class="text-gray-700">
                <strong>Created By:</strong> {{ image.created_by }}
              </p>
            </div>
            <div class="mt-2 rounded-md">
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
import SideNavbar from '@/components/SideNavbar.vue'
export default {
  name: 'PodImages',
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
	console.log(data)
        this.podImages = data.message
      } catch (error) {
        console.error('Error fetching images:', error)
      }
    },
   async extractFile(pod_id){
    try{
      let options = {
        method:"post",
        headers: {
          'Content-Type': 'application/json',
        },
        body:JSON.stringify({pod_id:pod_id})
      }
	    const response = await fetch('/api/method/flashdesk.api.pod_image.create_image_from_file',options)
	    const data = await response.json()
      this.toast(data.message.type,"Pod Image Extraction",data.message.message)
    }catch(error){
	    console.error('Error extracting tar to image',error)
    }
   },toast(icon, title, text) {
      this.$swal({
        toast: true,
        position: 'bottom-right',
        showConfirmButton: false,
        timer: 3000,
        icon: 'success',
        title: title,
        text: text,
        showCancelButton: 'true',
      })
    }
  },
  components: { SideNavbar },
}
</script>
