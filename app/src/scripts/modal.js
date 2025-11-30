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
    const chatContainer = document.getElementById("chatContainer");
    const message = input.value.trim();
    if (!message) return;

    // Add user's message to chat
    appendMessage("you", message);
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
                message: message,
                player_name: playerName
            })
        });

        const data = await response.json();

        console.log(data)

        // Add agent response to chat
        appendMessage("agent", data.content);
    } catch (err) {
        appendMessage("agent", "Error contacting server.");
        console.error(err);
    }
}

function appendMessage(sender, text) {
    const chatContainer = document.getElementById("chatContainer");
    const p = document.createElement("p");
    p.textContent = `${sender}: ${text}`;
    chatContainer.appendChild(p);

    // Auto-scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
