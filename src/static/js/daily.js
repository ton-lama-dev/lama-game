let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

const homeUrl = "https://playlama.fun/"

const $claim_button = document.getElementById("claim-btn");

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
}

document.getElementById("tasks-btn").onclick = function() {
    window.location.href = homeUrl + `tasks?user_id=${user_tg_id}`;
};

$claim_button.onclick = function() {
    if ($claim_button.classList.contains("disabled")) {
        return;
    }

    let url = homeUrl + "claim";
    const requestData = {
        user_id: user_tg_id,
    };
    const requestParams = {
        headers: {
          "content-type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify(requestData),
        method: "POST",
    };
    fetch(url, requestParams);
    wait(500)
    window.location.reload();
};
