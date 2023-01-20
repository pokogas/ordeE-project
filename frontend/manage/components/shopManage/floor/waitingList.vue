<template>
  <div>
    <v-row>
      <v-col
        cols="12"
        xl="6"
        lg="6"
        md="6"
        sm="6"
        class="pr-1"
      >
        <v-btn
          block
          elevation="0"
          large
          class="font-weight-medium"
          :class="{'green lighten-1 white--text' : unallocatedType === 'wait', 'white grey--text lighten-4--text' : unallocatedType !== 'wait'}"
          @click="unallocatedType='wait'"
        >
          待機 <span>({{ waitingList.length }})</span>
        </v-btn>
      </v-col>
      <v-col
        cols="12"
        xl="6"
        lg="6"
        md="6"
        sm="6"
        class="pl-1"
      >
        <v-btn
          block
          elevation="0"
          large
          class="font-weight-medium"
          :class="{'green lighten-1 white--text' : unallocatedType === 'reserved', 'white grey--text lighten-4--text' : unallocatedType !== 'reserved'}"
          @click="unallocatedType='reserved'"
        >
          予約 <span>({{ reserveList.length }})</span>
        </v-btn>
      </v-col>
    </v-row>
    <div class="pt-1" />
    <!--リスト-->
    <div v-if="unallocatedType === 'wait'" class="pt-2 pb-3">
      <div class="d-flex">
        <v-select
          v-model="waitingSpaceCount"
          hide-details="auto"
          flat
          dense
          :items="Array.from(Array.from({length: spaceMax}, (_, i) => i+1))"
          label="来店人数"
          solo
        >
          <template #selection="{ item }">
            <div class="grey--text ">
              <span class="font-weight-medium">{{ item }}</span><span>&nbsp;名様</span>
            </div>
          </template>
        </v-select>
        <v-btn color="teal lighten-3" class="mx-2 white--text" elevation="0" :disabled="waitingSpaceCount === null" @click="waitingTicketCreate()">
          番号札発行
        </v-btn>
      </div>
    </div>
    <div class="overflow-x-hidden" :style="`max-height: ${$vuetify.breakpoint.height -200}px`">
      <div v-if="unallocatedType === 'wait'">
        <shop-manage-floor-not-specified-table-card
          v-for="i in waitingList"
          ref="card_child"
          :key="i.id"
          class="my-3"
          :card-data="i"
          @click.native="openDetail(i, 'wait')"
        />
      </div>
      <div v-if="unallocatedType === 'reserved'" class="py-3">
        <shop-manage-floor-reserve-not-specified-table-card
          v-for="i in reserveList"
          ref="reserve_card_child"
          :key="i.id"
          :card-data="i"
          class="my-3"
          @click.native="openDetail(i, 'reserved')"
        />
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    waitingList: {
      type: Array,
      required: true
    },
    reserveList: {
      type: Array,
      required: true
    },
    spaceMax: {
      type: Number,
      required: true
    }
  },
  data () {
    return {
      waitingSpaceCount: null,
      detailView: false,
      unallocatedType: 'wait'
    }
  },
  mounted () {
    setInterval(this.updateTime, 1000)
  },
  methods: {
    openDetail (data, type) {
      this.$emit('openDetailPanel', 'open', data, type)
    },
    waitingTicketCreate () {
      this.$axios.post(`api/manage/floor/create_waiting_ticket/?shop_id=${this.$route.params.shop_id}&space=${this.waitingSpaceCount}`)
    },
    updateTime () {
      for (const i in this.$refs.card_child) {
        this.$refs.card_child[i].updateTime()
      }
      for (const i in this.$refs.reserve_card_child) {
        this.$refs.reserve_card_child[i].updateTime()
      }
    }
  }
}
</script>
<style>
.activeBtn {
  color: #4EBA6A;
}
</style>
