---
title: Test HTML Structures
author: Tao He
date: 2022-02-04
category: Jekyll
layout: post
---

Place for test code

<!-- Conjugation Block  -->

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

<!-- Conjugation Block End -->




<!-- POS Block  -->
<style>
  .pos-quiz-container {
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 6px;
    background-color: #ffffff;
    max-width: 650px;
    margin: 25px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    font-family: inherit;
  }
  .pos-sentence-display {
    font-size: 1.3em;
    line-height: 1.8;
    margin-bottom: 20px;
    word-wrap: break-word;
  }
  .pos-word {
    display: inline-block;
    transition: filter 0.25s ease, color 0.25s ease;
    border-bottom: 1px dashed #ccc;
  }
  .pos-word.blurred {
    filter: blur(5px);
    color: transparent;
    user-select: none; /* Prevents cheating by highlighting text */
    border-bottom: 1px dashed #aaa;
  }
  .pos-btn-group {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  .pos-toggle-btn {
    padding: 6px 12px;
    font-size: 0.9em;
    background-color: #f0f0f0;
    color: #333;
    border: 1px solid #ccc;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .pos-toggle-btn:hover {
    background-color: #e5e5e5;
  }
  .pos-toggle-btn.active {
    background-color: #0076df;
    color: white;
    border-color: #0056b3;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);
  }
</style>


<!-- POS Reveal Block Start -->
<div class="pos-quiz-container">
  <!-- Interactive Sentence Display -->
  <div class="pos-sentence-display"></div>
  
  <!-- Dynamic Toggle Buttons -->
  <div class="pos-btn-group"></div>
</div>

<script>
  (function() {
    // CONFIGURATION: Define your words and their associated part of speech (pos)
    const sentenceData = [
      { word: "The", pos: "Determiner" },
      { word: "quick", pos: "Adjective" },
      { word: "brown", pos: "Adjective" },
      { word: "fox", pos: "Noun" },
      { word: "jumps", pos: "Verb" },
      { word: "over", pos: "Preposition" },
      { word: "the", pos: "Determiner" },
      { word: "lazy", pos: "Adjective" },
      { word: "dog.", pos: "Noun" }
    ];

    // Locate the specific container just above this script
    const scripts = document.getElementsByTagName('script');
    const currentScript = scripts[scripts.length - 1];
    const container = currentScript.previousElementSibling;
    
    const sentenceDisplay = container.querySelector('.pos-sentence-display');
    const btnGroup = container.querySelector('.pos-btn-group');

    // Extract unique parts of speech to build toggle buttons
    const uniquePOS = [...new Set(sentenceData.map(item => item.pos))];

    // Build the sentence words as individual blurred spans
    sentenceData.forEach((item, index) => {
      const span = document.createElement('span');
      span.textContent = item.word;
      span.className = 'pos-word blurred';
      // Normalize POS class names (e.g., "Preposition" -> "pos-preposition")
      span.classList.add(`pos-${item.pos.toLowerCase()}`);
      sentenceDisplay.appendChild(span);
      
      // Add a tiny trailing space between words
      if (index < sentenceData.length - 1) {
        sentenceDisplay.appendChild(document.createTextNode(' '));
      }
    });

    // Build toggle buttons for each distinct part of speech found
    uniquePOS.forEach(posName => {
      const btn = document.createElement('button');
      btn.textContent = posName;
      btn.className = 'pos-toggle-btn';
      
      btn.addEventListener('click', function() {
        this.classList.toggle('active');
        const targetClass = `pos-${posName.toLowerCase()}`;
        const words = sentenceDisplay.querySelectorAll(`.${targetClass}`);
        
        words.forEach(word => {
          word.classList.toggle('blurred');
        });
      });
      
      btnGroup.appendChild(btn);
    });
  })();
</script>
<!-- POS Reveal Block End -->

<!-- POS Block End -->

<!-- function identification -->

<div class="latin-function-quiz">

<style>
.latin-function-quiz{
      max-width: 700px;
      margin: 20px auto;
      padding: 20px;
      border: 3px solid #e7c000;
      border-radius: 10px;
      background:  #fff8d8;
      font-family: Arial, Helvetica, sans-serif;
    }

.latin-function-quiz h3{
    margin-top:0;
}

.question{
    background:white;
    border:1px solid #ddd;
    border-radius:8px;
    padding:15px;
    margin:18px 0;
}

.question p{
    margin-top:0;
    font-size:1.05em;
}

.feedback{
    margin-top:10px;
    font-weight:bold;
}

.correct{
    color:green;
}

.incorrect{
    color:#b30000;
}

input[type=text]{
    padding:6px;
    font-size:1em;
    width:170px;
}

button{
    padding:10px 18px;
    margin-right:10px;
    margin-top:20px;
    cursor:pointer;
    font-size:1em;
}
</style>

<h3>Exercise B</h3>

<p><strong>For each clause, choose the grammatical function of the <u>underlined</u> word. Then enter the correct Latin form.</strong></p>

<div id="latinQuiz"></div>

<button onclick="gradeLatinQuiz()">Check Answers</button>
<button onclick="resetLatinQuiz()">Reset</button>

<div id="latinScore" style="margin-top:20px;font-weight:bold;font-size:1.1em;"></div>

<script>

const latinQuestions = [

{
sentence:'He loves his <u>mother</u>.',
answer:'Object',
latin:'matrem'
},

{
sentence:'He does see the <u>foot</u>.',
answer:'Object',
latin:'pedem'
},

{
sentence:'She <u>is holding</u> them.',
answer:'Verb',
latin:'tenet'
},

{
sentence:'My <u>eyes</u> see the sons.',
answer:'Subject',
latin:'oculi'
},

{
sentence:'The <u>men</u> are fathers.',
answer:'Subject',
latin:'viri'
}

];

const container=document.getElementById("latinQuiz");

function buildLatinQuiz(){

container.innerHTML="";

latinQuestions.forEach((q,i)=>{

container.innerHTML+=`

<div class="question">

<p>${q.sentence}</p>

<label>
<input type="radio" name="role${i}" value="Subject">
Subject
</label>

<label style="margin-left:15px;">
<input type="radio" name="role${i}" value="Object">
Object
</label>

<label style="margin-left:15px;">
<input type="radio" name="role${i}" value="Verb">
Verb
</label>

<br><br>

<label>
Latin form:
<input type="text" id="latin${i}">
</label>

<div id="feedback${i}" class="feedback"></div>

</div>

`;

});

}

function gradeLatinQuiz(){

let score=0;
let possible=latinQuestions.length*2;

latinQuestions.forEach((q,i)=>{

const role=document.querySelector(`input[name="role${i}"]:checked`);
const latin=document.getElementById(`latin${i}`).value.trim().toLowerCase();

let fb=document.getElementById(`feedback${i}`);

let roleCorrect=false;
let latinCorrect=false;

if(role && role.value===q.answer){
roleCorrect=true;
score++;
}

if(latin===q.latin.toLowerCase()){
latinCorrect=true;
score++;
}

if(roleCorrect && latinCorrect){

fb.className="feedback correct";
fb.innerHTML="✓ Both answers are correct.";

}else{

fb.className="feedback incorrect";

let text="";

if(!roleCorrect){
text+=`Role: <strong>${q.answer}</strong>. `;
}

if(!latinCorrect){
text+=`Latin: <strong>${q.latin}</strong>.`;
}

fb.innerHTML=text;

}

});

document.getElementById("latinScore").innerHTML=
`Score: ${score} / ${possible}`;

}

function resetLatinQuiz(){

buildLatinQuiz();

document.getElementById("latinScore").innerHTML="";

}

buildLatinQuiz();

</script>

</div>

<!-- END -->
