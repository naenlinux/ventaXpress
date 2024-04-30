<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Categorias</h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item active">Categorias</li>
          </ol>
        </div><!-- /.col -->
      </div><!-- /.row -->
    </div><!-- /.container-fluid -->
  </div>
  <!-- /.content-header -->

  <div class="card card-secondary card-outline">
      <div class="card-body">
          <div class="row">
              <div class="col-sm-6">
                  <h2><button class="btn btn-primary btn-sm toastrDefaultSuccess" @click="abrirModal('registrar')">Nuevo</button></h2>
              </div>
              <div class="col-sm-6">
                  <div class="input-group">
                      <input type="search" v-model="txtBuscar" @keyup="listarCategorias(1,txtBuscar)" class="form-control form-control-md" placeholder="Buscar categoria">
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
                  <thead class="bg-secondary">
                      <tr>
                          <th>Nombre</th>
                          <th>Descripcion</th>
                          <th width="7%">Opciones</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="c in categorias" :key="c.id">
                          <td v-text="c.nombre"></td>
                          <td v-text="c.descripcion"></td>
                          <td>
                              <button class="btn btn-sm btn-warning" @click="abrirModal('actualizar', c)"><i class="fas fa-edit"></i></button>&nbsp;
                              <button class="btn btn-sm btn-danger" @click="eliminarCategoria(c.id,c.nombre)"><i class="fas fa-trash-alt"></i></button>
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

  <!--- MODAL PEDIDO --->
     <div v-if="showModal">
      <div class="modal">
          <div class="modal-overlay"></div>
              <div class="modal-content" v-on:keyup.enter = "tipoAccion==1?registrarCategoria():actualizarCategoria()">
                  <div class="modal-header bg-primary text-white">
                      <h4>{{tituloModal}}</h4>
                      <button type="button" class="close" @click="cerrarModal()">&times;</button>
                  </div>
                  <div class="modal-body">
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Nombre: *</label>
                          <div class="col-sm-9">
                              <input type="text" class="form-control" v-model="nombre" placeholder="Nombre de la categoria">
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Descripción:</label>
                          <div class="col-sm-9">
                              <input type="text" class="form-control" v-model="descripcion" placeholder="Descripción de la categoria">
                          </div>
                      </div>
                  </div>
                  <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" @click="cerrarModal()">Cerrar</button>
                      <button type="button" v-if="tipoAccion==1" class="btn btn-primary" @click="registrarCategoria()">GUARDAR</button>
                      <button type="button" v-if="tipoAccion==2" class="btn btn-primary" @click="actualizarCategoria()">ACTUALIZAR</button>
                  </div>
              </div>
          </div>
          
      </div>
  <!--- FIN MODAL PEDIDO --->
</template>

