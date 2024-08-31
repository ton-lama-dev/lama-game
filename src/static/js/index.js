let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

const homeUrl = "https://playlama.fun/"

const currentUrl = window.location.href;

// getting startapp num (referrer id)
const url = new URL(currentUrl);
const searchParams = new URLSearchParams(url.search);
const startAppNumber = searchParams.get('tgWebAppStartParam');

const userName = tg.initDataUnsafe.user.first_name;

if (startAppNumber === "swap"){
    window.location.href = `${homeUrl}/swap?user_id=${user_tg_id}`;
} else {
    window.location.href = `${homeUrl}/main?user_id=${user_tg_id}&referrer_id=${startAppNumber}&name=${userName}`;
}

