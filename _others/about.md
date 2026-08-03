---
title: Test HTML Structures
author: Tao He
date: 2022-02-04
category: Jekyll
layout: post
---

Place for test code

<style>
  .verb-quiz-container {
    padding: 15px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
    max-width: 500px;
    margin: 20px 0;
    font-family: inherit;
  }
  .quiz-sentence {
    font-size: 1.1em;
    margin-bottom: 15px;
  }
  .quiz-select {
    padding: 5px;
    font-size: 1em;
    border: 2px solid #aaa;
    border-radius: 4px;
  }
  .quiz-btn {
    padding: 8px 15px;
    background-color: #0076df;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  .quiz-btn:hover { background-color: #0056b3; }
  .quizFeedback { margin-top: 10px; font-weight: bold; }
  .correct { color: #28a745; }
  .incorrect { color: #dc3545; }
</style>

<script>
  // Shared verification logic across all instances
  function checkVerbAnswer(buttonEl) {
    const container = buttonEl.parentElement;
    const selectEl = container.querySelector('.verbSelect');
    const feedbackEl = container.querySelector('.quizFeedback');
    
    const selectedValue = selectEl.value;
    const correctAnswer = selectEl.dataset.correct;
    
    if (!selectedValue) {
      feedbackEl.textContent = "Please select an answer first.";
      feedbackEl.className = "quizFeedback";
      return;
    }
    
    if (selectedValue === correctAnswer) {
      feedbackEl.textContent = "Correct! ✨";
      feedbackEl.className = "quizFeedback correct";
    } else {
      feedbackEl.textContent = "Incorrect. Try again!";
      feedbackEl.className = "quizFeedback incorrect";
    }
  }
</script>


<!-- Question Block Start -->
<div class="verb-quiz-container">
  <p class="quiz-sentence">
    <span class="sentenceBefore"></span>
    <select class="verbSelect quiz-select">
      <option value="" disabled selected>Select conjugation...</option>
    </select>
    <span class="sentenceAfter"></span>
  </p>
  
  <button onclick="checkVerbAnswer(this)" class="quiz-btn">Check Answer</button>
  <p class="quizFeedback"></p>
</div>

<script>
  (function() {
    // CONFIGURATION: Set your sentence details for THIS specific block here
    const quizData = {
      beforeText: "By the time we arrived, they had already ",
      afterText: " dinner.",
      correctAnswer: "eaten",
      options: ["eat", "ate", "eating", "eaten"]
    };

    // Get the current container (the one just created above this script)
    const scripts = document.getElementsByTagName('script');
    const currentScript = scripts[scripts.length - 1];
    const container = currentScript.previousElementSibling;

    // Populate data safely within this specific container
    container.querySelector('.sentenceBefore').textContent = quizData.beforeText;
    container.querySelector('.sentenceAfter').textContent = quizData.afterText;

    // Save the correct answer directly on the select element for validation later
    const selectEl = container.querySelector('.verbSelect');
    selectEl.dataset.correct = quizData.correctAnswer;

    quizData.options.forEach(opt => {
      let option = document.createElement('option');
      option.value = opt;
      option.textContent = opt;
      selectEl.appendChild(option);
    });
  })();
</script>
<!-- Question Block End -->

