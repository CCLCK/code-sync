<template>
    <div
      id="card"
      class="card"
      @mouseleave="startCountdown"
      @mouseenter="stopCountdown"
    >
      <h1>{{ word.word }}</h1>
  
      <p v-show="isDefinitionVisible">
        {{ word.definition }}
      </p>
      <p
        v-show="
          isDefinitionVisible && word.example.length > 0
        "
      >
        <strong>例句：</strong> {{ word.example }}
      </p>
      <p
        v-show="
          isDefinitionVisible &&
          word.example_translation.length > 0
        "
      >
        <strong>例句翻译：</strong>
        {{ word.example_translation }}
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
  
      <p v-if="focusLostCountdown > 0" class="countdown-message">
        焦点将在 {{ focusLostCountdown }} 秒后消失
      </p>
    </div>
  </template>
  
  <script>
  export default {
    props: ['word', 'isDefinitionVisible', 'showDefinition', 'nextWord', 'startCountdown', 'stopCountdown', 'focusLostCountdown'],
  }
  </script>
  