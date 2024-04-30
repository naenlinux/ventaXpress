<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0"><router-link to="/compras/">
            <i class="fas fa-caret-square-left text-secondary"></i>
                    </router-link> Nueva compra</h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item"><router-link :to="{ name:'compras'}">Compras</router-link></li>
            <li class="breadcrumb-item active">Nuevo</li>
          </ol>
        </div><!-- /.col -->
      </div><!-- /.row -->
    </div><!-- /.container-fluid -->
  </div>
  <!-- /.content-header -->
  <!--nuevo comentario-->
            <div class="card card-primary">
              <div class="card-header">
                <h3 class="card-title">Registrar nueva compra</h3>
              </div>
              <!-- /.card-header -->
              <div class="card-body">
                    <div class="row">
                    <div class="col-sm-6">
                      <!-- text input -->
                      <div class="form-group">
                        <label>Seleccionar Proveedor</label>
                        <VueMultiselect
                            v-model="proveedSelect"
                            :options="arrayProveedor"
                            :custom-label="nameWithLang"
                            :show-labels="false"
                            :searchable="true"
                            :select-label="placeholderSelectPro"
                            @search-change= 'buscarProveedor'
                            />
                      </div>
                    </div>
                    <div class="col-sm-6">
                      <div class="form-group">
                        <label>RUC</label>
                        <input type="text" v-if="proveedSelect" class="form-control" readonly v-model="proveedSelect.ruc">
                        <input type="text" v-else class="form-control" readonly placeholder="Sin seleccionar">
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-sm-4">
                      <div class="form-group">
                        <label>Tipo de comprobante</label>
                        <select class="form-control" v-model="idTipoComprob">
                          <option :value="0">Seleccione</option>
                          <option :value="tip.id"  v-for="tip in arrayTipoComp" :key="tip.id">{{ tip.nombre }}</option>
                        </select>
                      </div>
                    </div> 
                    <div class="col-sm-4">
                      <div class="form-group">
                        <label>Numero de comprobate</label>
                        <input type="text" class="form-control" placeholder="000-0001" v-model="numeroComprob">
                      </div>
                    </div> 
                    <div class="col-sm-4">
                      <div class="form-group">
                        <label>Fecha de compra</label>
                        <input type="date" class="form-control" v-model="fechaCompra">
                      </div>
                    </div> 
                  </div>
                  <div class="card card-secondary">
                    <div class="card-header">
                      Agregar productos de compra
                    </div>
                    <div class="card-body" v-on:keyup.enter="addListProd()">
                      <div class="row">
                        <div class="col-sm-6">
                          <label>Buscar producto</label>
                          <VueMultiselect
                            v-model="productoSelect"
                            :options="arrayProducto"
                            :custom-label="nameWithLangPro"
                            :show-labels="false"
                            :searchable="true"
                            :select-label="placeholderSelectPro"
                            @search-change= 'buscarProducto'
                            />
                        </div>
              
                        <div class="col-sm-2">
                            <label>Cantidad</label>
                          <div class="input-group">
                            <div class="input-group-prepend">
                              <span class="input-group-text"><i class="fas fa-calculator"></i></span>
                            </div>
                            <input type="number" class="form-control" placeholder="000" v-model="inputCantidad">
                          </div>
                        </div>
                        <div class="col-sm-2">
                            <label>Precio de compra</label>
                          <div class="input-group">
                            <div class="input-group-prepend">
                              <span class="input-group-text"><i class="fas fa-dollar-sign"></i></span>
                            </div>
                            <input type="number" class="form-control" placeholder="00.00" v-model="inputPrecio">
                          </div>
                        </div>
                        <div class="col-sm-2">
                            <label>Accion</label>
                          <div class="input-group">
                            <button type="button" class="btn btn-success"
                              @click="addListProd()">
                              <i class="fas fa-plus-square"></i> AGREGAR</button>
                          </div>
                        </div>
                      </div>
                      <label class="mt-3">Lista de productos:</label> 
                      <div class="row">
                        <div class="col-sm-12">
                          <table class="table table-sm table-bordered table-striped">
                            <thead class="bg-info">
                              <tr>
                                <th>#</th>
                                <th>x</th>
                                <th>Producto</th>
                                <th>Cantidad</th>
                                <th>Precio de Compra</th>
                                <th class="text-right">SubTotal</th>
                                
                              </tr>
                            </thead>
                            <tbody>
                              <tr v-for="(list,index) in  arrayProductoAdd" :key="list">
                                <td>{{index+1}}</td>
                                <td>
                                  <button class="btn btn-sm btn-danger" @click="eliminarItem(index)"><i class="fas fa-trash-alt"></i></button>
                                </td>
                                <td>{{ list.producto }}</td>
                                <td>
                                  <input v-model.number="list.cantidad" class="form-control" @keyup="recalcularItem(index)"/>  
                                </td>
                                <td>
                                  <input v-model.number="list.precio" class="form-control" @keyup="recalcularItem(index)"/>  
                                </td>  
                                <td class="text-right"><strong>{{ formattedTotal(list.subtotal) }}</strong>  </td>  
                              </tr>
                              <tr>
                                <td colspan="5" class="text-right">
                                  <h4>Total</h4>
                                </td>
                                <td class="text-right">
                                  <h4>{{ formattedTotal(sumatotal=sumaTotal) }}</h4>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- /.card-body -->
                <div class="card-footer">
                  <div class="text-center">
                    <button type="button" class="btn btn-primary" @click="grabarCompra()"><i class="fas fa-save"></i> GRABAR COMPRA</button>
                  </div>                  
                </div>
                <!-- /.card-footer -->
            </div>
            

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
    import VueMultiselect from 'vue-multiselect'
    import 'vue-multiselect/dist/vue-multiselect.css'
    

    export default{
        components:{
            VueMultiselect
        },
        props:{
            nombreUsuario:String,
            idUsuario:Number,
        },
      data(){
        return{
          id:'',
          idProveedor:'',
          fechaCompra:'',
          numeroComprob:'',
          arrayProveedor: [],
          proveedSelect:null,
          rucSelect:'',

          productoSelect:null,
          arrayProducto:[],
          uniMedidaSelect:null,
          

          placeholderSelectPro:'Buscar proveedor',

          showModal: false,
          tituloModal: '',
          errorAddListpro:0,
          arrayMostMsjAdd:[],
          tipoAccion: 0,
          txtBuscar:'',
          errorSaveUpdate:[],

          arrayTipoComp:[],
          idTipoComprob:0,

          arrayProductoAdd:[],
          inputCantidad:'',
          inputPrecio:'',
          sumatotal:'',

        }
      },
      computed: {
        isOnFirstPage() {
        return this.currentPage === 1;
        },
        isOnLastPage() {
        return this.currentPage === this.totalPages;
        },
        sumaTotal(){
          return this.arrayProductoAdd.reduce((subtotal,item) => subtotal + item.subtotal,0)
        }
      },
      methods:{
        formattedTotal(amount) {
            return new Intl.NumberFormat('es-PE', {
            style: 'currency',
            currency: 'PEN',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
            }).format(amount);
        },
        nameWithLang ({ empresa}) {
            return `${empresa}`
        },
        nameWithLangPro ({ nombre,  nombre_unimedida }) {
            return `${nombre} - ${nombre_unimedida}`
        },
        buscarProveedor(txtBuscar){
            let me = this
            this.$axios.get(`${process.env.VUE_APP_API_URL}/api/proveedores/?search=${txtBuscar}`)
            .then(function(response){
                me.arrayProveedor = response.data.results
            })
        },
        buscarProducto(txtBuscar){
          let me = this
          if(txtBuscar != ''){
            this.$axios.get(`${process.env.VUE_APP_API_URL}/api/productos/?search=${txtBuscar}`)
            .then(function(response){
                const filterProd =  response.data.results.filter(element => element.activo == 1)
                me.arrayProducto = filterProd
            })
          }else{me.arrayProducto = []}
        },
        buscarUniMedida(txtBuscar){
          let me = this
          if(txtBuscar != ''){
            this.$axios.get(`${process.env.VUE_APP_API_URL}/api/unidadmedida/?search=${txtBuscar}`)
            .then(function(response){
              const arrayfilter = response.data.results.filter(element => element.activo == 1);
              me.arrayUniMedida = arrayfilter
            })
          }else{me.arrayUniMedida = []}
          
        },
        validarAddLisPro(){
          this.errorAddListpro = 0
          this.arrayMostMsjAdd = []
          if(!this.inputPrecio) this.arrayMostMsjAdd.push("Ingrese precio de compra")
          if(!this.inputCantidad) this.arrayMostMsjAdd.push("Ingrese una cantidad")
          if(this.productoSelect==null || this.productoSelect == '') this.arrayMostMsjAdd.push("Ingrese un producto")
          const existeProduc = this.arrayProductoAdd.find((element) => element.idpro === this.productoSelect.id)//validar duplicado de producto al array
          if(existeProduc){this.arrayMostMsjAdd.push("Este producto ya esta agregado")}
          if(this.arrayMostMsjAdd.length) this.errorAddListpro = 1
          return this.errorAddListpro
        },
        addListProd(){
          //validamos
          if(this.validarAddLisPro()){
              this.arrayMostMsjAdd.forEach(element => {
                this.$toastr.error(element,'Atencion!')
              });
              return
          }
          var subtotal = this.inputCantidad * this.inputPrecio
          this.arrayProductoAdd.push({
            idpro: this.productoSelect.id,
            producto: this.productoSelect.nombre+' - '+this.productoSelect.nombre_unimedida,
            cantidad: this.inputCantidad,
            precio: this.inputPrecio,
            subtotal: subtotal,
            unidadMedida: this.productoSelect.unidadMedida, //este id solo se va usar para enviar a django y actualizar los stock
          })
          subtotal = 0
          this.productoSelect = ''
          this.inputCantidad = ''
          this.inputPrecio = ''
        },
        recalcularItem(index){
          const item = this.arrayProductoAdd[index]
          item.subtotal = item.precio * item.cantidad
        },         
        eliminarItem(index){
          this.arrayProductoAdd.splice(index,1)
        },
     
        validadGrabar(){
          this.errorGrabar = 0
          this.arrayMostMsjGra = []
          if(!this.arrayProductoAdd.length) this.arrayMostMsjGra.push("Agregue un producto a la lista")
          if(!this.fechaCompra) this.arrayMostMsjGra.push("Ingrese una fecha de compra")
          if(!this.numeroComprob) this.arrayMostMsjGra.push("Ingrese un número de comprobante")
          if(!this.idTipoComprob) this.arrayMostMsjGra.push("Seleccione un tipo de comprobante")
          if(this.proveedSelect==null) this.arrayMostMsjGra.push("Ingrese un Proveedor")
          

          //validar cantidad y costo de la tabla arrayProducAdd
          this.arrayProductoAdd.forEach(element => {
            if(element.subtotal <= 0 || isNaN(element.subtotal)){
              this.arrayMostMsjGra.push("Revisar la tabla de productos, cantidad y precio deben ser números positivos")
              return
            }
          })

          if(this.arrayMostMsjGra.length) this.errorGrabar = 1
          return this.errorGrabar
        },
        grabarCompra(){
          if(this.validadGrabar()){
            this.arrayMostMsjGra.forEach(element => {
              this.$toastr.error(element,'Atencion!')
            });
            return
          }
          let me = this
          this.$swal.fire({
          title: 'Registrar nueva compra?',
          text: "El STOCK de los productos se actualizaran",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Si, Registrar!'
        }).then((result) => {
          if (result.isConfirmed) {
            let detalleArray = this.arrayProductoAdd.map((detalle)=>{
            return {
              idProducto: detalle.idpro,
              cantidad: detalle.cantidad,
              precio: detalle.precio,
              unidadMedida: detalle.unidadMedida,
            }
            })
            this.$axios.post(`${process.env.VUE_APP_API_URL}/apinventario/compras/`, { //URL GRABAR COMPRA
                fecha: me.fechaCompra,
                numeroComprob: me.numeroComprob,
                compraTotal: me.sumatotal,
                idProveedor: me.proveedSelect.id,
                idTipoComprob: me.idTipoComprob,
                detalles: detalleArray,
            }).
            then((response)=>{
              console.log(response.data)
              me.$router.push('/compras/')
              me.$toastr.success('Nueva compra agregado', 'Registrado')
              me.$socket.send(JSON.stringify({
                'message':'nueva compra'
              }))
            }).
            catch((error)=>{
              console.error(error)
              me.$toastr.error('Hubo un error al registrar compra', 'Error');
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
         
      },
      mounted(){
        let me = this
        this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/tipocomprobante/`)
        .then(function(response){
          if(response.data.length){
              me.arrayTipoComp = response.data
          }
        })
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