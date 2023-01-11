<template>
  <v-card class="pa-2" elevation="0">
    <div class="d-flex">
      <div class="font-weight-bold align-self-center">
        T-1
      </div>
      <v-spacer />
      <v-chip small class="white--text font-weight-medium" color="#74D436">
        空席
      </v-chip>
    </div>
    <v-divider class="my-1" />
    <div class="py-8">
      詳細
    </div>
    <div class="d-flex justify-space-around">
      <v-btn elevation="0" class="rounded-xl white--text font-weight-bold" small color="#4AB0A0">
        アクション1
      </v-btn>
      <v-btn elevation="0" class="rounded-xl white--text font-weight-bold" small color="#4AB0A0">
        アクション2
      </v-btn>
    </div>
  </v-card>
</template>
<script>
export default {
  props: {
  }
}
</script>
