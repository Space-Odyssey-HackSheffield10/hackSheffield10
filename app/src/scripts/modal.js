function openModal(modalName) {
    const modal = document.getElementById(modalName);
    modal.style.display = 'flex';
    // Trigger reflow to ensure transition works
    modal.offsetHeight;
    modal.style.transform = 'translateX(100%)';

    const conversation_id = localStorage.getItem("conversation_id");
    if (conversation_id) {
        startEventStream(conversation_id);
    }
}

function closeModal(modalName) {
    const modal = document.getElementById(modalName);
    modal.style.display = 'none';
}

function startEventStream(conversation_id) {
    const evtSource = new EventSource(`/events/${conversation_id}`);

    evtSource.onmessage = (event) => {
        const data = JSON.parse(event.data);

        let colour = "white";
        if (data.agent_name === "scottie") colour = "blue";
        else if (data.agent_name === "cowboy") colour = "red";
        else if (data.agent_name === "siren") colour = "gold";
        else if (data.agent_name === "valentine") colour = "magenta";

        appendMessage(data.agent_name, data.text, colour);
    };
}


async function sendMessage() {
    const input = document.getElementById("chatMessage");
    const message = input.value.trim();
    const conversation_id = localStorage.getItem("conversation_id")
    const username = localStorage.getItem("username")
    if (!message) return;

    // Add user's message to chat
    appendMessage(username, message, "green");
    input.value = "";

    try {
        // Get player name from global scope
        const playerName = window.playerName || "anonymous";

        const response = await fetch("http://localhost:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify({
                message,
                conversation_id
            })
        });

        console.log("success")

    } catch (err) {
        appendMessage("agent", "Error contacting server.");
        console.error(err);
    }
}

function appendMessage(sender, text, colour) {
    const chatContainer = document.getElementById("chatContainer");
    const p = document.createElement("p");
    p.textContent = `${sender}: ${text}`;
    p.style.color = colour;
    chatContainer.appendChild(p);

    // Auto-scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
