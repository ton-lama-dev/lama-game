let tg = window.Telegram.WebApp

tg.BackButton.show()

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = "index.html";
};

document.getElementById("daily-btn").onclick = function() {
    window.location.href = "daily.html"
};