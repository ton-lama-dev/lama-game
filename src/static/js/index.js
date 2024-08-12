let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

const currentUrl = window.location.href;

// getting startapp num (referrer id)
const url = new URL(currentUrl);
const searchParams = new URLSearchParams(url.search);
const startAppNumber = searchParams.get('tgWebAppStartParam');

const userName = tg.initDataUnsafe.user.first_name;


window.location.href = `https://5994-217-25-86-44.ngrok-free.app/main?user_id=${user_tg_id}&referrer_id=${startAppNumber}&name=${userName}`;
