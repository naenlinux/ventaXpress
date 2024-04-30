<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Almacen</h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item active">Almacen</li>
          </ol>
        </div><!-- /.col -->
      </div><!-- /.row -->
    </div><!-- /.container-fluid -->
  </div>
  <!-- /.content-header -->

  <div class="card card-success card-outline">
      <div class="card-body">
          <div class="row">
            <div class="col-sm-4">
                <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <label class="input-group-text" for="inputGroupSelect01">Listar x categoria:</label>
                </div>
                <select class="custom-select" v-model="categoria" @change="listarAlmacen(1,txtBuscar,ordenar,categoria)">
                    <option :value="0">=== Todos ===</option>
                    <option :value="cat.id" v-for="cat in arrayCategorias" :key="cat.id" v-text="cat.nombre"></option>
                </select>
                </div>
              </div>
              <div class="col-sm-3">
                <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <label class="input-group-text" for="inputGroupSelect01">Ordenar stock:</label>
                </div>
                <select class="custom-select" v-model="ordenar" @change="listarAlmacen(1,txtBuscar,ordenar,categoria)">
                    <option value="-total">De Mayor a menor</option>
                    <option value="total">De Menor a mayor</option>
                </select>
                </div>
              </div>
              <div class="col-sm-4">
                <div class="input-group">
                    <input type="search" v-model="txtBuscar" @keyup="listarAlmacen(1,txtBuscar,ordenar,categoria)" class="form-control form-control-md" placeholder="Buscar producto">
                    <div class="input-group-append">
                        <button type="submit" class="btn btn-md btn-default">
                            <i class="fa fa-search"></i>
                        </button>
                    </div>
                </div>
            </div>
              <div class="col-sm-1 text-right">
                <button class="btn btn-success btn-flat btn-sm" @click="exportarExcel()"><i class="far fa-file-excel"></i> Excel</button>
              </div>
          </div>
          
          <div class="table-responsive">
              <table class="table table-bordered table-sm table-striped">
                  <thead class="bg-success">
                      <tr>
                          <th>Producto</th>
                          <th>Categoria</th>
                          <th>Stock x U/M</th>
                          <th class="text-center">Stock x Unid</th>
                          <th>S/ Compra</th>
                          <th class="text-center">Precios de Venta S/</th>
                          <th>Opciones</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="a in arrayAlmacen" :key="a.id">
                          <td v-text="a.nombre_producto"></td>
                          <td v-text="a.categoria"></td>
                          <td><strong>{{a.cantidad}}</strong> {{a.nombre_unimedida}}</td>
                          <td class="text-center" :class="a.total < 1?'bg-danger':(a.cantidad<2?'bg-warning':'text-success text-bold')">{{ a.total+' '+a.uniMedida }}</td>
                          <td class="text-center" v-text="a.precioCompra"></td>
                          <td>
                                <a href="#" v-for="pre in a.precios_um" :key="pre.id" @click="abrirModalPrecio('updatePrecio',pre,a)">
                                    <h6>{{ pre.nombre_unidad_medida+ ' S/. '+pre.precio }}</h6>
                                </a>                   
                          </td>
                          <td>
                            
                              <button class="btn btn-sm btn-primary tooltip-btn" data-tooltip="Agregar precio de venta" @click="abrirModalPrecio('addPrecio',a,'')"
                              ><i class="fas fa-plus-square"></i></button>&nbsp;
                              
                              <button class="btn btn-sm btn-warning tooltip-btn" data-tooltip="Editar Stock" @click="abrirModal(a)"><i class="fas fa-edit"></i></button>&nbsp;
                              <button class="btn btn-sm tooltip-btn" :data-tooltip="a.activo?'Anular':'Restaurar'"  :class="a.activo?'btn-danger':'btn-success'" @click="eliminarAlmacen(a.id,a.nombre_producto,a.activo)">
                                <i class="fas" :class="a.activo?'fa-trash-alt':'fa-trash-restore-alt'"></i>
                              </button>
                              &nbsp;
                              <span v-if="a.activo" class="badge badge-success">Habilitad</span>
                              <span v-else class="badge badge-danger">Anulado</span>
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

  <!--- MODAL ALMACEN --->
     <div v-if="showModal">
      <div class="modal">
          <div class="modal-overlay"></div>
              <div class="modal-content" v-on:keyup.enter = "actualizarAlmacen()">
                  <div class="modal-header bg-primary text-white">
                      <h4>Editar Stock</h4>
                      <button type="button" class="close" @click="cerrarModal()">&times;</button>
                  </div>
                  <div class="modal-body">
                    <div class="mb-3 row">
                          <label for="" class="col-sm-4 col-form-label">Producto:</label>
                          <div class="col-sm-8">
                            <label class="col-form-label">{{ tituloModal }}</label>
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-4 col-form-label">Stock x {{uniMedidaTxt}}:</label>
                          <div class="col-sm-8">
                              <input type="number" class="form-control" v-model="cantidad" placeholder="0">
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-4 col-form-label">Stock x Uni/kg:</label>
                          <div class="col-sm-8">
                              <input type="number" class="form-control" v-model="total" placeholder="0">
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-4 col-form-label">Costo producto:</label>
                          <div class="col-sm-8">
                              <input type="number" class="form-control" v-model="precioCompra" placeholder="0">
                          </div>
                      </div>
                
                  </div>
                  <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" @click="cerrarModal()">Cerrar</button>
                      <button type="button" class="btn btn-primary" @click="actualizarAlmacen()">ACTUALIZAR</button>
                  </div>
              </div>
          </div>
          
      </div>
  <!--- FIN MODAL ALMACEN --->

    <!--- MODAL PRECIO --->
    <div v-if="showModalPrecio">
      <div class="modal">
          <div class="modal-overlay"></div>
              <div class="modal-content" v-on:keyup.enter = "accion === 'addPrecio' ? addPrecio() : updatePrecio()">
                  <div class="modal-header bg-primary text-white">
                      <h4>{{tituloModalPrecio}} S/</h4>
                      <button type="button" class="close" @click="cerrarModal()">&times;</button>
                  </div>
                  <div class="modal-body">
                      <div class="mb-3 row">
                          <label for="" class="col-sm-4 col-form-label">Producto:</label>
                          <div class="col-sm-8">
                              <label for="" class="col-form-label">{{ producto }}</label>
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-4 col-form-label">Unidad de venta:</label>
                          <div class="col-sm-8">
                              <select class="form-control" v-model="uniMedida">
                                <option :value="0">=== seleccione ===</option>
                                <option :value="uni.id" v-for="uni in unidadMedidas" :key="uni.id">{{ uni.nombre }}</option>
                              </select>
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-4 col-form-label">Precio de venta:</label>
                          <div class="col-sm-8">
                              <input type="number" class="form-control" v-model="precioVenta" placeholder="0.0">
                          </div>
                      </div>
                
                  </div>
                    
                  <div class="container mb-2">
                    <div class="row">
                        <div class="col-md-6">
                            <button v-if="accion == 'updatePrecio' " type="button" class="btn btn-danger text-left" @click="eliminarPrecio()">Eliminar</button>
                        </div>
                        <div class="col-md-6 text-right">
                            <button type="button" class="btn btn-secondary" @click="cerrarModalPrecio()">Cerrar</button>&nbsp;
                            <button v-if="accion == 'addPrecio' " type="button" class="btn btn-primary" @click="addPrecio()">GUARDAR</button>
                            <button v-if="accion == 'updatePrecio' " type="button" class="btn btn-primary" @click="updatePrecio()">ACTUALIZAR</button>      
                        </div>
                    </div> 
                </div>
              </div>
          </div>
          
      </div>
  <!--- FIN MODAL PRECIO --->
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
            cantidad:0,
            total:0,
            precioCompra:'',
            arrayAlmacen:[],
            proporcion_um:'',
            uniMedidaTxt:'',
            arrayCategorias:[],
            categoria:0,

            showModal: false,
            tituloModal:'',

            showModalPrecio:false,
            tituloModalPrecio:'',
            producto:'',
            unidadMedidas:[],
            uniMedida:0,
            errorPrecio:0,
            precioVenta:'',
            idAlmacenPrecio:'',
            accion:'',
                        
            errorAlmacen:0,
            arrayMostMsj:[],
            
            txtBuscar:'',
            ordenar:'total',

            currentPage: 1,
            totalPages: 0,
            listporPage: 20,
            visiblePages: [], // Páginas visibles en el paginado
            totalPagesToShow: 5, // Cantidad de páginas visibles en el paginado
            totalRegistros:0,

            showTooltip: false,
            localSocket:null,
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
              this.listarAlmacen(pageNumber,'',this.ordenar);
          },
          goToPreviousPage() {
              if (this.currentPage > 1) {
                  this.currentPage -= 1;
                  this.listarAlmacen(this.currentPage,'',this.ordenar);
              }
          },
          goToNextPage() {
              if (this.currentPage < this.totalPages) {
                  this.currentPage += 1;
                  this.listarAlmacen(this.currentPage,'',this.ordenar);
              }
          },
          goToFirstPage() {
              if (this.currentPage !== 1) {
                  this.currentPage = 1;
                  this.listarAlmacen(this.currentPage,'',this.ordenar);
              }
          },
          goToLastPage() {
              if (this.currentPage !== this.totalPages) {
                  this.currentPage = this.totalPages;
                  this.listarAlmacen(this.currentPage,'',this.ordenar);
              }
          },
          listarAlmacen(pageNumber = 1,txtBuscar,ordenar,categoria){ console.log(categoria)
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apinventario/almacen/?page=${pageNumber}&search=${txtBuscar}&ordenar=${ordenar}&categoria=${categoria}`)
              .then(function(response){
                  me.arrayAlmacen = response.data.results
                  me.currentPage = pageNumber
                  me.totalPages = Math.ceil(response.data.count / me.listporPage)
                  me.totalRegistros = response.data.count
              })
          },
          listarCategorias(){
            
            let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/api/allcategorias`)
              .then(function(response){
                  me.arrayCategorias = response.data
              })
          },
          abrirModal(data=[]){
              
                this.showModal = true
                this.tituloModal = data.nombre_producto+' x '+data.nombre_unimedida
                this.uniMedidaTxt = data.nombre_unimedida
                this.id = data.id
                this.cantidad = data.cantidad
                this.total = data.total
                this.precioCompra = data.precioCompra
                this.proporcion_um = data.proporcion_um
          },
          cerrarModal(){
                this.showModal = false;
                this.id = ''
                this.stockxUM = ''
                this.stockxuni = ''
                this.costo = ''
          },
          validarCompra(){
            const numerosExp = /^\d*\.?\d*$/;
            this.errorAlmacen = 0
            this.arrayMostMsj = []
              
            if(!numerosExp.test(this.precioCompra) || this.precioCompra === '') this.arrayMostMsj.push("El valor Costo producto no debe estar vacío")
            if(!numerosExp.test(this.total) || this.total === '') this.arrayMostMsj.push("El valor Stock x unidad no debe estar vacío")
            if(!numerosExp.test(this.cantidad) || this.cantidad === '') this.arrayMostMsj.push("El valor Stock x U/M no debe estar vacío")
            
            if(this.arrayMostMsj.length) this.errorAlmacen = 1
            return this.errorAlmacen
          },
          actualizarAlmacen(){
            if(this.validarCompra()){
                this.arrayMostMsj.forEach(element => {
                    this.$toastr.error(element,'Atencion!')
                });
                return
            }
            var cant; var tot;
            if(this.cantidad > 0 && this.total == 0){
            cant = this.cantidad
            tot = this.cantidad * this.proporcion_um
            }
            if(this.total > 0 && this.cantidad == 0){
            tot = this.total
            var division = this.total / this.proporcion_um
            cant = division.toFixed(1) //redondeamos a 1 decimal
            }
            if(this.total == 0 && this.cantidad == 0){
            tot = 0
            cant = 0
            }

            let me = this
            this.$axios.patch(`${process.env.VUE_APP_API_URL}/apinventario/almacen/`+me.id+`/`,{
            cantidad: cant,
            total: tot,
            precioCompra: me.precioCompra,            
            })
            .then(function(response){
                console.log(response)
                me.listarAlmacen(me.currentPage,me.txtBuscar,me.ordenar,me.categoria)
                me.cerrarModal()
                me.$toastr.success('Stock actualizado', 'Actualizado');
            })
            .catch(function (error) {
            console.log(error)
            })
          },
          eliminarAlmacen(id,nombre,activo){
              let me = this
              this.$swal.fire({
              title: nombre,
              text: activo ? 'Presione si para anular' : 'Presione si para restaurar',
              icon: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: activo ? 'Anular' : 'Restaurar',
              }).then((result) => {
              if (result.isConfirmed) {
                  this.$axios.patch(`${process.env.VUE_APP_API_URL}/apinventario/almacen/`+id+`/`,{
                    activo : activo ?  0 : 1,
                  })
                  .then(function(response){
                      console.log(response)
                      me.listarAlmacen(me.currentPage,me.txtBuscar,me.ordenar,me.categoria)
                      me.cerrarModal()
                      if(activo) me.$toastr.success('Producto anulado', 'Anulado')
                      else me.$toastr.success('Producto restaurado', 'Restaurado')
                      
                  })
              }
              })
          },
          abrirModalPrecio(accion,data=[],dato=[]){
            this.showModal=false
            this.showModalPrecio=true
            this.listarUnidadMedidas()
            this.id = data.id
            this.accion = accion
            switch(accion){
                case 'addPrecio':{
                    this.tituloModalPrecio = 'Agregar Precio'
                    this.producto = data.nombre_producto+' x '+data.nombre_unimedida
                    break
                }
                case 'updatePrecio':{
                    console.log(data)
                    this.tituloModalPrecio = 'Actualizar precio'
                    this.uniMedida = data.idUnidadMed
                    this.precioVenta = data.precio
                    this.idAlmacenPrecio = data.id
                    this.producto = dato.nombre_producto+' x '+dato.nombre_unimedida
                    break
                }
            }      
                            
        },
        cerrarModalPrecio(){
            this.showModalPrecio = false
            this.uniMedida=0
            this.arrayMostMsj=[]
            this.precioVenta=''
            this.idAlmacenPrecio=''
        },
        listarUnidadMedidas(){
            let me = this
            this.$axios.get(`${process.env.VUE_APP_API_URL}/api/unidadmedidall/`)
            .then(function(response){
                me.unidadMedidas = response.data
            })
        },
        validarPrecio(){
            this.errorPrecio = 0
            this.arrayMostMsj = []
            const numerosExp = /^\d*\.?\d*$/
            if(!numerosExp.test(this.precioVenta) || this.precioVenta === '') this.arrayMostMsj.push("El precio de venta debe ser numero positivo")
            if(this.uniMedida == 0) this.arrayMostMsj.push('Seleccione unidad de venta')
            if(this.arrayMostMsj.length) this.errorPrecio = 1
            return this.errorPrecio
        },
        addPrecio(){
            if(this.validarPrecio()){
                this.arrayMostMsj.forEach(element => {
                    this.$toastr.error(element,'Atencion')
                });
                return
            }
            let me = this
              this.$axios.post(`${process.env.VUE_APP_API_URL}/apinventario/almacenprecio/`, {
                  precio: me.precioVenta,
                  idAlmacen: me.id,
                  idUnidadMed: me.uniMedida
            })
            .then(function (response) {
                me.listarAlmacen(me.currentPage,me.txtBuscar,me.ordenar,me.categoria)
                me.cerrarModalPrecio()
                console.log(response)
                me.$toastr.success('Precio agregado', 'Registrado');
            })
            .catch(function (error) {
                me.$toastr.error('Error al guardar precio', 'Error')
                console.log(error)    
            })
        },
        updatePrecio(){
            if(this.validarPrecio()){
                this.arrayMostMsj.forEach(element => {
                    this.$toastr.error(element,'Atencion')
                });
                return
            }
            let me = this            
            this.$axios.patch(`${process.env.VUE_APP_API_URL}/apinventario/almacenprecio/`+me.idAlmacenPrecio+`/`,{
                precio: me.precioVenta,
                idUnidadMed: me.uniMedida
            }).
            then(function(response){
                me.listarAlmacen(me.currentPage,me.txtBuscar,me.ordenar,me.categoria)
                me.cerrarModalPrecio()
                me.$toastr.success('Precio actualizado','Actualizado')
                console.log(response)
            }).
            catch(function(error){
                me.$toastr.error('Error al actualizar','Error')
                console.log(error)
            })
        },
        eliminarPrecio(){
            let me = this            
            this.$axios.delete(`${process.env.VUE_APP_API_URL}/apinventario/almacenprecio/`+me.idAlmacenPrecio+`/`).
            then(function(response){
                me.listarAlmacen(me.currentPage,me.txtBuscar,me.ordenar,me.categoria)
                me.cerrarModalPrecio()
                me.$toastr.success('Precio eliminado','Borrado')
                console.log(response)
            }).
            catch(function(error){
                me.$toastr.error('Error al borrar','Error')
                console.log(error)
            })
        },
        exportarExcel(){
            window.open(`${process.env.VUE_APP_API_URL}/impresiones/almacenexcel/`+this.categoria, '_blank')
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
      created(){
        
      },
      mounted(){
        this.$socket.onopen = () => {
            console.log('Conexión WebSocket establecida en Almacen');
            // Puedes enviar el mensaje después de que la conexión se haya establecido
            //this.enviarMensaje();
        }
        this.$socket.onmessage = (event) => {
            const data = JSON.parse(event.data)
            console.log('mensaje onmessage de almacen')
            console.log(data.message)
            if(data.message === 'nuevo producto'){this.$toastr.success('Nuevo producto agregado', 'Producto agregado');}
            if(data.message === 'nueva compra'){this.$toastr.success('Stock actualizado', 'Actualizacion Stock');}
            this.listarAlmacen(1,this.txtBuscar,this.ordenar,this.categoria)
        }
        
        this.listarCategorias()
        this.listarAlmacen(1,this.txtBuscar,this.ordenar,this.categoria)
        this.updateVisiblePages()
        
      },
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
/* Estilo base del botón */
.tooltip-btn {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

/* Estilo del tooltip */
.tooltip-btn::before {
  content: attr(data-tooltip);
  position: absolute;
  background-color: rgba(0, 0, 0, 0.8);
  color: #fff;
  padding: 5px 10px;
  
  white-space: nowrap;
  border-radius: 4px;
  top: -30px; /* Ajusta la posición vertical según tus necesidades */
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s ease;
}

/* Mostrar el tooltip al hacer hover */
.tooltip-btn:hover::before {
  opacity: 1;
  visibility: visible;
}

</style>