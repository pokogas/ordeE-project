<template>
  <v-sheet class="rounded-lg">
    <v-row class="pt-3 pb-6" justify="center">
      <v-avatar style="border: solid #14be91 2px" size="50">
        <v-img src="https://i.postimg.cc/rsmNVQ3B/S-17686534.jpg" />
      </v-avatar>
    </v-row>
    <div class="pb-2 text-center font-weight-bold">
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
    </div>
    <div class="text-center font-weight-bold pb-5" style="font-size: 19px">
      <span>{{ $auth.user.user.last_name }} {{ $auth.user.user.first_name }}</span>
    </div>
    <v-divider class="mx-6" />
    <div class="pb-4" />
    <div>
      <v-list nav dense no-action>
        <template v-for="nav_list in nav_lists">
          <v-list-item
            v-if="!nav_list.lists"
            :key="nav_list.name"
            exact
            color="#00BB8D"
            active-class="blue--text darken-3"
            :to="nav_list.link"
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
    </div>
  </v-sheet>
</template>

<script>
export default {
  data () {
    return {
      drawer: null,
      nav_lists: [
        {
          name: 'ホーム',
          icon: 'mdi-home',
          link: '/'
        },
        {
          name: 'メンバー管理',
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
  }
}
</script>
