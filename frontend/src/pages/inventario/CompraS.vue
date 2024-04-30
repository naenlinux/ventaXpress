<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Compras</h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item active">Compras</li>
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
                    <router-link to="/compras/nuevacompra">
                        <button class="btn btn-primary btn-sm toastrDefaultSuccess">Nuevo</button>
                    </router-link>
                </h2>
              </div>
              <div class="col-sm-6">
                  <div class="input-group">
                      <input type="search" v-model="txtBuscar" @keyup="listarCompras(1,txtBuscar)" class="form-control form-control-md" placeholder="Buscar proveedor">
                      <div class="input-group-append">
                          <button type="submit" class="btn btn-md btn-default">
                              <i class="fa fa-search"></i>
                          </button>
                      </div>
                  </div>
              </div> 
          </div>
          <div class="table-responsive">
              <table class="table table-bordered table-sm table-striped">
                  <thead class="bg-primary">
                      <tr>
                          <th>Proveedor</th>
                          <th>Fecha compra</th>
                          <th>Comprobante</th>
                          <th>Numero</th>
                          <th class="text-right">Compra S/</th>
                          <th>Opciones</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="c in arrayCompras" :key="c.id">
                          <td v-text="c.empresa">
                          </td>
                          <td v-text="c.fecha"></td>
                          <td>
                            <div v-for="ti in arrayTipo" :key="ti.id">
                                <div v-if="ti.id == c.idTipoComprob">{{ ti.nombre }}</div>
                            </div>
                          </td>
                          <td v-text="c.numeroComprob"></td>
                          <td v-text="formattedTotal(c.compraTotal)" class="text-right"></td>
                          <td>
                                <span v-if="c.activo" class="badge badge-success">Habilitad</span>
                                <span v-else class="badge badge-danger">Anulado</span>
                                &nbsp;
                                <button class="btn btn-sm btn-primary" @click="verDetalle(c.id)"><i class="fas fa-eye"></i></button>
                          </td>
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
            idProveedor:'',
            fecha:'',
            idTipoComprob:'',
            numeroComprob:'',

            showModal: false,
            tituloModal: '',
            arrayCompras: [],
            errorCompras:0,
            arrayMostMsj:[],
            tipoAccion: 0,
            txtBuscar:'',
            errorSaveUpdate:[],

            currentPage: 1,
            totalPages: 0,
            listporPage: 15,
            visiblePages: [], // Páginas visibles en el paginado
            totalPagesToShow: 5, // Cantidad de páginas visibles en el paginado
            totalRegistros:0,

            arrayTipo:[],
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
              this.listarCompras(pageNumber,'');
          },
          goToPreviousPage() {
              if (this.currentPage > 1) {
                  this.currentPage -= 1;
                  this.listarCompras(this.currentPage,'');
              }
          },
          goToNextPage() {
              if (this.currentPage < this.totalPages) {
                  this.currentPage += 1;
                  this.listarCompras(this.currentPage,'');
              }
          },
          goToFirstPage() {
              if (this.currentPage !== 1) {
                  this.currentPage = 1;
                  this.listarCompras(this.currentPage,'');
              }
          },

          goToLastPage() {
              if (this.currentPage !== this.totalPages) {
                  this.currentPage = this.totalPages;
                  this.listarCompras(this.currentPage,'');
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
          listarCompras(pageNumber = 1,txtBuscar){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apinventario/compras/?page=${pageNumber}&search=${txtBuscar}`)
              .then(function(response){
                  me.arrayCompras = response.data.results
                  me.currentPage = pageNumber
                  me.totalPages = Math.ceil(response.data.count / me.listporPage)
                  me.totalRegistros = response.data.count
              })
              
              //=== listar tipocomprobante ===//
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/tipocomprobante/`)
              .then(function(response){
                if(response.data.length){
                    me.arrayTipo = response.data
                }
              })
          },

          verDetalle(id){
            this.$router.push({path: `/compras/detalle/${id}`})
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
          this.listarCompras(1,'')
          this.updateVisiblePages();
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