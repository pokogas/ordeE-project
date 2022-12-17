<template>
  <v-card class="pa-3" elevation="0">
    <div>
      <p style="font-size: 12px">
        合計注文金額
      </p>
      <p style="font-size: 26px" class="pl-3">
        <span style="color: #707070; font-size: 17px">¥</span> {{ totalAmount | addComma }}
      </p>
    </div>
  </v-card>
</template>
<script>
export default {
  props: {
    totalAmount: {
      type: Number,
      required: true
    }
  }
}
</script>
