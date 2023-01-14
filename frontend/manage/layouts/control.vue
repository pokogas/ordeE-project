<template>
  <v-app :style="{ background: $vuetify.theme.themes.light.background }">
    <Header />
    <v-main>
      <v-container class="pt-10">
        <v-row>
          <v-col
            cols="12"
            xl="3"
            lg="3"
            md="0"
            sm="0"
          >
            <sideCard class="d-none d-lg-block d-xl-block" />
          </v-col>
          <v-col xl="9" lg="9" md="12" sm="12">
            <Nuxt />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
export default {
  name: 'Control'
}
</script>

<style lang="scss">

</style>
