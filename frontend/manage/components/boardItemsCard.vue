<template>
  <v-card flat class="rounded-lg">
    <v-row class="ma-4">
      <v-col
        v-for="item in itemsData"
        :key="item.title"
        :cols="cols[0]"
        :sm="cols[1]"
        :md="cols[2]"
        :lg="cols[3]"
        :xl="cols[4]"
      >
        <div style="font-size: 24px" class="font-weight-bold grey--text text--darken-2">
          {{ item.asg }}
        </div>
        <div style="font-size: 12px">
          {{ item.title }}
        </div>
      </v-col>
    </v-row>
  </v-card>
</template>
<script>
export default {
  props: {
    itemsData: {
      type: Array,
      required: true
    },
    cols: {
      type: Array,
      required: true
    }
  }
}
</script>
