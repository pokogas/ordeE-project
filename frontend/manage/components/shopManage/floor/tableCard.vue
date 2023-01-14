<template>
  <v-card class="pa-2" elevation="0">
    <div style="cursor: pointer;" @click="overlay=true">
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
    </div>
    <v-overlay
      :absolute="absolute"
      :value="overlay"
      z-index="1000"
      class="pa-1"
      @click="overlay=false"
    >
      <div>
        <div v-if="tableData.status === 0">
          <v-btn class="mb-2" block small color="orange" elevation="0">
            チェックイン
          </v-btn>
          <v-btn class="mb-2" block small color="red" elevation="0">
            予約席解除
          </v-btn>
        </div>
        <div v-else-if="tableData.status === 1">
          <v-btn class="mb-2" block small color="orange" elevation="0">
            利用に変更
          </v-btn>
          <v-btn class="mb-2" block small color="red" elevation="0">
            準備中に変更
          </v-btn>
        </div>
        <div v-else-if="tableData.status === 2">
          <v-btn class="mb-2" block small color="green" elevation="0">
            お会計
          </v-btn>
          <v-btn class="mb-2" block small color="orange" elevation="0">
            注文
          </v-btn>
        </div>
        <div v-else-if="tableData.status === 3">
          <v-btn class="mb-2" block small color="green" elevation="0">
            空席に変更
          </v-btn>
        </div>
      </div>
    </v-overlay>
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
  data () {
    return {
      absolute: true,
      overlay: false
    }
  },
  methods: {
    getStatusChip (tableData) {
      switch (tableData.status) {
        case 0:
          if (tableData.reserve !== null) {
            return [`予約 #${tableData.reserve.reserver_id}`, '#ea9612']
          }
          return ['エラー', '#ff0000']
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
