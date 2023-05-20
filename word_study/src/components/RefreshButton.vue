<template>
    <button class="button" @click="debouncedRefresh">获取新的单词</button>
  </template>
  
  <script>
  import { debounce } from "lodash";
  
  export default {
    methods: {
      refresh() {
        this.$emit("refresh");
      },
    },
    computed: {
      debouncedRefresh() {
        return debounce(this.refresh, 3000, { leading: true, trailing: false });
      },
    },
  };
  </script>
  
  <style scoped>
  .button {
    /* 这里定义按钮的样式 */
    background-color: #00667c;
    background-image: linear-gradient(to right, #00667c, #004999);
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    margin-top: 20px; /* 将按钮往下方移动20px */
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
    transition: background-color 0.3s ease;
  }
  
  .button:hover {
    background-color: #004999;
  }
  
  </style>
  