<template>
  <div class="p-6">
    <h1 class="text-3xl font-semibold my-4 text-gray-800">
      Download Tar Files
    </h1>
    <hr class="border-t-2 border-violet-500 my-6" />
  </div>

  <div class="p-4 m-2">
    <h3>List Of Downloadable Tar Files for images</h3>
    <div v-if="tarlist.length != 0">
      <li v-for="x in tarlist" class="flex items-center gap-6">
        {{ x }}
        <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
        <svg
          @click="download_tar(x)"
          fill="#000000"
          height="20px"
          width="20px"
          version="1.1"
          id="Capa_1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          viewBox="0 0 29.978 29.978"
          xml:space="preserve"
        >
          <g>
            <path
              d="M25.462,19.105v6.848H4.515v-6.848H0.489v8.861c0,1.111,0.9,2.012,2.016,2.012h24.967c1.115,0,2.016-0.9,2.016-2.012
		v-8.861H25.462z"
            />
            <path
              d="M14.62,18.426l-5.764-6.965c0,0-0.877-0.828,0.074-0.828s3.248,0,3.248,0s0-0.557,0-1.416c0-2.449,0-6.906,0-8.723
		c0,0-0.129-0.494,0.615-0.494c0.75,0,4.035,0,4.572,0c0.536,0,0.524,0.416,0.524,0.416c0,1.762,0,6.373,0,8.742
		c0,0.768,0,1.266,0,1.266s1.842,0,2.998,0c1.154,0,0.285,0.867,0.285,0.867s-4.904,6.51-5.588,7.193
		C15.092,18.979,14.62,18.426,14.62,18.426z"
            />
            <g></g>
            <g></g>
            <g></g>
            <g></g>
            <g></g>
            <g></g>
            <g></g>
            <g></g>
            <g></g>
            <g></g>
            <g></g>
            <g></g>
            <g></g>
            <g></g>
            <g></g>
          </g>
        </svg>
        <svg
          @click="delete_tar(x)"
          height="10px"
          width="10px"
          version="1.1"
          id="Layer_1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          viewBox="0 0 511.999 511.999"
          xml:space="preserve"
        >
          <path
            style="fill: #ff6465"
            d="M384.955,256l120.28-120.28c9.019-9.019,9.019-23.642,0-32.66L408.94,6.765
      c-9.019-9.019-23.642-9.019-32.66,0l-120.28,120.28L135.718,6.765c-9.019-9.019-23.642-9.019-32.66,0L6.764,103.058
      c-9.019,9.019-9.019,23.642,0,32.66l120.28,120.28L6.764,376.28c-9.019,9.019-9.019,23.642,0,32.66l96.295,96.294
      c9.019,9.019,23.642,9.019,32.66,0l120.28-120.28l120.28,120.28c9.019,9.019,23.642,9.019,32.66,0l96.295-96.294
      c9.019-9.019,9.019-23.642,0-32.66L384.955,256z"
          />
        </svg>
      </li>
    </div>
    <div v-else>No files here to download</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tarlist: [],
      required: false,
    }
  },
  methods: {
    async fetch_tar_list() {
      try {
        const response = await fetch(
          '/api/method/flashdesk.api.pod_image.list_all_tar_files'
        )
        const data = await response.json()
        console.log(data.message)
        this.tarlist = data.message
      } catch (error) {
        console.error('Error fetching tar files', error)
      }
    },
    async delete_tar(file_name) {
      let delete_endpoint =
        '/api/method/flashdesk.api.pod_image.saved_file_delete'
      let file_json = {
        name: file_name,
      }
      let response = await fetch(delete_endpoint, {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(file_json),
      })
      let reply = await response.json()
      this.fetch_tar_list()
    },
    async download_tar(file_name) {
      let download_endpoint = `/api/method/flashdesk.api.pod_image.download_tar_file?name=${file_name}`
      window.open(download_endpoint)
    },
  },
  created() {
    this.fetch_tar_list()
  },
}
</script>
