function closeStartingScreen() {
    const startingScreen = document.getElementById('startingScreen');
    startingScreen.style.display = 'none';

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
