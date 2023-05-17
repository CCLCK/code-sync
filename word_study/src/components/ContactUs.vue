<template>
    <div class="contact-us">
      <a href="tencent://message/?uin=1946605630&Site=&Menu=yes">联系我们</a>
      <font-awesome-icon icon="copy" @click="copyQQ" size="lg" />

    </div>
  </template>
  
  
<script>
import { useToast } from "vue-toast-notification";

export default {
  methods: {
    copyQQ() {
      const toast = useToast();
      navigator.clipboard
        .writeText("1946605630")
        .then(() => {
          toast.success("QQ号已复制到剪贴板");
        })
        .catch(() => {
          toast.error("复制失败");
        });
    },
  },
};
</script>

<style scoped>
.contact-us a {
  color: white; /* 文字颜色 */
  background-color: #0066cc; /* 背景颜色 */
  padding: 10px;
  border-radius: 5px;
  text-decoration: none;
  border: 2px solid white; /* 添加边框 */
}

.contact-us a:hover {
  background-color: pink; /* 鼠标悬停时的背景颜色 */
}
</style>

