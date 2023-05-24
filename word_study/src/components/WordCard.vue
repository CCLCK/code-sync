<template>
    <div
    id="card"
    class="card"
    
    @mouseleave="startCountdown"
    @mouseenter="stopCountdown"
  >
    <div class="word-container"
    @dblclick="$emit('add-word-to-notebook')">
      <h1>{{ word.word }}</h1>
      <font-awesome-icon
        icon="copy"
        class="copy-icon"
        @click="copyToClipboard(word.word)"
      />
    </div>

    <p v-show="isDefinitionVisible">
      {{ word.definition }}
    </p>
    <p v-show="isDefinitionVisible && word.example.length > 0">
      <strong>例句：</strong> {{ word.example }}
    </p>
    <p v-show="isDefinitionVisible && word.example_translation.length > 0">
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
  props: [
    "word",
    "isDefinitionVisible",
    "showDefinition",
    "nextWord",
    "startCountdown",
    "stopCountdown",
    "focusLostCountdown",
  ],
  methods: {
    // ...
    copyToClipboard(text) {
      navigator.clipboard.writeText(text).then(
        function () {
          console.log("Copying to clipboard was successful!");
        },
        function (err) {
          console.error("Could not copy text: ", err);
        }
      );
    },
    // ...
  },
};
</script>
  

<style scoped>
.word-container {
  position: relative;
}

.copy-icon {
  position: absolute;
  right: 0;
  top: 0;
  font-size: 0.9em;
  visibility: hidden;
}

.word-container:hover .copy-icon {
  visibility: visible;
}

  
</style>