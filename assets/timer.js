function startTimer(element, start_time) {
    if (element.getAttribute("data-used") == "true") {
        // avoid running the timer multiple times
        return;
    } else {
        element.setAttribute("data-used", "true");
    }
    time = start_time;
    background = element.parentNode;
    bg_final_size = 3;
    fill_scale = background.parentNode.offsetWidth / element.offsetWidth;
    ticking_transition = "all 0.8s cubic-bezier(.2, 15, 0, .61)";
    end_transition = "all 5s cubic-bezier(.45,.05,.55,.95)";
    timer = setInterval(function () {
        if (time > 0) {
            element.innerText = `${Math.floor(time / 60)}:${(time % 60).toString().padStart(2, '0')}`;
            scale = 1 + (bg_final_size - 1) * (1 - time / start_time);
            background.style.transform = "scale(" + scale + ")";
            element.style.transform = "scale(" + 1 / scale + ")";
            time--;
        } else {
            clearInterval(timer);
            element.innerText = "BREAK";
            scale = fill_scale;
            background.style.transition = end_transition;
            element.style.transition = end_transition;
            background.style.transform = "scale(" + scale + ")";
            background.style.borderRadius = 0;
            element.style.transform = "scale(" + 1 / scale + ")";
        }
    }, 1000);

    return timer;
}