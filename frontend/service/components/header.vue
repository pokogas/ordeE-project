<template>
  <v-app-bar
    app
    elevation="0"
    color="#FFFFFF"
  >
    <v-container class="py-0 fill-height">
      <v-toolbar-title style="color: #3B3B3B" class="font-weight-bold">
        SHOPNAME
      </v-toolbar-title>
      <v-spacer />
      <div v-if="!$auth.loggedIn">
        <v-btn color="#FF4600">
          <span class="white--text font-weight-bold">新規登録</span>
        </v-btn>
        <v-btn color="#FFFFFF" outlined @click="loginBtn">
          <span class="grey--text font-weight-bold">ログイン</span>
        </v-btn>
      </div>
      <div v-else>
        <v-btn icon>
          <v-icon>
            mdi-square-rounded-badge-outline
          </v-icon>
        </v-btn>
      </div>
    </v-container>
  </v-app-bar>
</template>
<script>
export default {
  methods: {
    loginBtn () {
      this.$cookies.set('auth.redirect', this.$route.path)
      return this.$router.replace('/login')
    }
  }
}
</script>
