<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Usuarios</h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item active">Usuarios</li>
          </ol>
        </div><!-- /.col -->
      </div><!-- /.row -->
    </div><!-- /.container-fluid -->
  </div>
  <!-- /.content-header -->

  <div class="card card-secondary card-outline">
      <div class="card-body">
          <div class="row">
              <div class="col-sm-6">
                  <h2><button class="btn btn-primary btn-sm toastrDefaultSuccess" @click="abrirModal('registrar')">Nuevo</button></h2>
              </div>
              <div class="col-sm-6">
                  <div class="input-group">
                      <input type="search" v-model="txtBuscar" @keyup="listarUsuarios(1,txtBuscar)" class="form-control form-control-md" placeholder="Buscar usuarios">
                      <div class="input-group-append">
                          <button type="submit" class="btn btn-md btn-default">
                              <i class="fa fa-search"></i>
                          </button>
                      </div>
                  </div>
              </div> 
          </div>
          <div class="table-responsive">
              <table class="table table-bordered table-sm table-striped">
                  <thead class="bg-secondary">
                      <tr>
                          <th>#</th>
                          <th>Nombre y apellidos</th>
                          <th>Usuario</th>
                          <th>Perfil</th>
                          <th>Puede hacer<br>descuentos al vender?</th>
                          <th>Sucursal</th>
                          <th width="20%">Opciones</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(u,index) in arrayUsuarios" :key="u.id">
                          <td>{{index+1}}</td>
                          <td>{{u.first_name+' '+u.last_name}}</td>
                          <td v-text="u.username"></td>
                          <td>
                            <div v-for="per in arrayPerfiles" :key="per.id">
                                <div v-if="per.id==u.groups" v-text="per.name"></div>
                            </div>                            
                          </td>
                          <td>
                            <span v-if="u.permisoDscto">SI</span>
                            <span v-else>NO</span>
                          </td>
                          <td v-text="u.sucursal"></td>
                          <td>
                              <button class="btn btn-sm btn-info" @click="abrirModalUser(u)"><i class="fas fa-key"></i></button>&nbsp;
                              <button class="btn btn-sm btn-warning" @click="abrirModal('actualizar', u)"><i class="fas fa-edit"></i></button>&nbsp;
                              <button v-if="u.is_active" class="btn btn-sm btn-danger" @click="eliminarUsuario(u.id,u.first_name,u.is_active)"><i class="fas fa-trash-alt"></i></button>
                              <button v-else class="btn btn-sm btn-success" @click="eliminarUsuario(u.id,u.first_name,u.is_active)"><i class="fas fa-trash-restore-alt"></i></button>&nbsp;
                              <span v-if="u.is_active" class="badge badge-success">Habilitad</span>
                              <span v-else class="badge badge-danger">Anulado</span>&nbsp;
                          </td>
                      </tr>
                  </tbody>
              </table>
          </div>
           <!-- Agrega el paginador aquí -->
      </div>      

  </div><!-- /.card -->

  <!--- MODAL USUARIOS --->
     <div v-if="showModal">
      <div class="modal">
          <div class="modal-overlay"></div>
              <div class="modal-content" v-on:keyup.enter = "tipoAccion==1?registrarUsuarios():actualizarUsuarios()">
                  <div class="modal-header bg-primary text-white">
                      <h4>{{tituloModal}}</h4>
                      <button type="button" class="close" @click="cerrarModal()">&times;</button>
                  </div>
                  <div class="modal-body">
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Nombre: *</label>
                          <div class="col-sm-9">
                              <input type="text" class="form-control" v-model="nombre" placeholder="Nombre">
                          </div>
                      </div>
                    <div class="mb-3 row">
                        <label for="" class="col-sm-3 col-form-label">Apeliidos: *</label>
                        <div class="col-sm-9">
                            <input type="text" class="form-control" v-model="apellidos" placeholder="Apellidos">
                        </div>
                    </div>
                    <div class="mb-3 row">
                        <label for="" class="col-sm-3 col-form-label">Usuario:</label>
                        <div class="col-sm-9">
                            <input type="text" class="form-control" v-model="usuario" placeholder="Usuario">
                        </div>
                    </div>
                    <div class="mb-3 row" v-if="tipoAccion==1">
                        <label for="" class="col-sm-3 col-form-label">Contraseña:</label>
                        <div class="col-sm-9">
                            <input type="password" class="form-control" v-model="contrasena" placeholder="******">
                        </div>
                    </div>
                      <div class="mb-3 row">
                          <label for="" class="col-sm-3 col-form-label">Perfil:</label>
                          <div class="col-sm-9">
                              <select class="form-control" v-model="perfil">
                                <option value="0">==== seleccione ====</option>
                                <option :value="pe.id" v-for="pe in arrayPerfiles" :key="pe.id">{{pe.name}}</option>
                              </select>
                          </div>
                      </div>                     
                      <div class="mb-3 row">
                        <label for="" class="col-sm-3 col-form-label">Sucursal:</label>
                        <div class="col-sm-9">
                            <select class="form-control" v-model="sucursal">
                                <option value="0">==== seleccione ====</option>
                                <option :value="su.id" v-for="su in arraySucursal" :key="su.id">{{su.nombre}}</option>
                            </select>
                        </div>
                    </div>
                    <div class="mb-3 row">
                        <label for="" class="col-sm-3 col-form-label">Permiso para hacer descuentos al vender</label>
                        <div class="col-sm-9">
                            <input type="checkbox" v-model="permisoDscto" class="mt-4">
                        </div>
                    </div> 
                  </div>
                  <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" @click="cerrarModal()">Cerrar</button>
                      <button type="button" v-if="tipoAccion==1" class="btn btn-primary" @click="registrarUsuarios()">GUARDAR</button>
                      <button type="button" v-if="tipoAccion==2" class="btn btn-primary" @click="actualizarUsuarios()">ACTUALIZAR</button>
                  </div>
              </div>
          </div>
          
      </div>
  <!--- FIN MODAL PEDIDO --->

  <!--- MODAL CAMBIO USUARIO CLAVE --->
  <div v-if="showModalUser">
    <div class="modal">
        <div class="modal-overlay"></div>
            <div class="modal-content" v-on:keyup.enter = "actualizarClave()">
                <div class="modal-header bg-primary text-white">
                    <h4>{{tituloModal}}</h4>
                    <button type="button" class="close" @click="cerrarModal()">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="mb-3 row">
                        <label for="" class="col-sm-3 col-form-label">Usuario: *</label>
                        <div class="col-sm-9">
                            <input type="text" class="form-control" v-model="usuarioUpdate" placeholder="Nombre">
                        </div>
                    </div>
                    <div class="mb-3 row">
                      <label for="" class="col-sm-3 col-form-label">Contraseña:</label>
                      <div class="col-sm-9">
                          <input type="password" class="form-control" v-model="contrasenaUpdate" placeholder="******">
                      </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="cerrarModal()">Cerrar</button>
                    <button type="button" class="btn btn-primary" @click="actualizarClave()">ACTUALIZAR</button>
                </div>
            </div>
        </div>
        
    </div>
