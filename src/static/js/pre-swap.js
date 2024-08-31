let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

const homeUrl = "https://playlama.fun/"
const currentUrl = window.location.href;

window.location.href = `${homeUrl}/swap?user_id=${user_tg_id}`;
