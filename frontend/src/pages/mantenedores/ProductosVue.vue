<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Productos</h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item active">Productos</li>
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
                      <input type="search" v-model="txtBuscar" @keyup="listarProductos(1,txtBuscar)" class="form-control form-control-md" placeholder="Buscar por nombre o código">
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
                          <th>U/M</th>
                          <th>Categoria</th>
                          <th>Descripción</th>                          
                          <th>Modelo</th>
                          <th>Código</th>
                          <th>Opciones</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="p in productos" :key="p.id">
                          <td v-text="p.nombre"></td>
                          <td v-text="p.nombre_unimedida" ></td>
                          <td v-text="p.nombre_categoria"></td>
                          <td v-text="p.descripcion"></td>
                          <td v-text="p.modelo"></td>
                          <td v-text="p.codigo"></td>
                          <td>
                            <span v-if="p.activo" class="badge badge-success">Habilitad</span>
                            <span v-else class="badge badge-danger">Anulado</span>&nbsp;
                              <button class="btn btn-sm btn-warning" @click="abrirModal('actualizar', p)"><i class="fas fa-edit"></i></button>&nbsp;
                              <button v-if="p.activo" class="btn btn-sm btn-danger" @click="eliminarProducto(p.id,p.nombre,p.activo)"><i class="fas fa-trash-alt"></i></button>
                              <button v-else class="btn btn-sm btn-success" @click="eliminarProducto(p.id,p.nombre,p.activo)"><i class="fas fa-trash-restore-alt"></i></button>
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
              <div class="modal-content" v-on:keyup.enter = "tipoAccion==1?registrarProducto():actualizarProducto()">
                  <div class="modal-header bg-primary text-white">
                      <h4>{{tituloModal}}</h4>
                      <button type="button" class="close" @click="cerrarModal()">&times;</button>
                  </div>
                  <div class="modal-body">
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Nombre: *</label>
                          <div class="col-sm-9">
                              <input type="text" class="form-control" v-model="nombre" placeholder="Nombre del producto">
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Unidad Medida Compra: *</label>
                          <div class="col-sm-9">
                            <select v-model="unidadMedida"  class="form-control">
                                <option :value="null">==seleccione==</option>
                                <option :value="uni.id" v-for="uni in arrayUniMe" :key="uni.id" v-text="uni.nombre"></option>
                            </select>
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Categoria: *</label>
                          <div class="col-sm-9">
                            <select v-model="categoria"  class="form-control">
                                <option :value="null">==seleccione==</option>
                                <option :value="ca.id" v-for="ca in categorias" :key="ca.id" v-text="ca.nombre"></option>
                            </select>
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Descripcion:</label>
                          <div class="col-sm-9">
                              <input type="text" class="form-control" v-model="descripcion" placeholder="Descripcion del producto">
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Modelo:</label>
                          <div class="col-sm-9">
                              <input type="text" class="form-control" v-model="modelo" placeholder="Modelo de producto">
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Código:</label>
                          <div class="col-sm-9">
                              <input type="text" class="form-control" v-model="codigo" placeholder="Código del producto">
                          </div>
                      </div>
                  </div>
                  <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" @click="cerrarModal()">Cerrar</button>
                      <button type="button" v-if="tipoAccion==1" class="btn btn-primary" @click="registrarProducto()">GUARDAR</button>
                      <button type="button" v-if="tipoAccion==2" class="btn btn-primary" @click="actualizarProducto()">ACTUALIZAR</button>
                  </div>
              </div>
          </div>
          
      </div>
  <!--- FIN MODAL PEDIDO --->
</template>

