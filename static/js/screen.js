function parseScreenSeries(node) {
  const raw = node.dataset.screenSeries;
  if (!raw) {
    return [];
  }

  try {
    const parsed = JSON.parse(raw);

    if (Array.isArray(parsed)) {
      return parsed.map((item) => ({
        label: item.date || item.label || "",
        value: Number(item.count ?? item.value) || 0,
      }));
    }

    return Object.entries(parsed).map(([label, value]) => ({
      label,
      value: Number(value) || 0,
    }));
  } catch (error) {
    console.warn("Failed to parse screen series", error);
    return [];
  }
}

function renderScreenChart(node) {
  const series = parseScreenSeries(node);
  const maxValue = series.reduce((max, item) => Math.max(max, item.value), 0);

  node.replaceChildren();

  if (!series.length) {
    const emptyState = document.createElement("div");
    emptyState.className = "screen-chart-empty";
    emptyState.textContent = "暂无统计数据";
    node.appendChild(emptyState);
    return;
  }

  series.forEach((item) => {
    const width = maxValue > 0 ? (item.value / maxValue) * 100 : 0;
    const row = document.createElement("div");
    row.className = "screen-chart-row";

    const meta = document.createElement("div");
    meta.className = "screen-chart-meta";

    const label = document.createElement("strong");
    label.className = "screen-chart-label";
    label.textContent = item.label;

    const value = document.createElement("span");
    value.className = "screen-chart-value";
    value.textContent = String(item.value);

    meta.append(label, value);

    const track = document.createElement("div");
    track.className = "screen-chart-track";

    const fill = document.createElement("div");
    fill.className = "screen-chart-fill";
    fill.style.width = `${width}%`;

    track.appendChild(fill);
    row.append(meta, track);
    node.appendChild(row);
  });
}

function updateScreenTimestamp() {
  const timestamp = document.getElementById("screen-timestamp");
  if (!timestamp) {
    return;
  }

  const formatter = new Intl.DateTimeFormat("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });

  timestamp.textContent = formatter.format(new Date());
}

document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector('[data-page="screen-dashboard"]');
  if (!page) {
    return;
  }

  updateScreenTimestamp();
  document.querySelectorAll("[data-screen-series]").forEach(renderScreenChart);
});
