import { createRouter, createWebHistory } from "vue-router";
import authMiddleware from "./authMiddleware";

//import Login from './pages/LogiN'
import DashBoard from './pages/DashBoard'
import ProveedoresVue from './pages/mantenedores/ProveedoresVue'
import CategoriasVue from './pages/mantenedores/CategoriasVue'
import ProductosVue from './pages/mantenedores/ProductosVue'
import UnidadMedida from './pages/mantenedores/UnidadMedida'

import EmpresaVue from './pages/empresa/EmpresaVue'
import ComprobanteS from './pages/empresa/ComprobanteS'
import MonedA from './pages/empresa/MonedA'
import UsuarioS from './pages/empresa/UsuarioS'

import CompraS from './pages/inventario/CompraS'
import NuevaCompra from './pages/inventario/NuevaCompra'
import CompraDetalle from './pages/inventario/CompraDetalle'
import AlmaceN from './pages/inventario/AlmaceN'

import Pedidos from './pages/venta/ListarPedido'
import NuevoPedido from './pages/venta/NuevoPedido'
import DetallePedido from './pages/venta/DetallePedido'
import Caja from './pages/venta/CajA'
import Ventas from './pages/venta/VentaS'
import ReporteVentas from './pages/venta/ReporteVentas'
import DetalleVenta from './pages/venta/DetalleVenta'
import NotaCredito from './pages/venta/NotaCredito'
import NuevaNotaCred from './pages/venta/NuevaNotaCred'


const routes = [
    //{name: 'login', path: '/login', component: Login},
    {name: 'dashboard', path: '/dashboard', component: DashBoard, meta: {requiresAuth:true}, beforeEnter: authMiddleware},
    {name: 'proveedores', path: '/proveedores', component: ProveedoresVue, beforeEnter: authMiddleware},
    {name: 'categorias', path: '/categorias', component: CategoriasVue, meta:{requiresAuth:true}, beforeEnter: authMiddleware},
    {name: 'productos', path: '/productos', component: ProductosVue, beforeEnter: authMiddleware},
    {name: 'unidadmedida', path: '/unidadmedida', component: UnidadMedida, beforeEnter: authMiddleware},
    {name: 'configuracion', path: '/configuracion', component:EmpresaVue, beforeEnter: authMiddleware},
    {name: 'usuarios', path: '/usuarios', component:UsuarioS, beforeEnter: authMiddleware},
    {name: 'comprobantes', path: '/comprobantes', component:ComprobanteS, beforeEnter: authMiddleware},
    {name: 'moneda', path: '/moneda', component:MonedA, beforeEnter: authMiddleware},
    {name: 'compras', path: '/compras', component:CompraS, beforeEnter: authMiddleware},
    {name: 'nuevacompra', path: '/compras/nuevacompra', component:NuevaCompra, beforeEnter: authMiddleware},
    {name: 'compradetalle', path: '/compras/detalle/:id', component:CompraDetalle, beforeEnter: authMiddleware},
    {name: 'almacen', path: '/almacen', component:AlmaceN, beforeEnter: authMiddleware},
    {name: 'pedidos', path: '/pedidos', component:Pedidos, beforeEnter: authMiddleware},
    {name: 'nuevopedido', path: '/pedidos/nuevo', component:NuevoPedido, beforeEnter: authMiddleware},
    {name: 'detallepedido', path: '/pedidos/detalle/:id', component:DetallePedido, beforeEnter: authMiddleware},
    {name: 'caja', path: '/caja', component:Caja, beforeEnter: authMiddleware},
    {name: 'ventas', path: '/ventas', component:Ventas, beforeEnter: authMiddleware},
    {name: 'reporteventas', path: '/reporteventas', component:ReporteVentas, beforeEnter: authMiddleware},
    {name: 'detalleventa', path: '/ventas/detalle/:id', component:DetalleVenta, beforeEnter: authMiddleware},
    {name: 'notacredito', path: '/ventas/notacredito/', component:NotaCredito, beforeEnter: authMiddleware},
    {name: 'nuevanotacre', path: '/ventas/notacredito/nuevo/:id', component:NuevaNotaCred, beforeEnter: authMiddleware},
]

const router = createRouter({
    history:createWebHistory(),
    routes:routes
})

export default router