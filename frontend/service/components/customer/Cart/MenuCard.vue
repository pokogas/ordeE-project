<template>
  <v-card elevation="0" class="mb-2">
    <div class="d-flex">
      <v-avatar class="ma-3 rounded-lg" size="85" tile>
        <v-img src="https://cdn.pixabay.com/photo/2014/11/05/15/57/salmon-518032_1280.jpg" alt="" />
      </v-avatar>
      <v-list-item style="padding: 0 10px 0 0;">
        <v-list-item-content>
          <p class="pb-1 font-weight-bold">
            {{ cartData.menu.title }}
          </p>
          <!-- optionはここでforを回してください。-->
          <p class="pb-1" style="font-size: 0.775rem">
            サイズ: 大きい
          </p>
          <p style="font-size: 0.955rem" class="pb-1 text--primary font-weight-bold">
            ¥ {{ cartData.amount | addComma }}
          </p>
        </v-list-item-content>

        <v-list-item-action>
          <div />
          <div>
            <div class="d-flex align-center justify-center">
              <span
                class="no-copy"
                style="padding-right: 10px;padding-left: 10px;font-size: 18px;color: #FE6363;font-weight: bold;"
              >1 <span style="font-size: 14px">個</span></span>
            </div>
          </div>
        </v-list-item-action>
      </v-list-item>
    </div>
  </v-card>
</template>
<script>
export default {
  props: {
    cartData: {
      type: Object,
      required: true
    }
  }
}
</script>
