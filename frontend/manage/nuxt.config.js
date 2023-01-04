export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - manage',
    title: 'manage',
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
    '@/plugins/vue-toastification',
    '@/plugins/axios',
    '~plugins/core-components.js'
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
    'cookie-universal-nuxt',
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/auth-next'
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    proxy: true
  },
  proxy: {
    '/api': 'http://127.0.0.1:81'
  },
  server: {
    port: 3001,
    host: '0.0.0.0'
  },
  router: {
    middleware: ['auth']
  },
  auth: {
    redirect: {
      login: '/login',
      logout: '/login',
      home: false
    },
    localStorage: false,
    strategies: {
      manageAuth: {
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
          maxAge: 60
        },
        endpoints: {
          login: {
            url: '/api/manage/auth/jwt/create/',
            method: 'post',
            propertyName: 'access'
          },
          refresh: { url: '/api/auth/jwt/refresh/', method: 'post' },
          logout: {
            url: '/api/account/logout',
            method: 'post'
          },
          user: {
            url: '/api/manage/manage_user_me/',
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
    // eslint-disable-next-line no-irregular-whitespace
    extend　(config, ctx) {
      config.module.rules.push({
        test: /\.(ogg|mp3|wav|mpe?g)$/i,
        loader: 'file-loader',
        options: {
          name: '[path][name].[ext]',
          esModule: false
        }
      })
    }
  }
}