<script>
    export default{   
      data(){
          return{
              id:'',
              nombre:'',
              descripcion:'',

              showModal: false,
              tituloModal: '',
              categorias: [],
              errorCategoria:0,
              arrayMostMsj:[],
              tipoAccion: 0,
              txtBuscar:'',
              errorSaveUpdate:[],

              currentPage: 1,
              totalPages: 0,
              listporPage: 10,
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
              this.listarCategorias(pageNumber,'');
          },
          goToPreviousPage() {
              if (this.currentPage > 1) {
                  this.currentPage -= 1;
                  this.listarCategorias(this.currentPage,'');
              }
          },
          goToNextPage() {
              if (this.currentPage < this.totalPages) {
                  this.currentPage += 1;
                  this.listarCategorias(this.currentPage,'');
              }
          },
          goToFirstPage() {
              if (this.currentPage !== 1) {
                  this.currentPage = 1;
                  this.listarCategorias(this.currentPage,'');
              }
          },

          goToLastPage() {
              if (this.currentPage !== this.totalPages) {
                  this.currentPage = this.totalPages;
                  this.listarCategorias(this.currentPage,'');
              }
          },
          listarCategorias(pageNumber = 1,txtBuscar){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/api/categorias/?page=${pageNumber}&search=${txtBuscar}`)
              .then(function(response){
                  me.categorias = response.data.results
                  me.currentPage = pageNumber
                  me.totalPages = Math.ceil(response.data.count / me.listporPage)
                  me.totalRegistros = response.data.count
              })
          },
          validarCategoria(){
              this.errorCategoria = 0
              this.arrayMostMsj = []
              if(!this.nombre.trim()) this.arrayMostMsj.push("Ingrese el nombre de la Categoria")
              if(this.arrayMostMsj.length) this.errorCategoria = 1
              return this.errorCategoria
          },
          registrarCategoria(){
              if(this.validarCategoria()){
                  this.arrayMostMsj.forEach(element => {
                      this.$toastr.error(element,'Atencion!')
                  });
                  return
              }
              let me = this
              this.$axios.post(`${process.env.VUE_APP_API_URL}/api/categorias/`, {
                  nombre: (me.nombre.toUpperCase()).trim(),
                  descripcion: (me.descripcion.toUpperCase()).trim(),
              })
              .then(function (response) {
                  me.listarCategorias(1,'')
                  me.cerrarModal()
                  console.log(response)
                  me.$toastr.success('Nueva categoria', 'Registrado');
              })
              .catch(function (error) {
                if(error.response && error.response.data){
                    if(error.response.data.nombre){me.errorSaveUpdate.push(error.response.data.nombre[0])}
                }
                if(me.errorSaveUpdate.length > 0){
                    me.errorSaveUpdate.forEach(element => {
                        me.$toastr.error(element,'Error')
                    });
                }
                me.errorSaveUpdate = []          
               })
          },
          actualizarCategoria(){
              if(this.validarCategoria()){
                  this.arrayMostMsj.forEach(element => {
                      this.$toastr.error(element,'Atencion!')
                  });
                  return
              }
              let me = this
              this.$axios.put(`${process.env.VUE_APP_API_URL}/api/categorias/`+me.id+`/`,{
                  nombre: (me.nombre.toUpperCase()).trim(),
                  descripcion: (me.descripcion.toUpperCase()).trim(),
              })
              .then(function(response){
                  console.log(response)
                  me.listarCategorias(me.currentPage,me.txtBuscar)
                  me.cerrarModal()
                  me.$toastr.success('Categoria actualizado', 'Actualizado');
              })
              .catch(function (error) {
                if(error.response && error.response.data){
                    if(error.response.data.nombre){me.errorSaveUpdate.push(error.response.data.nombre[0])}
                }
                if(me.errorSaveUpdate.length > 0){
                    me.errorSaveUpdate.forEach(element => {
                        me.$toastr.error(element,'Error')
                    });
                }
                me.errorSaveUpdate = []          
               })
          },
          eliminarCategoria(id,nombre){
              let me = this
              this.$swal.fire({
              title: nombre,
              text: 'Presione si para eliminar',
              icon: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Si, eliminar'
              }).then((result) => {
              if (result.isConfirmed) {
                  this.$axios.put(`${process.env.VUE_APP_API_URL}/api/categorias/`+id+`/`,{
                      activo : 0,
                  })
                  .then(function(response){
                      console.log(response)
                      me.listarCategorias(me.currentPage,me.txtBuscar)
                      me.cerrarModal()
                      me.$toastr.success('Categoria eliminado', 'Eliminado');
                  })
              }
              })
          },
          abrirModal(action, data=[]){
              switch(action){
                  case "registrar":{
                      this.showModal = true
                      this.tituloModal = "Nueva categoria"
                      this.tipoAccion = 1
                      break
                  }
                  case "actualizar":{
                      this.showModal = true
                      this.tituloModal = "Editar categoria"
                      this.id = data['id']
                      this.nombre = data['nombre']
                      this.descripcion = data['descripcion']
                      this.tipoAccion = 2
                      break
                  }
              }                
          },
          cerrarModal(){
              this.showModal = false;
              this.id = ''
              this.nombre = ''
              this.descripcion = ''
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
          this.listarCategorias(1,'')
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