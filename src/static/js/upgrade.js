let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

const homeUrl = "https://fb92-217-25-86-81.ngrok-free.app/"

let $tapUpgradeButton = document.getElementById("tap-upgrade-btn");
let $energyUpgradeButton = document.getElementById("energy-upgrade-btn");
let $refillUpgradeButton = document.getElementById("refill-upgrade-btn");

tg.BackButton.show()

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = homeUrl + `main?user_id=${user_tg_id}`;
};

function wait(ms){
    var start = new Date().getTime();
    var end = start;
    while(end < start + ms) {
      end = new Date().getTime();
   }
};

$tapUpgradeButton.addEventListener("click", () => {
    const data = {
        "user_id": user_tg_id,
    };
    fetch(homeUrl + `upgrade_tap`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    wait(500);
    window.location.reload();
});
$energyUpgradeButton.addEventListener("click", () => {
    const data = {
        "user_id": user_tg_id,
    };
    fetch(homeUrl + `upgrade_energy`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    wait(500);
    window.location.reload();
});
$refillUpgradeButton.addEventListener("click", () => {
    const data = {
        "user_id": user_tg_id,
    };
    fetch(homeUrl + `upgrade_refill`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    wait(500);
    window.location.reload();
});


// Popup
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
