export default async function ({ params, $axios, error }) {
  await $axios.$get(`api/customer/detail?customer_id=${params.id}`).then(function (res) {
  }).catch(function (res) {
    error({
      statusCode: 404,
      message: 'mes'
    })
  })
}
