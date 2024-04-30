<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Comprobantes</h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item active">Comprobantes</li>
          </ol>
        </div><!-- /.col -->
      </div><!-- /.row -->
    </div><!-- /.container-fluid -->
  </div>
  <!-- /.content-header -->

  <div class="row">
    <div class="col-md-6">
         <!-- tipo comprobante -->
         <div class="card card-info">
              <div class="card-header">
                <h3 class="card-title">Tipo de comprobantes</h3>
              </div>
                <div class="card-body">
                    <div class="mb-2">
                    <button type="button" class="btn btn-success btn-sm" @click="abrirModal('registrar')">Nuevo</button>
                </div>
                  <div class="table-responsive">
                  <table class="table table-sm table-bordered">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Codigo Sunat</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="t in arrayTipo" :key="t.id">
                            <td v-text="t.nombre"></td>
                            <td v-text="t.codigoSunat"></td>
                            <td>
                                <span v-if="t.activo" class="badge badge-success">Activado</span>
                                <span v-else class="badge badge-danger">Eliminado</span>
                                <button class="btn btn-sm btn-warning ml-2" @click="abrirModal('actualizar', t)"><i class="fas fa-edit"></i></button>&nbsp;
                                <button v-if="t.activo" class="btn btn-sm btn-danger" @click="eliminarTipo(t.id,t.nombre,t.activo)"><i class="fas fa-trash-alt"></i></button>
                                <button v-else class="btn btn-sm btn-success" @click="eliminarTipo(t.id,t.nombre,t.activo)"><i class="fas fa-trash-restore-alt"></i></button>
                            </td>
                        </tr>
                    </tbody>
                  </table>
                  </div>
                </div>
            </div>
            <!-- /.tipo comprobante -->
            <!-- tipo enviar sunat -->
         <div class="card card-info">
            <div class="card-header">
              <h3 class="card-title">Envio de comprobantes a Sunat</h3>
            </div>
              <div class="card-body">
                <div class="form-group">
                    <div class="custom-control custom-switch">
                      <input type="checkbox" class="custom-control-input" id="customSwitch1" v-model="envioSunat" @change="actualizarEnvio">
                      <label class="custom-control-label" for="customSwitch1">Enviar los comprobantes a SUNAT al momento de cobrar</label>
                    </div>
                  </div>    
              </div>
          </div>
          <!-- /.tipo enviar sunat -->
    </div>
    <!-- logo -->
    <div class="col-md-6">
          <!-- tipo serie -->
          <div class="card card-info">
              <div class="card-header">
                <h3 class="card-title">Serie Numerador</h3>
              </div>
              <div class="card-body">
                <div class="mb-2">
                    <button type="button" class="btn btn-success btn-sm" @click="abrirModalSerie('registrar')">Nuevo</button>
                </div>
                <div class="table-responsive">
                  <table class="table table-sm table-bordered">
                    <thead>
                        <tr>
                            <th>Comprobante</th>
                            <th>Serie</th>
                            <th>Numerador</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="s in arraySerie" :key="s.id">
                            <td>
                                <div v-for="t in arrayTipo" :key="t.id">
                                    <div v-if="t.id == s.tipocomprobante">
                                        {{ nom = t.nombre }}
                                    </div>
                                </div>
                            </td>
                            <td v-text="s.serie"></td>
                            <td v-text="s.numerocont"></td>
                            <td>
                                <span v-if="s.activo" class="badge badge-success">Activado</span>
                                <span v-else class="badge badge-danger">Eliminado</span>
                                <button class="btn btn-sm btn-warning ml-2" @click="abrirModalSerie('actualizar', s)"><i class="fas fa-edit"></i></button>&nbsp;
                                <button v-if="s.activo" class="btn btn-sm btn-danger" @click="eliminarSerie(s.id,nom,s.activo)"><i class="fas fa-trash-alt"></i></button>
                                <button v-else class="btn btn-sm btn-success" @click="eliminarSerie(s.id,nom,s.activo)"><i class="fas fa-trash-restore-alt"></i></button>
                            </td>
                        </tr>
                    </tbody>
                  </table>
                 </div>
                </div>
            </div>
            <!-- /.serie -->
    </div>
    <!-- /logo -->

      <!--- MODAL TIPO COMP --->
      <div v-if="showModal">
      <div class="modal">
          <div class="modal-overlay"></div>
              <div class="modal-content" v-on:keyup.enter = "tipoAccion==1?registrarTipo():actualizarTipo()">
                  <div class="modal-header bg-primary text-white">
                      <h4>{{tituloModal}}</h4>
                      <button type="button" class="close" @click="cerrarModal()">&times;</button>
                  </div>
                  <div class="modal-body">
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Nombre: *</label>
                          <div class="col-sm-9">
                              <input type="text" class="form-control" v-model="nombre" placeholder="Nombre del comprobante">
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Código Sunat:</label>
                          <div class="col-sm-9">
                              <input type="text" class="form-control" v-model="codigoSunat" placeholder="Código sunat">
                          </div>
                      </div>
                  </div>
                  <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" @click="cerrarModal()">Cerrar</button>
                      <button type="button" v-if="tipoAccion==1" class="btn btn-primary" @click="registrarTipo()">GUARDAR</button>
                      <button type="button" v-if="tipoAccion==2" class="btn btn-primary" @click="actualizarTipo()">ACTUALIZAR</button>
                  </div>
              </div>
          </div>
          
      </div>
  <!--- FIN MODAL TIPO COMP --->

        <!--- MODAL SERIE --->
        <div v-if="showModalSerie">
      <div class="modal">
          <div class="modal-overlay"></div>
              <div class="modal-content" v-on:keyup.enter = "tipoAccion==1?registrarSerie():actualizarSerie()">
                  <div class="modal-header bg-primary text-white">
                      <h4>{{tituloModal}}</h4>
                      <button type="button" class="close" @click="cerrarModalSerie()">&times;</button>
                  </div>
                  <div class="modal-body">
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Comprobante:</label>
                          <div class="col-sm-9">
                          <select v-model="tipocomprobante" class="form-control">
                            <option :value="0"> ==== Seleccione ===</option>
                            <option v-for="tip in arrayTipo" :key="tip.id" :value="tip.id">{{ tip.nombre }}</option>
                          </select>
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Serie:</label>
                          <div class="col-sm-9">
                              <input type="text" class="form-control" v-model="serie" placeholder="A001">
                          </div>
                      </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Número:</label>
                          <div class="col-sm-9">
                              <input type="number" class="form-control" v-model="numerocont" placeholder="0">
                          </div>
                      </div>
                  </div>
                  <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" @click="cerrarModalSerie()">Cerrar</button>
                      <button type="button" v-if="tipoAccion==1" class="btn btn-primary" @click="registrarSerie()">GUARDAR</button>
                      <button type="button" v-if="tipoAccion==2" class="btn btn-primary" @click="actualizarSerie()">ACTUALIZAR</button>
                  </div>
              </div>
          </div>
          
      </div>
  <!--- FIN MODAL SERIE --->
  </div>
