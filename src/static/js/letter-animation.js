const imgContainer = document.querySelector(".image-container");
const clickEl = document.querySelector(".click");

clickEl.addEventListener("mouseover", () => {
    imgContainer.classList.toggle("hover");
})

clickEl.addEventListener("mouseout", () => {
    imgContainer.classList.toggle("hover");
})

clickEl.addEventListener("focus", () => {
    imgContainer.classList.toggle("hover");
})

clickEl.addEventListener("blur", () => {
    imgContainer.classList.toggle("hover");
})

