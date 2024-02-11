<template>
  <div class="w-screen flex-grow p-8 bg-white-200 overflow-auto">
    <h1 class="text-3xl font-semibold mb-6 text-gray-800">
      {{ form_label }}
    </h1>
    <hr class="border-t-2 border-amber-400" />
    <div class="w-full p-8">
      <div v-for="detail in form_details" class="p-4">
        <div v-if="detail.type == 'FileUpload'">
          <FileUpload
            @file_path="file_uploaded"
            label="Upload Tar File"
            :required="detail.defaultRequired"
          />
        </div>
        <div v-else-if="detail.type == 'select'">
          <label
            :for="detail.type"
            class="block font-medium leading-6 text-gray-900" :class="detail.defaultRequired ? 'text-red-500': 'text-gray-900'"
            >{{ detail.label }}</label
          ><br />
          <select v-model="detail.value" :name="detail.name" :class="detail.defaultRequired ? 'border-red-300': 'border-black-300' ">
            <option v-for="option in detail.options" :value="option">
              {{ option }}
            </option>
          </select>
        </div>
        <div v-else>
          <label
            :for="detail.type"
            class="block font-medium leading-6 text-gray-900" :class="detail.defaultRequired ? 'text-red-500': 'text-gray-900' "
            >{{ detail.label }}</label
          >
          <div class="mt-2">
            <input
              :required="detail.default"
              :name="detail.name"
              v-model="detail.value"
              :type="detail.type"
              class="block w-full font-medium rounded-md border-1 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" :class="detail.defaultRequired ? 'border-red-300': 'border-black-300' "
            />
          </div>
        </div>
      </div>
      <div>
        <button
          class="bg-amber-300  p-4 m-4 hover:bg-amber-600 focus:outline focus:ring focus:border-amber-700"
          :disabled=disabled
          @click="validateform"
        >
          Submit
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import FileUpload from '@/components/FileUpload.vue'
import { FastForwardIcon } from 'vue-feather-icons'
export default {
  name: 'Forms',
  props: ['form_label', 'form_details', 'form_action'],
  data() {
    return {
      detail_to_be_sent: {},
      file_path: null,
      required_fields:[],
      disabled:null,
    }
  },
  created(){
    for(let i=0;i<this.form_details.length;i++){
      if(this.form_details[i].isRequired){
        this.required_fields.push(this.form_details[i])
      }
    }
  },
  methods: {
    async submitForm() {
      let detail_to_be_sent = new Object()
      for (let i = 0; i < this.form_details.length; i++) {
        if (this.form_details[i].type == 'FileUpload') {
          detail_to_be_sent[this.form_details[i].name] = this.file_path
        } else {
          detail_to_be_sent[this.form_details[i].name] =
            this.form_details[i].value
        }
      }
      let url = window.location.origin + this.form_action
      let response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(detail_to_be_sent),
      })
      if(response.status == 200){
          this.toast("success","Pod Details Added",'')
          window.location.reload()
      }else{

      }
    },
    file_uploaded(file_path) {
      this.file_path = file_path
    },
    validateform(){
      let filled_fields = 0
      for(let i =0;i<this.required_fields.length;i++){
        if(this.required_fields[i].type == "FileUpload"){
            if(this.file_path == null){
              this.required_fields[i].defaultRequired = true;
            }else{
              this.required_fields[i].defaultRequired = false;
              filled_fields++;
            }
        }else{
            if(this.required_fields[i].value == ''){
              this.required_fields[i].defaultRequired = true;
            }else{
              this.required_fields[i].defaultRequired = false;
              filled_fields++;
            }
        }
      }

      if(this.required_fields.length == filled_fields){
        this.submitForm()
      }else{
        this.toast("warning","Fill the required fields","The red ones")
      }
    },toast(icon, title, text) {
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
    }
  },
  components: {
    FileUpload,
  },
}
</script>
