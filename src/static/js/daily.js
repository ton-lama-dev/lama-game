let tg = window.Telegram.WebApp

tg.BackButton.show()

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = "https://680b-217-25-86-62.ngrok-free.app/src/templates/";
};