let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

tg.BackButton.show();

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = `https://5994-217-25-86-44.ngrok-free.app/main?user_id=${user_tg_id}`;
};

document.getElementById("daily-btn").onclick = function() {
    window.location.href = "https://5994-217-25-86-44.ngrok-free.app/daily?user_id=${user_tg_id}";
};