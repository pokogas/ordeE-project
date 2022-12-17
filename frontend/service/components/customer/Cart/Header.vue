<template>
  <div>
    <nuxt-link :to="`/customer/${$route.params.id}/`">
      <v-icon style="color: #282828">
        mdi-arrow-left
      </v-icon>
    </nuxt-link>
    <p class="font-weight-bold pb-4 text-center">
      カート <span>0 点</span>
    </p>
  </div>
</template>
<style scoped>
a {
  text-decoration: none;
}
</style>
