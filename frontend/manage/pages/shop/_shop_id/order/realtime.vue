<template>
  <div>
    <p class="subtitle-2 font-weight-bold">
      注文
    </p>
    <div class="mb-3" />
    <div class="text-h5 font-weight-bold">
      リアルタイム注文
    </div>
    <v-tabs v-model="tab" background-color="#EFEFEF">
      <v-tab class="font-weight-bold">
        全体
      </v-tab>
      <v-tab class="font-weight-bold">
        厨房
      </v-tab>
      <v-tab class="font-weight-bold">
        ホール
      </v-tab>
    </v-tabs>
    <v-divider />
    <div class="mb-6" />
    <div>
      <div class="d-flex overflow-x-auto lighten-5 flex-nowrap">
        <div v-for="order in orders" :id="order.id" :key="order.id">
          <div v-if="tab === 0">
            <ShopManageOrderCard :order-data="order" direction-type="ALL" />
          </div>
          <div v-if="tab === 1">
            <div v-if="order.cook_status === false">
              <ShopManageOrderCard :order-data="order" direction-type="COOK" />
            </div>
          </div>
          <div v-if="tab === 2">
            <div v-if="order.cook_status === true">
              <ShopManageOrderCard :order-data="order" direction-type="HALL" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- list式orderライン -->
  </div>
</template>

<script>
export default {
  layout: 'shopManage/default',
  async asyncData ({ $axios, route }) {
    const orders = await $axios.$get(`api/manage/order/get_orders/?shop_id=${route.params.shop_id}`)
    return { orders }
  },
  data () {
    return {
      tab: null,
      order_alarm: new Audio(require('@/assets/mp3/order-alarm.mp3'))
    }
  },
  created () {
    this.$store.dispatch('order/orderConnection', { token: this.$auth.strategy.token.get().slice(4), shopId: this.$route.params.shop_id })
    this.$store.state.order.websocket.onmessage = (m) => {
      if (typeof m.data === 'string') {
        const res = JSON.parse(m.data)
        if (res.direction === 'ORDER') {
          this.addOrder(JSON.parse(res.orders))
          if (this.tab === 0 || this.tab === 1) {
            this.order_alarm.play()
          }
        } else if (res.direction === 'COOK_COMP') {
          this.cookComp(Number(res.order_id))
          if (this.tab === 1) {
            this.order_alarm.play()
          }
        } else if (res.direction === 'COMP') {
          this.Comp(Number(res.order_id))
        }
      }
    }
  },
  methods: {
    addOrder (orders) {
      for (const order in orders) {
        this.orders.push(orders[order])
      }
    },
    cookComp (orderId) {
      const orderIndex = this.orders.findIndex(Order => Order.id === orderId)
      this.orders[orderIndex].cook_status = true
    },
    Comp (orderId) {
      const orderIndex = this.orders.findIndex(Order => Order.id === orderId)
      this.$delete(this.orders, orderIndex)
    }
  }
}
</script>

<style scoped>
p {
  margin: 0;
}
</style>
