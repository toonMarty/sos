/**
 * A script that generates random color bubbles for each submitted ticket
 */

const listItems = document.querySelectorAll(".ticket-bubble");

listItems.forEach(item => {
  const randomColor = generateRandomColor();
  item.style.backgroundColor = randomColor;
});

function generateRandomColor() {
  // generates random colors using the rgb color model
  const red = Math.floor(Math.random() * 256);
  const green = Math.floor(Math.random() * 256);
  const blue = Math.floor(Math.random() * 256);
  return `rgb(${red}, ${green}, ${blue})`;
}

