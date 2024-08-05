let tg = window.Telegram.WebApp

tg.BackButton.show()

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = "index.html";
};

document.getElementById("tasks-btn").onclick = function() {
    window.location.href = "tasks.html"
};