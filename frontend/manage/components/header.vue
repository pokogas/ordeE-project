<template>
  <div>
    <v-app-bar
      v-resize="onResize"
      app
      dense
      elevation="0"
      color="white"
    >
      <v-app-bar-nav-icon class="hidden-lg-and-up" @click="drawer = !drawer" />
      <v-toolbar-title class="font-weight-bold">
        OrdeE <span class="subtitle-1">management</span>
      </v-toolbar-title>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" disable-resize-watcher class="hidden-lg-and-up" app height="100%">
      <v-list-item class="px-0">
        <v-list-item-content>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="font-weight-bold">
                OrdeE-Control
              </v-list-item-title>
              <v-list-item-subtitle class="font-weight-bold">
                <!-- TODO forでしようね！ -->
                <span v-show="$auth.user.role === 1"><span style="color: rgba(1,203,4,0.72)">Admin</span>/店舗管理者</span>
                <span v-show="$auth.user.role === 2"><span style="color: rgba(213,147,0,0.72)">SuperStaff</span>/高級スタッフ</span>
                <span v-show="$auth.user.role === 3"><span style="color: rgba(0,178,162,0.72)">Staff</span>/一般スタッフ</span>
                <v-tooltip bottom>
                  <template #activator="{ on, attrs }">
                    <span
                      v-bind="attrs"
                      v-on="on"
                    ><span v-show="$auth.user.role === 0"><span style="color: rgba(115,0,128,0.72)">SuperAdmin</span>/全店舗管理者</span></span>
                  </template>
                  <span>フルアクセス可能/全権限利用可能</span>
                </v-tooltip>
              </v-list-item-subtitle>
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
            color="#00BB8D"
            active-class="blue--text darken-3"
            :to="nav_list.link"
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
                <v-list-item-title>
                  {{ nav_list.name }}
                </v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item
              v-for="list in nav_list.lists"
              :key="list.name"
              :to="list.link"
            >
              <v-list-item-title>
                {{ list.name }}
              </v-list-item-title>
            </v-list-item>
          </v-list-group>
        </template>
      </v-list>
      <template #append>
        <div>
          <v-divider />
          <v-list-item class="px-0">
            <v-list-item-content>
              <v-list-item>
                <v-list-item-avatar style="border: solid #14be91 2px">
                  <v-img src="https://i.postimg.cc/rsmNVQ3B/S-17686534.jpg" />
                </v-list-item-avatar>

                <v-list-item-content>
                  <v-list-item-title class="font-weight-bold">
                    {{ $auth.user.user.last_name }} {{ $auth.user.user.first_name }}
                  </v-list-item-title>
                  <v-list-item-subtitle style="max-width: 180px;" class="d-inline-block text-truncate">
                    {{ $auth.user.user.email }}
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-content>
          </v-list-item>
        </div>
      </template>
    </v-navigation-drawer>
  </div>
</template>

<script>
export default {
  name: 'ShopManageHeader',
  data () {
    return {
      drawer: false,
      windowSize: {
        x: 0,
        y: 0
      },
      nav_lists: [
        {
          name: 'ホーム',
          role_level: 1,
          icon: 'mdi-home',
          link: '/'
        },
        {
          name: 'メンバー管理',
          role_level: 3,
          icon: 'mdi-account-group',
          link: '',
          active: false,
          lists: [
            {
              name: 'メンバー招待',
              link: '/3'
            },
            {
              name: 'メンバー編集',
              link: '/3'
            }
          ]
        },
        {
          name: '店舗',
          role_level: 4,
          icon: 'mdi-newspaper-variant-multiple-outline',
          link: '',
          active: false,
          lists: [
            {
              name: '新規登録',
              link: '/3'
            },
            {
              name: '店舗リスト',
              link: '/3'
            }
          ]
        }
      ]
    }
  },
  mounted () {
    this.onResize()
  },
  methods: {
    onResize () {
      if (this.drawer === false) {
        return
      }
      if (window.innerWidth > 1264) {
        this.drawer = false
      }
    }
  }
}
</script>

<style scoped>

</style>
