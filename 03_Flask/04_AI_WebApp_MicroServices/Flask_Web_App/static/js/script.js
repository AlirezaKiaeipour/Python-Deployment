function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function start_progress(){
    var mind_progress = document.getElementById("mind-progress-bar");
    var mind_progress_style = document.getElementById("mind-progress-bar-style");
    for(var i=0; i<100; i++){
        mind_progress.setAttribute("aria-valuenow", i);
        mind_progress_style.setAttribute("style", "width: " + i + "%")
        sleep(1000)
    }
}

const btn = document.getElementById("btn-mind");
btn.addEventListener("click", start_progress);