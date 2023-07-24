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
const CARD_SWITCH_RANGE = '130%';

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

setCardOffset();
function setCardOffset() {
  CARD_ARRAY.forEach(function (item, index) {
    item.style.zIndex = Math.abs(index - COUNT_OF_CARDS);
    item.style.transform = `translate(${offsetArray[index]}px, ${offsetArray[index]}px)`;
  });
}

/******************************************************************/
window.addEventListener('keydown', function (e) { cardSwitching(e); });

function cardSwitching(e) {
  let animationObject = {}, previousSibling, scrolling = '';

  /* Return when you scroll during the animation of a card */
  if (isMoving) return;

  if ((e.keyCode !== 38 && e.keyCode !== 40) && (e.keyCode !== undefined)) return;

  for (let index of CARD_ARRAY) {
    if ((parseInt(window.getComputedStyle(index).zIndex) === CARD_ARRAY.length) || (parseInt(index.style.zIndex) === CARD_ARRAY.length)) {

      /* Switch the rearmost card */
      if (e.deltaY < 0 || e.keyCode === 38) { //deltaY < 0 -> scrolling up
        previousSibling = index.previousElementSibling;
        if (previousSibling === null) previousSibling = last_element;
      }

      animationObject = e.deltaY < 0 || e.keyCode === 38 ? previousSibling : e.deltaY > 0 || e.keyCode === 40 ? index : '';
      animationObject.style.transform = `translate(0px, -${CARD_SWITCH_RANGE})`;
      scrolling = e.deltaY < 0 || e.keyCode === 38 ? 'up' : e.deltaY > 0 || e.keyCode === 40 ? 'down' : '';
      isMoving = true;
      break; // Break the loop after the first match
    }
  }

  if (animationObject !== undefined) {
    // Create a promise that resolves when the transitionend event occurs
    const transitionEndPromise = new Promise((resolve) => {
      animationObject.addEventListener('transitionend', () => {
        resolve();
      }, { once: true });
    });

    // Handle the actions after the animation is complete
    transitionEndPromise.then(() => {
      if (scrolling === 'down') {
        animationObject.style.zIndex = 0;
        animationObject.style.transform = `translate(${offsetArray[COUNT_OF_CARDS]}px, ${offsetArray[COUNT_OF_CARDS]}px)`;
        offsetSwitch(scrolling);
      } else if (scrolling === 'up') {
        offsetSwitch(scrolling);
        animationObject.style.zIndex = COUNT_OF_CARDS;
        animationObject.style.transform = `translate(0px, 0px)`;
      }
      scrolling = '';
      isMoving = false; // Reset the isMoving flag after the animation is complete
    });
  }
}

function offsetSwitch(scrolling) {
  for (let index of CARD_ARRAY) {
    index.style.zIndex = scrolling === 'down' ? parseInt(index.style.zIndex) + 1 : parseInt(index.style.zIndex) - 1;
    let offsetIndex = Math.abs(parseInt(index.style.zIndex) - COUNT_OF_CARDS);
    index.style.transform = `translate(${offsetArray[offsetIndex]}px, ${offsetArray[offsetIndex]}px)`;
  }
}

function getRandomColor() {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
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