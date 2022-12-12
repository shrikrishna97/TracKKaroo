<template>
    <div class="container">
        <p class="alert alert-danger" v-if="error_1">{{error_1}}</p>
        <p class="alert alert-danger" v-if="error_1">{{error_2}}</p>
        <div class="row">
        <div class="col"></div>
        <div class="col-5">
            <br>
            <h3 class="title" align="center">Sign Up</h3>
            <div class="form-row">
            <div class="form-group">
                <label>Email Address</label>
                <input type="email" class="form-control " name="email" id="email" v-model="email" placeholder="Please enter a valid email..." pattern="^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$" required />
            </div>
            </div>
            <div class="form-row">
            <div class="form-group">
                <label>Name</label>
                <input type="text" class="form-control " name="username" id="username" v-model="username" placeholder="Please enter your name..." minlength="3" title="Name requires atleast 3 characters. " required />
            </div>
            </div>
            <div class="form-row">
            <div class="form-group">
                <label>Password</label>
                <input type="password" class="form-control " name="password" id="password" v-model="password" placeholder="Provide a valid  password..." minlength="6" title="Password requires atleast 6 characters. "
              pattern=".{6,}" required />
            </div>
            </div>
            <button type="submit" @click="register()" class="btn btn-dark btn-outline-primary btn-lg">Sign Up</button>
 
            <p>
                Already registered 
                 <router-link :to="{name: 'login'}">Log in ?</router-link>
            </p>
        
        </div>
        <div class="col"></div>
        </div>
    </div>
</template>
 
<script>
    export default {
        name:'register',
        data() {
            return {
                email: null,
                username: null,
                password: null,
                error_1: "",
                error_2: ""
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
        methods: {
            async register() {
                try {
                    fetch("http://127.0.0.1:5000/api/user",{
                        method: "POST",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            email: this.email, 
                            username: this.username, 
                            password: this.password 
                        })
                    }).then((response) => response.json())
                    .then(async (data) =>{
                        console.log(data)
                        if(!this.username){this.error_1 = "Please enter a valid username"}
                        if(!this.password){this.error_2 = "Please enter a valid password"}
                        else if(!this.passValidation(this.password)){
                            this.error_2 = "Password requires atleast 6 characters. "
                        }
                        if(!this.email){
                            this.error_1 = "Please enter a valid email"
                            console.log("wrong email")
                        }else if(!this.emailValidation(this.email)){
                            this.error_1 = "Not valid email"
                        }else{this.$router.push("login")}
                    }).catch((err) => {
                        console.log(err)
                    })

                }
                catch (error) {
                    console.log("Registration Failed: ",error)
                }
            },
            emailValidation: function (email){
                var result = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,3}))$/;
                return result.test(email)
            },
            passValidation: function (passs){
                // var result = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}/
                var result = /.{6,}/
                return result.test(passs)
            }
        }
    }
</script>
<style >
input:invalid:focus {
  background-image: linear-gradient(rgb(240, 12, 50), lightgreen);
}
</style>