console.log("universal.js");

const readButtonEl = document.querySelector(".header-read");
if (readButtonEl) {
        readButtonEl.addEventListener("click", () => {
        sessionStorage.setItem("source", "index");
    })
}