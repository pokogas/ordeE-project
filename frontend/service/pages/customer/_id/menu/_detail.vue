<template>
  <div>
    <v-img src="https://cdn.pixabay.com/photo/2014/11/05/15/57/salmon-518032_1280.jpg" max-height="250" gradient="to top right, rgba(100,115,201,.0), rgba(25,32,72,.0)" />
    <v-container class="mb-16">
      <!--detailZone-->
      <div class="font-weight-bold">
        <p class="text-h6 font-weight-bold">
          {{ menu.title }}
        </p>
        <p class="red--text">
          ¥  <span style="font-size: 22px">{{ menu.price | addComma }} <span class="blue-grey--text" style="font-size: 14px">(税込み)</span></span>
        </p>
        <p class="font-weight-bold">
          説明<br>
          <span class="caption">{{ menu.detail }}</span>
        </p>
      </div>
      <v-banner class="pb-4" />
      <!--optionZone-->
      <div>
        <v-form>
          <v-row justify="center">
            <v-expansion-panels v-model="option_panel" accordion flat multiple>
              <v-expansion-panel
                v-for="(option, optionIndex) in menu.option"
                :key="optionIndex"
              >
                <v-expansion-panel-header>{{ option.name }}</v-expansion-panel-header>
                <v-expansion-panel-content>
                  <div>
                    <v-radio-group v-if="option.type === 'radioBtn'" v-model="options[optionIndex]" mandatory @change="menuTotalAmountCalculation">
                      <div
                        v-for="(optionItem, optionItemIndex) in option.optionItems"
                        :key="optionItemIndex"
                        class="d-flex"
                      >
                        <v-radio
                          :value="optionItem"
                          color="red"
                        />
                        <span class="font-weight-bold">{{ optionItem.name }}</span> <span class="grey--text pl-3">¥ {{ optionItem.fee }}</span>
                      </div>
                    </v-radio-group>
                    <div v-if="option.type === 'checkBox'">
                      <div
                        v-for="(optionItem, optionItemIndex) in option.optionItems"
                        :key="optionItemIndex"
                        class="d-flex"
                      >
                        <v-checkbox
                          :id="`option_${optionIndex}_${optionItemIndex}`"
                          :key="optionItemIndex"
                          v-model="options[optionIndex]"
                          :label="optionItem.name"
                          :value="optionItem"
                          color="red"
                          style="margin-top: 0"
                          @change="menuTotalAmountCalculation"
                        >
                          <template #label>
                            <span class="font-weight-bold black--text">{{ optionItem.name }}</span> <span class="grey--text pl-3">¥ {{ optionItem.fee }}</span>
                          </template>
                        </v-checkbox>
                      </div>
                    </div>
                  </div>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-row>
        </v-form>
      </div>
      <!--counterBTN-->
      <div class="pt-10">
        <div class="d-flex align-center justify-center">
          <span class="" @click="countButton('minus')">
            <svg
              style="color: #ff0003"
              xmlns="http://www.w3.org/2000/svg"
              width="40"
              height="40"
              fill="currentColor"
              class="bi bi-dash-circle"
              viewBox="0 0 16 16"
            >
              <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
              <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z" />
            </svg>
          </span>
          <span
            class="no-copy"
            style="padding-right: 10px;padding-left: 10px;font-size: 18px;color: #FE6363;font-weight: bold;"
          >{{ count }}</span>
          <span class="" @click="countButton('plus')">
            <svg
              style="color: #61f568"
              xmlns="http://www.w3.org/2000/svg"
              width="40"
              height="40"
              fill="currentColor"
              class="bi bi-plus-circle"
              viewBox="0 0 16 16"
            >
              <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
              <path
                d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"
              />
            </svg>
          </span>
        </div>
      </div>
      <!-- errorBar -->
      <v-snackbar
        v-model="error_bar"
        :timeout="timeout"
      >
        {{ error_bar_text }}
      </v-snackbar>
    </v-container>
    <!--footerZone-->
    <v-footer fixed style="background-color: white; padding: 0">
      <v-container>
        <v-row>
          <v-col cols="3">
            <nuxt-link :to="`/customer/${$route.params.id}/menu`">
              <div class="grey text-center pa-2 rounded-lg">
                <span class="white--text font-weight-medium font-weight-bold">戻る</span>
              </div>
            </nuxt-link>
          </v-col>
          <v-col cols="9">
            <div class="red accent-2 pa-2 rounded-lg d-flex" @click="addCart">
              <span v-if="!buy_able" class="pl-2 white--text font-weight-medium font-weight-bold">売り切れ</span>
              <span v-else class="pl-2 white--text font-weight-medium font-weight-bold">カートに追加</span>
              <span style="margin-left:auto; font-size: 16px" class="pl-2 white--text pr-2">¥ <span class="font-weight-bold">{{ total_amount | addComma }}</span></span>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </div>
