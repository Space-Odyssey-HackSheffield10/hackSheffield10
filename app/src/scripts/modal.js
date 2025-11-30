function openModal(modalName) {
    const modal = document.getElementById(modalName);
    modal.style.display = 'flex';
    // Trigger reflow to ensure transition works
    modal.offsetHeight;
    modal.style.transform = 'translateX(100%)';
}

function closeModal(modalName) {
    const modal = document.getElementById(modalName);
    modal.style.display = 'none';
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
        const response = await fetch("/chat", {
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

        const data = await response.json();

        console.log(data);

        agent_name = data.agent_name;
        colour = "white"
        if (agent_name === "scottie") {
            colour = "blue"
        } else if (agent_name === "cowboy") {
            colour = "red"
        } else if (agent_name === "siren") {
            colour = "gold"
        } else if (agent_name === "valentine") {
            colour = "magenta"
        }


        // Add agent response to chat
        appendMessage(agent_name, data.content, colour);
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
