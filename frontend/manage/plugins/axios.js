import Vue from 'vue'

export default function ({ $axios, redirect }) {
  $axios.onError((error) => {
    if (error.response.data.detail === 'ShopNotAccessPermission') {
      redirect('/')
      Vue.$toast.error('こちらへのアクセスまたは操作の権限が無いようです、詳しくはシステム管理者にお問い合わせください。')
    }
  })
}
