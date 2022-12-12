<template>
    <div class="container">
        <p class="alert alert-danger" v-if="error_1">{{error_1}}</p>
        <p class="alert alert-danger" v-if="error_2">{{error_2}}</p>
        <div class="row">
        <div class="col"></div>
        <div class="col-5">
            <br>
            <h3 class="title" align="center">Log In</h3>
            <div class="from-row">   
                <div class="form-group">
                <label>Email Address</label>
                <input type="email" class="form-control " name="email" id="email" v-model="email" placeholder="Please enter a valid email..." pattern="^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$" required  />
                </div>
            </div>
            <div class="from-row">
            <div class="form-group">
                <label>Password</label>
                <input type="password" class="form-control " name="password" id="password" v-model="password" placeholder="Provide a valid  password..." minlength="6" title="Password requires atleast 6 characters. "
              pattern=".{6,}" required/>
                </div>
            </div>
            <br>
            <button type="submit" @click="login" class="btn btn-dark btn-outline-primary btn-lg">Log In</button>
 
            <p class="forgot-password text-right mt-2 mb-4">
                Not yet Registered ?
                <router-link to="/register">Register here</router-link>
            </p>
            </div>
            <div class="col"></div>
        </div>
    </div>
</template>
 
<script>
    export default {
        name: 'login',
        data() {
            return {
                email:null,
                password:null,
                error_1:"",
                error_2:"",
                auth:null,
                is_authenticated: false
            }
        },
        async created() {
            sessionStorage.clear()
            localStorage.clear()
        },
        async updated() {
            sessionStorage.clear()
            localStorage.clear()
        },
        methods:{
            async login() {
                try {
                    fetch("http://127.0.0.1:5000/login?include_auth_token",{
                        method: "POST",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            email: this.email, password: this.password 
                        })
                    }).then((respons) => respons.json())
                    .then(async (data) =>{
                        const { response } = data;
                        console.log(data);
                        if (response.errors) {
                            if (response.errors[1]) {
                                this.error_1 = response.errors[1];
                            }
                            this.error_password = response.errors[0];
                            console.log(this.error_1, this.error_2);
                        } 
                        else {
                            this.auth = response.user.authentication_token;
                            sessionStorage.setItem( "auth-token", this.auth);
                            sessionStorage.setItem("email", this.email);
                            this.$router.push("dashboard");
                            console.log("its dashboard");
                        }
                    })
                    .catch((error) => {
                        console.log("some error first time",error)
                    })
                } 
                catch(error){
                    console.log("No way home: ", error)
                }
            }
        }
    }
</script>

<style>
input:invalid:focus {
  background-image: linear-gradient(rgb(240, 12, 50), white);
}
</style>