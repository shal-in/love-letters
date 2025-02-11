// Click (to navigate to next page)
clickEl.addEventListener("click", () => {
    clickFunction();
});

setTimeout(() => {
    clickEl.querySelector(".open").classList.add("active");
}, 500)

clickEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        clickFunction();
    }
});

function clickFunction() {
    sessionStorage.setItem("source", "index");

    window.location.href = "/read";
}