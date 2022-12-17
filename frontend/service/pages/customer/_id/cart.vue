<template>
  <v-container>
    <!-- /TODO カート商品が０の場合空注文出来てしまうため注文できないようにする -->
    <nuxt-link :to="`/customer/${$route.params.id}/`">
      <v-icon style="color: #282828">
        mdi-arrow-left
      </v-icon>
    </nuxt-link>
    <div style="padding-bottom: 100px">
      <p class="font-weight-bold pb-4 text-center">
        カート <span>{{ cart.length }} 点</span>
      </p>
      <div>
        <div v-for="cartItem in sortedCart" :key="cartItem.id">
          <v-card elevation="0" class="mb-2" @click="cartDialogOpen(cartItem)">
            <div class="d-flex">
              <v-avatar class="ma-3 rounded-lg" size="85" tile>
                <v-img src="https://cdn.pixabay.com/photo/2014/11/05/15/57/salmon-518032_1280.jpg" alt="" />
              </v-avatar>
              <v-list-item style="padding: 0 10px 0 0;">
                <v-list-item-content>
                  <p class="pb-1 font-weight-medium">
                    {{ cartItem.menu.title }}
                  </p>
                  <!-- //TODO optionはここでforを回してください めんどくさい場合オプションありなしで表示。-->
                  <p class="pb-1" style="font-size: 0.775rem">
                    サイズ: 大きい
                  </p>
                  <p style="font-size: 0.955rem" class="pb-1 text--primary font-weight-bold">
                    ¥ {{ cartItem.amount | addComma }}
                  </p>
                </v-list-item-content>

                <v-list-item-action>
                  <div />
                  <div>
                    <div class="d-flex align-center justify-center">
                      <span
                        class="no-copy"
                        style="padding-right: 10px;padding-left: 10px;font-size: 18px;color: #FE6363;font-weight: bold;"
                      >{{ cartItem.count }} <span style="font-size: 14px">個</span></span>
                    </div>
                  </div>
                </v-list-item-action>
              </v-list-item>
            </div>
          </v-card>
        </div>
      </div>
    </div>
    <!-- カート編集ダイアログ -->
    <v-bottom-sheet v-model="cart_dialog.open" persistent class="fullscreen" scrollable>
      <v-card v-if="cart_dialog.open">
        <v-img src="https://cdn.pixabay.com/photo/2014/11/05/15/57/salmon-518032_1280.jpg" max-height="250" gradient="to top right, rgba(100,115,201,.0), rgba(25,32,72,.0)" />
        <v-container class="overflow-auto">
          <div>
            <p class="font-weight-bold pb-3 text-h6">
              {{ cart_dialog.before_change_cart_data.menu.title }}
            </p>
            <p class="red--text pb-3">
              ¥  <span style="font-size: 22px">{{ cart_dialog.amount | addComma }}</span>
            </p>
            <div class="pl-2">
              <p class="pb-2 font-weight-black">
                オプション
              </p>
              <div class="pl-2">
                <div
                  v-for="(option, optionIndex) in cart_dialog.before_change_cart_data.menu.option"
                  :key="optionIndex"
                >
                  <p>
                    {{ option.name }}
                  </p>
                  <div>
                    <div v-if="option.type === 'checkBox'">
                      <div
                        v-for="(optionItem, optionItemIndex) in cart_dialog.before_change_cart_data.option[optionIndex]"
                        :key="optionItemIndex"
                      >
                        <p>・{{ optionItem.name }}</p>
                      </div>
                    </div>
                    <div v-else-if="option.type === 'radioBtn'">
                      <p>・{{ cart_dialog.cart_data.option[optionIndex].name }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="pt-10 mb-3">
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
              >{{ cart_dialog.count }}</span>
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
          <div>
            <v-btn
              block
              elevation="0"
              large
              class="mb-3 rounded-0"
              @click="cartItemRemove('DELETE')"
            >
              カートから消去
            </v-btn>
            <v-btn
              block
              elevation="0"
              large
              class="mb-3 rounded-0 white--text"
              color="grey darken-4"
              @click="cartDialogClose('CLOSE')"
            >
              閉じる
            </v-btn>
          </div>
        </v-container>
      </v-card>
    </v-bottom-sheet>
    <!--footerZone-->
    <v-footer fixed style="background-color: transparent; padding: 0">
      <v-container>
        <div class="pb-7">
          <v-card class="pa-3" elevation="0">
            <div class="d-flex">
              <p class="font-weight-bold">
                メニュー合計料金 ({{ cart.length }}点)
              </p>
              <p style="margin-left:auto; font-size: 16px">
                ¥ {{ cartTotalAmount | addComma }}
              </p>
            </div>
          </v-card>
        </div>
        <v-btn block elevation="0" class="red accent-1 pa-2 rounded-xl" @click="order_dialog.open = true">
          <p class="pl-2 white--text font-weight-medium font-weight-bold text-center">
            注文
          </p>
        </v-btn>
      </v-container>
    </v-footer>
    <!-- 注文確定確認ダイアログ -->
    <v-bottom-sheet v-model="order_dialog.open" persistent>
      <v-card>
        <v-container>
          <div class="pt-3">
            <v-btn
              block
              elevation="0"
              large
              class="mb-3 rounded-0"
              @click="order_dialog.open = false"
            >
              閉じる
            </v-btn>
            <v-btn
              :disabled="usableBtn !== true"
              :loading="usableBtn !== true"
              block
              elevation="0"
              large
              class="mb-3 rounded-0 white--text"
              color="grey darken-4"
              @click="orderFixing()"
            >
              注文を確定する
            </v-btn>
          </div>
        </v-container>
      </v-card>
    </v-bottom-sheet>
    <!-- 注文在庫エラーダイアログ -->
    <v-bottom-sheet v-model="stock_error_dialog.open" scrollable>
      <v-card v-if="stock_error_dialog" class="overflow-x-hidden">
        <v-container>
          <v-icon x-large class="d-flex align-center justify-center pb-2">
            mdi-exclamation-thick
          </v-icon>
          <p class="text-center">
            以下のメニューは売り切れまたは在庫数が<br>限られています、変更してください。
          </p>
          <div class="pt-3">
            <div>
              <v-card v-for="errorItem in stock_error_dialog.data" :key="errorItem.id" elevation="0" class="mb-2">
                <div class="d-flex">
                  <v-avatar class="ma-3 rounded-lg" size="85" tile>
                    <v-img src="https://cdn.pixabay.com/photo/2014/11/05/15/57/salmon-518032_1280.jpg" alt="" />
                  </v-avatar>
                  <div class="pa-3">
                    <p>
                      {{ errorItem.menu.title }}
                    </p>
                    <p
                      class="d-inline-block text-truncate"
                      style="font-size: 12px ; max-width: 180px;"
                    >
                      option
                    </p>
                    <div class="d-flex">
                      <p style="font-size: 15px" class="font-weight-medium">
                        ¥ {{ errorItem.menu.price | addComma }}
                      </p>
                      <div class="pr-1" />
                      <v-chip v-if="!errorItem.menu.stock_unlimited && 1 <= errorItem.menu.stock && errorItem.menu.stock <= 5 && !errorItem.menu.sold_out" color="red lighten-1" small style="font-size: 11px" class="white--text">
                        残り <span class="font-weight-bold">{{ errorItem.menu.stock }}</span> 点
                      </v-chip>
                      <v-chip v-else-if="!errorItem.menu.stock_unlimited && errorItem.menu.stock <= 0 || errorItem.menu.sold_out" color="red lighten-1" small style="font-size: 11px" class="white--text">
                        <span class="font-weight-bold">SOLD</span>
                      </v-chip>
                    </div>
                  </div>
                </div>
              </v-card>
            </div>
          </div>
        </v-container>
      </v-card>
    </v-bottom-sheet>
    <!-- errorBar -->
    <v-snackbar
      v-model="error_bar"
      :timeout="timeout"
    >
      {{ error_bar_text }}
    </v-snackbar>
  </v-container>
</template>
<script>
export default {
  auth: false,
  middleware: 'customer/customerConfirmationMiddleware',
  async asyncData ({ $axios, route }) {
    const cart = await $axios.$get(`api/customer/cart/data?customer_id=${route.params.id}`)
    return {
      cart
    }
  },
  data () {
    return {
      usableBtn: true,
      cart_dialog: {
        open: false,
        cart_data: null,
        before_change_cart_data: null,
        count: 0,
        amount: 0,
        before_change_count: 0,
        usableBtn: true
      },
      order_dialog: {
        open: false,
        usableBtn: true
      },
      stock_error_dialog: {
        open: false,
        data: null,
        usableBtn: true
      },
      error_bar: false,
      error_bar_text: '',
      timeout: 2000
    }
  },
  computed: {
    sortedCart () {
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      return this.cart.sort((a, b) => {
        return a.id - b.id
      })
    },
    cartTotalAmount () {
      let amount = 0
      for (const cartIndex in this.cart) {
        amount += this.cart[cartIndex].amount
      }
      return amount
    }
  },
  created () {
  },
  methods: {
    stockErrorSetData (data) {
      data = data.filter((v1, i1, a1) => {
        return a1.findIndex(v => v1.menu.id === v.menu.id) === i1
      })
      this.stock_error_dialog.data = data
    },
    orderFixing () {
      this.usableBtn = false
      setTimeout(() => (this.dialog = false))
      this.$axios.post(`api/customer/order/action?customer_id=${this.$route.params.id}`).then(function () {
        return this.$router.replace({ path: `/customer/${this.$route.params.id}/` })
      }.bind(this)).catch(function (res) {
        if (res.response.data.detail.error === 'stockError') {
          this.stockErrorSetData(res.response.data.detail.soldMenus)
          this.stock_error_dialog.open = true
          this.order_dialog.open = false
        } else {
          this.error_bar_text = '予期せぬエラーが発生しました、もう一度お試しください。'
          this.error_bar = true
        }
      }.bind(this))
    },
    async cartItemRemove (type) {
      const data = {
        cart_id: this.cart_dialog.cart_data.id,
        action: 'REMOVE'
      }
      await this.$axios.post(`api/customer/cart/action?customer_id=${this.$route.params.id}`, data)
      this.cartDialogClose(type)
      this.$nuxt.refresh()
    },
    getMenuStock () {
      const menuData = this.cart_dialog.before_change_cart_data.menu
      if (menuData.sold_out) {
        return 0
      }
      if (!menuData.stock_unlimited) {
        if (menuData.stock < 1) {
          return 0
        }
        return menuData.stock
      }
      // 無制限STOCKの1回の注文の購入上限は100個まで
      return 100
    },
    countButton (type) {
      if (type === 'plus' && this.cart_dialog.count < this.getMenuStock()) {
        this.cart_dialog.count += 1
      } else if (type === 'minus' && this.cart_dialog.count > 1) {
        this.cart_dialog.count += -1
      }
      const price = this.cart_dialog.before_change_cart_data.amount / this.cart_dialog.before_change_cart_data.count
      this.cart_dialog.amount = this.cart_dialog.count * price
    },
    cartDialogDataSet (data) {
      this.cart_dialog.cart_data = data
      this.cart_dialog.before_change_cart_data = data
      this.cart_dialog.count = data.count
      this.cart_dialog.amount = data.amount
      this.cart_dialog.before_change_count = data.count
    },
    cartDialogOpen (data) {
      this.cartDialogDataSet(data)
      this.cart_dialog.open = true
    },
    async cartItemEditPost () {
      const data = {
        cart_id: this.cart_dialog.cart_data.id,
        count: this.cart_dialog.count,
        action: 'CHANGE'
      }
      await this.$axios.post(`api/customer/cart/action?customer_id=${this.$route.params.id}`, data).catch(function (res) {
        if (res.response.data.detail.error === 'stockError') {
          this.error_bar_text = 'メニューの在庫の在庫が指定した数ございません。'
        } else {
          this.error_bar_text = '予期せぬエラーが発生しました、もう一度お試しください。'
        }
        this.error_bar = true
      }.bind(this))
      this.$nuxt.refresh()
    },
    cartDialogClose (type) {
      if (this.cart_dialog.count !== this.cart_dialog.before_change_count && type === 'CLOSE') {
        this.cartItemEditPost()
      }
      this.cart_dialog.cart_data = null
      this.cart_dialog.before_change_cart_data = null
      this.cart_dialog.open = false
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
