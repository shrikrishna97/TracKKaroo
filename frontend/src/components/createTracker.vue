<template>
  <div class="container">
        <p class="alert alert-danger" v-if="error">{{error}}</p>
        <p class="alert alert-success" v-if="good">{{ good }}</p>
    <div class="row">
      <div class="col"></div>
      <div class="col-5">
            <br>
            <h3 class="title" align="center">Create A Tracker</h3>
            <div class="from-row">   
                <div class="form-group">
                <label>Tracker Name</label>
                <input type="text" class="form-control " name="tracker_name" id="tracker_name" v-model="tracker_name" placeholder="Please enter Tracker name..."  required  />
                </div>
            </div>
            <div class="from-row">
                <div class="form-group">
                <label>Tracker Description</label>
                <textarea type="text" v-model="tracker_desc" class="form-control" name="tracker_desc" id="tracker_desc" placeholder="Tracker Description" rows="3" ></textarea>
                </div>
            </div>
            <div class="from-row">
                <div class="form-group">
                <label>Tracker Type</label>
                <select v-model="tracker_type" class="form-control" name="tracker_type" id="tracker_type"  required>
                    <option >Numeric</option>
                    <option>Multiple Choice</option>
                    <option>Boolean</option>
                </select>
                </div>
            </div>
            <div v-if="tracker_type === 'Multiple Choice' " class="from-row">
                <div class="form-group">
                <label>Settings</label>
                <textarea type="text" v-model="tracker_settings" class="form-control" name="tracker_settings" id="tracker_settings" placeholder="Tracker settings(Enter different settings as comma separated values)" rows="3" ></textarea>
                </div>
            </div>
            <br><br>
            <button type="submit" @click="addTrack" class="btn btn-dark btn-outline-primary btn-lg">Add Tracker</button>          
      </div>
      <div class="col"></div>
    </div>    
  </div>
  
</template>

<script>

export default {
  name: "createTracker",
  data() {
    return {
        email: null,
        auth_token: null,
        trackers: [],
        error: "",
        good: "",
        tracker_name: null,
        tracker_desc:null,
        tracker_type:null,
        tracker_settings:null
    };
  },
  mounted() {
    this.email = sessionStorage.getItem("email");
    this.auth_token = sessionStorage.getItem("auth-token");
  },
  methods: {
    async addTrack() {
      if (!this.tracker_name || !this.tracker_desc || !this.tracker_type) {
        this.error = "Tracker name or description or type cannot be empty";
      }
       else {
        console.log("all ok")
        try {
          fetch("http://127.0.0.1:5000/api/tracker/"+`${this.email}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json;charset=utf-8",
              "Authentication-Token": `${this.auth_token}`,
            },
            body: JSON.stringify({
              email: this.email,      
              Tracker_name : this.tracker_name,
              Tracker_Description : this.tracker_desc,
              Tracker_Type : this.tracker_type,
              Setting : this.tracker_settings
            }),
          })
            .then((resp) =>  resp.json())
            .then((data) => {
              const response = data;
              if (response.message) {
                this.error = response.message;
                console.log(response.message);
              } else {
                this.tracker = data;
                console.log(this.tracker);
                this.good = data
                console.log("Tracker Added");
                this.$router.go(-1);
                console.log("its dashboard returns");
              }
            })
            .catch((error) => {
              console.log("1st",error);
            });
        } catch (error) {
          console.log("2nd",error);
        }
      }
    },
  },
};


</script>