</template>

<script>
    export default{   
        data(){
            return{
                idtipo:'',
                nombre:'',
                codigoSunat:'',
                activotipo:'',
                arrayTipo:[],

                idserie:'',
                tipocomprobante:0,
                serie:'',
                numerocont:'',
                activo:'',
                arraySerie:[],
                envioSunat:'',
                envioSunatId:'',
                
                errorTipo:0,
                errorSerie:0,
                arrayMostMsj:[],

                showModal:false,
                showModalSerie:false,
                errorSaveUpdate:[],
            }
        },
      computed: {
        
      },
      methods:{          
          listarTipo(){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/tipocomprobante/`)
              .then(function(response){
                if(response.data.length){
                    me.arrayTipo = response.data
                }
              })
          },
          listarEnviarSunat(){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/enviarsunat/`)
              .then(function(response){
                if(response.data.length){
                    me.envioSunat = response.data[0].valor
                    me.envioSunatId = response.data[0].id
                }
              })
          },
          actualizarEnvio(){
            let me = this
              this.$axios.put(`${process.env.VUE_APP_API_URL}/apiempresa/enviarsunat/`+me.envioSunatId+`/`,{
                valor: me.envioSunat
              })
              .then(function(response){
                console.log(response)
                if(me.envioSunat){
                    me.$toastr.success('Enviar Sunat', 'Activado');
                }else{
                    me.$toastr.error('Enviar Sunat', 'Desactivado');
                }
              })
          },
          validarTipo(){
              this.errorTipo = 0
              this.arrayMostMsj = []
              if(!this.nombre.trim()) this.arrayMostMsj.push("Ingrese nombre de comprobante")
              if(this.arrayMostMsj.length) this.errorTipo = 1
              return this.errorTipo
          },
          registrarTipo(){
            if(this.validarTipo()){
                this.arrayMostMsj.forEach(element => {
                  this.$toastr.error(element,'Atencion!')
              });
              return
            }
            let me = this
            this.$axios.post(`${process.env.VUE_APP_API_URL}/apiempresa/tipocomprobante/`, {
                nombre: me.nombre.trim(),
                codigoSunat: me.codigoSunat.trim(),
            })
            .then(function (response) {
                me.listarTipo()
                console.log(response)
                me.cerrarModal()
                me.$toastr.success('Comprobante registrado', 'Registrado');
            })
          },
          actualizarTipo(){
              if(this.validarTipo()){
                  this.arrayMostMsj.forEach(element => {
                      this.$toastr.error(element,'Atencion!')
                  });
                  return
              }
              let me = this
              this.$axios.put(`${process.env.VUE_APP_API_URL}/apiempresa/tipocomprobante/`+me.id+`/`,{
                  nombre: me.nombre.trim(),
                  codigoSunat: me.codigoSunat.trim(),
              })
              .then(function(response){
                  console.log(response)
                  me.listarTipo()
                  me.cerrarModal()
                  me.$toastr.success('Comprobante actualizado', 'Actualizado');
              })
          },
          eliminarTipo(id,nombre,activo){
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
                  this.$axios.put(`${process.env.VUE_APP_API_URL}/apiempresa/tipocomprobante/`+id+`/`,{
                      activo : activo ?  0 : 1,
                  })
                  .then(function(response){
                      console.log(response)
                      me.listarTipo()
                      me.cerrarModal()
                      if(activo){me.$toastr.success('Comprobante deshabilitado', 'Desactivado')}
                      else{me.$toastr.success('Comprobante Habilitado', 'Habilitado')}
                  })
              }
              })
          },
          abrirModal(action, data=[]){
              switch(action){
                  case "registrar":{
                      this.showModal = true
                      this.tituloModal = "Nuevo tipo comprobante"
                      this.tipoAccion = 1
                      break
                  }
                  case "actualizar":{
                      this.showModal = true
                      this.tituloModal = "Editar tipo comprobante"
                      this.id = data['id']
                      this.nombre = data['nombre']
                      this.codigoSunat = data['codigoSunat']
                      this.tipoAccion = 2
                      break
                  }
              }                
          },
          cerrarModal(){
              this.showModal = false;
              this.id = ''
              this.nombre = ''
              this.codigoSunat = ''
          },
          //=========FIN DE COMPROBANTES=============//

          // ============= codigo DE SERIE NUMERADOR===========//
          listarSerie(){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/comprobanteconfig/`)
              .then(function(response){
                if(response.data.length){
                    me.arraySerie = response.data
                }
              })
          },
          validarSerie(){
              this.errorSerie = 0
              this.arrayMostMsj = []
              if(!this.tipocomprobante) this.arrayMostMsj.push("Seleccione un comprobante")
              if(!this.serie.trim()) this.arrayMostMsj.push("Ingrese el numero de serie")
              if(!this.numerocont) this.arrayMostMsj.push("Ingrese un numero al contador")
              if(this.arrayMostMsj.length) this.errorSerie = 1
              return this.errorSerie
          },
          registrarSerie(){
            if(this.validarSerie()){
                this.arrayMostMsj.forEach(element => {
                  this.$toastr.error(element,'Atencion!')
              });
              return
            }
            let me = this
            this.$axios.post(`${process.env.VUE_APP_API_URL}/apiempresa/comprobanteconfig/`, {
                tipocomprobante: me.tipocomprobante,
                serie: me.serie.trim(),
                numerocont: me.numerocont,
            })
            .then(function (response) {
                me.listarSerie()
                console.log(response)
                me.cerrarModalSerie()
                me.$toastr.success('Comprobante configurado', 'Exito');
            })
            .catch(function (error) {
                if(error.response && error.response.data){
                    if(error.response.data.tipocomprobante){me.errorSaveUpdate.push(error.response.data.tipocomprobante[0])}
                }
                if(me.errorSaveUpdate.length > 0){
                    me.errorSaveUpdate.forEach(element => {
                        me.$toastr.error(element,'Error')
                    });
                }
                me.errorSaveUpdate = []          
            }) 
          },
          actualizarSerie(){
              if(this.validarSerie()){
                  this.arrayMostMsj.forEach(element => {
                      this.$toastr.error(element,'Atencion!')
                  });
                  return
              }
              let me = this
              this.$axios.put(`${process.env.VUE_APP_API_URL}/apiempresa/comprobanteconfig/`+me.id+`/`,{
                  tipocomprobante: me.tipocomprobante,
                  serie: me.serie.trim(),
                  numerocont: me.numerocont,
              })
              .then(function(response){
                  console.log(response)
                  me.listarSerie()
                  me.cerrarModalSerie()
                  me.$toastr.success('Configuracion actualizado', 'Actualizado');
              })
              .catch(function (error) {
                if(error.response && error.response.data){
                    if(error.response.data.tipocomprobante){me.errorSaveUpdate.push(error.response.data.tipocomprobante[0])}
                }
                if(me.errorSaveUpdate.length > 0){
                    me.errorSaveUpdate.forEach(element => {
                        me.$toastr.error(element,'Error')
                    });
                }
                me.errorSaveUpdate = []          
               }) 
          },
          eliminarSerie(id,nombre,activo){
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
                  this.$axios.put(`${process.env.VUE_APP_API_URL}/apiempresa/comprobanteconfig/`+id+`/`,{
                      activo : activo ?  0 : 1,
                  })
                  .then(function(response){
                      console.log(response)
                      me.listarSerie()
                      me.cerrarModalSerie()
                      if(activo){me.$toastr.success('Comprobante deshabilitado', 'Desactivado')}
                      else{me.$toastr.success('Comprobante Habilitado', 'Habilitado')}
                  })
              }
              })
          },
          abrirModalSerie(action, data=[]){
              switch(action){
                  case "registrar":{
                      this.showModalSerie = true
                      this.tituloModal = "Nuevo comprobante - serie"
                      this.tipoAccion = 1
                      break
                  }
                  case "actualizar":{
                      this.showModalSerie = true
                      this.tituloModal = "Editar comprobante - serie"
                      this.id = data['id']
                      this.tipocomprobante = data['tipocomprobante']
                      this.serie = data['serie']
                      this.numerocont = data['numerocont']
                      this.tipoAccion = 2
                      break
                  }
              }                
          },
          cerrarModalSerie(){
              this.showModalSerie = false;
              this.id = ''
              this.tipocomprobante = 0
              this.serie = ''
              this.numerocont=''
          },
      },
      watch: {
      },
      mounted(){
          this.listarTipo()
          this.listarSerie()
          this.listarEnviarSunat()
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