<template>
  <v-container>
    <div>
      <v-sheet class="pa-2 rounded-lg" height="100">
        <p class="text-h6 font-weight-bold black--text">
          WEB予約ページ
        </p>
      </v-sheet>
      <div class="pb-4" />
      <v-row>
        <v-col cols="12" xl="8" lg="8" md="12" sm="12">
          <v-sheet class="pa-2 rounded-lg">
            <div class="pb-4">
              <p class="font-weight-bold black--text pb-3">
                店舗
              </p>
              <v-card
                v-if="selected_shop === null"
                elevation="0"
                class="mb-2 py-8 rounded-lg"
                style="border: solid rgba(86,84,84,0.45) 2px"
                @click="openShopsModal"
              >
                <div style="text-align: center;" class="grey--text lighten-2">
                  店舗を選択
                </div>
              </v-card>
              <MainServiceReserveShopCard v-else :selecting="true" :shop-data="selected_shop" @openShopsModal="openShopsModal" />
            </div>
            <div v-if="selected_shop !== null">
              <div class="pb-4">
                <p class="pb-3 font-weight-bold black--text">
                  人数
                </p>
                <div>
                  <v-chip-group
                    v-model="customers.selection"
                    center-active
                    mandatory
                    class="green--text darken-4--text"
                  >
                    <v-chip
                      v-for="tag in customers.max_selection"
                      :key="tag"
                    >
                      <span class="px-2 font-weight-bold grey--text text--darken-3">{{ tag }} 人</span>
                    </v-chip>
                  </v-chip-group>
                </div>
              </div>

              <div class="pb-4">
                <p class="pb-3 font-weight-bold black--text">
                  ご来店日
                </p>
                <div>
                  <v-chip-group
                    v-model="visits_date.selection"
                    center-active
                    class="green--text darken-4--text"
                    change
                  >
                    <v-chip
                      v-for="(value, key , index) in visits_date.data"
                      :key="key"
                      :disabled="dayReservableDecision(value) === 'disabled'"
                      :class="GetBorder(dayReservableDecision(value))"
                      outlined
                      @click="visits_time.data = value; visits_time.selection = undefined"
                    >
                      <span v-if="$dayjs().format('YYYY-MM-DD') === key" :id="index" class="px-1 font-weight-black grey--text text--darken-3">今日</span>
                      <span v-else :id="index" class="px-1 font-weight-black grey--text text--darken-3">{{ $dayjs(key).format("M/D (ddd)") }}</span>
                    </v-chip>
                  </v-chip-group>
                </div>
              </div>
              <div v-if="visits_date.selection !== undefined" class="pb-4">
                <p class="pb-3 font-weight-bold black--text">
                  ご来店時間
                </p>
                <div>
                  <v-chip-group
                    v-model="visits_time.selection"
                    center-active
                    class="green--text darken-4--text"
                  >
                    <v-chip
                      v-for="(value, key , index) in visits_time.data"
                      :key="key"
                      :disabled="timeReservableDecision(value) === 'disabled'"
                      :class="GetBorder(timeReservableDecision(value))"
                      outlined
                    >
                      <span :id="index" class="px-1 font-weight-black grey--text text--darken-3">{{ $dayjs(key).format("HH:mm") }}</span>
                    </v-chip>
                  </v-chip-group>
                </div>
              </div>
            </div>
          </v-sheet>
        </v-col>
        <v-col cols="12" xl="4" lg="4" md="12" sm="12">
          <v-sheet elevation="0" class="rounded-lg">
            <div class=" pa-4">
              <p class="caption">
                ここに予約の説明を載せます
              </p>
            </div>
            <v-expand-transition>
              <div v-if="AllSelectCheck">
                <div class="pb-4 pa-4">
                  <div class="text-center font-weight-bold grey--text text--darken-1">
                    <div class="pb-1" style="font-size: 20px">
                      {{ selected_shop.name }}
                    </div>
                    <div class="pb-1" style="font-size: 20px">
                      {{ customers.selection + 1 }}名様
                    </div>
                    <div class="pb-1" style="font-size: 14px">
                      {{ $dayjs(Object.keys(visits_time.data)[visits_time.selection]).format("YYYY/MM/DD") }}
                    </div>
                    <div class="pb-1" style="font-size: 27px">
                      {{ $dayjs(Object.keys(visits_time.data)[visits_time.selection]).format("HH:mm") }} ~ {{ $dayjs(Object.keys(visits_time.data)[visits_time.selection]).add(10, 'm').format("HH:mm") }}
                    </div>
                  </div>
                  <div>
                    <v-btn
                      large
                      block
                      class="rounded-lg"
                      color="#52B41A"
                      elevation="0"
                      :disabled="usableBtn !== true"
                      :loading="usableBtn !== true"
                      @click="reserving"
                    >
                      <span class="white--text font-weight-bold">上記の内容で予約する</span>
                    </v-btn>
                  </div>
                </div>
              </div>
            </v-expand-transition>
          </v-sheet>
        </v-col>
      </v-row>
    </div>
    <v-dialog
      v-model="shopsModal"
      width="600"
      content-class="elevation-0"
    >
      <div v-for="shop in shops" :key="shop.id">
        <MainServiceReserveShopCard :selecting="false" :shop-data="shop" @selectShop="selectShop" />
      </div>
    </v-dialog>
    <v-dialog
      v-model="result.dialog"
      persistent
      width="600"
      content-class="elevation-0"
    >
      <v-sheet>
        <div class="text-center pa-12">
          <v-icon size="80" color="#80E293">
            mdi-check-circle-outline
          </v-icon>
          <div class="py-2" />
          <div class="font-weight-bold" style="font-size: 22px">
            予約を受け付けました。
          </div>
          <div class="py-2" />
          <div>
            <div>予約時間: {{ $dayjs(result.data.reservation_date).format("HH:mm") }} ~ {{ $dayjs(result.data.reservation_date).add(10, 'm').format("HH:mm") }}</div>
            <div>来店人数: {{ result.data.reserve_num }}</div>
            <div>予約ID: <span class="font-weight-bold red--text">{{ result.data.reserver_id }}</span></div>
            <span class="caption">上記のIDはチェックインする際に使用しますので保存しておいてください。</span><br>
            <span class="caption">予約IDはマイページからも確認できます。</span>
          </div>
          <div class="py-2" />
          <nuxt-link to="/">
            ホームに戻る
          </nuxt-link>
        </div>
      </v-sheet>
    </v-dialog>
  </v-container>
