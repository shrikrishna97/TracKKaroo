<template>
  <div class="home">
    <img alt="TracK Karoo logo" src="../assets/logo.jpg" />
    <HelloWorld msg="Welcome to TracK Karoo App" />
        <div class="container-fluid">
    <p style="text-align:center">
      <h4 style="text-align: center;color:brown;font-size:large;font-family:Verdana;"> 
        The quantified self (QS) is, any individual engaged in the self-tracking of any kind of biological, physical, behavioral, or environmental information. 
                    There is a proactive stance toward obtaining information and acting on it. A variety of areas may be tracked and analyzed, for example, weight, energy level, mood, time usage, sleep quality, health, cognitive performance, athletics, and learning strategies. 
                    Health is an important but not exclusive focus, where objectives may range from general tracking to pathology resolution to physical and mental performance enhancement.</h4>
                    <h3 style="font-size: medium;font-style: oblique; color:black;">So, this is a small help from my end to your betterment.Use this webapp to <span style="color:blue">tracker your habbits</span>.</h3>
            </p>
                
                </div>
                
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";
// import login from "@/components/login.vue";
// import register from "@/components/registration.vue";

export default {
  name: "HomeView",
  components: {
    HelloWorld,
  },
};
</script>
