let tg = window.Telegram.WebApp

tg.BackButton.show()

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = "https://9e10-217-25-86-62.ngrok-free.app/src/templates/";
};

document.getElementById("tasks-btn").onclick = function() {
    window.location.href = "https://9e10-217-25-86-62.ngrok-free.app/src/templates/tasks.html"
};