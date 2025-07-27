let seconds = 0;
let timer = null;

function updateTimerDisplay() {
  const hrs = String(Math.floor(seconds / 3600)).padStart(2, '0');
  const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
  const secs = String(seconds % 60).padStart(2, '0');
  const timerEl = document.getElementById('timer-display');
  if (timerEl) {
    timerEl.textContent = `${hrs}:${mins}:${secs}`;
  }
}

function showToast(message) {
  alert(message);
}

document.addEventListener("DOMContentLoaded", function () {
  const gameId = typeof GAME_ID_FROM_TEMPLATE !== 'undefined' ? GAME_ID_FROM_TEMPLATE : null;
  const csrfToken = typeof CSRF_TOKEN !== 'undefined' ? CSRF_TOKEN : null;

  if (!gameId || !csrfToken) {
    console.error("Tracking JS: Missing GAME_ID_FROM_TEMPLATE or CSRF_TOKEN.");
    return;
  }

  const startBtn = document.getElementById("start-btn");
  const stopBtn = document.getElementById("stop-btn");

  if (startBtn) {
    startBtn.addEventListener("click", function () {
      fetch(`/tracking/start/${gameId}/`, {
        method: "POST",
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
        .then(() => {
          startBtn.disabled = true;
          stopBtn.disabled = false;
          timer = setInterval(() => {
            seconds++;
            updateTimerDisplay();
          }, 1000);
        })
        .catch(err => {
          console.error("Error starting tracking:", err);
          showToast("Failed to start tracking.");
        });
    });
  }

if (stopBtn) {
    stopBtn.addEventListener("click", function () {
      clearInterval(timer);

      fetch(`/tracking/stop/${gameId}/`, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ seconds: seconds })
      })
        .then(response => response.json())
        .then(data => {
          console.log("Server responded with:", data);
          if (data && typeof data.total_minutes === 'number') {
            const hours = (data.total_minutes / 60).toFixed(2);
            const userTimeEl = document.getElementById('user-time-played');
            if (userTimeEl) {
              userTimeEl.textContent = hours;
            }
          } else {
            console.warn("Unexpected response from server:", data);
            showToast("Error updating your time.");
          }

          startBtn.disabled = false;
          stopBtn.disabled = true;
          seconds = 0;
          updateTimerDisplay();
        })
        .catch(err => {
          console.error("Error stopping tracking:", err);
          showToast("Failed to stop tracking.");
        });
    });
  }
});