let tg = window.Telegram.WebApp

tg.BackButton.show()

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = "https://0d9f-31-40-140-89.ngrok-free.app/src/templates/";
};