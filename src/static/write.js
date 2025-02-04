const toInputEl = document.querySelector("input.to");
const fromInputEl = document.querySelector("input.from");
const textInputEl = document.querySelector("textarea");
const sendBtnEl = document.querySelector("button.send");

sendBtnEl.addEventListener("click", () => {
    if (!textInputEl.value) {
        alert("Write a love letter...");

        return
    }

    let data = {
        "to": toInputEl.value,
        "from": fromInputEl.value,
        "text": textInputEl.value
    }

    console.log(data);

    let url = "/letters"
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success:", data);

        // REDIRECT TO ESSAY PAGE
    })
    .catch(error => {
        console.error("Error:", error);
    });

    toInputEl.value = ""
    fromInputEl.value = ""
    textInputEl.value = ""
})