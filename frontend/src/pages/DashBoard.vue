<template>
        <div id="app">
                <div class="row">
                        <div class="col-md-4 mt-3">
                                <div class="card">
                                        <div class="card-content">
                                          <div class="card-body">
                                            <div class="media d-flex">
                                              <div class="media-body text-left">
                                                <h3 class="text-success">{{countProducto}}</h3>
                                                <span>Productos</span>
                                              </div>
                                              <div class="align-self-center">
                                                <i class="fas fa-dolly text-success" style="font-size: 30pt;"></i>
                                              </div>
                                            </div>
                                          </div>
                                        </div>
                                </div>
                        </div>
                        <div class="col-md-4 mt-3">
                                <div class="card">
                                        <div class="card-content">
                                          <div class="card-body">
                                            <div class="media d-flex">
                                              <div class="media-body text-left">
                                                <h3 class="text-gray">{{countCategoria}}</h3>
                                                <span>Categorias</span>
                                              </div>
                                              <div class="align-self-center">
                                                <i class="fas fa-truck-loading text-gray" style="font-size: 30pt;"></i>
                                              </div>
                                            </div>
                                          </div>
                                        </div>
                                </div>
                        </div>
                        <div class="col-md-4 mt-3">
                                <div class="card">
                                        <div class="card-content">
                                          <div class="card-body">
                                            <div class="media d-flex">
                                              <div class="media-body text-left">
                                                <h3 class="text-info">{{countProveedor}}</h3>
                                                <span>Proveedores</span>
                                              </div>
                                              <div class="align-self-center">
                                                <i class="fas fa-truck text-info" style="font-size: 30pt;"></i>
                                              </div>
                                            </div>
                                          </div>
                                        </div>
                                </div>
                        </div>        
                </div>                
                <div class="row">
                  <div class="col-md-4 mt-3">
                    <div class="card">
                            <div class="card-content">
                              <div class="card-body">
                                <div class="media d-flex">
                                  <div class="media-body text-left">
                                    <h3 class="text-danger">S/ {{formatNumber(sumCompras)}}</h3>
                                    <span>Compras</span>
                                  </div>
                                  <div class="align-self-center">
                                    <i class="fas fa-box text-danger" style="font-size: 30pt;"></i>
                                  </div>
                                </div>
                              </div>
                            </div>
                    </div>
            </div>
                  <div class="col-md-4 mt-3">
                          <div class="card">
                                  <div class="card-content">
                                    <div class="card-body">
                                      <div class="media d-flex">
                                        <div class="media-body text-left">
                                          <h3 class="text-primary">S/ {{formatNumber(sumVentas)}}</h3>
                                          <span>Ventas</span>
                                        </div>
                                        <div class="align-self-center">
                                          <i class="fas fa-hand-holding-usd text-primary" style="font-size: 30pt;"></i>
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                          </div>
                  </div>
                  
                  <div class="col-md-4 mt-3">
                          <div class="card">
                                  <div class="card-content">
                                    <div class="card-body">
                                      <div class="media d-flex">
                                        <div class="media-body text-left">
                                          <h3 class="text-warning">{{countSucursales}}</h3>
                                          <span>Sucursales</span>
                                        </div>
                                        <div class="align-self-center">
                                          <i class="fas fa-warehouse text-warning" style="font-size: 30pt;"></i>
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                          </div>
                  </div>
                  <div class="col-md-6">
                    <div>
                      <Bar :data="data" :options="options" />
                    </div>
                  </div>                
          </div>  
              </div>
</template>
      
<script>
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default {
  name: 'App',
  components:{
    Bar
  },

  data() {
    return {
      countProveedor:0,
      countProducto:0,
      countCategoria:0,
      sumCompras:0,
      sumVentas:0,
      countSucursales:0,
      arrayVenxMes:[],
      array_meses:['enero'],
      array_venta:[],
  
      data: {
        labels:[],
        datasets: [{
        }],
        
      },
      options: {
        responsive: true
      }

    }
  },
methods:{
      listarProveedor(){
        let me = this
        this.$axios.get(`${process.env.VUE_APP_API_URL}/impresiones/countProveedores/`)
        .then(function(response){
            me.countProveedor = response.data.countProveedores
        })
      },
      listarProducto(){
        let me = this
        this.$axios.get(`${process.env.VUE_APP_API_URL}/impresiones/countProductos/`)
        .then(function(response){
            me.countProducto = response.data.countProductos
        })
      },
      listarCategoria(){
        let me = this
        this.$axios.get(`${process.env.VUE_APP_API_URL}/impresiones/countCategorias/`)
        .then(function(response){
            me.countCategoria = response.data.countCategorias
        })
      },
      sumaVentas(){
        let me = this
        this.$axios.get(`${process.env.VUE_APP_API_URL}/impresiones/sumaVentas/`)
        .then(function(response){
            me.sumVentas = response.data.sumaVentas
        })
      },
      sumaCompras(){
        let me = this
        this.$axios.get(`${process.env.VUE_APP_API_URL}/impresiones/sumaCompras/`)
        .then(function(response){
            me.sumCompras = response.data.sumaCompras
        })
      },
      countSucursal(){
        let me = this
        this.$axios.get(`${process.env.VUE_APP_API_URL}/impresiones/countSucursal/`)
        .then(function(response){
            me.countSucursales = response.data.countSucursal
        })
      },
      ventasxMes(){
        let me = this
        this.$axios.get(`${process.env.VUE_APP_API_URL}/impresiones/ventasxMes/`)
        .then(function(response){
          let meses=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre']
          let labels = []
          let valores = []
            response.data.forEach(item =>{
              labels.push(meses[item.mes-1])
              valores.push(item.venta_total)
            })
            let currentDate = new Date();
            let currentYear = currentDate.getFullYear();
              me.data = {
                labels: labels,
                datasets: [{
                data: valores,
                label: 'Ventas del año '+currentYear,
                backgroundColor: '#96CCE8' ,
              }],
              
              }
              console.log(labels)          
        })
      },
      formatNumber(value) {
      // Formatear el valor numérico con miles y dos decimales
      return value.toLocaleString('en', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });
    },
        
  
    },
  mounted(){
    this.listarProveedor()
    this.listarProducto()
    this.listarCategoria()
    this.sumaCompras()
    this.sumaVentas()
    this.countSucursal()
    this.ventasxMes()
    
  }
};
</script>

<style>
/* Estilos opcionales */
</style>
