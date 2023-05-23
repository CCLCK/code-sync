<template>
  <div class="word-notebook" v-if="isVisible">
    <h2>Your Word Notebook</h2>
    <ul>
      <li v-for="(word, index) in words" :key="index">
        {{ word }}
        <button @click="removeWord(word, index)">Remove</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    words: {
      type: Array,
      default: () => [],
    },
    isVisible: {
      type: Boolean,
      default: false,
    },
  },
  data() {
  
  },
  methods: {
    async removeWord(word, index) {
  try {
    // Remove word from the backend notebook
    const userId = localStorage.getItem('user_id');
    const response = await axios.post('http://localhost:5500/api/user/remove_word', {
      user_id: userId,
      word: word
    });
    if (response.data.status === 'success') {
      // If word removed successfully from backend, remove from the frontend list
      let newWords = [...this.words]; // 创建words数组的副本
      newWords.splice(index, 1); // 在副本上进行修改
      this.$emit('updateWords', newWords); // 发送更新事件，带上新的数组
    } else {
      console.error(response.data.message);
    }
  } catch (error) {
    console.error(error);
  }
},

    toggleVisibility() {
      this.$emit("toggle-visibility");
    },

  },

};
</script>

<style scoped>
@import url("../../css/notebook.css");
</style>
