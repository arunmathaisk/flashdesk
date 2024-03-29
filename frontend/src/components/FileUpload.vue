<template>
  <div class="w-full" @dragover="prevent" @drop="dropFile">
    <label class="block font-medium leading-6  py-2" :class="required ? 'text-red-700': 'border-black-300'">{{
      label
    }}</label>
    <div
      v-if="!uploaded_files"
      class="flex justify-center w-full h-32 px-4 transition bg-white border-2  border-dashed rounded-md appearance-none cursor-pointer hover:border-gray-400 focus:outline-none"  :class="required ? 'border-red-300': 'border-black-300' "
    >
      <span class="flex items-center space-x-2">
        <svg
          @click="removeFile"
          xmlns="http://www.w3.org/2000/svg"
          class="w-6 h-6 text-gray-600"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
        <span class="font-medium text-gray-600">
          Drop files to Attach, or
          <a @click="browserfile" class="text-blue-600 underline">browse</a>
        </span>
      </span>
      <input

        @change="dropFile"
        type="file"
        ref="file"
        name="file_upload"
        class="hidden"
        multiple
      />
    </div>
    <div
      v-else
      class="flex flex-col w-full h-32 px-4 justify-center transition bg-white border-2 border-black-300 border rounded-md appearance-none cursor-pointer hover:border-gray-400 focus:outline-none max-wd-max" :class="required ? 'border-red-300': 'border-black-300' "
    >
      <div class="text-gray-600 font-medium flex items-center justify-between">
        {{ uploaded_files.name }}
        <div @click="removeFile">
          <svg
            class="font-medium w-5 h-5"
            viewBox="0 0 21 21"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g
              fill="none"
              fill-rule="evenodd"
              stroke="#000000"
              stroke-linecap="round"
              stroke-linejoin="round"
              transform="matrix(0 1 1 0 2.5 2.5)"
            >
              <path
                d="m3.98652376 1.07807068c-2.38377179 1.38514556-3.98652376 3.96636605-3.98652376 6.92192932 0 4.418278 3.581722 8 8 8s8-3.581722 8-8-3.581722-8-8-8"
              />

              <path d="m4 1v4h-4" transform="matrix(1 0 0 -1 0 6)" />
            </g>
          </svg>
        </div>
      </div>
      <br />
      <div class="mb-5 h-2 rounded-full bg-gray-200 w-full">
        <div
          class="h-2 rounded-full bg-orange-500"
          :style="{ width: upload_progress+ '%' }"
        ></div>
      </div>
      <br />
    </div>
  </div>
</template>

<script>
export default {
  name: 'FileUpload',
  props: ['label', 'required'],
  data() {
    return {
      uploaded_files: null,
      total_chunks: 0,
      chunksize: 1000000,
      file_upload_endpoint:
        '/api/method/flashdesk.api.fileupload.files.file_upload',
      upload_progress: 0,
    }
  },
  methods: {
    async submitFile() {
      for(let chunk_id = 0;chunk_id < this.total_chunks + 1;chunk_id++){
        let chunk = this.uploaded_files.slice(chunk_id * this.chunksize,chunk_id * this.chunksize + this.chunksize)
        let file_parts = new FormData()
        file_parts.set('file', chunk)
        file_parts.set('current_chunk', chunk_id)
        file_parts.set('filename', this.uploaded_files.name)
        file_parts.set('filesize', this.uploaded_files.size)
        file_parts.set('offset', chunk_id * this.chunksize)
        file_parts.set('total_chunks', this.total_chunks)

        let fetch_options = {
          method:"post",
          body:file_parts
        }
        let response = await fetch(window.location.origin + this.file_upload_endpoint,fetch_options)
        let reply =await response.json()
        if(reply.exc_type == 'CSRFTokenError'){
          window.location.href = '/frontend/login'
        }

        if(reply.message.type){
          if(reply.message.success){
            this.toast(reply.message.type,reply.message.title,reply.message.body);
            this.$emit("file_path",reply.message.filepath)
            break;
          }else{
            this.toast(reply.message.type,reply.message.title,reply.message.body);
            this.removeFileUI()
            break;
          }
        }

        

        this.upload_progress = Math.round((chunk_id*100)/this.total_chunks)
      }
    },
    browserfile() {
      this.$refs.file.click()
    },
    prevent(event) {
      event.preventDefault()
    },
    dropFile(event) {
      event.preventDefault()
      if (event.type == 'change') {
        this.uploaded_files = this.$refs.file.files[0]
      } else {
        this.uploaded_files = event.dataTransfer.files[0]
      }
      this.total_chunks = this.uploaded_files.size / this.chunksize
      console.log('No of chunks to transmit are', this.total_chunks)
      this.submitFile()
    },
    async removeFile() {
      let delete_endpoint  = '/api/method/flashdesk.api.fileupload.files.file_delete';
      let file_json = {
        name : this.uploaded_files.name
      }
      let response = await fetch(delete_endpoint,{
        method:"post",
        headers:{
          "Content-Type":"application/json"
        },
        body:JSON.stringify(file_json)
      })
      let reply = await response.json()
      this.uploaded_files = null
      this.no_of_chunks = null
      this.upload_progress = null
    },async removeFileUI() {
      this.uploaded_files = null
      this.no_of_chunks = null
      this.upload_progress = null
    },
    toast(icon, title, text) {
      this.$swal({
        toast: true,
        position: 'bottom-right',
        showConfirmButton: false,
        timer: 3000,
        icon: icon,
        title: title,
        text: text,
        showCancelButton: 'true',
      })
    },
  },
  emits: ['file_path'],
}
</script>
