<template>
<div class="container">
        <p class="alert alert-danger" v-if="error">{{error}}</p>
        <p class="alert alert-success" v-if="good">{{ good }}</p>
    <div class="row">
      <div class="col"></div>
      <div class="col-5">
        <br>
        <h3 class="title" align="center">Update Logs of {{this.tracker_name}} Tracker</h3>
        <h5 class="title" align="center">Tracker Type: {{this.tracker_type}} </h5>
        <div class="form-row" v-if="this.tracker_type === 'Numeric' ">
          <div class="form-group">
            <label>Value</label>
            <input type="number" class="form-control" name="value" id="value" v-model="value" required />
          </div>
        </div>
        <div class="form-row" v-else-if="this.tracker_type === 'Multiple Choice' ">
          <div class="form-group">
            <label>Value</label>
              <select class="form-select" v-model="value" name="value" id="value" required >
                <option v-for="opt in this.x" :key="opt" >{{opt}}</option>
              </select>
          </div>
        </div>
        <div class="form-row" v-else-if="this.tracker_type === 'Boolean' ">
          <div class="form-group">
            <label>Value</label>
            <input type="radio"  name="value" id="value" v-model="value" value="Yes" required />
            <label for="value">Yes</label>
            <input type="radio"  name="value" id="value" v-model="value" value="No" />
            <label for="value">No</label>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Note</label>
            <textarea type="text" class="form-control" v-model="note" name="name" id="name" placeholder="Type any note about the log" rows="3"></textarea>
          </div>
        </div>
      </div>
      <div class="col"></div>
    </div>
  
<br>
    <button type="submit" @click="updateLog" class="btn btn-dark btn-outline-primary btn-lg" style="border-radius: 15px" >
      Update Log
    </button>
</div>
</template>

<script>
export default {
    name: "updateLog",
    data() {
        return {
        id:null,
        idL:null,
        email: null,
        auth_token: null,
        trackers: [],
        logs: {},
        error: "",
        good: "",
        tracker_name: null,
        tracker_desc:null,
        tracker_type:null,
        tracker_settings:null,
        note:null,
        value:null,
        x:null
        }
    },
    async created() {
        this.idL = localStorage.getItem("id");
        this.id = localStorage.getItem("tracker_id")
        console.log(this.idL);
        console.log(this.id);
        this.email = sessionStorage.getItem("email");
        this.auth_token = sessionStorage.getItem("auth-token");
        this.tracker_name = localStorage.getItem("tracker_name")
        this.tracker_desc = localStorage.getItem("tracker_desc")
        this.tracker_type = localStorage.getItem("tracker_type")
        this.tracker_settings = localStorage.getItem("tracker_settings")
        this.value = localStorage.getItem("Value")
        this.note = localStorage.getItem("Note")
        var y = this.tracker_settings
        this.x = y.split(",")
        console.log(this.x)

    },
    methods: {
        async updateLog() {
        if (!this.tracker_name) {
        this.error = "Tracker name cannot be empty";
      } else {
        console.log("all ok")
        try {
          fetch(`http://127.0.0.1:5000/api/log/${this.id}/${this.idL}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json;charset=utf-8",
              "Authentication-Token": `${this.auth_token}`,
            },
            body: JSON.stringify({
              email: this.email,      
              Tracker_name : this.tracker_name,
              Note : this.note,
              Value : this.value
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
                console.log("its AddLog returns");
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
    }

}
</script>