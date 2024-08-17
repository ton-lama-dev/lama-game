let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

tg.BackButton.show();

tg.onEvent('backButtonClicked', backCallback)
function backCallback() {
    window.location.href = `https://b042-217-25-86-16.ngrok-free.app/main?user_id=${user_tg_id}`;
};

document.getElementById("daily-btn").onclick = function() {
    window.location.href = "https://b042-217-25-86-16.ngrok-free.app/daily?user_id=${user_tg_id}";
};


document.addEventListener("DOMContentLoaded", function() {
    const taskLinks = document.querySelectorAll('.item-link');

    taskLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            const goImg = this.querySelector('.go');
            goImg.src = '../static/img/loading.gif';
            goImg.classList.add('loading');

            task_id = Number(this.querySelector('.item').id)
            const url = 'https://b042-217-25-86-16.ngrok-free.app/check_subscription';
            const requestData = {
                user_id: user_tg_id,
                task_id: task_id,
            };

            let response = fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
    
            // Check if the response is OK (status code 200-299)
            if (response.ok) {
                goImg.src = '../static/img/completed.png';
            } else {
                // Handle the case where the response status is not OK
                console.error('Server responded with status:', response.status);
            }
            // setTimeout(() => {
            //     goImg.src = '../static/img/completed.png';
            // }, 4000);
        });
    });
});

