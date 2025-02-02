const letterEl = document.querySelector(".letter-container");
const fontSelectEl = document.querySelector(".font-select");

fontSelectEl.addEventListener("click", () => {
    toggleFont();
});

function toggleFont() {
    letterEl.classList.toggle("cursive");
}