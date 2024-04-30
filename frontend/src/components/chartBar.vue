<template>
    <div>
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import Chart from 'chart.js';
  
  export default {
    name: 'ChartComponent',
    props: ['chartData'],
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const ctx = this.$refs.chartCanvas.getContext('2d');
        new Chart(ctx, {
          type: 'bar', // Tipo de gráfico, puedes cambiarlo según tu necesidad
          data: this.chartData,
          options: {
            // opciones de Chart.js
          }
        });
      }
    }
  };
  </script>
  
  <style scoped>
  /* Estilos opcionales */
  </style>
  