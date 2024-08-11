let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

tg.BackButton.show()

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = "index.html";
};

document.getElementById("tasks-btn").onclick = function() {
    window.location.href = "tasks.html"
};