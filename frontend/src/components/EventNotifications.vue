<template>
  <div class="bg-white border rounded-lg p-4 m-4">
    <div v-for="job in reversedCompletedJobs" :key="job.job_id" class="border rounded-lg p-4 m-4">
      <div class="flex justify-between items-center">
        <p class="text-lg font-semibold">Job Name: {{ job.job_name }}</p>
        <button @click="toggleDropdown(job.job_id)" class="focus:outline-none">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            class="w-6 h-6 transition-transform transform rotate-0 hover:rotate-180 duration-300 ease-in-out"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 9l-7 7-7-7"
            ></path>
          </svg>
        </button>
      </div>
      <div v-if="showDropdown(job.job_id)" class="mt-2 bg-white border border-gray-300 p-4 rounded-lg shadow-lg">
        <div class="mb-2">
          <p class="text-sm text-gray-600"><strong>Status:</strong> {{ job.status }}</p>
          <p class="text-sm text-gray-600"><strong>Started At:</strong> {{ job.started_at }}</p>
          <p class="text-sm text-gray-600"><strong>Ended At:</strong> {{ job.ended_at }}</p>
          <p class="text-sm text-gray-600"><strong>Time Taken:</strong> {{ job.time_taken }} seconds</p>
          <p class="text-sm text-gray-600"><strong>Arguments:</strong></p>
          <pre class="text-sm text-gray-600 p-2 bg-gray-100 rounded-md">{{ job.arguments }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      completedJobs: [],
      openDropdowns: [], // To keep track of open/closed dropdowns
    };
  },
  computed: {
    reversedCompletedJobs() {
      return this.completedJobs.slice().reverse();
    },
  },
  methods: {
    toggleDropdown(jobId) {
      if (this.openDropdowns.includes(jobId)) {
        this.openDropdowns = this.openDropdowns.filter((id) => id !== jobId);
      } else {
        this.openDropdowns.push(jobId);
      }
    },
    showDropdown(jobId) {
      return this.openDropdowns.includes(jobId);
    },
    async fetchData() {
      // Replace with your API endpoint
      const apiUrl = "/api/method/flashdesk.api.rq_stuff.get_new_completed_queues2";
      
      try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        if (data.message && data.message.completed_jobs) {
          this.completedJobs = data.message.completed_jobs;
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
  mounted() {
    this.fetchData();
    // Fetch data every 5 seconds
    setInterval(this.fetchData, 5000);
  },
};
</script>
