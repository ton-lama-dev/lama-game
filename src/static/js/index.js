let tg = window.Telegram.WebApp
const $lama = document.getElementById("lama")
const $balance = document.getElementById("balance")

tg.BackButton.show()


function increaseBalance(num) {
  $balance.textContent = Number($balance.textContent) + num;
}


$lama.addEventListener("click", (event) => {
  const rect = $lama.getBoundingClientRect();
  const offsetX = event.clientX - rect.left - rect.width / 2;
  const offsetY = event.clientY - rect.top - rect.height / 2;
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
  plusOne.textContent = "+1";
  plusOne.style.left = `${event.clientX - rect.left + 30}px`;
  plusOne.style.top = `${event.clientY - rect.top + 200}px`;
  $lama.parentElement.appendChild(plusOne);
  increaseBalance(1);
  setTimeout(() => {
    plusOne.remove()
  }, 2000);
});




// progress bar logic
document.addEventListener('DOMContentLoaded', () => {
  const progressBar = document.getElementById('progress-bar');
  const progressText = document.getElementById('progress-text');

  // Example of updating progress
  let progress = 100; // Starting value
  const maxProgress = 1000; // Max value
  const updateProgress = (newProgress) => {
      progress = newProgress;
      const progressPercentage = (progress / maxProgress) * 100;
      progressBar.style.width = `${progressPercentage}%`;
      progressText.textContent = `${progress}/${maxProgress}`;
  };

  // Example: Update progress to 500 after 2 seconds
  setTimeout(() => {
      updateProgress(500);
  }, 2000);
});
