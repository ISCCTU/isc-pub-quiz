function countdownText(time) {
    if (time > 0)
        return `${Math.floor(time / 60)}:${(time % 60).toString().padStart(2, '0')}`;
    else
        return "BREAK";
}
function startTimer(element, start_time) {
    time = start_time;
    background=element.parentNode;
    bg_final_size = 3;

    timer = setInterval(function () {
        if (time > 0) {
            time--;
            text = countdownText(time);
            element.innerText = text;
            scale=1+(bg_final_size-1)*(1 - time / start_time);
            background.style.transform="scale("+scale+")";
            element.style.transform="scale("+1/scale+")";
        } else {
            clearInterval(timer);
        }
    }, 1000);
    return timer;
}