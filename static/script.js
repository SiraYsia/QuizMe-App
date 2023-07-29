function validateForm() {
  var password = document.getElementById("password").value;
  var confPassword = document.getElementById("conf_password").value;

  if (password !== confPassword) {
    alert("Passwords do not match. Please re-enter your password.");
    return false;
  }

  return true;
}


/* Set your own values */
const CARD_PEN_OFFSET = 10; // Displacement of the cards
const CARD_SWITCH_RANGE = '70%';

const CARD_ARRAY = [...document.querySelectorAll('.card-design')];
/* Do not change this */
const COUNT_OF_CARDS = CARD_ARRAY.length;
let last_element = CARD_ARRAY[CARD_ARRAY.length - 1];
let isMoving = false;

let offsetArray = [],
  offset = 0,
  l = CARD_ARRAY.length;
for (let i = 1; i <= l; i++) {
  offsetArray.push(offset);
  offset += CARD_PEN_OFFSET;
}

function setCardOffset() {
  CARD_ARRAY.forEach(function (item, index) {
    const distance = Math.abs(currentFlashcardIndex - index);
    const offsetValue = distance <= 1 ? offsetArray[distance] : CARD_SWITCH_RANGE;
    item.style.zIndex = Math.abs(index - COUNT_OF_CARDS);
    item.style.transform = `translate(${offsetValue}px, ${offsetValue}px)`;
  });
}


/******************************************************************/



function getRandomColor() {
  const minColorValue = 50; // Minimum value for each RGB component
  const maxColorValue = 205; // Maximum value for each RGB component
  let color = '#';
  const components = ['R', 'G', 'B'];

  // Ensure at least one component is close to 0 or 255
  let index = Math.floor(Math.random() * components.length);
  for (let i = 0; i < 3; i++) {
    const componentValue =
      i === index
        ? Math.floor(Math.random() * (maxColorValue - minColorValue + 1))
        : Math.floor(Math.random() * (maxColorValue - minColorValue + 1) + minColorValue);

    const colorHex = componentValue.toString(16).padStart(2, '0');
    color += colorHex;
  }
  return color;
}

const cardArray = [...document.querySelectorAll('.card-design')];
cardArray.forEach(card => {
  const randomColor = getRandomColor();
  card.style.backgroundColor = randomColor;
});



function setupFavoriteButtons() {
  const favoriteButtons = document.querySelectorAll('.favorite-button');

  favoriteButtons.forEach(button => {
    button.addEventListener('click', () => {
      button.classList.toggle('favorited');
    });
  });
}
setupFavoriteButtons();
// Add these variables to keep track of the current flashcard index
// Add these variables to keep track of the current flashcard index and the total number of flashcards
let currentFlashcardIndex = 0;
const flashcards = document.querySelectorAll('.card-design');
const totalFlashcards = flashcards.length;

// Show the first flashcard by default
flashcards[currentFlashcardIndex].classList.add('active');

// Attach click event listener to the "Previous" button
const prevButton = document.querySelector('.prev-button');
prevButton.addEventListener('click', prevFlashcard);

// Attach click event listener to the "Next" button
const nextButton = document.querySelector('.next-button');
nextButton.addEventListener('click', nextFlashcard);

// Function to navigate to the previous flashcard
function prevFlashcard() {
  // Hide the current flashcard
  flashcards[currentFlashcardIndex].classList.remove('active');

  // Move to the previous flashcard index
  currentFlashcardIndex--;

  // Check if we have reached the first flashcard, then reset to the last flashcard
  if (currentFlashcardIndex < 0) {
    currentFlashcardIndex = totalFlashcards - 1;
  }

  // Show the previous flashcard
  flashcards[currentFlashcardIndex].classList.add('active');
}

// Function to navigate to the next flashcard
function nextFlashcard() {
  // Hide the current flashcard
  flashcards[currentFlashcardIndex].classList.remove('active');

  // Move to the next flashcard index
  currentFlashcardIndex++;

  // Check if we have reached the last flashcard, then reset to the first flashcard
  if (currentFlashcardIndex >= totalFlashcards) {
    currentFlashcardIndex = 0;
    document.querySelector('.end-section').style.display = 'block';
    return;
  }
  

  // Show the next flashcard
  flashcards[currentFlashcardIndex].classList.add('active');
}
function handleKeyboardEvent(event) {
  if (event.key === "ArrowRight" || event.key === "ArrowUp") {
    nextFlashcard();
  } else if (event.key === "ArrowLeft" || event.key === "ArrowDown") {
    prevFlashcard();
  }
}

// Attach event listener for "keydown" event on the document object
document.addEventListener('keydown', handleKeyboardEvent);

function startOver() {
  currentFlashcardIndex = 0;
  showFlashcards();
}

function showFlashcards() {
  // Hide the "End" section
  const endSection = document.querySelector('.end-section');
  endSection.style.display = 'none';

  // Show the current flashcard
  flashcards[currentFlashcardIndex].classList.add('active');
}