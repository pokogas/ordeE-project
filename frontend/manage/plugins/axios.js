import Vue from 'vue'

const SAFE_METHODS = ['get', 'head', 'option', 'trace']

export default function ({ $axios, redirect, $cookies }) {
  $axios.onError((error) => {
    if (error.response.data.detail === 'ShopNotAccessPermission' || error.response.data.detail === 'UseAuthorityInAccessProhibited') {
      Vue.$toast.error('こちらへのアクセスまたは操作の権限が無いようです、詳しくはシステム管理者にお問い合わせください。')
    } else if (error.response.data.detail === 'shopNotFound') {
      Vue.$toast.error('SHOPが見つかりませんでした。')
    }
  })

  $axios.onRequest(async (config) => {
    const isUnsafe = !SAFE_METHODS.includes(config.method)
    if (isUnsafe) {
      config.headers['Content-Type'] = 'application/json'
      config.xsrfCookieName = 'csrftoken'
      config.xsrfHeaderName = 'X-CSRFToken'
      let csrftoken = $cookies.get('csrftoken')
      if (csrftoken === undefined) {
        await $axios.$get('api/csrf').then(function (res) {
          $cookies.set('csrftoken', res.token)
          csrftoken = $cookies.get('csrftoken')
        })
      }
      config.headers.common['X-CSRFToken'] = csrftoken
    }
    return config
  })
}
