let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

tg.BackButton.show()

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = "index.html";
};


// Popup, written by ChatGPT 
document.addEventListener('DOMContentLoaded', function() {
    const openTapPopup = document.getElementById('tap-item');
    const openBatteryPopup = document.getElementById('battery-item');
    const openSpeedPopup = document.getElementById('speed-item');
    const overlay = document.getElementById('overlay');
    const tapPopup = document.getElementById('tap-popup');
    const batteryPopup = document.getElementById('battery-popup');
    const speedPopup = document.getElementById('speed-popup');

    openTapPopup.addEventListener('click', function() {
        overlay.classList.add('active');
        tapPopup.classList.add('active');
    });
    openBatteryPopup.addEventListener('click', function() {
        overlay.classList.add('active');
        batteryPopup.classList.add('active');
    });
    openSpeedPopup.addEventListener('click', function() {
        overlay.classList.add('active');
        speedPopup.classList.add('active');
    });

    function closeTapPopup() {
        overlay.classList.remove('active');
        tapPopup.classList.remove('active');
    }
    function closeBatteryPopup() {
        overlay.classList.remove('active');
        batteryPopup.classList.remove('active');
    }
    function closeSpeedPopup() {
        overlay.classList.remove('active');
        speedPopup.classList.remove('active');
    }

    overlay.addEventListener('click', closeTapPopup);
    overlay.addEventListener('click', closeBatteryPopup);
    overlay.addEventListener('click', closeSpeedPopup);
});
