function countdownText(time) {
    if (time > 0) 
        return `${Math.floor(time / 60)}:${(time % 60).toString().padStart(2, '0')}`;
    else
        return "BREAK";
}

function startTimer(element, start_time) {
    time = start_time;
    timer = setInterval(function () {
        if (time > 0) {
            time--;
            text=countdownText(time);
            element.innerText=text;
        } else {
            clearInterval(timer);
        }
    }, 1000);
}