<template>
  <div>
    a
  </div>
</template>
<script>
export default {
  layout: 'shopManage/default',
  async asyncData ({ $axios, route, redirect }) {
    await $axios.$get(`api/manage/access_home/?shop_id=${route.params.shop_id}`).catch(function () {
      redirect('/')
    })
  }
}
</script>
