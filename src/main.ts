import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import VueLatex from 'vatex'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@/assets/icons/iconfont.css' 

const app = createApp(App)
import * as ElementPlusIconsVue  from '@element-plus/icons-vue' // 引入所有图标，并命名为 Icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

  app.use(store)
  .use(router)
  .use(ElementPlus)
  .use(VueLatex)
  .mount('#app')
