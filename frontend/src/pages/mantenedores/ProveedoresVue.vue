<template>
      <!-- Content Header (Page header) -->
      <div class="content-header">
      <div class="container-fluid">
        <div class="row mb-2">
          <div class="col-sm-6">
            <h1 class="m-0">Proveedores</h1>
          </div><!-- /.col -->
          <div class="col-sm-6">
            <ol class="breadcrumb float-sm-right">
              <li class="breadcrumb-item"><router-link :to="{ name:'dashboard'}">Home</router-link></li>
              <li class="breadcrumb-item active">Proveedores</li>
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
                        <input type="search" v-model="txtBuscar" @keyup="listarProveedores(1,txtBuscar)" class="form-control form-control-md" placeholder="Buscar por empresa o RUC">
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
                            <th>Empresa</th>
                            <th>Ruc</th>
                            <th>Direccion</th>
                            <th>Correo</th>
                            <th>Telefono</th>
                            <th>Celular</th>
                            <th>Contacto</th>
                            <th width="7%">Opciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="p in proveedores" :key="p.id">
                            <td v-text="p.empresa"></td>
                            <td v-text="p.ruc"></td>
                            <td v-text="p.direccion"></td>
                            <td v-text="p.correo"></td>
                            <td v-text="p.telefono"></td>                        
                            <td v-text="p.celular"></td>
                            <td v-text="p.contacto"></td>
                            <td>
                                <button class="btn btn-sm btn-warning" @click="abrirModal('actualizar', p)"><i class="fas fa-edit"></i></button>&nbsp;
                                <button class="btn btn-sm btn-danger" @click="eliminarProveedor(p.id,p.empresa)"><i class="fas fa-trash-alt"></i></button>
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

    <!--- MODAL PEDIDO --->
       <div v-if="showModal">
        
        <div class="modal">
            <div class="modal-overlay"></div>
                <div class="modal-content" v-on:keyup.enter = "tipoAccion==1?registrarProveedor():actualizarProveedor()">
                    <div class="modal-header bg-primary text-white">
                        <h4>{{tituloModal}}</h4>
                        <button type="button" class="close" @click="cerrarModal()">&times;</button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3 row">
                            <label for="" class="col-sm-3 col-form-label">Empresa: *</label>
                            <div class="col-sm-9">
                                <input type="text" class="form-control" v-model="empresa" placeholder="Nombre de la empresa">
                            </div>
                        </div>
                        <div class="mb-3 row">
                            <label for="" class="col-sm-3 col-form-label">RUC: *</label>
                            <div class="col-sm-9">
                                <input type="text" class="form-control" v-model="ruc" placeholder="Número de RUC">
                            </div>
                        </div>
                        <div class="mb-3 row">
                            <label for="" class="col-sm-3 col-form-label">Dirección:</label>
                            <div class="col-sm-9">
                                <input type="text" class="form-control" v-model="direccion" placeholder="Dirección">
                            </div>
                        </div>
                        <div class="mb-3 row">
                            <label for="" class="col-sm-3 col-form-label">Correo:</label>
                            <div class="col-sm-9">
                                <input type="text" class="form-control" v-model="correo" placeholder="Correo electrónico">
                            </div>
                        </div>
                        <div class="mb-3 row">
                            <label for="" class="col-sm-3 col-form-label">Teléfono:</label>
                            <div class="col-sm-9">
                                <input type="text" class="form-control" v-model="telefono" placeholder="Número de teléfono">
                            </div>
                        </div>
                        <div class="mb-3 row">
                            <label for="" class="col-sm-3 col-form-label">Celular:</label>
                            <div class="col-sm-9">
                                <input type="text" class="form-control" v-model="celular" placeholder="Número de celular">
                            </div>
                        </div>
                        <div class="mb-3 row">
                            <label for="" class="col-sm-3 col-form-label">Contacto:</label>
                            <div class="col-sm-9">
                                <input type="text" class="form-control" v-model="contacto" placeholder="Nombre de la persona de contacto">
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="cerrarModal()">Cerrar</button>
                        <button type="button" v-if="tipoAccion==1" class="btn btn-primary" @click="registrarProveedor()">GUARDAR</button>
                        <button type="button" v-if="tipoAccion==2" class="btn btn-primary" @click="actualizarProveedor()">ACTUALIZAR</button>
                    </div>
                </div>
            </div>
            
        </div>
    <!--- FIN MODAL PEDIDO --->
</template>

