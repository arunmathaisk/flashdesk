<template>
  <div class="w-screen flex-grow p-8 bg-white-200 overflow-auto">
    <h1 class="text-3xl font-semibold mb-6 text-gray-800">
      {{ form_label}}
    </h1>
    <hr class="border-t-2 border-violet-400" />
    <div class="w-full p-8" >
      <div v-for="detail in form_details" class="p-4">
          <div v-if="detail.type == 'FileUpload'">
                <FileUpload @file_path="file_uploaded" label="Upload Tar File" :required="detail.isRequired"/>
          </div>
          <div v-else-if="detail.type == 'select'">
            <label :for=detail.type class="block font-medium leading-6 text-gray-900">{{ detail.label }}</label><br>
            <select v-model="detail.value" :name="detail.name">
              <option v-for="option in detail.options" :value="option">{{ option }}</option>
            </select>
          </div>
          <div v-else>
          <label :for=detail.type class="block font-medium leading-6 text-gray-900">{{ detail.label }}</label>
          <div class="mt-2">
            <input  :required=detail.isRequired :name=detail.name v-model="detail.value" :type=detail.type   required class="block w-full font-medium rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
          </div>
          </div>
      </div>
      <div>
        <button 
          class="bg-violet-500 text-white p-4 m-4 hover:bg-violet-600 focus:outline focus:ring focus:border-violet-700" @click="submitForm"
        >
          Submit
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import FileUpload from '@/components/FileUpload.vue';
export default{
  name:"Forms",
  props:['form_label','form_details','form_action'],
  data(){
    return {
      detail_to_be_sent:{},
      file_path:null
    }
  },
  methods:{
    async submitForm(){
      let detail_to_be_sent = new Object()
      for (let i = 0; i < this.form_details.length; i++) {
          if(this.form_details[i].type == "FileUpload"){
            console.log("hi")
            detail_to_be_sent[this.form_details[i].name] = this.file_path
            console.log(detail_to_be_sent[this.form_details[i].name])
          }else{
            console.log("i")
            detail_to_be_sent[this.form_details[i].name] = this.form_details[i].value
          }
      }
      let url = window.location.origin + this.form_action
      console.log(detail_to_be_sent)
      let response = await fetch(url,{
        method:"POST",
        headers: {
          "Content-Type": "application/json",
        },
        body:JSON.stringify(detail_to_be_sent)
      })
      let reply = response.json()
      console.log(response)
      
    },
    file_uploaded(file_path){
      this.file_path = file_path
      console.log(this.file_path)
    }
  },
  components:{
    FileUpload
  }
}
</script>