<template>
    <div class="h-screen flex">
      <SideNavbar />
      <div class="flex flex-col w-screen bg-sky-200">
        <div class="p-4 flex items-center">
          <input
            type="text"
            placeholder="Search..."
            class="p-2 border border-gray-300 focus:outline-none focus:ring focus:border-blue-500 flex-grow"
          />
          <div class="pl-4">
            <button
              class="bg-blue-500 text-white p-2 hover:bg-blue-600 focus:outline-none focus:ring focus:border-blue-700"
            >
              Search
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>

<script>
import { Dialog } from 'frappe-ui';
import SideNavbar from '@/components/SideNavbar.vue';
import UserDetails from '../components/UserDetails.vue';
import UserDisclaimer from '../components/UserDisclaimer.vue';


export default {
  name: 'DockerHubSearch',
  components: {
    SideNavbar,
    UserDetails,
    UserDisclaimer
}

}
</script>
