<template>
  <v-app :style="{ background: $vuetify.theme.themes.light.background }">
    <Header v-if="$auth.loggedIn" />
    <v-main>
      <Nuxt />
    </v-main>
    <GlobalModal />
  </v-app>
</template>

<script>
export default {
  name: 'Control'
}
</script>
