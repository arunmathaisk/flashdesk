<template>
  <div class="flex bg-white h-screen md:w-1/6 shadow-lg rounded-lg overflow-y-auto">
    <div class="p-6 w-full bg-gray-100"> <!-- Add bg-gray-100 class here for the light grey background -->
      <h1 class="text-blue-500 text-4xl md:text-5xl font-semibold mb-6">FlashDesk</h1>
      <ul class="space-y-3">
        <li v-for="item in menuItems" :key="item.id">
          <router-link :to="item.path" class="text-gray-800 text-xl md:text-2xl hover:text-blue-500">{{ item.title }}</router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  export default {
    name:'SideNavbar',
    data() {
      return {
        menuItems: [
          { id: 1, title: '', path: '/' },
          { id: 2, title: 'About', path: '/about' },
          { id: 3, title: 'Contact', path: '/contact' },
          { id: 3, title: 'Say hello', path: '/hello' },
        ],
      };
    },
  };
  </script>
