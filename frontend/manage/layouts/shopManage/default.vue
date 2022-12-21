<template>
  <v-app :style="{ background: $vuetify.theme.themes.light.background }">
    <ShopManageHeader />
    <v-main>
      <v-container fluid>
        <Nuxt />
      </v-container>
    </v-main>
    <!--<ShopManageChat />-->
    <GlobalModal />
  </v-app>
</template>

<script>
export default {
  name: 'Default'
}
</script>
