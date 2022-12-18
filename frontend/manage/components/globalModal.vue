<template>
  <v-dialog
    v-model="isActive"
    persistent
    width="600"
  >
    <v-card class="pa-4">
      <div class="text-center py-7">
        <v-icon size="80">
          mdi-lock-alert
        </v-icon>
      </div>
      <div class="text-center font-weight-bold text-h4 py-4">
        権限が必要です。
      </div>
      <div class="text-center caption">
        こちらへのアクセス権限が無いようです、詳しくはシステム管理者にお問い合わせください。
      </div>
      <div class="text-right pt-10">
        <v-btn elevation="0" class="rounded-xl white--text font-weight-bold" color="#FF7417" @click="closeErrorModal">
          閉じる
        </v-btn>
      </div>
    </v-card>
  </v-dialog>
</template>
<script>
import { mapState, mapActions } from 'vuex'

export default {
  computed: {
    ...mapState('global_modal', [
      'message',
      'icon',
      'title',
      'isActive'
    ])
  },
  methods: {
    ...mapActions('global_modal', [
      'closeErrorModal'
    ])
  }
}
</script>
