<template>
  <v-simple-table>
    <template #default>
      <tbody>
        <tr>
          <td class="font-weight-bold">
            個数
          </td>
          <td>{{ orderData.count }} 点</td>
        </tr>
        <tr>
          <td>大きさ</td>
          <td>L</td>
        </tr>
        <tr>
          <td class="font-weight-bold">
            テーブル
          </td>
          <td>t-3</td>
        </tr>
        <tr>
          <td class="font-weight-bold">
            経過時間
          </td>
          <td>10分12秒</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>
<script>
export default {
  props: {
    orderData: {
      type: Object,
      required: true
    }
  }
}
</script>
