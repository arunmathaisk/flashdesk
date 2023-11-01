<template>
  <div
    class="card"
    style="
      background-color: #ffffff;
      border: 2px solid #0000ff;
      border-radius: 10px;
      box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
      padding: 10px;
      margin: 10px;
    "
  >
    <div class="bg-violet text-gray px-4 py-2">Live CPU and Memory Usage</div>
    <div class="p-4">
      <div ref="chart"></div>
    </div>
  </div>
</template>

<script>
import Highcharts from 'highcharts'
import HighchartsVue from 'highcharts-vue'
import stockInit from 'highcharts/modules/stock'

stockInit(Highcharts)

export default {
  name: 'UsageGraph',
  data() {
    return {
      chartOptions: {
        xAxis: {
          type: 'datetime',
        },
        yAxis: {
          title: {
            text: 'Percentage',
          },
        },
        series: [
          {
            name: 'CPU Usage',
            data: [],
          },
          {
            name: 'Memory Usage',
            data: [],
          },
        ],
      },
    }
  },
  mounted() {
    this.chart = Highcharts.stockChart(this.$refs.chart, this.chartOptions)

    // Simulate live data
    setInterval(() => {
      const x = new Date().getTime() // current time
      const yCPU = Math.random() * 100 // random CPU usage
      const yMemory = Math.random() * 100 // random Memory usage

      const cpuSeries = this.chart.series[0]
      const memorySeries = this.chart.series[1]

      const shift = cpuSeries.data.length > 20 // shift if the series is longer than 20

      cpuSeries.addPoint([x, yCPU], true, shift)
      memorySeries.addPoint([x, yMemory], true, shift)
    }, 1000) // Update every 1 second
  },
}
</script>

<style>
.border-violet {
  border-color: violet;
}
</style>
