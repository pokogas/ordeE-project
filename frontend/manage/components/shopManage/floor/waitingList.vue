<template>
  <div>
    <v-row>
      <v-col
        cols="12"
        xl="6"
        lg="6"
        md="6"
        sm="6"
        class="pr-1"
      >
        <v-btn
          block
          elevation="0"
          large
          class="font-weight-medium"
          :class="{'green lighten-1 white--text' : unallocatedType === 'wait', 'white grey--text lighten-4--text' : unallocatedType !== 'wait'}"
          @click="unallocatedType='wait'"
        >
          待機
        </v-btn>
      </v-col>
      <v-col
        cols="12"
        xl="6"
        lg="6"
        md="6"
        sm="6"
        class="pl-1"
      >
        <v-btn
          block
          elevation="0"
          large
          class="font-weight-medium"
          :class="{'green lighten-1 white--text' : unallocatedType === 'reserved', 'white grey--text lighten-4--text' : unallocatedType !== 'reserved'}"
          @click="unallocatedType='reserved'"
        >
          予約
        </v-btn>
      </v-col>
    </v-row>
    <div class="pt-1" />
    <!--リスト-->
    <div v-if="unallocatedType === 'wait'" class="pt-2">
      <div class="d-flex">
        <v-select
          hide-details="auto"
          flat
          dense
          :items="[1,2,3,4,5]"
          label="来店人数"
          solo
        />
        <v-btn color="teal lighten-3" class="mx-2 white--text" elevation="0">
          番号札発行
        </v-btn>
      </div>
    </div>
    <div class="py-3">
      <shop-manage-floor-waiting-card />
    </div>
  </div>
</template>
<script>
export default {
  data () {
    return {
      detailView: false,
      unallocatedType: 'wait'
    }
  }
}
</script>
<style>
.activeBtn {
  color: #4EBA6A;
}
</style>
