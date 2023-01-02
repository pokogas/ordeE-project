<template>
  <div>
    <v-row>
      <v-col cols="12" xl="10" lg="9" md="9">
        <p class="subtitle-2 font-weight-bold">
          フロア管理
        </p>
        <div class="mb-2" />
        <div class="text-h5 font-weight-bold">
          フロアの状態
        </div>
        <v-row>
          <v-col cols="12" xl="3" lg="6" md="6">
            <board-items-card :items-data="status_data" :cols="[6,6,6,3,3]" />
          </v-col>
          <v-col cols="12" xl="2" lg="4" md="6" @click="right_drawer = true">
            <board-items-card :items-data="waiting_data" :cols="[6,6,12,6,6]" />
          </v-col>
        </v-row>
        <div class="mb-2" />
      </v-col>
      <v-col cols="12" xl="2" lg="3" md="3" class="d-none d-md-block d-lg-block d-xl-block">
        こる２
      </v-col>
    </v-row>
  </div>
</template>
<script>
export default {
  layout: 'shopManage/default',
  async asyncData ({ $axios, route, redirect }) {
    await $axios.$get(`api/manage/access_home/?shop_id=${route.params.shop_id}`).catch(function () {
      redirect('/')
    })
  },
  data () {
    return {
      right_drawer: false,
      status_data: [
        { title: '空席', asg: 0 },
        { title: '予約', asg: 0 },
        { title: '利用中', asg: 0 },
        { title: '準備中', asg: 0 }
      ],
      waiting_data: [
        { title: '待ち人数', asg: 0 },
        { title: '組', asg: 0 }
      ]
    }
  }
}
</script>
<style scoped>
p {
  margin: 0;
}
</style>
