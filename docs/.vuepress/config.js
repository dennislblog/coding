const path = require("path")

module.exports = {
  base: "/docs/",
  title: "Leetcode Problems",
  description: "A simple demo of the vuepress-theme-book",
  themeConfig: {
    logo: "/logo.png",
    searchPlaceholder: "搜索...",
    docsRepo: "https://github.com/dennislblog/coding/tree/gh-pages",
    // docsDir: "docs",
    // editLinks: false,
    // editLinkText: "Edit this page on Github",
    smoothScroll: true,
    // nav: [
    //   { text: "Home", link: "/" },
    //   {
    //     text: "Github",
    //     link:
    //       "www.baidu.com"
    //   },
    //   {
    //     text: "Default Theme Config",
    //     link: "https://vuepress.vuejs.org/theme/default-theme-config.html"
    //   }
    // ],
    sidebar: {
      "/": [
        {
          title: "",
          collapsable: false,
          sidebarDepth: 0,
          children: [["/", "Home"]]
        },
        {
          title: "",
          collapsable: false,
          sidebarDepth: 0,
          children: [["/theme-configuration", "Configuration 🔧"]]
        },
        {
          title: "Random",
          collapsable: true,
          children: [
            ["/random/dev", "Dev 💻"],
            ["/random/website", "Websites using this theme 👌"],
            ["/random/emoji", "Emoji 😃"],
            ["/random/lorem", "Lorem Ipsum 🌟"]
          ]
        },
        {
          title: "Extras",
          collapsable: true,
          children: [
            ["/extras/contributing", "Contributing ✨"],
            ["/extras/license", "License 📚"]
          ]
        }
      ]
    }
  },
  plugins: [
    ['@vuepress/back-to-top', true],
    ['@vuepress/search', {searchMaxSuggestions: 10}]
  ],
  configureWebpack: {
    resolve: {
      alias: {
        "@assets": path.resolve(__dirname, "../assets")
      }
    }
  }
}