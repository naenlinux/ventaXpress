<template>
    <!-- Content Header (Page header) -->
    <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Configuración</h1>
        </div><!-- /.col -->
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-right">
            <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
            <li class="breadcrumb-item active">Configuración</li>
          </ol>
        </div><!-- /.col -->
      </div><!-- /.row -->
    </div><!-- /.container-fluid -->
  </div>
  <!-- /.content-header -->

  <div class="row">
    <div class="col-md-7">
         <!-- card empresa -->
         <div class="card card-info">
              <div class="card-header">
                <h3 class="card-title">Datos de la empresa</h3>
              </div>
              <!-- /.card-header -->
              <!-- form start -->
                <div class="card-body" v-on:keyup.enter = "registrarEmpresa()">
                  <div class="form-group row">
                    <label for="inputEmail3" class="col-sm-3 col-form-label">Nombre:</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" v-model="nombre" placeholder="MI EMPRESA EIRL">
                    </div>
                  </div>
                  <div class="form-group row">
                    <label for="inputEmail3" class="col-sm-3 col-form-label">Nombre Comercial:</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" v-model="nombre_comercial" placeholder="MI EMPRESA">
                    </div>
                  </div>
                  <div class="form-group row">
                    <label for="inputPassword3" class="col-sm-3 col-form-label">RUC:</label>
                    <div class="col-sm-9">
                      <input type="number" class="form-control" v-model="ruc" placeholder="NUMERO DE RUC">
                    </div>
                  </div>
                  <div class="form-group row">
                    <label for="inputPassword3" class="col-sm-3 col-form-label">Dirección:</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" v-model="direccion" placeholder="Dirección, domicilio">
                    </div>
                  </div>
                  <div class="form-group row">
                    <label for="inputPassword3" class="col-sm-3 col-form-label">Urbanización:</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" v-model="urbanizacion" placeholder="Urbanización">
                    </div>
                  </div>
                  <div class="form-group row">
                    <label for="inputPassword3" class="col-sm-3 col-form-label">Ubigeo:</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" v-model="ubigeo" placeholder="Numero de Ubigeo">
                    </div>
                  </div>
                  <div class="form-group row">
                    <label for="inputPassword3" class="col-sm-3 col-form-label">Correo:</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" v-model="correo" placeholder="Correo@.com">
                    </div>
                  </div>
                  <div class="form-group row">
                    <label for="inputPassword3" class="col-sm-3 col-form-label">Teléfono:</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" v-model="telefono" placeholder="92827221">
                    </div>
                  </div>
                  <div class="form-group row">
                    <label for="inputPassword3" class="col-sm-3 col-form-label">Gerente/Contac:</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" v-model="gerente" placeholder="Gerente o socio de la empresa">
                    </div>
                  </div>
                  <div class="form-group row">
                    <label for="inputPassword3" class="col-sm-3 col-form-label">Ciudad:</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" v-model="ciudad" placeholder="Ciudad">
                    </div>
                  </div>
                  <div class="form-group row">
                    <label for="inputPassword3" class="col-sm-3 col-form-label">Distrito:</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" v-model="distrito" placeholder="Distrito">
                    </div>
                  </div>
                  <div class="form-group row">
                    <label for="inputPassword3" class="col-sm-3 col-form-label">Provincia:</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" v-model="provincia" placeholder="Provincia">
                    </div>
                  </div>
                  <div class="form-group row">
                    <label for="inputPassword3" class="col-sm-3 col-form-label">Departamento:</label>
                    <div class="col-sm-9">
                      <input type="text" class="form-control" v-model="departamento" placeholder="Departamento">
                    </div>
                  </div>
                
                </div>
                <!-- /.card-body -->
                <div class="card-footer">
                  <button type="button" class="btn btn-info float-right" @click="registrarEmpresa()">Guardar</button>
                </div>
                <!-- /.card-footer -->
            </div>
            <!-- /.empresa -->
    </div>
    <!-- logo -->
    <div class="offset-md-1 col-md-4">
        <div class="form-group">
            <label for="exampleInputFile">Logo - Imagen</label>
            <div class="input-group">
                <div class="custom-file">
                    <input type="file" @change="onFileChange" class="custom-file-input" >
                    <label class="custom-file-label"  for="validatedCustomFile">{{ selectedFileName }}</label>
                </div>
                <div class="input-group-append">
                    <button type="button" @click="uploadImage()" class="btn btn-primary">Subir</button>
                </div>
            </div>
        </div>
        <img :src="logo" class="img-thumbnail" alt="Sin imagen">
        <div class="mt-2" v-if="logo">
          <button class="btn btn-warning btn-sm" @click="removerLogo()">Quitar logo</button>
        </div>
        <br><br>
        <div class="card card-success" v-on:keyup.enter = "registrarSunat()">
          <div class="card-header">DATOS SUNAT</div>
          <div class="card-body">
            <div class="form-group">
              <label>Usuario</label>
              <input type="text" class="form-control" v-model="usuario_sunat">
              <small class="form-text text-muted">Este usuario es el mismo de la plataforma SUNAT.</small>
            </div>
            <div class="form-group">
              <label>Clave</label>
              <input type="password" class="form-control" v-model="clave_sunat">
              <small class="form-text text-muted">Esta clave es el mismo de la plataforma SUNAT.</small>
            </div>
          </div>
          <div class="card-footer">
            <div class="row justify-content-center">
              <div class="col-sm-6">
                <button class="btn btn-success btn-block" @click="registrarSunat()">GUARDAR</button>
              </div>
            </div>
          </div>
        </div>
    </div>
    <!-- /logo -->
  </div>
