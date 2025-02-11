console.log("Thank you for engaging with this project! 💌");

const readButtonEl = document.querySelector(".header-read");
if (readButtonEl) {
        readButtonEl.addEventListener("click", () => {
        sessionStorage.setItem("source", "index");
    })
}

const headerButtonEl = document.querySelector(".header-container .header");
headerButtonEl.addEventListener("click", () => {
    window.location.href = "/";
});