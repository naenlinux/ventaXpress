<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0"><router-link to="/pedidos"><i class="fas fa-caret-square-left text-secondary"></i></router-link> Registrar Venta </h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item"><router-link :to="{ name:'pedidos'}">Venta</router-link></li>
            <li class="breadcrumb-item active">Nuevo</li>
          </ol>
        </div><!-- /.col -->
      </div><!-- /.row -->
    </div><!-- /.container-fluid -->
  </div>
  <!-- /.content-header -->

  <div class="card card-primary card-outline">
    <div class="card-body">
      <div class="row ">
        <div class="col-md-6">
          <div class="card card-warning">
            <div class="card-header">Datos del comprobante</div>
            <div class="card-body">
              <div class="col-sm-12">
                <div class="form-group">
                  <label for="exampleInputEmail1"><i class="fas fa-file-alt"></i> Comprobante</label>
                  <select class="form-control" v-model="idTipoComprob">
                    <option :value="0">=== Seleccione ===</option>
                    <option :value="tip.id"  v-for="tip in arrayTipoComp" :key="tip.id">{{ tip.nombre }}</option>
                  </select>
                </div>
              </div>
              <div class="row">
                <div class="col-sm-6">
                  <div class="form-group">
                    <label for="exampleInputEmail1"><i class="far fa-calendar-check"></i> Fecha</label>
                    <input type="date" class="form-control" readonly v-model="fechaHoy">
                  </div>
                </div>
                <div class="col-sm-6">
                  <div class="form-group">
                    <label for="exampleInputEmail1"><i class="fas fa-user-lock"></i> Vendedor</label>
                    <input type="text" class="form-control" readonly v-bind:value="nombreUsuario">
                  </div>
                </div>
              </div>
              <p></p>
              <div class="col-sm-12">
                <div class="form-group">
                  <label for="exampleInputEmail1"> <i class="fas fa-percent"></i> </label><br>
                  <div class="custom-control custom-switch">
                    <input type="checkbox" class="custom-control-input" id="customSwitch1" v-model="check_igv">
                    <label class="custom-control-label" for="customSwitch1">Aplicar IGV {{load_igv}}%</label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card card-primary">
            <div class="card-header">Datos del cliente</div>
            <div class="card-body">

          <div class="col-sm-12">
            <div class="form-group">
              <label for="exampleInputEmail1"><i class="fas fa-address-card"></i> N° Documento del Cliente</label>
              <input type="number" class="form-control" placeholder="0000000" v-model="cliente_doc">
            </div>
          </div>
          <div class="col-sm-12">
            <div class="form-group">
              <label for="exampleInputEmail1"><i class="fas fa-user"></i> Nombre de Cliente</label>
              <input type="text" class="form-control" placeholder="Nombre del cliente" v-model="cliente">
            </div>
          </div>
          <div class="col-sm-12">
            <div class="form-group">
              <label for="exampleInputEmail1"><i class="fas fa-address-book"></i> Dirección del cliente</label>
              <input type="text" class="form-control" placeholder="Dirección del cliente" v-model="cliente_dir">
            </div>
          </div>
          </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-md-12">
          <label for=""> <button class="btn btn-success" @click="abrirModal()"><i class="fas fa-shopping-cart"></i> Agregar Producto <i class="fas fa-search"></i></button></label> <button class="float-right btn-sm btn-danger" @click="cancelarVenta()">Limpiar</button>
          <table class="table table-sm table-bordered table-striped">
            <thead class="bg-success">
              <tr>
                <th>#</th>
                <th class="text-center">x</th>  
                <th>Producto</th>
                <th>Stock Uni</th>
                <th>U/M de Venta</th>
                <th width="8%">Precio</th>
                <th width="8%">Cantidad</th>
                <!--<th width="8%">Descuento %</th>-->
                <th class="text-right">Importe</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(tab,index) in arrayListProd" :key="tab.id">
                <td>{{ index+1 }}</td>
                <td class="text-center"><i class="fas fa-trash-alt text-danger" @click="eliminarItem(index)"></i></td>
                <td><strong>{{ tab.producto }}</strong></td>
                <td>{{ tab.stock }}</td>
                <td>{{ tab.umventa }}</td>
                <td>
                  <input v-model.number="tab.precio" :readonly="readonlyP" @dblclick="enableEditingP" @blur="disableEditingP" @keyup.enter="disableEditingP" @keyup="recalcularItem(index)" class="form-control">
                </td>
                <td>
                  <input v-model.number="tab.cantidad" class="form-control" @keyup="recalcularItem(index)"/>
                </td>
                <!--<td>
                  <input v-model.number="tab.descuento" class="form-control" :readonly="readonly" @dblclick="enableEditing" @blur="disableEditing" @keyup.enter="disableEditing" @keyup="recalcularItem(index)">
                </td>-->
                <td class="text-right"><strong>{{ formattedTotal(tab.importe) }}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <br>
      <div class="row">
        <div class="col-md-2">
          <select name="" class="form-control form-control-md bg-light" v-model="moneda">
            <option :value="mone.id" v-for="mone in arrayMoneda" :key="mone.id">{{mone.nombre}}</option>
          </select>
        </div>
        <div class="col-md-2">
          <div class="input-group mb-3">
            <div class="input-group-prepend">
              <span class="input-group-text">IGV</span>
            </div>
            <input type="text" class="form-control form-control-md bg-white" readonly :value="formattedTotal(sumaigv=sumaIgv)">
          </div>
        </div>
        <div class="col-md-2">
          <div class="input-group mb-3">
            <div class="input-group-prepend">
              <span class="input-group-text">DSCTO</span>
            </div>
            <input type="text" class="form-control form-control-md bg-white" readonly :value="formattedTotal(totalDscto=(sumaTotalSINdscto-sumaSubtotal))">
          </div>
        </div>
        <div class="col-md-2">
          <div class="input-group mb-3">
            <div class="input-group-prepend">
              <span class="input-group-text">Subtotal</span>
            </div>
            <input type="text" class="form-control form-control-md bg-white" readonly :value="formattedTotal(subtotal=sumaSubtotal)">
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="input-group ">
            <div class="input-group-prepend ">
              <div class="input-group-text"><b>TOTAL A PAGAR:</b></div>
            </div>
            <input type="text" class="form-control font-weight-bold form-control-lg bg-white text-md-right " readonly :value="formattedTotal(sumatotal=sumaTotal)">
          </div>
        </div>
      </div>
      <br>
      <div class="row justify-content-end">
        <div class="col-md-2 text-right">
          <button class="btn btn-primary btn-lg" @click="grabarPedido()"><i class="fas fa-save"></i> Grabar Venta</button>
        </div>
      </div>
    </div>
  </div><!-- /.card -->


    <!-- Modal -->
  <div v-if="showModal">
    <div class="modal">
      <div class="modal-overlay"></div>
      
        <div class="modal-content">
          <div class="modal-header bg-primary">
            <h5 class="modal-title">Productos</h5>
            <button type="button" class="close" aria-label="Close">
              <span aria-hidden="true" @click="cerrarModal()">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="input-group mb-3">
              <div class="input-group-prepend">
                <span class="input-group-text">Productos: </span>
              </div>
              <input type="text" class="form-control" v-model="txtBuscar" placeholder="Buscar producto" @keyup="listarProducto(txtBuscar)">
              <div class="input-group-append">
                <span class="input-group-text"><i class="fas fa-search"></i></span>
              </div>
            </div>


            <div class="table-responsive">
              <div style="height: 300px; overflow: auto;">
              <table class="table table-sm table-bordered cabeceraFija table-striped">
                <thead class="bg-primary">
                  <tr>
                    <th>Producto</th>
                    <th>Stock Unidad</th>
                    <th>Precios</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="p in arrayProducto" :key="p.id">
                    <td v-text="p.nombre_producto"></td>
                    <td v-text="p.total"></td>
                    <td>
                      <button class="btn btn-sm btn-info ml-1" href="#" v-for="pre in p.precios_um" :key="pre.id" @click="agregarTablaVenta(p,pre)">
                          {{ pre.nombre_unidad_medida+ ' S/. '+pre.precio }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-dark" @click="cerrarModal()">Cerrar</button>
          </div>
        </div>
      
    </div>
  </div>

</template>

<script>
import { ref, onMounted } from 'vue' //sobre fechas
import { DateTime } from 'luxon' //timezone manejo
    export default{
      setup() {
        const fechaHoy = ref('');
        onMounted(() => {
          const today = DateTime.now().setZone('America/Lima');
          fechaHoy.value = today.toISODate();
        });
        return {
          fechaHoy,
        };
      },
      props:{
        nombreUsuario:String,
        idUsuario:Number,
        idSucursal:Number,
        permisoDscto:Boolean,
      },
      data(){
          return{
            txtBuscar:'',
            arrayProducto:[],
            igv:0,
            load_igv:'',
            arrayMoneda:[],
            moneda:1,
            check_igv: false,
            readonly: true,
            readonlyP: true,
            
            idTipoComprob:0,
            arrayTipoComp:[],

            showModal: false,

            arrayListProd:[],
            errorGenerar:0,
            arrayMostMsjGenerar:[],
            cliente:'',
            cliente_doc:'',
            cliente_dir:'',
          }
      },
      computed: {
        fechaFormateada() {
          if (this.fechaHoy) {
            const date = new Date(this.fechaHoy);
            const options = {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit',
            };
            return date.toLocaleDateString(undefined, options);
          } else {
            return '';
          }
        },
        sumaSubtotal(){
          return this.arrayListProd.reduce((importe,item) => importe + item.importe,0)
        },
        sumaTotal(){
          var sub = this.arrayListProd.reduce((importe,item) => importe + item.importe,0)
          var totalIgv = this.arrayListProd.reduce((igv,item) => igv + item.igv,0)
          return sub + totalIgv
        },
        sumaIgv(){
          return this.arrayListProd.reduce((igv,item) => igv + item.igv,0)
        },
        sumaTotalSINdscto(){
          return this.arrayListProd.reduce((sumatoria, item) => (sumatoria + (item.cantidad * item.precio)), 0);
        }
      },
      methods:{
        listarProducto(txtBuscar){
          let me = this
          this.$axios.get(`${process.env.VUE_APP_API_URL}/apinventario/almacen/?page=1&search=${txtBuscar}&ordenar=`)
          .then(function(response){
              me.arrayProducto = response.data.results
          })
        },
        abrirModal(){
          this.showModal = true
          this.listarProducto('')
        },
        cerrarModal(){
          this.showModal = false
          this.arrayProducto=[]
          this.txtBuscar=''
        },
        agregarTablaVenta(data=[],dato=[]){//alert(data.total+ ' '+ dato.proporcion)
        
          if(parseFloat(data.total) < dato.proporcion ){
            this.$toastr.error('Producto sin STOCK','Atencion!')
            return
          }
          const existeProduc = this.arrayListProd.find((element) => element.idAlmacen === data.id)//validar duplicado de producto al array
          if(existeProduc){
            this.$toastr.error('Este producto ya esta agregado','Duplicado!')
            return
          }
          
          this.arrayListProd.push({
            idAlmacen: data.id,
            producto: data.nombre_producto,
            umventa: dato.nombre_unidad_medida,
            idUMventa: dato.idUnidadMed,
            precio: dato.precio,
            proporcionVentaUM:dato.proporcion,
            proporcionUM: data.proporcion_um,
            stock: data.total,
            cantidad: 1,
            descuento: 0,
            importe: dato.precio * 1,
            igv: (dato.precio * 1) * (this.igv/100)
          })
          this.cerrarModal()
        },
        recalcularItem(index){
          const item = this.arrayListProd[index]
          if(item.cantidad * item.proporcionVentaUM > item.stock){
            this.$toastr.error('La cantidad '+item.cantidad+' supera STOCK','NO HAY STOCK!')
            item.cantidad = 1
            return
          }
          let descuen = (item.precio * (item.descuento)/100).toFixed(1) //calculamos si hay descuento
          console.log(descuen)
          item.importe = (item.precio - descuen) * item.cantidad
          item.igv = (item.precio * item.cantidad) * (this.igv/100)
        },
        formattedTotal(amount) {
            return new Intl.NumberFormat('es-PE', {
            style: 'currency',
            currency: 'PEN',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
            }).format(amount);
        },
        eliminarItem(index){
          this.arrayListProd.splice(index,1)
        },
        validarVenta(){
          this.errorGenerar = 0
          this.arrayMostMsjGenerar = []
          if(!this.arrayListProd.length) this.arrayMostMsjGenerar.push("Agregue un producto a la lista")
          //validar cantidad y costo de la tabla arrayListProd
          this.arrayListProd.forEach(element => {
            if(element.importe <= 0 || isNaN(element.importe)){
              this.arrayMostMsjGenerar.push("Revisar la tabla de productos, cantidad y precio deben ser números positivos")
              return
            }
          })
          if(this.cliente){
            if(this.cliente.length < 3) this.arrayMostMsjGenerar.push("El nombre de cliente debe tener más de 3 letras")
          } 
          if(!this.cliente) this.arrayMostMsjGenerar.push("Ingrese nombre de cliente")
          if(!this.idTipoComprob) this.arrayMostMsjGenerar.push("Seleccione un tipo de comprobante")
          if(this.arrayMostMsjGenerar.length) this.errorGenerar = 1
          return this.errorGenerar
        },
        grabarPedido(){
          if(this.validarVenta()){
            this.arrayMostMsjGenerar.forEach(element => {
              this.$toastr.error(element,'Atencion!')
            });
            return
          }
          let me = this
          this.$swal.fire({
          title: 'Generar nueva venta',
          text: "Esta seguro?",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Si, generar'
          }).then((result) => {
            if (result.isConfirmed) {
              let detalleArray = this.arrayListProd.map((detalle)=>{
              return {
                idAlmacen: detalle.idAlmacen,
                producto: detalle.producto,
                umVenta: detalle.umventa,
                idUMventa: detalle.idUMventa,
                precio:detalle.precio,
                proporcionVentaUM:detalle.proporcionVentaUM,
                proporcionUM:detalle.proporcionUM,
                stock: detalle.total,
                cantidad:detalle.cantidad,
                descuento: detalle.descuento,
                importe:detalle.importe
              }
              })
              this.$axios.post(`${process.env.VUE_APP_API_URL}/apiventa/pedidos/`, { //URL GRABAR PEDIDO
                  idUsuario: me.idUsuario,
                  idComprob:me.idTipoComprob,
                  cliente:me.cliente,
                  cliente_doc:me.cliente_doc,
                  cliente_dir:me.cliente_dir,
                  estado:'Pendiente',
                  numero:null,
                  subtotal: me.subtotal,
                  igv_total: parseFloat(me.sumaigv).toFixed(2), // redondear a dos decimales la suma del IGV
                  idMoneda: me.moneda,
                  detalles: detalleArray,
                  idSucursal:me.idSucursal,
                  dscto_total: me.totalDscto,
              }).
              then((response)=>{
                console.log(response.data)
                me.$router.push('/pedidos/')
                me.$toastr.success('Nuevo Pedido generado', 'Excelente!')
                me.$socket.send(JSON.stringify({
                  'message':'nuevo pedido'
                }))
              }).
              catch((error)=>{
                console.error(error)
                me.$toastr.error('Error al generar pedido', 'Error');
              })
            }
          })
        },
        cancelarVenta(){
          this.cliente=''
          this.cliente_doc=''
          this.cliente_dir=''
          this.idTipoComprob=0
          this.check_igv = false
          this.arrayListProd=[]
        },
        listarCompro(){
          let me = this
          this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/tipocomprobante/`)
          .then(function(response){
            if(response.data.length){
                me.arrayTipoComp = response.data
            }
          })
        },
        listarIgv(){
            let me = this
            this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/impuesto/`)
            .then(function(response){
              if(response.data.length){
                me.load_igv = response.data[0]['valor_porcentaje']
              }else{
                me.$toastr.error('El IGV no esta configurado','Atencion!')
              }
            })
        },
        changeIgv(){
          this.$nextTick(() => {
            this.igv = this.check_igv ? 18 : 0;
            
          });
        },
        listarMoneda(){
          let me = this
          this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/moneda/`)
          .then(function(response){
            if(response.data.length){
                me.arrayMoneda = response.data
            }
          })
        },
        enableEditing() {
          if(this.permisoDscto){
            this.readonly = false; // Cambia readonly a falso cuando se hace doble clic
          }else{
            this.$toastr.info('No cuenta con permiso para esta función','Sin autorización!')
          }
          
        },
        disableEditing() {
          this.readonly = true; // Cambia readonly a verdadero cuando se pierde el foco o se presiona Enter
        },
        enableEditingP() {
          console.log(this.permisoDscto)
          if(this.permisoDscto){
            this.readonlyP = false; // Cambia readonly a falso cuando se hace doble clic
          }else{
            this.$toastr.info('No cuenta con permiso para esta función','Sin autorización!')
          }
          
        },
        disableEditingP() {
          this.readonlyP = true; // Cambia readonly a verdadero cuando se pierde el foco o se presiona Enter
        }
      },
      watch: {
        check_igv: {
          handler(newVal) {
            this.igv = newVal ? this.load_igv : 0;
            if(this.arrayListProd.length){ // Recalcular el IGV de la lista de productos
              this.arrayListProd.forEach(item => {
                item.igv = (item.precio * item.cantidad) * (this.igv/100)
              })
            }
            
          },
          immediate: true // Esto garantiza que se ejecute el watcher cuando se carga el componente por primera vez.
        }
      },
      mounted(){
        this.listarCompro()
        this.listarIgv()
        this.listarMoneda()
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
  width: 70%;
  background-color: white;
  margin-top: 100px;
}
.cabeceraFija thead th {
  position: sticky;
  top: 0;
  background-color:dodgerblue; /* Color de fondo para resaltar la cabecera */
  z-index: 1; /* Asegura que la cabecera se superponga sobre el contenido */
}
</style>