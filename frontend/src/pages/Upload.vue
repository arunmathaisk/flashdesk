<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <div class="flex-col w-screen bg-white-200 overflow-auto">
      <PDFList></PDFList>
    </div>
  </div>
</template>
<script>
import SideNavbar from '@/components/SideNavbar.vue'
import FileUpload from '@/components/FileUpload.vue'
import Forms from '@/components/Forms.vue'
import PDFList from '@/components/PDFList.vue'

export default {
  name: 'PDFS',
  components: {
    SideNavbar,
    FileUpload,
    Forms,
    PDFList,
  },
  methods: {
    file_uploaded() {
      console.log(file_path)
    },
  },
  data() {
    return {
      formObj: [
        {
          type: 'FileUpload',
          name: 'image_file',
          value: '',
          isRequired: true,
          defaultRequired: null,
        },
      ],
    }
  },
}
</script>
