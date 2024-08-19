// let tg = window.Telegram.WebApp;
// let user_tg_id = tg.initDataUnsafe.user.id;
let user_tg_id = 6257396100;

// tg.BackButton.show();

// tg.onEvent('backButtonClicked', backCallback);
// function backCallback() {
//     window.location.href = `https://b042-217-25-86-16.ngrok-free.app/main?user_id=${user_tg_id}`;
// }

document.getElementById("daily-btn").onclick = function() {
    window.location.href = `https://b042-217-25-86-16.ngrok-free.app/daily?user_id=${user_tg_id}`;
};

document.addEventListener("DOMContentLoaded", function() {
    const taskLinks = document.querySelectorAll('.item-link');

    taskLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            const goImg = this.querySelector('.go');
            goImg.src = '../static/img/loading.gif';

            let task_id = Number(this.querySelector('.item').id);
            const url = 'https://b042-217-25-86-16.ngrok-free.app/check_subscription';
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
                        goImg.src = '../static/img/completed.png';
                    } else {
                        function repeat() {
                            setTimeout(check, 4000);
                        };
                        repeat();
                    }
                });
            };

            check();
        });
    });
});

