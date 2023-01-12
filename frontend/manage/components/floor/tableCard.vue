<template>
  <v-card class="pa-2" elevation="0">
    <div class="d-flex">
      <div class="font-weight-bold align-self-center">
        {{ tableData.name }}
      </div>
      <v-spacer />
      <v-chip small class="white--text font-weight-medium" :color="getStatusChip(tableData)[1]">
        {{ getStatusChip(tableData)[0] }}
      </v-chip>
    </div>
    <v-divider class="my-1" />
    <div class="py-8">
      詳細
    </div>
    <div class="d-flex justify-space-around">
      <v-btn elevation="0" class="rounded-xl white--text font-weight-bold" small color="#4AB0A0">
        アクション1
      </v-btn>
      <v-btn elevation="0" class="rounded-xl white--text font-weight-bold" small color="#4AB0A0">
        アクション2
      </v-btn>
    </div>
  </v-card>
</template>
<script>
export default {
  props: {
    tableData: {
      type: Object,
      required: true
    },
    actions: {
      type: Object,
      required: true
    }
  },
  methods: {
    getStatusChip (tableData) {
      switch (tableData.status) {
        case 0:
          return [`予約 #${tableData.reserve.reserver_id}`, '#ea9612']
        case 1:
          return ['空席', '#93DA65']
        case 2:
          return ['使用中', '#FA5353']
        case 3:
          return ['準備中', '#bbbbbb']
      }
    }
  }
}
</script>
