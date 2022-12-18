<template>
  <v-card
    elevation="1"
    min-width="300"
    max-width="300"
    class="mr-5"
    outlined
  >
    <v-container>
      <span style="font-size: 14px"># {{ orderData.id }}</span>
      <p style="font-size: 18px" class="font-weight-bold">
        {{ orderData.menu.title }}
      </p>
      <ShopManageOrderCardTable :order-data="orderData" />
      <div class="mb-1" />
      <ShopManageOrderCardAction :order-data="orderData" :direction-type="directionType" />
    </v-container>
  </v-card>
</template>
<script>
export default {
  props: {
    directionType: {
      type: String,
      required: true
    },
    orderData: {
      type: Object,
      required: true
    }
  }
}
</script>
<style scoped>
p {
  margin: 0;
}
</style>