<!--- FIN CAMBIO USUARIO CLAVE --->
</template>

<script>
    export default{   
      data(){
          return{
              id:'',
              nombre:'',
              apellidos:'',
              perfil:0,
              sucursal:0,
              descripcion:'',
              usuario:'',
              contrasena:'',
              usuarioUpdate:'',
              contrasenaUpdate:'',
              permisoDscto:false,
            
              arrayUsuarios:[],
              arraySucursal:[],
              arrayPerfiles:[],
              showModal: false,
              showModalUser: false,
              tituloModal: '',
              usuarios: [],
              errorUsuario:0,
              errorClave:0,
              arrayMostMsj:[],
              arrayMostMsjClave:[],
              tipoAccion: 0,
              txtBuscar:'',
              errorSaveUpdate:[],

              currentPage: 1,
              totalPages: 0,
              listporPage: 10,
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
              this.listarCategorias(pageNumber,'');
          },
          goToPreviousPage() {
              if (this.currentPage > 1) {
                  this.currentPage -= 1;
                  this.listarCategorias(this.currentPage,'');
              }
          },
          goToNextPage() {
              if (this.currentPage < this.totalPages) {
                  this.currentPage += 1;
                  this.listarCategorias(this.currentPage,'');
              }
          },
          goToFirstPage() {
              if (this.currentPage !== 1) {
                  this.currentPage = 1;
                  this.listarCategorias(this.currentPage,'');
              }
          },
          goToLastPage() {
              if (this.currentPage !== this.totalPages) {
                  this.currentPage = this.totalPages;
                  this.listarCategorias(this.currentPage,'');
              }
          },
          listarUsuarios(){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/usuarios/`)
              .then(function(response){
                  me.arrayUsuarios = response.data
              })
          },
          validarUsuarios(){
              this.errorUsuario = 0
              this.arrayMostMsj = []
              
              if(this.sucursal==0) this.arrayMostMsj.push("Seleccione una sucursal")
              if(this.perfil==0) this.arrayMostMsj.push("Seleccione un perfil")
              if(this.tipoAccion==1) {
                if(!this.contrasena) this.arrayMostMsj.push("Ingrese una contraseña")
                if(this.contrasena.length < 4) this.arrayMostMsj.push("La contraseña debe tener al menos 4 caracteres")
              }
              if(!this.usuario) this.arrayMostMsj.push("Ingrese el usuario")
              if(this.usuario.length < 4) this.arrayMostMsj.push("El usuario debe tener al menos 4 caracteres")
              if(!this.apellidos) this.arrayMostMsj.push("Ingrese apellidos")
              if(!this.nombre.trim()) this.arrayMostMsj.push("Ingrese el nombre")
              if(this.arrayMostMsj.length) this.errorUsuario = 1
              return this.errorUsuario
          },
          validarClave(){
              this.errorClave = 0
              this.arrayMostMsjClave = []
                            
              if(!this.contrasenaUpdate) this.arrayMostMsjClave.push("Ingrese una contraseña")
              if(this.contrasenaUpdate.length < 4) this.arrayMostMsjClave.push("La contraseña debe tener al menos 4 caracteres")
              if(!this.usuarioUpdate) this.arrayMostMsjClave.push("Ingrese el usuario")
              if(this.usuarioUpdate.length < 4) this.arrayMostMsjClave.push("El usuario debe tener al menos 4 caracteres")
              
              if(this.arrayMostMsjClave.length) this.errorClave = 1
              return this.errorClave
          },
          registrarUsuarios(){
              if(this.validarUsuarios()){
                  this.arrayMostMsj.forEach(element => {
                      this.$toastr.error(element,'Atencion!')
                  });
                  return
              }
              let me = this
              this.$axios.post(`${process.env.VUE_APP_API_URL}/apiempresa/usuarios/`, {
                  first_name: (me.nombre.toUpperCase()).trim(),
                  last_name: (me.apellidos.toUpperCase()).trim(),
                  username: me.usuario.trim(),
                  password: me.contrasena.trim(),
                  groups: [me.perfil],
                  idSucursal: me.sucursal,
                  permisoDscto: me.permisoDscto,
              })
              .then(function (response) {
                  me.listarUsuarios(1,'')
                  me.cerrarModal()
                  console.log(response)
                  me.$toastr.success('Nuevo usuario', 'Registrado');
              })
              .catch(function (error) {
                if(error.response && error.response.data){
                    if(error.response.data.nombre){me.errorSaveUpdate.push(error.response.data.nombre[0])}
                }
                if(me.errorSaveUpdate.length > 0){
                    me.errorSaveUpdate.forEach(element => {
                        me.$toastr.error(element,'Error')
                    });
                }
                me.errorSaveUpdate = []          
               })
          },
          actualizarUsuarios(){
              if(this.validarUsuarios()){
                  this.arrayMostMsj.forEach(element => {
                      this.$toastr.error(element,'Atencion!')
                  });
                  return
              }
              let me = this
              this.$axios.patch(`${process.env.VUE_APP_API_URL}/apiempresa/usuarios/`+me.id+`/`,{
                  first_name: (me.nombre.toUpperCase()).trim(),
                  last_name: (me.apellidos.toUpperCase()).trim(),
                  username: me.usuario.trim(),
                  groups: [me.perfil],
                  idSucursal: me.sucursal,
                  permisoDscto: me.permisoDscto,
              })
              .then(function(response){
                  console.log(response)
                  me.listarUsuarios(me.currentPage,me.txtBuscar)
                  me.cerrarModal()
                  me.$toastr.success('Usuario actualizado', 'Actualizado');
              })
              .catch(function (error) {
                console.log('error al gurdar'+ error)  
               })
          },
          actualizarClave(){
              if(this.validarClave()){
                  this.arrayMostMsjClave.forEach(element => {
                      this.$toastr.error(element,'Atencion!')
                  });
                  return
              }
              let me = this
              this.$axios.patch(`${process.env.VUE_APP_API_URL}/apiempresa/usuarios/`+me.id+`/`,{
                  username: me.usuarioUpdate.trim(),
                  password: me.contrasenaUpdate.trim()
              })
              .then(function(response){
                  console.log(response)
                  me.listarUsuarios(me.currentPage,me.txtBuscar)
                  me.cerrarModal()
                  me.$toastr.success('Usuario y clave', 'Actualizados');
              })
              .catch(function (error) {
                console.log('error al gurdar'+ error)  
               })
          },
          eliminarUsuario(id,nombre, activo){
              let me = this
              this.$swal.fire({
              title: nombre,
              text: activo ? 'Presione si para eliminar':'Presione si para restaurar',
              icon: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: activo ? 'Si, eliminar' : 'Si, Restaurar'
              }).then((result) => {
                if (result.isConfirmed) {
                  this.$axios.patch(`${process.env.VUE_APP_API_URL}/apiempresa/usuarios/`+id+`/`,{
                    is_active : activo ?  0 : 1,
                  })
                  .then(function(response){
                      console.log(response)
                      me.listarUsuarios(me.currentPage,me.txtBuscar)
                      me.cerrarModal()
                      if(activo){me.$toastr.success('Usuario anulado', 'Desactivado')}
                      else{me.$toastr.success('Usuario Habilitado', 'Activado')}
                  })
                }
              })
          },
          abrirModal(action, data=[]){ console.log(data)
              switch(action){
                  case "registrar":{
                      this.showModal = true
                      this.tituloModal = "Nuevo usuario"
                      this.tipoAccion = 1
                      break
                  }
                  case "actualizar":{
                      this.showModal = true
                      this.tituloModal = "Editar usuario"
                      this.id = data['id']
                      this.apellidos = data['last_name']
                      this.nombre = data['first_name']
                      this.usuario = data['username']
                      this.sucursal = data['idSucursal']
                      this.perfil = data['groups'][0]
                      this.tipoAccion = 2
                      this.permisoDscto = data['permisoDscto']
                      break
                  }
              }                
          },
          abrirModalUser(data=[]){
            this.showModalUser = true
            this.tituloModal = "Cambiar Usuario y clave: "+data['first_name']
            this.id = data['id']
            this.usuarioUpdate = data['username']
            //this.contrasenaUpdate = data['password']              
          },
          listar_perfil_sucursal(){
            let me = this
            this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/sucursal/`)
            .then(function(response){
            if(response.data.length){
                me.arraySucursal = response.data
            }
            })

            this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/grupos/`)
            .then(function(response){
            if(response.data.length){
                me.arrayPerfiles = response.data
            }
            })
          },
          cerrarModal(){
              this.showModal = false
              this.showModalUser = false
              this.id = ''
              this.apellidos = ''
              this.nombre = ''
              this.usuario = ''
              this.contrasena = ''
              this.perfil = 0
              this.sucursal = 0
              this.usuarioUpdate=''
              this.contrasenaUpdate=''
              this.permisoDscto=false
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
          this.listarUsuarios(1,'')
          this.listar_perfil_sucursal()
          this.updateVisiblePages();
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