<template>
    <div class="p-6">
      <h1 class="text-3xl font-semibold my-4 text-gray-800">Upload PDFs for chatbot</h1>
      <hr class="border-t-2 border-violet-500 my-6" />
    </div>
    <div class="rounded-lg p-4 m-2">
        <FileUpload
            @file_path="file_uploaded"
            label="Upload PDF File"
            :required=required
        />
    </div>

    <div class="p-4 m-2">
      <h3>List of PDFs Uploaded</h3>
      <div v-if="pdflist.length != 0"> 
        <li v-for="x in pdflist" class="flex items-center justify-between">{{ x }}
    <svg @click="delete_pdf(x)" height="10px" width="10px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
      viewBox="0 0 511.999 511.999" xml:space="preserve">
    <path style="fill:#FF6465;" d="M384.955,256l120.28-120.28c9.019-9.019,9.019-23.642,0-32.66L408.94,6.765
      c-9.019-9.019-23.642-9.019-32.66,0l-120.28,120.28L135.718,6.765c-9.019-9.019-23.642-9.019-32.66,0L6.764,103.058
      c-9.019,9.019-9.019,23.642,0,32.66l120.28,120.28L6.764,376.28c-9.019,9.019-9.019,23.642,0,32.66l96.295,96.294
      c9.019,9.019,23.642,9.019,32.66,0l120.28-120.28l120.28,120.28c9.019,9.019,23.642,9.019,32.66,0l96.295-96.294
      c9.019-9.019,9.019-23.642,0-32.66L384.955,256z"/>
    </svg>
</li>

      </div>
      <div v-else>
        No files for the Chatbot here yet
      </div>
    </div>
  </template>
  
  <script>
  import FileUpload from '@/components/FileUpload.vue'
  export default {
    data() {
      return {
        pdflist:[],
        required:false,
      }
    },
    methods:{
    file_uploaded(file_path) {
      console.log("file done",file_path)
      this.start_processing()
    },
    async start_processing(){
      const process_endpoint = '/api/method/flashdesk.api.ai.process_pdfs.start_processing'
      const response =  await fetch(process_endpoint);
      const reply = response.json()
      this.$toast("success","Processing begins",reply.message);
      this.fetch_pdf_list()
    },
    async fetch_pdf_list(){
      try {
        const response = await fetch(
          '/api/method/flashdesk.api.fileupload.files.list_all_pdf_files'
        )
        const data = await response.json()
        console.log(data.message)
        this.pdflist = data.message
      } catch (error) {
        console.error('Error fetching pdf files', error)
      }
    },
    async delete_pdf(file_name) {
      let delete_endpoint  = '/api/method/flashdesk.api.fileupload.files.file_delete';
      let file_json = {
        name : file_name
      }
      let response = await fetch(delete_endpoint,{
        method:"post",
        headers:{
          "Content-Type":"application/json"
        },
        body:JSON.stringify(file_json)
      })
      let reply = await response.json()
      this.fetch_pdf_list()
    }
    },
    created(){
      this.fetch_pdf_list()
    },
    components: {
    FileUpload,
  },
  }
  </script>
  