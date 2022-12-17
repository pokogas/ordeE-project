<template>
  <v-card id="gallery" class="rounded-lg toc-view mb-5">
    <v-tabs fixed-tabs color="#FCA457">
      <v-tab
        v-for="tab_list in tab_lists"
        :key="tab_list.name"
        exact
        nuxt
        :to="tab_list.link"
        class="font-weight-bold"
      >
        {{ tab_list.name }}
      </v-tab>
    </v-tabs>
  </v-card>
</template>
<script>
export default {
  data () {
    return {
      tab_lists: [
        {
          name: 'トップ',
          link: `/customer/${this.$route.params.id}/`
        },
        {
          name: 'メニュー',
          link: `/customer/${this.$route.params.id}/menu`
        }
      ]
    }
  }
}
</script>
