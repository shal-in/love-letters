const toInputEl = document.querySelector(".write input");

const prefix = "To: ";

// Set initial value and ensure "To" is the first thing visible
toInputEl.value = prefix;

toInputEl.addEventListener("input", (e) => {
    const inputtedChar = e.data;

    // If a character is typed
    if (inputtedChar) {
        // If the input field is empty or just "To", add the typed character
        if (toInputEl.value === "" || toInputEl.value === prefix) {
            toInputEl.value = prefix + inputtedChar;
        }
    }
});

toInputEl.addEventListener("keydown", (e) => {
    // Prevent deletion of "To"
    if ((e.key === "Backspace" || e.key === "Delete") && toInputEl.selectionStart <= prefix.length) {
        e.preventDefault(); // Stop the deletion
    }
});

toInputEl.addEventListener("blur", () => {
    // When the input loses focus, if it's empty, set it back to "To"
    if (toInputEl.value === "") {
        toInputEl.value = prefix;
    }
});
