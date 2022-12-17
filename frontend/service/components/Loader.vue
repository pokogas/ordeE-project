<template>
  <v-dialog
    :value="loaderDialog"
    persistent
    width="300"
  >
    <v-card
      color="primary"
      dark
    >
      <v-card-text>
        {{ loaderName }}
        <v-progress-linear
          indeterminate
          color="white"
          class="mb-0"
        />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    loaderName: {
      type: String,
      required: true
    },
    loaderDialog: {
      type: Boolean,
      default: false,
      required: true
    }
  }
}
</script>

<style scoped>

</style>
