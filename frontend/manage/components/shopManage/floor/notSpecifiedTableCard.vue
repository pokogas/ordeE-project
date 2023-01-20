<template>
  <v-card elevation="0" style="cursor: pointer;">
    <div class="pa-3 d-flex">
      <div>
        <div class="text-body-2 font-weight-bold">
          <span>番号札待機</span>
        </div>
        <span class="text-caption font-weight-bold grey--text"># {{ cardData.id }}</span>
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
