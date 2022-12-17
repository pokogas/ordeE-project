<template>
  <v-footer v-if="cart_data.length > 0" fixed style="background-color: transparent;">
    <v-container>
      <v-btn
        height="40"
        block
        elevation="0"
        class="rounded-lg pa-2 text-center center-block"
        color="#FF8686"
        :to="`/customer/${$route.params.id}/cart/`"
      >
        <span class="white--text font-weight-bold">
          カート <span class="font-weight-bold" />{{ cart_data.length }} 点
        </span>
      </v-btn>
    </v-container>
  </v-footer>
</template>
<script>
export default {
  data () {
    return {
      cart_data: ''
    }
  },
  created () {
    this.setCartData()
  },
  methods: {
    setCartData () {
      this.$axios.$get(`api/customer/cart/data?customer_id=${this.$route.params.id}`).then(function (res) {
        this.cart_data = res
      }.bind(this))
    }
  }
}
</script>
