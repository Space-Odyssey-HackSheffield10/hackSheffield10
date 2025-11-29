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

let timeoutHandle

function timer(minutes, seconds){
    function tick(){
        let counter = document.getElementById("timer");
        counter.innerHTML = minutes.toString() + ":" + (seconds < 10 ? "0" : "") + String(seconds);
        seconds --;
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
    tick();
}