</template>
<script>
export default {
  layout: 'mainService/default',
  async asyncData ({ $axios }) {
    const shops = await $axios.$get('api/service/reservation/get_reservation_shops')
    return {
      shops
    }
  },
  data () {
    return {
      usableBtn: true,
      result: {
        dialog: false,
        data: []
      },
      selected_shop: null,
      selected_shop_setting: null,
      customers: {
        selection: null,
        max_selection: null
      },
      visits_date: {
        data: [],
        selection: null
      },
      visits_time: {
        data: [],
        selection: null
      },
      shopsModal: false
    }
  },
  computed: {
    AllSelectCheck () {
      return this.selected_shop !== null && this.customers.selection !== null && this.visits_date.selection !== undefined && this.visits_time.selection !== undefined
    }
  },
  created () {
  },
  methods: {
    reserving () {
      this.usableBtn = false
      const data = {
        shop_id: this.selected_shop.id,
        reserved_datetime: Object.keys(this.visits_time.data)[this.visits_time.selection],
        reserve_num: this.customers.selection + 1
      }
      this.$axios.post('api/service/reservation/reserving', data).then(function (res) {
        this.result.data = res.data
        this.result.dialog = true
      }.bind(this)).catch(function (res) {
        location.reload()
      })
    },
    openShopsModal () {
      this.shopsModal = true
    },
    selectionsInit () {
      this.customers.selection = null
      this.visits_date.selection = undefined
      this.visits_time.selection = undefined
      this.visits_date.data = null
      this.visits_time.data = null
    },
    reservationTotalValue (data) {
      return Object.values(data).reduce((sum, i) => sum + i, 0)
    },
    setShopData (shopId) {
      this.$axios.$get(`api/service/reservation/get_shop_reservation_datetime?shop_id=${shopId}`).then(function (res) {
        this.selectionsInit()
        this.customers.max_selection = res.setting.max_visits_count
        this.selected_shop_setting = res.setting
        this.visits_date.data = res.datetime
      }.bind(this))
    },
    selectShop (shopData) {
      this.selected_shop = shopData
      this.setShopData(shopData.id)
      this.shopsModal = false
    },
    timeReservableDecision (value) {
      const reservationCount = value
      const setting = this.selected_shop_setting
      const countReservableDaily = setting.one_hour_max_reservation
      if (countReservableDaily <= reservationCount) {
        return 'disabled'
      } else if (countReservableDaily / 2 <= reservationCount) {
        return 'onlyAFew'
      } else {
        return 'possible'
      }
    },
    dayReservableDecision (value) {
      const reservationCount = this.reservationTotalValue(value)
      const setting = this.selected_shop_setting
      const countReservableDaily = setting.one_hour_max_reservation * Object.values(value).length
      if (countReservableDaily <= reservationCount) {
        return 'disabled'
      } else if (countReservableDaily / 2 <= reservationCount) {
        return 'onlyAFew'
      } else {
        return 'possible'
      }
    },
    GetBorder (level) {
      if (level === 'disabled') {
        return 'red-border'
      } else if (level === 'onlyAFew') {
        return 'yellow-border'
      } else if (level === 'possible') {
        return 'green-border'
      }
    }
  }
}
</script>
<style scoped>
p {
  margin-bottom: 0;
}
a {
  text-decoration: none;
}
.theme--light.v-chip--active:hover::before, .theme--light.v-chip--active::before {
  opacity: 0.3
}
.red-border {
  border: solid rgba(255, 0, 0, 0.38) 2px;
}
.yellow-border {
  border: solid rgba(255, 177, 48, 0.55) 2px;
}
.green-border {
  border: solid rgba(124, 225, 124, 0.66) 2px;
}
</style>
