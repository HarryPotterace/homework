const card = document.getElementById("emotion-card");
const input = document.getElementById("pause-input");

if (card) {
  const state = {
    clickCount: 0,
    pauseCount: 0,
    lastMoveAt: Date.now(),
    moveDistances: [],
    lastX: null,
    lastY: null,
  };

  document.addEventListener("click", () => {
    state.clickCount += 1;
  });

  document.addEventListener("mousemove", (event) => {
    if (state.lastX !== null && state.lastY !== null) {
      const dx = event.clientX - state.lastX;
      const dy = event.clientY - state.lastY;
      state.moveDistances.push(Math.sqrt(dx * dx + dy * dy));
      if (state.moveDistances.length > 30) {
        state.moveDistances.shift();
      }
    }
    state.lastX = event.clientX;
    state.lastY = event.clientY;
    state.lastMoveAt = Date.now();
  });

  if (input) {
    let lastKeyAt = Date.now();
    input.addEventListener("keydown", () => {
      const now = Date.now();
      if (now - lastKeyAt > 2000) {
        state.pauseCount += 1;
      }
      lastKeyAt = now;
    });
  }

  const setField = (field, value) => {
    const target = card.querySelector(`[data-field="${field}"]`);
    if (target) {
      target.textContent = value;
    }
  };

  const updateHint = (emotion) => {
    if (emotion === "焦虑") {
      return "建议深呼吸并放慢操作节奏";
    }
    if (emotion === "低落") {
      return "建议先休息，再考虑测评或预约";
    }
    return "保持节奏";
  };

  window.setInterval(async () => {
    const averageDistance = state.moveDistances.length
      ? state.moveDistances.reduce((sum, item) => sum + item, 0) / state.moveDistances.length / 10
      : 0;

    const payload = {
      page_name: card.dataset.pageName || "emotion",
      mouse_speed: averageDistance.toFixed(2),
      click_count: state.clickCount,
      pause_count: state.pauseCount,
    };

    const response = await fetch("/api/behavior", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    card.dataset.uiMode = result.ui_mode;
    setField("emotion", result.emotion);
    setField("mode", result.ui_mode);
    setField("hint", updateHint(result.emotion));
    state.clickCount = 0;
    state.pauseCount = 0;
  }, 5000);
}