</template>

<script>
    export default{   
        data(){
            return{
                id:'',
                nombre:'',
                nombre_comercial:'',
                ruc:'',
                direccion:'',
                gerente:'',
                arrayEmpresa:[],
                logo:'',
                telefono:'',
                correo:'',
                ubigeo:'',
                ciudad:'',
                distrito:'',
                provincia:'',
                departamento:'',

                usuario_sunat:'',
                clave_sunat:'',

                selectedFile:null,
                selectedFileName: 'Elegir imagen',

                errorEmpresa:0,
                arrayMostMsj:[],              
            }
        },
      computed: {
        
      },
      methods:{          
          listarEmpresa(){
              let me = this
              this.$axios.get(`${process.env.VUE_APP_API_URL}/apiempresa/empresa/`)
              .then(function(response){
                if(response.data.length){
                    me.id = response.data[0].id,
                    me.nombre = response.data[0].nombre,
                    me.nombre_comercial = response.data[0].nombre_comercial,
                    me.ruc = response.data[0].ruc,
                    me.direccion = response.data[0].direccion,
                    me.gerente = response.data[0].gerente,
                    me.logo = response.data[0].logo,
                    me.correo = response.data[0].correo,
                    me.telefono = response.data[0].telefono
                    me.ubigeo = response.data[0].ubigeo
                    me.ciudad = response.data[0].ciudad
                    me.distrito = response.data[0].distrito
                    me.provincia = response.data[0].provincia
                    me.departamento = response.data[0].departamento
                    me.usuario_sunat = response.data[0].usuario_sunat
                    me.clave_sunat = response.data[0].clave_sunat
                }
              })
          },
          validarEmpresa(){
              this.errorEmpresa = 0
              this.arrayMostMsj = []
              if(!this.nombre.trim()) this.arrayMostMsj.push("Ingrese nombre de la Empresa")
              if(!this.nombre_comercial.trim()) this.arrayMostMsj.push("Ingrese el nombre comercial")
              if(!this.ruc) this.arrayMostMsj.push("Ingrese el RUC")
              if(!this.direccion.trim()) this.arrayMostMsj.push("Ingrese la direccion")
              if(!this.gerente.trim()) this.arrayMostMsj.push("Ingrese nombre del gerente o contacto")
              if(!this.correo.trim()) this.arrayMostMsj.push("Ingrese un correo electronico")
              if(!this.telefono.trim()) this.arrayMostMsj.push("Ingrese numero de telefono")
              if(!this.ubigeo.trim()) this.arrayMostMsj.push("Ingrese el numero de ubigeo")
              //if(!this.ciudad.trim()) this.arrayMostMsj.push("Ingrese el numero de ubigeo")
              if(!this.distrito.trim()) this.arrayMostMsj.push("Ingrese el distrito")
              if(!this.provincia.trim()) this.arrayMostMsj.push("Ingrese la provincia")
              if(!this.departamento.trim()) this.arrayMostMsj.push("Ingrese el departamento")

              if(this.arrayMostMsj.length) this.errorEmpresa = 1
              return this.errorEmpresa
          },
          registrarEmpresa(){
            if(this.validarEmpresa()){
                this.arrayMostMsj.forEach(element => {
                  this.$toastr.error(element,'Atencion!')
              });
              return
            }
            let me = this
            if(!this.id){ // registrar empresa arrayEmpresa esta vacio
                this.$axios.post(`${process.env.VUE_APP_API_URL}/apiempresa/empresa/`, {
                    nombre: (me.nombre.toUpperCase()).trim(),
                    nombre_comercial: (me.nombre_comercial.toUpperCase()).trim(),
                    ruc: me.ruc,
                    direccion: (me.direccion.toUpperCase()).trim(),
                    gerente: (me.gerente.toUpperCase()).trim(),
                    telefono: me.telefono.trim(),
                    correo: me.correo.trim(),
                    ubigeo: me.ubigeo.trim(),
                    ciudad: (me.ciudad.toUpperCase()).trim(),
                    distrito: (me.distrito.toUpperCase()).trim(),
                    provincia: (me.provincia.toUpperCase()).trim(),
                    departamento: (me.departamento.toUpperCase()).trim(),
                })
                .then(function (response) {
                    me.listarEmpresa()
                    console.log(response)
                    me.$toastr.success('Empresa registrado', 'Registrado');
                })
            }else{ //si no va actualizar los datos de la empresa
              this.$axios.put(`${process.env.VUE_APP_API_URL}/apiempresa/empresa/`+me.id+`/`, {
                    nombre: (me.nombre.toUpperCase()).trim(),
                    nombre_comercial: (me.nombre_comercial.toUpperCase()).trim(),
                    ruc: me.ruc,
                    direccion: (me.direccion.toUpperCase()).trim(),
                    gerente: (me.gerente.toUpperCase()).trim(),
                    telefono: me.telefono.trim(),
                    correo: me.correo.trim(),
                    ubigeo: me.ubigeo.trim(),
                    ciudad: (me.ciudad.toUpperCase()).trim(),
                    distrito: (me.distrito.toUpperCase()).trim(),
                    provincia: (me.provincia.toUpperCase()).trim(),
                    departamento: (me.departamento.toUpperCase()).trim(),
                })
                .then(function (response) {
                    me.listarEmpresa()
                    console.log(response)
                    me.$toastr.success('Empresa actualizado', 'Actualizado');
                })
            }
              
          },
          registrarSunat(){
            if(this.id == ''){
              this.$toastr.error('Registre primero la empresa', 'Error');
              return
            }
            let me = this
            this.$axios.patch(`${process.env.VUE_APP_API_URL}/apiempresa/empresa/`+me.id+`/`, {
                    usuario_sunat: me.usuario_sunat.trim(),
                    clave_sunat: me.clave_sunat.trim(),
                })
                .then(function (response) {
                    me.listarEmpresa()
                    console.log(response)
                    me.$toastr.success('Usuario y clave agregado', 'Registrado');
                })
          },
          onFileChange(event){
            this.selectedFile = event.target.files[0]
            this.selectedFileName = this.selectedFile ? this.selectedFile.name: 'Elegir imagen'
          },
          uploadImage(){
            if(!this.selectedFile){this.$toastr.error('Seleccione una imagen', 'Error');return}
            if(this.id){ //si hay un registro de empresa se subira una imagen
              const formData = new FormData()
              formData.append('logo', this.selectedFile)
              let me = this
              this.$axios.put(`${process.env.VUE_APP_API_URL}/apiempresa/empresa/`+me.id+`/`, formData,{
                headers:{
                  'Content-Type': 'multipart/form-data',
                }
              })
              .then(function(response){
                me.$toastr.success('Imagen cargada', 'Exito');
                me.listarEmpresa()
                console.log('img subido exitosamente',response)
              })
              .catch(function(error){
                console.log(error)
                me.$toastr.error(error.response.data.logo[0],'Error')
              })
            }else{
              this.$toastr.error('Registre una empresa', 'Error');
            }
          },
          removerLogo(){
            let me = this
            this.$axios.put(`${process.env.VUE_APP_API_URL}/apiempresa/empresa/`+me.id+`/`, {
                logo: null,
            })
            .then(function (response) {
                me.listarEmpresa()
                console.log(response)
                me.$toastr.success('Logo removido', 'Eliminado');
            })
          }
      },
      watch: {
      },
      mounted(){
          this.listarEmpresa()      
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