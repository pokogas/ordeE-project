<template>
  <div>
    <v-app-bar
      app
      dense
      elevation="0"
      color="white"
    >
      <v-toolbar-title class="font-weight-bold">
        OrdeE <span class="subtitle-1">management</span>
      </v-toolbar-title>
    </v-app-bar>
  </div>
</template>

<script>
export default {
  name: 'ShopManageHeader',
  data () {
    return {
      drawer: null
    }
  }
}
</script>

<style scoped>

</style>
