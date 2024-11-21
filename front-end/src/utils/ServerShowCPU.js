import * as echarts from 'echarts';

export function initCpuPieChart(el, data) {
    const PieCpuChart = echarts.init(el);
    const pieCpuChartOption = {
        title: {
            text: "CPU 占用率",
            left: "center",
        },
        tooltip: {
            trigger: "item",
        },

        series: [
            {
                name: "CPU 占用率",
                type: "pie",
                radius: "50%",
                data: data,
            }
        ]
    }
    PieCpuChart.setOption(pieCpuChartOption);
}

export function initGpuPieChart(el, data) {
    const PieGpuChart = echarts.init(el);
    const PieGpuChartOption = {
        title: {
            text: "GPU 占用率",
            left: "center",
        },
        tooltip: {
            trigger: "item",
        },

        series: [
            {
                name: "GPU 占用率",
                type: "pie",
                radius: "50%",
                data: data
            }
        ]
    }
    PieGpuChart.setOption(PieGpuChartOption);
}

export function updatePieChart(chart, data) {
    const option = {
        series: [
            {
                data: data
            }
        ]
    }
    chart.setOption(option);
}
