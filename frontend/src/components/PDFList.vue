<template>
    <div class="p-6">
      <h1 class="text-3xl font-semibold my-4 text-gray-800">Upload PDS for chatbot</h1>
      <hr class="border-t-2 border-violet-500 my-6" />
    </div>
    <div class="bg-white rounded-lg p-4 m-2">
        <FileUpload
            @file_path="file_uploaded"
            label="Upload PDF File"
            :required=required
        />
    </div>
  </template>
  
  <script>
  import FileUpload from '@/components/FileUpload.vue'
  export default {
    data() {
      return {
        required:false,
      }
    },
    methods:{
        file_uploaded(file_path) {
      this.file_path = file_path
    }
    },
    components: {
    FileUpload,
  },
  }
  </script>
  