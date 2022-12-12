<template>
<div class="container">
        <p class="alert alert-danger" v-if="error">{{error}}</p>
        <p class="alert alert-success" v-if="good">{{ good }}</p>
    <div class="row">
      <div class="col"></div>
      <div class="col-5">
        <br>
        <h3 class="title" align="center">Add Logs to {{this.tracker_name}} Tracker</h3>
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
              <select class="form-select"  v-model="value" name="value" id="value" required >
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
    <button type="submit" @click="addLog" class="btn btn-dark btn-lg" style="border-radius: 15px" >
      Add Log
    </button>

  <div class="container">
    <h3>My Logs</h3>
    <!-- <div v-if="this.logs">Please Log Something.Your Tracker is Empty.</div> -->
    <div >
    <table class="table table-dark talbe-striped">
      <thead>
        <tr>
          <th>Serial Number</th>
          <th>Value</th>
          <th>Note</th>
          <th>On</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody v-for="(value,index) in logs" :key="index">
        <td>{{index}}</td>
        <td>{{value.Value}}</td>
        <td>{{value.Note}}</td>
        <td>{{value.date_created}}</td>
        <td><router-link :to="`/addLog/${index}/updateLog`" >
        <button class="btn btn-dark btn-outline-primary btn-lg" @click="storeLog(value.id,value.Value,value.Note)">
          Update</button></router-link></td>
        <td><button type="submit" class="btn btn-dark btn-outline-danger btn-lg" @click="deleteLog(value.id)">
          Delete</button></td>
      </tbody>
    </table>
    </div>
  </div>
  <br>
  <button type="submit" class="btn btn-dark btn-outline-success btn-lg" @click="exportLog">Export Log</button>
<br>
  <div class="container">
    <div class="row">
      <div class="col"></div>
      <div class="col-6">
        <div class="row" v-if="this.tracker_type === 'Boolean' ">
        <!-- <img alt="Boolean Graph " src="../assets/graph_boolean.png" /> -->
            <img :src="`data:image/png;base64,${this.b_file}`"  />

        </div>
        <div class="row" v-if="this.tracker_type === 'Numeric' ">
          <!-- <img alt="Numerical Graph " src="../assets/graph_numeric.png" /> -->
            <img :src="`data:image/png;base64,${this.g_file}`"  />
          </div>
          <div class="row" v-if="this.tracker_type === 'Multiple Choice' ">
            <!-- <img alt="Multiple Choice Graph " src="../assets/graph_multiple.png" /> -->
              <img :src="`data:image/png;base64,${this.m_file}`" />
          </div>
      </div>
      <div class="col"></div>
    </div>
  </div>
  </div>


</template>

<script>

export default {
  name: "addLog",
  data() {
    return {
        id:null,
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
        x:null,
        g_file:null,
        m_file:null,
        b_file:null

    };
  },
  async created() {
    this.id = localStorage.getItem("tracker_id");
    this.email = sessionStorage.getItem("email");
    this.auth_token = sessionStorage.getItem("auth-token");
    console.log(this.id);
    this.tracker_name = localStorage.getItem("tracker_name")
    this.tracker_desc = localStorage.getItem("tracker_desc")
    this.tracker_type = localStorage.getItem("tracker_type")
    this.tracker_settings = localStorage.getItem("tracker_settings")
    var y = this.tracker_settings
    this.x = y.split(",")
    console.log(this.x)
    return fetch(`http://127.0.0.1:5000/api/log/${this.tracker_type}/${this.id}`,{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": `${this.auth_token}`
      }
    }).then((response) => response.json())
    .then((data) =>{
      this.logs = data[0]
      this.g_file = data[1]["base64"]
      this.m_file = data[1]["base64_1"]
      this.b_file = data[1]["base64_2"]
      // console.log(data[0],"kuch hello")
      // console.log(data[1]["base64"],"photo hwllo")
      // console.log(data,"sab hwllo")

      
      // var tracke = JSON.stringify(data);
      //     this.trackers = tracke;
      //     console.log(this.trackers);
    }).catch((error) => console.log("1st",error))
  },
  // mounted() {
  //   this.email = sessionStorage.getItem("email");
  //   this.auth_token = sessionStorage.getItem("auth-token");
  // },
  methods: {
    async addLog() {
      if (!this.value) {
        this.error = "Log value cannot be empty";
      } else {
        console.log("all ok")
        try {
          fetch(`http://127.0.0.1:5000/api/log/${this.tracker_type}/${this.id}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json;charset=utf-8",
              "Authentication-Token": `${this.auth_token}`,
            },
            body: JSON.stringify({
              email: this.email,      
              Note: this.note,
              Value: this.value,
              Tracker_Type : this.tracker_type,
              // Setting : this.tracker_settings
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
                console.log("Log Hua");
                this.$router.go()
                console.log("Logged value");
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
deleteLog(Tid){
    try{
      fetch(`http://127.0.0.1:5000/api/log/${this.id}/${Tid}`,{
        method: "DELETE",
        headers:{
          "Content-Type" : "application/json",
          "Authentication-Token":`${this.auth_token}`
        }
      })
      .then((resp) =>  resp.json())
      .then((data) => {
              const response = data;
              console.log(response)
              if (response.message) {
                this.error = response.message;
                console.log(response.message);
              } else {
                this.good = data
                console.log("Log Deleted");}
                this.$router.go();
            }).catch((error) => {
              console.log("1st",error);
            });

    }catch(error){
      console.log("2nd",error)
    }
  },
  storeLog(idL,Value,Note){
        localStorage.setItem("Value",Value)
        localStorage.setItem("Note",Note)
        localStorage.setItem("id",idL)
      },
      async exportLog(){
        return fetch(`http://127.0.0.1:5000/api/csv/${this.email}/${this.id}`,{
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": `${this.auth_token}`
      }
    }).then((response) => response.json())
    .then((data) => {
      console.log(data)
      this.good = "Please Check your mail and Download the Csv File."
    }).catch((error) => console.log(error))
      }
  }
}
</script>

<style></style>
