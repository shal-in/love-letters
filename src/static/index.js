console.log("index.js");

const gifContainerEl = document.querySelector(".gif-container");

gifContainerEl.addEventListener("click", () => {
    const imgEl = gifContainerEl.querySelector("img");
    const gifSrc = imgEl.getAttribute("data-gif");
    const imgSrc = imgEl.getAttribute("src");
    const gifDuration = parseInt(imgEl.getAttribute("data-duration"));

    if (imgEl.src !== gifSrc) {
        imgEl.src = gifSrc;

        setTimeout(() => {
            imgEl.src = imgSrc;
            window.location.href = "/read"
        }, gifDuration);
    }
})