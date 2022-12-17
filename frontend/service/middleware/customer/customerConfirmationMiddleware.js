export default async function ({ params, $axios, error }) {
  await $axios.$get(`/customer/detail?customer_id=${params.id}`).then(function (res) {
  }).catch(function () {
    error({
      statusCode: 404,
      message: 'mes'
    })
  })
}
