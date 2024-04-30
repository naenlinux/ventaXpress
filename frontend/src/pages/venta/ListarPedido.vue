<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Ventas</h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item active">Ventas</li>
          </ol>
        </div><!-- /.col -->
      </div><!-- /.row -->
    </div><!-- /.container-fluid -->
  </div>
  <!-- /.content-header -->

  <div class="card card-primary card-outline">
      <div class="card-body">
          <div class="row">
              <div class="col-sm-6">
                <h2>
                    <router-link to="/pedidos/nuevo">
                        <button class="btn btn-primary btn-sm toastrDefaultSuccess">Nueva Venta</button>
                    </router-link>
                </h2>
              </div>
              <div class="col-sm-6">
                  <div class="input-group" @keyup.enter="listarPedidos(1,fechaBuscar,numBuscar)">
                    <div class="input-group-append">
                          <button type="submit" class="btn btn-md btn-default">
                              Fecha
                          </button>
                    </div>
                    <input type="date" v-model="fechaBuscar" class="form-control form-control-md" >
                    <div class="input-group-append">
                          <button type="submit" class="btn btn-md btn-default">
                            Número
                          </button>
                    </div>
                    <input type="number" v-model="numBuscar" class="form-control form-control-md" placeholder="0">
                    <div class="input-group-append">
                          <button type="submit" class="btn btn-md btn-info" @click="listarPedidos(1,fechaBuscar,numBuscar)">
                              <i class="fa fa-search"></i> Buscar
                          </button>
                    </div>
                  </div>
              </div> 
          </div>
          <div class="table-responsive">
              <table class="table table-bordered table-sm table-striped">
                  <thead class="bg-primary">
                      <tr>
                          <th>#</th>
                          <th class="text-center">Ver</th>
                          <th>Comprobante</th>
                          <th>Cliente</th>
                          <th>Vendedor</th>
                          <th>Sucursal</th>
                          <th>Fecha</th>
                          <th>Hora</th>
                          <th class="text-center">Pedido N°</th>
                          <th class="text-right">Importe S/</th>
                          <th class="text-center">Estado</th>
                          
                      </tr>
                  </thead>
                  <tbody>
                     <tr v-for="(pe, index) in arrayPedidos" :key="pe.id">
                        <td>{{index+1}}</td>
                        <td class="text-center">
                            <button class="btn btn-sm btn-primary" @click="verDetalle(pe.id)"><i class="fas fa-eye"></i></button>
                        </td>
                        <td>{{ pe.comprobante }}</td>
                        <td>{{ pe.cliente }}</td>
                        <td>{{ pe.usuario }}</td>
                        <td>{{ pe.sucursal }}</td>
                        <td>{{ fechaFormateada(pe.fecha) }}</td>
                        <td>{{ horaFormateada(pe.hora) }}</td>
                        <td class="text-center">{{ pe.numero }}</td>
                        <td class="text-right">{{ formattedTotal(Number(pe.igv_total) + Number(pe.subtotal)) }}</td>
                        <td class="text-center" :class="pe.activo==0 ? 'bg-danger' : (pe.estado=='Pagado' ? 'bg-success' : 'bg-warning')" >{{ pe.estado }}</td>
                     </tr>
                  </tbody>
              </table>
          </div>
           <!-- Agrega el paginador aquí -->
          <div class="row">
              <div class="col-sm-6">
                  <span>Registros: {{ totalRegistros }}</span>
              </div>
              <div class="col-sm-6">
                  <ul class="pagination pagination-sm justify-content-end">
                      <li class="page-item"  :class="{disabled: isOnFirstPage}">
                          <a class="page-link" @click="goToFirstPage" :disabled="isOnFirstPage">Primero</a>
                      </li>
                      <li class="page-item"  :class="{disabled: isOnFirstPage}">
                          <a class="page-link" @click="goToPreviousPage" >Anterior</a>
                      </li>
                      <li class="page-item" :class="{ active: currentPage === page }" v-for="page in visiblePages" :key="page">
                          <a class="page-link" @click="goToPage(page)">{{ page }}</a>
                      </li>
                      <li class="page-item" :class="{disabled: isOnLastPage}">
                          <a class="page-link" @click="goToNextPage" >Siguiente</a>
                      </li>
                      <li class="page-item" :class="{disabled: isOnLastPage}">
                          <a class="page-link" @click="goToLastPage" :disabled="isOnLastPage">Último</a>
                      </li>
                  </ul>
              </div>
          </div>
      </div>      

  </div><!-- /.card -->

</template>

