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
            e.stopPropagation(); // Prevent the card flip on favorite button click
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
        fetch(`/DeleteSet/${flashcardSetName}`, {
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



function updateSaveButton() {
    const flashcardRows = document.querySelectorAll('#flashcard-table tr:not(:first-child)');
    const saveButton = document.getElementById('save_fulashcards');
    saveButton.disabled = flashcardRows.length === 0;
}

/* Delete and edit flashcard On edit mode */

function deleteFlashcard(button) {
    // Remove the row from the table
    const row = button.closest('tr');
    row.remove();
    updateSaveButton()
}

function addFlashcard() {
    const table = document.getElementById('flashcard-table');
    const newRow = table.insertRow(-1);
    newRow.innerHTML = `
    <td><input type="text" required oninput="checkInput(this)" id="flashcard_input" name="question[]" placeholder="Enter question"></td>
    <td><input type="text" required oninput="checkInput(this)" id="flashcard_input" name="answer[]" placeholder="Enter answer"></td>
    <td><button type="button" class="delete-flashcard-button" onclick="deleteFlashcard(this)">Delete</button>
  `;
    updateSaveButton()
}

document.addEventListener('DOMContentLoaded', function() {
  const contentWrappers = document.querySelectorAll('.content-wrapper');
  
  contentWrappers.forEach(wrapper => {
    const content = wrapper.querySelector('p');
    const wrapperHeight = wrapper.clientHeight;
    const contentHeight = content.clientHeight;
    
    if (contentHeight > wrapperHeight) {
      wrapper.style.justifyContent = 'flex-end';
    } else {
      wrapper.style.justifyContent = 'center';
    }
  });
});

// Trim the input's value and check if it's still empty
function checkInput(input) {
    if (input.value.trim() === "") {
      input.setCustomValidity("This field cannot be empty or just spaces.");
    } else {
      input.setCustomValidity(""); 
    }
  }

// Share your flashcards 

  var modal = document.getElementById("shareModal");

  function openShareModal() {
      modal.style.display = "block";
  }

  function closeShareModal() {
      modal.style.display = "none";
  }



  // Close the modal if the user clicks outside of it
  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
      }
  }

function copyShareLink() {
    var shareLink = "{{ share_link }}";
    navigator.clipboard.writeText(shareLink).then(function() {
    alert("Share link copied to clipboard!");
    }, function(err) {
    console.error('Could not copy text: ', err);
    });
}
