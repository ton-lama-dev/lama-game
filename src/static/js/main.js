let tg = window.Telegram.WebApp;
let user_tg_id = tg.initDataUnsafe.user.id;

const $lama = document.getElementById("lama");
const $balance = document.getElementById("balance");
const $tasks = document.getElementById("tasks");
const $upgrade = document.getElementById("upgrade");
const $friends = document.getElementById("friends");
const $progressBar = document.getElementById("progress-bar");
const $progressText = document.getElementById("progress-text");

let availableEnergy = Number($progressText.textContent.split("/")[0]);
let maxEnergy = Number($progressText.textContent.split("/")[1]);
let tap = 1;
let refillSpeed = 1;  // per second

tg.BackButton.show();

addEventListener("beforeunload", updateBalance);
var repetition = setInterval(updateBalance, 2000);
var last_balance = 0
function updateBalance() {
  if (Number($balance.textContent) != last_balance) {
    const data = {
      "user_id": user_tg_id,
      "balance": $balance.textContent
    };
  
    fetch('https://d43a-217-25-86-44.ngrok-free.app/exit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    last_balance = Number($balance.innerHTML)};
}


function increaseBalance(num) {
  $balance.textContent = Number($balance.textContent) + num;

  availableEnergy -= num;
  newWidth = availableEnergy / maxEnergy * 100;
  $progressBar.style.width = `${newWidth}%`;

  $progressText.textContent = `${availableEnergy}/${maxEnergy}`;
}

function refillBar(speed) {
  availableEnergy += speed * 10; // because i call this function each 10s

  newWidth = availableEnergy / maxEnergy * 100;
  $progressBar.style.width = `${newWidth}%`;

  $progressText.textContent = `${availableEnergy}/${maxEnergy}`;
}

function setBar() {
  newWidth = availableEnergy / maxEnergy * 100;
  $progressBar.style.width = `${newWidth}%`;
}

$lama.addEventListener("touchstart", (event) => {
  const rect = $lama.getBoundingClientRect();
  for (let i = 0; i < event.touches.length; i++) {
    if (tap <= availableEnergy) {
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
      // plusOne.textContent = `+${tap}`; // temporarily commented for the alpha-version
      plusOne.textContent = `test`;
      plusOne.style.left = `${touch.clientX - rect.left + 30}px`;
      plusOne.style.top = `${touch.clientY - rect.top + 200}px`;
      $lama.parentElement.appendChild(plusOne);
      increaseBalance(tap);
      setTimeout(() => {
        plusOne.remove();
      }, 2000);
    } else {
      console.log("you're out of energy");
    }
  }
});

$tasks.addEventListener("click", function() {
  window.location.href = "http://127.0.0.1:5000/tasks";
});

$upgrade.addEventListener("click", function() {
  window.location.href = "http://127.0.0.1:5000/upgrade";
});

$friends.addEventListener("click", function() {
  window.location.href = "http://127.0.0.1:5000/friends";
});


function refillProgressBar() {
  setInterval(() => {
      if ((availableEnergy < maxEnergy) && ((maxEnergy - availableEnergy) >= refillSpeed)) {
          refillBar(refillSpeed);
      }
  }, 10000);
};


function onBeforeUnload(event) {
  const data = {
    "user_id": user_tg_id,
    "balance": $balance.textContent
  };

  fetch('https://78e7-217-25-86-62.ngrok-free.app/exit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {
    console.log('Response from server:', result);
  })
  .catch(error => {
    console.error('Error sending data:', error);
  });
}


// Add the event listener for beforeunload
window.addEventListener('beforeunload', onBeforeUnload);
setBar();
refillProgressBar();
