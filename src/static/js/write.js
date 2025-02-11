const recipientsToInputEl = document.querySelector("input.to");
const recipientsFromInputEl = document.querySelector("input.from");
const letterInputEl = document.querySelector(".letter textarea");
const sendButtonEl = document.querySelector("button.send");

sendButtonEl.addEventListener("click", () => {
    if (!letterInputEl.value) {
        alert("Write a love letter...");

        return
    }

    let data = {
        "to": recipientsToInputEl.value,
        "from": recipientsFromInputEl.value,
        "text": letterInputEl.value
    }

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
        // Maybe some kind of fake loading screen?

        console.log(data);

        sessionStorage.setItem("source", "write");

        window.location.href = `/${data.id}`;
    })
    .catch(error => {
        console.error("Error:", error);

        alert("Unexpected error occured. Please try again.");
        return
    });

    recipientsToInputEl.value = ""
    recipientsFromInputEl.value = ""
    letterInputEl.value = ""
})