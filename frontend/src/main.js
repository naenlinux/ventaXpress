import { createApp } from 'vue'
import App from './App.vue'

import 'admin-lte/plugins/fontawesome-free/css/all.min.css'
import 'admin-lte/plugins/tempusdominus-bootstrap-4/css/tempusdominus-bootstrap-4.min.css'
import 'admin-lte/plugins/icheck-bootstrap/icheck-bootstrap.min.css'
import 'admin-lte/dist/css/adminlte.min.css'
//import 'admin-lte/plugins/overlayScrollbars/css/OverlayScrollbars.min.css'

//import 'admin-lte/plugins/jquery/jquery.min.js'
import 'admin-lte/plugins/bootstrap/js/bootstrap.bundle.min.js'
import 'admin-lte/dist/js/adminlte.js'
import 'admin-lte/plugins/popper/popper.js'
//import 'admin-lte/plugins/overlayScrollbars/js/jquery.overlayScrollbars.min.js'

import 'admin-lte/plugins/select2/js/select2.js'
import 'admin-lte/plugins/select2/css/select2.min.css'

import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';

import toastr  from 'toastr'
import 'toastr/build/toastr.min.css'

import router from './router'

import axios from 'axios'

import VueNativeSock from 'vue-native-websocket-vue3'


axios.defaults.withCredentials = true;

const app = createApp(App)
app.config.globalProperties.$axios = axios
window.axios = axios
app.use(router)
app.use(VueSweetalert2)
app.use(VueNativeSock, 'ws://localhost:8000/ws/productos/',{
    //format: 'json', // Formato de mensajes (puedes personalizarlo)
    reconnection: true, // Habilita la reconexión automática
    reconnectionAttempts: 5, // Número de intentos de reconexión
    reconnectionDelay: 3000,

})
app.config.globalProperties.$toastr = toastr;
app.mount('#app')

toastr.options.timeOut = 2000; //configurar el tiempo de dismis de toastr a 2 segundos
