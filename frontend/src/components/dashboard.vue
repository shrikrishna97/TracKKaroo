<template>
<div>
    <p class="alert alert-danger" v-if="error">{{ error }}</p>
    <p class="alert alert-success" v-if="good">{{ good }}</p> 
    <h3>My Dashboard</h3>
    <table class="table table-dark table-striped">
        <thead>
            <tr>
            <th>Serial Number</th>
            <th>Tracker name</th>
            <th>Tracker Description</th>
            <th>Tracker Type</th>
            <th>Tracker settings</th>
            <th>Date Created</th>
            <th>Add TrackerLog</th>
            <th>Actions</th>
            </tr>
        </thead>
        <tbody v-for="(value, index) in trackers" :key="index">
            <td>{{ index }}</td>
            <td>{{ value.Tracker_name }}</td>
            <td>{{ value.Tracker_Description }}</td>
            <td>{{ value.Tracker_Type }}</td>
            <td>{{ value.Setting }}</td>
            <td>{{ value.date_created }}</td>
            <td><router-link :to="`/addLog/${index}`" >
            <button class="btn btn-dark btn-outline-success btn-lg" @click="storeID(value.id); storeData(value.Tracker_name,value.Tracker_Description,value.Tracker_Type,value.Setting)">
                  +Addlog</button></router-link></td>
            <td><router-link :to="`/dashboard/${value.id}/updateTracker`" >
            <button class="btn btn-dark btn-outline-primary btn-lg" @click="storeID(value.id); storeData(value.Tracker_name,value.Tracker_Description,value.Tracker_Type,value.Setting)">
                  Update</button></router-link></td>
            <td><button type="submit" class="btn btn-dark btn-outline-danger btn-lg" @click="deleteTrack(value.id)">Delete</button></td>

        </tbody>
    </table>

    <router-link to="/createTracker"><button class="btn btn-dark btn-outline-warning btn-lg">Click to add trackers</button></router-link> 
    <br>
    <button type="submit" class="btn btn-dark btn-outline-success btn-lg" @click="exportTrack">Export trackers</button>
</div>
</template>

<script>
export default {
 name: "UserDashboard",
  data() {
    return {
      email: null,
      auth_token: null,
      trackers: {},
      error: "",
      good: "",
      time: null
    };
  },
  async created() {
    localStorage.removeItem("tracker_id")
    localStorage.clear()
    this.time = sessionStorage.getItem("time_updated")
    console.log(this.time)
    this.auth_token = sessionStorage.getItem("auth-token")
    this.email = sessionStorage.getItem("email")
    console.log(this.email)
    return fetch(`http://127.0.0.1:5000/api/tracker/${this.email}`,{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": `${this.auth_token}`
      }
    }).then((response) => response.json())
    .then((data) =>{
      this.trackers = data
      console.log(data)
    }).catch((error) => console.log("1st",error))
  },
  
  methods:{
  deleteTrack(Tid){
    try{
      fetch(`http://127.0.0.1:5000/api/tracker/${this.email}/${Tid}`,{
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
                console.log("Tracker Deleted");}
                this.$router.go();
            }).catch((error) => {
              console.log("1st",error);
            });

    }catch(error){
      console.log("2nd",error)
    }
  },
    storeID(iid){
    localStorage.setItem("tracker_id",iid)
  },
  storeData(Tracker_name,Tracker_Description,Tracker_Type,Setting){
    localStorage.setItem("tracker_name",Tracker_name)
    localStorage.setItem("tracker_desc",Tracker_Description)
    localStorage.setItem("tracker_type",Tracker_Type)
    localStorage.setItem("tracker_settings",Setting)
  },
  async exportTrack() {
    return fetch(`http://127.0.0.1:5000/api/export/tracker/${this.email}`,{
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": `${this.auth_token}`
      }
    }).then((response) => response.json())
    .then((data) => {
      console.log(data)
      this.good = "Please Check your mail and Download the Csv File."
      // this.$router.go();
    }).catch((error) => console.log(error))
  }
  }
}
</script>