let tg = window.Telegram.WebApp

tg.BackButton.show()

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = "https://61e5-217-25-86-62.ngrok-free.app/src/templates/";
};


// Popup, written by ChatGPT 
document.addEventListener('DOMContentLoaded', function() {
    const openPopupButton = document.getElementById('open-popup');
    const closePopupButton = document.getElementById('close-popup');
    const overlay = document.getElementById('overlay');
    const popup = document.getElementById('popup');

    openPopupButton.addEventListener('click', function() {
        overlay.classList.add('active');
        popup.classList.add('active');
    });

    function closePopup() {
        overlay.classList.remove('active');
        popup.classList.remove('active');
    }

    overlay.addEventListener('click', closePopup);
    closePopupButton.addEventListener('click', closePopup);
});
