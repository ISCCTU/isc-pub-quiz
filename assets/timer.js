document.addEventListener("DOMContentLoaded", function () {
    let timer;
    let time = 60; // 60 seconds = 1 minute

    function updateCountdown() {
        const countdown = document.querySelectorAll(".countdown");
        for (let i = 0; i < countdown.length; i++) {
            if (time > 0) {
                countdown[i].innerText = `${Math.floor(time / 60)}:${(time % 60).toString().padStart(2, '0')}`
            } else {
                countdown[i].innerText = 'BREAK'
            }
        }
    }

    function startTimer() {
        if (timer) clearInterval(timer);
        timer = setInterval(function () {
            if (time > 0) {
                time--;
                updateCountdown();
            } else {
                clearInterval(timer);
            }
        }, 1000);
    }

    function resetTimer() {
        time = 60;
        updateCountdown();
        clearInterval(timer);
    }

    function startOrRestartTimerOnKeyPress(e) {
        if (e.key === " " || e.key === "ArrowRight") {
            resetTimer();
            startTimer();
        }
    }

    document.addEventListener("keydown", (e) => {
        startOrRestartTimerOnKeyPress(e)
    });
    document.getElementById("startButton").addEventListener("click", startTimer);
    document.getElementById("resetButton").addEventListener("click", resetTimer);
});