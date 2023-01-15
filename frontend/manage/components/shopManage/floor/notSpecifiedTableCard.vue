<template>
  <v-card>
    <div class="pa-3 d-flex">
      <div>
        <div class="text-body-2 font-weight-bold">
          <span v-if="cardType === `wait`">番号札待機</span>
          <span v-else>酒井 将弘 様</span>
        </div>
        <span class="text-caption font-weight-bold grey--text"># {{ cardData.id }}</span>
      </div>
      <div v-if="cardType === `reserved`" class="ml-auto">
        <v-progress-circular
          :rotate="-90"
          :size="50"
          :width="4"
          :value="20"
          color="red"
        >
          <span style="font-size: 12px">18分</span>
        </v-progress-circular>
      </div>
    </div>
    <v-divider />
    <div class="pa-2 d-flex">
      <div class="text-body-2 font-weight-bold grey--text">
        待機経過時間
      </div>
      <v-spacer />
      <div class="text-end text-caption">
        <span class="red--text text--darken-4 font-weight-bold">{{ $dayjs(now_time).diff(cardData.visits_time, "m") }}</span> 分
      </div>
    </div>
  </v-card>
</template>
<script>
export default {
  props: {
    cardType: {
      type: String,
      required: true
    },
    cardData: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      now_time: new this.$dayjs()
    }
  },
  methods: {
    updateTime () {
      this.now_time = this.$dayjs()
    }
  }
}
</script>