<script>
      export default{   
        data(){
            return{
                id:'',
                empresa:'',
                ruc:'',
                direccion:'',
                correo:'',
                telefono:'',
                celular:'',
                contacto:'',

                showModal: false,
                tituloModal: '',
                proveedores: [],
                errorProveedor:0,
                arrayMostMsj:[],
                tipoAccion: 0,
                txtBuscar:'',

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
                this.listarProveedores(pageNumber,'');
            },
            goToPreviousPage() {
                if (this.currentPage > 1) {
                    this.currentPage -= 1;
                    this.listarProveedores(this.currentPage,'');
                }
            },
            goToNextPage() {
                if (this.currentPage < this.totalPages) {
                    this.currentPage += 1;
                    this.listarProveedores(this.currentPage,'');
                }
            },
            goToFirstPage() {
                if (this.currentPage !== 1) {
                    this.currentPage = 1;
                    this.listarProveedores(this.currentPage,'');
                }
            },

            goToLastPage() {
                if (this.currentPage !== this.totalPages) {
                    this.currentPage = this.totalPages;
                    this.listarProveedores(this.currentPage,'');
                }
            },
            listarProveedores(pageNumber = 1,txtBuscar){
                let me = this
                this.$axios.get(`${process.env.VUE_APP_API_URL}/api/proveedores/?page=${pageNumber}&search=${txtBuscar}`)
                .then(function(response){
                    me.proveedores = response.data.results
                    me.currentPage = pageNumber
                    me.totalPages = Math.ceil(response.data.count / me.listporPage)
                    me.totalRegistros = response.data.count
                })
            },
            validarProveedor(){
                this.errorProveedor = 0
                this.arrayMostMsj = []
                if(!this.empresa.trim()) this.arrayMostMsj.push("Ingrese el nombre de la Empresa")
                if(!this.ruc.trim()) this.arrayMostMsj.push("Ingrese el RUC de la Empresa")
                if(this.arrayMostMsj.length) this.errorProveedor = 1
                return this.errorProveedor
            },
            registrarProveedor(){
                if(this.validarProveedor()){
                    this.arrayMostMsj.forEach(element => {
                        this.$toastr.error(element,'Atencion!')
                    });
                    return
                }
                let me = this
                this.$axios.post(`${process.env.VUE_APP_API_URL}/api/proveedores/`, {
                    empresa: (me.empresa.toUpperCase()).trim(),
                    ruc: me.ruc.trim(),
                    direccion: me.direccion.trim(),
                    correo: me.correo.trim(),
                    telefono: me.telefono.trim(),
                    celular: me.celular.trim(),
                    contacto: me.contacto.trim(),
                })
                .then(function (response) {
                    me.listarProveedores(1,'')
                    me.cerrarModal()
                    console.log(response)
                    me.$toastr.success('Nuevo proveedor registrado', 'Registrado');
                })
            },
            actualizarProveedor(){
                if(this.validarProveedor()){
                    this.arrayMostMsj.forEach(element => {
                        this.$toastr.error(element,'Atencion!')
                    });
                    return
                }
                let me = this
                this.$axios.put(`${process.env.VUE_APP_API_URL}/api/proveedores/`+me.id+`/`,{
                    empresa: (me.empresa.toUpperCase()).trim(),
                    ruc: me.ruc.trim(),
                    direccion: me.direccion.trim(),
                    correo: me.correo.trim(),
                    telefono: me.telefono.trim(),
                    celular: me.celular.trim(),
                    contacto: me.contacto.trim(),
                })
                .then(function(response){
                    console.log(response)
                    me.listarProveedores(me.currentPage,me.txtBuscar)
                    me.cerrarModal()
                    me.$toastr.success('Proveedor actualizado', 'Actualizado');
                })
            },
            eliminarProveedor(id,nombre){
                let me = this
                this.$swal.fire({
                title: nombre,
                text: 'Presione si para eliminar',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Si, eliminar'
                }).then((result) => {
                if (result.isConfirmed) {
                    this.$axios.put(`${process.env.VUE_APP_API_URL}/api/proveedores/`+id+`/`,{
                        activo : 0,
                    })
                    .then(function(response){
                        console.log(response)
                        me.listarProveedores(me.currentPage,me.txtBuscar)
                        me.cerrarModal()
                        me.$toastr.success('Proveedor eliminado', 'Eliminado');
                    })
                }
                })
            },
            abrirModal(action, data=[]){
                switch(action){
                    case "registrar":{
                        this.showModal = true
                        this.tituloModal = "Nuevo proveedor"
                        this.tipoAccion = 1
                        break
                    }
                    case "actualizar":{
                        this.showModal = true
                        this.tituloModal = "Editar proveedor"
                        this.id = data['id']
                        this.empresa = data['empresa']
                        this.ruc = data['ruc']
                        this.direccion = data['direccion']
                        this.correo = data['correo']
                        this.telefono = data['telefono']
                        this.celular = data['celular']
                        this.contacto = data['contacto']
                        this.tipoAccion = 2
                        break
                    }
                }                
            },
            cerrarModal(){
                this.showModal = false;
                this.id = ''
                this.empresa = ''
                this.ruc = ''
                this.direccion = ''
                this.correo = ''
                this.telefono = ''
                this.celular = ''
                this.contacto = ''
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
            this.listarProveedores(1,'')
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