// let tg = window.Telegram.WebApp;
// let user_tg_id = tg.initDataUnsafe.user.id;
let user_tg_id = 6257396100;

const homeUrl = "https://c5f1-217-25-86-16.ngrok-free.app/"

// tg.BackButton.show();

// tg.onEvent('backButtonClicked', backCallback);
// function backCallback() {
//     window.location.href = homeUrl + `main?user_id=${user_tg_id}`;
// }

document.getElementById("daily-btn").onclick = function() {
    window.location.href = homeUrl + `daily?user_id=${user_tg_id}`;
};

document.addEventListener("DOMContentLoaded", function() {
    const items = document.querySelectorAll('.item.active');

    items.forEach(item => {
        item.addEventListener('click', function(event) {
            // event.preventDefault();

            if (item.classList.contains("done")) {
                return;
            }; 

            const goImg = this.querySelector('.go');
            goImg.classList.add("loading")
            goImg.src = '../static/img/loading.gif';

            let task_id = Number(this.id);
            const url = homeUrl + 'check_subscription';
            const requestData = {
                user_id: user_tg_id,
                task_id: task_id,
            };
            const requestParams = {
                headers: {
                  "content-type": "application/json; charset=UTF-8",
                },
                body: JSON.stringify(requestData),
                method: "POST",
            };

            function check() {
                fetch(url, requestParams)
                .then(response => {
                    if (response.status === 200) {
                        goImg.src = '../static/img/done.png';
                        item.classList.remove("active");
                        item.classList.add("done");
                    } else {
                        setTimeout(check, 5000);
                    }
                });
            };

            check();
        });
    });
});

