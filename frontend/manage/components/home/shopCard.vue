<template>
  <v-card class="pa-1">
    <v-chip
      v-if="roleNum !== null"
      class="ma-2 white--text font-weight-bold"
      small
      style="border: #EFEFEF"
      :color="getPermissionColor(roleNum)"
    >
      <span v-if="roleNum === 0">Admin</span>
      <span v-if="roleNum === 1">Admin</span>
      <span v-if="roleNum === 2">SuperStaff</span>
      <span v-if="roleNum === 3">Staff</span>
    </v-chip>
    <div class="px-4 pb-3">
      <p class="font-weight-bold text-h6">
        {{ shopData.name }}
      </p>
      <div>
        <v-icon class="pr-1" dense color="orange">
          mdi-account-star
        </v-icon>
        <v-tooltip bottom>
          <template #activator="{ on, attrs }">
            <span
              v-bind="attrs"
              v-on="on"
            >{{ shopData.owner.last_name }} {{ shopData.owner.first_name }}</span>
          </template>
          <span>店舗オーナー</span>
        </v-tooltip>
      </div>
      <div>
        <v-icon class="pr-1" dense color="green">
          mdi-phone
        </v-icon>
        <v-tooltip bottom>
          <template #activator="{ on, attrs }">
            <span
              v-bind="attrs"
              v-on="on"
            >{{ shopData.phone }}</span>
          </template>
          <span>店舗電話番号</span>
        </v-tooltip>
      </div>
    </div>
  </v-card>
</template>
<script>
export default {
  props: {
    shopData: {
      type: Object,
      required: true
    },
    roleNum: {
      type: Number,
      default: null,
      required: false
    }
  },
  methods: {
    getPermissionColor (permissionLevel) {
      if (permissionLevel === 0) { return 'green' }
      if (permissionLevel === 1) { return 'green' }
      if (permissionLevel === 2) { return 'orange' }
      if (permissionLevel === 3) { return 'light-blue lighten-2' }
    }
  }
}
</script>
<style scoped>
p {
  margin-bottom: 0;
}
</style>
