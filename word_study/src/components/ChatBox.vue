<template>
  <div class="chat-box-container">
    <div v-if="isChatOpen" class="chat-box">
      <div class="chat-header" @click="isChatOpen = !isChatOpen">
        <h3 class="header-text">Word Usage</h3>
      </div>
      <div class="chat-content">
        <div v-for="(message, index) in messages" :key="index" class="message">
          <div v-if="message.sender === 'user'" class="user-message">
            <div>{{ message.text }}</div> <!-- Modified this line -->
          </div>
          <div v-else class="bot-message">
            <div>{{ message.text }}</div> <!-- And this line -->
          </div>
        </div>
      </div>
      <div class="chat-input">
        <textarea
          v-model="userInput"
          placeholder="Type your message..."
          @keydown.enter.exact.prevent="handleEnterKey"
          @keydown.enter.ctrl.exact.prevent="handleCtrlEnterKey"
          @keydown.enter.exact.shift="handleShiftEnterKey"
        ></textarea>

        <button class="send-button" @click="sendMessage">Send</button>
      </div>
    </div>
    <div v-else class="chat-icon" @click="isChatOpen = !isChatOpen">
      <font-awesome-icon icon="comments" />
    </div>
  </div>
</template>

  
  <script>
import axios from "axios";

export default {
  data() {
    return {
      userInput: "",
      isChatOpen: false,
      messages: [],
    };
  },
  methods: {
    sendMessage() {
      if (this.userInput.trim() === "") {
        return; // 用户输入为空，不执行任何操作
      }

      // 将连续的换行替换为一个换行
      this.userInput = this.userInput.replace(/\n\s*\n/g, "\n");

      this.messages.push({ sender: "user", text: this.userInput });
      const userInput = this.userInput;
      this.userInput = "";

      // 滚动聊天框到底部
      const chatContent = this.$el.querySelector(".chat-content");
      chatContent.scrollTop = chatContent.scrollHeight;

      // 发送请求到Flask服务器
      axios
        .post("http://localhost:5200/api/chat", { message: userInput })
        .then((response) => {
          // 服务器响应成功
          this.messages.push({ sender: "bot", text: response.data.message });

          this.$nextTick(() => {
            // 再次滚动聊天框到底部
            chatContent.scrollTop = chatContent.scrollHeight;
          });
        })
        .catch((error) => {
          // 处理错误
          console.error(error);
        });
    },

    handleEnterKey(event) {
      if (!event.shiftKey) {
        event.preventDefault();
        this.sendMessage();
      }
    },
    handleShiftEnterKey(event) {
      if (event.shiftKey) {
        event.preventDefault();
        this.userInput += "\n";
      }
    },
    handleCtrlEnterKey(event) {
      if (event.ctrlKey) {
        event.preventDefault();
        this.sendMessage();
      }
    },
  },
};
</script>
  
  <style scoped>
@import url("../../css/ChatBoxStyles.css");
</style>
  