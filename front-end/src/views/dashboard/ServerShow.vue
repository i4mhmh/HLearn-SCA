<template>
  <div class="container h-screen flex flex-col" style="height: 100%">
    <el-row class="flex-1">
      <el-col :span="12" style="justify-content: space-between">
        <div
          ref="pieCpuCharts"
          class="chart-container"
          style="width: 48%"
        ></div>
      </el-col>
      <el-col :span="12">
        <div ref="chartContainer" class="chart-container"></div>
      </el-col>
    </el-row>
    <el-row class="flex-1">
      <el-col :span="12"> 左下 </el-col>
      <el-col :span="12">
        <div>右下</div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from "echarts";
import { formatter } from "element-plus";
import {
  initCpuPieChart,
  initGpuPieChart,
  updatePieChart,
} from "@/utils/ServerShowCPU.js";

export default {
  name: "LineChart",
  data() {
    return {
      chart: null,
      data: [32, 25, 55, 33, 14, 56, 12, 23, 66, 78],
      xData: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    };
  },
  mounted() {
    this.initChart();
    this.startUpdatingData();
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose();
    }
  },
  methods: {
    // 初始化饼状图

    initChart() {
      this.chart = echarts.init(this.$refs.chartContainer);

      const option = {
        title: {
          text: "CPU占用率 %",
          top: "top",
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: [
            "11:10",
            "11:10",
            "11:10",
            "11:10",
            "11:10",
            "11:10",
            "11:10",
            "11:10",
            "11:10",
            "11:10",
          ],
        },
        yAxis: {
          type: "value",
          axisLabel: {
            formatter: "{value}%",
          },
        },
        series: [
          {
            name: "销量",
            type: "line",
            smooth: true,
            data: this.data,
            areaStyle: {},
          },
        ],
      };

      this.chart.setOption(option);
    },
    startUpdatingData() {
      setInterval(
        function () {
          this.data.shift();
          this.data.push(Math.round(Math.random() * 100));
          this.chart.setOption({
            series: [
              {
                data: this.data,
                xAxis: {
                  data: this.xData,
                },
              },
            ],
          });
        }.bind(this),
        2000
      );
    },
  },
};
</script>

<style scoped>
.chart-container {
  flex: 1;
  width: 100%;
  height: 100%; /* 确保图表容器占满整个列的高度和宽度 */
}

.el-row {
  height: 50%;
}
.el-col {
  height: 100%;
}
.row {
  flex: 1; /* 每个行占据相等的高度 */
  display: flex;
  flex-direction: row;
}
/* 可以在这里添加样式 */
</style>
