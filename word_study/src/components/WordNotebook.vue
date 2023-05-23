<template>
    <div class="word-notebook" v-if="isVisible">
      <h2>Your Word Notebook</h2>
      <ul>
        <li v-for="(word, index) in words" :key="index">
          {{ word }}
          <button @click="removeWord(index)">Remove</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
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
    methods: {
      removeWord(index) {
        this.$emit("remove-word", index);
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
  