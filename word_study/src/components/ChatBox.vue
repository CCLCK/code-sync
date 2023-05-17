<template>
    
  <div class="chat-box-container">
    
    <div v-if="isChatOpen" class="chat-box">
      <div class="chat-header" @click="isChatOpen = !isChatOpen">
        <h3 class="header-text">Word Usage</h3>
      </div>
      <div class="chat-content">
        <div v-for="(message, index) in messages" :key="index" class="message">
          <div v-if="message.sender === 'user'" class="user-message">
            <pre>{{ message.text }}</pre>
          </div>
          <div v-else class="bot-message">
            <pre>{{ message.text }}</pre>
          </div>
        </div>
      </div>
      <div class="chat-input">
        <textarea
          v-model="userInput"
          placeholder="Type your message..."
          @keydown.enter.exact.prevent="handleEnterKey"
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
        .post("http://localhost:5000/api/chat", { message: userInput })
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
  },
};
</script>
  
  <style scoped>
.chat-box-container {
  position: fixed;
  right: 20px;
  bottom: 80px; /* 调整适应右边的位置 */
  z-index: 1000;
}

.chat-box {
  height: calc(100vh - 200px);

  bottom: 0;
  width: 400px;
  background-color: #f2f2f2;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  right: 0; /* 调整聊天框靠右对齐 */
  left: unset; /* 移除左对齐属性 */
}

.chat-header {
  margin-bottom: 10px;
  cursor: pointer;
  background-color: #007bff;
  color: white;
  padding: 5px;
  text-align: center;
}

.header-text {
  margin: 0;
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
}

.chat-content {
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  padding: 10px;
  overflow-y: auto;
}
.message {
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
    max-width: 80%;
  }
  .user-message,
  .bot-message {
    position: relative;
    margin-bottom: 10px;  /* 减小了消息之间的间隔 */
    padding: 2px 3px;  /* 减小了消息内的填充空间 */
    border-radius: 10px;
    max-width: 80%;
    font-size: 14px;  /* 减小了字体的大小 */
    font-family: "Microsoft YaHei", sans-serif;
  }
  
  .user-message {
    align-self: flex-end; /* 靠右对齐 */
    background: linear-gradient(135deg, #1e6b7f 0%, #0084ff 100%);
    color: white;
    margin-left: 20%;
  }
  
  .user-message::after {
    content: "";
    position: absolute;
    top: 0;
    right: -8px;
    border-width: 8px 8px 8px 0;
    border-style: solid;
    border-color: transparent #1e6b7f transparent transparent;
  }
  
  .bot-message {
    align-self: flex-start; /* 靠左对齐 */
    background: linear-gradient(135deg, #f4f4f4 0%, #e9e9e9 100%);
    color: #333;
    margin-right: 20%;
  }
  
  .bot-message::before {
    content: "";
    position: absolute;
    top: 0;
    left: -8px;
    border-width: 8px 0 8px 8px;
    border-style: solid;
    border-color: transparent transparent transparent #f4f4f4;
  }
  
  
  

.chat-input {
  display: flex;
  align-items: center;
}

textarea {
  flex: 1;
  height: 100px;
  width: 280px;
  margin-bottom: 10px;
  resize: none;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-family: Arial, sans-serif;
  font-size: 14px;
}

.send-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 3px;
  padding: 8px 15px;
  font-family: Arial, sans-serif;
  font-size: 14px;
  margin-left: 10px;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.send-button:hover {
  background-color: #0056b3;
}

.chat-icon {
  width: 40px;
  height: 40px;
  background-color: #007bff;
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.chat-icon:hover {
  background-color: #0056b3;
}

@media (max-width: 400px) {
  .chat-box {
    width: 90%;
  }
}
</style>
  