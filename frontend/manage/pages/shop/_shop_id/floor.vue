<template>
  <div>
    <v-row>
      <v-col cols="12" xl="10" lg="9" md="9">
        <v-row>
          <v-col cols="12" xl="3" lg="6" md="6">
            <board-items-card :items-data="status_data" :cols="[6,6,6,3,3]" />
          </v-col>
          <v-col cols="12" xl="2" lg="4" md="6">
            <board-items-card :items-data="waiting_data" :cols="[6,6,12,6,6]" />
          </v-col>
          <v-col class="d-flex align-self-center" cols="12" xl="7" lg="6" md="12" />
        </v-row>
        <v-sheet max-height="600" class="overflow-auto overflow-x-hidden" color="#EFEFEF">
          <v-row>
            <v-col
              v-for="(room, i) in rooms"
              :key="i"
              cols="12"
              xl="2"
              lg="3"
              md="4"
              sm="6"
            >
              <span @click="room.status = 1">{{ room.space }}</span>
              <shop-manage-floor-table-card :table-data="room" table-status="a" />
            </v-col>
          </v-row>
        </v-sheet>
        <div class="mb-2" />
      </v-col>
      <v-col
        cols="12"
        xl="2"
        lg="3"
        md="3"
        class="d-none d-md-block d-lg-block d-xl-block"
        style="background-color: #e0e0e0"
        :style="`height: ${$vuetify.breakpoint.height -50}px`"
      >
        <v-window v-model="sidePanelView">
          <v-window-item :value="1">
            <shop-manage-floor-waiting-list
              v-show="sidePanelView === 1"
              :waiting-list="waitingList"
              :reserve-list="reserveList"
              :space-max="getSpaceRange('max')"
              @openDetailPanel="detailPanelAction"
            />
          </v-window-item>
          <v-window-item :value="2">
            <v-fade-transition>
              <shop-manage-floor-waiting-detail
                v-show="sidePanelView === 2"
                :detail-data="detail.data"
                :detail-type="detail.type"
                :rooms="rooms"
                @closeDetailPanel="detailPanelAction"
              />
            </v-fade-transition>
          </v-window-item>
        </v-window>
      </v-col>
    </v-row>
  </div>
</template>
<script>
export default {
  layout: 'shopManage/default',
  async asyncData ({ $axios, route }) {
    const rooms = await $axios.$get(`api/manage/floor/get_rooms/?shop_id=${route.params.shop_id}`)
    const waitingList = await $axios.$get(`api/manage/floor/get_waiting_list/?shop_id=${route.params.shop_id}`)
    const reserveList = await $axios.$get(`api/manage/floor/get_today_reserve_list/?shop_id=${route.params.shop_id}`)
    return { rooms, waitingList, reserveList }
  },
  data () {
    return {
      status_data: [
        { title: '空席', asg: 0 },
        { title: '予約', asg: 0 },
        { title: '利用中', asg: 0 },
        { title: '準備中', asg: 0 }
      ],
      waiting_data: [
        { title: '待ち人数', asg: 0 },
        { title: '組', asg: 0 }
      ],
      sidePanelView: 1,
      detail: {
        data: [],
        type: ''
      }
    }
  },
  watch: {
    rooms: {
      handler () {
        this.statusDataUpdate()
      },
      deep: true
    }
  },
  mounted () {
    this.statusDataUpdate()
  },
  methods: {
    detailPanelAction (...args) {
      switch (args[0]) {
        case 'close':
          this.sidePanelView = 1
          this.detail.data = {}
          this.detail.type = ''
          break
        case 'open':
          this.sidePanelView = 2
          this.detail.data = args[1]
          this.detail.type = args[2]
          break
      }
      this.$emit('openDetail')
    },
    openDetail () {
      this.sidePanelView = 2
    },
    statusDataUpdate () {
      for (const i in this.status_data) {
        this.status_data[Number(i)].asg = this.rooms.filter(u => u.status === Number(i)).length
      }
    },
    getSpaceRange (type) {
      const space = this.rooms.map(function (p) {
        return p.space
      })
      switch (type) {
        case 'max':
          return Math.max.apply(null, space)
        case 'min':
          return Math.min.apply(null, space)
      }
    },
    settingUpdate () {
      location.reload()
    }
  }
}
</script>
<style scoped>
p {
  margin: 0;
}
</style>
