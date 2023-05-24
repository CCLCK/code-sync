let words = [
    { word: 'apple', definition: '一种常见的水果' },
    { word: 'banana', definition: '一种常见的黄色水果' },
    { word: 'cat', definition: '一种家养的小型猫科动物' },
    // 可以添加更多单词
];
let currentWordIndex = 0;

function showWord() {
    document.getElementById('word').innerText = words[currentWordIndex].word;
    document.getElementById('showDefinition').disabled = false;
    document.getElementById('definition').style.display = 'none';
}

function showDefinition() {
    document.getElementById('definition').style.display = 'block';
    document.getElementById('definition').innerText = words[currentWordIndex].definition;
    document.getElementById('showDefinition').disabled = true;
}

function nextWord() {
    // 计算下一个单词的索引。这里使用模运算符 (%) 以确保索引在合理的范围内（0 到 words.length - 1）。
    currentWordIndex = (currentWordIndex + 1) % words.length;

    // 获取单词卡片元素，并将 'sliding' 类添加到它的类列表中。这将应用CSS中定义的滑动动画。
    var card = document.getElementById('card');
    card.classList.add('sliding');

    // 设置一个定时器，在 300 毫秒后执行。
    setTimeout(function() {
        // 在动画结束后，从卡片的类列表中删除 'sliding' 类。
        card.classList.remove('sliding');

        // 显示新的单词。
        showWord();
    }, 500);
}

document.addEventListener('DOMContentLoaded', (event) => {
    showWord();
});

