<template>
  <v-card elevation="0" style="cursor: pointer;">
    <div class="pa-3 d-flex">
      <div>
        <div class="text-body-2 font-weight-bold">
          <span>{{ cardData.reserver_account.first_name }} {{ cardData.reserver_account.last_name }} 様</span>
        </div>
        <span class="text-caption font-weight-bold grey--text"># {{ cardData.reserver_id }}</span>
      </div>
      <div class="ml-auto">
        <v-progress-circular
          :rotate="-90"
          :size="53"
          :width="4"
          :value="time_circular('value')"
          :color="time_circular('getColor')"
        >
          <span style="font-size: 12px">{{ time_circular("formattedTime") }}</span>
        </v-progress-circular>
      </div>
    </div>
    <v-divider />
    <div class="pa-2 d-flex">
      <div class="text-body-2 font-weight-bold grey--text">
        来店時刻
      </div>
      <v-spacer />
      <div class="text-end text-caption">
        <span :class="`${time_circular('getColor')}--text text--darken-4 font-weight-bold`">{{ $dayjs(cardData.reservation_date).format("HH時mm分") }} ~ </span>
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
    },
    time_circular (type) {
      switch (type) {
        case 'getColor':
          if (this.time_circular('value') <= 60) {
            return 'red'
          } else if (this.time_circular('value') <= 100) {
            return 'amber'
          } else {
            return 'green'
          }
        case 'formattedTime':
          if (this.time_circular('value') <= 360) {
            return `${this.time_circular('value')}分`
          } else {
            return `${this.$dayjs(this.cardData.reservation_date).diff(this.now_time, 'h')}時間`
          }
        case 'value':
          return this.$dayjs(this.cardData.reservation_date).diff(this.now_time, 'm')
      }
    }
  }
}
</script>
