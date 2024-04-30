<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0"><router-link to="/pedidos"><i class="fas fa-caret-square-left text-secondary"></i></router-link> Detalle de Venta <strong>N° {{ arrayPedido.numero }}</strong>&nbsp;&nbsp;
            <span v-if="arrayPedido.activo==0" class="badge badge-danger">ANULADO</span>
            <span v-if="arrayPedido.estado=='Pendiente' " class="badge badge-warning">PENDIENTE</span>
            <span v-if="arrayPedido.estado=='Pagado' " class="badge badge-success">PAGADO</span>
          </h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item"><router-link :to="{ name:'pedidos'}">Pedidos</router-link></li>
            <li class="breadcrumb-item active">Detalle</li>
          </ol>
        </div><!-- /.col -->
      </div><!-- /.row -->
    </div><!-- /.container-fluid -->
  </div>
  <!-- /.content-header -->

  <div class="card card-primary">
    <div class="card-header">
        Detalle de Pedido
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col-sm-4">
          <div class="form-group">
            <label for="exampleInputEmail1"><i class="fas fa-user"></i> N° Documento del Cliente</label>
            <input type="text" class="form-control" placeholder="Nombre del cliente" :value="arrayPedido.cliente_doc" readonly>
          </div>
        </div>
        <div class="col-sm-4">
          <div class="form-group">
            <label for="exampleInputEmail1"><i class="fas fa-user"></i> Nombre del Cliente</label>
            <input type="text" class="form-control" placeholder="Nombre del cliente" :value="arrayPedido.cliente" readonly>
          </div>
        </div>
        <div class="col-sm-4">
          <div class="form-group">
            <label for="exampleInputEmail1"><i class="fas fa-user-lock"></i> Dirección</label>
            <input type="text" class="form-control" readonly :value="arrayPedido.cliente_dir">
          </div>
      </div>
      </div>
      <div class="row">
        <div class="col-sm-4">
          <div class="form-group">
            <label for="exampleInputEmail1"><i class="fas fa-file-alt"></i> Comprobante</label>
            <select class="form-control" v-model="idTipoComprob" disabled>
              <option :value="0">{{arrayPedido.comprobante}}</option>
            </select>
          </div>
        </div>
        <div class="col-sm-4">
          <div class="form-group">
            <label for="exampleInputEmail1"><i class="far fa-calendar-check"></i> Fecha</label>
            <input type="date" class="form-control" readonly :value="arrayPedido.fecha">
          </div>
        </div>
        <div class="col-sm-4">
          <div class="form-group">
            <label for="exampleInputEmail1"> Vendedor</label><br>
            <input type="text" class="form-control" readonly :value="arrayPedido.usuario">
          </div>
        </div>
      </div>
      <br>
      <div class="row">
        <div class="col-md-12">
          <label for="">Lista de Productos</label>
          <table class="table table-sm table-bordered table-striped">
            <thead class="bg-success">
              <tr>
                <th>#</th>
                <th class="text-center">x</th>  
                <th>Producto</th>
                <th>U/M de Venta</th>
                <th width="8%">Cantidad</th>
                <th>Precio S/</th>
                <th width="8%">Descuento %</th>
                <th class="text-right">Importe</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(tab,index) in arrayListProd" :key="tab.id">
                <td>{{ index+1 }}</td>
                <td class="text-center"><i class="fas fa-trash-alt text-secondary"></i></td>
                <td><strong>{{ tab.producto }}</strong></td>
                <td>{{ tab.umVenta }}</td>
                <td>{{tab.cantidad}}</td>
                <td>{{ tab.precio }}</td>
                <td>{{ tab.descuento }} %</td>
                <td class="text-right"><strong>{{ formattedTotal(tab.importe) }}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <br>
      <div class="row">
        <div class="col-md-2">
          <input type="text" class="form-control form-control-lg" :value="arrayPedido.moneda" readonly>
        </div>
        <div class="col-md-2">
          <div class="input-group">
            <div class="input-group-prepend">
              <div class="input-group-text">IGV </div>
            </div>
            <input type="text" class="form-control form-control-lg bg-white text-md-left" readonly :value="arrayPedido.igv_total">
          </div>
        </div>
        <div class="col-md-2">
          <div class="input-group">
            <div class="input-group-prepend">
              <div class="input-group-text">DSCTO </div>
            </div>
            <input type="text" class="form-control form-control-lg bg-white text-md-left" readonly :value="arrayPedido.dscto_total">
          </div>
        </div>
        <div class="col-md-3">
          <div class="input-group">
            <div class="input-group-prepend">
              <div class="input-group-text">SubTotal </div>
            </div>
            <input type="text" class="form-control form-control-lg bg-white text-md-left" readonly :value="arrayPedido.subtotal">
          </div>
        </div>
       
        <div class="col-md-3 ml-md-auto">
          <div class="input-group">
            <div class="input-group-prepend">
              <div class="input-group-text"><strong>Importe Total:</strong></div>
            </div>
            <input type="text"  class="form-control form-control-lg bg-white text-md-right" readonly :value="formattedTotal(sumaTotal)">
          </div>
        </div>
      </div><br>
      <div class="row">
        <div class="offset-md-10 col-md-2">
          <div v-if="arrayPedido.activo==1 && arrayPedido.estado=='Pendiente'">
            <button class="btn btn-danger float-right" @click="anularPedido()"><i class="fas fa-trash-alt"></i> Anular Venta</button>
          </div>
          <div v-else>
            <button class="btn btn-secondary float-right"><i class="fas fa-trash-alt"></i> Anular Venta</button>
          </div>
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
            idPedido:'',
            txtBuscar:'',
            arrayPedido:[],
                        
            fechaHoy:'',
            idTipoComprob:0,
            
            showModal: false,

            arrayListProd:[],
            errorGenerar:0,
            arrayMostMsjGenerar:[],
            cliente:'',
          }
      },
      computed: {
        fechaFormateada() {
          if (this.fechaHoy) {
            const date = new Date(this.fechaHoy);
            const year = date.getFullYear();
            const month = date.getMonth() + 1;
            const day = date.getDate();
            return `${year}-${month < 10 ? '0' : ''}${month}-${day < 10 ? '0' : ''}${day}`;
          } else {
            return '';
          }
        },
        sumaTotal(){
          var suma = Number(this.arrayPedido.igv_total) + Number(this.arrayPedido.subtotal)
          return suma
        },
        id(){
            return this.$route.params.id
        }
      },
      methods:{
        listarPedido(){
            let me = this
            this.$axios.get(`${process.env.VUE_APP_API_URL}/apiventa/pedidos/${me.idPedido}/`)
              .then(function(response){
                  me.arrayPedido = response.data
              })
        },
        listarDetalle(){
            let me = this
            this.$axios.get(`${process.env.VUE_APP_API_URL}/apiventa/detalle/?idPedido=${me.idPedido}`)
              .then(function(response){
                  me.arrayListProd = response.data
              })
            
        }, 
        anularPedido(){
          let me = this
          this.$swal.fire({
          title: 'Anular Pedido',
          text: "Esta seguro?",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Si, Anular'
          }).then((result) => {
            if (result.isConfirmed) {
        
              this.$axios.post(`${process.env.VUE_APP_API_URL}/apiventa/detalle/`, { //URL ANULAR PEDIDO
                  idPedido: me.idPedido,
                  detalles: me.arrayListProd,
              }).
              then((response)=>{
                console.log(response.data)
                me.$router.push('/pedidos/')
                me.$toastr.success('Pedido anulado', 'Excelente!')
              }).
              catch((error)=>{
                console.error(error)
                me.$toastr.error('Error al anular venta', 'Error');
              })
            }
          })
        },
        
        recalcularItem(index){
          const item = this.arrayListProd[index]
          item.importe = item.precio * item.cantidad
        },
        formattedTotal(amount) {
            return new Intl.NumberFormat('es-PE', {
            style: 'currency',
            currency: 'PEN',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
            }).format(amount);
        },


    
      },
          
      watch: {
          
      },
      mounted(){
        this.idPedido = this.id
        this.listarPedido()
        this.listarDetalle()
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