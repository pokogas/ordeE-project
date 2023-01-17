<template>
  <div>
    <v-app-bar
      app
      style="z-index: 10000"
      dense
      elevation="0"
      color="white"
    >
      <v-app-bar-nav-icon class="" @click="drawer = !drawer" />
      <v-toolbar-title class="font-weight-bold">
        OrdeE <span class="subtitle-1">management</span>
      </v-toolbar-title>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" app height="100%">
      <v-list-item class="px-0">
        <v-list-item-content>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="font-weight-bold">
                OrdeE-ShopManage
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-content>
      </v-list-item>
      <v-divider />
      <v-list nav dense no-action>
        <template v-for="nav_list in nav_lists">
          <v-list-item
            v-if="!nav_list.lists"
            :key="nav_list.name"
            exact
            color="#00BB8D"
            active-class="blue--text darken-3"
            :to="nav_list.link"
            :class="{'blue--text darken-3 v-list-item--active v-list-item v-list-item--link theme--light': nav_list.same_links.includes($route.path)}"
            @click="menu_close"
          >
            <v-list-item-icon>
              <v-icon>{{ nav_list.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title class="font-weight-bold">
                {{ nav_list.name }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-group
            v-else
            :key="nav_list.name"
            v-model="nav_list.active"
            color="#00BB8D"
            active-class="blue--text darken-3"
            no-action
            :prepend-icon="nav_list.icon"
          >
            <template #activator>
              <v-list-item-content>
                <v-list-item-title class="font-weight-bold">
                  {{ nav_list.name }}
                </v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item
              v-for="list in nav_list.lists"
              :key="list.name"
              :to="list.link"
              color="#00BB8D"
              active-class="blue--text darken-3"
            >
              <v-list-item-title class="font-weight-bold">
                {{ list.name }}
              </v-list-item-title>
            </v-list-item>
          </v-list-group>
        </template>
      </v-list>
      <template #append>
        <div>
          <nuxt-link to="/" class="text-center">
            コントロールに戻る
          </nuxt-link>
          <v-divider />
        </div>
      </template>
    </v-navigation-drawer>
  </div>
</template>

<script>
export default {
  name: 'ManageHeader',
  data () {
    return {
      drawer: null,
      nav_lists: [
        {
          name: 'ホーム',
          icon: 'mdi-home',
          link: `/shop/${this.$route.params.shop_id}/`,
          same_links: []
        },
        {
          name: '注文管理',
          icon: 'mdi-newspaper-variant-multiple-outline',
          link: `/shop/${this.$route.params.shop_id}/order/`,
          active: false,
          lists: [
            {
              name: 'リアルタイム',
              link: `/shop/${this.$route.params.shop_id}/order/realtime`
            },
            {
              name: '履歴',
              link: `/shop/${this.$route.params.shop_id}/order/history`
            }
          ]
        },
        {
          name: 'フロア管理',
          icon: 'mdi-floor-plan',
          link: `/shop/${this.$route.params.shop_id}/floor`,
          same_links: []
        },
        {
          name: 'メニュー管理',
          icon: 'mdi-silverware',
          link: `/shop/${this.$route.params.shop_id}/menu/`,
          same_links: [
            `/shop/${this.$route.params.shop_id}/menu/manager`
          ]
        },
        {
          name: '予約管理',
          icon: 'mdi-book-check-outline',
          link: `/shop/${this.$route.params.shop_id}/reserve`,
          same_links: []
        }
      ]
    }
  },
  methods: {
    menu_close () {
      // eslint-disable-next-line camelcase
      this.nav_lists.forEach(nav_list => (nav_list.active = false))
    }
  }
}
</script>

<style scoped>

</style>
