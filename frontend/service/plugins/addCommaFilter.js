import Vue from 'vue'

Vue.filter('addComma', function (value) {
  return value.toLocaleString()
})
