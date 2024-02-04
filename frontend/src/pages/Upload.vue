<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <Forms
      form_label="Upload PDFS"
      :form_details="formObj"
      form_action="/api/method/flashdesk.api.image_create.insert_image"
      submit_button="off"
    />
  </div>
</template>
<script>
  import SideNavbar from '@/components/SideNavbar.vue'
  import FileUpload from '@/components/FileUpload.vue'
  import Forms from '@/components/Forms.vue'
  
  export default {
    name: 'PDFS',
    components: {
      SideNavbar,
      FileUpload,
      Forms
    },
    data(){
      return {
      formObj: [
        {
          type: 'FileUpload',
          name: 'image_file',
          value: '',
          isRequired: true,
          defaultRequired:null
        },
      ],
    }
    }
  }
</script>
  