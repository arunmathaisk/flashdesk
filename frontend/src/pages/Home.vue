<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <div class="flex flex-col w-screen bg-white-200 overflow-auto">
      <UserDisclaimer />
      <UserDetails />
    </div>
  </div>
</template>

<script>
import { Dialog } from 'frappe-ui'
import SideNavbar from '@/components/SideNavbar.vue'
import UserDetails from '../components/UserDetails.vue'
import UserDisclaimer from '../components/UserDisclaimer.vue'

export default {
  name: 'Home',
  components: {
    SideNavbar,
    UserDetails,
    UserDisclaimer,
  },
}
</script>
