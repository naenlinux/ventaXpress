<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Nota de crédito</h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item active">Nota de crédito</li>
          </ol>
        </div><!-- /.col -->
      </div><!-- /.row -->
    </div><!-- /.container-fluid -->
  </div>
  <!-- /.content-header -->

  <div class="card card-primary card-outline">
      <div class="card-body">
          <div class="row">
            <div class="offset-md-6 col-sm-6">
                <div class="input-group" @keyup.enter="listarNotaCredito(1,serieBuscar, numBuscar)">
                    <div class="input-group-append">
                        <button type="button" class="btn btn-md btn-default">
                        Serie
                        </button>
                    </div>
                    <input type="text" v-model="serieBuscar" class="form-control form-control-md" placeholder="BC01">
                    <div class="input-group-append">
                        <button type="button" class="btn btn-md btn-default">
                        Numero
                        </button>
                    </div>
                    <input type="text" v-model="numBuscar" class="form-control form-control-md" placeholder="1">
                    <div class="input-group-append">
                        <button type="button" class="btn btn-md btn-info" @click="listarNotaCredito(1,serieBuscar,numBuscar)">
                            <i class="fa fa-search"></i> Buscar
                        </button>
                    </div>
                </div>
            </div>
          </div>
          <br>
          <div class="table-responsive">
              <table class="table table-bordered table-sm table-striped">
                  <thead class="bg-warning">
                      <tr>
                          <th>#</th>
                          <th>Nota Credito</th>
                          <th>Fecha NC</th>
                          <th>Motivo</th>
                          <th>Comprob anulado</th>
                          <th>Subtotal</th>
                          <th>IGV</th>
                          <th class="text-right">S/ Total</th>
                          <th class="text-center">XML</th>
                          <th class="text-center">SUNAT</th>
                      </tr>
                  </thead>
                  <tbody>
                     <tr v-for="(not, index) in arrayNotas" :key="not.id">
                        <td>{{index+1}}</td>
                        <td>{{not.serie+'-'+not.numComprobante}}</td>
                        <td>{{ fechaFormateada(not.fecha) }}</td>
                        <td>{{not.motivo}}</td>
                        <td>{{ not.serieAnulado+'-'+not.numeroAnulado}}</td>
                        <td>{{ not.subtotal }}</td>
                        <td>{{ not.igv }}</td>
                        <td class="text-right">{{formattedTotal(Number(not.subtotal) + Number(not.igv)) }}</td>
                        <td class="text-center">
                            <button v-if="not.nombre_xmlzip" class="btn btn-sm btn-success tooltip-btn btn-flat" data-tooltip="Descargar" @click="descargarxmlNC(not.nombre_xmlzip)">XML <i class="fas fa-file"></i></button>
                            <button v-else class="btn btn-sm btn-danger btn-flat" @click="generarxmlNC(not.id)">Generar</button>
                        </td>
                        <td class="text-center">
                            <button v-if="not.nombre_cdr" class="btn btn-sm btn-primary tooltip-btn btn-flat" data-tooltip="Descargar" @click="descargar_cdr(not.nombre_cdr)">CDR <i class="fas fa-file"></i></button>
                            <button v-else class="btn btn-sm btn-danger btn-flat" @click="enviarSunat(not.nombre_xmlzip)">Enviar</button>
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
            arrayNotas: [],
                        
            serieBuscar:'',
            numBuscar:'',
            fechaBuscar:'',
            
            currentPage: 1,
            totalPages: 0,
            listporPage: 15,
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
              this.listarNotaCredito(pageNumber,'','');
          },
          goToPreviousPage() {
              if (this.currentPage > 1) {
                  this.currentPage -= 1;
                  this.listarNotaCredito(this.currentPage,'','');
              }
          },
          goToNextPage() {
              if (this.currentPage < this.totalPages) {
                  this.currentPage += 1;
                  this.listarNotaCredito(this.currentPage,'','');
              }
          },
          goToFirstPage() {
              if (this.currentPage !== 1) {
                  this.currentPage = 1;
                  this.listarNotaCredito(this.currentPage,'','');
              }
          },
          goToLastPage() {
              if (this.currentPage !== this.totalPages) {
                  this.currentPage = this.totalPages;
                  this.listarNotaCredito(this.currentPage,'','');
              }
          },
          formattedTotal(amount) {
            return new Intl.NumberFormat('es-PE', {
            style: 'currency',
            currency: 'PEN',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
            }).format(amount);
          },
          listarNotaCredito(pageNumber = 1, serieBuscar, numBuscar){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apiventa/notacredito/?page=${pageNumber}&serieNumero=${serieBuscar+'-'+numBuscar}`)
              .then(function(response){
                  me.arrayNotas = response.data.results
                  me.currentPage = pageNumber
                  me.totalPages = Math.ceil(response.data.count / me.listporPage)
                  me.totalRegistros = response.data.count
              })
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
        generarxmlNC(id){
            let me = this
            me.$axios.get(`${process.env.VUE_APP_API_URL}/apisunat/generarxmlnc/?id_notac=${id}&generar_xmlnc=1`)
            .then(function (response) {
                console.log(response.data)
                me.listarNotaCredito(me.currentPage, me.serieBuscar, me.numBuscar)
                if(response.data.message == 'success') me.$toastr.success(response.data.mensaje,'Excelente')
                else me.$toastr.error(response.data.mensaje,'Error')
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        descargarxmlNC(nombre_zip){
            let me = this
            me.$axios.get(`${process.env.VUE_APP_API_URL}/apisunat/generarxmlnc/?nombre_zip=${nombre_zip}`,{
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
                me.listarNotaCredito(me.currentPage, me.serieBuscar, me.numBuscar)
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
          this.listarNotaCredito(1,'','')
          this.updateVisiblePages();
          this.$socket.onmessage = (event)=>{
            console.log(event.data)
            var dataObject = JSON.parse(event.data)
            this.listarNotaCredito( 1, this.serieBuscar, this.numBuscar)
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