<script>
    export default{
        props:{
            nombreUsuario:String,
            idUsuario:Number,
        },
      data(){
          return{
            id:'',
            arrayPedidos: [],
                        
            numBuscar:'',
            fechaBuscar:'',
            
            currentPage: 1,
            totalPages: 0,
            listporPage: 15,
            visiblePages: [], // Páginas visibles en el paginado
            totalPagesToShow: 5, // Cantidad de páginas visibles en el paginado
            totalRegistros:0,

          }
      },
      computed: {
          isOnFirstPage() {
          return this.currentPage === 1;
          },
          isOnLastPage() {
          return this.currentPage === this.totalPages;
          },
        
      },
      methods:{
          updateVisiblePages() {
              const halfTotalPagesToShow = Math.floor(this.totalPagesToShow / 2);

              let startPage = Math.max(this.currentPage - halfTotalPagesToShow, 1);
              let endPage = Math.min(this.currentPage + halfTotalPagesToShow, this.totalPages);

              if (this.totalPages > this.totalPagesToShow) {
                  // Si el número de páginas es mayor que el total de páginas a mostrar, ajustamos los extremos
                  if (endPage === this.totalPages) {
                  startPage = Math.max(endPage - this.totalPagesToShow + 1, 1);
                  } else if (startPage === 1) {
                  endPage = Math.min(startPage + this.totalPagesToShow - 1, this.totalPages);
                  }
              }

              this.visiblePages = Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i);
          },
          goToPage(pageNumber) {
              // Cambiar la página actual al número de página seleccionado
              this.currentPage = pageNumber;
              // Llamar al método para obtener los datos de la página seleccionada
              this.listarPedidos(pageNumber,'','');
          },
          goToPreviousPage() {
              if (this.currentPage > 1) {
                  this.currentPage -= 1;
                  this.listarPedidos(this.currentPage,'','');
              }
          },
          goToNextPage() {
              if (this.currentPage < this.totalPages) {
                  this.currentPage += 1;
                  this.listarPedidos(this.currentPage,'','');
              }
          },
          goToFirstPage() {
              if (this.currentPage !== 1) {
                  this.currentPage = 1;
                  this.listarPedidos(this.currentPage,'','');
              }
          },

          goToLastPage() {
              if (this.currentPage !== this.totalPages) {
                  this.currentPage = this.totalPages;
                  this.listarPedidos(this.currentPage,'','');
              }
          },
          formattedTotal(amount) {
            return new Intl.NumberFormat('es-PE', {
            style: 'currency',
            currency: 'PEN',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
            }).format(amount);
          },
          listarPedidos(pageNumber = 1,fechaBuscar, numBuscar){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apiventa/pedidos/?page=${pageNumber}&numero=${numBuscar}&fecha=${fechaBuscar}`)
              .then(function(response){
                  me.arrayPedidos = response.data.results
                  me.currentPage = pageNumber
                  me.totalPages = Math.ceil(response.data.count / me.listporPage)
                  me.totalRegistros = response.data.count
              })
          },
          
          verDetalle(id){
            this.$router.push({path: `/pedidos/detalle/${id}`})
          },
    
        fechaFormateada(fecha) {
        // Separar la fecha en partes (año, mes, día)
        const partes = fecha.split('-');

        // Crear una nueva cadena en el formato deseado
        return `${partes[2]}/${partes[1]}/${partes[0]}`;
        },
        horaFormateada(hora) {
        // Dividir la hora en partes usando ":" como separador
        const partes = hora.split(':');

        // Tomar las dos primeras partes (horas y minutos)
        const horas = partes[0];
        const minutos = partes[1];

        // Crear una cadena en el formato 'hh:mm'
        return `${horas}:${minutos}`;
        },
        
      },
          
      watch: {
          currentPage() {
          // Actualizar las páginas visibles cuando se cambia la página actual
          this.updateVisiblePages();
          },
          totalPages() {
          // Actualizar las páginas visibles cuando se actualiza el número total de páginas
          this.updateVisiblePages();
          },
      },
      mounted(){
          this.listarPedidos(1,'','')
          this.updateVisiblePages();
          this.$socket.onmessage = (event)=>{
            console.log(event.data)
            this.listarPedidos(1,'','')
            this.$toastr.success('Hay un nuevo pedido','NUEVO PEDIDO')
          }
      }
  }
</script>

<style scoped>.modal{
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  overflow: auto;
}
.modal-overlay{
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}
.modal-content{
  width: 40%;
  background-color: white;
  margin-top: 100px;
}
</style>