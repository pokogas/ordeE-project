<template>
  <v-card class="pa-3" elevation="0">
    <v-row>
      <v-col cols="6">
        <p style="font-size: 12px">
          注文数
        </p>
        <p style="font-size: 26px" class="pl-3">
          {{ orderCount }} <span style="color: #707070; font-size: 17px">点</span>
        </p>
      </v-col>
      <v-col cols="6">
        <p style="font-size: 12px">
          お届け済
        </p>
        <p style="font-size: 26px" class="pl-3">
          {{ orderComp }} <span style="color: #707070; font-size: 17px">点</span>
        </p>
      </v-col>
    </v-row>
  </v-card>
</template>
<script>
export default {
  props: {
    orderCount: {
      type: Number,
      required: true
    },
    orderComp: {
      type: Number,
      required: true
    }
  }
}
</script>
