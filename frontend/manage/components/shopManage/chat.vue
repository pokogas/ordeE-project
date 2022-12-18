<template>
  <div>
    <v-expand-transition>
      <v-btn
        v-if="chat_btn"
        fixed
        fab
        color="#FF735D"
        bottom
        right
        elevation="1"
        @click="openMessage()"
      >
        <v-icon color="white">
          mdi-message
        </v-icon>
      </v-btn>
    </v-expand-transition>

    <v-expand-transition>
      <v-card
        v-show="!chat_btn"
        class="card_fixed ma-4"
        max-width="470"
        height="500"
        style="width: 90%"
      >
        <v-system-bar
          color="#FF735D"
          dark
        >
          <span>チャット <span class="font-weight-bold ml-3">{{ category[selectionCategoryIndex].name }}</span></span>
          <v-spacer />
          <v-icon @click="chat_btn=true">
            mdi-window-minimize
          </v-icon>
        </v-system-bar>
        <div>
          <v-container style="background-color: rgb(255,255,255)">
            <div ref="chats" class="overflow-x-hidden" style="height: 330px">
              <div v-for="message in messages" :id="message.id" :key="message.id">
                <div v-if="message.user === null || message.system" class="pb-2 d-flex align-center">
                  <div class="ml-2 mr-2">
                    <v-card style="border: 1px #dcdcdc solid" elevation="0" class="">
                      <v-card-subtitle class="orange darken-1 white--text font-weight-bold">
                        ご注文
                      </v-card-subtitle>
                      <v-card-title>ROOM:{{ message.oc_data.room }}</v-card-title>
                      <v-card-subtitle class="font-weight-bold">
                        OCID:{{ message.oc_data.oc_id }}
                      </v-card-subtitle>
                    </v-card>
                  </div>
                </div>
                <div v-else-if="message.user.id === $auth.user.user.id" class="pb-2 d-flex align-center fromMe">
                  <div class="ml-2 mr-2">
                    <v-card class="pa-1 pl-1 pr-1 white--text" :color="message.category.color">
                      <span>{{ message.message }}</span>
                    </v-card>
                  </div>
                </div>
                <div v-else class="pb-2 d-flex align-center">
                  <v-avatar
                    color="warning lighten-2"
                    size="36"
                    class="align-self-start"
                  />
                  <div class="ml-2 mr-2">
                    <span>{{ message.user.last_name }} {{ message.user.first_name }}</span>
                    <v-card class="pa-1 pl-1 pr-1 white--text" :color="message.category.color">
                      <span>{{ message.message }}</span>
                    </v-card>
                  </div>
                </div>
              </div>
            </div>
            <v-banner />
            <div>
              <div>
                <v-chip-group
                  v-model="selectionCategoryIndex"
                  center-active
                  mandatory
                  active-class="accent-2"
                >
                  <v-chip
                    v-for="Category in category"
                    :key="Category.id"
                    :color="Category.color"
                    :active-class="Category.color"
                    outlined
                  >
                    {{ Category.name }}
                  </v-chip>
                </v-chip-group>
              </div>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="send_message"
                    append-outer-icon="mdi-send"
                    outlined
                    dense
                    hide-details
                    clear-icon="mdi-close-circle"
                    clearable
                    label="メッセージ"
                    type="text"
                    @click:append-outer="addMessage()"
                  />
                </v-col>
              </v-row>
            </div>
          </v-container>
        </div>
      </v-card>
    </v-expand-transition>
  </div>
</template>

<script>
export default {
  data: () => ({
    chat_btn: true,
    send_message: '',
    category: [
      {
        id: 1,
        name: '全体',
        color: 'red lighten-1'
      },
      {
        id: 2,
        name: '注文',
        color: 'orange darken-1'
      }
    ],
    selectionCategoryIndex: 0,
    origin_messages: [],
    messages: [],
    rules: {
      required: value => !!value || '入力してください'
    }
  }),
  watch: {
    messages (newValue) {
      this.scrollToEnd()
    },
    selectionCategoryIndex (newValue) {
      this.messagesFilter(this.category[this.selectionCategoryIndex].id)
    }
  },
  created () {
    this.dataSet()
    this.$store.dispatch('chat/chatConnection', { token: this.$auth.strategy.token.get().slice(4), shopId: this.$route.params.shop_id })
    this.$store.state.chat.websocket.onmessage = (e) => {
      if (typeof e.data === 'string') {
        const res = JSON.parse(e.data)
        this.origin_messages.push(res)
        if (this.chat_btn) {
          this.notOpenChat()
        }
        this.messagesFilter(this.category[this.selectionCategoryIndex].id)
      }
    }
  },
  methods: {
    async dataSet () {
      await this.$axios.get(`api/manage/messages_custom_category?shop_id=${this.$route.params.shop_id}`).then(function (res) {
        for (const resDataKey in res.data) {
          this.category.push(res.data[resDataKey])
        }
      }.bind(this))
      await this.$axios.get(`api/manage/to_day_messages?shop_id=${this.$route.params.shop_id}`).then(function (res) {
        this.messages = res.data
        this.origin_messages = res.data
        this.messagesFilter(1)
      }.bind(this))
    },
    notOpenChat () {
      this.$toast.info('メッセージが届きました。', {
        position: 'top-right',
        timeout: 2029,
        closeOnClick: true,
        pauseOnFocusLoss: false,
        pauseOnHover: true,
        draggable: true,
        draggablePercent: 0.6,
        showCloseButtonOnHover: true,
        hideProgressBar: false,
        closeButton: 'button',
        icon: false,
        rtl: false
      })
    },
    getAccessToken () {
      let token = this.$auth.strategy.token
      token = this.$auth.strategy.token.get().slice(4)
      return token
    },
    openMessage () {
      this.chat_btn = false
      this.scrollToEnd()
    },
    addMessage () {
      if (this.send_message !== '') {
        this.$store.state.chat.websocket.send(JSON.stringify({
          message: this.send_message,
          category_id: this.category[this.selectionCategoryIndex].id
        }))
        this.send_message = ''
      }
    },
    scrollToEnd () {
      const chatLog = this.$refs.chats
      if (!chatLog) { return }
      this.$nextTick(function () {
        chatLog.scrollTo({ top: chatLog.scrollHeight })
      })
    },
    messagesFilter (categoryId) {
      this.messages = this.origin_messages.filter(mes => mes.category.id === categoryId)
    },
    logout () {
      return this.$auth.logout()
    }
  }
}
</script>

<style scoped>
.card_fixed {
  position: fixed;
  bottom: 0;
  right: 0;
}

.fromMe {
  flex-direction: row-reverse;

}
</style>
