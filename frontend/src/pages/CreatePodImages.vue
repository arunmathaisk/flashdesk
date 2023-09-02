<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <Forms
      form_label="Create Pod Images"
      :form_details="formObj"
      form_action="/api/method/flashdesk.api.image_create.insert_image"
    />
  </div>
</template>

<script>
import SideNavbar from '../components/SideNavbar.vue'
import FileUpload from '../components/FileUpload.vue'
import Forms from '../components/Forms.vue'
export default {
  name: 'CreatePodImages',
  components: {
    SideNavbar,
    FileUpload,
    Forms,
  },
  data() {
    return {
      formObj: [
        {
          label: 'Image Name',
          type: 'text',
          name: 'image_name',
          value: '',
          isRequired: true,
        },
        {
          label: 'Image Description',
          type: 'text',
          name: 'image_description',
          value: '',
          isRequired: true,
        },
        {
          type: 'FileUpload',
          name: 'image_file',
          value: '',
          isRequired: true,
        },
        {
          label: 'Tags',
          type: 'text',
          name: 'tags',
          value: '',
          isRequired: null,
        },
        {
          label: 'Status',
          type: 'select',
          name: 'status',
          options: ['Draft', 'Published', 'Deprecated'],
          value: '',
          isRequired: null,
        },
      ],
    }
  },
}
</script>
