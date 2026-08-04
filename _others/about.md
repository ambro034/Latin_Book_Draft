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

<!-- Subject predicate  -->
<div class="sp-quiz-container">

<style>
.sp-quiz-container {
  max-width: 700px;
  margin: 20px auto;
  padding: 20px;
  border: 3px solid #e7c000;
  border-radius: 10px;
  background: #fff8d8;
  font-family: Arial, Helvetica, sans-serif;
}

.sp-quiz-container h3 {
  margin-top: 0;
}

.sp-question {
  margin: 20px 0;
  padding: 5px 20px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e7c000;
}

.sp-sentence {
  font-weight: bold;
  font-size: 1.1em;
  margin-bottom: 12px;
}

.sp-word {
  padding: 5px;
  margin: 2px;
  cursor: pointer;
  border-radius: 4px;
  display: inline-block;
}

.sp-word:hover {
  background: #fff1a8;
}

.sp-selected-subject {
  background: #cce5ff;
}

.sp-selected-predicate {
  background: #d4edda;
}

.sp-no-clause {
  margin-top: 10px;
}

.sp-feedback {
  margin-top: 8px;
  font-weight: bold;
}

.sp-correct {
  color: #0b7a0b;
}

.sp-incorrect {
  color: #b00020;
}

.sp-button {
  margin-top: 20px;
  margin-right: 10px;
  padding: 10px 18px;
  font-size: 1em;
  cursor: pointer;
}

#sp-score {
  margin-top: 20px;
  font-size: 1.1em;
  font-weight: bold;
}
</style>


<h3>Exercise A</h3>

<p>
<strong>
Circle the subject(s) and underline the predicate(s). 
If there is no clause, write an X.
</strong>
</p>


<div id="sp-quiz"></div>


<button class="sp-button" onclick="checkSPQuiz()">Check Answers</button>
<button class="sp-button" onclick="resetSPQuiz()">Reset</button>

<div id="sp-score"></div>



<script>

(function(){

const spQuestions = [

{
sentence:["The","dog","barks","at","the","bird"],
subjects:["dog"],
predicates:["barks"],
noclause:false
},

{
sentence:["After","we","see","the","field"],
subjects:["we"],
predicates:["see"],
noclause:false
},

{
sentence:["Once","my","friends","leave"],
subjects:["friends"],
predicates:["leave"],
noclause:false
},

{
sentence:["In","the","afternoon"],
subjects:[],
predicates:[],
noclause:true
},

{
sentence:["If","you","build","it,","they","will","come"],
subjects:["you","they"],
predicates:["build","will come"],
noclause:false
},

{
sentence:["We","are","happy"],
subjects:["We"],
predicates:["are happy"],
noclause:false
},

{
sentence:["We","are"],
subjects:["We"],
predicates:["are"],
noclause:false
},

{
sentence:["Many","of","the","people"],
subjects:[],
predicates:[],
noclause:true
},

{
sentence:["She’s","happy"],
subjects:["She’s"],
predicates:["happy"],
noclause:false
},

{
sentence:["I","am","reading","the","book"],
subjects:["I"],
predicates:["am reading"],
noclause:false
}

];


const spContainer=document.getElementById("sp-quiz");


let spSelections=[];


function buildSPQuiz(){

spContainer.innerHTML="";
spSelections=[];


spQuestions.forEach((q,i)=>{

spSelections[i]=[];


let words=q.sentence.map((word,index)=>{

return `
<span 
class="sp-word" 
onclick="selectSPWord(${i},${index},this)">
${word}
</span>`;

}).join(" ");


spContainer.innerHTML+=`

<div class="sp-question">

<div class="sp-sentence">
${i+1}. ${words}
</div>


<label class="sp-no-clause">
<input 
type="checkbox" 
id="sp-x-${i}">
No clause (X)
</label>


<div id="sp-feedback-${i}" class="sp-feedback"></div>

</div>

`;

});

}



window.selectSPWord=function(qIndex,wIndex,element){

let existing=
spSelections[qIndex].findIndex(x=>x.index===wIndex);


if(existing>-1){

spSelections[qIndex].splice(existing,1);
element.classList.remove(
"sp-selected-subject",
"sp-selected-predicate"
);

}

else{

spSelections[qIndex].push({
index:wIndex,
word:element.innerText
});

element.classList.add("sp-selected-subject");

}

}



window.checkSPQuiz=function(){

let score=0;


spQuestions.forEach((q,i)=>{

let feedback=document.getElementById(`sp-feedback-${i}`);

let selected=
spSelections[i].map(x=>x.word);


let noClause=
document.getElementById(`sp-x-${i}`).checked;


let correctSubjects=
q.subjects.every(x=>selected.includes(x));

let correctPredicates=
q.predicates.every(x=>selected.includes(x));


let correctX=
q.noclause ? noClause : !noClause;


if(correctSubjects && correctPredicates && correctX){

score++;

feedback.className="sp-feedback sp-correct";
feedback.innerHTML="✓ Correct.";

}

else{

feedback.className="sp-feedback sp-incorrect";

let answer="";

if(q.noclause){

answer="Correct answer: X (no clause).";

}

else{

answer=
`Subject(s): ${q.subjects.join(", ")} | 
Predicate(s): ${q.predicates.join(", ")}`;

}

feedback.innerHTML=answer;

}


});


document.getElementById("sp-score").innerHTML=
`Score: ${score} / ${spQuestions.length}`;

}



window.resetSPQuiz=function(){

buildSPQuiz();

document.getElementById("sp-score").innerHTML="";

}



buildSPQuiz();


})();

</script>

</div>

<!-- Subject predicate END -->
