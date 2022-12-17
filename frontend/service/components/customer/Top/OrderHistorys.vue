<template>
  <v-card elevation="0">
    <v-expansion-panels>
      <v-expansion-panel class="py-8">
        <v-expansion-panel-header>
          <span class="font-weight-bold">
            注文履歴
          </span>
        </v-expansion-panel-header>
        <v-expansion-panel-content id="expansion-panel-content-1">
          <div v-for="value in order" :key="value.id">
            <div class="d-flex">
              <v-avatar class="ma-3 rounded-lg" size="85" tile>
                <v-img src="https://cdn.pixabay.com/photo/2014/11/05/15/57/salmon-518032_1280.jpg" alt="" />
              </v-avatar>
              <div class="pa-3">
                <p class="font-weight-bold pb-2">
                  {{ value.menu.title }}
                </p>
                <p style="font-size: 14px" class="font-weight-medium">
                  ¥ {{ value.amount | addComma }}
                </p>
                <v-chip
                  small
                  :color="getConvertedStatus (value.status, 'color')"
                  style="font-size: 12px; color: #EFEFEF"
                >
                  {{ getConvertedStatus(value.status, 'text') }}
                </v-chip>
              </div>
            </div>
            <v-divider />
          </div>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-card>
</template>
<script>
export default {
  props: {
    order: {
      type: Array,
      required: true
    }
  },
  methods: {
    getConvertedStatus (status, type) {
      let text = '調理中'
      let color = 'red'
      if (status) {
        text = 'お届け済'
        color = 'green'
      }
      if (type === 'text') {
        return text
      } else if (type === 'color') {
        return color
      }
    }
  }
}
</script>
<style scoped>
p {
  margin-bottom: 0;
}
.v-expansion-panel-content::v-deep(.v-expansion-panel-content__wrap) {
  padding: 0 !important;
}
</style>
