<template>
  <div class="p-8">
    <h1 class="text-xl font-semibold text-black">Remote Queue Jobs</h1>
    <hr class="border-t-2 border-black my-6" />
    <div class="bg-white">
      <div
        v-for="job in reversedCompletedJobs"
        :key="job.job_id"
        class="border-2 border-black rounded-lg p-4 m-4"
      >
        <div class="flex justify-between items-center">
          <p class="text-black"> <span class="text-md font-bold">Job Name: </span>{{ job.job_name }}</p>
        </div>
      
        <hr class="border-t-2 border-black my-3" />

        <div class="mt-2">
          <div class="mb-2">
            <p class="text-sm text-black">
              Status: {{ job.status }}
            </p>
            <p class="text-sm text-black">
              Started At: {{ job.started_at }}
            </p>
            <p class="text-sm text-black">
              Ended At: {{ job.ended_at }}
            </p>
            <p class="text-sm text-black">
              Time Taken: {{ job.time_taken }} seconds
            </p>
            <br>
            <pre class="text-sm text-black p-2 bg-gray-100 rounded-md">{{ job.arguments }}</pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      completedJobs: [], // Array to hold job data
    }
  },
  computed: {
    reversedCompletedJobs() {
      return this.completedJobs.slice().reverse();
    },
  },
  methods: {
    async fetchData() {
      // API endpoint to fetch job data
      const apiUrl = '/api/method/flashdesk.api.rq_stuff.get_new_completed_queues2';
      try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        if (data.message && data.message.completed_jobs) {
          this.completedJobs = data.message.completed_jobs;
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
  },
  mounted() {
    this.fetchData();
    // Set an interval to fetch data every 5 seconds
    setInterval(this.fetchData, 5000);
  },
}
</script>
