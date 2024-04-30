<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Unidad de medida U/M</h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item active">UnidadMedida</li>
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
                      <input type="search" v-model="txtBuscar" @keyup="listarUnidadMedidas(1,txtBuscar)" class="form-control form-control-md" placeholder="Buscar por nombre">
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
                          <th>Abreviado</th>
                          <th>Proporción</th>
                          <th>U/M Stock</th>
                          <th>Estado</th>
                          <th width="7%">Opciones</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="u in unidadMedidas" :key="u.id">
                          <td v-text="u.nombre"></td>
                          <td v-text="u.nombrecorto"></td>
                          <td v-text="u.proporcion"></td>
                          <td v-text="u.unidadStock"></td>
                          <td>
                            <span v-if="u.activo" class="badge badge-success">Habilitad</span>
                            <span v-else class="badge badge-danger">Anulado</span>
                          </td>
                          <td>
                              <button class="btn btn-sm btn-warning" @click="abrirModal('actualizar', u)"><i class="fas fa-edit"></i></button>&nbsp;
                              <button v-if="u.activo" class="btn btn-sm btn-danger" @click="eliminarUnidadModelo(u.id,u.nombre,u.activo)"><i class="fas fa-trash-alt"></i></button>
                              <button v-else class="btn btn-sm btn-success" @click="eliminarUnidadModelo(u.id,u.nombre,u.activo)"><i class="fas fa-trash-restore-alt"></i></button>
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
              <div class="modal-content" v-on:keyup.enter = "tipoAccion==1?registrarUnidadMedida():actualizarUnidadMedida()">
                  <div class="modal-header bg-primary text-white">
                      <h4>{{tituloModal}}</h4>
                      <button type="button" class="close" @click="cerrarModal()">&times;</button>
                  </div>
                  <div class="modal-body">
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Nombre: *</label>
                          <div class="col-sm-9">
                              <input type="text" class="form-control" v-model="nombre" placeholder="Nombre de la unidad">
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Nombre Abrev: *</label>
                          <div class="col-sm-9">
                              <input type="text" class="form-control" v-model="nombrecorto" placeholder="Nombre abreviado">
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Proporción: *</label>
                          <div class="col-sm-9">
                              <input type="number" class="form-control" v-model="proporcion" placeholder="1">
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">U/M en Stock:</label>
                          <div class="col-sm-9">
                            <select v-model="unidadStock" class="form-control">
                                <option value="Unidades">Unidades</option>
                                <option value="Kilos">Kilos</option>
                                <option value="Metros">Metros</option>
                            </select>
                          </div>
                      </div>
                      
                  </div>
                  <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" @click="cerrarModal()">Cerrar</button>
                      <button type="button" v-if="tipoAccion==1" class="btn btn-primary" @click="registrarUnidadMedida()">GUARDAR</button>
                      <button type="button" v-if="tipoAccion==2" class="btn btn-primary" @click="actualizarUnidadMedida()">ACTUALIZAR</button>
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
              nombrecorto:'',
              proporcion:'',
              unidadStock:'Unidades',
              activo:'',
              
              showModal: false,
              tituloModal: '',
              unidadMedidas: [],
              errorUnidadMedida:0,
              arrayMostMsj:[],
              tipoAccion: 0,
              txtBuscar:'',

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
              this.listarUnidadMedidas(pageNumber,'');
          },
          goToPreviousPage() {
              if (this.currentPage > 1) {
                  this.currentPage -= 1;
                  this.listarUnidadMedidas(this.currentPage,'');
              }
          },
          goToNextPage() {
              if (this.currentPage < this.totalPages) {
                  this.currentPage += 1;
                  this.listarUnidadMedidas(this.currentPage,'');
              }
          },
          goToFirstPage() {
              if (this.currentPage !== 1) {
                  this.currentPage = 1;
                  this.listarUnidadMedidas(this.currentPage,'');
              }
          },

          goToLastPage() {
              if (this.currentPage !== this.totalPages) {
                  this.currentPage = this.totalPages;
                  this.listarUnidadMedidas(this.currentPage,'');
              }
          },
          listarUnidadMedidas(pageNumber = 1,txtBuscar){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/api/unidadmedida/?page=${pageNumber}&search=${txtBuscar}`)
              .then(function(response){
                  me.unidadMedidas = response.data.results
                  me.currentPage = pageNumber
                  me.totalPages = Math.ceil(response.data.count / me.listporPage)
                  me.totalRegistros = response.data.count
              })
          },
          validarUnidadMedida(){
              this.errorUnidadMedida = 0
              this.arrayMostMsj = []
              if(!this.proporcion || this.proporcion < 1) this.arrayMostMsj.push("Ingrese el numero de proporción mayor a 0")
              if(!this.nombrecorto.trim()) this.arrayMostMsj.push("Ingrese una abreviatura")
              if(!this.nombre.trim()) this.arrayMostMsj.push("Ingrese el nombre de la unidad")
              if(this.arrayMostMsj.length) this.errorUnidadMedida = 1
              return this.errorUnidadMedida
          },
          registrarUnidadMedida(){
              if(this.validarUnidadMedida()){
                  this.arrayMostMsj.forEach(element => {
                      this.$toastr.error(element,'Atencion!')
                  });
                  return
              }
              let me = this
              this.$axios.post(`${process.env.VUE_APP_API_URL}/api/unidadmedida/`, {
                  nombre: (me.nombre.toUpperCase()).trim(),
                  nombrecorto: (me.nombrecorto.toUpperCase()).trim(),
                  //proporcion: me.proporcion,
                  proporcion: me.proporcion, //...(me.proporcion ? { proporcion: me.proporcion } : {} ),
                  unidadStock: me.unidadStock,

              })
              .then(function (response) {
                  me.listarUnidadMedidas(1,'')
                  me.cerrarModal()
                  console.log(response)
                  me.$toastr.success('Nueva unidad registrado', 'Registrado');
              })
          },
          actualizarUnidadMedida(){
              if(this.validarUnidadMedida()){
                  this.arrayMostMsj.forEach(element => {
                      this.$toastr.error(element,'Atencion!')
                  });
                  return
              }
              let me = this
              this.$axios.put(`${process.env.VUE_APP_API_URL}/api/unidadmedida/`+me.id+`/`,{
                  nombre: (me.nombre.toUpperCase()).trim(),
                  nombrecorto: (me.nombrecorto.toUpperCase()).trim(),
                  ...(me.proporcion ? { proporcion: me.proporcion } : {proporcion: null}),
                  unidadStock: me.unidadStock,
              })
              .then(function(response){
                  console.log(response)
                  me.listarUnidadMedidas(me.currentPage,me.txtBuscar)
                  me.cerrarModal()
                  me.$toastr.success('Unidad actualizado', 'Actualizado');
              })
          },
          eliminarUnidadModelo(id,nombre,activo){
              let me = this
              this.$swal.fire({
              title: nombre,
              text:  activo ? 'Presione si para eliminar' : 'Presione si para restaurar',
              icon: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: activo ? 'Eliminar' : 'Restaurar',
              }).then((result) => {
              if (result.isConfirmed) {
                  this.$axios.put(`${process.env.VUE_APP_API_URL}/api/unidadmedida/`+id+`/`,{
                      activo : activo ?  0 : 1,
                  })
                  .then(function(response){
                      console.log(response)
                      me.listarUnidadMedidas(me.currentPage,me.txtBuscar)
                      me.cerrarModal()
                      if(activo){me.$toastr.success('Unidad deshabilitado', 'Desactivado')}
                      else{me.$toastr.success('Unidad Habilitado', 'Habilitado')}
                  })
              }
              })
          },
          abrirModal(action, data=[]){
              switch(action){
                  case "registrar":{
                      this.showModal = true
                      this.tituloModal = "Nueva unidad de medida"
                      this.tipoAccion = 1
                      break
                  }
                  case "actualizar":{
                      this.showModal = true
                      this.tituloModal = "Editar unidad de medida"
                      this.id = data['id']
                      this.nombre = data['nombre']
                      this.nombrecorto = data['nombrecorto']
                      this.proporcion = data['proporcion']
                      this.unidadStock = data['unidadStock']
                      this.tipoAccion = 2
                      break
                  }
              }                
          },
          cerrarModal(){
              this.showModal = false;
              this.id = ''
              this.nombre = ''
              this.nombrecorto = ''
              this.proporcion = ''
              this.activo = ''
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
          this.listarUnidadMedidas(1,'')
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