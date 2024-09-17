// script.js 

let currentFlashcardIndex = 0;
const flashcards = document.querySelectorAll('.card-design');
const totalFlashcards = flashcards.length;

const prevButton = document.getElementById('prev-button');
const nextButton = document.getElementById('next-button');
const flashcardCount = document.getElementById('flashcard-count');

// Show the first flashcard by default
flashcards[currentFlashcardIndex].classList.add('active');
updateFlashcardCount();

// Attach click event listener to flip card on click
flashcards.forEach(flashcard => {
  flashcard.addEventListener('click', () => {
    flashcard.classList.toggle('flipped');
  });
});

// Function to navigate to the previous flashcard
function prevFlashcard() {
  flashcards[currentFlashcardIndex].classList.remove('active');
  currentFlashcardIndex = (currentFlashcardIndex - 1 + totalFlashcards) % totalFlashcards;
  flashcards[currentFlashcardIndex].classList.add('active');
  updateFlashcardCount();
}

// Function to navigate to the next flashcard
function nextFlashcard() {
  flashcards[currentFlashcardIndex].classList.remove('active');
  currentFlashcardIndex = (currentFlashcardIndex + 1) % totalFlashcards;
  flashcards[currentFlashcardIndex].classList.add('active');
  updateFlashcardCount();
}

// to update the flashcard count display
function updateFlashcardCount() {
  flashcardCount.textContent = `${currentFlashcardIndex + 1} / ${totalFlashcards}`;
}

// Handle keyboard navigation for flashcards
function handleKeyboardEvent(event) {
  if (event.key === "ArrowRight" || event.key === "ArrowUp") {
    console.log("Arrow Next Cliked")
    nextFlashcard();
  } else if (event.key === "ArrowLeft" || event.key === "ArrowDown") {
    console.log("Arrow PREV Cliked")
    prevFlashcard();
  }
}

// Attach event listeners
document.addEventListener('keydown', handleKeyboardEvent);
prevButton.addEventListener('click', prevFlashcard);
nextButton.addEventListener('click', nextFlashcard);

// Setup favorite button functionality
function setupFavoriteButtons() {
  const favoriteButtons = document.querySelectorAll('.favorite-button');

  favoriteButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      e.stopPropagation();  // Prevent the card flip on favorite button click
      button.classList.toggle('favorited');
    });
  });
}
setupFavoriteButtons();


document.querySelector('.close-button').addEventListener('click', function() {
  document.querySelector('.instructions-card').style.display = 'none';
});


function deleteFlashcardSet(flashcardSetName) {
  var deleteConfirmation = confirm("Are you sure you want to delete this flashcard set?");
  if (deleteConfirmation) {
    fetch(`/delete_flashcard_set/${flashcardSetName}`, {
      method: 'DELETE'
    })
    .then(response => {
      if (response.ok) {
        window.location.reload();
      } else {
        alert('Failed to delete the flashcard set. Please try again later.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred. Please try again later.');
    });
  }
}


function toggleAppendName() {
  var appendOption = document.getElementById("append_option");
  var appendNameLabel = document.getElementById("append_name_label");
  var appendNameContainer = document.getElementById("append_name_container");

  if (appendOption.value === "yes") {
    appendNameContainer.style.display = "block"; // Show the container
  } else {
    appendNameContainer.style.display = "none"; // Hide the container
  }
}

function showGeneratingMessage() {
  var generatingMessage = document.getElementById("generating-message");
  var submitButton = document.querySelector(".create-flashcard-button");
  var errorMessage = document.getElementById("error-message"); 

  generatingMessage.style.display = "block";
  submitButton.style.display = "none";
  errorMessage.style.display = "none";

  // Return true to allow form submission
  return true;
}

document.getElementById('menu-toggle').addEventListener('click', function() {
  document.getElementById('dropdown-menu').classList.toggle('show');
});
