let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

const homeUrl = "https://playlama.fun/"

const $lama = document.getElementById("lama");
const $balance = document.getElementById("balance");
const $tasks = document.getElementById("tasks");
const $upgrade = document.getElementById("upgrade");
const $friends = document.getElementById("friends");
const $progressBar = document.getElementById("progress-bar");
const $progressText = document.getElementById("progress-text");
const $tap = document.getElementById("tap-power");

let availableEnergy = Number($progressText.textContent.split("/")[0]);
let maxEnergy = Number($progressText.textContent.split("/")[1]);
let tap_power = Number($tap.textContent);
let refillSpeed = 1;  // per second

tg.BackButton.show();

addEventListener("beforeunload", update);
var repetition = setInterval(update, 2000);
var last_balance = 0;
function update() {
  if (Number($balance.textContent) != last_balance) {
    const data = {
      "user_id": user_tg_id,
      "balance": $balance.textContent,
      "energy_available": availableEnergy,
    };
  
    fetch(homeUrl + 'update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    last_balance = Number($balance.innerHTML)};
};


function increaseBalance(num) {
  $balance.textContent = Number($balance.textContent) + num;

  availableEnergy -= num;
  newWidth = availableEnergy / maxEnergy * 100;
  $progressBar.style.width = `${newWidth}%`;

  $progressText.textContent = `${availableEnergy}/${maxEnergy}`;
};

function refillBar(speed) {
  if (maxEnergy - availableEnergy >= tap_power){
    availableEnergy += speed * 10; // because i call this function each 10s
  } else {
    availableEnergy += maxEnergy - availableEnergy;
  }

  newWidth = availableEnergy / maxEnergy * 100;
  $progressBar.style.width = `${newWidth}%`;

  $progressText.textContent = `${availableEnergy}/${maxEnergy}`;
};

function setBar() {
  newWidth = availableEnergy / maxEnergy * 100;
  $progressBar.style.width = `${newWidth}%`;
};

$lama.addEventListener("touchstart", (event) => {
  const rect = $lama.getBoundingClientRect();
  for (let i = 0; i < event.touches.length; i++) {
    if (tap_power <= availableEnergy) {
      const touch = event.touches[i];
      const offsetX = touch.clientX - rect.left - rect.width / 2;
      const offsetY = touch.clientY - rect.top - rect.height / 2;
      const DEG = 60;
      const tiltX = (offsetY / rect.height) * DEG;
      const tiltY = (offsetX / rect.width) * -DEG;

      $lama.style.setProperty("--tiltX", `${tiltX}deg`);
      $lama.style.setProperty("--tiltY", `${tiltY}deg`);

      setTimeout(() => {
        $lama.style.setProperty("--tiltX", `0deg`);
        $lama.style.setProperty("--tiltY", `0deg`);
      }, 100);

      const plusOne = document.createElement("div");
      plusOne.classList.add("plus-one");
      plusOne.textContent = `+${tap_power}`;
      plusOne.style.left = `${touch.clientX - rect.left + 30}px`;
      plusOne.style.top = `${touch.clientY - rect.top + 200}px`;
      $lama.parentElement.appendChild(plusOne);
      increaseBalance(tap_power);
      setTimeout(() => {
        plusOne.remove();
      }, 2000);
    } else {
      console.log("you're out of energy");
    }
  }
});

$tasks.addEventListener("click", function() {
  window.location.href = homeUrl + `tasks?user_id=${user_tg_id}`;
});

$upgrade.addEventListener("click", function() {
  window.location.href = homeUrl + `upgrade?user_id=${user_tg_id}`;
});

$friends.addEventListener("click", function() {
  window.location.href = homeUrl + `friends?user_id=${user_tg_id}`;
});


function refillProgressBar() {
  setInterval(() => {
      if ((availableEnergy < maxEnergy) && ((maxEnergy - availableEnergy) >= refillSpeed)) {
          refillBar(refillSpeed);
      }
  }, 10000);
};


setBar();
refillProgressBar();
