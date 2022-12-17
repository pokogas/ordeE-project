<template>
  <v-container>
    <CustomerTab />
    <v-row class="pb-3">
      <v-col
        cols="12"
        sm="6"
        md="6"
        lg="4"
      >
        <CustomerTopTotalOrderAmountCard :total-amount="customer.total_fee" />
      </v-col>
      <v-col
        cols="12"
        sm="6"
        lg="4"
      >
        <CustomerTopOrderItemsCountCard :order-count="orderCount" :order-comp="orderComp" />
      </v-col>
      <v-col
        cols="12"
        sm="12"
        md="12"
        lg="4"
      >
        <CustomerTopOrderHistorys :order="orderHistory" />
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
export default {
  layout: 'customer/default',
  auth: false,
  async asyncData ({ $axios, route }) {
    const customer = await $axios.$get(`api/customer/detail?customer_id=${route.params.id}`)
    const orderHistory = await $axios.$get(`api/customer/order/data?customer_id=${route.params.id}`)
    const orderCount = orderHistory.length
    let orderComp = 0
    for (const i in orderHistory) {
      if (orderHistory[i].status === true) {
        orderComp += 1
      }
    }
    return { customer, orderHistory, orderCount, orderComp }
  }
}
</script>
