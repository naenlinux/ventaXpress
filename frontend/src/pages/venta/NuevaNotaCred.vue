<template>
       <!-- Content Header (Page header) -->
       <div class="content-header">
        <div class="container-fluid">
          <div class="row mb-2">
            <div class="col-sm-6">
              <h1 class="m-0">Crear Nota de Crédito</h1>
            </div><!-- /.col -->
            <div class="col-sm-6">
              <ol class="breadcrumb float-sm-right">
                <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
                <li class="breadcrumb-item active">Crear Nota crédito</li>
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
                    <div class="form-group">
                        <label for="staticEmail" class="col-form-label">Tipo de Nota de Crédito</label>
                          <select name="" class="form-control" v-model="tipoNota">
                            <option value="0">==== Seleccione ====</option>
                            <option v-for="not in arrayCodigoNC" :key="not.id" :value="not.id">{{not.descripcion}}</option>
                          </select>
                      </div>
                      <div class="form-group">
                        <label  class="col-form-label">Fecha de emisión</label>
                          <input type="date" class="form-control bg-white" :value="fechaHoy" readonly>
                      </div>
                      <div class="form-group">
                        <label  class="col-form-label">Motivo de la anulación</label>
                          <input type="text" class="form-control" v-model="motivo" placeholder="Describe el motivo">
                      </div>
                      <div class="form-group">
                          <button class="btn btn-primary" @click="grabarNota()"><i class="fas fa-save"></i> GENERAR</button>
                      </div>
                </div>
                <div class="col-sm-6">
                    <div class="form-group">
                        <label for="staticEmail" class="col-form-label">Comprobante a anular</label>
                        <input type="text" class="form-control" readonly :value="comprobante">
                      </div>
                      <div class="form-group">
                        <label  class="col-form-label">Número de comprobante</label>
                          <input type="text" class="form-control" readonly :value="serieNumero">
                      </div>
                      <div class="form-group">
                        <label class="col-form-label">Cliente</label>
                          <input type="text" class="form-control" readonly :value="cliente">
                      </div>                    
                </div>
              </div>
              <br>
              <h4>Detalle del comprobante a anular</h4>
              <div class="table-responsive">
                <table class="table table-sm table-striped table-bordered">
                    <thead class="bg-danger">
                        <tr>
                            <th>Producto</th>
                            <th>U/M Venta</th>
                            <th>Cantidad</th>
                            <th>Precio Uni</th>
                            <th>Descuento %</th>
                            <th class="text-right">Importe</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="de in arrayDetalle" :key="de.id">
                            <td>{{ de.producto }}</td>
                            <td>{{ de.umVenta }}</td>
                            <td>{{ de.cantidad }}</td>
                            <td>{{ de.precio }}</td>
                            <td>{{ de.descuento }} %</td>
                            <td class="text-right">{{ formattedTotal(de.importe) }}</td>
                        </tr>
                    </tbody>
                    <tfoot class="">
                        <tr>
                            <td colspan="3"></td>
                            <th>Subtotal: {{subtotal}}</th>
                            <th>IGV: {{igv}}</th>
                            <th class="text-right">IMPORTE TOTAL: <h3>{{formattedTotal(Number(subtotal) + Number(igv))}}</h3></th>
                        </tr>
                    </tfoot>
                </table>
              </div>
          </div>
      </div><!-- /.card -->
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
        data(){
            return{
                idVenta:'',
                arrayPedido: [],
                arrayDetalle: [],
                cliente:'',
                comprobante:'',
                numPedido:'',
                fechaPedido:'',
                idComprob:'',
                fecha:'',
                serieNumero:'',
                metodoPago:'',
                vendedor:'',
                //motivo:'',
                subtotal:'',
                igv:'',
                moneda:'',
                idPedido:'',

                arrayCodigoNC:[],
                tipoNota:0,
                motivo:'',
                errorGenerar:0,
                arrayMostMsjGenerar:[],
            }
        },
        computed:{
            id(){
                return this.$route.params.id
            }
        },
        methods:{
            listarVenta(){
            let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apiventa/ventas/${me.idVenta}/`)
              .then(function(response){console.log(response.data)
                  if(response.data){
                    me.cliente = response.data.cliente
                    me.idPedido = response.data.idPedido
                    me.comprobante = response.data.comprobanteobservacion
                    me.fechaPedido = response.data.fechaPedido
                    me.fecha = response.data.fecha
                    me.idComprob = response.data.tipComprobante
                    me.metodoPago = response.data.metodoPago
                    me.serieNumero = response.data.serie+'-'+response.data.numComprobante
                    me.vendedor = response.data.vendedor
                    me.ventactivo = response.data.activo
                    //me.motivo = response.data.observacion
                    me.numPedido = response.data.numPedido
                    me.comprobante = response.data.comprobante
                    me.subtotal = response.data.subtotal
                    me.igv = response.data.igv_total
                    me.moneda = response.data.moneda
                    me.listarDetalle()
                  }else{me.$toastr.info('No se encontraron datos','Sin registro');me.limpiar()}
              })
          },
          validarNota(){
            this.errorGenerar = 0
            this.arrayMostMsjGenerar = []
            if(!this.motivo) this.arrayMostMsjGenerar.push("Describa el motivo de la anulacion")
            if(!this.tipoNota) this.arrayMostMsjGenerar.push("Seleccione el tipo de nota de credito")
            if(this.arrayMostMsjGenerar.length) this.errorGenerar = 1
            return this.errorGenerar
          },
          listarDetalle(){
            let me = this
            this.$axios.get(`${process.env.VUE_APP_API_URL}/apiventa/detalle/?idPedido=${me.idPedido}`)
              .then(function(response){
                  me.arrayDetalle = response.data
              })
          },
          listarCodigNotaCre(){
            let me = this
            this.$axios.get(`${process.env.VUE_APP_API_URL}/apisunat/codigonotacredito`)
              .then(function(response){
                  me.arrayCodigoNC = response.data
              })
          },
          grabarNota(){
            if(this.validarNota()){
                this.arrayMostMsjGenerar.forEach(element => {
                this.$toastr.error(element,'Atencion!')
                });
                return
            }
            let me = this
            this.$swal.fire({
            title: 'Crear Nota de Crédito',
            text: "Esta seguro?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si, crear'
            }).then((result) => {
                if (result.isConfirmed) {
                this.$axios.post(`${process.env.VUE_APP_API_URL}/apiventa/notacredito/`, { //URL GRABAR NOTA DE CREDITO
                    subtotal: me.subtotal,
                    igv: me.igv,
                    motivo: me.motivo,
                    idVenta: me.idVenta,
                    idPedido: me.idPedido,
                    codigoNC: me.tipoNota,
                    serieNumeroAnu: me.serieNumero
                }).
                then((response)=>{
                    console.log(response.data)
                    me.$router.push('/ventas/notacredito')
                    me.$toastr.success('Nota de credito generado', 'Excelente!')
                }).
                catch((error)=>{
                    console.error(error)
                    me.$toastr.error('Error al generar NC', 'Error');
                })
                }
            })
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
        mounted(){
            this.idVenta = this.id
            this.listarVenta()
            this.listarCodigNotaCre()
        }
    }
</script>