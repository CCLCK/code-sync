import { createApp } from 'vue'
import App from './App.vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { library } from '@fortawesome/fontawesome-svg-core';
import Toast from "vue-toast-notification";
import 'vue-toast-notification/dist/theme-default.css';
import '@fortawesome/fontawesome-free/css/all.css'

library.add(fas);  // 将所有 solid 图标添加到库中

const app = createApp(App);

app.component('font-awesome-icon', FontAwesomeIcon);
app.use(Toast);

app.mount('#app');
