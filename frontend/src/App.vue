<template>
  <div :key="logIn" id="app">
    <nav class="navbar shadow   navbar-expand-lg navbar-dark" style="background-color: #00006d;" >
    <div class="container-fluid">
    <a class="navbar-brand" href="#" style="color: rgb(231, 181, 181);"><em> &emsp13; &#160; <strong>Track Karoo</strong></em></a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
    <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
    <div class="navbar-nav me-auto mb-2 mb-lg-0">
      <router-link v-if="logIn === false" class="nav-item nav-link active" to="/">Home</router-link>
      <div class="col-sm-1 col-xs-1 col-md-1 col-lg-1"></div>
      <router-link v-if="logIn === true" class="nav-item nav-link active" to="/dashboard">Dashboard</router-link>  
    </div>
      <router-link v-if="logIn === false" class="nav-item nav-link" style="color: #0d6efd;" to="/login">Login</router-link> 
      <div class="col-sm-1 col-xs-1 col-md-1 col-lg-1"></div>
      <router-link v-if="logIn === false" class="nav-item nav-link" style="color: #0d6efd;" to="/register">Registration</router-link>
      <span v-if="logIn === true" class="navbar-text">LoggedIn as: {{ this.email }}</span>
      <div class="col-sm-1 col-xs-1 col-md-1 col-lg-1"></div>
      <button v-if="logIn === true" @click="logout()" class="btn btn-danger">LogOut</button>
      </div>
      

      </div>
    </nav>
    
    <br><br>
    <router-view />
  </div>
</template>

<script>
export default {
  name: "navBar",
  data() {
    return {
      auth_token: null,
      logIn: false,
      email: null,
    }
  },
  methods: {
    logout() {
      try {
        sessionStorage.clear()
        localStorage.clear()
        this.$router.push("/")
      } 
      catch (error) {
        console.log(error)
      }
    }
  },
  async mounted(){
    let aToken = sessionStorage.getItem("auth-token")
    if (aToken){
      this.logIn = true
      this.email = sessionStorage.getItem("email")
    }
    else {
      this.logIn = false
    }
  },
  async updated() {
    let atoken = sessionStorage.getItem("auth-token");
    if (atoken) {
      this.logIn = true;
      this.email = sessionStorage.getItem("email");
    } else {
      this.logIn = false;
    }
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  /* color: #2c3e50; */
}

nav {
  padding: 30px;
  text-align: center;
}



nav a.router-link-exact-active {
  /* color: #4272b9; */
  color: #42b983;
}
body {
  background: linear-gradient(#21407e, #f19a9a);
}
</style>
