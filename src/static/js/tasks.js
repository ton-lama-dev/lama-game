let tg = window.Telegram.WebApp

tg.BackButton.show()

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = "https://61e5-217-25-86-62.ngrok-free.app/src/templates/";
};

document.getElementById("daily-btn").onclick = function() {
    window.location.href = "https://61e5-217-25-86-62.ngrok-free.app/src/templates/daily.html"
};