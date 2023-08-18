<template>
<div class="h-screen">
<SideNavbar />
</div>
</template>

<script>
import { Dialog } from 'frappe-ui';
import SideNavbar from '@/components/SideNavbar.vue';

export default {
  name: 'Home',
  components: {
    SideNavbar
  }

}
</script>
