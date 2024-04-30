<template>
     <!-- Main Sidebar Container -->
 <aside class="main-sidebar sidebar-dark-primary elevation-4">
    <!-- Brand Logo -->
    <router-link :to="{ name:'dashboard' }" class="brand-link" @click="seleecionarMenu('dashboard','')">
      <img src="./../dist/img/logoVenta.png" alt="AdminLTE Logo" class="brand-image img-circle elevation-3" style="opacity: .8">
      <span class="brand-text font-weight-light">VentaXpress</span>
    </router-link>

    <!-- Sidebar -->
    <div class="sidebar">
      <!-- Sidebar user panel (optional) -->
      <div class="user-panel mt-3 pb-3 mb-3 d-flex">
        <div class="image">
          <img src="./../dist/img/usuario.png" class="" alt="User Image">
        </div>
        <div class="info">
          <a>{{ nombreUsuario }}</a>
        </div>
      </div>

      <!-- SidebarSearch Form -->
      <div class="form-inline">
        <div class="input-group" data-widget="sidebar-search">
          <input class="form-control form-control-sidebar" type="search" placeholder="Search" aria-label="Search">
          <div class="input-group-append">
            <button class="btn btn-sidebar">
              <i class="fas fa-search fa-fw"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Sidebar Menu -->
      <nav class="mt-2">
        <ul class="nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu" data-accordion="false">
          <!-- Add icons to the links using the .nav-icon class
               with font-awesome or any other icon font library -->
               <li class="nav-item" :class="{'menu-open':menuPrincipal==='empresa'}" v-if="tipoUsuario == 1">
            <a href="#" class="nav-link" :class="{'active':menuPrincipal==='empresa'}">
              <i class="nav-icon fas fa-city"></i>
              <p>
                Empresa
                <i class="right fas fa-angle-left"></i>
              </p>
            </a>
            <ul class="nav nav-treeview">
              <li class="nav-item">
                <router-link :to="{name:'configuracion'}" class="nav-link"
                  :class="{'active':menuSeleccionado==='configuracion'}" 
                  @click="seleecionarMenu('configuracion','empresa')">
                  <i class="far fa-circle nav-icon"></i>
                  <p>Configuracion</p>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link :to="{name:'comprobantes'}" class="nav-link"
                  :class="{'active':menuSeleccionado==='comprobantes'}" 
                  @click="seleecionarMenu('comprobantes','empresa')">
                  <i class="far fa-circle nav-icon"></i>
                  <p>Comprobantes</p>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link :to="{name:'moneda'}" class="nav-link"
                  :class="{'active':menuSeleccionado==='moneda'}" 
                  @click="seleecionarMenu('moneda','empresa')">
                  <i class="far fa-circle nav-icon"></i>
                  <p>Sucursal Moneda-IGV</p>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link :to="{name:'usuarios'}" class="nav-link"
                  :class="{'active':menuSeleccionado==='usuarios'}" 
                  @click="seleecionarMenu('usuarios','empresa')">
                  <i class="far fa-circle nav-icon"></i>
                  <p>Usuarios</p>
                </router-link>
              </li>
            </ul>
          </li>
          <li class="nav-item" :class="{'menu-open':menuPrincipal==='mantenedores'}" v-if="tipoUsuario == 1">
            <a href="#" class="nav-link" :class="{'active':menuPrincipal==='mantenedores'}">
              <i class="nav-icon fas fa-cogs"></i>
              <p>
                Mantenedores
                <i class="right fas fa-angle-left"></i>
              </p>
            </a>
            <ul class="nav nav-treeview">
              <li class="nav-item">
                <router-link :to="{name:'categorias'}" class="nav-link"
                  :class="{'active':menuSeleccionado==='categorias'}" 
                  @click="seleecionarMenu('categorias','mantenedores')">
                  <i class="far fa-circle nav-icon"></i>
                  <p>Categorias</p>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link :to="{ name: 'unidadmedida'}" class="nav-link"
                  :class="{'active':menuSeleccionado==='unidadmedida'}" 
                  @click="seleecionarMenu('unidadmedida','mantenedores')">
                  <i class="far fa-circle nav-icon"></i>
                  <p>Unidad medida</p>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link :to="{name:'productos'}" class="nav-link"
                  :class="{'active':menuSeleccionado==='productos'}" 
                  @click="seleecionarMenu('productos','mantenedores')">
                  <i class="far fa-circle nav-icon"></i>
                  <p>Productos</p>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link :to="{ name: 'proveedores'}" class="nav-link"
                  :class="{'active':menuSeleccionado==='proveedores'}" 
                  @click="seleecionarMenu('proveedores','mantenedores')">
                  <i class="far fa-circle nav-icon"></i>
                  <p>Proveedores</p>
                </router-link>
              </li>
            </ul>
          </li>
         
          <li class="nav-item" :class="{'menu-open':menuPrincipal==='inventario'}" v-if="tipoUsuario == 1">
            <a href="#" class="nav-link" :class="{'active':menuPrincipal==='inventario'}">
              <i class="nav-icon fas fa-dolly-flatbed"></i>
              <p>
                Inventarios
                <i class="right fas fa-angle-left"></i>
              </p>
            </a>
            <ul class="nav nav-treeview">
              <li class="nav-item">
                <router-link :to="{name:'compras'}" class="nav-link"
                  :class="{'active':menuSeleccionado==='compras'}" 
                  @click="seleecionarMenu('compras','inventario')">
                  <i class="far fa-circle nav-icon"></i>
                  <p>Compras</p>
                </router-link>
              </li>
            </ul>
            <ul class="nav nav-treeview">
              <li class="nav-item">
                <router-link :to="{name:'almacen'}" class="nav-link"
                  :class="{'active':menuSeleccionado==='almacen'}" 
                  @click="seleecionarMenu('almacen','inventario')">
                  <i class="far fa-circle nav-icon"></i>
                  <p>Almacen</p>
                </router-link>
              </li>
            </ul>
          </li>
          <li class="nav-item" :class="{'menu-open':menuPrincipal==='ventas'}" v-if="tipoUsuario == 1 || tipoUsuario == 2 || tipoUsuario == 3 || tipoUsuario == 4">
            <a href="#" class="nav-link" :class="{'active':menuPrincipal==='ventas'}">
              <i class="nav-icon fab fa-shopify"></i>
              <p>
                Ventas
                <i class="right fas fa-angle-left"></i>
              </p>
            </a>
            <ul class="nav nav-treeview">
              <li class="nav-item" v-if="tipoUsuario == 1 || tipoUsuario == 3 || tipoUsuario == 4">
                <router-link :to="{name:'pedidos'}" class="nav-link"
                :class="{'active':menuSeleccionado==='pedidos'}"
                @click="seleecionarMenu('pedidos','ventas')">
                  <i class="far fa-circle nav-icon"></i>
                  <p>
                  Vender
                  </p>
                </router-link>
              </li>
            </ul>
            <ul class="nav nav-treeview">
              <li class="nav-item" v-if="tipoUsuario == 1 || tipoUsuario == 2 || tipoUsuario == 4">
                <router-link :to="{name:'caja'}" class="nav-link"
                :class="{'active':menuSeleccionado==='caja'}"
                @click="seleecionarMenu('caja','ventas')">
                  <i class="nav-icon far fa-circle"></i>
                  <p>
                  Cobrar
                  </p>
                </router-link>
              </li>
            </ul>
            <ul class="nav nav-treeview">
              <li class="nav-item" v-if="tipoUsuario == 1 || tipoUsuario == 2 || tipoUsuario == 4">
                <router-link :to="{name:'ventas'}" class="nav-link"
                :class="{'active':menuSeleccionado==='ventas'}"
                @click="seleecionarMenu('ventas','ventas')">
                  <i class="nav-icon far fa-circle"></i>
                  <p>
                  Mis ventas
                  </p>
                </router-link>
              </li>
            </ul>
            <ul class="nav nav-treeview">
              <li class="nav-item" v-if="tipoUsuario == 1 || tipoUsuario == 2 || tipoUsuario == 4">
                <router-link :to="{name:'reporteventas'}" class="nav-link"
                :class="{'active':menuSeleccionado==='reporteventas'}"
                @click="seleecionarMenu('reporteventas','ventas')">
                  <i class="nav-icon far fa-circle"></i>
                  <p>
                  Reporte de ventas
                  </p>
                </router-link>
              </li>
            </ul>
            <ul class="nav nav-treeview">
              <li class="nav-item" v-if="tipoUsuario == 1 || tipoUsuario == 2 || tipoUsuario == 4">
                <router-link :to="{name:'notacredito'}" class="nav-link"
                :class="{'active':menuSeleccionado==='notacredito'}"
                @click="seleecionarMenu('notacredito','ventas')">
                  <i class="nav-icon far fa-circle"></i>
                  <p>
                  Notas de Créditos
                  </p>
                </router-link>
              </li>
            </ul>
          </li>
      
          <li class="nav-item">
            <a href="#" class="nav-link">
              <i class="nav-icon fas fa-th"></i>
              <p>
               Manual
                <span class="right badge badge-danger">New</span>
              </p>
            </a>
          </li>
        </ul>
      </nav>
      <!-- /.sidebar-menu -->
    </div>
    <!-- /.sidebar -->
  </aside>
</template>
<script>
//Tipo Usuario: 1 Administrador, 2 Cajero, 3 Vendedor, 4 CajaVenta
  export default{
    props :['nombreUsuario','tipoUsuario'],
    data(){
      return{
        menuSeleccionado : '',
        menuPrincipal : '',
      }
    },
    methods:{
      seleecionarMenu(seleccionado,menuPrincipal){
        this.menuSeleccionado = seleccionado
        this.menuPrincipal = menuPrincipal
        
      }
    }
  }
</script>