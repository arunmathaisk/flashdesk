<template>
<div class="h-screen flex">
<SideNavbar />
<UserDisclaimer />
<UserDetails />
</div>

</template>

<script>
import { Dialog } from 'frappe-ui';
import SideNavbar from '@/components/SideNavbar.vue';
import UserDetails from '../components/UserDetails.vue';
import UserDisclaimer from '../components/UserDisclaimer.vue';


export default {
  name: 'Home',
  components: {
    SideNavbar,
    UserDetails,
    UserDisclaimer
}

}
</script>
