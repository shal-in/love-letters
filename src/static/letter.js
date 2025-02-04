const letterEl = document.querySelector(".letter-container");
const letterId = getLetterIdFromURL();
if (!letterId) {
    window.location.href = "/"
}

// GET REQUEST
const requestURL = `/letters/read?letter_id=${letterId}`
fetch(requestURL)
.then(response => {
    if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
    }
    return response.json();
})
.then(data => {
    handleLetterData(data);
})
.catch(error => {
    window.location.href = "/"
});


const letterHeader = letterEl.querySelector(".letter-header");
function handleLetterData(data) {
    document.title = `#${data.id} | I wrote you a love letter` // Decide if you want the i wrote you... bit

    const letterHeaderId = letterHeader.querySelector(".letter-id");
    letterHeaderId.textContent = data.id;

    // Copy button stuff (Need an icon or tool tip for copied)

    const letterRecipients = letterEl.querySelector(".recipients");
    console.log(letterRecipients);
    if (data.raw.to) {
        letterRecipients.querySelector(".to").textContent = `To ${data.raw.to}`;
    } else if (!data.raw.to) {
        letterRecipients.querySelector(".to").textContent = `To Anonymous`;
    }

    if (data.raw.from) {
        letterRecipients.querySelector(".from").textContent = `, from ${data.raw.from}`;
    } else if(data.raw.from) {
        letterRecipients.querySelector(".from").textContent = `, from Anonymous`;
    }

    createLetterHTML(data.raw.text)
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

const letterTextEl = letterEl.querySelector(".letter")
function createLetterHTML(text) {
    // Split the letter content by line breaks
    if (!text) {
        console.error("Letter text is empty.");
        return;  // Exit if text is empty or undefined
    }

    let parags = text.split("\n"); // Split by newline
    parags.forEach(parag => {
        let p = document.createElement("p")

        p.textContent = parag;

        letterTextEl.appendChild(p);
    })
}