<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    
  </div>
</template>

<script>

export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
  async created() {
    sessionStorage.clear()
    localStorage.clear()
  },
    async updated() {
    sessionStorage.clear()
    localStorage.clear()
  }
};

</script>
<style  scoped>
* {
  box-sizing: border-box;
}

</style>