</template>
<script>
export default {
  auth: false,
  middleware: 'customer/customerConfirmationMiddleware',
  async asyncData ({ $axios, route }) {
    const menu = await $axios.$get(`api/customer/menu/detail?customer_id=${route.params.id}&menu_id=${route.params.detail}`)
    for (const menuOptionIndex in menu.option) {
      for (const optionItemIndex in menu.option[menuOptionIndex].optionItems) {
        menu.option[menuOptionIndex].optionItems[optionItemIndex].cat = `${menu.option[menuOptionIndex].name}`
      }
    }
    return { menu }
  },
  data () {
    return {
      usableBtn: true,
      radioGroup: 1,
      options: [],
      count: 1,
      buy_able: false,
      option_panel: [],
      total_amount: 0,
      error_bar: false,
      error_bar_text: '',
      timeout: 2000
    }
  },
  created () {
    this.setBuyAble()
    this.setOption()
    this.optionRadioBtnPanelSpecification()
    this.menuTotalAmountCalculation()
  },
  methods: {
    addCart () {
      if (!this.usableBtn) {
        return
      }
      this.usableBtn = false
      if (!this.buy_able) {
        this.error_bar_text = 'メニューの在庫がございません。'
        this.buy_able = false
        this.error_bar = true
        return
      }
      const data = {
        menu_id: this.menu.id,
        count: this.count,
        option: this.options,
        action: 'ADD'
      }
      this.$axios.post(`api/customer/cart/action?customer_id=${this.$route.params.id}`, data).then(function () {
        return this.$router.replace({ path: `/customer/${this.$route.params.id}/menu` })
      }.bind(this)).catch(function (res) {
        if (res.response.data.detail.error === 'stockError') {
          this.error_bar_text = 'メニューの在庫がございません。'
          this.buy_able = false
        } else {
          this.error_bar_text = '予期せぬエラーが発生しました、もう一度お試しください。'
        }
        this.error_bar = true
      }.bind(this))
    },
    setOption () {
      // eslint-disable-next-line no-unused-vars
      for (const option in this.menu.option) {
        this.options.push([])
      }
    },
    optionRadioBtnPanelSpecification () {
      const options = this.menu.option
      for (const option in options) {
        if (options[option].type === 'radioBtn') {
          this.option_panel.push(Number(option))
        }
      }
    },
    menuTotalAmountCalculation () {
      const options = this.options
      let totalAmount = 0
      totalAmount += this.menu.price
      for (const optionBoxIndex in options) {
        if (Array.isArray(options[optionBoxIndex])) {
          for (const optionIndex in options[optionBoxIndex]) {
            totalAmount += options[optionBoxIndex][optionIndex].fee
          }
        } else {
          totalAmount += options[optionBoxIndex].fee
        }
      }
      totalAmount *= this.count
      this.total_amount = totalAmount
    },
    getMenuStock () {
      if (this.menu.sold_out) {
        return 0
      }
      if (!this.menu.stock_unlimited) {
        if (this.menu.stock < 1) {
          return 0
        }
        return this.menu.stock
      }
      // 無制限STOCKの1回の注文の購入上限は100個まで
      return 100
    },
    countButton (type) {
      if (type === 'plus' && this.count < this.getMenuStock()) {
        this.count += 1
      } else if (type === 'minus' && this.count > 1) {
        this.count += -1
      }
      this.menuTotalAmountCalculation()
    },
    setBuyAble () {
      const stock = this.menu.stock
      const stockUnlimited = this.menu.stock_unlimited
      const soldOut = this.menu.sold_out
      // eslint-disable-next-line no-mixed-operators
      if (stock < 1 && !stockUnlimited || soldOut) {
        // eslint-disable-next-line no-return-assign
        return this.buy_able = false
      }
      // eslint-disable-next-line no-return-assign
      return this.buy_able = true
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
</style>
