let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

const homeUrl = "https://fb92-217-25-86-81.ngrok-free.app"
const currentUrl = window.location.href;

window.location.href = `${homeUrl}/swap?user_id=${user_tg_id}`;
