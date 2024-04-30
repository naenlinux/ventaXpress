<template>
    <div class="hold-transition login-page">
   <div class="login-box">
  <!-- /.login-logo -->
  <div class="card card-outline card-primary">
    <div class="card-header text-center">
      <p class="h1 m-2"><b>Ventas</b>PRO</p>
    </div>
    <div class="card-body">
      <p class="login-box-msg">Ingrese sus credenciales</p>

      <form action="../../index3.html" method="post">
        <div class="input-group mb-3">
          <input type="email" class="form-control" placeholder="Email">
          <div class="input-group-append">
            <div class="input-group-text">
              <span class="fas fa-envelope"></span>
            </div>
          </div>
        </div>
        <div class="input-group mb-3">
          <input type="password" class="form-control" placeholder="Password">
          <div class="input-group-append">
            <div class="input-group-text">
              <span class="fas fa-lock"></span>
            </div>
          </div>
        </div>
        <div class="row">
          <!-- /.col -->
          <div class="col-12">
            <button type="button" @click="login()" class="btn btn-primary btn-block">Ingresar</button>
          </div>
          <!-- /.col -->
        </div>
      </form>
    </div>
    <!-- /.card-body -->
  </div>
  <!-- /.card -->
</div>
<!-- /.login-box -->
</div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: '',
        usuarioAuth:true
      };
    },
    methods: {
      async login() {
        //this.$router.push('compras')
      },
    },
  };
  </script>
  
  <style scoped>
  /* Estilos específicos del componente aquí */
  </style>