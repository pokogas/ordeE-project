<template>
  <v-dialog
    v-model="dialog"
    :persistent="persistent"
    width="600"
    content-class="elevation-0"
  >
    <v-sheet>
      <div class="text-center pa-12">
        <v-icon size="80" color="#80E293">
          mdi-check-circle-outline
        </v-icon>
        <div class="py-2" />
        <div class="font-weight-medium">
          予約を受け付けました。
        </div>
        <div class="py-2" />
        <div class="py-2" />
        <div v-if="redirectLink.length === 0">
          <div>a</div>
        </div>
        <nuxt-link v-else :to="redirectLink[0]">
          ホームに戻る
        </nuxt-link>
      </div>
    </v-sheet>
  </v-dialog>
</template>
<script>
export default {
  data () {
    return {
      dialog: false,
      icon: '',
      persistent: false,
      redirectLink: []
    }
  },
  methods: {
    openDialog (icon, persistent, title, redirectLink) {
      this.dialog = true
      this.icon = icon
      this.persistent = persistent
      this.title = title
      this.redirectLink = redirectLink
    }
  }
}
</script>
