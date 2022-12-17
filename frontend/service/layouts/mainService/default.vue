<template>
  <v-app :style="{ background: $vuetify.theme.themes.light.background }">
    <div>
      <Header />
      <v-main>
        <Nuxt />
      </v-main>
    </div>
  </v-app>
</template>
<script>
import Header from '@/components/header'
export default {
  components: {
    Header
  }
}
</script>
