<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0"><router-link to="/compras/"><i class="fas fa-caret-square-left text-secondary"></i></router-link> Detalle de compra</h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item active">Detalle</li>
          </ol>
        </div><!-- /.col -->
      </div><!-- /.row -->
    </div><!-- /.container-fluid -->
  </div>
  <!-- /.content-header -->


    <div class="card card-primary">
      <div class="card-header">
        <h3 class="card-title">Detalle de compra</h3>
      </div>
      <!-- /.card-header -->
      <div class="card-body">
            <div class="row">
            <div class="col-sm-6">
              <!-- text input -->
              <div class="form-group">
                <label>Proveedor</label>
                <select class="form-control" disabled>
                    <option value="">{{ arrayProveedor.proveedor }}</option>
                </select>
              </div>
            </div>
            <div class="col-sm-6">
              <div class="form-group">
                <label>RUC</label>
                <input type="text"  class="form-control" readonly v-model="arrayProveedor.ruc">
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-sm-3">
              <div class="form-group">
                <label>Comprobante</label>
                <input type="text" class="form-control" v-model="arrayProveedor.comprobante" readonly>
              </div>
            </div> 
            <div class="col-sm-3">
              <div class="form-group">
                <label>Numero</label>
                <input type="text" class="form-control" v-model="arrayProveedor.numeroComprob" readonly>
                
              </div>
            </div> 
            <div class="col-sm-6">
              <div class="form-group">
                <label>Fecha de compra</label>
                <input type="date" class="form-control" v-model="arrayProveedor.fecha" readonly>
              </div>
            </div> 
          </div>

              <div class="row">
                <div class="col-sm-12">
                    <label for="">Productos</label>
                  <table class="table table-sm table-bordered table-striped">
                    <thead class="bg-info">
                      <tr>
                        <th>#</th>
                        <th>x</th>
                        <th>Producto</th>
                        <th>Descripción</th>
                        <th class="text-center">Cantidad</th>
                        <th class="text-right">Precio de Compra</th>
                        <th class="text-right">SubTotal</th>
                      </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(de,index) in arrayDetalle" :key="de.id">
                            <td>{{ index+1 }}</td>
                            <td></td>
                            <td>{{ de.producto }}</td>
                            <td>{{ de.producto_um }}</td>
                            <td class="text-center">{{ de.cantidad }}</td>
                            <td class="text-right">{{ de.precio }}</td>
                            <td class="text-right">{{ formattedTotal(de.cantidad * de.precio) }}</td>
                        </tr>
                        <tr>
                            <td colspan="6" class="text-right"><h5>TOTAL</h5></td>
                            <td class="text-right"><h5><strong>{{ formattedTotal(total) }}</strong></h5></td>
                        </tr>
                    </tbody>
                  </table>
                </div>
              
          </div>
        </div>
        <!-- /.card-body -->
        <div class="card-footer">
          <div class="text-right">
            <button type="button" v-if="arrayProveedor.activo" class="btn btn-danger" @click="AnularCompra()"><i class="fas fa-trash"></i> ANULAR COMPRA</button>
            <button type="button" v-else class="btn btn-danger" disabled>ANULADO</button>
          </div>                  
        </div>
        <!-- /.card-footer -->
    </div>
            

</template>
<script>
    import 'vue-multiselect/dist/vue-multiselect.css'
    
    export default{
      props:{
            nombreUsuario:String,
            idUsuario:Number,
        },
        components:{
            
        },
      data(){
        return{
          idCompra:'',
          arrayProveedor:[],
          arrayDetalle:[],

          idTipoComprob:0,

          inputCantidad:'',
          inputPrecio:'',
          sumatotal:'',

        }
      },
      computed:{
        id(){
           return this.$route.params.id
        },
        total(){
            return this.arrayDetalle.reduce((suma, de) => suma + de.cantidad * de.precio, 0)
        },
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
        listarProveedor(){
            let me = this
            this.$axios.get(`${process.env.VUE_APP_API_URL}/apinventario/compras/${me.idCompra}/`)
              .then(function(response){
                  me.arrayProveedor = response.data
              })
        },
        listarDetalle(){
            let me = this
            this.$axios.get(`${process.env.VUE_APP_API_URL}/apinventario/detalle/?idCompra=${me.idCompra}`)
              .then(function(response){
                  me.arrayDetalle = response.data
              })
            
        },        
        formatCosto(value){
          this.sumatotal = value
            // Utilizar Intl.NumberFormat para formatear el precio con dos decimales y separador de miles
          const formatter = new Intl.NumberFormat('es-ES', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          });
          return formatter.format(value).replace(/,/g, ' ').replace(/\./g, ',').replace(/ /g, '.');
        },
        AnularCompra(){

            let me = this
            this.$swal.fire({
            title: 'Anular esta compra?',
            text: "El STOCK de los productos se actualizaran",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si, Anular!'
            }).then((result) => {
                if (result.isConfirmed) {
                    this.$axios.post(`${process.env.VUE_APP_API_URL}/apinventario/detalle/`, { //URL  ACTUALIZAR
                        idCompra: me.idCompra,
                        detalles: me.arrayDetalle,
                    }).
                    then((response)=>{
                    console.log(response.data)
                    me.$router.push('/compras/')
                    me.$toastr.success('Compra anulada', 'Anulado')
                    }).
                    catch((error)=>{
                        console.log(error)
                        me.$toastr.error('Hubo un error al anular', 'Error');
                    })
                }
            })
        }
          
      },
          
      watch: {
         
      },
      mounted(){
        this.idCompra = this.id
        this.listarProveedor()
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
  width: 40%;
  background-color: white;
  margin-top: 100px;
}
</style>