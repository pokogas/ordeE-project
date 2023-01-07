<template>
  <v-card>
    <div class="pa-3 d-flex">
      <div>
        <div class="text-body-2 font-weight-bold">
          酒井 将弘 様
        </div>
        <span class="text-caption font-weight-bold grey--text"># 9381</span>
      </div>
      <div class="ml-auto">
        <v-progress-circular
          :rotate="-90"
          :size="50"
          :width="4"
          :value="20"
          color="red"
        >
          <span style="font-size: 12px">18分</span>
        </v-progress-circular>
      </div>
    </div>
    <v-divider />
    <div class="pa-2 d-flex">
      <div class="text-body-2 font-weight-bold grey--text">
        チェックイン
      </div>
      <v-spacer />
      <div class="text-end text-caption">
        10:00 ~
      </div>
    </div>
  </v-card>
</template>
