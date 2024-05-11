<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <div class="flex-col w-screen bg-white-200 overflow-auto">
      <TarList />
    </div>
  </div>
</template>

<script>
import SideNavbar from '@/components/SideNavbar.vue'
import FileUpload from '@/components/FileUpload.vue'
import Forms from '@/components/Forms.vue'
import PDFList from '@/components/PDFList.vue'
import TarList from '@/components/TarList.vue'
export default {
  name: 'SavedFiles',
  components: {
    SideNavbar,
    FileUpload,
    Forms,
    PDFList,
    TarList,
  },
}
</script>
