import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router';
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/index.css'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas, faCopy } from '@fortawesome/free-solid-svg-icons';
import { library } from '@fortawesome/fontawesome-svg-core';
import Toast from "vue-toast-notification";
import 'vue-toast-notification/dist/theme-default.css';
import '@fortawesome/fontawesome-free/css/all.css'
import App from './App.vue'
library.add(fas, faCopy);  // 将所有 solid 图标以及复制图标添加到库中

// 创建路由配置
const routes = [
  { path: '/words/:word', component: App }
];

// 创建 router 实例
const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);

app.component('font-awesome-icon', FontAwesomeIcon);
app.use(Toast);
app.use(router);  // 使用 router
app.use(ElementPlus)
app.mount('#app');
