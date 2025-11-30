const audio = document.getElementById('backgroundMusic');

async function closeStartingScreen() {
    const startingScreen = document.getElementById('startingScreen');
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
    audio.play().catch(error => {
        console.log('Audio autoplay prevented:', error);
    });

    
    timer(5, 0);
}

function pauseMusic(){
    audio.pause();
}



let timeoutHandle;
const outOfTimeModal = document.getElementById("outOfTimeModal");
const wonModal = document.getElementById("wonModal");

function timer(minutes, seconds){
    let outOfTime = false;
    function tick(){

        if (!won){
            let counter = document.getElementById("timer");

            console.log("won: ", won);
            counter.innerHTML = minutes.toString() + ":" + (seconds < 10 ? "0" : "") + String(seconds);
            seconds --;
            if (minutes == 0 && seconds == 0){
                outOfTime = true;
                setTimeout(function(){
                    showOutOfTimeModal();
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
        } else { // if game won show wonModal
            showWonModal();
            pauseMusic();
            const victoryMusic = document.getElementById("victoryMusic");
            victoryMusic.play();
            
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

function showWonModal(){
    wonModal.style.display = "flex";
    wonModal.classList.add("show");
    wonModal.classList.add("modal-content-center");
}