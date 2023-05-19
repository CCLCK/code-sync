<template>
  <div id="app">
    <!-- 添加一个头部 -->
    <header>
      <h1>Word Journeyman</h1>
      <nav>
        <a href="#"></a>
        <contact-us></contact-us>
      </nav>
    </header>

    <!-- 添加侧边栏 -->
    <div class="sidebar">
      <h2>单词探索历程</h2>
      <ul>
        <li v-for="word in browsedWords" :key="word" @click="jumpToWord(word)">
          {{ word }}
        </li>
      </ul>
    </div>

    <div class="center-container">
      <!-- 搜索栏 -->
      <div class="search-bar">
        <input
          v-model="searchTerm"
          type="text"
          placeholder="搜索单词..."
          @keyup.enter="searchWord"
        />
        <button @click="searchWord">搜索</button>
        <p>{{ searchMessage }}</p>
        <!-- 新增一行来显示searchMessage -->

        <!-- 单词卡片 -->
        <div
          id="card"
          class="card"
          @mouseleave="startCountdown"
          @mouseenter="stopCountdown"
        >
          <!-- 卡片内容 -->
          <h1>{{ words[currentWordIndex].word }}</h1>

          <!-- 定义显示 -->
          <p v-show="isDefinitionVisible">
            {{ words[currentWordIndex].definition }}
          </p>
          <p v-show="isDefinitionVisible">
            <strong>例句：</strong> {{ words[currentWordIndex].example }}
          </p>

          <div class="card-buttons">
            <button
              class="button"
              @click="showDefinition"
              :disabled="isDefinitionVisible"
            >
              显示定义
            </button>
            <button class="button" @click="nextWord">下一个单词</button>
          </div>

          <!-- 小字提醒 -->
          <p v-if="focusLostCountdown > 0" class="countdown-message">
            焦点将在 {{ focusLostCountdown }} 秒后消失
          </p>
        </div>
      </div>

      <!-- 聊天框组件 -->
      <chat-box></chat-box>
    </div>

    <!-- 添加一个底部 -->
    <footer>
      <p>©2023 Word Journeyman</p>
    </footer>
  </div>
</template>


<script>
import ContactUs from "./components/ContactUs.vue"; // 确保这里的路径是正确的
import ChatBox from "./components/ChatBox.vue"; // 引入你的聊天框组件
import axios from "axios";

export default {
  components: {
    "contact-us": ContactUs, // 在这里注册你的组件
    "chat-box": ChatBox, // 注册你的聊天框组件
  },
  data() {
    return {
      words: [
        { word: "apple", definition: "一种常见的水果" },
        { word: "banana", definition: "一种常见的黄色水果" },
        { word: "cat", definition: "一种家养的小型猫科动物" },
        { word: "dog", definition: "一种家养的哺乳动物" },
        { word: "elephant", definition: "一种大型陆生哺乳动物" },
        { word: "fox", definition: "一种小型犬科动物" },
        { word: "grape", definition: "一种常见的浆果" },
        { word: "horse", definition: "一种大型哺乳动物" },
        { word: "iguana", definition: "一种大型蜥蜴" },
        { word: "jaguar", definition: "一种大型猫科动物" },
      ],
      currentWordIndex: 0,
      isDefinitionVisible: false,
      searchTerm: "",
      focusLostCountdown: 0,
      countdownInterval: null, // 新增一个变量来存储倒计时的interval
      browsedWords: [], // 新增一个变量来存储已浏览的单词
    };
  },
  created() {
    const word = this.$route.params.word;
    if (word) {
      this.jumpToWord(word);
    }
  },
  methods: {
    showDefinition() {
      this.isDefinitionVisible = true;
    },
    fetchWord(word) {
      axios
        .get(`http://localhost:5000/words/${word}`)
        .then((response) => {
          console.log(response.data);
          const index = this.words.findIndex((w) => w.word === word);
          if (index >= 0) {
            this.words[index].definition = response.data.definition;
            this.words[index].example = response.data.example; // 新增的例句
          } else {
            this.words.push({
              word: response.data.word,
              definition: response.data.definition,
              example: response.data.example, // 新增的例句
            });
            this.currentWordIndex = this.words.length - 1;
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },

    nextWord() {
      const currentWord = this.words[this.currentWordIndex].word;
      if (!this.browsedWords.includes(currentWord)) {
        // 如果当前单词不在已浏览单词列表中，就添加到列表
        this.browsedWords.push(currentWord);
      }
      this.currentWordIndex = (this.currentWordIndex + 1) % this.words.length;
      this.isDefinitionVisible = false;
      this.$router.push(`/words/${this.words[this.currentWordIndex].word}`);
      this.fetchWord(this.words[this.currentWordIndex].word);
    },

    // ...

    jumpToWord(word) {
      const index = this.words.findIndex((w) => w.word === word);
      if (index !== -1) {
        this.currentWordIndex = index;
      }
      this.$router.push(`/words/${word}`);
      this.fetchWord(word);
    },

    searchWord() {
      this.fetchWord(this.searchTerm);
    },
    startCountdown() {
      this.focusLostCountdown = 5;
      this.countdownInterval = setInterval(() => {
        if (this.focusLostCountdown > 0) {
          this.focusLostCountdown--;
        } else {
          clearInterval(this.countdownInterval);
        }
      }, 1000);
    },
    stopCountdown() {
      clearInterval(this.countdownInterval);
      this.focusLostCountdown = 0;
    },

    clearBrowsedWords() {
      this.browsedWords = [];
    },
  },
};
</script>


<style scoped>
@import url("../css/styles.css");
</style>