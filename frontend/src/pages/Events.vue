<template>
  <div class="h-screen flex overflow-hidden">
    <SideNavbar />
    <div class="flex flex-col w-screen bg-white-200 overflow-auto">
    <EventNotifications></EventNotifications>
    </div>
  </div>
</template>

<script>
import SideNavbar from '@/components/SideNavbar.vue'
import EventNotifications from '@/components/EventNotifications.vue'

export default {
  name: 'Events',
  components: {
    SideNavbar,
    EventNotifications
  },
}
</script>