<script>
    export default{
        props:{
            nombreUsuario:String,
            idUsuario: Number,
        },
      data(){
          return{
              id:'',
              nombre:'',
              unidadMedida:null,
              descripcion:'',
              modelo:'',
              codigo:'',
              categoria:null,

              showModal: false,
              tituloModal: '',
              productos: [],
              categorias: [],
              errorProducto:0,
              arrayMostMsj:[],
              errorSaveUpdate:[],
              tipoAccion: 0,
              txtBuscar:'',
              arrayUniMe:[],

              currentPage: 1,
              totalPages: 0,
              listporPage: 10,
              visiblePages: [], // Páginas visibles en el paginado
              totalPagesToShow: 5, // Cantidad de páginas visibles en el paginado
              totalRegistros:0,
              localeSocket:null,
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
              this.listarProductos(pageNumber,'');
          },
          goToPreviousPage() {
              if (this.currentPage > 1) {
                  this.currentPage -= 1;
                  this.listarProductos(this.currentPage,'');
              }
          },
          goToNextPage() {
              if (this.currentPage < this.totalPages) {
                  this.currentPage += 1;
                  this.listarProductos(this.currentPage,'');
              }
          },
          goToFirstPage() {
              if (this.currentPage !== 1) {
                  this.currentPage = 1;
                  this.listarProductos(this.currentPage,'');
              }
          },

          goToLastPage() {
              if (this.currentPage !== this.totalPages) {
                  this.currentPage = this.totalPages;
                  this.listarProductos(this.currentPage,'');
              }
          },
          listarProductos(pageNumber = 1,txtBuscar){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/api/productos/?page=${pageNumber}&search=${txtBuscar}`)
              .then(function(response){
                  me.productos = response.data.results
                  me.currentPage = pageNumber
                  me.totalPages = Math.ceil(response.data.count / me.listporPage)
                  me.totalRegistros = response.data.count
              })

          },
          listarUM(){
            let me = this
            this.$axios.get(`${process.env.VUE_APP_API_URL}/api/unidadmedida/`)
              .then(function(response){
                response.data.results.forEach(element => {
                    if(element.activo){
                        me.arrayUniMe.push(element)
                    }
                });
              })
          },
          validarProducto(){
              this.errorProducto = 0
              this.arrayMostMsj = []
              if(!this.categoria) this.arrayMostMsj.push("Seleccione una categoria")
              if(!this.unidadMedida) this.arrayMostMsj.push("Seleccione unidad de medida")
              if(!this.nombre.trim()) this.arrayMostMsj.push("Ingrese el nombre del producto")
              if(this.arrayMostMsj.length) this.errorProducto = 1
              return this.errorProducto
          },
          registrarProducto(){
              if(this.validarProducto()){
                  this.arrayMostMsj.forEach(element => {
                      this.$toastr.error(element,'Atencion!')
                  });
                  return
              }
              let me = this
              this.$axios.post(`${process.env.VUE_APP_API_URL}/api/productos/`, {
                  nombre: (me.nombre.toUpperCase()).trim(),
                  unidadMedida: me.unidadMedida,
                  descripcion: (me.descripcion.toUpperCase()).trim(),
                  modelo: (me.modelo.toUpperCase()).trim(),
                  ...((me.codigo.toUpperCase()).trim() ? { codigo: (me.codigo.toUpperCase()).trim()} : {codigo: null} ),
                  categoria: me.categoria,
              })
              .then(function (response) {
                  me.listarProductos(1,'')
                  me.cerrarModal()
                  console.log(response)
                  me.$toastr.success('Nuevo producto registrado', 'Registrado');
                  me.$socket.send(JSON.stringify({
                    'message': 'nuevo producto'
                  }))
              })
              .catch(function (error) {
                if(error.response && error.response.data){
                    if(error.response.data.nombre){me.errorSaveUpdate.push(error.response.data.nombre[0])}
                    if(error.response.data.codigo){me.errorSaveUpdate.push(error.response.data.codigo[0])}
                }
                if(me.errorSaveUpdate.length > 0){
                    me.errorSaveUpdate.forEach(element => {
                        me.$toastr.error(element,'Error')
                    });
                }
                me.errorSaveUpdate = []          
               })           
          },
          actualizarProducto(){
              if(this.validarProducto()){
                  this.arrayMostMsj.forEach(element => {
                      this.$toastr.error(element,'Atencion!')
                  });
                  return
              }
              let me = this
              this.$axios.put(`${process.env.VUE_APP_API_URL}/api/productos/`+me.id+`/`,{
                  nombre: (me.nombre.toUpperCase()).trim(),
                  unidadMedida: me.unidadMedida,
                  descripcion: (me.descripcion.toUpperCase()).trim(),
                  modelo: (me.modelo.toUpperCase()).trim(),
                  codigo: (me.codigo.toUpperCase()).trim(),
                  categoria: me.categoria,
              })
              .then(function(response){
                  console.log(response)
                  me.listarProductos(me.currentPage,me.txtBuscar)
                  me.cerrarModal()
                  me.$toastr.success('Producto actualizado', 'Actualizado');
              })
              .catch(function (error) {
                if(error.response && error.response.data){
                    if(error.response.data.nombre){me.errorSaveUpdate.push(error.response.data.nombre[0])}
                    if(error.response.data.codigo){me.errorSaveUpdate.push(error.response.data.codigo[0])}
                }
                if(me.errorSaveUpdateunidadMedida.length > 0){
                    me.errorSaveUpdate.forEach(element => {
                        me.$toastr.error(element,'Error')
                    });
                }
                me.errorSaveUpdate = []          
               }) 
          },
          eliminarProducto(id,nombre,activo){
              let me = this
              this.$swal.fire({
              title: nombre,
              text: activo ? 'Presione si para eliminar' : 'Presione si para restaurar',
              icon: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: activo ? 'Eliminar' : 'Restaurar',
              }).then((result) => {
              if (result.isConfirmed) {
                  this.$axios.put(`${process.env.VUE_APP_API_URL}/api/productos/`+id+`/`,{
                    activo : activo ?  0 : 1,
                  })
                  .then(function(response){
                      console.log(response)
                      me.listarProductos(me.currentPage,me.txtBuscar)
                      me.cerrarModal()
                      if(activo){me.$toastr.success('Unidad deshabilitado', 'Desactivado')}
                      else{me.$toastr.success('Unidad Habilitado', 'Habilitado')}
                  })
              }
              })
          },
          abrirModal(action, data=[]){
            //consultamos las categorias
            let me = this
            this.$axios.get(`${process.env.VUE_APP_API_URL}/api/categoriasporname/`)
            .then(function(response){
                me.categorias = response.data
            })
            this.listarUM()
            //console.log('hola data '+JSON.stringify(data['categoria'].id))
            switch(action){
                case "registrar":{
                    this.showModal = true
                    this.tituloModal = "Nuevo producto"
                    this.tipoAccion = 1
                    break
                }
                case "actualizar":{
                    this.showModal = true
                    this.tituloModal = "Editar producto"
                    this.id = data['id']
                    this.nombre = data['nombre']
                    this.unidadMedida = data['unidadMedida']
                    this.descripcion = data['descripcion']
                    this.modelo = data['modelo']
                    data['codigo'] ? this.codigo = data['codigo'].trim() : this.codigo = null
                    this.categoria = data['categoria']
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
              this.modelo = ''
              this.codigo = ''
              this.categoria = null
              this.unidadMedida=null
              this.arrayUniMe=[]
              this.categorias=[]
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
          this.listarProductos(1,'')
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