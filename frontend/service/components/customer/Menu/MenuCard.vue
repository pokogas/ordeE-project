<template>
  <v-card elevation="0" class="mb-2">
    <div class="d-flex">
      <v-avatar class="ma-3 rounded-lg" size="80" tile>
        <v-img src="https://cdn.pixabay.com/photo/2014/11/05/15/57/salmon-518032_1280.jpg" alt="" />
      </v-avatar>
      <div class="pa-3 pl-0">
        <p style="font-size: 15px" class="font-weight-bold">
          {{ menuData.title }}
        </p>
        <p
          class="d-inline-block text-truncate"
          style="font-size: 12px ; max-width: 180px;"
        >
          {{ menuData.detail }}
        </p>
        <div class="d-flex">
          <p style="font-size: 15px" class="font-weight-medium">
            ¥ {{ menuData.price | addComma }}
          </p>
          <div class="pr-1" />
          <v-chip v-if="!menuData.stock_unlimited && 1 <= menuData.stock && menuData.stock <= 5 && !menuData.sold_out" color="red lighten-1" small style="font-size: 11px" class="white--text">
            残り <span class="font-weight-bold">{{ menuData.stock }}</span> 点
          </v-chip>
          <v-chip v-else-if="!menuData.stock_unlimited && menuData.stock <= 0 || menuData.sold_out" color="red lighten-1" small style="font-size: 11px" class="white--text">
            <span class="font-weight-bold">SOLD</span>
          </v-chip>
        </div>
      </div>
    </div>
  </v-card>
</template>
<script>
export default {
  props: {
    menuData: {
      type: Object,
      required: true
    }
  }
}
</script>
<style scoped>
p {
  margin-bottom: 0;
}
</style>
