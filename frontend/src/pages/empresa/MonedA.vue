<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
        <div class="container-fluid">
            <div class="row mb-2">
                <div class="col-sm-6">
                    <h1 class="m-0">Sucursal - Moneda e IGV</h1>
                </div><!-- /.col -->
                <div class="col-sm-6">
                    <ol class="breadcrumb float-sm-right">
                        <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
                        <li class="breadcrumb-item active">Moneda</li>
                    </ol>
                </div><!-- /.col -->
            </div><!-- /.row -->
        </div><!-- /.container-fluid -->
  </div>
  <!-- /.content-header -->

    <div class="row">
        <div class="col-md-6">
            <!-- Sucursales -->
            <div class="card card-success">
                <div class="card-header">
                    <h3 class="card-title">Sucursales</h3>
                </div>
                <div class="card-body">
                    <div class="mb-2">
                        <button type="button" class="btn btn-success btn-sm" @click="abrirModalSucursal('registrar')">Nuevo</button>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-sm table-bordered">
                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Direccion</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="s in arraySucursal" :key="s.id">
                                <td v-text="s.nombre"></td>
                                <td v-text="s.direccion"></td>
                                <td>
                                    <button class="btn btn-sm btn-warning ml-2" @click="abrirModalSucursal('actualizar', s)"><i class="fas fa-edit"></i></button>&nbsp;
                                    <button v-if="s.activo" class="btn btn-sm btn-danger" @click="eliminarSucursal(s.id,s.nombre,s.activo)"><i class="fas fa-trash-alt"></i></button>
                                    <button v-else class="btn btn-sm btn-success" @click="eliminarSucursal(s.id,s.nombre,s.activo)"><i class="fas fa-trash-restore-alt"></i></button>&nbsp;
                                    <span v-if="s.activo" class="badge badge-success">Habilitad</span>
                                    <span v-else class="badge badge-danger">Anulado</span>
                                </td>
                            </tr>
                        </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <!-- Sucursales -->
        </div>
        <!--- MODAL SUCURSAL --->
        <div v-if="showModalSuc">
            <div class="modal">
                <div class="modal-overlay"></div>
                    <div class="modal-content" v-on:keyup.enter = "tipoAccion==1?registrarSucursal():actualizarSucursal()">
                        <div class="modal-header bg-primary text-white">
                            <h4>{{tituloModal}}</h4>
                            <button type="button" class="close" @click="cerrarModal()">&times;</button>
                        </div>
                        <div class="modal-body">
                            <div class="mb-3 row">
                                <label for="" class="col-sm-3 col-form-label">Nombre: *</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" v-model="nombreSucur" placeholder="Local 001">
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label for="" class="col-sm-3 col-form-label">Dirección:</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" v-model="direccion" placeholder="Calle...">
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" @click="cerrarModal()">Cerrar</button>
                            <button type="button" v-if="tipoAccion==1" class="btn btn-primary" @click="registrarSucursal()">GUARDAR</button>
                            <button type="button" v-if="tipoAccion==2" class="btn btn-primary" @click="actualizarSucursal()">ACTUALIZAR</button>
                        </div>
                    </div>
                </div>
                
            </div>
            <!--- FIN MODAL SUCURSAL --->
        <!--- MODAL MONEDA --->
        <div v-if="showModal">
        <div class="modal">
            <div class="modal-overlay"></div>
                <div class="modal-content" v-on:keyup.enter = "tipoAccion==1?registrarMoneda():actualizarMoneda()">
                    <div class="modal-header bg-primary text-white">
                        <h4>{{tituloModal}}</h4>
                        <button type="button" class="close" @click="cerrarModal()">&times;</button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3 row">
                            <label for="" class="col-sm-3 col-form-label">Nombre: *</label>
                            <div class="col-sm-9">
                                <input type="text" class="form-control" v-model="nombre" placeholder="Nombre de la moneda">
                            </div>
                        </div>
                        <div class="mb-3 row">
                            <label for="" class="col-sm-3 col-form-label">Código:</label>
                            <div class="col-sm-9">
                                <input type="text" class="form-control" v-model="codigo" placeholder="PEN, USD, etc">
                            </div>
                        </div>
                        <div class="mb-3 row">
                            <label for="" class="col-sm-3 col-form-label">Símbolo:</label>
                            <div class="col-sm-9">
                                <input type="text" class="form-control" v-model="simbolo" placeholder="S/ $">
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="cerrarModal()">Cerrar</button>
                        <button type="button" v-if="tipoAccion==1" class="btn btn-primary" @click="registrarMoneda()">GUARDAR</button>
                        <button type="button" v-if="tipoAccion==2" class="btn btn-primary" @click="actualizarMoneda()">ACTUALIZAR</button>
                    </div>
                </div>
            </div>
            
        </div>
        <!--- FIN MODAL MONEDA --->

        <div class="col-md-6">
            <div class="card card-info">
                <div class="card-header">
                    <h3 class="card-title">Tipo de monedas</h3>
                </div>
              <!-- /.card-header -->
              <!-- form start -->
                
                <div class="card-body">
                    <div class="mb-2">
                        <button type="button" class="btn btn-success btn-sm" @click="abrirModal('registrar')">Nuevo</button>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-sm table-bordered">
                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Código</th>
                                <th>Simbolo</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="m in arrayMoneda" :key="m.id">
                                <td v-text="m.nombre"></td>
                                <td v-text="m.codigo"></td>
                                <td v-text="m.simbolo"></td>
                                <td>
                                    <span v-if="m.activo" class="badge badge-success">Habilitad</span>
                                    <span v-else class="badge badge-danger">Anulado</span>
                                    <button class="btn btn-sm btn-warning ml-2" @click="abrirModal('actualizar', m)"><i class="fas fa-edit"></i></button>&nbsp;
                                    <button v-if="m.activo" class="btn btn-sm btn-danger" @click="eliminarMoneda(m.id,m.nombre,m.activo)"><i class="fas fa-trash-alt"></i></button>
                                    <button v-else class="btn btn-sm btn-success" @click="eliminarMoneda(m.id,m.nombre,m.activo)"><i class="fas fa-trash-restore-alt"></i></button>
                                </td>
                            </tr>
                        </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <!-- tipo comprobante -->
            <div class="card card-info">
                <div class="card-header">
                    <h3 class="card-title">IGV</h3>
                </div>
              <!-- /.card-header -->
              <!-- form start -->
                
                <div class="card-body">
                    <div class="mb-2">
                        <h4>Impuesto general a las ventas: <strong>{{igv}} %</strong> </h4>
                    </div>
                    <div class="input-group mb-3" v-on:keyup.enter="saveUpdateIgv()">
                        <div class="input-group-prepend">
                            <span class="input-group-text">IGV</span>
                        </div>
                        <input type="number" class="form-control" placeholder="0" v-model="newIgv">
                        <div class="input-group-append">
                            <button class="btn btn-primary" type="button" @click="saveUpdateIgv()">Guardar</button>
                        </div>
                    </div>
                </div>
            </div>
            <!-- /.tipo comprobante -->
        </div>
    </div>
