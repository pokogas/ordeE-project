<template>
  <div>
    <v-btn
      text
      icon
      color="blue-grey darken-1"
      @click="closeDetail"
    >
      <v-icon>
        mdi-arrow-left
      </v-icon>
    </v-btn>
    <div class="pb-2" />
    <div v-if="detailType === 'reserved'">
      <v-card class="pa-3 py-4 rounded-lg" elevation="0">
        <div class="caption text-center grey--text text--darken-2">
          来店予約時刻
        </div>
        <div class="font-weight-bold text-h4 text-center">
          {{ $dayjs(detailData.reservation_date).format("HH:mm ~") }}
        </div>
      </v-card>
      <div class="pb-9" />
      <div class="d-flex grey--text text--darken-2">
        <div class="font-weight-bold">
          予約ID
        </div>
        <v-spacer />
        <div class="font-weight-medium grey--text text--darken-2">
          # {{ detailData.reserver_id }}
        </div>
      </div>
      <div class="pb-3" />
      <div class="d-flex grey--text text--darken-2">
        <div class="font-weight-bold">
          ご予約様名
        </div>
        <v-spacer />
        <div class="font-weight-medium grey--text text--darken-2">
          {{ detailData.reserver_account.last_name }} {{ detailData.reserver_account.first_name }} 様
        </div>
      </div>
      <div class="pb-3" />
      <div class="d-flex grey--text text--darken-2">
        <div class="font-weight-bold">
          来店人数
        </div>
        <v-spacer />
        <div class="font-weight-medium grey--text text--darken-2">
          {{ detailData.reserve_num }} 名様
        </div>
      </div>
    </div>
    <div v-if="detailType === 'wait'">
      <v-card class="pa-3 py-4 rounded-lg" elevation="0">
        <div class="caption text-center grey--text text--darken-2">
          待機時間
        </div>
        <div class="font-weight-bold text-h4 text-center">
          {{ $dayjs().diff(detailData.visits_time, "m") }} 分
        </div>
      </v-card>
      <div class="pb-3" />
      <div class="d-flex grey--text text--darken-2">
        <div class="font-weight-bold">
          来店時刻
        </div>
        <v-spacer />
        <div class="font-weight-medium">
          {{ $dayjs(detailData.visits_time).format("HH時mm分") }}
        </div>
      </div>
      <div class="pb-3" />
      <div class="d-flex grey--text text--darken-2">
        <div class="font-weight-bold">
          来店人数
        </div>
        <v-spacer />
        <div class="font-weight-medium">
          {{ detailData.space }} 名様
        </div>
      </div>
    </div>
    <div class="pb-3" />
    <v-divider />
    <div class="pb-3" />
    <div class="overflow-x-hidden" :style="`max-height: ${$vuetify.breakpoint.height -300}px`">
      <div class="font-weight-bold grey--text text--darken-2">
        割り当て可能テーブル
      </div>
      <div class="pb-2" />
      <v-card v-for="(i, index) in getAppropriateRooms()" :key="index" class="pa-3 mb-2" flat>
        <div class="d-flex grey--text text--darken-2">
          <div class="font-weight-bold">
            {{ i.name }}
          </div>
          <v-spacer />
          <div class="font-weight-regular">
            {{ i.space }} 人まで
          </div>
        </div>
        <div class="pb-3" />
        <v-btn block elevation="0" color="blue lighten-3" class="white--text">
          テーブル割り当て
        </v-btn>
      </v-card>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    detailData: {
      type: Object,
      required: true
    },
    detailType: {
      type: String,
      required: true
    },
    rooms: {
      type: Array,
      required: true
    }
  },
  data () {
    return {}
  },
  watch: {
    rooms: {
      handler () {
        this.getAppropriateRooms()
      },
      deep: true
    }
  },
  methods: {
    getAppropriateRooms () {
      let space = ''
      if (this.detailType === 'wait') {
        space = this.detailData.space
      } else if (this.detailType === 'reserve') {
        space = this.detailData.reserve_num
      }
      return this.rooms.filter(room => room.status === 1 && room.space >= space)
    },
    closeDetail () {
      this.$emit('closeDetailPanel', 'close')
    }
  }
}
</script>
