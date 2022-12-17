<template>
  <v-container>
    <CustomerTab />
    <div>
      <div v-for="menuCategory in sortedCategoryByDisplayPriority" :key="menuCategory.id">
        <p class="font-weight-bold mb-2">
          {{ menuCategory.name }}
        </p>
        <div v-for="menu in getCategorizationMenu (menuCategory.id)" :id="getForMenuIdTag(menu.id)" :key="menu.id">
          <nuxt-link :to="`/customer/${$route.params.id}/menu/${menu.id}`">
            <CustomerMenuCard :menu-data="menu" />
          </nuxt-link>
        </div>
      </div>
    </div>
  </v-container>
</template>
<script>
export default {
  auth: false,
  layout: 'customer/default',
  async asyncData ({ $axios, route }) {
    const menu = await $axios.$get(`api/customer/menu?customer_id=${route.params.id}`)
    const menuCategory = await $axios.$get(`api/customer/menu/category?customer_id=${route.params.id}`)
    return { menu, menuCategory }
  },
  computed: {
    sortedCategoryByDisplayPriority () {
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      return this.menuCategory.sort((a, b) => {
        return a.display_priority - b.display_priority
      })
    }
  },
  methods: {
    getForMenuIdTag (id) {
      return `menu_id_${id}`
    },
    getCategorizationMenu (categoryId) {
      const res = []
      for (const i in this.menu) {
        for (const c in this.menu[i].category) {
          if (this.menu[i].category[c].id === categoryId) {
            res.push(this.menu[i])
          }
        }
      }
      return res
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
