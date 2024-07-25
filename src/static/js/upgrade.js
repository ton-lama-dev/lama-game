window.Telegram.WebApp.BackButton.show()

window.Telegram.WebApp.onEvent('backButtonClicked', backCallback)

function backCallback() {
    window.location.href = "https://d5a4-217-25-86-110.ngrok-free.app/src/templates/";
};