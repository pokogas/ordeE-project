<template>
  <v-container>
    <div style="max-width:500px" class="mx-auto">
      <div class="text-center  ma-10 pt-10">
        <p style="color: #ff4600; font-size: 28px" class="font-weight-bold">
          ordeE-Management <br>
          <span style="color: #ff4600; font-size: 18px">管理者専用ログインページ</span>
        </p>
      </div>
      <div>
        <div v-if="form.error.status" class="py-2">
          <v-alert
            dense
            outlined
            type="error"
          >
            {{ form.error.detail }}
          </v-alert>
        </div>
        <v-form ref="form">
          <v-text-field
            v-model="form.email"
            type="email"
            :rules="emailRules"
            label="管理者ID(メールアドレス)"
            outlined
            color="#7886FF"
            elevation="0"
            class="rounded-lg"
          />
          <v-text-field
            v-model="form.password"
            type="password"
            :rules="passwordRules"
            label="パスワード"
            outlined
            color="#7886FF"
            class="rounded-lg"
          />
        </v-form>
        <v-btn
          :disabled="usableBtn !== true"
          :loading="usableBtn !== true"
          block
          x-large
          color="#FF4600C2"
          @click="login"
        >
          <span class="white--text font-weight-bold">ログイン</span>
        </v-btn>
      </div>
    </div>
  </v-container>
</template>
<script>
export default {
  middleware ({ store, redirect }) {
    if (store.$auth.loggedIn) {
      redirect('/')
    }
  },
  data () {
    return {
      form: {
        email: '',
        password: '',
        error: {
          status: false,
          detail: ''
        }
      },
      usableBtn: true,
      emailRules: [
        v => !!v || '入力してください。',
        v => /.+@.+\..+/.test(v) || '正しいメールアドレスを入力してください。'
      ],
      passwordRules: [
        v => !!v || '入力してください。'
      ]
    }
  },
  methods: {
    popError (detail) {
      this.form.error.status = true
      this.form.error.detail = detail
    },
    async login () {
      if (this.$refs.form.validate()) {
        this.usableBtn = false
        try {
          await this.$auth.loginWith('manageAuth', { data: this.form })
          // TODO auth.redirectがない場合 ドメイン/ <=にログインする
          return this.$router.replace({ path: '/' })
        } catch (error) {
          this.popError('メールアドレスまたはパスワードに誤りがあります。')
          this.form.password = ''
          // eslint-disable-next-line no-return-assign
          return this.usableBtn = true
        }
      }
    }
  }
}
</script>
