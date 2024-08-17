let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

tg.BackButton.show()

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = `https://5994-217-25-86-44.ngrok-free.app/main?user_id=${user_tg_id}`;
};

document.getElementById("tasks-btn").onclick = function() {
    window.location.href = `https://b042-217-25-86-16.ngrok-free.app/tasks?user_id=${user_tg_id}`;
};