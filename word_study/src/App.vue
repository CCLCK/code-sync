<template>
  <div id="app">
    <!-- 添加一个头部 -->
    <header>
      <h1>Word Journeyman</h1>
      <div class="user-actions-container">
        <user-actions></user-actions> <!-- 放在容器内 -->
      </div>
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
      </div>
      <word-card
  v-if="words.length > 0"
  :word="words[currentWordIndex]"
  :isDefinitionVisible="isDefinitionVisible"
  :showDefinition="showDefinition"
  :nextWord="nextWord"
  :startCountdown="startCountdown"
  :stopCountdown="stopCountdown"
  :focusLostCountdown="focusLostCountdown"
  @add-word-to-notebook="addWordToNotebook"
>
</word-card>

<div v-else class="loading-wrap" >
  <div class="balls">
    <div></div>
    <div></div>
    <div></div>
  </div>
</div>


  <refresh-button
        class="refresh-button"
        @refresh="getNewWords"
      ></refresh-button>


      
      
      <!-- 聊天框组件 -->
      <chat-box></chat-box>

      <button class="sidebar-button" @click="toggleNotebookVisibility">Toggle Word Notebook</button>
      <word-notebook
      :words="notebookWords"
      :isVisible="isNotebookVisible"
      @remove-word="removeWordFromNotebook"
      @toggle-visibility="toggleNotebookVisibility"
      @updateWords="updateWords"
    ></word-notebook>
    </div>

    <!-- 添加一个底部 -->
    <footer>
      <p>©2023 Word Journeyman</p>
    </footer>
  </div>
</template>


<script>
import UserActions from './components/UserActions.vue'
import ContactUs from "./components/ContactUs.vue"; // 确保这里的路径是正确的
import ChatBox from "./components/ChatBox.vue"; // 引入你的聊天框组件
import RefreshButton from "./components/RefreshButton.vue";
import axios from "axios";
import WordCard from "./components/WordCard.vue";
import WordNotebook from "./components/WordNotebook.vue";
export default {
  components: {
    "contact-us": ContactUs, // 在这里注册你的组件
    "chat-box": ChatBox, // 注册你的聊天框组件
    RefreshButton,
    WordCard,
    WordNotebook,
    "user-actions":UserActions
  },
  data() {
    return {
      words: [],
      currentWordIndex: 0,
      isDefinitionVisible: false,
      searchTerm: "",
      focusLostCountdown: 0,
      countdownInterval: null, // 新增一个变量来存储倒计时的interval
      browsedWords: [], // 新增一个变量来存储已浏览的单词
      newWords: [], // 新的一组单词
      isNotebookVisible: false,
      notebookWords: [], // 生词本中的单词
     
     
    };
  },
  created() {
    const word = this.$route.params.word;
    if (word) {
      this.jumpToWord(word);
    }
    axios
      .get("http://localhost:5800/random-words")
      .then((response) => {
        this.words = response.data;
        
      })
      .catch((error) => {
        console.error("Error fetching random words:", error);
       
      });
  },
  methods: {
    
    updateWords(newWords) {
    this.notebookWords = newWords;
  },
    async toggleNotebookVisibility() {
      this.isNotebookVisible = !this.isNotebookVisible;
      try {
        console.log('111');
        const userId = localStorage.getItem('user_id');
        const response = await axios.get('http://localhost:5500/api/user/words', {
          params: { user_id: userId }
        });
        if (response.data.status === 'success') {
          this.notebookWords = response.data.words;
        } else {
          console.error(response.data.message);
        }
      } catch (error) {
        console.error(error);
      }
    },
    
    removeWordFromNotebook(index) {
  this.notebookWords.splice(index, 1);
},

async addWordToNotebook() {
	const currentWord = this.words[this.currentWordIndex].word;
	if (!this.notebookWords.includes(currentWord)) {
		// 如果当前单词不在生词本中，就添加到列表
		this.notebookWords.push(currentWord);

		try {
			// 向后端发送添加生词的请求
			const userId = localStorage.getItem('user_id'); // 获取存储在localStorage中的用户ID
			const response = await axios.post('http://localhost:5500/api/user/add_word', {
				user_id: userId,
				word: currentWord
			});

			if (response.data.status !== 'success') {
				// 如果后端返回的状态不是'success'，则将单词从生词本中移除，并打印错误消息
				const index = this.notebookWords.indexOf(currentWord);
				if (index > -1) {
					this.notebookWords.splice(index, 1);
				}
				console.error(response.data.message);
			}
		} catch (error) {
			console.error(error);
		}
	}
},


    showDefinition() {
      this.isDefinitionVisible = true;
    },
    fetchWord(word, showDefinitionImmediately = false) {
      axios
        .get(`http://localhost:5100/words/${word}`)
        .then((response) => {
          console.log(response.data);
          const index = this.words.findIndex((w) => w.word === word);
          if (index >= 0) {
            this.words[index].definition = response.data.definition;
            this.words[index].example = response.data.example;
            this.words[index].example_translation =
              response.data.example_translation; // 新增的例句翻译

            this.currentWordIndex = index;
          } else {
            this.words.push({
              word: response.data.word,
              definition: response.data.definition,
              example: response.data.example,
              example_translation: response.data.example_translation, // 新增的例句翻译
            });
            this.currentWordIndex = this.words.length - 1;
          }

          // console.log(this.words[index].word);
          // console.log(response.data.word);
          console.log(response.data);
          console.log(showDefinitionImmediately);
          // Only show definition if we got a valid response and we should show definition immediately.
          if (
            response.data &&
            response.data.word &&
            showDefinitionImmediately
          ) {
            this.showDefinition(); // 显示搜索到的单词定义
          }
        })
        .catch((error) => {
          console.error("Error fetching word:", error);
        });
    },

    searchWord() {
      this.fetchWord(this.searchTerm, true); // Search should show definition immediately
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
      this.fetchWord(this.words[this.currentWordIndex].word); // 'Next' should not show definition immediately
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

    getNewWords() {
     
      this.words = [];  // 清空单词列表
      axios
        .get("http://localhost:5800/random-words")
        .then((response) => {
          this.newWords = response.data;
          this.words = this.newWords; // 更新单词列表
           
        })
        .catch((error) => {
          console.error("Error fetching new words:", error);
          
        });
    },
  },
};
window.addEventListener('beforeunload', function() {
  localStorage.clear();
});

</script>


<style scoped>

@import url("../css/loading.css");
@import url("../css/styles.css");
@import url("../css/notebook-button.css");
</style>