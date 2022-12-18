<template>
  <div>
    <div v-if="!Confirm">
      <div v-if="directionType === 'ALL'">
        <v-btn block color="green" class="white--text font-weight-bold" @click="Confirm = true">
          お届け完了
        </v-btn>
      </div>
      <div v-else-if="directionType === 'COOK'" @click="Confirm = true">
        <v-btn block color="green" class="white--text font-weight-bold">
          調理完了
        </v-btn>
      </div>
      <div v-else-if="directionType === 'HALL'" @click="Confirm = true">
        <v-btn block color="green" class="white--text font-weight-bold">
          お届け完了
        </v-btn>
      </div>
      <div class="pb-2" />
      <v-btn block color="gray" class="black--text font-weight-bold">
        詳細
      </v-btn>
    </div>
    <div v-else>
      <v-btn block color="white" class="green--text font-weight-bold" @click="buttonConfirm(orderData.id, directionType)">
        確定
      </v-btn>
      <div class="pb-2" />
      <v-btn block color="white" class="red--text font-weight-bold" @click="Confirm = false">
        キャンセル
      </v-btn>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    directionType: {
      required: true,
      type: String
    },
    orderData: {
      required: true,
      type: Object
    }
  },
  data () {
    return {
      Confirm: false
    }
  },
  methods: {
    Comp (orderId) {
      this.$axios.$post(`api/manage/order/order_action/?shop_id=${this.$route.params.shop_id}&direction=COMP&order_id=${orderId}`)
    },
    CookComp (orderId) {
      this.$axios.$post(`api/manage/order/order_action/?shop_id=${this.$route.params.shop_id}&direction=COOK_COMP&order_id=${orderId}`)
    },
    buttonConfirm (orderId, directionType) {
      if (directionType === 'COOK') {
        this.CookComp(orderId)
      } else {
        this.Comp(orderId)
      }
      this.Confirm = false
    }
  }
}
</script>
