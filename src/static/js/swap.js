let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

const homeUrl = "https://playlama.fun/"
const $claimBtn = document.getElementById("claim-btn");

function wait(ms){
    var start = new Date().getTime();
    var end = start;
    while(end < start + ms) {
      end = new Date().getTime();
   }
};

if ($claimBtn.classList.contains("active")) {
    $claimBtn.addEventListener("click", () => {
        const data = {
            "user_id": user_tg_id,
        };
        fetch(homeUrl + `reward`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        wait(500);
        window.location.reload();
    });
};
