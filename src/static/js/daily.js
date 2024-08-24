// let tg = window.Telegram.WebApp;
// let user_tg_id = tg.initDataUnsafe.user.id;

const homeUrl = "https://9113-217-25-86-16.ngrok-free.app/"

// tg.BackButton.show()

// tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = homeUrl + `main?user_id=${user_tg_id}`;
};

document.getElementById("tasks-btn").onclick = function() {
    window.location.href = homeUrl + `tasks?user_id=${user_tg_id}`;
};