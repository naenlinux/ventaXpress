<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Reporte de ventas</h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item active">Reporte Ventas</li>
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
              <button class="btn btn-success btn-flat" @click="exportarExcel()">Excel</button>
            </div>
            <div class="col-sm-6">
                <div class="input-group" @keyup.enter="listarVentas(fini, ffin)">
                    <div class="input-group-append">
                        <button type="button" class="btn btn-md btn-default">
                        De fecha
                        </button>
                    </div>
                    <input type="date" v-model="fini" class="form-control form-control-md" >
                    <div class="input-group-append">
                        <button type="button" class="btn btn-md btn-default">
                        A fecha
                        </button>
                    </div>
                    <input type="date" v-model="ffin" class="form-control form-control-md" >
                    <div class="input-group-append">
                        <button type="button" class="btn btn-md btn-info" @click="listarVentas(fini,ffin)">
                            <i class="fa fa-search"></i> Buscar
                        </button>
                    </div>
                </div>
            </div>
          </div>
          <br>
          <div class="table-responsive">
              <table class="table table-bordered table-sm table-striped">
                  <thead class="bg-primary">
                      <tr>
                          <th>#</th>
                          <th>Estado</th>
                          <th class="text-center">Ver</th>
                          <th>Comprobante</th>
                          <th>Número</th>
                          <th>Fecha de venta</th>
                          <th>Sucursal</th>
                          <th class="text-center">N° Pedido</th>
                          <th class="text-right">S/ Total Venta</th>
                          
                          <th class="text-center">XML ZIP</th>
                          <th class="text-center">SUNAT</th>
                      </tr>
                  </thead>
                  <tbody>
                     <tr v-for="(ve, index) in arrayVentas" :key="ve.id">
                        <td>{{index+1}}</td>
                        <td class="text-center" :class="ve.activo==2 ? 'text-danger' : 'text-success'" >
                            <div v-if="ve.activo==1"><strong>Activo</strong></div>
                            <div v-if="ve.activo==2"><strong>NC Anulado</strong></div>
                        </td>
                        <td class="text-center"><button class="btn btn-sm btn-info btn-flat" @click="verDetalle(ve.id)"><i class="fas fa-eye"></i></button></td>
                        <td>{{ ve.comprobante }}</td>
                        <td>{{ ve.serie+'-'+ve.numComprobante }}</td>
                        <td>{{ fechaFormateada(ve.fecha) }}</td>
                        <td>{{ve.sucursal}}</td>
                        <td class="text-center">{{ ve.numPedido }}</td>
                        <td class="text-right">{{formattedTotal(Number(ve.subtotal) + Number(ve.igv_total)) }}</td>
                        <td class="text-center">
                            <button v-if="ve.nombre_xmlzip" class="btn btn-sm btn-success tooltip-btn btn-flat" data-tooltip="Descargar" @click="descargar_xml(ve.nombre_xmlzip)">XML <i class="fas fa-file"></i></button>
                            <button v-else class="btn btn-sm btn-danger btn-flat" @click="generar_xml(ve.id)">Generar</button>
                        </td>
                        <td class="text-center">
                            <button v-if="ve.nombre_cdr" class="btn btn-sm btn-primary tooltip-btn btn-flat" data-tooltip="Descargar" @click="descargar_cdr(ve.nombre_cdr)">CDR <i class="fas fa-file"></i></button>
                            <button v-else class="btn btn-sm btn-danger btn-flat" @click="enviarSunat(ve.nombre_xmlzip)">Enviar</button>
                        </td>
                     </tr>
                  </tbody>
              </table>
              <br>
              <table class="table border">
                <tbody>
                <tr>
                
                    <td>Ventas {{formattedTotal(sumaTotal)}}</td>
                    <td>Notas de Cred: {{formattedTotal(sumaTotalNC)}}</td>
                    <th>TOTAL DE VENTAS {{formattedTotal(sumaTotal-sumaTotalNC)}}</th>
                    
                </tr>
                
                </tbody>
                      
              </table>
          </div>
           <!-- Agrega el paginador aquí -->
          
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
            arrayVentas: [],
                        
            fini:'',
            ffin:'',
            ventas:'',
            ncreditos:'',
            
            currentPage: 1,
            totalPages: 0,
            listporPage: 15,
            visiblePages: [], // Páginas visibles en el paginado
            totalPagesToShow: 5, // Cantidad de páginas visibles en el paginado
            totalRegistros:0,

          }
      },
      computed: {
         sumaTotal(){
          return this.arrayVentas.reduce((subtotal, item) => subtotal + Number(item.subtotal),0)
         },
         sumaTotalNC(){
          return this.arrayVentas.filter(item => item.activo === 2).reduce((subtotal, item) => subtotal + Number(item.subtotal),0)
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
          listarVentas(fini, ffin){
            if(fini != '' && ffin != ''){
                let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apiventa/reporteventas/?fini=${fini}&ffin=${ffin}`)
              .then(function(response){
                  me.arrayVentas = response.data.results
                  if(me.arrayVentas.length < 1){me.$toastr.info('No se halló resultados', 'Intente con otra fecha')}
              })
            }else{
                this.$toastr.error('Campos de fechas vacios', 'Error!')
            }
              
          },
          
          verDetalle(id){
            this.$router.push({path: `/ventas/detalle/${id}`})
          },
    
        fechaFormateada(fecha) {
        // Separar la fecha en partes (año, mes, día)
        const partes = fecha.split('-');

        // Crear una nueva cadena en el formato deseado
        return `${partes[2]}/${partes[1]}/${partes[0]}`;
        },
        horaFormateada(hora) {
        // Dividir la hora en partes usando ":" como separador
        const partes = hora.split(':');

        // Tomar las dos primeras partes (horas y minutos)
        const horas = partes[0];
        const minutos = partes[1];

        // Crear una cadena en el formato 'hh:mm'
        return `${horas}:${minutos}`;
        },
        generar_xml(id){
            let me = this
            me.$axios.get(`${process.env.VUE_APP_API_URL}/apisunat/generarxml/?id_venta=${id}&generar_xml=1`)
            .then(function (response) {
                console.log(response.data)
                me.listarVentas(me.currentPage, me.serieBuscar, me.numBuscar)
                if(response.data.message == 'success') me.$toastr.success(response.data.mensaje,'Excelente')
                else me.$toastr.error(response.data.mensaje,'Error')
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        descargar_xml(nombre_zip){
            let me = this
            me.$axios.get(`${process.env.VUE_APP_API_URL}/apisunat/generarxml/?nombre_zip=${nombre_zip}`,{
                responseType: 'blob'
            })
            .then(function (response) {
                console.log(response)
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', nombre_zip);
                document.body.appendChild(link);
                link.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        enviarSunat(nombre_xmlzip){
            if(!nombre_xmlzip){this.$toastr.error('no existe el XML','Error'); return}
            let me = this
            me.$axios.get(`${process.env.VUE_APP_API_URL}/apisunat/enviarsunatxml/?nombre_xmlzip=${nombre_xmlzip}&enviar_sunat=1`)
            .then(function (response) {
                //console.log(response.data.message)
                me.listarVentas(me.currentPage, me.serieBuscar, me.numBuscar)
                if(response.data.message == 'success') me.$toastr.success(response.data.mensaje,'Excelente')
                else me.$toastr.error(response.data.mensaje,'Error')
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        descargar_cdr(nombre_cdr){
            let me = this
            me.$axios.get(`${process.env.VUE_APP_API_URL}/apisunat/enviarsunatxml/?nombre_cdr=${nombre_cdr}`,{
                responseType: 'blob'
            })
            .then(function (response) {
                console.log(response)
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', nombre_cdr);
                document.body.appendChild(link);
                link.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        exportarExcel(){
          if(this.arrayVentas.length > 0){
            window.open(`${process.env.VUE_APP_API_URL}/impresiones/reporteventas/`+this.fini+`/`+this.ffin, '_blank')
          }else{
            this.$toastr.error('No hay registros a exportar', 'Error!')
          }
        },
      },
      watch: {
          
      },
      mounted(){
          
          this.$socket.onmessage = (event)=>{
            console.log(event.data)
            var dataObject = JSON.parse(event.data)
            this.listarVentas( 1, this.serieBuscar, this.numBuscar)
            if(dataObject.message == 'nueva venta'){this.$toastr.success('Venta agregado','Nueva Venta')}
          }
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
  padding: 1px 5px;
  
  white-space: nowrap;
  border-radius: 4px;
  top: -15px; /* Ajusta la posición vertical según tus necesidades */
  left: 80%;
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