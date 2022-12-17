<template>
  <v-app :style="{ background: $vuetify.theme.themes.light.background }">
    <div>
      <Header />
      <v-main>
        <Nuxt />
      </v-main>
      <CartButton />
    </div>
  </v-app>
</template>
<script>
import Header from '@/components/header'
import CartButton from '~/components/customer/cartButton'
export default {
  components: {
    Header,
    CartButton
  },
  middleware: 'customer/customerConfirmationMiddleware'
}
</script>
