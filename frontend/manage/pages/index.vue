<template>
  <div>
    <div class="text-h5 font-weight-bold">
      店舗マネージャー
    </div>
    <div class="mb-3" />
    <div>
      <v-row class="pb-3">
        <v-col
          v-for="manageShop in manageShop"
          :key="manageShop.id"
          cols="12"
          lg="4"
          md="6"
          sm="12"
        >
          <nuxt-link :to="`/shop/${manageShop.shop.id}`">
            <HomeShopCard :role-num="manageShop.role" :shop-data="manageShop.shop" />
          </nuxt-link>
        </v-col>
      </v-row>
      <div v-show="manageShop.length === 0" class="text-center">
        管理しているショップが見つかりませんでした。
      </div>
    </div>
  </div>
</template>
<script>
export default {
  layout: 'control',
  async asyncData ({ $axios }) {
    const manageShop = await $axios.$get('api/manage/shops/?type=userManage')
    return { manageShop }
  },
  data () {
    return {
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
