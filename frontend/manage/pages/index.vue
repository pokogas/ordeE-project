<template>
  <v-container fluid>
    <p class="subtitle-2 font-weight-bold">
      トップ
    </p>
    <div class="mb-6" />
    <div class="text-h5 font-weight-bold">
      管理店舗
    </div>
    <div class="mb-3" />
    <div>
      <v-row class="pb-3">
        <v-col
          v-for="manageShop in manageShop"
          :key="manageShop.id"
          cols="12"
          lg="3"
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
    <div class="mb-9" />
    <div class="d-flex">
      <div class="text-h5 font-weight-bold">
        全店舗
      </div>
      <v-switch
        v-model="allShopView"
        class="mt-0 ml-6"
        inset
        color="green"
        label="表示"
      />
    </div>
    <div v-show="allShopView">
      <div class="d-flex" style="width: 300px">
        <v-text-field
          label="検索"
          solo
          flat
          dense
        />
      </div>
      <div>
        <v-row class="pb-3">
          <v-col
            v-for="allShop in allShop"
            :key="allShop.id"
            cols="12"
            lg="3"
            md="6"
            sm="12"
          >
            <nuxt-link :to="`/shop/${allShop.id}`">
              <HomeShopCard :shop-data="allShop" />
            </nuxt-link>
          </v-col>
        </v-row>
      </div>
    </div>
  </v-container>
</template>
<script>
export default {
  layout: 'control',
  async asyncData ({ $axios }) {
    const manageShop = await $axios.$get('api/manage/shops/?type=userManage')
    const allShop = await $axios.$get('api/manage/shops/?type=all')
    return { manageShop, allShop }
  },
  data () {
    return {
      allShopView: false
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
