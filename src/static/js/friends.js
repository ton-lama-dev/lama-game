let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

const homeUrl = "https://fb92-217-25-86-81.ngrok-free.app/"

tg.BackButton.show()

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = homeUrl + `main?user_id=${user_tg_id}`;
};

document.addEventListener('DOMContentLoaded', function() {
    const $refLink = document.getElementById("ref-link");
    $refLink.innerText = `https://t.me/lama_airdrop_bot/game?startapp=${user_tg_id}`


    const $copyBtn = document.getElementById("copy-btn");
    $copyBtn.addEventListener('click', function() {
        navigator.clipboard.writeText($refLink.innerText);
        closeTapPopup();
    });


    const $inviteBtn = document.getElementById('invite-btn');
    const $popup = document.getElementById('popup');
    const $overlay = document.getElementById('overlay');

    $inviteBtn.addEventListener('click', function() {
        $overlay.classList.add('active');
        $popup.classList.add('active');
    });

    function closeTapPopup() {
        $overlay.classList.remove('active');
        $popup.classList.remove('active');
    };

    $overlay.addEventListener('click', closeTapPopup);
});
