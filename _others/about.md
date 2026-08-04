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

<!-- Pronounciation -->

<div class="pron-quiz-container">

<style>
.pron-quiz-container {
  max-width: 700px;
  margin: 20px auto;
  padding: 20px;
  border: 3px solid #e7c000;
  border-radius: 10px;
  background: #fff8d8;
  font-family: Arial, Helvetica, sans-serif;
}

.pron-quiz-container h3 {
  margin-top: 0;
}

.pron-question {
  margin: 20px 0;
  padding: 5px 20px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e7c000;
}

.pron-word {
  font-weight: bold;
  font-size: 1.1em;
  margin-bottom: 8px;
}

.pron-answer {
  width: 90%;
  padding: 8px;
  font-size: 1em;
  margin-top: 8px;
}

.pron-feedback {
  margin-top: 8px;
  font-weight: bold;
}

.pron-correct {
  color: #0b7a0b;
}

.pron-incorrect {
  color: #b00020;
}

.pron-button {
  margin-top: 20px;
  margin-right: 10px;
  padding: 10px 18px;
  font-size: 1em;
  cursor: pointer;
}

#pron-score {
  margin-top: 20px;
  font-size: 1.1em;
  font-weight: bold;
}

</style>


<h3>Exercise B</h3>

<p>
<strong>
Review the rules for pronunciation above, then write the following Latin words phonetically.
</strong>
</p>

<p>
Example: <em>amīcus</em> → a-mee-kus
</p>


<div id="pron-quiz"></div>


<button class="pron-button" onclick="checkPronQuiz()">Check Answers</button>
<button class="pron-button" onclick="resetPronQuiz()">Reset</button>


<div id="pron-score"></div>



<script>

(function(){

const pronQuestions = [

{
word:"faciō",
answer:"fa-kee-oh"
},

{
word:"audīvī",
answer:"ow-dee-wee"
},

{
word:"pedibus",
answer:"pe-dee-boos"
},

{
word:"virōrum",
answer:"wee-roh-room"
},

{
word:"cognōscere",
answer:"kog-noh-skeh-reh"
},

{
word:"iacuī",
answer:"yah-koo-ee"
},

{
word:"pudicitia",
answer:"poo-dee-kee-tee-ah"
},

{
word:"iubeō",
answer:"yoo-beh-oh"
},

{
word:"inimīcus",
answer:"ee-nee-mee-koos"
},

{
word:"viae",
answer:"wee-eye"
}

];


const pronContainer=document.getElementById("pron-quiz");


function normalizePron(text){

return text
.toLowerCase()
.replace(/[.,!?]/g,"")
.replace(/\s+/g," ")
.trim();

}



function buildPronQuiz(){

pronContainer.innerHTML="";


pronQuestions.forEach((q,i)=>{


pronContainer.innerHTML += `

<div class="pron-question">

<div class="pron-word">
${i+1}. ${q.word}
</div>


<input 
class="pron-answer"
id="pron-answer-${i}"
type="text"
placeholder="Write phonetic pronunciation here">


<div 
id="pron-feedback-${i}" 
class="pron-feedback">
</div>


</div>

`;

});

}



window.checkPronQuiz=function(){

let score=0;


pronQuestions.forEach((q,i)=>{


let studentAnswer=
document.getElementById(`pron-answer-${i}`).value;


let feedback=
document.getElementById(`pron-feedback-${i}`);



if(normalizePron(studentAnswer)===normalizePron(q.answer)){


score++;

feedback.className="pron-feedback pron-correct";
feedback.innerHTML="✓ Correct.";


}

else{


feedback.className="pron-feedback pron-incorrect";
feedback.innerHTML=
`Suggested pronunciation: <strong>${q.answer}</strong>`;

}


});


document.getElementById("pron-score").innerHTML =
`Score: ${score} / ${pronQuestions.length}`;


}



window.resetPronQuiz=function(){

buildPronQuiz();

document.getElementById("pron-score").innerHTML="";

}



buildPronQuiz();


})();

</script>

</div>

<!-- Pronouncation END -->