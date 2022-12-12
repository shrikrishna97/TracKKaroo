<template>
  <div class="container">
        <p class="alert alert-danger" v-if="error">{{error}}</p>
        <p class="alert alert-success" v-if="good">{{ good }}</p>
    <div class="row">
      <div class="col"></div>
      <div class="col-5">
            <br>
            <h3 class="title" align="center">Update {{this.tracker_type}} Tracker</h3>
            <div class="form-row">   
                <div class="form-group">
                <label>Tracker Name</label>
                <input type="text" class="form-control " name="tracker_name" id="tracker_name" v-model="tracker_name" placeholder="Please enter Tracker name..."  required  />
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                <label>Tracker Description</label>
                <textarea type="text" v-model="tracker_desc" class="form-control" name="tracker_desc" id="tracker_desc" placeholder="Tracker Description" rows="3" ></textarea>
                </div>
            </div>
            <div v-if="tracker_type === 'Multiple Choice' " class="form-row">
                <div class="form-group">
                <label>Settings</label>
                <textarea type="text" v-model="tracker_settings" class="form-control" name="tracker_settings" id="tracker_settings" placeholder="Tracker settings(Enter different settings as comma separated values)" rows="3" ></textarea>
                </div>
            </div>
            <br><br>
            <button type="submit" @click="updateTrack" class="btn btn-dark btn-outline-primary btn-lg">Update Tracker</button>          
      </div>
      <div class="col"></div>
    </div>    
  </div>
  
</template>

<script>

export default {
  name: "updateTracker",
  data() {
    return {
        id:null,
        email: null,
        auth_token: null,
        trackers: [],
        error: "",
        good: "",
        tracker_name: null,
        tracker_desc:null,
        tracker_type:null,
        tracker_settings:null,
        time_updated:null
    };
  },
  async created() {
    this.id = localStorage.getItem("tracker_id");
    console.log(this.id);
    this.email = sessionStorage.getItem("email");
    this.auth_token = sessionStorage.getItem("auth-token");
    this.tracker_name = localStorage.getItem("tracker_name")
    this.tracker_desc = localStorage.getItem("tracker_desc")
    this.tracker_type = localStorage.getItem("tracker_type")
    this.tracker_settings = localStorage.getItem("tracker_settings")
  },
  mounted() {
    this.email = sessionStorage.getItem("email");
    this.auth_token = sessionStorage.getItem("auth-token");
  },
  methods: {
    async updateTrack() {
      if (!this.tracker_name) {
        this.error = "Tracker name cannot be empty";
      } else {
        console.log("all ok")
        try {
          fetch(`http://127.0.0.1:5000/api/tracker/${this.email}/${this.id}`, {
            method: "PUT",
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
                console.log("Tracker Updated");
                this.$router.go(-1)
                console.log("its dashboard returns");
                this.time_updated = new Date().toLocaleString().replace(",","").replace(/:.. /," ")
                console.log(this.time_updated)
                sessionStorage.setItem("time_updated",this.time_updated)
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