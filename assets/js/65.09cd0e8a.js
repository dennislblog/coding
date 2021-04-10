(window.webpackJsonp=window.webpackJsonp||[]).push([[65],{1231:function(s,t,e){"use strict";e.r(t);var a=e(2),n=Object(a.a)({},(function(){var s=this,t=s.$createElement,e=s._self._c||t;return e("ContentSlotsDistributor",{attrs:{"slot-key":s.$parent.slotKey}},[e("h2",{attrs:{id:"配置文件"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#配置文件"}},[s._v("#")]),s._v(" 配置文件")]),s._v(" "),e("p",[s._v("如果没有任何配置，这个网站将会是非常局限的，用户也无法在你的网站上自由导航。为了更好地自定义你的网站，让我们首先在你的文档目录下创建一个 "),e("code",[s._v(".vuepress")]),s._v(" 目录，所有 VuePress 相关的文件都将会被放在这里。你的项目结构可能是这样：")]),s._v(" "),e("div",{staticClass:"language- extra-class"},[e("pre",{pre:!0,attrs:{class:"language-text"}},[e("code",[s._v(".\n├─ docs\n│  ├─ README.md\n│  └─ .vuepress\n│     └─ config.js\n└─ package.json\n")])])]),e("p",[s._v("一个 VuePress 网站必要的配置文件是 "),e("code",[s._v(".vuepress/config.js")]),s._v("，它应该导出一个 JavaScript 对象：")]),s._v(" "),e("div",{staticClass:"language-js extra-class"},[e("pre",{pre:!0,attrs:{class:"language-js"}},[e("code",[s._v("module"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(".")]),s._v("exports "),e("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("{")]),s._v("\n  title"),e("span",{pre:!0,attrs:{class:"token operator"}},[s._v(":")]),s._v(" "),e("span",{pre:!0,attrs:{class:"token string"}},[s._v("'Hello VuePress'")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(",")]),s._v("\n  description"),e("span",{pre:!0,attrs:{class:"token operator"}},[s._v(":")]),s._v(" "),e("span",{pre:!0,attrs:{class:"token string"}},[s._v("'Just playing around'")]),s._v("\n"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("}")]),s._v("\n")])])]),e("p",[s._v("对于上述的配置，如果你运行起 dev server，你应该能看到一个页面，它包含一个页头，里面包含一个标题和一个搜索框。VuePress 内置了基于 headers 的搜索 —— 它会自动为所有页面的标题、"),e("code",[s._v("h2")]),s._v(" 和 "),e("code",[s._v("h3")]),s._v(" 构建起一个简单的搜索索引。")]),s._v(" "),e("p",[s._v("参见 "),e("RouterLink",{attrs:{to:"/2021/config/"}},[s._v("配置")]),s._v(" 来查看所有可配置的选项。")],1),s._v(" "),e("div",{staticClass:"custom-block tip"},[e("p",{staticClass:"custom-block-title"},[s._v("其他配置格式")]),s._v(" "),e("p",[s._v("你也可以使用 YAML ("),e("code",[s._v(".vuepress/config.yml")]),s._v(") 或是 TOML ("),e("code",[s._v(".vuepress/config.toml")]),s._v(") 格式的配置文件。")])]),s._v(" "),e("h2",{attrs:{id:"主题配置"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#主题配置"}},[s._v("#")]),s._v(" 主题配置")]),s._v(" "),e("p",[s._v("一个 VuePress 主题应该负责整个网站的布局和交互细节。在 VuePress 中，目前自带了一个默认的主题（正是你现在所看到的），它是为技术文档而设计的。同时，默认主题提供了一些选项，让你可以去自定义导航栏（navbar）、 侧边栏（sidebar）和 首页（homepage） 等，详情请参见 "),e("RouterLink",{attrs:{to:"/2021/theme/default-theme-config.html"}},[s._v("默认主题")]),s._v(" 。")],1),s._v(" "),e("p",[s._v("如果你想开发一个自定义主题，可以参考 "),e("RouterLink",{attrs:{to:"/2021/theme/"}},[s._v("自定义主题")]),s._v("。")],1),s._v(" "),e("h2",{attrs:{id:"应用级别的配置"}},[e("a",{staticClass:"header-anchor",attrs:{href:"#应用级别的配置"}},[s._v("#")]),s._v(" 应用级别的配置")]),s._v(" "),e("p",[s._v("由于 VuePress 是一个标准的 Vue 应用，你可以通过创建一个 "),e("code",[s._v(".vuepress/enhanceApp.js")]),s._v(" 文件来做一些应用级别的配置，当该文件存在的时候，会被导入到应用内部。"),e("code",[s._v("enhanceApp.js")]),s._v(" 应该 "),e("code",[s._v("export default")]),s._v(" 一个钩子函数，并接受一个包含了一些应用级别属性的对象作为参数。你可以使用这个钩子来安装一些附加的 Vue 插件、注册全局组件，或者增加额外的路由钩子等：")]),s._v(" "),e("details",{staticClass:"custom-block details"},[e("summary",[s._v("点击查看代码")]),s._v(" "),e("div",{staticClass:"language-js extra-class"},[e("pre",{pre:!0,attrs:{class:"language-js"}},[e("code",[e("span",{pre:!0,attrs:{class:"token comment"}},[s._v("// 使用异步函数也是可以的")]),s._v("\n"),e("span",{pre:!0,attrs:{class:"token keyword"}},[s._v("export")]),s._v(" "),e("span",{pre:!0,attrs:{class:"token keyword"}},[s._v("default")]),s._v(" "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("(")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("{")]),s._v("\n  Vue"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(",")]),s._v(" "),e("span",{pre:!0,attrs:{class:"token comment"}},[s._v("// VuePress 正在使用的 Vue 构造函数")]),s._v("\n  options"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(",")]),s._v(" "),e("span",{pre:!0,attrs:{class:"token comment"}},[s._v("// 附加到根实例的一些选项")]),s._v("\n  router"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(",")]),s._v(" "),e("span",{pre:!0,attrs:{class:"token comment"}},[s._v("// 当前应用的路由实例")]),s._v("\n  siteData"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(",")]),s._v(" "),e("span",{pre:!0,attrs:{class:"token comment"}},[s._v("// 站点元数据")]),s._v("\n  isServer "),e("span",{pre:!0,attrs:{class:"token comment"}},[s._v("// 当前应用配置是处于 服务端渲染 或 客户端")]),s._v("\n"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("}")]),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(")")]),s._v(" "),e("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=>")]),s._v(" "),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("{")]),s._v("\n  "),e("span",{pre:!0,attrs:{class:"token comment"}},[s._v("// ...做一些其他的应用级别的优化")]),s._v("\n"),e("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("}")]),s._v("\n")])])])]),s._v(" "),e("p",[e("strong",[s._v("相关阅读：")])]),s._v(" "),e("ul",[e("li",[e("RouterLink",{attrs:{to:"/2021/plugin/option-api.html#enhanceappfiles"}},[s._v("插件 API 中的 enhanceApp")])],1)])])}),[],!1,null,null,null);t.default=n.exports}}]);