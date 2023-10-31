import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import { createPinia } from 'pinia';
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import { initSocket } from './socket'

let app = createApp(App)
const pinia = createPinia();
    
let socket

socket = initSocket()

app.config.globalProperties.$socket = socket

app.use(router)
app.use(pinia);
app.use(VueSweetalert2)
app.mount('#app')