</template>

<script>
    export default{   
        data(){
            return{
                id:'',
                idSuc:'',
                nombre:'',
                simbolo:'',
                codigo:'',
                activo:'',
                arrayMoneda:[],
                arrayIgv:[],
                arraySucursal:[],
                igv:'',
                newIgv:'',
                igvId:'',
                nombreSucur:'',
                direccion:'',

                errorMoneda:0,
                arrayMostMsj:[],
                errorSucursal:0,
                arrayMostMsjSucursal:[],
                errorIgv:0,
                arrayMsjIgv:[],

                showModal:false,
                showModalSuc:false,
                errorSaveUpdate:[],
            }
        },
      computed: {
        
      },
      methods:{          
          listarMoneda(){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/moneda/`)
              .then(function(response){
                if(response.data.length){
                    me.arrayMoneda = response.data
                }
              })
          },
          listarIgv(){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/impuesto/`)
              .then(function(response){
                if(response.data.length){
                    me.igv = response.data[0]['valor_porcentaje']
                    me.igvId = response.data[0]['id']
                    me.newIgv = me.igv
                }
              })
          },
          listarSucursal(){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/sucursal/`)
              .then(function(response){
                if(response.data.length){
                    me.arraySucursal = response.data
                }
              })
          },
          validarIgv(){
            this.errorIgv = 0
            this.arrayMsjIgv = []
            const igvValue = parseFloat(this.newIgv)
            if(isNaN(igvValue) || igvValue < 0) this.arrayMsjIgv.push("Ingrese un valor de IGV válido")
            if(this.arrayMsjIgv.length) this.errorIgv = 1
            return this.errorIgv
          },
          saveUpdateIgv(){
            if(this.validarIgv()){
                this.arrayMsjIgv.forEach(element => {
                    this.$toastr.error(element,'Atencion!')
                });
                return
            }
            let me = this
            if(!this.igvId){ // Registrar primera vez
                this.$axios.post(`${process.env.VUE_APP_API_URL}/apiempresa/impuesto/`, {
                    valor_porcentaje: me.newIgv
                })
                .then(function (response) {
                    me.listarIgv()
                    console.log(response)
                    me.$toastr.success('IGV agregado', 'Registrado');
                })
            }else{ // Actualizar
                this.$axios.put(`${process.env.VUE_APP_API_URL}/apiempresa/impuesto/`+me.igvId+`/`, {
                    valor_porcentaje: me.newIgv
                })
                .then(function (response) {
                    me.listarIgv()
                    console.log(response)
                    me.$toastr.success('IGV registrado', 'Actualizado');
                })
            }
          },
          validar(){
              this.errorMoneda = 0
              this.arrayMostMsj = []
              if(!this.nombre.trim()) this.arrayMostMsj.push("Ingrese nombre de la moneda")
              if(!this.codigo.trim()) this.arrayMostMsj.push("Ingrese el codigo de la moneda")
              if(!this.simbolo.trim()) this.arrayMostMsj.push("Ingrese el simbolo de la moneda")
              if(this.arrayMostMsj.length) this.errorMoneda = 1
              return this.errorMoneda
          },
          validarSucursal(){
              this.errorSucursal = 0
              this.arrayMostMsjSucursal = []
              if(!this.nombreSucur.trim()) this.arrayMostMsjSucursal.push("Ingrese nombre de Sucursal")
              if(!this.direccion.trim()) this.arrayMostMsjSucursal.push("Ingrese una direccion de la sucursal")
              if(this.arrayMostMsjSucursal.length) this.errorSucursal = 1
              return this.errorSucursal
          },
          registrarMoneda(){
            if(this.validar()){
                this.arrayMostMsj.forEach(element => {
                  this.$toastr.error(element,'Atencion!')
              });
              return
            }
            let me = this
            this.$axios.post(`${process.env.VUE_APP_API_URL}/apiempresa/moneda/`, {
                nombre: (me.nombre.toUpperCase()).trim(),
                codigo: (me.codigo.toUpperCase()).trim(),
                simbolo: (me.simbolo.toUpperCase()).trim(),
            })
            .then(function (response) {
                me.listarMoneda()
                console.log(response)
                me.cerrarModal()
                me.$toastr.success('Nueva moneda agregado', 'Registrado');
            })
          },
          actualizarMoneda(){
              if(this.validar()){
                  this.arrayMostMsj.forEach(element => {
                      this.$toastr.error(element,'Atencion!')
                  });
                  return
              }
              let me = this
              this.$axios.put(`${process.env.VUE_APP_API_URL}/apiempresa/moneda/`+me.id+`/`,{
                nombre: (me.nombre.toUpperCase()).trim(),
                codigo: (me.codigo.toUpperCase()).trim(),
                simbolo: (me.simbolo.toUpperCase()).trim(),
              })
              .then(function(response){
                  console.log(response)
                  me.listarMoneda()
                  me.cerrarModal()
                  me.$toastr.success('Moneda actualizado', 'Actualizado');
              })
          },
          registrarSucursal(){
            if(this.validarSucursal()){
                this.arrayMostMsjSucursal.forEach(element => {
                  this.$toastr.error(element,'Atencion!')
              });
              return
            }
            let me = this
            this.$axios.post(`${process.env.VUE_APP_API_URL}/apiempresa/sucursal/`, {
                nombre: (me.nombreSucur.toUpperCase()).trim(),
                direccion: (me.direccion.toUpperCase()).trim(),
                idEmpresa: 1,
            })
            .then(function (response) {
                me.listarSucursal()
                console.log(response)
                me.cerrarModal()
                me.$toastr.success('Nuevo Sucursal', 'Registrado');
            })
            .catch(function(error){
                var msg = error.response.data.error
                me.$toastr.error(msg, 'Error');
                console.log(error.response.data)
            })
          },
          actualizarSucursal(){
              if(this.validarSucursal()){
                  this.arrayMostMsjSucursal.forEach(element => {
                      this.$toastr.error(element,'Atencion!')
                  });
                  return
              }
              let me = this
              this.$axios.put(`${process.env.VUE_APP_API_URL}/apiempresa/sucursal/`+me.idSuc+`/`,{
                nombre: (me.nombreSucur.toUpperCase()).trim(),
                direccion: (me.direccion.toUpperCase()).trim(),
              })
              .then(function(response){
                  console.log(response)
                  me.listarSucursal()
                  me.cerrarModal()
                  me.$toastr.success('Sucursal actualizado', 'Actualizado');
              })
          },
          eliminarMoneda(id,nombre,activo){
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
                  this.$axios.put(`${process.env.VUE_APP_API_URL}/apiempresa/moneda/`+id+`/`,{
                      activo : activo ?  0 : 1,
                  })
                  .then(function(response){
                      console.log(response)
                      me.listarMoneda()
                      me.cerrarModal()
                      if(activo){me.$toastr.success('Moneda deshabilitado', 'Desactivado')}
                      else{me.$toastr.success('Moneda Habilitado', 'Habilitado')}
                  })
              }
              })
          },
          eliminarSucursal(id,nombre,activo){
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
                  this.$axios.put(`${process.env.VUE_APP_API_URL}/apiempresa/sucursal/`+id+`/`,{
                      activo : activo ?  0 : 1,
                  })
                  .then(function(response){
                      console.log(response)
                      me.listarSucursal()
                      me.cerrarModal()
                      if(activo){me.$toastr.success('Local deshabilitado', 'Desactivado')}
                      else{me.$toastr.success('Local Habilitado', 'Habilitado')}
                  })
              }
              })
          },
          abrirModal(action, data=[]){
              switch(action){
                  case "registrar":{
                      this.showModal = true
                      this.tituloModal = "Nueva moneda"
                      this.tipoAccion = 1
                      break
                  }
                  case "actualizar":{
                      this.showModal = true
                      this.tituloModal = "Editar moneda"
                      this.id = data['id']
                      this.nombre = data['nombre']
                      this.codigo = data['codigo']
                      this.simbolo = data['simbolo']
                      this.tipoAccion = 2
                      break
                  }
              }                
          },
          abrirModalSucursal(action, data=[]){
              switch(action){
                  case "registrar":{
                      this.showModalSuc = true
                      this.tituloModal = "Nueva Sucursal"
                      this.tipoAccion = 1
                      break
                  }
                  case "actualizar":{
                      this.showModalSuc = true
                      this.tituloModal = "Editar Sucursal"
                      this.idSuc = data['id']
                      this.nombreSucur = data['nombre']
                      this.direccion = data['direccion']
                      this.tipoAccion = 2
                      break
                  }
              }                
          },
          cerrarModal(){
              this.showModal = false;
              this.showModalSuc = false;
              this.id = ''
              this.nombre = ''
              this.nombreSucur = ''
              this.codigo = ''
              this.simbolo = ''
              this.direccion = ''
          },
          //=========FIN DE COMPROBANTES=============//
      },
      watch: {
      },
      mounted(){
          this.listarMoneda()
          this.listarIgv()
          this.listarSucursal()
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