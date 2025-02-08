const letterEl = document.querySelector(".letter-container");
const letterHeader = letterEl.querySelector(".letter-header");
const letterId = getLetterIdFromURL();
if (!letterId) {
    window.location.href = "/"
}

const copyButtonEl = letterHeader.querySelector(".copy");
copyButtonEl.addEventListener("click", () => {
    const to = document.querySelector(".letter .recipients .to").textContent;
    copyButtonFunction(letterId, to);

    // TODO: ping a GET to `shares/<letter_id>` to create a share_log in the database

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
        setTimeout(() => notification.classList.add("hidden"), 300); // Hide after fade out
    }, 1500); // Display for 1.5 seconds
}






// HELPER FUNCTIONS
function getLetterIdFromURL() {
    // Get the path from the URL (e.g., "/12")
    const path = window.location.pathname; // "/12"
    
    // Extract the number from the path (remove the leading slash)
    const letterId = path.split("/")[1]; // "12"

    if (!letterId) {
        return null;
    } 

    return letterId;
}