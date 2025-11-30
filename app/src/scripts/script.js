async function closeStartingScreen() {
    const startingScreen = document.getElementById('startingScreen');
    const nameInput = document.querySelector('.starting-screen input');

    // Get player name from input
    playerName = nameInput.value.trim() || "anonymous";

    startingScreen.style.display = 'none';

    // add the user to database and save the conversation id
    const message = document.getElementById('Name').value.trim();

    try {
        const response = await fetch("/start_game", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        localStorage.setItem("conversation_id", data.conversation_id)
        localStorage.setItem("username", data.username)

        console.log(data.status)
    } catch (err) {
        console.error(err);
    }


    // Start playing background music
    const audio = document.getElementById('backgroundMusic');
    audio.play().catch(error => {
        console.log('Audio autoplay prevented:', error);
    });

    timer(2, 0);
}



let timeoutHandle;
const outOfTimeModal = document.getElementById("outOfTimeModal");

function timer(minutes, seconds){
    let outOfTime = false;
    function tick(){
        let counter = document.getElementById("timer");

        counter.innerHTML = minutes.toString() + ":" + (seconds < 10 ? "0" : "") + String(seconds);
        seconds --;
        if (minutes == 0 && seconds == 0){
            outOfTime = true;
            setTimeout(function(){
                showOutOfTimeModal();
                recordGameEnd(false); // Game failed due to timeout
            }, 2000);
        }

        if (seconds >= 0){
            timeoutHandle = setTimeout(tick, 1000);
        } else {
            if (minutes >= 1){
                setTimeout(function () {
                    timer(minutes - 1, 59);
                }, 1000);
            }
        }
    }

    if (!outOfTime){
        tick();
    }
}

function showOutOfTimeModal(){
    outOfTimeModal.style.display = "flex";
    outOfTimeModal.classList.add("show");
    outOfTimeModal.classList.add("modal-content-center");
}

function recordGameEnd(success) {
    if (!gameStartTime) return;
    
    const duration = (Date.now() - gameStartTime) / 1000; // Convert to seconds
    
    fetch("http://localhost:8000/game/end", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            player_name: playerName,
            duration: duration,
            success: success
        })
    }).catch(err => console.error("Failed to record game end:", err));
}

// Export playerName so other scripts can use it
window.playerName = playerName;
