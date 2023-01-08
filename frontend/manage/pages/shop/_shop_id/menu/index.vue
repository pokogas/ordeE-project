<template>
  <div>
    <p class="subtitle-2 font-weight-bold">
      メニュー管理
    </p>
    <div class="mb-2" />
    <div class="text-h5 font-weight-bold">
      メニュー
    </div>
    <v-container>
      <v-row>
        <v-col cols="12" sm="12" md="12" lg="7" xl="7">
          <v-simple-table height="650px">
            <template #default>
              <thead>
                <tr>
                  <th class="text-left">
                    商品名
                  </th>
                  <th class="text-left">
                    在庫
                  </th>
                  <th class="text-left">
                    ステータス
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in desserts"
                  :key="item.name"
                >
                  <td class="font-weight-black">
                    {{ item.name }}
                  </td>
                  <td class="font-weight-medium">
                    {{ item.stock }}
                  </td>
                  <td>
                    <span v-if="item.status">
                      <v-chip
                        class="ma-2 font-weight-bold"
                        color="green"
                        label
                        text-color="white"
                        small
                      >
                        販売中
                      </v-chip>
                    </span>
                    <span v-else>
                      <v-chip
                        small
                        class="ma-2 ml-0"
                        color="red"
                        label
                        text-color="white font-weight-bold"
                      >
                        売り切れ
                      </v-chip>
                    </span>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-col>
        <v-col cols="12" sm="12" md="12" lg="4" xl="4">
          <v-sheet class="rounded-l">
            メニュー詳細
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  layout: 'shopManage/default',
  data () {
    return {
      desserts: [
        {
          name: 'ぼんじり',
          stock: 159,
          status: false
        }
      ]
    }
  }
}
</script>

<style scoped>
p {
  margin: 0;
}
</style>
