// Animation stuff
const contentWrapper = document.querySelector(".content-wrapper");
const videoEl = document.querySelector("video");
const sessionSource = sessionStorage.getItem("source");

const triggerAnimation = () => playAnimation();

function playAnimation() {
    videoEl.play();
    clickEl.classList.add("hidden");
    setTimeout(() => {
        showLetter();
    }, 2350);

    sessionStorage.setItem("source", "next");
}

function showLetter() {
    videoEl.currentTime = 2.3;
    clickEl.classList.add("hidden");
    
    ["top", "main", "bottom"].forEach(element => {
        contentWrapper.querySelector(`.${element}`).classList.add("fade-in");
    })
}

if (sessionSource === "write" || sessionSource === "next") {
    showLetter();
} else if (sessionSource === "index") {
    videoEl.currentTime = 0;
    playAnimation();
} else {
    videoEl.currentTime = 0;

    clickEl.addEventListener("click", triggerAnimation);
    clickEl.addEventListener("keydown", (e) => {
        if (e.key === "Enter") triggerAnimation();
    });
}

// Scroll down arrow
const mainEl = document.querySelector("#letter .main");
const arrowDown = document.querySelector("#letter .arrow-down");

function checkOverflow() {
    if (mainEl.scrollHeight > mainEl.clientHeight) {
        arrowDown.style.display = "block";
    } else {
        arrowDown.style.display = "none";
    }
}

checkOverflow();

mainEl.addEventListener("scroll", () => {
    if (mainEl.scrollTop + mainEl.clientHeight >= mainEl.scrollHeight) {
        arrowDown.style.display = "none";
    } else {
        arrowDown.style.display = "block";
    }
});

window.addEventListener('resize', checkOverflow);


// Copy to clipboard
const letterId = getLetterIdFromURL();
if (!letterId) {
    window.location.href = "/"
}

const copyButtonEl = document.querySelector(".top button.copy");
copyButtonEl.addEventListener("click", () => {
    const to = document.querySelector(".recipients .to span").textContent;
    copyButtonFunction(letterId, to);

    fetch(`/shares/${letterId}`, { method: 'GET' });
})

function copyButtonFunction(letterId, to) {
    message = `I wrote you a love letter💌.\n\niwroteyoualoveletter.com/${letterId}`;
    if (to && to !== "Anonymous") {
        message = `Dear ${to},\n` + message
    }

    copyToClipboard(message);
    copyButtonEl.blur();
}

function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text)
            .then(() => showCopyNotification())
            .catch(err => console.error("Clipboard API failed:", err));
    } else {
        copyToClipboardFallback(text);
    }
}

function showCopyNotification() {
    const notification = document.getElementById("copy-notification");
    notification.classList.remove("hidden");
    notification.classList.add("show");

    setTimeout(() => {
        notification.classList.remove("show");
        setTimeout(() => notification.classList.add("hidden"), 300);
    }, 1500);
}


function getLetterIdFromURL() {
    const path = window.location.pathname;
    
    const letterId = path.split("/")[1];

    if (!letterId) {
        return null;
    } 

    return letterId;
}

// Next button
const nextButtonEl = document.querySelector(".top .next");
nextButtonEl.addEventListener("click", () => {
    window.location.href = "/read";
})