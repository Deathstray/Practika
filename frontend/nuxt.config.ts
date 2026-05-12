// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  devtools: { enabled: false },

  modules: ["@pinia/nuxt", "@nuxtjs/tailwindcss"],

  compatibilityDate: '2026-05-07',

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "/api"
    }
  },

  nitro: {
    devProxy: {
      "/api": {
        target: process.env.NUXT_PUBLIC_API_TARGET || "http://127.0.0.1:8001",
        changeOrigin: true
      }
    }
  },

  app: {
    head: {
      title: "Диспетчеризация транспорта",
      meta: [{ charset: "utf-8" }, { name: "viewport", content: "width=device-width, initial-scale=1" }],
      link: [
        { rel: "preconnect", href: "https://fonts.googleapis.com" },
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap"
        }
      ]
    }
  },

  css: ["~/assets/css/main.css"]
})
