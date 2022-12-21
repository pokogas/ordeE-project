export default {
  watchers: {
    webpack: {
      poll: true
    }
  },
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - service',
    title: 'service',
    htmlAttrs: {
      lang: 'ja'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '~/plugins/addCommaFilter'
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify'
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    'cookie-universal-nuxt',
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    '@nuxtjs/dayjs'
  ],
  dayjs: {
    locales: ['ja'],
    defaultLocale: 'ja',
    defaultTimeZone: 'Asia/Tokyo',
    plugins: [
      'utc', // import 'dayjs/plugin/utc'
      'timezone' // import 'dayjs/plugin/timezone'
    ]
  },

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    baseURL: process.env.AXIOS_BASEURL,
    browserBaseURL: process.env.AXIOS_BROWSER_BASEURL
  },
  router: {
    middleware: ['auth']
  },
  // TODO NavigationDuplicated: Avoided redundant navigation to current location: "/login". customerにログイン後遷移した際にでるerror
  auth: {
    redirect: {
      login: '/login',
      logout: '/login',
      home: '/'
    },
    localStorage: false,
    strategies: {
      local: {
        scheme: 'refresh',
        tokenType: 'JWT',
        token: {
          type: 'JWT',
          property: 'access',
          maxAge: 60
        },
        user: {
          property: false
        },
        refreshToken: {
          property: 'refresh',
          data: 'refresh',
          maxAge: 60 * 60 * 24 * 30
        },
        endpoints: {
          login: {
            url: 'api/auth/jwt/create/',
            method: 'post',
            propertyName: 'access'
          },
          refresh: { url: 'api/auth/jwt/refresh/', method: 'post' },
          logout: {
            url: 'api/account/logout',
            method: 'post'
          },
          user: {
            url: 'api/auth/users/me/',
            method: 'get',
            propertyName: 'access'
          }
        }
      }
    }
  },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    treeShake: true,
    theme: {
      themes: {
        light: {
          background: '#EFEFEF'
        }
      }
    }
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    loadingScreen: false
  }
}
