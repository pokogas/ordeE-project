<template>
  <v-card elevation="0" class="mb-2 rounded-lg" :class="{'selecting-border': selecting}" @click="action(selecting, shopData)">
    <div class="d-flex">
      <v-avatar class="ma-3 rounded-lg" size="70" tile>
        <v-img src="https://cdn.pixabay.com/photo/2014/11/05/15/57/salmon-518032_1280.jpg" alt="" />
      </v-avatar>
      <div class="pa-3 pl-0">
        <p style="font-size: 15px" class="font-weight-bold">
          {{ shopData.name }}
        </p>
        <p
          class="d-inline-block text-truncate"
          style="font-size: 12px ; max-width: 180px;"
        >
          ショップ詳細
        </p>
      </div>
    </div>
  </v-card>
</template>
<script>
export default {
  props: {
    selecting: {
      required: true,
      type: Boolean
    },
    shopData: {
      required: true,
      type: Object
    }
  },
  methods: {
    action (selecting, shopData) {
      if (selecting) {
        this.$emit('openShopsModal')
      } else {
        this.$emit('selectShop', shopData)
      }
    }
  }
}
</script>
<style scoped>
p {
  margin-bottom: 0;
}
.selecting-border {
  border: solid #54D13B 2px
}
.v-card--link:focus:before {
  opacity: 0;
}
</style>
