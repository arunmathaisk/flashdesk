<template>
          <div
        v-if="modal_close"
        class="flex flex-col p-2 border-2 border-teal-500 bg-white shadow-lg p-6 m-6 rounded w-fit fixed inset-0 max-w-xl mx-auto my-auto z-50 h-fit"
      >
        <h1>New Image Details</h1>
        <div class="flex flex-col">
          <div class="flex items-center">
            <label for="text-gray-900">Image Name</label>
            <input
              type="text"
              v-model="container_params.image_name"
              class="block w-full font-medium rounded-md border-1 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 m-4"
            />
          </div>
          <div class="flex items-center ">
            <label for="text-gray-900">Tag</label>
            <input
              type="text"
              v-model="container_params.tag"
              class="block w-full font-medium rounded-md border-1 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 m-4"
            />
          </div>
          <div class="flex items-center">
            <label for="text-gray-900">Message</label>
            <input
              type="text"
              v-model="container_params.message"
              class="block w-full font-medium rounded-md border-1 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 m-4"
            />
          </div>
          <div class="flex items-center justify-evenly">
            <input checked id="checked-checkbox" type="checkbox" v-model="container_params.pause" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
            <label for="checked-checkbox" class="text-gray-900 ">Pause Container</label>
          </div>
          <button
            @click="commit_pod()"
            class="bg-blue-500 text-white ml-2 mr-2 p-2 pl-4 pr-4 rounded-md hover:bg-blue-600 focus:outline focus:ring focus:border-blue-700 m-4"
          >
            Commit
          </button>
        </div>
      </div>
</template>

<script>
export default {
    name:"Modal",
    props:['modal_close','selected_pod'],
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
    methods:{
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
          this.$emit('close_modal',false);
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