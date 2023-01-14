<template>
  <div />
</template>
<script>
export default {
  created () {
    this.$store.dispatch('action/actionConnection', { token: this.$auth.strategy.token.get().slice(4), shopId: this.$route.params.shop_id })
    this.$store.state.action.websocket.onmessage = (m) => {
      if (typeof m.data === 'string') {
        console.log('action')
      }
    }
  }
}
</script>
